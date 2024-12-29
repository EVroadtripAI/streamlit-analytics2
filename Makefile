.PHONY: clean_for_tests

## Clean up files automatically to make them more likely to pass linting, formatting, etc. tests
clean_for_tests:
	black src/
	isort src/
	flake8 src/
	mypy src/
