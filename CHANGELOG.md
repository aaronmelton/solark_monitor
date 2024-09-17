# CHANGELOG

## [0.6.0] - 2024-09-17
### Added
- CODEOWNERS
- solark_monitor/__init__.py: Namespace control
- solark_monitor/log/: Place-holder for log files
- solark_monitor/solark_modbus.py: A complete list of Sol-Ark memory registers.
- tests/: One day I'll populate this with some real unit tests.
### Changed
- Apologies for the poor CHANGELOG details.  The changes made to this code
  spanned many months of fractional work that weren't made in smaller commits.
- README.md: Corrected my abysmal spelling.
- Bumping Python packages versions.
- dashboard/grafana_dashboard.json: Updated to match changes made to latest
  train of Grafana.
- database/solark_monitor_database.sql: Updating database schema.
- solark_dashboard.png: I have no idea what changed here.
- solark_monitor/config.py: Moved configuration variables into a dataclass.
- solark_monitor/solark_monitor.py
  - Replacing local functions with those in my aaron_common_libs library.
  - Removed superfluous logging messages.
  - Improved function docstrings.
  - db_query(): Cleaned up this function to remove unused code.
  - read_register(): Updated to include changes to the Python package.
    This should resolve Issue #3.
  - solark(): Included new subcommands to specify how the data was being
    retrieved (TCP vs Serial); Updated SQL query syntax to remove static
    schema/table assignment.
  - 
### Removed
- .bandit.yml: Settings moved into pyproject.toml
- .flake8: Settings moved into pyproject.toml
- .pydocstyle.ini: Settings moved into pyproject.toml
- .yamllint: Settings moved into pyproject.toml
- solark_monitor/solark_modbus_example.py: Replaced with solark_modbus.py

## [0.5.0] - 2023-07-22
### Changed
- solark_monitor.py: Commented out debug log that captures password.
- pyproject.toml: Updating libraries.


## [0.4.0] - 2022-01-09
### Added
- Added screenshot of Grafana Dashboard.
- Added Grafana Dashboard JSON file.
### Changed
- Moved code into project subdirectory.
- build_register_dict(): Improved functions to decode 16 and 32-bit registers.
  This should fix the issue with registers falling outside vendor-defined
  integer ranges.
### Removed
- check_reg_value() function: No longer used after correcting for reading
  unsigned integers.
- find_item_in_list() function: No longer used after correcting for reading
  unsigned integers.
- temp_in_c() function: Not used.
- temp_in_f() function: Not used.
- value_in_range() function: No longer used after correcting for reading
  unsigned integers.


## [0.3.1] - 2022-01-07
### Changed
- value_in_range(): Corrected range function to include the last element in the
  range.


## [0.3.0] - 2022-01-06
### Added
- Added Modbus via TCP connection as an option.  Dictionary passed to the 
  connect_solark() function defines which Modbus connection (Serial/TCP) is
  used.
- Now that I'm obtaining my Modbus values via TCP, I'm moving back to managing
  packages with Poetry vs Pip.
### Changed
- Determined that all values were treated as unsigned integers leading to
  incorrect values for some registers.  Added additional fields to 
  register_table[] to define which values are signed and which are unsigned and
  updated the build_register_dict() function to return the correct value.
### Removed
- requirements.txt: now using Poetry for package management.


## [0.2.1] - 2022-01-05
### Changed
- Improved SQL query to satisfy Pylint (formatting) and Bandit (SQLi) findings.
- Converted args description from % (old code) to f-string format.
- Removed the logging statement recording the query statement (left in by
  mistake).


## [0.2.0] - 2022-01-04
### Added
- Sol-Ark Modbus RTU Protocol document does not provide any data ranges for
  these memory registers so I've made a best guess based on the operation of the
  inverter or the register description:
- grid_side_l1_power: 0->12,000 Watts
- grid_side_l2_power: 0->12,000 Watts
- battery_output_power: -32768->32767 Watts
- battery_output_current: -32768->32767 Amps
- inverter_outputs_l1_power: -32768->32767 Watts
- inverter_outputs_l2_power: -32768->32767 Watts
- inverter_output_total_power: -32768->32767 Watts
  When the register value is out of range I am assuming the actual value is 0
  according to my inverter display.  Uncertain if this is the correct approach
  but it's how I've decided to police my database inputs to prevent skewing the
  data.
- Created new function to address values that are out-of-range for the memory
  register (according to Sol-Ark modbus docs).
### Changed
- Applied spell check.
- Corrected range value for corrected_batt_capacity: 100->1000
- Improved database query to satisfy Pylint.  Nevermind; pylint is stupid.
  Ignoring this warning.
- Improved db_query() by reducing function input arguments.


## [0.1.1] - 2022-01-03
### Changed
- Improving debug logging to include the values of each register.


## [0.1.1] - 2022-01-01
### Added
- Publishing a new project.
