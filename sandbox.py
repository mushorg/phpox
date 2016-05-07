#!/usr/bin/env python3

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

import os
import asyncio
from asyncio.subprocess import PIPE

from pprint import pprint

import analysis


class PHPSandbox(object):

    def __init__(self, pre=os.getcwd() + '/', debug_level=0):
        self.pre = pre

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

    @asyncio.coroutine
    def read_process(self):
        while True:
            line = yield from self.proc.stdout.readline()
            if not line:
                break
            else:
                self.stdout_value += line

    @asyncio.coroutine
    def sandbox(self, script):
        if not os.path.isfile(script):
            raise Exception("Sample not found: {0}".format(script))
        # self.fake_listener = listener.FakeListener()
        # self.greenlet = self.fake_listener.run()
        try:
            cmd = ["php5", self.pre + "sandbox.php", script]
            self.proc = yield from asyncio.create_subprocess_exec(*cmd, stdout=PIPE)
            self.stdout_value = b''
            yield from asyncio.wait_for(self.read_process(), timeout=3)
        except Exception as e:
            try:
                self.proc.kill()
            except Exception:
                pass
            print("Error executing the sandbox: {}".format(e))
            # raise e

        print("Sandbox running...")
        analyzer = analysis.DataAnalysis(script)
        botnet = analyzer.analyze(self.stdout_value)
        print("Parsed with sandbox")
        pprint(botnet.todict())
        return botnet


class EchoServer(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        # print('connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        # print('data received: {}'.format(data.decode()))
        self.transport.write(data)

    def connection_lost(self, exc):
        server.close()


if __name__ == '__main__':
    DEBUG_LEVEL = 1
    sb = PHPSandbox(debug_level=DEBUG_LEVEL)
    loop = asyncio.get_event_loop()
    try:
        server = loop.run_until_complete(loop.create_server(EchoServer, '127.0.0.1', 1234))
        fut = asyncio.wait_for(sb.sandbox('bot.php'), timeout=10)
        loop.run_until_complete(fut)
        server.close()
    except KeyboardInterrupt:
        pass
    loop.close()
