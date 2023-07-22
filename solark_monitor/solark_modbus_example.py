"""A Python list with the Sol-Ark Memory Registers."""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# THIS FILE IS INTENTIONALLY MISSING VALUES
#
# You'll need to obtain the Modbus register addresses from Sol-Ark (or you may
# find them published online) and populate register_table with these values
# following the format below:

register_table = [
    {
        "address": 186,
        "description": "PV1 input power",
        "key": "pv1_input_power",
        "permission": "R",
        "signed": False,
        "bits": 16,
        "range": None,
        "multiplier": None,
        "unit": "watt",
        "pull": True,
    },
    {
        "address": 187,
        "description": "PV2 input power",
        "key": "pv2_input_power",
        "permission": "R",
        "signed": False,
        "bits": 16,
        "range": None,
        "multiplier": None,
        "unit": "watt",
        "pull": True,
    },
]
