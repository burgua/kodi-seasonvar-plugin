import urllib
import urllib2
import sys
import re
import json


def create_opener():
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'sva=lVe324PqsI24'))
    urllib2.install_opener(opener)
    return opener


def get_html(url):
    try:
        conn = opener.open(url)
        html = conn.read()
        conn.close()
        return html
    except:
        # ToDo: failed!
        return
    else:
        return


def load_json(url):
    response = get_html(url)
    return json.loads(response)


def get_file_links(json_response):
    files = []
    for row in json_response['playlist']:
        if row.has_key('file'):
            files.append(row['file'])
        elif row.has_key('playlist'):
            for row2 in row['playlist']:
                files.append(row2['file'])
    return files


def play(url, name):
    listitem = xbmcgui.ListItem(name)
    listitem.setInfo('video', {'Title': name})
    xbmc.Player().play(url, listitem)


def PrintFilmLinks(html):
    exepat = re.compile(r'film-list-item">.*?<a href="(.*?)".*?>(.*?)<\/a>', re.DOTALL)
    data = exepat.findall(html)
    for row in data:
        print row[1]
        page = site + row[0]
        name = row[1]
        add_dir(page, name, 1)


def index(page, name):
    html = get_html(page)
    elem = re.findall('id": "(.*)", "serial": "(.*)" , "type": "html5", "secure": "(.*)"', html)[0]
    id = elem[0]
    secure = elem[2]
    print_playlist(id, secure, name)


def print_playlist(id, secure, name):
    url = 'http://seasonvar.ru/playls2/' + secure + 'x/trans/' + id + '/list.xml'
    json_response = load_json(url)
    files = get_file_links(json_response)
    i = 0
    for one_file in files:
        i = i + 1
        add_downLink(name + " " + str(i), one_file, 2)


def add_downLink(name, url, mode):
    u = (sys.argv[0] +
         "?url=" + urllib.quote_plus(url) +
         "&mode=" + str(mode) +
         "&name=" + urllib.quote_plus(name))
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="icon.png")
    liz.setInfo(type="Video", infoLabels={"Title": name})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),
                                     url=u, listitem=liz, isFolder=False)
    return ok


def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params) - 1] == '/'):
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]

    return param


def add_dir(url, name, mode):
    u = (sys.argv[0] +
         "?url=" + urllib.quote_plus(url) +
         "&mode=" + str(mode) +
         "&name=" + urllib.quote_plus(name))
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="icon.png")
    liz.setInfo(type="Video", infoLabels={"Title": name})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),
                                     url=u, listitem=liz, isFolder=True)
    return ok


site = "http://seasonvar.ru"
opener = create_opener()

import xbmcaddon, xbmc, xbmcgui, xbmcplugin

params = get_params()
url = None
name = None
mode = None

try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
try:
    name = urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode = int(params["mode"])
except:
    pass

# first page
if mode == None:
    html = get_html(site)
    PrintFilmLinks(html)

# page with links
elif mode == 1:
    index(url, name)

# page with links
elif mode == 2:
    play(url, name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
