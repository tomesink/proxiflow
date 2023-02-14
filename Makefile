
PYTHON = python3
PIP = pip3
NAME=adprep

# The @ makes sure that the command itself isn't echoed in the terminal
help:
	@echo "---------------HELP-----------------"
	@echo "To test the project type make test"
	@echo "To run the project type make run"
	@echo "------------------------------------"

python-version:
	${PYTHON} --version
	${PIP} --version	

run:
	${PYTHON} -m ${NAME}

test:
	${PYTHON} -m pytest -v