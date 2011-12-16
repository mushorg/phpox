#!/usr/bin/env python
"""apd_sandbox.py
apd_sandbox.py runs the replaced php function, it is also the main 
function of the sandbox. 
"""
import random
import os
import sys
import time
import subprocess
import threading
import sqlite3
from functools import partial
import getopt
import json

import analysis
import log_sqlite
from lang import lang_detection
import listener
import report.hp_feed
#import classifier.classification


VERSION = '1.0'
DEBUG_LEVEL = 0

def killer(proc): 
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

def analysis_check(sample):
    analyze = 0
    threshold_hr = 10
    conn = sqlite3.connect('sandbox.db')
    curs = conn.cursor()
    curs.execute("SELECT DISTINCT file_md5 FROM botnets")
    filehash = [str(row[0]) for row in curs.fetchall()]
    try:
        #sample analyzed before
        if filehash.index(sample) >= 0:
            curs.execute("SELECT (strftime('%s','now','localtime')-strftime('%s',last_analysis_date)) /3600 AS period_hr "\
                         "FROM botnets WHERE file_md5 = :sample "\
                         "AND last_analysis_date = (SELECT MAX(last_analysis_date) FROM botnets WHERE file_md5 =:sample )",{"sample": sample})
            for row in curs:
                if row[0] > threshold_hr:
                    analyze = 1
    except Exception:
        analyze = 1
        print "Sample file has not been analyzed before."
    curs.close()
    conn.commit()
    conn.close()
    return analyze

def sandbox(script, secs, pre=os.getcwd() + '/'):
    feeder = report.hp_feed.HPFeedClient(pre)
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
        proc_listener = subprocess.Popen(["php", pre + "listener.php"], shell = False)
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
        timer = threading.Timer(secs, killer, (proc_sandbox,))
        timer.start()
        stdout_value = proc_sandbox.communicate()[0]
        timer.cancel()
    except Exception as e:
        proc_listener.kill()
        print "Communication error:", e.message
    else:
        proc_listener.kill()
        analyzer = analysis.DataAnalysis(script, debug=DEBUG_LEVEL)
        botnet = analyzer.analyze(stdout_value)
        logger = log_sqlite.LogSQLite()
        logger.insert(botnet)
        feeder.handle_send('glastopf.sandbox', json.dumps(botnet.todict()))
        feeder.close()
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
        #classifier.classification.classifier_start(opts[1][0])
        sandbox(opts[1][0], secs)
    except(IndexError):
        while True:
            sample_list = os.listdir("samples/")
            random.shuffle(sample_list)
            for sample in sample_list:
                #scriptclass=classifier.classification.classifier_start("samples/get/" + sample)
                if analysis_check(sample) == 1:
                    sandbox("samples/" + sample, secs)
            print "This round is over. Next round will start after 10 minutes... ^.<"
            time.sleep(10*60)
