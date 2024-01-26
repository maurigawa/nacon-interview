## Prepare development environment 

### on Ubuntu

Create a python 3.11 virtual environment
- `sudo apt install python3.11 python3.11-venv`
- `python3.11 -m venv .venv`

Activate your virtual environment
- `source .venv/bin/activate`

Install needed requirements
- `pip install -r requirements.txt`


## Launch local service

`make run`

You can now access the service documentation (swagger) at:

http://127.0.0.1:8000/docs


## Run tests/linter

`make tests` to run tests.

`make code-format` to format python files.
