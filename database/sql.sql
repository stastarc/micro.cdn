-- --------------------------------------------------------
-- Host:                         database-1.c8uwhqzmqgop.ap-northeast-2.rds.amazonaws.com
-- Server version:               10.6.7-MariaDB - managed by https://aws.amazon.com/rds/
-- Server OS:                    Linux
-- HeidiSQL Version:             12.0.0.6468
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for pl.cdn
CREATE DATABASE IF NOT EXISTS `pl.cdn` /*!40100 DEFAULT CHARACTER SET utf8mb3 COLLATE utf8mb3_bin */;
USE `pl.cdn`;

-- Dumping structure for table pl.cdn.approach
CREATE TABLE IF NOT EXISTS `approach` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `key` varchar(32) COLLATE utf8mb3_bin NOT NULL,
  `level` tinyint(3) unsigned NOT NULL,
  `tag` varchar(100) COLLATE utf8mb3_bin DEFAULT NULL,
  `exp` datetime DEFAULT NULL,
  `role` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;

-- Dumping data for table pl.cdn.approach: ~1 rows (approximately)
DELETE FROM `approach`;
INSERT INTO `approach` (`id`, `key`, `level`, `tag`, `exp`, `role`) VALUES
	(1, '6nA4shTc7N2N4UmOta2ExfSHDXpLd5U', 255, NULL, NULL, 255);

-- Dumping structure for table pl.cdn.contents
CREATE TABLE IF NOT EXISTS `contents` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `access` varchar(32) COLLATE utf8mb3_bin NOT NULL,
  `level` bigint(20) unsigned NOT NULL,
  `title` varchar(500) COLLATE utf8mb3_bin DEFAULT NULL,
  `detail` varchar(1000) COLLATE utf8mb3_bin DEFAULT NULL,
  `media_type` varchar(50) COLLATE utf8mb3_bin NOT NULL,
  `uploaded_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`,`access`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;

-- Dumping data for table pl.cdn.contents: ~1 rows (approximately)
DELETE FROM `contents`;
INSERT INTO `contents` (`id`, `access`, `level`, `title`, `detail`, `media_type`, `uploaded_at`) VALUES
	(1, 'loooooooooooooooooooooooooooooog', 254, 'the log file', NULL, 'text/plain', '1970-01-01 00:00:00');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
