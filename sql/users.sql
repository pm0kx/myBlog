/*
Navicat MySQL Data Transfer

Source Server         : mysql
Source Server Version : 50624
Source Host           : localhost:3306
Source Database       : fans_blog

Target Server Type    : MYSQL
Target Server Version : 50624
File Encoding         : 65001

Date: 2018-07-27 21:49:48
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `users`
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `status` int(11) DEFAULT NULL COMMENT '状态，1->启用，0->禁用',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creater` varchar(45) DEFAULT NULL,
  `modified_time` datetime DEFAULT NULL COMMENT '修改时间',
  `modifier` varchar(45) DEFAULT NULL,
  `id` varchar(45) NOT NULL,
  `username` varchar(64) DEFAULT NULL,
  `password_hash` varchar(64) DEFAULT NULL COMMENT '加密密文',
  `nick_name` varchar(64) DEFAULT NULL,
  `full_name` varchar(64) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL COMMENT '1:man,0:women',
  `birthday` datetime DEFAULT NULL,
  `address` text,
  `confirmed` tinyint(1) DEFAULT NULL COMMENT '状态，true->已确认，false->未确认',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES ('1', '2018-07-25 22:16:35', 'null', '2018-07-25 22:16:35', 'null', '0afd94a8-fa41-4302-9297-e3fea21694fb', 'abcd', '$2b$12$s02BZIA9SD5dYe855gL/peV3PczrgAfg8RFpmdMnh0iX.q5v94yEq', 'blog', 'test', '1', '1990-12-01 00:00:00', 'china', '0');
INSERT INTO `users` VALUES ('1', '2018-07-25 22:28:05', 'null', '2018-07-25 22:28:05', 'null', '46eb50f1-2529-4223-aded-e6e0638a7e5b', 'sss', '$2b$12$mjB09dEmaIZq2Eav35/rp.7OdgkG/qOrX9uziLuHRMDUnAQDjDg0S', 'stan', 'test1', '0', '1990-12-01 00:00:00', '陕西西安', '0');
INSERT INTO `users` VALUES ('1', '2018-07-22 23:13:30', 'null', '2018-07-22 23:13:30', 'null', '4713ffc3-5db4-4bb7-b890-c891e5c53487', 'zhu', '$2b$12$Zb7Q9J1rntuHAMpF.iyE8eor1Jc0OKfzJ53JvbSMHLg1Z55Aj/are', 'blog', 'test', '1', '1990-12-01 00:00:00', 'asia', '0');
INSERT INTO `users` VALUES ('1', '2018-07-25 22:16:35', 'null', '2018-07-25 22:16:35', 'null', '6557b996-3660-488b-8593-a50a0c574267', 'abcd2', '$2b$12$1Bbvi16Caj/CAF8eBIb3VenxVXkpZDjakvF/tJynF23GEH6K9w9JS', 'blog', 'test', '1', '1990-12-01 00:00:00', 'china', '0');
INSERT INTO `users` VALUES ('1', '2018-07-22 22:44:47', 'null', '2018-07-22 22:44:47', 'null', '8ab42334-ec1e-4722-89e9-09766b4a773d', 'admin', '$2b$12$UVTvSFRCrnSxRpLYF228ZOcDYc7rOWgozKyDKLqoDKeO8wTiesele', 'admin', 'admin', null, null, 'xian', '0');
INSERT INTO `users` VALUES ('1', '2018-07-22 22:44:47', 'null', '2018-07-22 22:44:47', 'null', 'c195c2a1-c6ff-4ffd-a8d3-1485cd8ac590', 'test', '$2b$12$sEwtuhP1mnzTkgqtmd/TkOvFkrO.UtIklYR/WLKagg2NrW3yN/Gvq', 'coder', 'test-name', null, null, 'china', '0');
INSERT INTO `users` VALUES ('1', '2018-07-25 22:16:35', 'null', '2018-07-25 22:16:35', 'null', 'da4ef2e3-1187-4ed9-9224-c10ad7ffbca2', 'abc', '$2b$12$2s5lDhT4QUFj3X4wT5QJd.Q1lRQdbY5CP2KlYDvT3xlJM9MeWGYzq', 'blog', 'test', '1', '1990-12-01 00:00:00', 'china', '0');
INSERT INTO `users` VALUES ('1', '2018-07-27 21:24:13', 'null', '2018-07-27 21:24:13', 'null', 'ef9bd83f-2eed-4a00-b215-cc3fee5ca545', 'abc123', '$2b$12$6oeQoglMojBOfO1sihvFTuDGoUCeDqrSzvdnMwQaaiKMR75cNIGf.', 'blog', 'test', '1', '1990-12-01 00:00:00', 'china', '0');
