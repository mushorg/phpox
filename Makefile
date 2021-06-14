PYTHONPATH=`pwd`

all: sandbox.php

sandbox.php: generate.py replacement/*.py php/* functions.py
	python3 generate.py > sandbox.php

clean:
	rm sandbox.php
