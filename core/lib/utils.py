# -*- coding: utf-8 -*- 

"""
HTCAP - beta 1
Author: filippo.cavallarin@wearesegment.com

This program is free software; you can redistribute it and/or modify it under 
the terms of the GNU General Public License as published by the Free Software 
Foundation; either version 2 of the License, or (at your option) any later 
version.
"""

import sys
import os
import time
import pipes
import re
import posixpath

from urlparse import urlsplit, urljoin, parse_qsl
from core.lib.exception import *
from core.constants import *
from core.crawl.lib.shared import *


def generate_filename(name, ext=None, out_file_overwrite=False, ask_out_file_overwrite=False):

	def fname():
		return ".".join([f for f in ft if f])

	ft = name.split(".")

	if not ext and len(ft) > 1:
		ext = ft[-1]

	# remove extension if present in name and equal to ext
	if ft[-1] == ext: ft.pop()

	# always append ext, even if None
	ft.append(ext)

	if ask_out_file_overwrite and os.path.exists(fname()):
		try:
			sys.stdout.write("File %s already exists. Overwrite [y/N]: " % fname())
			out_file_overwrite = sys.stdin.read(1) == "y"
		except KeyboardInterrupt:
			print "\nAborted"
			sys.exit(0)

	if not out_file_overwrite:
		bn = ft[-2]
		i = 1
		while os.path.exists(fname()):
			ft[-2] = "%s-%d" % (bn, i)
			i += 1

	return fname()


def cmd_to_str(cmd):
	ecmd = [pipes.quote(o) for o in cmd]
	return " ".join(ecmd)


def stdoutw(str):
	sys.stdout.write(str)
	sys.stdout.flush()


def getrealdir(path):
	return os.path.dirname(os.path.realpath(path)) + os.sep 



def print_progressbar(tot, scanned, start_time, label):
	perc = (scanned * 33) / (tot if tot > 0 else 1)
	sys.stdout.write("\b"*150)
	out = "[%s%s]   %d of %d %s in %d minutes" % ("="*perc, " "*(33-perc), scanned, tot, label, int(time.time() - start_time) / 60)
	stdoutw(out)


def join_qsl(qs):
	"""
	join a list returned by parse_qsl
	do not use urlencode since it will encode values and not just join tuples
	"""
	return "&".join(["%s=%s" % (k,v) for k,v in qs])


# ?a=1&a=2&a=3 -> ?a=3, ?a[]=1&a[]=2&a[]=3 -> UNCHANGED
def group_qs_params(url):
	purl = urlsplit(url)
	qs = parse_qsl(purl.query)
	nqs = list()

	for t in reversed(qs):
		if t[0].endswith("[]") or t[0] not in [f for f,_ in nqs]:
			nqs.append(t)


	purl = purl._replace(query = join_qsl(reversed(nqs)))

	return purl.geturl();



def normalize_url(url):
	# add http if scheme is not present 
	# if an url like 'test.com:80//path' is passed to urlsplit the result is:
	# (scheme='test.com',  path='80//path', ...)
	if not re.match("^[a-z]+://", url, re.I):
		url = "http://%s" % url

	purl = urlsplit(url)

	# no path and no query_string .. just ensure url ends with /
	if not purl.path:
		return "%s/" % purl.geturl()

	# group multiple / (path//to///file -> path/to/file)
	new_path = re.sub(r"/+","/", purl.path)
	# normalize ../../../
	new_path = posixpath.normpath(new_path)
	if purl.path.endswith('/') and not new_path.endswith('/'):
		new_path += '/'

	purl = purl._replace(path = new_path)

	return purl.geturl()




def extract_http_auth(url):
	"""
	returns a tuple with httpauth string and the original url with http auth removed
	http://foo:bar@example.local -> (foo:bar, http://example.local)
	"""

	purl = urlsplit(url)
	if not purl.netloc:
		return (None, url)
	try:
		auth, netloc = purl.netloc.split("@", 1)
	except:
		return (None, url)


	purl = purl._replace(netloc=netloc)

	return (auth, purl.geturl())




def remove_tokens(query):
	"""
	tries to detect and remove tokens from a query string
	used to compare request ignoring, for example, CSRF tokens
	"""

	qs = parse_qsl(query)
	nqs = []
	for k,v in qs:
		if len(v) < 32 or not re.match(r'^[a-z0-9\-_\.:=]+$', v, re.I):
			nqs.append((k,v))

	return join_qsl(nqs)


def get_phantomjs_cmd():
	standard_paths = [os.getcwd()]
	envpath = os.environ['PATH'].split(os.pathsep)
	exe_name = "phantomjs"

	if sys.platform != "win32":
		# force check to standard paths in case $PATH is not set (ie crontab)
		standard_paths.extend(["/usr/bin", "/usr/local/bin", "/usr/share/bin"])
	else:
		exe_name = "%s.exe" % exe_name

	exe_paths = ["%s%s%s" % (p, os.sep, exe_name) for p in standard_paths + envpath]

	for exe in exe_paths:
		if os.path.isfile(exe):
			return [exe, "--ignore-ssl-errors=yes", "--web-security=false", "--ssl-protocol=any", "--load-images=false","--debug=false","--load-images=no"]

	return None



def url_is_valid(url):
	purl = urlsplit(url)

	if not purl.scheme or not purl.netloc:
		return False

	# ensure netloc is in the form "something dot something"
	#if not re.match(r'^[^\.]+\..*(?<!\.)$', purl.netloc, re.I):
	if not re.match(r'^.+\..+$', purl.netloc):
		return False

	return True

class HostFilter(object):
    
    def __init__(self, url):
        self.host = url
		
    def isip(self,host):
        '''
        match host is IP
        '''
        pattern = "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
        regex = re.compile(pattern)
        if regex.match(host):
            return True
        return False

    def get_subsititute(self,host):
        from tld import get_tld
        if not self.isip(host):
            try:
                domain = get_tld('http://'+host)
            except Exception as e:
                domain = host
            
            return domain
        else:
            return host

    #获取根域名
    def urlfilter(self):
        import urlparse,os

        IGNORE_DOMAIN = [	#强制过滤域名.常见的bat和一些统计分享类的网站
    		'taobao.com','51.la','weibo.com','qq.com','t.cn','baidu.com','gravatar.com','cnzz.com','51yes.com',
    		'google-analytics.com','tanx.com','360.cn','yy.com','163.com','263.com','eqxiu.com','','gnu.org','github.com',
			'facebook.com','twitter.com','google.com'
    	]

        IGNORE_EXT = [ #强制过滤后缀.from sqlmap
    		".css", ".js", ".3ds", ".ttf", ".3g2", ".3gp", ".7z", ".DS_Store", ".a", ".aac", ".adp", ".ai", ".aif", 
    		".aiff", ".apk", ".ar", ".asf", ".au", ".avi", ".bak", ".bin", ".bk", ".bmp", ".btif", ".bz2", ".cab", ".caf", 
    		".cgm", ".cmx", ".cpio", ".cr2", ".dat", ".deb", ".djvu", ".dll", ".dmg", ".dmp", ".dng", ".doc", ".docx", 
    		".dot", ".dotx", ".dra", ".dsk", ".dts", ".dtshd", ".dvb", ".dwg", ".dxf", ".ear", ".ecelp4800", ".ecelp7470", 
    		".ecelp9600", ".egg", ".eol", ".eot", ".epub", ".exe", ".f4v", ".fbs", ".fh", ".fla", ".flac", ".fli", ".flv", 
    		".fpx", ".fst", ".fvt", ".g3", ".gif", ".gz", ".h261", ".h263", ".h264", ".ico", ".ief", ".image", ".img", 
    		".ipa", ".iso", ".jar", ".jpeg", ".jpg", ".jpgv", ".jpm", ".jxr", ".ktx", ".lvp", ".lz", ".lzma", ".lzo", 
    		".m3u", ".m4a", ".m4v", ".mar", ".mdi", ".mid", ".mj2",".ttf",".ico",".mka", ".mkv", ".mmr", ".mng", ".mov", 
    		".movie", ".mp3", ".mp4", ".mp4a", ".mpeg", ".mpg", ".mpga", ".mxu", ".nef", ".npx", ".o", ".oga", ".ogg", 
    		".ogv", ".otf", ".pbm", ".pcx", ".pdf", ".pea", ".pgm", ".pic", ".png", ".pnm", ".ppm", ".pps", ".ppt", 
    		".pptx", ".ps", ".psd", ".pya", ".pyc", ".pyo", ".pyv", ".qt", ".rar", ".ras", ".raw", ".rgb", ".rip", 
    		".rlc", ".rz", ".s3m", ".s7z", ".scm", ".scpt", ".sgi", ".shar", ".sil", ".smv", ".so", ".sub", ".swf", 
    		".tar", ".tbz2", ".tga", ".tgz", ".tif", ".tiff", ".tlz", ".ts", ".ttf", ".uvh", ".uvi", ".uvm", ".uvp", 
    		".uvs", ".uvu", ".viv", ".vob", ".war", ".wav", ".wax", ".wbmp", ".wdp", ".weba", ".webm", ".webp", ".whl", 
    		".wm", ".wma", ".wmv", ".wmx", ".woff", ".woff2", ".wvx", ".xbm", ".xif", ".xls", ".xlsx", ".xlt", ".xm", 
    		".xpi", ".xpm", ".xwd", ".xz", ".z", ".zip", ".zipx",".axd"
    	]
        
        parser = urlparse.urlparse(self.host)

        file_ext = os.path.splitext(parser.path)[-1]

        host = self.get_subsititute(parser.netloc)
        host = host.replace('http:','').replace('https:','')

        #print WebProbe(self.host)
        
        if host in IGNORE_DOMAIN or host not in Shared.allowed_domains or file_ext in IGNORE_EXT:
            return False

    	else:
			return True
    		

if __name__ == '__main__':
    url = "http://www.ddcpc.cn/2017/jr_0525/102157.html"
    urlfilt = HostFilter(url)
    print urlfilt.filter()

