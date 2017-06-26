# -*- coding: utf-8 -*- 

"""
HTCAP - beta 1
Author: filippo.cavallarin@wearesegment.com

This program is free software; you can redistribute it and/or modify it under 
the terms of the GNU General Public License as published by the Free Software 
Foundation; either version 2 of the License, or (at your option) any later 
version.
"""


class Shared:
	"""
	data shared between threads
	"""
	
	main_condition = None
	th_condition = None

	requests = []
	requests_index = 0
	crawl_results = []

	starturl = ""
	start_cookies = []
	allowed_domains = set()
	excluded_urls = set()	
	
	options = {}	

