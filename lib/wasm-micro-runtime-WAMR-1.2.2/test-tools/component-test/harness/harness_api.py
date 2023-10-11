#
# Copyright (C) 2019 Intel Corporation.  All rights reserved.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
#

import os
import shutil
import subprocess
import json
import time

from framework import test_api
from framework.test_utils import *

output = "output.txt"

def start_env():
    os.system("./start.sh")

def stop_env():
    os.system("./stop.sh")
    time.sleep(0.5)
    os.chdir("../") #reset path for other cases in the same suite

def check_is_timeout():
    line_num = 0
    with open(output, 'r') as ft:
        lines = ft.readlines()

        for line in reversed(lines):
            if line[:36] == "--------one operation begin.--------":
                break
            line_num = line_num + 1

    return lines[-(line_num)] == "operation timeout"

def parse_ret(file):
    with open(file, 'a') as ft:
        ft.writelines("\n")
        ft.writelines("--------one operation finish.--------")
        ft.writelines("\n")
    ft = open(file, 'r')
    for line in reversed(ft.readlines()):
        if line[:16] == "response status ":
            ret = line[16:]
            ft.close()
            return int(ret)

def run_host_tool(cmd, file):
    with open(file, 'a') as ft:
        ft.writelines("--------one operation begin.--------")
        ft.writelines("\n")
    os.system(f"{cmd} -o{file}")
    return -1 if (check_is_timeout() == True) else parse_ret(file)

def install_app(app_name, file_name):
    return run_host_tool(
        f"./host_tool -i {app_name} -f ../test-app/{file_name}", output
    )

def uninstall_app(app_name):
    return run_host_tool(f"./host_tool -u {app_name}", output)

def query_app():
    return run_host_tool("./host_tool -q ", output)

def send_request(url, action, payload):
    if (payload is None):
        return run_host_tool(f"./host_tool -r {url} -A {action}", output)
    else:
        return run_host_tool(f"./host_tool -r {url} -A {action} -p {payload}", output)

def register(url, timeout, alive_time):
    return run_host_tool(
        f"./host_tool -s {url} -t {str(timeout)} -a {str(alive_time)}", output
    )

def deregister(url):
    return run_host_tool(f"./host_tool -d {url}", output)

def get_response_payload():
    line_num = 0
    with open(output, 'r') as ft:
        lines = ft.readlines()

        for line in reversed(lines):
            if line[:16] == "response status ":
                break
            line_num = line_num + 1

        payload_lines = lines[-(line_num):-1]
    return payload_lines

def check_query_apps(expected_app_list):
    if (check_is_timeout() == True):
        return False
    json_lines = get_response_payload()
    json_str = " ".join(json_lines)
    json_dict = json.loads(json_str)
    app_list = [value for key, value in json_dict.items() if key[:6] == "applet"]
    return sorted(app_list) == sorted(expected_app_list)

def check_response_payload(expected_payload):
    if (check_is_timeout() == True):
        return False
    json_lines = get_response_payload()
    json_str = " ".join(json_lines)

    json_dict = json.loads(json_str) if (json_str.strip() != "") else {}
    return json_dict == expected_payload

def check_get_event():
    line_num = 0
    with open(output, 'r') as ft:
        lines = ft.readlines()

        for line in reversed(lines):
            if line[:16] == "response status ":
                break
            line_num = line_num + 1

        payload_lines = lines[-(line_num):-1]
    return payload_lines[1][:17] == "received an event"
