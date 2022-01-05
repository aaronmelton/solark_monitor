-- MariaDB dump 10.19  Distrib 10.6.5-MariaDB, for Linux (x86_64)
--
-- Host: X.X.X.X    Database: solarkmon
-- ------------------------------------------------------
-- Server version	10.6.5-MariaDB

--
-- Table structure for table `solarkmon`
--

DROP TABLE IF EXISTS `solarkmon`;

CREATE TABLE `solarkmon` (
  `data_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `datetime` datetime DEFAULT NULL,
  `day_active_power` mediumint(9) DEFAULT NULL,
  `total_active_power_low_word` int(10) unsigned DEFAULT NULL,
  `total_active_power_high_word` int(10) unsigned DEFAULT NULL,
  `grid_frequency` smallint(5) unsigned DEFAULT NULL,
  `dcdc_transformer_temp` smallint(5) unsigned DEFAULT NULL,
  `igbt_heat_sink_temp` smallint(5) unsigned DEFAULT NULL,
  `fault_info_word_1` smallint(5) unsigned DEFAULT NULL,
  `fault_info_word_2` smallint(5) unsigned DEFAULT NULL,
  `fault_info_word_3` smallint(5) unsigned DEFAULT NULL,
  `fault_info_word_4` smallint(5) unsigned DEFAULT NULL,
  `corrected_batt_capacity` smallint(5) unsigned DEFAULT NULL,
  `daily_pv_power` smallint(5) unsigned DEFAULT NULL,
  `dc_voltage_1` smallint(5) unsigned DEFAULT NULL,
  `dc_current_1` smallint(5) unsigned DEFAULT NULL,
  `dc_voltage_2` smallint(5) unsigned DEFAULT NULL,
  `dc_current_2` smallint(5) unsigned DEFAULT NULL,
  `grid_side_voltage_l1n` smallint(5) unsigned DEFAULT NULL,
  `grid_side_voltage_l2n` smallint(5) unsigned DEFAULT NULL,
  `grid_side_voltage_l1l2` smallint(5) unsigned DEFAULT NULL,
  `voltage_middle_side_relay_l1l2` smallint(5) unsigned DEFAULT NULL,
  `inverter_output_voltage_l1n` smallint(5) unsigned DEFAULT NULL,
  `inverter_output_voltage_l2n` smallint(5) unsigned DEFAULT NULL,
  `inverter_output_voltage_l1l2` smallint(5) unsigned DEFAULT NULL,
  `load_voltage_l1` smallint(5) unsigned DEFAULT NULL,
  `load_voltage_l2` smallint(5) unsigned DEFAULT NULL,
  `grid_side_current_l1` smallint(6) DEFAULT NULL,
  `grid_side_current_l2` smallint(6) DEFAULT NULL,
  `grid_external_limiter_current_l1` smallint(6) DEFAULT NULL,
  `grid_external_limiter_current_l2` smallint(6) DEFAULT NULL,
  `inverter_output_current_l1` smallint(6) DEFAULT NULL,
  `inverter_output_current_l2` smallint(6) DEFAULT NULL,
  `gen_ac_coupled_power_input` smallint(6) DEFAULT NULL,
  `grid_side_l1_power` smallint(6) DEFAULT NULL,
  `grid_side_l2_power` smallint(6) DEFAULT NULL,
  `total_power_grid_side_l1l2` smallint(6) DEFAULT NULL,
  `grid_external_limiter1_power` smallint(6) DEFAULT NULL,
  `grid_external_limiter2_power` smallint(6) DEFAULT NULL,
  `grid_external_total_power` smallint(6) DEFAULT NULL,
  `inverter_outputs_l1_power` smallint(6) DEFAULT NULL,
  `inverter_outputs_l2_power` smallint(6) DEFAULT NULL,
  `inverter_output_total_power` smallint(6) DEFAULT NULL,
  `load_side_l1_power` smallint(6) DEFAULT NULL,
  `load_side_l2_power` smallint(6) DEFAULT NULL,
  `load_side_total_power` smallint(6) DEFAULT NULL,
  `load_current_l1` smallint(6) DEFAULT NULL,
  `load_current_l2` smallint(6) DEFAULT NULL,
  `gen_port_voltage_l1l2` smallint(6) DEFAULT NULL,
  `battery_temp` smallint(5) unsigned DEFAULT NULL,
  `battery_voltage` smallint(5) unsigned DEFAULT NULL,
  `battery_capacity_soc` tinyint(3) unsigned DEFAULT NULL,
  `pv1_input_power` smallint(5) unsigned DEFAULT NULL,
  `pv2_input_power` smallint(5) unsigned DEFAULT NULL,
  `battery_output_power` smallint(6) DEFAULT NULL,
  `battery_output_current` smallint(6) DEFAULT NULL,
  `load_frequency` smallint(5) unsigned DEFAULT NULL,
  `inverter_output_frequency` smallint(5) unsigned DEFAULT NULL,
  `grid_side_relay_status` tinyint(3) unsigned DEFAULT NULL,
  `generator_side_relay_status` tinyint(3) unsigned DEFAULT NULL,
  `generator_relay_frequency` smallint(5) unsigned DEFAULT NULL,
  PRIMARY KEY (`data_id`),
  UNIQUE KEY `idnew_table_UNIQUE` (`data_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2376 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
