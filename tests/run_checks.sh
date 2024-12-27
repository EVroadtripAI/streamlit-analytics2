#!/usr/bin/env bash

# Define color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NO_COLOR='\033[0m'

# Exit on undefined variables and pipe failures
set -uo pipefail

# Help function
show_help() {
    echo "Usage: ./run_checks.sh [--fix]"
    echo ""
    echo "Options:"
    echo "  --help    Show this help message"
    echo "  --fix     Run formatters and linters in fix mode"
    echo ""
    echo "Without options, runs in check-only mode"
    exit 0
}

# Parse arguments
FIX_MODE=false
while [[ $# -gt 0 ]]; do
    case $1 in
        --help)
            show_help
            ;;
        --fix)
            FIX_MODE=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            ;;
    esac
done

# Function to print formatted section headers
print_section() {
    echo -e "\n${BLUE}=== $1 ===${NO_COLOR}"
}

# Function to run a check and record its status
run_check() {
    local cmd="$1"
    local name="$2"
    print_section "Running $name"
    if eval "$cmd" 2>&1 | tee -a "$error_log"; then
        echo -e "${GREEN}✓ $name passed${NO_COLOR}"
        return 0
    else
        echo -e "${RED}✗ $name failed${NO_COLOR}"
        return 1
    fi
}

# Check that we're in the tests directory
if [ ! -f "run_checks.sh" ]; then
    echo -e "${RED}Error: Please run this script from the tests directory${NO_COLOR}"
    exit 1
fi

# Define source directory
SRC_DIR="../src/streamlit_analytics2"

# Generate timestamp and filenames
timestamp=$(date +"%Y-%m-%d_%H-%M-%S")
filename="test_results_$timestamp.md"
error_log="errors_$timestamp.tmp"

# Initialize results file with markdown formatting
{
    echo "# Code Quality Check Results"
    echo "Run on: $(date)"
    echo "Mode: $([ "$FIX_MODE" = true ] && echo 'Fix' || echo 'Check')"
    echo ""
    echo '```text'
} > "$filename"

# Initialize error count
any_failures=0

# Ensure virtual environment is activated
if [ -z "${VIRTUAL_ENV:-}" ]; then
    print_section "Setting up virtual environment"
    if command -v uv >/dev/null 2>&1; then
        uv venv
        source .venv/bin/activate
        uv pip install -e "..[dev]"
    else
        echo -e "${RED}Error: uv is not installed. Please install it first.${NO_COLOR}"
        exit 1
    fi
fi

# Run all checks
{
    # Format checks
    if [ "$FIX_MODE" = true ]; then
        run_check "black ${SRC_DIR}" "Black formatting" || any_failures=1
        run_check "isort ${SRC_DIR}" "Import sorting" || any_failures=1
    else
        run_check "black ${SRC_DIR} --check --verbose" "Black formatting" || any_failures=1
        run_check "isort ${SRC_DIR} --check-only --verbose --diff" "Import sorting" || any_failures=1
    fi
    
    # Lint checks
    run_check "flake8 ${SRC_DIR}" "Flake8 linting" || any_failures=1
    
    # Type checks
    run_check "mypy ${SRC_DIR} --config-file ../mypy.ini" "MyPy type checking" || any_failures=1
    
    # Security checks
    run_check "bandit -r ${SRC_DIR}" "Bandit security check" || any_failures=1
    
    # Tests with coverage
    run_check "pytest ../ --cov=${SRC_DIR} --cov-report=term-missing" "Pytest with coverage" || any_failures=1

    # Summary
    echo -e "\n=== Summary ==="
    if [ $any_failures -eq 0 ]; then
        echo -e "${GREEN}✨ All checks passed! Ready for production.${NO_COLOR}"
    else
        echo -e "${RED}❌ Some checks failed. Please review the log for details.${NO_COLOR}"
        if [ "$bla" = false ]; then
            echo -e "${YELLOW}Try running with --fix to automatically fix formatting issues${NO_COLOR}"
        fi
    fi
} 2>&1 | tee -a "$filename"

# Finalize markdown file
echo '```' >> "$filename"

# Add error log if there are any errors
if [ -s "$error_log" ]; then
    {
        echo -e "\n## Detailed Error Log"
        echo '```text'
        cat "$error_log"
        echo '```'
    } >> "$filename"
fi

# Cleanup
rm -f "$error_log"

# Optional: Open the results file
if command -v code >/dev/null 2>&1; then
    code "$filename"
elif command -v open >/dev/null 2>&1; then
    open "$filename"
fi

exit $any_failures