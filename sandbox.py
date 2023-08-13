#!/usr/bin/env python3

# Copyright (C) 2023 Lukas Rist
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
import tempfile
import asyncio
import hashlib

from aiohttp import web


class PHPSandbox(object):
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


    async def sandbox(self, script, phpbin="php8.1"):
        self.stdout_value = b""
        if not os.path.isfile(script):
            raise Exception("sample not found: {0}".format(script))
        try:
            cmd = [phpbin, "sandbox.php", script]
            self.proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE)
            stdout, _ = await asyncio.wait_for(self.proc.communicate(), timeout=3)
            self.stdout_value = stdout.decode()
        except Exception as e:
            try:
                self.proc.kill()
            except Exception:
                pass
            print("Error executing the sandbox: {}".format(e))
            # raise e
        return {"stdout": self.stdout_value}


class EchoServer(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        self.transport.write(data)


async def api(request):
    files = await request.post()
    data = files['file'].file.read()
    file_md5 = hashlib.md5(data).hexdigest()
    with tempfile.NamedTemporaryFile(suffix=".php") as f:
        f.write(data)
        f.seek(0)
        sb = PHPSandbox()
        try:
            server = await asyncio.get_event_loop().create_server(EchoServer, "127.0.0.1", 1234)
            ret = await asyncio.wait_for(sb.sandbox(f.name, "php8.1"), timeout=10)
            server.close()
        except KeyboardInterrupt:
            pass
        ret["file_md5"] = file_md5
        return web.json_response(ret)


if __name__ == '__main__':
    app = web.Application()
    app.add_routes([web.post('/', api)])
    web.run_app(app, host='127.0.0.1', port=8088, reuse_port=True)
