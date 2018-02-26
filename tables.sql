CREATE TABLE `deep_user` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(128) NOT NULL,
  `password` varchar(128) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE `deep_company` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) DEFAULT NULL,
  `address` varchar(50) DEFAULT NULL,
  `contact` varchar(50) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `products` varchar(1024) DEFAULT NULL,
  `machines` varchar(1024) DEFAULT NULL,
  `tags` varchar(1024) DEFAULT NULL,
  `info` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=gbk;

CREATE TABLE `deep_line` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `full_name` varchar(256) DEFAULT NULL,
  `name` varchar(128) DEFAULT NULL,
  `shazhi` varchar(128) DEFAULT NULL,
  `guangzedu` varchar(128) DEFAULT NULL,
  `jianian` varchar(128) DEFAULT NULL,
  `jianianfangxiang` varchar(128) DEFAULT NULL,
  `pailie` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=gbk;

CREATE TABLE `deep_order` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `user_id` int(10) NOT NULL,
  `class` int(5) DEFAULT NULL,
  `subclass` int(5) DEFAULT NULL,
  `name_num` varchar(20) DEFAULT NULL,
  `name` varchar(30) NOT NULL,
  `cf` varchar(30) DEFAULT NULL,
  `zz` varchar(20) DEFAULT NULL,
  `js` varchar(30) DEFAULT NULL,
  `ws` varchar(30) DEFAULT NULL,
  `jss` varchar(30) DEFAULT NULL,
  `wss` varchar(30) DEFAULT NULL,
  `md` varchar(20) DEFAULT NULL,
  `cpmd` varchar(20) DEFAULT NULL,
  `xjmf` int(10) DEFAULT NULL,
  `cpkz` int(10) DEFAULT NULL,
  `kz` int(10) DEFAULT NULL,
  `type` varchar(10) DEFAULT NULL,
  `zjtype` varchar(10) DEFAULT NULL,
  `jg` double(10,2) DEFAULT NULL,
  `cpy` varchar(4) DEFAULT NULL,
  `kcl` varchar(50) DEFAULT NULL COMMENT '图片',
  `cpmf` int(10) DEFAULT NULL,
  `sjmf` int(10) DEFAULT NULL,
  `report` int(2) DEFAULT '0',
  `addtime` varchar(10) DEFAULT NULL,
  `info` text,
  `gm` int(10) DEFAULT NULL,
  `isjb` int(2) DEFAULT '0',
  `checknum` int(10) DEFAULT '0',
  `zjxl` varchar(50) DEFAULT NULL,
  `ylpp` varchar(50) DEFAULT NULL,
  `ssl` varchar(50) DEFAULT NULL,
  `pz` varchar(100) DEFAULT NULL,
  `kjl` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=gbk;