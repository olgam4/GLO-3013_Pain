default: install

run: env
	. env/bin/activate; \
	python src/baseStation.py -m remote

test: env update
	. env/bin/activate; \
	nosetests

coverage: env update
	. env/bin/activate; \
	nosetests --with-coverage --cover-package=src --cover-erase --cover-inclusive &> coverage.txt

install: env update

update: env
	. env/bin/activate; \
	pip install -r requirements.txt

env:
	python3.7 -m venv env
	. env/bin/activate; \
	pip install -U pip

.PHONY: clean
clean:
	rm -r env/
