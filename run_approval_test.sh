#!/bin/bash
poetry run coverage erase
poetry run pytest approval_test/ && \
	poetry run coverage run --branch --source game game_runner.py && \
	poetry run coverage report -m && \
	poetry run coverage html
