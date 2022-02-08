build:
	python -m build

sdist:
	python3 setup.py sdist

.PHONY: build sdist
