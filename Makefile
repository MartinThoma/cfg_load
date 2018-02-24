clean:
	pyclean .
	rm -rf tests/reports .tox build dist cfg_load.egg-info tests/__pycache__ cfg_load/__pycache__

stats:
	make clean
	cloc .

test:
	tox
