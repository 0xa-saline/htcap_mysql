'''
crawl_info
'''
DROP TABLE IF EXISTS `crawl_info`;
CREATE TABLE IF NOT EXISTS `crawl_info` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`target` varchar(255)  NOT NULL  COMMENT '扫描目标',
	`start_date` varchar(255)  NOT NULL  COMMENT '扫描开始时间',
	`end_date` varchar(255)  NOT NULL  COMMENT '扫描结束时间',
	`commandline` varchar(255)  NOT NULL  COMMENT '扫描执行的命令',
	`user_agent` varchar(255)  NOT NULL  COMMENT '扫描的ua',
	PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

INSERT INTO crawl_info VALUES('1.0.1 - dev','http://testphp.vulnweb.com/',1498273975,NULL,'-d testphp.vulnweb.com http://testphp.vulnweb.com t.db','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36');
'''
request
'''

DROP TABLE IF EXISTS `request`;
CREATE TABLE IF NOT EXISTS `request` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`id_parent` int(11)  COMMENT '节点',
	`type` varchar(255)  COMMENT '类型',
	`method` varchar(255) NOT NULL  COMMENT '请求类型',
	`url` varchar(255) NOT NULL  COMMENT '地址',
	`referer` varchar(255)  COMMENT '来路',
	`redirects` enum('0','1') NOT NULL DEFAULT '0'  COMMENT '什么鬼',
	`data`  varchar(255) NOT NULL  COMMENT '参数',
	`cookies`  varchar(255)  COMMENT 'cookie',
	`http_auth`  varchar(255)  COMMENT 'http认证',
	`out_of_scope` varchar(255),
	`trigger` varchar(255),
	`crawled` INTEGER NOT NULL DEFAULT 0,
	`crawler_errors` TEXT,
	`html` TEXT,
	`user_output` TEXT,
	PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

INSERT INTO request VALUES(1,NULL,'link','GET','http://testphp.vulnweb.com/guestbook.php','http://testphp.vulnweb.com/',0,'','[]','',0,'',1,'[]','','');
INSERT INTO request VALUES(2,NULL,'link','GET','http://testphp.vulnweb.com/','http://testphp.vulnweb.com/pictures/',0,'','[]','',0,'',0,NULL,'','');
INSERT INTO request VALUES(3,NULL,'link','GET','http://testphp.vulnweb.com/pictures/1.jpg.tn','http://testphp.vulnweb.com/pictures/',0,'','[]','',0,'',1,'[\'contentType\']','','');
INSERT INTO request VALUES(4,NULL,'link','GET','http://testphp.vulnweb.com/pictures/2.jpg.tn','http://testphp.vulnweb.com/pictures/',0,'','[]','',0,'',1,'[\'contentType\']','','');
INSERT INTO request VALUES(5,NULL,'link','GET','http://testphp.vulnweb.com/pictures/3.jpg.tn','http://testphp.vulnweb.com/pictures/',0,'','[]','',0,'',1,'[\'contentType\']','','');

'''
request_child
'''
DROP TABLE IF EXISTS `request_child`;
CREATE TABLE IF NOT EXISTS `request_child` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`id_request` INTEGER NOT NULL,
	`id_child` INTEGER NOT NULL,
	PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
