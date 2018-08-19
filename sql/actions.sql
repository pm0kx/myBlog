/*
Navicat MySQL Data Transfer

Source Server         : mysql
Source Server Version : 50624
Source Host           : localhost:3306
Source Database       : fans_blog

Target Server Type    : MYSQL
Target Server Version : 50624
File Encoding         : 65001

Date: 2018-08-05 15:59:03
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `actions`
-- ----------------------------
DROP TABLE IF EXISTS `actions`;
CREATE TABLE `actions` (
  `status` int(11) DEFAULT NULL COMMENT '状态，1->启用，0->禁用',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creater` varchar(45) DEFAULT NULL,
  `modified_time` datetime DEFAULT NULL COMMENT '修改时间',
  `modifier` varchar(45) DEFAULT NULL,
  `id` varchar(45) NOT NULL,
  `name` varchar(128) DEFAULT NULL,
  `type` varchar(32) DEFAULT NULL,
  `code` varchar(45) DEFAULT NULL,
  `comments` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of actions
-- ----------------------------
INSERT INTO `actions` VALUES ('1', '2018-08-05 15:45:14', 'null', '2018-08-05 15:45:14', 'null', '245ee36b-cbb6-41d4-b1c9-4f7c58869b75', 'swsss', 'admin', 'rrsssss', 'bthgtth');
INSERT INTO `actions` VALUES ('1', '2018-07-22 22:44:47', 'null', '2018-07-22 22:44:47', 'null', '50a20f77-a448-45c3-abf8-203dd3b8690f', 'post', 'post', 'add_post', null);
INSERT INTO `actions` VALUES ('1', '2018-08-05 15:53:15', 'null', '2018-08-05 15:53:15', 'null', 'dcaeab86-ffb6-498e-87e9-71fb5bd52cf8', 'edit a post', 'main', 'edit_post', 'edit_post');
