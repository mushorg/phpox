#!/usr/bin/env python

# Copyright (C) 2015 Lukas Rist
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

from gevent.monkey import patch_all
patch_all()

import os

import gevent
import gevent.timeout
import gevent.subprocess

from pprint import pprint
from ConfigParser import ConfigParser

import analysis
import listener


class PHPSandbox(object):

    def __init__(self, pre=os.getcwd() + '/', debug_level=0):
        self.pre = pre
        self.conf_parser = ConfigParser()
        self.conf_parser.read(self.pre + "sandbox.cfg")
        self.DEBUG_LEVEL = debug_level
        self.greenlet = None
        self.fake_listener = None

    @classmethod
    def php_tag_check(cls, script):
        with open(script, "r+") as check_file:
            file_content = check_file.read()
            if "<?" not in file_content:
                file_content = "<?php" + file_content
            if "?>" not in file_content:
                file_content += "?>"
            check_file.write(file_content)
        return script

    def sandbox(self, script, secs):
        if not os.path.isfile(script):
            raise Exception("Sample not found: {0}".format(script))
        self.fake_listener = listener.FakeListener()
        self.greenlet = self.fake_listener.run()
        try:
            proc_sandbox = gevent.subprocess.Popen(
                [
                    "php5",
                    self.pre + "sandbox.php", script
                ],
                stdout=gevent.subprocess.PIPE,
                stderr=gevent.subprocess.PIPE,
                shell=False
            )
        except Exception as e:
            proc_sandbox = None
            print("Error executing the sandbox:", e.message)
        else:
            if self.DEBUG_LEVEL > 0:
                print("Sandbox running...")
        try:
            with gevent.Timeout(secs):
                stdout_value = ""
                while True:
                    try:
                        stdout_value += proc_sandbox.stdout.readline()
                    except gevent.timeout.Timeout:
                        break
                    gevent.sleep(0.1)
            proc_sandbox.kill()
        except Exception as e:
            self.greenlet.kill()
            print("Communication error:", e.message)
        else:
            self.greenlet.kill()
            analyzer = analysis.DataAnalysis(script, debug=self.DEBUG_LEVEL)
            botnet = analyzer.analyze(stdout_value)
            if self.DEBUG_LEVEL > 0:
                print("Parsed with sandbox")
                pprint(botnet.todict())
            return botnet

if __name__ == '__main__':
    DEBUG_LEVEL = 1
    sb = PHPSandbox(debug_level=DEBUG_LEVEL)
    try:
        sb.sandbox('samples/irc_bot.php', secs=10)
    except IndexError:
        print("Specify the file to analyze...")
        raise
    except:
        if sb.greenlet:
            sb.greenlet.kill()
        raise
