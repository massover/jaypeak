lint:
	pep8 . --exclude=venv,config.py,jaypeak/yodlee/__init__.py
	pep8 config.py jaypeak/yodlee/__init__.py --ignore=E501

test:
	py.test jaypeak/yodlee/tests.py jaypeak/transactions/tests.py

coverage:
	py.test --cov=jaypeak/yodlee jaypeak/yodlee/tests.py
