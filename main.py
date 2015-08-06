import urllib, urllib2, re, sys, os
from urllib import urlencode, quote
from pyquery import PyQuery as pq
import re
import json
import cookielib

site = "http://seasonvar.ru"

opener = urllib2.build_opener()
opener.addheaders.append(('Cookie', 'sva=lVe324PqsI24'))
urllib2.install_opener(opener)

def GetHTML(url):
	headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3)'+
		'Gecko/2008092417 Firefox/3.0.3', 'Content-Type':'application/x-www-form-urlencoded'}
	conn = opener.open(url)
	html = conn.read()
	conn.close()
	return html 

def LoadJson(url):
	response = GetHTML(url)
	return json.loads(response)

def getPlayList(id, secure):
	url = 'http://seasonvar.ru/playls2/'+secure+'x/trans/'+id+'/list.xml'
	print url
	json_response = LoadJson(url)

	for row in json_response['playlist']:
		if row.has_key('file'):
			print row['file']
		elif row.has_key('playlist'):
			for row2 in row['playlist']:
				print row2['file']

def PrintFilmLinks(html):
	doc = pq(html)
	for row in doc('.film-list-item a'):
		page = site+row.attrib['href']
		html = GetHTML(page)
		elem = re.findall('id": "(.*)", "serial": "(.*)" , "type": "html5", "secure": "(.*)"', html)[0]
		id = elem[0]
		secure = elem[2]
		getPlayList(id, secure)

html = GetHTML(site)
PrintFilmLinks(html)
