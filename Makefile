all: build install

.PHONY: build install test docs distclean dist upload

install:
	python3 -m pip install .

test:
	python3 -m pytest --record-mode=once --cov-report term --cov=talbot tests/

test_no_vcr:
	python3 -m pytest --disable-recording --cov-report term --cov=talbot tests/

docs:
	cd docs;\
	make html

opendocs:
	open docs/_build/html/index.html

clean:
	rm -rf dist/* build/*

dist:
	python3 -m build --sdist --wheel

register:
	python3 setup.py register

upload_test:
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload:
	python3 -m twine upload dist/*
