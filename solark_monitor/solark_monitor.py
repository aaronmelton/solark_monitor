"""Sol-Ark Monitor."""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

import argparse
import datetime
import logging
import sys
import time
import MySQLdb

from pymodbus.client import ModbusSerialClient, ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
# edit the solark_modbus_example.py to fit your needs, copy and rename it to solark_modbus.py
from solark_modbus import register_table

import config


def build_register_dict(client, reg_table):
    """Build a Python Dictionary of the Sol-Ark's memory registers.

    Args
    ----
    client : pymodbus.client
    reg_table : list

    Returns
    -------
    reg_result : dict
    """
    logger.debug("START")
    logger.info("Building a dictionary of Sol-Ark register values...")
    reg_result = {}
    for item in reg_table:
        if item["pull"]:
            if item["signed"] and item["bits"] == 16:
                corrected_register = read_register(
                    client, item["address"], 1, 1
                ).decode_16bit_int()
            elif not item["signed"] and item["bits"] == 16:
                corrected_register = read_register(
                    client, item["address"], 1, 1
                ).decode_16bit_uint()
            elif item["signed"] and item["bits"] == 32:
                corrected_register = read_register(
                    client, item["address"], 2, 1
                ).decode_32bit_int()
            elif not item["signed"] and item["bits"] == 32:
                corrected_register = read_register(
                    client, item["address"], 2, 1
                ).decode_32bit_uint()
            else:
                logger.warning("Error reading register; Setting corrected_register=0.")
                corrected_register = 0
            if item["multiplier"]:
                corrected_register = corrected_register / item["multiplier"]
            reg_result[item["key"]] = corrected_register
    logger.debug("STOP")
    return reg_result


def connect_solark(modbus_dict):
    """Make Modbus connection to Sol-Ark.

    Args
    ----
    modbus_dict: dict

    Returns
    -------
    modbus_connection: ModbusSerialClient or ModbusTcpClient
    """
    logger.debug("START")
    if modbus_dict["method"] == "rtu":
        logger.info("Connection to Inverter set to serial.")
        modbus_connection = ModbusSerialClient(
            method=modbus_dict["method"],
            port=modbus_dict["port"],
            baudrate=modbus_dict["baudrate"],
            timeout=modbus_dict["timeout"],
            parity=modbus_dict["parity"],
            stopbits=modbus_dict["stopbits"],
            bytesize=modbus_dict["bytesize"],
        )
    elif modbus_dict["method"] == "tcp":
        logger.info("Connection to Inverter set to TCP.")
        modbus_connection = ModbusTcpClient(
            host=modbus_dict["hostname"],
            port=modbus_dict["port"],
            timeout=modbus_dict["timeout"],
        )
    else:
        modbus_connection = None
    logger.info("Connecting to Sol-Ark Inverter...")
    try:
        if modbus_connection.connect():
            logger.info("Successfully connected to Sol-Ark.")
    except Exception as some_exception:
        logger.exception("ERROR=='%s'", some_exception)
        logger.error("ERROR connecting to Sol-Ark.")
    logger.debug("STOP")
    return modbus_connection


def db_query(db_deets, query, some_list):
    """Query database and return results.

    Args
    ----
    db_deets["host"] : str
    db_deets["user"] : str
    db_deets["passwd"] : str
    db_deets["database"] : str
    query : str
    some_list : dict

    Returns
    -------
    output_json : str
    """
    logger.info("START")
    host = db_deets["host"]
    user = db_deets["username"]
    passwd = db_deets["password"]
    database = db_deets["schema"]
    logger.debug("host=='%s'", host)
    logger.debug("user=='%s'", user)
    # logger.debug("passwd=='%s'", passwd)  # Reveals sensitive data
    logger.debug("database=='%s'", database)
    logger.debug("query=='%s'", query)
    logger.debug("some_list=='%s'", some_list)
    output_json = []
    database_connection = MySQLdb.connect(host, user, passwd, database)
    cursor = database_connection.cursor()
    # If some_list is provided, this query will be writing changes to
    # the database.
    if some_list:
        try:
            try:
                logger.info("Writing changes to database...")
                cursor.execute(query, some_list.values())
            except Exception as some_exception:
                logger.error("ERROR running query.")
                logger.exception("ERROR=='%s'", some_exception)
            try:
                database_connection.commit()
            except Exception as some_exception:
                logger.exception("ERROR=='%s'", some_exception)
                logger.error("ERROR committing changes.")
        except Exception as some_exception:
            logger.error("ERROR running query: %s", str(query))
            logger.exception("ERROR=='%s'", some_exception)

    # If some_list is NOT provided, this query will be retrieving data
    # from the database.
    if not some_list:
        try:
            logger.info("Querying database...")
            cursor.execute(query)
            # Convert SQL output to JSON.  This way we can iterate
            # through key:value pairs instead of worrying about adjusting
            # list positions if we change the query
            field_names = [i[0] for i in cursor.description]
            results = cursor.fetchall()
            for row in results:
                output_json.append(dict(zip(field_names, row)))
        except Exception as some_exception:
            logger.error("ERROR running query: %s", str(query))
            logger.exception("ERROR=='%s'", some_exception)

    database_connection.close()
    # logger.debug("output_json==%s", output_json)
    logger.info("STOP")
    return output_json


def read_register(client, addressess, reg_count, reg_unit):
    """Return register from Sol-Ark Inverter.

    Args
    ----
    client : pymodbus.client
    addresses : int
    reg_count : int
    reg_unit : int

    Returns
    -------
    decoder : str
    """
    logger.debug("START")
    logger.info("Reading Sol-Ark Register Address %s...", addressess)
    reg = client.read_holding_registers(
        address=addressess, count=reg_count, unit=reg_unit
    )
    decoder = BinaryPayloadDecoder.fromRegisters(
        reg.registers, byteorder=Endian.Big, wordorder=Endian.Little
    )
    return decoder


def main():
    """Main Function.

    Args
    ----
    args : dict

    Returns
    -------
    None
    """
    start_time = time.time()

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        # pylint: disable=line-too-long
        description=f"""{config.app_dict["name"]} {config.app_dict["version"]} {config.app_dict["date"]}\n--\nDescription: {config.app_dict["desc"]}\nAuthor:      {config.app_dict["author"]}\nURL:         {config.app_dict["url"]}""",
    )
    parser.add_argument(
        "--pull",
        help="Pull Sol-Ark Registers and display to console.",
        action="store_true",
        required=False,
    )
    parser.add_argument(
        "--push",
        help="Pull Sol-Ark Registers and insert into database.",
        action="store_true",
        required=False,
    )
    args = parser.parse_args()

    # Setup Logging Functionality
    logging.basicConfig(
        # pylint: disable=line-too-long
        filename=f"""{config.log_dict["path"]}solark_monitor_{datetime.date.today().strftime("%Y%m%d")}.log""",
        filemode="a",
        format="{asctime}  Log Level: {levelname:8}  Line: {lineno:3}  Function: {funcName:21}  Msg: {message}",
        style="{",
        datefmt="%Y-%m-%dT%H:%M:%S",
        level=config.log_dict["level"],
    )

    logger.info("")
    logger.info("")
    logger.info("")
    logger.info("START START START")
    logger.info(
        "%s %s (%s)",
        config.app_dict["name"],
        config.app_dict["version"],
        config.app_dict["date"],
    )

    if vars(args)["pull"]:
        solark = connect_solark(config.modbus_dict_tcp)
        if solark is not None:
            solark_list = build_register_dict(solark, register_table)
            for item in solark_list.items():
                print(item)
        else:
            logger.error("Unable to connect to Sol-Ark.")
    elif vars(args)["push"]:
        solark = connect_solark(config.modbus_dict_tcp)
        if solark is not None:
            solark_list = build_register_dict(solark, register_table)
            solark_list["datetime"] = datetime.datetime.now().isoformat("T")
            solark_list["timestamp"] = int(time.time())

            db_placeholders = ", ".join(["%s"] * len(solark_list))
            db_columns = ", ".join(solark_list.keys())
            # pylint: disable=line-too-long
            query = f"""INSERT INTO {config.db_dict["schema"] + ".solarkmon"} ({db_columns}) VALUES ({db_placeholders})"""

            try:
                db_query(config.db_dict, query, solark_list)
            except Exception as some_exception:
                logger.error("ERROR running db_query")
                logger.exception("EXCEPTION='%s'", str(some_exception))
        else:
            logger.error("Error connecting to Sol-Ark.")
    else:
        logger.error("Incorrect or missing arguments.")
    logger.info("Total Execution Time: %s seconds", time.time() - start_time)
    logger.info("STOP STOP STOP")
    return 0


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    sys.exit(main())
