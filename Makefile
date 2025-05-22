flake8 = flake8 plugins tests
black = black plugins tests
isort = isort plugins tests


.PHONY: install
install:
	pip install -U --upgrade-strategy=eager pip setuptools wheel
	pip install -U --upgrade-strategy=eager -e . -c requirements.txt -r requirements.dev.txt


.PHONY: format
format:
	$(isort)
	$(black)
	$(flake8)


.PHONY: pep8
pep8:
	$(flake8)
