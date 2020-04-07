# locate all the files in this directory or below:
FILES=`find . -name '*.py'`

# The command for running mypy:
lint:
	python3 -m mypy $(FILES)

