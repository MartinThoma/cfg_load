clean:
	pyclean .
	rm -rf tests/reports .tox build dist cfg_load.egg-info tests/__pycache__ cfg_load/__pycache__
	rm -rf examples/ignore_image.jpg examples/ignore_zip.zip

stats:
	make clean
	cloc .

test:
	tox

upload:
	python setup.py sdist bdist_wheel
	twine upload dist/*
