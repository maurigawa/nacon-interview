venv:
	@sudo apt install python3.11 python3.11-venv
	@python3.11 -m venv .venv

install:
	@pip install -r requirements.txt

code-format:
	@ruff format .

code-check:
	@ruff check .
