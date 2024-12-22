# Contributing to Streamlit-Analytics2

We appreciate your interest in contributing to Streamlit-Analytics2! This guide will walk you through the process of setting up your development environment and submitting a pull request.

## Getting Started

1. Fork the repository on GitHub.
2. Clone your forked repository to your local machine.
   ```sh
   git clone https://github.com/444B/streamlit-analytics2.git
   cd streamlit-analytics2
   ```
3. Create a new branch for your changes. Make sure to start the branch name with "test/".
   ```sh
   git checkout -b test/your-feature-name
   ```
4. Set up your development environment (see below).
5. Make your changes and test them locally.
6. Commit your changes and push them to your forked repository.
   ```sh
   git add .
   git commit -m "Your commit message"
   git push origin test/your-feature-name
   ```
7. Open a pull request on the main repository.

## Setting Up Your Development Environment

1. Make sure you have Python 3.12.x installed.
2. Install pipenv.
   ```sh 
   pip install --user pipenv
   ```
3. Create a pipenv environment and install dependencies.
   ```sh
   pipenv --python 3.12
   pipenv install --dev
   ```
4. Activate the virtual environment.
   ```sh
   pipenv shell
   pipenv update
   ```
5. Run a minimal example to ensure everything is set up correctly.
   ```sh
   streamlit run examples/minimal.py
   ```

## Before Submitting Your Pull Request

1. Make sure your code follows the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide.
2. Run the provided checks to ensure your code is compliant.
   ```sh
   cd tests/
   chmod +x /run_checks.sh
   ./run_check.sh
   ```
   This will perform formatting and checks using black, isort, flake8, mypy, bandit, and pytest.

## Reporting Issues

If you encounter a bug or have a feature request, please submit an issue on the [GitHub issue tracker](https://github.com/444B/streamlit-analytics2/issues/new/choose). Be sure to provide a clear description and steps to reproduce the issue if applicable.

## License

By contributing to this project, you agree that your contributions will be licensed under the same [license](LICENSE.md) as the project.

Thank you for contributing to Streamlit-Analytics2! Your efforts help make this project better for everyone.
