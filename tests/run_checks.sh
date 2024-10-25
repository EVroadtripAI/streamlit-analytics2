#!/usr/bin/bash

# Define color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
NO_COLOR='\033[0m' # No Color

# Check that the user is in the tests directory
if [ ! -f "run_checks.sh" ]; then
    echo -e "${RED}Please run this script from the tests directory.${NO_COLOR}"
    exit 1
fi

# Allow script to continue running even if errors occur
set +e

# Initialize a variable to keep track of any failures
any_failures=0

# Generate a timestamp
timestamp=$(date +"%Y-%m-%d_%H-%M-%S")

# Create a markdown file to store the results
filename="test_results_$timestamp.md"
# Temporary file to store errors
error_log="errors_$timestamp.tmp"

# Prepend a go syntax to the file in order to increase readability
echo '```go' > $filename

# Run checks and capture their exit statuses
{
echo "Running Black..."
black ../src --check --verbose 2>&1 | tee -a $error_log || any_failures=1
echo -e "Complete.\n"

echo "Sorting imports with isort..."
isort ../src --check-only --verbose --diff 2>&1 | tee -a $error_log || any_failures=1
echo -e "Complete.\n"

echo "Linting with Flake8..."
flake8 ../src 2>&1 | tee -a $error_log || any_failures=1
echo -e "Complete.\n"

echo "Static type check with mypy..."
mypy ../src --config-file ../mypy.ini 2>&1 | tee -a $error_log || any_failures=1
echo -e "Complete.\n"

echo "Checking for security issues with bandit..."
bandit -r ../src 2>&1 | tee -a $error_log || any_failures=1
echo -e "Complete.\n"

echo "Running pytest with coverage..."
pytest ../ 2>&1 | tee -a $error_log || any_failures=1
echo -e "Complete.\n"

if [ $any_failures -eq 0 ]; then
    echo -e "${GREEN}All checks passed! This would likely pass the GitHub Actions when being pushed to prod. Read the log file for more details.${NO_COLOR}"
else
    echo -e "${RED}Some checks failed. Please review the log file for details.${NO_COLOR}"
fi
} | tee -a $filename

# Check if there are errors and append them to the markdown file
if [ -s $error_log ]; then
    echo -e "\n\n## Errors\n" >> $filename
    cat $error_log >> $filename
fi

echo '```' >> $filename

# Cleanup temporary error log
rm $error_log
