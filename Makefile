flake8 = flake8 inmanta_plugins tests
black = black inmanta_plugins tests
isort = isort inmanta_plugins tests


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
