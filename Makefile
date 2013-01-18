PYTHONPATH=`pwd`

all: sandbox.php

sandbox.php: generate.py replacement/*.py php/* functions.py
	python generate.py > sandbox.php
clean:
	rm sandbox.php
test_shell:
	python sandbox.py -v samples/shell_sandbox.php
