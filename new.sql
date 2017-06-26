/*
 Navicat Premium Data Transfer

 Source Server         : 本地测试
 Source Server Type    : MySQL
 Source Server Version : 50542
 Source Host           : localhost
 Source Database       : w3a_scan

 Target Server Type    : MySQL
 Target Server Version : 50542
 File Encoding         : utf-8

 Date: 06/26/2017 13:51:33 PM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `crawl_info`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_info`;
CREATE TABLE `crawl_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `target` varchar(255) NOT NULL COMMENT '扫描目标',
  `start_date` varchar(255) NOT NULL COMMENT '扫描开始时间',
  `end_date` varchar(255) NOT NULL COMMENT '扫描结束时间',
  `commandline` varchar(255) NOT NULL COMMENT '扫描执行的命令',
  `user_agent` varchar(255) NOT NULL COMMENT '扫描的ua',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `request`
-- ----------------------------
DROP TABLE IF EXISTS `request`;
CREATE TABLE `request` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `taskid` int(11) DEFAULT NULL,
  `method` varchar(255) NOT NULL COMMENT '请求类型',
  `host` varchar(255) DEFAULT NULL COMMENT '请求地址',,
  `url` varchar(255) NOT NULL COMMENT '地址',
  `data` text COMMENT '参数',
  `referer` varchar(255) DEFAULT NULL COMMENT '来路',
  `type` varchar(255) NOT NULL COMMENT '类型',
  `redirects` varchar(255) DEFAULT '' COMMENT '什么鬼',
  `cookies` varchar(255) DEFAULT NULL COMMENT 'cookie',
  `http_auth` varchar(255) DEFAULT NULL COMMENT 'http认证',
  `out_of_scope` varchar(255) DEFAULT NULL,
  `trigger` varchar(255) DEFAULT NULL  COMMENT '触发事件',
  `html` text  COMMENT 'http内容',
  `user_output` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
