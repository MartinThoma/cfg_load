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
	python3 setup.py sdist bdist_wheel && twine upload dist/*
