PYTHON = python3
PIP = pip3
LINTER = flakeheaven
FORMATTER = black
NAME=prepflow
DOC=docs
VERSION=0.1.2


# The @ makes sure that the command itself isn't echoed in the terminal
help:
	@echo "---------------HELP-----------------"
	@echo "To test the project type make test"
	@echo "To run the project type make run"
	@echo "------------------------------------"

python-version:
	@${PYTHON} --version
	@${PIP} --version	
	@${FORMATTER} --version
	@${LINTER} --version

format:
	${FORMATTER} ${NAME}

lint:
	${PYTHON} -m $(LINTER) lint prepflow

test:
	${PYTHON} -m pytest -v

doc:
	# @#${PYTHON} -m pdoc --html --output-dir docs ${NAME}
	sphinx-apidoc -f -o ${DOC}/source ${NAME} --ext-autodoc && cd ${DOC} && make html

html:
	cd ${DOC} && make html

install:
	${PYTHON} -m pip install .

build:
	${PYTHON} -m build

run:
	@${PYTHON} -m ${NAME} --config-file=tests/data/config.yaml --input-file=tests/data/input.csv --output-file=tests/data/output.csv

deploy_test:
	${PYTHON} -m twine upload --repository testpypi dist/prepflow-${VERSION}.tar.gz --verbose

check_build:
	twine check dist/*

clean:
	@rm -rf build dist *.egg-info
	