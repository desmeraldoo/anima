requirements:
	pip install -r requirements.txt

development: requirements
	pip install -r dev-requirements.txt
	pip install -e . --force-reinstall

test:
	python -m pytest -vv --cov src

package:
	del /q dist
	python -m build

upload:
	python -m twine upload dist/*
