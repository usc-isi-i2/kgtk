# locate all the files in this directory or below:
FILES=`find . -name '*.py'`

# The command for running mypy:
lint:
	python3 -m mypy $(FILES)

requirements:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pip install -r requirements-full.txt

mkdocs:
	mkdocs build --clean
	mkdocs serve -a localhost:8080

precommit:
	tox

clean-build:
	rm -rf kgtk*.egg-info
	python setup.py clean --all

update-version:
	python3 kgtk/utils/updateversion.py --show-changes=True $(FILES)

unittest:
	cd tests && python3 -m unittest discover --verbose

coverage:
	cd kgtk/tests && coverage run --source=kgtk -m unittest discover --verbose

download-spacy-model:
	python3 -m spacy download en_core_web_sm
