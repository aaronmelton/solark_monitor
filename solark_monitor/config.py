"""solark_monitor Config Class."""

# !/usr/bin/env python
# -*- coding: utf-8 -*-
#


from dataclasses import dataclass
from datetime import datetime
from os import environ as os_environ


@dataclass
class Config:
    """Class for Application variables."""

    def __init__(self):
        """Application Variables."""
        self.app_dict = {
            "author": "Aaron Melton <aaron@aaronmelton.com>",
            "date": "2025-11-06",
            "desc": "A Python script to read memory register(s) from Sol-Ark Inverters and insert them into a database.",
            "title": "solark_monitor",
            "url": "https://github.com/aaronmelton/solark_monitor",
            "version": "0.7.1",
        }

        # Logging Variables
        self.log_dict = {
            "filename": f"""{os_environ.get("SOLARK_LOG_PATH", "./log/")}{self.app_dict["title"]}_{datetime.now().strftime("%Y%m%d")}.log""",
            "level": os_environ.get("SOLARK_LOG_LEVEL", "INFO"),
            "path": os_environ.get("SOLARK_LOG_PATH", "./log/"),
        }

        # Modbus Variables
        self.modbus_dict_ser = {
            "method": "rtu",
            "port": "/dev/ttyUSB0",
            "baudrate": 9600,
            "timeout": 3,
            "parity": "N",
            "stopbits": 1,
            "bytesize": 8,
        }
        self.modbus_dict_tcp = {
            "method": "tcp",
            "hostname": os_environ.get("SOLARK_INV_HOSTNAME"),
            "port": "502",
            "timeout": 5,
        }

        # Database Variables
        self.db_dict = {
            "host": os_environ.get("SOLARK_DB_HOSTNAME"),
            "username": os_environ.get("SOLARK_DB_USERNAME"),
            "password": os_environ.get("SOLARK_DB_PASSWORD"),
            "schema_name": os_environ.get("SOLARK_DB_SCHEMA"),
            "table_name": os_environ.get("SOLARK_DB_TABLE"),
        }
