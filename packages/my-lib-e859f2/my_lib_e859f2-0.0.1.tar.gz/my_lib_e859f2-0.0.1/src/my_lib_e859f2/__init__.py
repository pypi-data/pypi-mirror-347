# SPDX-FileCopyrightText: 2025-present Adrian Herscu <adrian.herscu@gmail.com>
#
# SPDX-License-Identifier: MIT
import requests

def ping():
    response = requests.get("https://httpbin.org/get")
    return response.status_code
