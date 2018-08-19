/*
Navicat MySQL Data Transfer

Source Server         : mysql
Source Server Version : 50624
Source Host           : localhost:3306
Source Database       : fans_blog

Target Server Type    : MYSQL
Target Server Version : 50624
File Encoding         : 65001

Date: 2018-07-11 13:05:01
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
  UNIQUE KEY `type` (`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of actions
-- ----------------------------
INSERT INTO `actions` VALUES ('1', '2018-07-08 17:19:30', null, '2018-07-08 17:19:35', null, '9d398f85-15f9-43a1-a750-38128da825f5\r\n\r\n', '新增博客', 'post', 'add_post', null);

-- ----------------------------
-- Table structure for `action_log`
-- ----------------------------
DROP TABLE IF EXISTS `action_log`;
CREATE TABLE `action_log` (
  `id` varchar(45) NOT NULL,
  `action_name` varchar(128) DEFAULT NULL,
  `client_ip` varchar(128) DEFAULT NULL,
  `action_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of action_log
-- ----------------------------

-- ----------------------------
-- Table structure for `alembic_version`
-- ----------------------------
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of alembic_version
-- ----------------------------

-- ----------------------------
-- Table structure for `article`
-- ----------------------------
DROP TABLE IF EXISTS `article`;
CREATE TABLE `article` (
  `status` int(11) DEFAULT NULL COMMENT '状态，1->启用，0->禁用',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creater` varchar(45) DEFAULT NULL,
  `modified_time` datetime DEFAULT NULL COMMENT '修改时间',
  `modifier` varchar(45) DEFAULT NULL,
  `id` varchar(45) NOT NULL,
  `title` varchar(100) NOT NULL,
  `content` text,
  `publish_date` datetime DEFAULT NULL,
  `catalog_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `catalog_id` (`catalog_id`),
  CONSTRAINT `article_ibfk_1` FOREIGN KEY (`catalog_id`) REFERENCES `catalog` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of article
-- ----------------------------

-- ----------------------------
-- Table structure for `attachments`
-- ----------------------------
DROP TABLE IF EXISTS `attachments`;
CREATE TABLE `attachments` (
  `id` varchar(45) NOT NULL,
  `attach_name` varchar(255) DEFAULT NULL,
  `path` text,
  `belong_type` varchar(45) DEFAULT NULL,
  `belong_id` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of attachments
-- ----------------------------

-- ----------------------------
-- Table structure for `catalog`
-- ----------------------------
DROP TABLE IF EXISTS `catalog`;
CREATE TABLE `catalog` (
  `status` int(11) DEFAULT NULL COMMENT '状态，1->启用，0->禁用',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creater` varchar(45) DEFAULT NULL,
  `modified_time` datetime DEFAULT NULL COMMENT '修改时间',
  `modifier` varchar(45) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(40) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of catalog
-- ----------------------------

-- ----------------------------
-- Table structure for `comments`
-- ----------------------------
DROP TABLE IF EXISTS `comments`;
CREATE TABLE `comments` (
  `status` int(11) DEFAULT NULL COMMENT '状态，1->启用，0->禁用',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creater` varchar(45) DEFAULT NULL,
  `modified_time` datetime DEFAULT NULL COMMENT '修改时间',
  `modifier` varchar(45) DEFAULT NULL,
  `id` varchar(45) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `text` text,
  `date` datetime DEFAULT NULL,
  `post_id` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `post_id` (`post_id`),
  CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of comments
-- ----------------------------

-- ----------------------------
-- Table structure for `group`
-- ----------------------------
DROP TABLE IF EXISTS `group`;
CREATE TABLE `group` (
  `status` int(11) DEFAULT NULL COMMENT '状态，1->启用，0->禁用',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creater` varchar(45) DEFAULT NULL,
  `modified_time` datetime DEFAULT NULL COMMENT '修改时间',
  `modifier` varchar(45) DEFAULT NULL,
  `id` varchar(45) NOT NULL,
  `group_name` varchar(64) DEFAULT NULL,
  `parent_id` varchar(45) DEFAULT NULL,
  `comments` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of group
-- ----------------------------

-- ----------------------------
-- Table structure for `mails`
-- ----------------------------
DROP TABLE IF EXISTS `mails`;
CREATE TABLE `mails` (
  `status` int(11) DEFAULT NULL COMMENT '状态，1->启用，0->禁用',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creater` varchar(45) DEFAULT NULL,
  `modified_time` datetime DEFAULT NULL COMMENT '修改时间',
  `modifier` varchar(45) DEFAULT NULL,
  `id` varchar(45) NOT NULL,
  `date` datetime DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `text` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of mails
-- ----------------------------

-- ----------------------------
-- Table structure for `posts`
-- ----------------------------
DROP TABLE IF EXISTS `posts`;
CREATE TABLE `posts` (
  `status` int(11) DEFAULT NULL COMMENT '状态，1->启用，0->禁用',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creater` varchar(45) DEFAULT NULL,
  `modified_time` datetime DEFAULT NULL COMMENT '修改时间',
  `modifier` varchar(45) DEFAULT NULL,
  `id` varchar(45) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `text` text,
  `publish_date` datetime DEFAULT NULL,
  `user_id` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `posts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of posts
-- ----------------------------
INSERT INTO `posts` VALUES ('1', '2018-07-08 16:48:51', 'null', '2018-07-08 16:48:51', 'null', '0f86e988-2def-4f41-9c0b-1cce00e96cf8', 'post1', 'u7K7TBozXz+#hSyJ9pT22v15v===ZR4sLbalnlQ-!-x!K+JgSoZh%qz9gdCv-7wJ', '2018-07-08 16:49:36', '6b497c67-2fda-4c3f-9632-1c4ea2c6c7d9');
INSERT INTO `posts` VALUES ('1', '2018-07-08 16:48:51', 'null', '2018-07-08 16:48:51', 'null', '1c6fe0f2-0873-499a-b766-5e0c330ce6d6', 'post5', 'Y0=A^YTYspM-T2e8XyzqiG0R11i3+Jo-k6wtaHLAh3l1q0V375wYzT9Xn2UDyB^f', '2018-07-08 16:49:36', '6b497c67-2fda-4c3f-9632-1c4ea2c6c7d9');
INSERT INTO `posts` VALUES ('1', '2018-07-08 16:48:51', 'null', '2018-07-08 16:48:51', 'null', '32ee7587-82f7-4945-8d94-4c59378cd3ec', 'post0', 'RWI!5lE$d4akFz=NQ9MX!K*hs!qF2Fol1a*xnLfL369nMIz0&0WEI*Z2eYXVo(1l', '2018-07-08 16:49:36', '6b497c67-2fda-4c3f-9632-1c4ea2c6c7d9');
INSERT INTO `posts` VALUES ('1', '2018-07-08 16:48:51', 'null', '2018-07-08 16:48:51', 'null', '33104216-f82e-48aa-8a9e-cdd20373e888', 'post8', 'ONnNl6IOQ%5DmV8gJvPNSf3RJxcmId+GlL@$ODjlSUVlSMyb90FCVbo_AQkXEJ!-', '2018-07-08 16:49:36', '6b497c67-2fda-4c3f-9632-1c4ea2c6c7d9');
INSERT INTO `posts` VALUES ('1', '2018-07-08 16:48:51', 'null', '2018-07-08 16:48:51', 'null', '41303eed-427d-459c-b87e-f2a35d89df39', 'post6', '7z&TEKeqCJ&RX-=9-lyVl-xlaGuJG+O!ZATS+f-(5#OptnTHlugmyWCp*EpjH2NG', '2018-07-08 16:49:36', '6b497c67-2fda-4c3f-9632-1c4ea2c6c7d9');
INSERT INTO `posts` VALUES ('1', '2018-07-08 17:13:39', 'null', '2018-07-08 17:13:39', 'null', '42d15c60-ffa6-4d50-9486-f54a126a6910', 'Python 测试', '<p>权限管理功能的实现可以分为以下几个小块：&nbsp;<br />\r\n1，新建数据库表Role，里面包括id（Integer，主键）name（String），permission（Integer），default(boolean)。users是指向User模型的对外关系，反向赋给User模型一个role属性，这样就可以同郭User.role来访问Role模型，这样就创建了数据库之间的关系。模型里面还定义了一个静态方法（@staticmethod,可以直接通过类访问这个方法而不需要创建实例之后才能访问这个方法），它的作用是初始化Role数据表中的数据，数据库模型代码如下：</p>\r\n', '2018-07-08 17:15:11', '6b497c67-2fda-4c3f-9632-1c4ea2c6c7d9');
INSERT INTO `posts` VALUES ('1', '2018-07-08 16:48:51', 'null', '2018-07-08 16:48:51', 'null', '68228b36-5baa-4999-9dca-bfaf66b46c9f', 'post4', 'yfFqb@i^Hhq+esxhUdGf8^cIktRCau1Fa_O#gl*uDSgMyj$uMwT&s+4PIg3N2wt2', '2018-07-08 16:49:36', '6b497c67-2fda-4c3f-9632-1c4ea2c6c7d9');
INSERT INTO `posts` VALUES ('1', '2018-07-08 16:48:51', 'null', '2018-07-08 16:48:51', 'null', '6c134e00-2840-48b9-a887-21fa74b7856d', 'post2', 'l*d=qUELX4pxe)!KonszLuzi_L4*4phfUd&k(AS00CKIApH=+Q5%*4MRiEKqZKsJ', '2018-07-08 16:49:36', '6b497c67-2fda-4c3f-9632-1c4ea2c6c7d9');
INSERT INTO `posts` VALUES ('1', '2018-07-08 16:48:51', 'null', '2018-07-08 16:48:51', 'null', 'a46d0807-d059-43a3-9b3e-92fef16fafbe', 'post7', 'BNK61LSlId-+S8&1Y0g5L8CeNL_NXzgNcq)wNowt3D2fnxV2!rq5^1WmKfVfE)lw', '2018-07-08 16:49:36', '6b497c67-2fda-4c3f-9632-1c4ea2c6c7d9');
INSERT INTO `posts` VALUES ('1', '2018-07-08 16:48:51', 'null', '2018-07-08 16:48:51', 'null', 'a9767321-24a1-4e80-a24d-0b073d22984a', 'post3', '+xK1^o7^n4-(xr_wm)xT(OxY#q8%SHNjz56vEm7i=0#WAh6x@6scgET0+i85SR8h', '2018-07-08 16:49:36', '6b497c67-2fda-4c3f-9632-1c4ea2c6c7d9');
INSERT INTO `posts` VALUES ('1', '2018-07-08 16:48:51', 'null', '2018-07-08 16:48:51', 'null', 'c22ac539-c8c9-4b1a-8a8b-7472166bfc7c', 'post9', '6ciZtvs9jhzh(#WW7B-x$diA9jJsq7slp2&E9Ne5O80GUqx7gmtL%I3-$WC_hqhr', '2018-07-08 16:49:36', '6b497c67-2fda-4c3f-9632-1c4ea2c6c7d9');

-- ----------------------------
-- Table structure for `posts_tags`
-- ----------------------------
DROP TABLE IF EXISTS `posts_tags`;
CREATE TABLE `posts_tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `post_id` varchar(45) DEFAULT NULL,
  `tag_id` varchar(45) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `post_id` (`post_id`),
  KEY `tag_id` (`tag_id`),
  CONSTRAINT `posts_tags_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`),
  CONSTRAINT `posts_tags_ibfk_2` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of posts_tags
-- ----------------------------
INSERT INTO `posts_tags` VALUES ('1', '0f86e988-2def-4f41-9c0b-1cce00e96cf8', '205f585e-fd2c-4fce-9fa9-a4c320102745', null);
INSERT INTO `posts_tags` VALUES ('2', '0f86e988-2def-4f41-9c0b-1cce00e96cf8', '75137a74-ebff-4b3e-8caf-80250a9cad8b', null);
INSERT INTO `posts_tags` VALUES ('3', '41303eed-427d-459c-b87e-f2a35d89df39', '36051d51-e4b4-4454-8ca4-23915b00ad7f', null);
INSERT INTO `posts_tags` VALUES ('4', '41303eed-427d-459c-b87e-f2a35d89df39', '205f585e-fd2c-4fce-9fa9-a4c320102745', null);
INSERT INTO `posts_tags` VALUES ('5', '41303eed-427d-459c-b87e-f2a35d89df39', '75137a74-ebff-4b3e-8caf-80250a9cad8b', null);
INSERT INTO `posts_tags` VALUES ('6', 'a46d0807-d059-43a3-9b3e-92fef16fafbe', '75137a74-ebff-4b3e-8caf-80250a9cad8b', null);
INSERT INTO `posts_tags` VALUES ('7', 'a46d0807-d059-43a3-9b3e-92fef16fafbe', '36051d51-e4b4-4454-8ca4-23915b00ad7f', null);
INSERT INTO `posts_tags` VALUES ('8', 'a46d0807-d059-43a3-9b3e-92fef16fafbe', 'b410b77a-9466-4868-a93d-cc6315004e8d', null);
INSERT INTO `posts_tags` VALUES ('9', 'a46d0807-d059-43a3-9b3e-92fef16fafbe', '205f585e-fd2c-4fce-9fa9-a4c320102745', null);
INSERT INTO `posts_tags` VALUES ('10', 'a9767321-24a1-4e80-a24d-0b073d22984a', 'b410b77a-9466-4868-a93d-cc6315004e8d', null);
INSERT INTO `posts_tags` VALUES ('11', 'a9767321-24a1-4e80-a24d-0b073d22984a', '205f585e-fd2c-4fce-9fa9-a4c320102745', null);
INSERT INTO `posts_tags` VALUES ('12', '33104216-f82e-48aa-8a9e-cdd20373e888', 'b410b77a-9466-4868-a93d-cc6315004e8d', null);
INSERT INTO `posts_tags` VALUES ('13', '33104216-f82e-48aa-8a9e-cdd20373e888', '36051d51-e4b4-4454-8ca4-23915b00ad7f', null);
INSERT INTO `posts_tags` VALUES ('14', '33104216-f82e-48aa-8a9e-cdd20373e888', '205f585e-fd2c-4fce-9fa9-a4c320102745', null);
INSERT INTO `posts_tags` VALUES ('15', '1c6fe0f2-0873-499a-b766-5e0c330ce6d6', '75137a74-ebff-4b3e-8caf-80250a9cad8b', null);
INSERT INTO `posts_tags` VALUES ('16', '6c134e00-2840-48b9-a887-21fa74b7856d', 'b410b77a-9466-4868-a93d-cc6315004e8d', null);
INSERT INTO `posts_tags` VALUES ('17', '6c134e00-2840-48b9-a887-21fa74b7856d', '36051d51-e4b4-4454-8ca4-23915b00ad7f', null);
INSERT INTO `posts_tags` VALUES ('18', '32ee7587-82f7-4945-8d94-4c59378cd3ec', '75137a74-ebff-4b3e-8caf-80250a9cad8b', null);
INSERT INTO `posts_tags` VALUES ('19', '32ee7587-82f7-4945-8d94-4c59378cd3ec', 'b410b77a-9466-4868-a93d-cc6315004e8d', null);
INSERT INTO `posts_tags` VALUES ('20', '32ee7587-82f7-4945-8d94-4c59378cd3ec', '36051d51-e4b4-4454-8ca4-23915b00ad7f', null);
INSERT INTO `posts_tags` VALUES ('21', '32ee7587-82f7-4945-8d94-4c59378cd3ec', '205f585e-fd2c-4fce-9fa9-a4c320102745', null);
INSERT INTO `posts_tags` VALUES ('22', 'c22ac539-c8c9-4b1a-8a8b-7472166bfc7c', 'b410b77a-9466-4868-a93d-cc6315004e8d', null);
INSERT INTO `posts_tags` VALUES ('23', 'c22ac539-c8c9-4b1a-8a8b-7472166bfc7c', '75137a74-ebff-4b3e-8caf-80250a9cad8b', null);
INSERT INTO `posts_tags` VALUES ('24', '68228b36-5baa-4999-9dca-bfaf66b46c9f', '36051d51-e4b4-4454-8ca4-23915b00ad7f', null);
INSERT INTO `posts_tags` VALUES ('25', '68228b36-5baa-4999-9dca-bfaf66b46c9f', '75137a74-ebff-4b3e-8caf-80250a9cad8b', null);
INSERT INTO `posts_tags` VALUES ('26', '68228b36-5baa-4999-9dca-bfaf66b46c9f', '205f585e-fd2c-4fce-9fa9-a4c320102745', null);
INSERT INTO `posts_tags` VALUES ('27', '42d15c60-ffa6-4d50-9486-f54a126a6910', '205f585e-fd2c-4fce-9fa9-a4c320102745', null);

-- ----------------------------
-- Table structure for `resources`
-- ----------------------------
DROP TABLE IF EXISTS `resources`;
CREATE TABLE `resources` (
  `status` int(11) DEFAULT NULL COMMENT '状态，1->启用，0->禁用',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creater` varchar(45) DEFAULT NULL,
  `modified_time` datetime DEFAULT NULL COMMENT '修改时间',
  `modifier` varchar(45) DEFAULT NULL,
  `id` varchar(45) NOT NULL,
  `name` varchar(128) DEFAULT NULL,
  `icon` varchar(50) DEFAULT NULL,
  `url` varchar(250) DEFAULT NULL,
  `order` smallint(6) DEFAULT NULL,
  `bg_color` varchar(50) DEFAULT NULL,
  `comments` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of resources
-- ----------------------------

-- ----------------------------
-- Table structure for `roles`
-- ----------------------------
DROP TABLE IF EXISTS `roles`;
CREATE TABLE `roles` (
  `status` int(11) DEFAULT NULL COMMENT '状态，1->启用，0->禁用',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creater` varchar(45) DEFAULT NULL,
  `modified_time` datetime DEFAULT NULL COMMENT '修改时间',
  `modifier` varchar(45) DEFAULT NULL,
  `id` varchar(45) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of roles
-- ----------------------------
INSERT INTO `roles` VALUES ('1', '2018-07-08 16:42:08', 'null', '2018-07-08 16:42:08', 'null', 'ae4bb4fd-8c94-4731-8a4f-f38ecec06392', 'admin', null);
INSERT INTO `roles` VALUES ('2', '2018-07-08 17:46:18', null, '2018-07-08 17:46:21', null, 'da60f911-785d-4d31-b499-e68d71767690\r\n\r\n', 'poster', null);

-- ----------------------------
-- Table structure for `roles_actions`
-- ----------------------------
DROP TABLE IF EXISTS `roles_actions`;
CREATE TABLE `roles_actions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_id` varchar(45) DEFAULT NULL,
  `role_id` varchar(45) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `action_id` (`action_id`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `roles_actions_ibfk_1` FOREIGN KEY (`action_id`) REFERENCES `actions` (`id`),
  CONSTRAINT `roles_actions_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of roles_actions
-- ----------------------------
INSERT INTO `roles_actions` VALUES ('1', '9d398f85-15f9-43a1-a750-38128da825f5\r\n\r\n', 'da60f911-785d-4d31-b499-e68d71767690\r\n\r\n', '1');

-- ----------------------------
-- Table structure for `roles_resources`
-- ----------------------------
DROP TABLE IF EXISTS `roles_resources`;
CREATE TABLE `roles_resources` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_id` varchar(45) DEFAULT NULL,
  `resource_id` varchar(45) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `role_id` (`role_id`),
  KEY `resource_id` (`resource_id`),
  CONSTRAINT `roles_resources_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`),
  CONSTRAINT `roles_resources_ibfk_2` FOREIGN KEY (`resource_id`) REFERENCES `resources` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of roles_resources
-- ----------------------------

-- ----------------------------
-- Table structure for `tags`
-- ----------------------------
DROP TABLE IF EXISTS `tags`;
CREATE TABLE `tags` (
  `status` int(11) DEFAULT NULL COMMENT '状态，1->启用，0->禁用',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creater` varchar(45) DEFAULT NULL,
  `modified_time` datetime DEFAULT NULL COMMENT '修改时间',
  `modifier` varchar(45) DEFAULT NULL,
  `id` varchar(45) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of tags
-- ----------------------------
INSERT INTO `tags` VALUES ('1', '2018-07-08 16:48:51', 'null', '2018-07-08 16:48:51', 'null', '205f585e-fd2c-4fce-9fa9-a4c320102745', 'popular');
INSERT INTO `tags` VALUES ('1', '2018-07-08 16:48:51', 'null', '2018-07-08 16:48:51', 'null', '36051d51-e4b4-4454-8ca4-23915b00ad7f', 'classic');
INSERT INTO `tags` VALUES ('1', '2018-07-08 16:48:51', 'null', '2018-07-08 16:48:51', 'null', '75137a74-ebff-4b3e-8caf-80250a9cad8b', 'diary');
INSERT INTO `tags` VALUES ('1', '2018-07-08 16:48:51', 'null', '2018-07-08 16:48:51', 'null', 'b410b77a-9466-4868-a93d-cc6315004e8d', 'faddish');

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
  `_password` varchar(64) DEFAULT NULL COMMENT '加密密文',
  `nick_name` varchar(64) DEFAULT NULL,
  `full_name` varchar(64) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL COMMENT '1:man,0:women',
  `birthday` datetime DEFAULT NULL,
  `address` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES ('1', '2018-07-08 16:38:57', 'null', '2018-07-08 16:38:57', 'null', '6b497c67-2fda-4c3f-9632-1c4ea2c6c7d9', 'admin', '$2b$12$9LU8uN9cHHoZer1lTy9gVeRSsQ/B0.yhsiQRRyTxC6x4LGGnyrOcq', 'zhu', 'zhu', null, null, 'china');
INSERT INTO `users` VALUES ('1', '2018-07-08 16:50:49', 'null', '2018-07-08 16:50:49', 'null', '7b5484bb-6e90-4f8e-818c-d022086cfd44', 'stan', '$2b$12$abk0tdhOuRIGiKx4VFhCDuYdpApliXWucc8BsI5.pN28VkQHeLi7u', 'stan', '无名', '1', '1088-12-01 00:00:00', '陕西西安');

-- ----------------------------
-- Table structure for `users_roles`
-- ----------------------------
DROP TABLE IF EXISTS `users_roles`;
CREATE TABLE `users_roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(45) DEFAULT NULL,
  `role_id` varchar(45) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `users_roles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `users_roles_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of users_roles
-- ----------------------------
INSERT INTO `users_roles` VALUES ('1', '6b497c67-2fda-4c3f-9632-1c4ea2c6c7d9', 'ae4bb4fd-8c94-4731-8a4f-f38ecec06392', '1');
INSERT INTO `users_roles` VALUES ('2', '7b5484bb-6e90-4f8e-818c-d022086cfd44', 'da60f911-785d-4d31-b499-e68d71767690\r\n\r\n', '1');

-- ----------------------------
-- Table structure for `user_group`
-- ----------------------------
DROP TABLE IF EXISTS `user_group`;
CREATE TABLE `user_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(45) DEFAULT NULL,
  `group_id` varchar(45) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `group_id` (`group_id`),
  CONSTRAINT `user_group_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `user_group_ibfk_2` FOREIGN KEY (`group_id`) REFERENCES `group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user_group
-- ----------------------------
