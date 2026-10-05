.PHONY: install run test lint

install:
	python -m pip install -e ".[dev]"

run:
	streamlit run app.py

test:
	pytest -q

lint:
	ruff check .

