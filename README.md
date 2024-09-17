# Sol-Ark Monitor

A Python script to read memory register(s) from Sol-Ark Inverters and insert them into a database.

![Sol-Ark Dashboard](solark_dashboard.png)

## Getting Started

### About This Code
This script was written in order to maintain local control of your Sol-Ark Inverter.

It is known to work with Model Sol-Ark 12k-P, COMM 142a-0717, MCU Ver6983.

#### Why Re-Invent The Wheel?
* Your Sol-Ark Inverter likely came with a Wi-Fi dongle that allows for remote
  monitoring, troubleshooting and software updates of your inverter.  I have a
  few issues with Sol-Ark's implementation of these remote capabilities:
  - The Wi-Fi dongle allows for unprotected access via HTTP.  Any individual on
    the same Wi-Fi network can alter the firmware of the dongle, change its Wi-Fi
    AP association, use it to scan for nearby access points and who knows what
    else.  I prefer to unplug it unless in need of support, but I'd also like to
    monitor my inverter's activity without standing in front of it too.
  - The same data I'm collecting via MODBUS protocol from the inverter is being
    sent overseas to China.  I prefer my data not be collected by unknown parties
    in a different country.**
  - The application/website (PowerView) used by Sol-Ark is also developed and
    maintained in China.  This application allows you to remotely alter the
    configuration of your inverter.  This same application also allows anyone
    to view the Operational Data of other Customers simply by providing their
    serial number, so I don't trust the possibility that a determined individual
    with the correct scripting skills may not be able to alter the configuration
    of my inverter without my knowledge OR consent.**
  
  ** Sol-Ark allegedly moved their remote capabilities to the United States. Browse [diysolarforum.com](https://diysolarforum.com/) for details.
* Other vendors already have well-established products in this space.
  [Victron Energy's Venu OS](https://github.com/victronenergy/venus) and [Solar Assistant](https://solar-assistant.io/) come to mind.
  But I want a database with my own data to play with.  I also like to build
  my own dashboards and home automation/monitoring solutions.
* Because I can.  I enjoy writing code and learning new technology.

#### Design Decisions
* I'm only working with Read-Only memory registers here.
* solar_modbus.py was created to contain what I knew about the Sol-Ark's memory
  registers; I later included the range values as a sanity check.  (What I
  previously thought were incorrect values by my inverter were actually being
  decoded incorrectly.)
* MySQL: I went with what I know.  I would have liked to try a time-series
  database (like InfluxDB).  Perhaps in a new release?
* Script variables are picked up from the environment (see config.py).

#### My Personal Setup
* I have a [Raspberry Pi](https://www.raspberrypi.org/) connected to my inverter.
* I use [mbusd](https://github.com/3cky/mbusd) to make the Modbus details available 
  via TCP so they can be consumed by multiple sources.
  * [HA-solark-PV Home Assistant integration](https://github.com/pbix/HA-solark-PV) collects Modbus details via TCP.
  * This script, which runs on another VM collects Modbus data and inserts it into a database.
* You could just as easily run this script on the PC connected to your Inverter
  without the need to make the inverter's Modbus details available via TCP.  I
  just prefer all my solutions to be over-engineered. :) 

### Prerequisites
* A computer located near your inverter to make the Modbus calls to the
  inverter.  (I'm using a Raspberry Pi 3 Model B v1.2.)
* Python v3.11+
* Python's [Poetry](https://python-poetry.org/) package manager
* A specially-crafted cable to connect your computer to your inverter.  The
  MODBUS/RJ45 Application Note in your manual has some info.  I'm using a
  [JBtek USB to RS485 Converter Adapter](https://www.amazon.com/gp/product/B00NKAJGZM/ref=ppx_yo_dt_b_asin_title_o06_s00?ie=UTF8&psc=1) 
  as mentioned by [Solardad's first post in this thread](https://diysolarforum.com/threads/sol-ark-inverter-monitoring.23717/#post-279953) on the Solar DIY Forums.

#### Python Libraries
* See [pyproject.toml](pyproject.toml)

### Instructions For Use
* Install [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)
* Clone the repository: `git clone https://github.com/aaronmelton/solark_monitor.git`
* Change directory into the newly cloned repository: `cd solark_monitor`
* Invoke Poetry shell: `poetry shell`
* Install Python dependencies: `poetry update`
* Test run script: `python3 solark_monitor.py solark --help`
* Set the following environment variables (or modify `config.py` to hard-code them):
  * INV_HOSTNAME: Hostname or IP Address of the device providing RTU data.
  * DB_HOSTNAME: Hostname or IP Address of the database server.
  * DB_USERNAME: Database username with write permissions.
  * DB_PASSWORD: Database username's password
  * DB_SCHEMA: Name of the database schema.
  * DB_TABLE: Name of the database table.

#### Troubleshooting Installation
* If you encounter an issue installing the Python mysqlclient library, [visit the library project](https://pypi.org/project/mysqlclient/) for more information.

#### Python Commands
`python3 solark_monitor.py solark --help` for help.

`python3 solark_monitor.py solark --pull --serial` to pull Modbus values via Serial and display to screen.

`python3 solark_monitor.py solark --pull --tcp` to pull Modbus values via TCP and display to screen.

`python3 solark_monitor.py solark --pullpush --serial` to pull Modbus values via Serial and store them in a database.

`python3 solark_monitor.py solark --pullpush --tcp` to pull Modbus values via TCP and store them in a database.

## Acknowledgements
* Solardad's [Sol-Ark - Inverter Monitoring](https://diysolarforum.com/threads/sol-ark-inverter-monitoring.23717/) thread on DIY Solar Power Forum.
* offthehook for [sharing his code](https://diysolarforum.com/threads/sol-ark-inverter-monitoring.23717/post-299534) illustrating how to read memory registers via pymodbus.
* Borrowed some techniques from [Home Assistant integration for the SolArk PV Inverter](https://github.com/pbix/HA-solark-PV).

## Authors
* **Aaron Melton** - *Author* - Aaron Melton <aaron@aaronmelton.com>
