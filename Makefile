PYTHON = python3
PIP = pip3
LINTER = ruff
FORMATTER = black
NAME=proxiflow
DOC=docs

.PHONY = test

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
	$(LINTER) check ${NAME}

typecheck:
	mypy proxiflow

test:
	${PYTHON} -m pytest -v

doc:
	@sphinx-apidoc -f -o ${DOC}/source ${NAME} --ext-autodoc && cd ${DOC}
	@sphinx-build ${DOC}/source ${DOC}/build

install:
	${PYTHON} -m pip install .[dev,docs]

build:
	${MANAGER} build

dev:
	@${PYTHON} -m ${NAME} --config-file=tests/data/config.yaml --input-file=tests/data/input.csv --output-file=tests/data/output.csv

publish-test:
	${MANAGER} publish --repository test-pypi

publish:
	${MANAGER} publish

check-build:
	twine check dist/*

clean:
	@rm -rf build dist *.egg-info
	
