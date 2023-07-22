"""Config file required to support Solark Monitor."""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os

# Application Variables
app_dict = {
    "author": "Aaron Melton <aaron@aaronmelton.com>",
    "date": "2023-07-22",
    # pylint: disable=line-too-long
    "desc": "A Python script to read memory register(s) from Sol-Ark Inverters and insert them into a database.",
    "name": "solark_monitor.py",
    "title": "Solark Monitor",
    "url": "https://github.com/aaronmelton/solark_monitor",
    "version": "v0.5.0",
}

# Logging Variables
log_dict = {"level": os.environ.get("LOG_LEVEL"), "path": os.environ.get("LOG_PATH")}

# Modbus Variables
modbus_dict_ser = {
    "method": "rtu",
    "port": "/dev/ttyUSB0",
    "baudrate": 9600,
    "timeout": 3,
    "parity": "N",
    "stopbits": 1,
    "bytesize": 8,
}
modbus_dict_tcp = {
    "method": "tcp",
    "hostname": "solarkinv",
    "port": "502",
    "timeout": 5,
}

# Database Variables
db_dict = {
    "host": os.environ.get("DB_HOST"),
    "username": os.environ.get("DB_USERNAME"),
    "password": os.environ.get("DB_PASSWORD"),
    "schema": os.environ.get("DB_SCHEMA"),
}
