# -*- coding: utf-8 -*-
import os
import re
import time
import urllib.request, urllib.error, urllib.parse
import xbmcgui
import requests
from bs4 import BeautifulSoup
from kodibgcommon.logging import *
from kodibgcommon.utils import *
from kodibgcommon.notifications import *
import ssl

params = get_params()
action = params.get("action")
id = params.get("id")
url = params.get("url")
title = params.get("title")
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
host = "https://btvplus.bg/"
next_page_title = 'Следваща страница'
view_mode = 500

if not action:
    show_categories()

elif action == 'show_products':
    products = get_products(url)
    log("Found %s items" % len(products), 0)

    for product in products:
        url = make_url({"action": "show_episodes", "url": product["url"]})
        add_listitem_folder(product["title"], url, iconImage=product["logo"], thumbnailImage=product["logo"])

elif action == 'show_episodes':
    show_episodes(get_episodes(url))

elif action == 'play_stream':
    stream = get_stream(url)["url"]
    log('Extracted stream %s ' % stream, 0)
    if stream:
        add_listitem_resolved_url(title, stream)


# elif action == 'play_live':
#   stream = get_stream("https://btvplus.bg/live/")["url"]
#   log('Extracted stream %s ' % stream, 0)
#   if stream:
#     add_listitem_resolved_url(title, stream)
# if settings.btv_username == '' or settings.btv_password == '':
#   notify_error('Липсва потребителско име и парола за bTV')

# body = { "username": settings.btv_username, "password": settings.btv_password }
# headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
# s = requests.session()
#
# r = s.post(base64.b64decode('aHR0cHM6Ly9idHZwbHVzLmJnL2xiaW4vc29jaWFsL2xvZ2luLnBocA=='), headers=headers, data=body)
# log(r.text, 0)
#
# if r.json()["resp"] != "success":
#   log("Unable to login to btv.bg", 4)
# else:
#   url = base64.b64decode('aHR0cHM6Ly9idHZwbHVzLmJnL2xiaW4vdjMvYnR2cGx1cy9wbGF5ZXJfY29uZmlnLnBocD9tZWRpYV9pZD0yMTEwMzgzNjI1Jl89JXM=').decode('utf-8')
#   log(url, 0)
#   url = url % str(time.time() * 100)
#   r = s.get(url, headers=headers)
#   m = re.compile('(http.*\.m3u.*?)[\s\'"\\\\]+[\s\'"\\\\]+').findall(r.text)
#   if len(m) > 0:
#     stream = m[0].replace('\/', '/')
#     if not stream.startswith('http'):
#       stream = 'https:' + stream
#     log('Извлечен видео поток %s' % stream, 2)
#     add_listitem_resolved_url('bTV на живо', stream)
#   else:
#     log("No match for playlist url found", 4)

elif action == 'search':

    keyboard = xbmc.Keyboard('', 'Търсене...')
    keyboard.doModal()
    searchText = ''
    if keyboard.isConfirmed():
        searchText = urllib.parse.quote_plus(keyboard.getText())
        if searchText != '':
            show_episodes(get_episodes('search/?q=%s' % searchText))


xbmcplugin.endOfDirectory(get_addon_handle())
xbmcplugin.setContent(get_addon_handle(), 'movies')
xbmc.executebuiltin("Container.SetViewMode(%s)" % view_mode)