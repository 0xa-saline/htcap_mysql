## HTCAP

Htcap is a web application scanner able to crawl single page application (SPA) in a recursive manner by intercepting ajax calls and DOM changes.  
Htcap is not just another vulnerability scanner since it's focused mainly on the crawling process and uses external tools to discover vulnerabilities. It's designed to be a tool for both manual and automated penetration test of modern web applications.

More infos at [htcap.org](http://htcap.org).

## SETUP

### Requirements

 1. Python 2.7
 2. PhantomJS v2  [PS:因为PhantomJS作者不再维护PhantomJS项目了..估计这个也不会继续更新了]

### Download and Run

```console
$ git clone https://github.com/0xa-saline/htcap_mysql htcap
$ cd htcap
$ vi core/lib/DB_config.py
	#数据库信息
    'host' : 'localhost',
    'user' : 'root',
    'port' : '3306',
    'password' : 'mysqlroot',
    'db' : 'w3a_scan',
$ sudo pip install -r requirements.txt
$ python htcap.py crawl http://0day5.com

```

使用姿势和原本的一样的

```bash
$ python htcap.py crawl http://testphp.vulnweb.com/
*****************************************************
* / _ \|  _ \  / \ \ / / ___/ ___|  ___ __ _| \ | | *
*| | | | | | |/ _ \ V /|___ \___ \ / __/ _` |  \| | *
*| |_| | |_| / ___ \| |  ___) |__) | (_| (_| | |\  |*
* \___/|____/_/   \_\_| |____/____/ \___\__,_|_| \_|*
*****************************************************
. No handlers could be found for logger "tldextract"
[*][debug] http://testphp.vulnweb.com/pictures/
[*][debug] http://testphp.vulnweb.com/images/
[*][debug] http://testphp.vulnweb.com/bxss/
[*][debug] http://testphp.vulnweb.com/Connections/
[*][debug] http://testphp.vulnweb.com/admin/
[*][debug] http://testphp.vulnweb.com/CVS/
[*][debug] http://testphp.vulnweb.com/secured/
```

PhantomJs can be downloaded [here](http://phantomjs.org//download.html). It comes as a self-contained executable with all libraries linked statically, so there is no need to install or compile anything else.  


## DOCUMENTATION

Documentation, examples and demos can be found at the official website [http://htcap.org](http://htcap.org).


## TO DO

0.禁止dns刷新缓存 done


1.修改htcap的数据库为mysql done


2.增加常见统计代码和分享网站的过滤功能 done


3.增加常见静态后缀的识别 done


4.获取url在原有的robots基础上增加目录爆破和搜索引擎采集.识别一些不能访问的目录 done


5.砍掉sqlmap和Arachni扫描功能. done


6.增加页面信息识别功能.


7.增加重复去重和相似度去重功能


## demo

http://htcap.org/scanme/

<img src="http://htcap.org/scanme/db_screen.png"></img>

## LICENSE

This program is free software; you can redistribute it and/or modify it under the terms of the [GNU General Public License](https://www.gnu.org/licenses/gpl-2.0.html) as published by the Free Software Foundation; either version 2 of the License, or(at your option) any later version.
