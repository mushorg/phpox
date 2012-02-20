#!/usr/bin/env python

import os
import sys
import subprocess
import threading
import sqlite3
import getopt
import json

import analysis
import log_sqlite
from lang import lang_detection
import hpfeed.hpf_feed as hpf_feed


class PHPSandbox(object):

    def __init__(self, pre=os.getcwd() + '/'):
        self.pre = pre
        self.DEBUG_LEVEL = 0
        self.feeder = hpf_feed.HPFeedClient(pre)

    def killer(self, proc):
        try:
            proc.kill()
        except OSError:
            pass

    def php_tag_check(self, script):
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

    def detect_language(self, script):
        lang_classifier = lang_detection.LangClassifier()
        language = lang_classifier.classify(open(script, "r").read())
        return language

    def analysis_check(self, sample):
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

    def sandbox(self, script, secs):
        if self.DEBUG_LEVEL > 0:
            print "\n PRE: ", self.pre, "\n"
            stderr_opt = None
        else:
            stderr_opt = subprocess.PIPE

        try:
            if self.DEBUG_LEVEL > 0:
                print self.pre + "listener.php"
            proc_listener = subprocess.Popen(["php5-cgi", self.pre + "listener.php"],
                                             shell=False)
        except Exception as e:
            print "Error running the socket listener:", e
        else:
            if self.DEBUG_LEVEL > 0:
                print "Listener running..."
        try:
            proc_sandbox = subprocess.Popen(["php5-cgi", self.pre + "apd_sandbox.php", script],
                    shell=False,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=stderr_opt,
                    )
        except Exception as e:
            print "Error executing the sandbox:", e.message
        else:
            if self.DEBUG_LEVEL > 0:
                print "Sandbox running..."
        stdout_value = ""
        try:
            timer = threading.Timer(secs, self.killer, (proc_sandbox,))
            timer.start()
            stdout_value = proc_sandbox.communicate()[0]
            timer.cancel()
        except Exception as e:
            proc_listener.kill()
            print "Communication error:", e.message
        else:
            proc_listener.kill()
            analyzer = analysis.DataAnalysis(script, debug=self.DEBUG_LEVEL)
            botnet = analyzer.analyze(stdout_value)
            logger = log_sqlite.LogSQLite()
            logger.insert(botnet)
            self.feeder.publish('glastopf.sandbox',
                                    json.dumps(botnet.todict()))
            if self.DEBUG_LEVEL > 0:
                print "Parsed with sandbox"
            return botnet

if __name__ == '__main__':
    sb = PHPSandbox()
    DEBUG_LEVEL = 0
    opts = getopt.getopt(sys.argv[1:], "v", [])
    for i in opts[0]:
        if i[0] == '-v':
            DEBUG_LEVEL += 1
    try:
        sb.sandbox(opts[1][0], secs=10)
    except(IndexError):
        print "Specify the file to analyze..."
