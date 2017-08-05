/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50529
Source Host           : localhost:3306
Source Database       : test

Target Server Type    : MYSQL
Target Server Version : 50529
File Encoding         : 65001

Date: 2017-05-19 21:11:27
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `day_data`
-- ----------------------------
DROP TABLE IF EXISTS `day_data`;
CREATE TABLE `day_data` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `index` bigint(20),
  `date` varchar(20) NOT NULL,
  `open` double,
  `close` double,
  `high` double,
  `low` double,
  `volume` double,
  `code` varchar(20) NOT NULL,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_id` (`id`) USING BTREE,
  KEY `_date` (`date`) USING BTREE,
  KEY `_code` (`code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

