PYTHONPATH=`pwd`

all: sandbox.php

sandbox.php: generate.py replacement/*.py php/* functions.py
	python3 generate.py > sandbox.php
clean:
	rm sandbox.php
test_shell:
	python3 sandbox.py -v samples/shell_sandbox.php
