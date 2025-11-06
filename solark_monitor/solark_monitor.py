"""solark_monitor."""

# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

import datetime
import sys
import time
from time import perf_counter

import MySQLdb
from aaron_common_libs.common_funcs import argument, cli, pretty_print, subcommand
from aaron_common_libs.logger.custom_logger import CustomLogger
from config import Config
from pymodbus.client import ModbusSerialClient, ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from solark_modbus import register_table

config = Config()
logging_handler = CustomLogger(log_dict=config.log_dict)
logger = logging_handler.default
logger_all = logging_handler.all


def build_register_dict(client, reg_table):
    """Build a Python Dictionary of the Sol-Ark's memory registers.

    Args:
        client (pymodbus.client)
        reg_table (list)

    Returns:
        reg_result (dict)
    """
    logger.info("Building a dictionary of Sol-Ark register values...")
    reg_result = {}
    for item in reg_table:
        logger.debug("item==%s", item)
        if item["pull"]:
            decoder = None
            if item["signed"] and item["bits"] == 16:
                decoder = read_register(client, item["address"], 1, 1)
                corrected_register = decoder.decode_16bit_int() if decoder else 0
            elif not item["signed"] and item["bits"] == 16:
                decoder = read_register(client, item["address"], 1, 1)
                corrected_register = decoder.decode_16bit_uint() if decoder else 0
            elif item["signed"] and item["bits"] == 32:
                decoder = read_register(client, item["address"], 2, 1)
                corrected_register = decoder.decode_32bit_int() if decoder else 0
            elif not item["signed"] and item["bits"] == 32:
                decoder = read_register(client, item["address"], 2, 1)
                corrected_register = decoder.decode_32bit_uint() if decoder else 0
            else:
                logger.warning("Error reading register; Setting corrected_register=0.")
                corrected_register = 0

            if decoder is None:
                logger.warning("Failed to read register at address %s; Setting corrected_register=0.", item["address"])
                corrected_register = 0
            elif item["multiplier"]:
                corrected_register = corrected_register / item["multiplier"]

            reg_result[item["key"]] = corrected_register
            logger.debug("corrected_register==%s", corrected_register)
    return reg_result


def connect_solark(modbus_dict):
    """Make Modbus connection to Sol-Ark.

    Args:
        modbus_dict (dict)

    Returns:
        modbus_connection: ModbusSerialClient or ModbusTcpClient
    """
    if modbus_dict["method"] == "rtu":
        modbus_connection = ModbusSerialClient(
            port=modbus_dict["port"],
            baudrate=modbus_dict["baudrate"],
            timeout=modbus_dict["timeout"],
            parity=modbus_dict["parity"],
            stopbits=modbus_dict["stopbits"],
            bytesize=modbus_dict["bytesize"],
        )
        logger.info("Connecting to Sol-Ark Inverter via Serial...")
    elif modbus_dict["method"] == "tcp":
        modbus_connection = ModbusTcpClient(
            host=modbus_dict["hostname"],
            port=modbus_dict["port"],
            timeout=modbus_dict["timeout"],
        )
        logger.info("Connecting to Sol-Ark Inverter via TCP...")
    else:
        modbus_connection = None
        logger.error("Invalid modbus method specified.")
        return None

    try:
        modbus_connection.connect()
        if modbus_connection.is_socket_open():
            logger.info("Successfully connected to Sol-Ark.")
            logger.debug("modbus_connection==%s", modbus_connection)
            return modbus_connection
        logger.error("ERROR: Socket not open after connect attempt.")
        return None
    except Exception as some_exception:  # pylint: disable=broad-exception-caught
        logger.exception("ERROR=='%s'", some_exception)
        logger.error("ERROR connecting to Sol-Ark.")
        return None


def db_query(db_details, query, some_dict):
    """Query database and return results.

    Args:
        db_details (dict)
        query (str)
        some_dict (dict)

    Returns:
        output_json (str)
    """
    output_json = {}
    database_connection = MySQLdb.connect(
        db_details["host"], db_details["username"], db_details["password"], db_details["schema_name"]
    )
    cursor = database_connection.cursor()
    try:  # Execute database query
        logger.info("Writing changes to database...")
        output_json = cursor.execute(
            query.format(schema_name=db_details["schema_name"], table_name=db_details["table_name"]),
            some_dict.values(),
        )
    except Exception as some_exception:  # pylint: disable=broad-exception-caught
        logger.error("ERROR running query.")
        logger.exception("ERROR=='%s'", some_exception)
    try:  # Python MySQL connector does not autocommit
        database_connection.commit()
    except Exception as some_exception:  # pylint: disable=broad-exception-caught
        logger.exception("ERROR=='%s'", some_exception)
        logger.error("ERROR committing changes.")

    database_connection.close()
    return output_json


def read_register(client, address, reg_count, reg_unit):
    """Return register from Sol-Ark Inverter.

    Args:
        client (pymodbus).client
        address (int)
        reg_count (int)
        reg_unit (int)

    Returns:
        decoder (str)
    """
    logger.debug("address==%s", address)
    logger.debug("reg_count==%s", reg_count)
    logger.debug("reg_unit==%s", reg_unit)
    logger.info("Reading Sol-Ark Register Address %s...", address)
    try:
        reg = client.read_holding_registers(address=address, count=reg_count)
        decoder = BinaryPayloadDecoder.fromRegisters(reg.registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
    except Exception as some_exception:  # pylint: disable=broad-exception-caught
        logger.error("ERROR=='%s'", some_exception)
        decoder = None
    return decoder


# Sub-Commands for Sol-Ark operations
@subcommand(
    [
        argument("--pull", help="Pull Sol-Ark Registers and display to console.", action="store_true", required=False),
        argument(
            "--pullpush", help="Pull Sol-Ark Registers and insert into database.", action="store_true", required=False
        ),
        argument("--serial", help="Connect to Sol-Ark via Serial connection.", action="store_true", required=False),
        argument("--tcp", help="Connect to Sol-Ark via TCP connection.", action="store_true", required=False),
    ]
)
def solark(args):
    """Subcommand options for Sol-Ark operations."""
    logger.debug("args==%s", vars(args))
    solark_results = {}

    # Establish connection
    if args.serial:
        solark_connected = connect_solark(config.modbus_dict_ser)
    elif args.tcp:
        solark_connected = connect_solark(config.modbus_dict_tcp)
    else:
        logger.error("No connection method specified (--serial or --tcp required).")
        solark_connected = None

    # Check if connection was successful
    if solark_connected is None:
        logger.error("Failed to connect to Sol-Ark. Cannot proceed with requested operation.")
        return solark_results

    # Perform requested operations
    if args.pull:
        solark_results = build_register_dict(client=solark_connected, reg_table=register_table)
        logger.debug("solark_results==%s", solark_results)
    if args.pullpush:
        solark_dict = build_register_dict(client=solark_connected, reg_table=register_table)
        solark_dict["datetime"] = datetime.datetime.now().isoformat("T")
        solark_dict["timestamp"] = int(time.time())
        query = """INSERT INTO {schema_name}.{table_name} (day_active_power, total_active_power_low_word, total_active_power_high_word, grid_frequency, dcdc_transformer_temp, igbt_heat_sink_temp, fault_info_word_1, fault_info_word_2, fault_info_word_3, fault_info_word_4, corrected_batt_capacity, daily_pv_power, dc_voltage_1, dc_current_1, dc_voltage_2, dc_current_2, grid_side_voltage_l1n, grid_side_voltage_l2n, grid_side_voltage_l1l2, voltage_middle_side_relay_l1l2, inverter_output_voltage_l1n, inverter_output_voltage_l2n, inverter_output_voltage_l1l2, load_voltage_l1, load_voltage_l2, grid_side_current_l1, grid_side_current_l2, grid_external_limiter_current_l1, grid_external_limiter_current_l2, inverter_output_current_l1, inverter_output_current_l2, gen_ac_coupled_power_input, grid_side_l1_power, grid_side_l2_power, total_power_grid_side_l1l2, grid_external_limiter1_power, grid_external_limiter2_power, grid_external_total_power, inverter_outputs_l1_power, inverter_outputs_l2_power, inverter_output_total_power, load_side_l1_power, load_side_l2_power, load_side_total_power, load_current_l1, load_current_l2, gen_port_voltage_l1l2, battery_temp, battery_voltage, battery_capacity_soc, pv1_input_power, pv2_input_power, battery_output_power, battery_output_current, load_frequency, inverter_output_frequency, grid_side_relay_status, generator_side_relay_status, generator_relay_frequency, datetime, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        try:
            solark_results = db_query(config.db_dict, query, solark_dict)
        except Exception as some_exception:  # pylint: disable=broad-exception-caught
            logger.error("ERROR running db_query")
            logger.exception("EXCEPTION='%s'", str(some_exception))
    return solark_results


def main():
    """Do Something."""
    start_time = perf_counter()

    logger.info("")
    logger_all.info("---------- START START START ----------")
    logger_all.info(
        "%s v%s (%s)",
        config.app_dict["title"],
        config.app_dict["version"],
        config.app_dict["date"],
    )

    required_vars = {}
    find_null_vars = [value for value in required_vars.items() if None is value[1]]
    if find_null_vars:
        logger.error("Missing Environment Variable(s): %s", find_null_vars)
        print(f"\nERROR: Missing Environment Variable(s): {find_null_vars}")
    else:
        args = cli.parse_args()
        if args.subcommand is None:
            cli.print_help()
        else:
            arg_results = args.func(args)
            if arg_results:
                print(pretty_print(arg_results))
            else:
                cli.print_help()

    logger_all.info("Total Execution Time: %s seconds", round(perf_counter() - start_time, 2))
    logger_all.info("----------   STOP STOP STOP  ----------")
    logger.info("")


if __name__ == "__main__":
    sys.exit(main())
