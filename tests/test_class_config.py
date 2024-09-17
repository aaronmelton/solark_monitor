"""Test class Config."""

# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# pylint: disable=invalid-name, duplicate-code

from re import match as re_match

from solark_monitor.config import Config


def test_config():
    """Test config.py"""
    # Application Variables
    config = Config()
    assert config.app_dict["author"] == "Aaron Melton <aaron@aaronmelton.com>"
    assert re_match("\\d{4}(-\\d{2}){2}", "2024-03-21")
    assert (
        config.app_dict["desc"]
        == "A Python script to read memory register(s) from Sol-Ark Inverters and insert them into a database."
    )
    assert config.app_dict["title"] == "solark_monitor"
    assert config.app_dict["url"] == "https://github.com/aaronmelton/solark_monitor"
    assert re_match("\\d{1,2}(\\.\\d{1,2}){2}", config.app_dict["version"])
