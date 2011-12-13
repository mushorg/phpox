PYTHONPATH=`pwd`

all: apd_sandbox.php

apd_sandbox.php: apd_generate.py replacement/*.py php/* apd_functions.py
	python apd_generate.py > apd_sandbox.php
clean:
	rm apd_sandbox.php
test_shell:
	python apd_sandbox.py -v samples/shell_sandbox.php
