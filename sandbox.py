#!/usr/bin/env python

# Copyright (C) 2012  Lukas Rist
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import os
import sys
import subprocess
import threading
import sqlite3
import getopt
import json

from pprint import pprint
from ConfigParser import ConfigParser

import analysis
import log_sqlite
import listener

from lang import lang_detection
import hpfeed.hpf_feed as hpf_feed


class PHPSandbox(object):

    def __init__(self, pre=os.getcwd() + '/', debug_level=0):
        self.pre = pre
        self.conf_parser = ConfigParser()
        self.conf_parser.read(self.pre + "sandbox.cfg")
        if self.conf_parser.get("hpfeed", "enabled") == "True":
            self.feeder = hpf_feed.HPFeedClient(pre)
        self.DEBUG_LEVEL = debug_level

    def killer(self, proc):
        try:
            proc.kill()
        except OSError:
            print "Failed to kill process:", proc

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
        if not os.path.isfile(script):
            raise Exception("Sample not found: {0}".format(script))
        if self.DEBUG_LEVEL > 0:
            stderr_opt = None
        else:
            stderr_opt = subprocess.PIPE
        self.fake_listener = listener.ListenerThread()
        self.fake_listener.start()
        try:
            proc_sandbox = subprocess.Popen(["php5",
                                self.pre + "sandbox.php", script],
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
            self.fake_listener.stop()
            print "Communication error:", e.message
        else:
            self.fake_listener.stop()
            analyzer = analysis.DataAnalysis(script, debug=self.DEBUG_LEVEL)
            botnet = analyzer.analyze(stdout_value)
            logger = log_sqlite.LogSQLite()
            botnet.id = logger.insert(botnet)
            if self.conf_parser.get("hpfeed", "enabled") == "True":
                self.feeder.connect()
                self.feeder.publish('glastopf.sandbox',
                                    json.dumps(botnet.todict()))
                self.feeder.close()
            if self.DEBUG_LEVEL > 0:
                print "Parsed with sandbox"
                pprint(botnet.todict())
            return botnet

if __name__ == '__main__':
    DEBUG_LEVEL = 0
    opts = getopt.getopt(sys.argv[1:], "v", [])
    for i in opts[0]:
        if i[0] == '-v':
            DEBUG_LEVEL += 1
    sb = PHPSandbox(debug_level=DEBUG_LEVEL)
    try:
        sb.sandbox(opts[1][0], secs=30)
    except(IndexError):
        print "Specify the file to analyze..."
    except:
        raise
        sb.fake_listener.stop()
