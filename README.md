# nacon-interview
Technical test for Nacon interview


## Clone repository

### HTTPS:
`git clone https://github.com/maurigawa/nacon-interview.git`

### SSH:

If not already done, [create a ssh key and add it to your github repository](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

Then:

`git clone git@github.com:maurigawa/nacon-interview.git`



## Prepare development environment (Backend) 

`cd nacon-interview/services/game-content`

### on Ubuntu

Create a python 3.11 virtual environment
- `sudo apt install python3.11 python3.11-venv`
- `python3.11 -m venv .venv`

Activate your virtual environment
- `source .venv/bin/activate`

Install needed requirements
- `pip install -r requirements.txt`


## Launch local service

`cd app`

`uvicorn main:app --reload`

You can now access the service documentation (swagger) at:

http://127.0.0.1:8000/docs

 

