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

from pymodbus.client.sync import ModbusSerialClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
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
            reg_result[item["key"]] = read_register(
                client, item["address"], 1, 1
            ).decode_16bit_uint()
    logger.debug("STOP")
    return reg_result


def connect_solark(modbus_dict):
    """Make Modbus connection to Sol-Ark.

    Args
    ----
    modbus_dict: dict

    Returns
    -------
    modbus_connection: ModbusSerialClient
    """
    logger.debug("START")
    logger.info("Connecting to Sol-Ark Inverter...")
    modbus_connection = ModbusSerialClient(
        method=modbus_dict["method"],
        port=modbus_dict["port"],
        baudrate=modbus_dict["baudrate"],
        timeout=modbus_dict["timeout"],
        parity=modbus_dict["parity"],
        stopbits=modbus_dict["stopbits"],
        bytesize=modbus_dict["bytesize"],
    )
    try:
        if modbus_connection.connect():
            logger.info("Successfully connected to Sol-Ark.")
    except Exception as some_exception:
        logger.exception("ERROR=='%s'", some_exception)
        logger.error("ERROR connecting to Sol-Ark.")
    logger.debug("STOP")
    return modbus_connection


def db_query(host, user, passwd, database, query, some_list):
    """Query database and return results.

    Args
    ----
    host : str
    user : str
    password : str
    database : str
    query : str
    some_list : dict

    Returns
    -------
    output_json : str
    """
    logger.info("START")
    logger.debug("host=='%s'", host)
    logger.debug("user=='%s'", user)
    logger.debug("passwd=='%s'", passwd)
    logger.debug("database=='%s'", database)
    logger.debug("query=='%s'", query)
    logger.debug("some_list=='%s'", some_list)
    output_json = []
    database_connection = MySQLdb.connect(host, user, passwd, database)
    cursor = database_connection.cursor()
    # If some_list is provided, this query will be writing chagnes to
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
                logger.error("ERROR commiting changes.")
        except Exception as some_exception:
            logger.error("ERROR running query: %s", str(query))
            logger.exception("ERROR=='%s'", some_exception)

    # If some_list is NOT provdied, this query will be retrieving data
    # from the database.
    if not some_list:
        try:
            logger.info("Querying database...")
            cursor.execute(query)
            # Convert SQL output to JSON.  This way we can iterate
            # through key:value pairs instead of worring about adjusting
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


def find_item_in_list(this_item, this_list, key):
    """Find the position of a string in a list of lists.

    Args
    ----
    this_item : str
    this_list : dict
    key : str

    Returns
    -------
    index : int
    """
    logger.debug("START")
    index = None
    for index, row in enumerate(this_list):
        if row[key] == this_item:
            break
    logger.debug("index=='%s'", index)
    logger.debug("STOP")
    return index


def read_register(client, addressess, reg_count, reg_unit):
    """Return register from Sol-Ark Inverter.

    Args
    ----
    client : pymodbus.client
    addressess : int
    reg_count : int
    reg_unit : int

    Returns
    -------
    decoder : str
    """
    logger.debug("START")
    logger.info("Reading Sol-Ark Register Address %s", addressess)
    reg = client.read_holding_registers(
        address=addressess, count=reg_count, unit=reg_unit
    )
    decoder = BinaryPayloadDecoder.fromRegisters(
        reg.registers, byteorder=Endian.Big, wordorder=Endian.Little
    )
    logger.debug("STOP")
    return decoder


def temp_in_c(temperature):
    """Convert register to Degrees Celsius.

    Args
    ----
    temperature : str

    Returns
    -------
    return : int
    """
    logger.debug("")
    return (int(temperature) - 1000) / 10.0


def temp_in_f(temperature):
    """Convert integer to Degrees Fahrenheit.

    Args
    ----
    temperature : str

    Returns
    -------
    return : int
    """
    logger.debug("")
    return (int(temp_in_c(temperature)) * 1.8) + 32


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
        description=(
            config.app_dict["name"]
            + " "
            + config.app_dict["version"]
            + " "
            + config.app_dict["date"]
            + "\n"
            + "--\n"
            + "Description: "
            + config.app_dict["desc"]
            + "\n"
            + "Author:      "
            + config.app_dict["author"]
            + "\n"
            + "URL:         "
            + config.app_dict["url"]
        ),
    )
    parser.add_argument(
        "--pull",
        help="Pull Solark Registers and display to terminal.",
        action="store_true",
        required=False,
    )
    parser.add_argument(
        "--push",
        help="Push Solark Registers to database.",
        action="store_true",
        required=False,
    )
    args = parser.parse_args()

    # Setup Logging Functionality
    logging.basicConfig(
        filename=config.log_dict["path"]
        + "solark_monitor_"
        + datetime.date.today().strftime("%Y%m%d")
        + ".log",
        filemode="a",
        # pylint: disable=C0301
        format="%(asctime)s  Log Level: %(levelname)-8s  Line: %(lineno)-3d  Function: %(funcName)-21s  Msg: %(message)s",
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
        solark = connect_solark(config.modbus_dict)
        if solark is not None:
            solark_list = build_register_dict(solark, register_table)
            for item in solark_list:
                print(item, solark_list[item])
        else:
            logger.error("Unable to connect to Sol-Ark.")
    elif vars(args)["push"]:
        solark = connect_solark(config.modbus_dict)
        # serial_number = read_register(solark, 3, 5, 1).decode_string(10).decode('utf-8')
        if solark is not None:
            solark_list = build_register_dict(solark, register_table)
            timestamp = datetime.datetime.now().isoformat("T")
            solark_list["datetime"] = timestamp

            ###
            # INCLUDED TO CAPTURE DEBUG OUTPUT
            for item in solark_list:
                logger.info("%s: %s" % (item, solark_list[item]))
            ###
            ###

            db_placeholders = ", ".join(["%s"] * len(solark_list))
            db_columns = ", ".join(solark_list.keys())
            query = "INSERT INTO %s ( %s ) VALUES ( %s )" % (
                config.db_dict["schema"] + ".solarkmon",
                db_columns,
                db_placeholders,
            )
            try:
                db_query(
                    config.db_dict["host"],
                    config.db_dict["username"],
                    config.db_dict["password"],
                    config.db_dict["schema"],
                    query,
                    solark_list,
                )
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
