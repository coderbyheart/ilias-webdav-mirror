all: install 

install: remove-deps install-deps

install-virtualenv:
	wget https://raw.github.com/pypa/virtualenv/master/virtualenv.py -O ./virtualenv.py
	python2 ./virtualenv.py VIRTUALENV

install-deps: install-virtualenv
	. VIRTUALENV/bin/activate; pip install -U Python_WebDAV_Library

remove-deps:
	-rm -rf vendor
	-rm -rf VIRTUALENV