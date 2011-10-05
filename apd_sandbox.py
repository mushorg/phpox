#!/usr/bin/env python

import random
import os
import sys
import time
import subprocess
import threading
from functools import partial

import analysis
import log_sqlite
from lang import lang_detection

VERSION = '1.0'

def killer(proc, secs):
    time.sleep(secs)
    try:
        proc.kill()
    except OSError:
        pass

def php_tag_check(script):
    file = open(script, "r+")
    file_content = file.read()
    if not "<?" in file_content:
        file_content = "<?php" + file_content
        raw_input("tag fixed!")
    if not "?>" in file_content:
        file_content = file_content + "?>"
    file.write(file_content)
    file.close()
    return script

def detect_language(script):
    lang_classifier = lang_detection.LangClassifier()
    language = lang_classifier.classify(open(script, "r").read())
    return language

def sandbox(script, secs):
    language = detect_language(script)
    if language == "php":
        php_tag_check(script)
    try:
        proc_listener = subprocess.Popen(["php", "listener.php"], shell = False)
    except Exception as e:
        print "Error running the socket listener:", e.message
    else:
        print "Listener running..."
    #script = php_tag_check(script)
    try:
        proc_sandbox = subprocess.Popen(["php", "apd_sandbox.php", script], 
                shell = False,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                )
    except Exception as e:
        print "Error executing the sandbox:", e.message
    else:
        print "Sandbox running..."
    stdout_value = ""
    try:
        threading.Thread(target=partial(killer, proc_sandbox, secs)).start()
        stdout_value = proc_sandbox.communicate()[0]
    except Exception as e:
        proc_listener.kill()
        print "Communication error:", e.message
    else:
        proc_listener.kill()
        analyzer = analysis.DataAnalysis(script)
        botnet = analyzer.analyze(stdout_value)
        logger = log_sqlite.LogSQLite()
        logger.insert(botnet)
        print language
        #print stdout_value
        print "Parsed with sandbox"
    
if __name__ == '__main__':
    print "\nPHP sandbox version: %s\n" % VERSION
    secs = 3
    try:
        sandbox(sys.argv[1], secs)
    except(IndexError):
        list = os.listdir("samples/get")
        random.shuffle(list)
        for sample in list:
            print sample
            sandbox("samples/get/" + sample, secs)
            raw_input("Enter to continue")