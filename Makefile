.PHONY: init run

init:
	virtualenv -p python3 env
	env/bin/pip install -U pip wheel setuptools
	env/bin/pip install -r requirements.txt

scrape:
	env/bin/python scrape.py

