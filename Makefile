all: apd_sandbox.php

apd_sandbox.php: apd_generate.py replacement/*.py
	python apd_generate.py > apd_sandbox.php
clean:
	rm apd_sandbox.php
