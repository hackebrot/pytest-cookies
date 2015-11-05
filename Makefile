.PHONY: clean-py

help:
	@echo "clean-py - remove Python file artifacts"

clean-py:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
