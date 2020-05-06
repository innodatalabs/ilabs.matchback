.PHONY: docs test

all: wheel

export PATH := $(PATH):/depot_tools
ON_TAG := $(shell git tag --points-at HEAD)

test:
	pip install pytest
	pytest

wheel: test
	rm -rf wheelhouse
	mkdir wheelhouse
	pip wheel -v --wheel-dir=wheelhouse .

publish: wheel
	pip install twine
	twine upload wheelhouse/*.whl -u __token__ -p $(PYPI_TOKEN)

maybe_publish: wheel
ifneq ($(ON_TAG),)
	pip install twine
	twine upload wheelhouse/*.whl -u __token__ -p $(PYPI_TOKEN)
endif
