# CHANGELOG

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
- requirements.txt -- now using Poetry for package management.

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
