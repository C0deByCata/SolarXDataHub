/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para openweather
CREATE DATABASE IF NOT EXISTS `openweather` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `openweather`;

-- Volcando estructura para tabla openweather.master_tb_request_options
CREATE TABLE IF NOT EXISTS `master_tb_request_options` (
  `id` int NOT NULL AUTO_INCREMENT,
  `request_type` varchar(50) NOT NULL COMMENT 'Tipo de petición realizada',
  `description` varchar(250) DEFAULT NULL COMMENT 'Descripción del tipo de petición',
  `timestamp_insert` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de inserción',
  `user_insert` varchar(50) DEFAULT NULL COMMENT 'Usuario que inserta',
  `timestamp_update` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT 'Fecha de actualización',
  `user_update` varchar(50) DEFAULT NULL COMMENT 'Usuario que actualiza',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla openweather.tb_air_pollution
CREATE TABLE IF NOT EXISTS `tb_air_pollution` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'ID interno del registro',
  `calculation_datetime` datetime NOT NULL COMMENT 'Fecha y hora de la consulta',
  `lat` float DEFAULT NULL COMMENT 'Latitud',
  `lon` float DEFAULT NULL COMMENT 'Longitud',
  `dt` int NOT NULL COMMENT 'Timestamp de la medición',
  `aqi` int NOT NULL COMMENT 'Índice de calidad del aire',
  `co` float NOT NULL COMMENT 'Monóxido de carbono (µg/m3)',
  `no` float NOT NULL COMMENT 'Óxidos de nitrógeno (µg/m3)',
  `no2` float NOT NULL COMMENT 'Dióxido de nitrógeno (µg/m3)',
  `o3` float NOT NULL COMMENT 'Ozono (µg/m3)',
  `so2` float NOT NULL COMMENT 'Dióxido de azufre (µg/m3)',
  `pm2_5` float NOT NULL COMMENT 'Partículas finas (µg/m3)',
  `pm10` float NOT NULL COMMENT 'Partículas gruesas (µg/m3)',
  `nh3` float NOT NULL COMMENT 'Amoníaco (µg/m3)',
  `timestamp_insert` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de inserción',
  `user_insert` varchar(50) DEFAULT NULL COMMENT 'Usuario que inserta',
  `timestamp_update` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT 'Fecha de actualización',
  `user_update` varchar(50) DEFAULT NULL COMMENT 'Usuario que actualiza',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_air_pollution` (`lat`,`lon`,`dt`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla openweather.tb_current_weather
CREATE TABLE IF NOT EXISTS `tb_current_weather` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'ID interno del registro',
  `calculation_datetime` datetime NOT NULL COMMENT 'Fecha y hora de la consulta',
  `city_name` varchar(100) DEFAULT NULL COMMENT 'Nombre de la ciudad',
  `country` varchar(10) DEFAULT NULL COMMENT 'Código del país',
  `lat` float DEFAULT NULL COMMENT 'Latitud',
  `lon` float DEFAULT NULL COMMENT 'Longitud',
  `temp` float DEFAULT NULL COMMENT 'Temperatura actual en °C',
  `feels_like` float DEFAULT NULL COMMENT 'Sensación térmica en °C',
  `temp_min` float DEFAULT NULL COMMENT 'Temperatura mínima en °C',
  `temp_max` float DEFAULT NULL COMMENT 'Temperatura máxima en °C',
  `pressure` int DEFAULT NULL COMMENT 'Presión atmosférica (hPa)',
  `humidity` int DEFAULT NULL COMMENT 'Humedad (%)',
  `sea_level` float DEFAULT NULL COMMENT 'Presión a nivel del mar (hPa)',
  `grnd_level` float DEFAULT NULL COMMENT 'Presión en el suelo (hPa)',
  `visibility` int DEFAULT NULL COMMENT 'Visibilidad en metros',
  `wind_speed` float DEFAULT NULL COMMENT 'Velocidad del viento (m/s)',
  `wind_deg` int DEFAULT NULL COMMENT 'Dirección del viento (grados)',
  `wind_gust` float DEFAULT NULL COMMENT 'Ráfagas del viento (m/s)',
  `clouds` int DEFAULT NULL COMMENT 'Nubosidad (%)',
  `dt` int DEFAULT NULL COMMENT 'Timestamp de la medición',
  `sunrise` int DEFAULT NULL COMMENT 'Hora de salida del sol (timestamp)',
  `sunset` int DEFAULT NULL COMMENT 'Hora de puesta del sol (timestamp)',
  `weather_main` varchar(255) DEFAULT NULL COMMENT 'Grupo(s) del clima (ej. Clear, Rain)',
  `weather_description` varchar(255) DEFAULT NULL COMMENT 'Descripción(es) detallada(s) del clima',
  `weather_icon` varchar(50) DEFAULT NULL COMMENT 'Código(s) del icono del clima',
  `timezone` int DEFAULT NULL COMMENT 'Desfase horario en segundos',
  `base` varchar(50) DEFAULT NULL COMMENT 'Fuente de los datos',
  `city_id` int DEFAULT NULL COMMENT 'ID de la ciudad en OpenWeather',
  `sys_type` int DEFAULT NULL COMMENT 'Tipo del sistema (sys.type)',
  `sys_id` int DEFAULT NULL COMMENT 'ID interno del sistema (sys.id)',
  `rain_1h` float DEFAULT NULL COMMENT 'Volumen de lluvia en la última hora (mm)',
  `rain_3h` float DEFAULT NULL COMMENT 'Volumen de lluvia en las últimas 3 horas (mm)',
  `timestamp_insert` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de inserción',
  `user_insert` varchar(50) DEFAULT NULL COMMENT 'Usuario que inserta',
  `timestamp_update` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT 'Fecha de actualización',
  `user_update` varchar(50) DEFAULT NULL COMMENT 'Usuario que actualiza',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_city_calc` (`city_id`,`calculation_datetime`),
  KEY `idx_calculation_datetime` (`calculation_datetime`),
  KEY `idx_city_name` (`city_name`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla openweather.tb_requests_log
CREATE TABLE IF NOT EXISTS `tb_requests_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `request_datetime` datetime NOT NULL COMMENT 'Fecha y hora en que se realizó la petición',
  `request_option_id` int NOT NULL COMMENT 'ID de la opción de petición (FK a master_tb_request_options)',
  `status` smallint DEFAULT NULL COMMENT 'Estado de la petición (éxito, error, etc.)',
  `timestamp_insert` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de inserción',
  `user_insert` varchar(50) DEFAULT NULL COMMENT 'Usuario que inserta',
  `timestamp_update` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT 'Fecha de actualización',
  `user_update` varchar(50) DEFAULT NULL COMMENT 'Usuario que actualiza',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_request_datetime` (`request_datetime`),
  KEY `fk_request_option_idx` (`request_option_id`),
  CONSTRAINT `fk_request_option` FOREIGN KEY (`request_option_id`) REFERENCES `master_tb_request_options` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para disparador openweather.master_tb_request_options_before_insert
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `master_tb_request_options_before_insert` BEFORE INSERT ON `master_tb_request_options` FOR EACH ROW SET NEW.user_insert = USER()//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Volcando estructura para disparador openweather.master_tb_request_options_before_update
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `master_tb_request_options_before_update` BEFORE UPDATE ON `master_tb_request_options` FOR EACH ROW SET NEW.user_update = USER()//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Volcando estructura para disparador openweather.tb_air_pollution_before_insert
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `tb_air_pollution_before_insert` BEFORE INSERT ON `tb_air_pollution` FOR EACH ROW SET NEW.user_insert = USER()//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Volcando estructura para disparador openweather.tb_air_pollution_before_update
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `tb_air_pollution_before_update` BEFORE UPDATE ON `tb_air_pollution` FOR EACH ROW SET NEW.user_update = USER()//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Volcando estructura para disparador openweather.tb_current_weather_before_insert
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `tb_current_weather_before_insert` BEFORE INSERT ON `tb_current_weather` FOR EACH ROW SET NEW.user_insert = USER()//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Volcando estructura para disparador openweather.tb_current_weather_before_update
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `tb_current_weather_before_update` BEFORE UPDATE ON `tb_current_weather` FOR EACH ROW SET NEW.user_update = USER()//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Volcando estructura para disparador openweather.tb_requests_log_before_insert
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `tb_requests_log_before_insert` BEFORE INSERT ON `tb_requests_log` FOR EACH ROW SET NEW.user_insert = USER()//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Volcando estructura para disparador openweather.tb_requests_log_before_update
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `tb_requests_log_before_update` BEFORE UPDATE ON `tb_requests_log` FOR EACH ROW SET NEW.user_update = USER()//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;


-- Volcando estructura de base de datos para solaxcloud
CREATE DATABASE IF NOT EXISTS `solaxcloud` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `solaxcloud`;

-- Volcando estructura para tabla solaxcloud.master_tb_device_status_mapping
CREATE TABLE IF NOT EXISTS `master_tb_device_status_mapping` (
  `code` smallint NOT NULL AUTO_INCREMENT,
  `status` varchar(100) NOT NULL,
  `description` varchar(100) DEFAULT NULL,
  `timestamp_insert` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `user_insert` varchar(50) DEFAULT NULL,
  `timestamp_update` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `user_update` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=134 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla solaxcloud.master_tb_error_codes
CREATE TABLE IF NOT EXISTS `master_tb_error_codes` (
  `code` smallint NOT NULL AUTO_INCREMENT,
  `message` varchar(50) NOT NULL,
  `timestamp_insert` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `user_insert` varchar(50) DEFAULT NULL,
  `timestamp_update` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `user_update` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=2003 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla solaxcloud.master_tb_inverters
CREATE TABLE IF NOT EXISTS `master_tb_inverters` (
  `id` int NOT NULL AUTO_INCREMENT,
  `inverterSN` varchar(50) NOT NULL,
  `sn` varchar(50) NOT NULL,
  `inverterType` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `site_name` varchar(100) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `timestamp_insert` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `user_insert` varchar(50) DEFAULT NULL,
  `timestamp_update` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `user_update` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_inverterSN` (`inverterSN`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla solaxcloud.tb_battery_data
CREATE TABLE IF NOT EXISTS `tb_battery_data` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `periodo` smallint NOT NULL,
  `min` smallint NOT NULL,
  `inverter_id` int NOT NULL,
  `batPower` float DEFAULT NULL,
  `soc` float DEFAULT NULL,
  `batStatus` varchar(50) DEFAULT NULL,
  `uploadTime` datetime NOT NULL,
  `timestamp_insert` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `user_insert` varchar(50) DEFAULT NULL,
  `timestamp_update` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `user_update` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_measurement_battery` (`fecha`,`periodo`,`min`,`inverter_id`),
  KEY `inverter_id` (`inverter_id`),
  CONSTRAINT `tb_battery_data_ibfk_1` FOREIGN KEY (`inverter_id`) REFERENCES `master_tb_inverters` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla solaxcloud.tb_energy_data
CREATE TABLE IF NOT EXISTS `tb_energy_data` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `periodo` smallint NOT NULL,
  `min` smallint NOT NULL,
  `inverter_id` int NOT NULL,
  `acpower` float DEFAULT NULL,
  `yieldtoday` float DEFAULT NULL,
  `yieldtotal` float DEFAULT NULL,
  `feedinpower` float DEFAULT NULL,
  `feedinenergy` float DEFAULT NULL,
  `consumeenergy` float DEFAULT NULL,
  `uploadTime` datetime NOT NULL,
  `timestamp_insert` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `user_insert` varchar(50) DEFAULT NULL,
  `timestamp_update` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `user_update` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_measurement` (`fecha`,`periodo`,`min`,`inverter_id`),
  KEY `inverter_id` (`inverter_id`),
  CONSTRAINT `tb_energy_data_ibfk_1` FOREIGN KEY (`inverter_id`) REFERENCES `master_tb_inverters` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla solaxcloud.tb_notification_log
CREATE TABLE IF NOT EXISTS `tb_notification_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `inverter_id` int NOT NULL,
  `notification_type` varchar(50) NOT NULL,
  `sent_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `timestamp_insert` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `user_insert` varchar(50) DEFAULT NULL,
  `timestamp_update` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `user_update` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_inverter_notif` (`inverter_id`,`notification_type`),
  CONSTRAINT `fk_notif_inverter` FOREIGN KEY (`inverter_id`) REFERENCES `master_tb_inverters` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla solaxcloud.tb_phase_power_data
CREATE TABLE IF NOT EXISTS `tb_phase_power_data` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `periodo` smallint NOT NULL,
  `min` smallint NOT NULL,
  `inverter_id` int NOT NULL,
  `peps1` float DEFAULT NULL,
  `peps2` float DEFAULT NULL,
  `peps3` float DEFAULT NULL,
  `powerdc1` float DEFAULT NULL,
  `powerdc2` float DEFAULT NULL,
  `powerdc3` float DEFAULT NULL,
  `powerdc4` float DEFAULT NULL,
  `uploadTime` datetime NOT NULL,
  `timestamp_insert` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `user_insert` varchar(50) DEFAULT NULL,
  `timestamp_update` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `user_update` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_measurement_phase` (`fecha`,`periodo`,`min`,`inverter_id`),
  KEY `inverter_id` (`inverter_id`),
  CONSTRAINT `tb_phase_power_data_ibfk_1` FOREIGN KEY (`inverter_id`) REFERENCES `master_tb_inverters` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para disparador solaxcloud.master_tb_device_status_mapping_before_insert
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `master_tb_device_status_mapping_before_insert` BEFORE INSERT ON `master_tb_device_status_mapping` FOR EACH ROW SET NEW.user_insert = USER()//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Volcando estructura para disparador solaxcloud.master_tb_device_status_mapping_before_update
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `master_tb_device_status_mapping_before_update` BEFORE UPDATE ON `master_tb_device_status_mapping` FOR EACH ROW SET NEW.user_update = USER()//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Volcando estructura para disparador solaxcloud.master_tb_error_codes_before_insert
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `master_tb_error_codes_before_insert` BEFORE INSERT ON `master_tb_error_codes` FOR EACH ROW SET NEW.user_insert = USER()//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Volcando estructura para disparador solaxcloud.master_tb_error_codes_before_update
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `master_tb_error_codes_before_update` BEFORE UPDATE ON `master_tb_error_codes` FOR EACH ROW SET NEW.user_update = USER()//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Volcando estructura para disparador solaxcloud.master_tb_inverters_before_insert
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `master_tb_inverters_before_insert` BEFORE INSERT ON `master_tb_inverters` FOR EACH ROW SET NEW.user_insert = USER()//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Volcando estructura para disparador solaxcloud.master_tb_inverters_before_update
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `master_tb_inverters_before_update` BEFORE UPDATE ON `master_tb_inverters` FOR EACH ROW SET NEW.user_update = USER()//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Volcando estructura para disparador solaxcloud.tb_battery_data_before_insert
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `tb_battery_data_before_insert` BEFORE INSERT ON `tb_battery_data` FOR EACH ROW SET NEW.user_insert = USER()//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Volcando estructura para disparador solaxcloud.tb_battery_data_before_update
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `tb_battery_data_before_update` BEFORE UPDATE ON `tb_battery_data` FOR EACH ROW SET NEW.user_update = USER()//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Volcando estructura para disparador solaxcloud.tb_energy_tb_data_before_insert
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `tb_energy_tb_data_before_insert` BEFORE INSERT ON `tb_energy_data` FOR EACH ROW SET NEW.user_insert = USER()//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Volcando estructura para disparador solaxcloud.tb_energy_tb_data_before_update
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `tb_energy_tb_data_before_update` BEFORE UPDATE ON `tb_energy_data` FOR EACH ROW SET NEW.user_update = USER()//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Volcando estructura para disparador solaxcloud.tb_notification_log_before_insert
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `tb_notification_log_before_insert` BEFORE INSERT ON `tb_notification_log` FOR EACH ROW SET NEW.user_insert = USER()//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Volcando estructura para disparador solaxcloud.tb_notification_log_before_update
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `tb_notification_log_before_update` BEFORE UPDATE ON `tb_notification_log` FOR EACH ROW SET NEW.user_update = USER()//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Volcando estructura para disparador solaxcloud.tb_phase_power_data_before_insert
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `tb_phase_power_data_before_insert` BEFORE INSERT ON `tb_phase_power_data` FOR EACH ROW SET NEW.user_insert = USER()//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Volcando estructura para disparador solaxcloud.tb_phase_power_data_before_update
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `tb_phase_power_data_before_update` BEFORE UPDATE ON `tb_phase_power_data` FOR EACH ROW SET NEW.user_update = USER()//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;


-- Volcando estructura de base de datos para weatherbit
CREATE DATABASE IF NOT EXISTS `weatherbit` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `weatherbit`;

-- Volcando estructura para tabla weatherbit.tb_hourly_data
CREATE TABLE IF NOT EXISTS `tb_hourly_data` (
  `id` int NOT NULL AUTO_INCREMENT,
  `calculation_datetime` datetime NOT NULL COMMENT 'Fecha y hora de la petición (redondeada a la hora)',
  `app_temp` float DEFAULT NULL COMMENT 'Temperatura aparente en °C',
  `aqi` int DEFAULT NULL COMMENT 'Índice de calidad del aire',
  `city_name` varchar(100) DEFAULT NULL COMMENT 'Nombre de la ciudad',
  `clouds` int DEFAULT NULL COMMENT 'Porcentaje de nubes',
  `country_code` varchar(10) DEFAULT NULL COMMENT 'Código del país',
  `datetime` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'Fecha y hora del reporte, formato: YYYY-MM-DD:HH',
  `dewpt` float DEFAULT NULL COMMENT 'Punto de rocío en °C',
  `dhi` float DEFAULT NULL COMMENT 'Irradiancia difusa horizontal (W/m2)',
  `dni` float DEFAULT NULL COMMENT 'Irradiancia normal directa (W/m2)',
  `elev_angle` float DEFAULT NULL COMMENT 'Ángulo de elevación solar',
  `ghi` float DEFAULT NULL COMMENT 'Irradiancia horizontal global (W/m2)',
  `gust` float DEFAULT NULL COMMENT 'Velocidad de ráfagas del viento (m/s)',
  `h_angle` float DEFAULT NULL COMMENT 'Ángulo horario solar',
  `lat` float DEFAULT NULL COMMENT 'Latitud',
  `lon` float DEFAULT NULL COMMENT 'Longitud',
  `ob_time` datetime DEFAULT NULL COMMENT 'Tiempo de observación (YYYY-MM-DD HH:MM)',
  `pod` varchar(5) DEFAULT NULL COMMENT 'Período del día (d = día, n = noche)',
  `precip` float DEFAULT NULL COMMENT 'Precipitación en mm',
  `pres` float DEFAULT NULL COMMENT 'Presión atmosférica en mb',
  `rh` int DEFAULT NULL COMMENT 'Humedad relativa (%)',
  `slp` float DEFAULT NULL COMMENT 'Presión a nivel del mar en mb',
  `snow` float DEFAULT NULL COMMENT 'Cantidad de nieve',
  `solar_rad` float DEFAULT NULL COMMENT 'Radiación solar (W/m2)',
  `sources` varchar(255) DEFAULT NULL COMMENT 'Fuentes de datos (separadas por coma)',
  `state_code` varchar(10) DEFAULT NULL COMMENT 'Código de estado',
  `station` varchar(50) DEFAULT NULL COMMENT 'Estación meteorológica',
  `sunrise` time DEFAULT NULL COMMENT 'Hora de salida del sol',
  `sunset` time DEFAULT NULL COMMENT 'Hora de puesta del sol',
  `temp` float DEFAULT NULL COMMENT 'Temperatura en °C',
  `timezone` varchar(50) DEFAULT NULL COMMENT 'Zona horaria',
  `ts` bigint DEFAULT NULL COMMENT 'Timestamp Unix',
  `uv` float DEFAULT NULL COMMENT 'Índice UV',
  `vis` float DEFAULT NULL COMMENT 'Visibilidad en km',
  `weather_icon` varchar(10) DEFAULT NULL COMMENT 'Código del icono meteorológico',
  `weather_description` varchar(255) DEFAULT NULL COMMENT 'Descripción del clima',
  `weather_code` int DEFAULT NULL COMMENT 'Código del clima',
  `wind_cdir` varchar(10) DEFAULT NULL COMMENT 'Dirección del viento (abreviada)',
  `wind_cdir_full` varchar(50) DEFAULT NULL COMMENT 'Dirección completa del viento',
  `wind_dir` int DEFAULT NULL COMMENT 'Dirección del viento en grados',
  `wind_spd` float DEFAULT NULL COMMENT 'Velocidad del viento (m/s)',
  `timestamp_insert` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de inserción',
  `user_insert` varchar(50) DEFAULT NULL COMMENT 'Usuario que inserta',
  `timestamp_update` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT 'Fecha de actualización',
  `user_update` varchar(50) DEFAULT NULL COMMENT 'Usuario que actualiza',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_calculation` (`calculation_datetime`),
  KEY `idx_city_calculation` (`city_name`,`calculation_datetime`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla weatherbit.tb_requests_log
CREATE TABLE IF NOT EXISTS `tb_requests_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `request_datetime` datetime NOT NULL COMMENT 'Fecha y hora en que se realizó la petición',
  `status` smallint DEFAULT NULL COMMENT 'Estado de la petición (éxito, error, etc.)',
  `timestamp_insert` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de inserción',
  `user_insert` varchar(50) DEFAULT NULL COMMENT 'Usuario que inserta',
  `timestamp_update` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT 'Fecha de actualización',
  `user_update` varchar(50) DEFAULT NULL COMMENT 'Usuario que actualiza',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_request_datetime` (`request_datetime`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para disparador weatherbit.tb_hourly_data_before_insert
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `tb_hourly_data_before_insert` BEFORE INSERT ON `tb_hourly_data` FOR EACH ROW SET NEW.user_insert = USER()//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Volcando estructura para disparador weatherbit.tb_hourly_data_before_update
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `tb_hourly_data_before_update` BEFORE UPDATE ON `tb_hourly_data` FOR EACH ROW SET NEW.user_update = USER()//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Volcando estructura para disparador weatherbit.tb_requests_log_before_insert
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `tb_requests_log_before_insert` BEFORE INSERT ON `tb_requests_log` FOR EACH ROW SET NEW.user_insert = USER()//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Volcando estructura para disparador weatherbit.tb_requests_log_before_update
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `tb_requests_log_before_update` BEFORE UPDATE ON `tb_requests_log` FOR EACH ROW SET NEW.user_update = USER()//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
