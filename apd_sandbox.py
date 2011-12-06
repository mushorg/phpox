#!/usr/bin/env python

import random
import os
import sys
import time
import subprocess
import threading
from functools import partial
import classifier.classification

import analysis
import log_sqlite
from lang import lang_detection
import listener

import getopt

VERSION = '1.0'
DEBUG_LEVEL = 0

def killer(proc, secs):
    time.sleep(secs)
    try:
        proc.kill()
    except OSError:
        pass

def php_tag_check(script):
    check_file = open(script, "r+")
    file_content = check_file.read()
    if not "<?" in file_content:
        file_content = "<?php" + file_content
        raw_input("tag fixed!")
    if not "?>" in file_content:
        file_content = file_content + "?>"
    check_file.write(file_content)
    check_file.close()
    return script

def detect_language(script):
    lang_classifier = lang_detection.LangClassifier()
    language = lang_classifier.classify(open(script, "r").read())
    return language

def sandbox(script, secs, pre=os.getcwd() + '/'):
    #language = detect_language(script)
    #pre = os.getcwd().rsplit("/",1)[0] + "/"
    if DEBUG_LEVEL > 0:
        print "\n PRE: ", pre, "\n"
        stderr_opt = None
    else:
        stderr_opt = subprocess.PIPE

        #if language == "php":
            #php_tag_check(script)
    try:
        """fake_listener = listener.FakeListener()
        server = fake_listener.main(script)
        t = threading.Thread(target=server.serve_forever)
        t.setDaemon(True)
        t.start()"""
        if DEBUG_LEVEL > 0:
            print pre+"listener.php"
        proc_listener = subprocess.Popen(["php", pre+"listener.php"], shell = False)
    except Exception as e:
        print "Error running the socket listener:", e
    else:
        if DEBUG_LEVEL > 0:
            print "Listener running..."
    try:
        proc_sandbox = subprocess.Popen(["php", pre+"apd_sandbox.php", script], 
                shell = False,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=stderr_opt,
                )
    except Exception as e:
        print "Error executing the sandbox:", e.message
    else:
        if DEBUG_LEVEL > 0:
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
        analyzer = analysis.DataAnalysis(script, debug=DEBUG_LEVEL)
        botnet = analyzer.analyze(stdout_value)
        logger = log_sqlite.LogSQLite()
        logger.insert(botnet)
        #print language
        #print stdout_value
        if DEBUG_LEVEL > 0:
            print "Parsed with sandbox"
        return botnet
    
if __name__ == '__main__':
    if DEBUG_LEVEL > 0:
        print "\nPHP sandbox version: %s\n" % VERSION
    secs = 10

    opts = getopt.getopt(sys.argv[1:], "v", [])
    for i in opts[0]:
        if i[0] == '-v' :
            DEBUG_LEVEL += 1

    try:
        classifier.classification.classifier_start(opts[1][0])
        sandbox(opts[1][0], secs)
    except(IndexError):
        sample_list = os.listdir("samples/get")
        random.shuffle(sample_list)
        for sample in sample_list:
            scriptclass=classifier.classification.classifier_start("samples/get/" + sample)
            sandbox("samples/get/" + sample, secs)
            
            raw_input("Enter to continue")

