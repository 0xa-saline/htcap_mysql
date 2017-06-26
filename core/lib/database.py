# -*- coding: utf-8 -*- 

"""
HTCAP - beta 1
Author: filippo.cavallarin@wearesegment.com

This program is free software; you can redistribute it and/or modify it under 
the terms of the GNU General Public License as published by the Free Software 
Foundation; either version 2 of the License, or (at your option) any later 
version.
"""

import json
from core.lib.request import Request
from core.lib.DB_config import query,execute,executmany

class Database:
	def __init__(self,dbname, report_name = "" , infos = ""):
    		self.dbname = dbname
		self.report_name = report_name
		self.conn = None

	def dict_from_row(self, row):
		return dict(zip(row.keys(), row)) 

	def checkdir(self,url):
		import re
		pawd = re.findall('\?[A-Z]=[A-Z];[A-Z]=[A-Z]',url,re.IGNORECASE)
		##
		#
		##
		if pawd:
			if url.endswith(pawd[0]):
				url = url.replace(pawd[0],'')
			else:
				url = url
		else:
			url =url
		return url


	def save_crawl_info(self, target=None, start_date=None, end_date=None, commandline=None, user_agent=None):
		values = []
		pars = []

		if target:
			values.append(target)

		if start_date:
			values.append(start_date)

		if end_date:
			values.append(end_date)
		else:
			values.append('')

		if commandline:
			values.append(commandline)

		if user_agent:
			values.append(user_agent)
			
		sql = "insert `crawl_info` (`target`,`start_date`,`end_date`,`commandline`,`user_agent`) value (%s,%s,%s,%s,%s)"
		try:
			execute(sql,values)
			result = query("select max(id) from crawl_info")

			for x,v in result[0].iteritems():
				taskid = v

			return taskid
		except Exception as e:
			print str(e)

	def update_crawl_info(self,taskid,endtime):
		if not taskid:
			return
		try:
			sql = "update `crawl_info` set `end_date`=%s where id=%s"
			value = str(endtime),str(taskid)
			execute(sql,value)
		except Exception as e:
			print str(e)

    					

	def save_request(self,request,taskid=''):
		gettype = request.type if request.type else ''
		method = request.method if request.method else ''
		geturl = request.url
		referer = request.referer if request.referer else ''
		redirects = request.redirects if request.redirects else ''
		pdata = request.data if request.data else ''
		cookie = json.dumps([r.get_dict() for r in request.cookies])
		http_auth = request.http_auth if request.http_auth else ''
		out_of_scope = 1 if request.out_of_scope else 0
		trigger = json.dumps(request.trigger) if request.trigger else ''
		html = request.html if request.html else ''
		user_output = json.dumps(request.user_output) if len(request.user_output) > 0 else ''

		sql = "INSERT INTO `request` (`taskid`, `type`, `method`, `url`, `referer`, `redirects`, `data`, `cookies`, `http_auth`,`out_of_scope`,`trigger`,`html`,`user_output`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		newvalue = taskid,gettype,method,self.checkdir(request.url), request.referer,request.redirects,request.data,cookie,http_auth,out_of_scope,trigger,html,user_output


		# include trigger in query to save the same request with different triggers
		# (normally requests are compared using type,method,url and data only) 
		sql_select = "SELECT * FROM `request` WHERE `type`=%s AND `method`=%s AND `url`=%s AND `http_auth`=%s AND `data`=%s and `taskid`=%s"
		sevalue = gettype,method,self.checkdir(request.url),http_auth,pdata,taskid

		try:
			exsit_res = query(sql_select,sevalue)
			if len(exsit_res) == 0:
				execute(sql,newvalue)
				#max = query("select max(id) from `request`")
				#print max[0]
		except  Exception as e:
			print str(e)
			pass


	def save_crawl_result(self, result, crawled):

		if result.request.db_id == 0: # start url has id=0
			return
		qry = "UPDATE request SET crawled=?, crawler_errors=?, html=?, user_output=? WHERE id=?"
		values = (
			1 if crawled else 0,
			json.dumps(result.errors),
			result.request.html if result.request.html else "",
			json.dumps(result.request.user_output) if len(result.request.user_output) > 0 else "",
			result.request.db_id
		)
		try:
			cur = self.conn.cursor()
			cur.execute(qry, values)
		except Exception as e:
			print str(e)
			pass