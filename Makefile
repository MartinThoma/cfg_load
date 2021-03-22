maint:
	pip install -r requirements/dev.txt
	pre-commit autoupdate && pre-commit run --all-files
	pip-compile -U setup.py -o requirements/prod.txt
	pip-compile -U requirements/ci.in
	pip-compile -U requirements/dev.in

clean:
	python setup.py clean --all
	pyclean .
	rm -rf tests/reports .tox build dist __pycache__ cfg_load.egg-info tests/__pycache__ cfg_load/__pycache__
	rm -rf examples/ignore_image.jpg examples/ignore_zip.zip

stats:
	make clean
	cloc .

test:
	tox

upload:
	make clean
	python setup.py sdist bdist_wheel && twine upload dist/*
