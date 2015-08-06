import urllib, urllib2, re, sys, os
from urllib import urlencode, quote
from pyquery import PyQuery as pq
import re
import json
import cookielib

def CreateOpener():
	opener = urllib2.build_opener()
	opener.addheaders.append(('Cookie', 'sva=lVe324PqsI24'))
	urllib2.install_opener(opener)
	return opener

site = "http://seasonvar.ru"
opener = CreateOpener()

def GetHTML(url):
	conn = opener.open(url)
	html = conn.read()
	conn.close()
	return html 

def LoadJson(url):
	response = GetHTML(url)
	return json.loads(response)

def GetFilesLinks(json_response):
	files = []
	for row in json_response['playlist']:
		if row.has_key('file'):
			files.append(row['file'])
		elif row.has_key('playlist'):
			for row2 in row['playlist']:
				files.append(row2['file'])
	return files

def PrintPlayList(id, secure):
	url = 'http://seasonvar.ru/playls2/'+secure+'x/trans/'+id+'/list.xml'
	json_response = LoadJson(url)
	print GetFilesLinks(json_response)

def PrintFilmLinks(html):
	doc = pq(html)
	for row in doc('.film-list-item a'):
		page = site+row.attrib['href']
		html = GetHTML(page)
		elem = re.findall('id": "(.*)", "serial": "(.*)" , "type": "html5", "secure": "(.*)"', html)[0]
		id = elem[0]
		secure = elem[2]
		PrintPlayList(id, secure)

html = GetHTML(site)
PrintFilmLinks(html)
