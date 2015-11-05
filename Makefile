.PHONY: clean-py clean-build

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-py - remove Python file artifacts"

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

clean-py:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
