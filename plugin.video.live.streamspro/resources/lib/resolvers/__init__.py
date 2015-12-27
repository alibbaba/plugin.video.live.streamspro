# -*- coding: utf-8 -*-

'''
    Genesis Add-on
    Copyright (C) 2015 lambda

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import re,urllib,urlparse,json

#from resources.lib.libraries import cache
#from resources.lib.libraries import control
from resources.lib.libraries import client


def request(url, debrid=''):
    try:
        u = url
        if '</regex>' in url:
            import regex ; url = regex.resolve(url)

        if url.startswith('rtmp'):
            if len(re.compile('\s*timeout=(\d*)').findall(url)) == 0: url += ' timeout=10'
            return url

        if not debrid == '': return debridResolver(url, debrid)

        n = (urlparse.urlparse(url).netloc).lower() ; n = re.sub('www\d+\.|www\.|embed\.', '', n)

        try: url = re.compile('://(http.+)').findall(url)[0]
        except: pass
        print [i['class'] for i in info()]
        r = [i['class'] for i in info() if n in i['netloc']][0]
        r = __import__(r, globals(), locals(), [], -1)
        r = r.resolve(url)

        if r == None: return r

        elif type(r) == list:
            for i in range(0, len(r)): r[i].update({'url': parser(r[i]['url'], url)})

        elif r.startswith('http'): r = parser(r, url)

        return r
    except:
        return u


def parser(url, referer):
    if url == None: return

    try: headers = dict(urlparse.parse_qsl(url.rsplit('|', 1)[1]))
    except: headers = dict('')

    if not 'User-Agent' in headers: headers['User-Agent'] = client.agent()
    if not 'Referer' in headers: headers['Referer'] = referer

    url = '%s|%s' % (url.split('|')[0], urllib.urlencode(headers))
    return url



def rdDict():
    try:
        user, password = [(i['user'], i['pass']) for i in debridCredentials() if i['debrid'] == 'realdebrid' and not (i['user'] == '' or i['pass'] == '')][0]
        url = 'http://real-debrid.com/api/hosters.php'
        result = cache.get(client.request, 24, url)
        hosts = json.loads('[%s]' % result)
        hosts = [i.lower() for i in hosts]
        return hosts
    except:
        return []


def pzDict():
    try:
        user, password = [(i['user'], i['pass']) for i in debridCredentials() if i['debrid'] == 'premiumize' and not (i['user'] == '' or i['pass'] == '')][0]
        url = 'http://api.premiumize.me/pm-api/v1.php?method=hosterlist&params[login]=%s&params[pass]=%s' % (user, password)
        result = cache.get(client.request, 24, url)
        hosts = json.loads(result)['result']['hosterlist']
        hosts = [i.lower() for i in hosts]
        return hosts
    except:
        return []


def adDict():
    try:
        user, password = [(i['user'], i['pass']) for i in debridCredentials() if i['debrid'] == 'alldebrid' and not (i['user'] == '' or i['pass'] == '')][0]
        url = 'http://alldebrid.com/api.php?action=get_host'
        result = cache.get(client.request, 24, url)
        hosts = json.loads('[%s]' % result)
        hosts = [i.lower() for i in hosts]
        return hosts
    except:
        return []




def hostDict():
    d = [i['netloc'] for i in info()]
    try: d = [i.lower() for i in reduce(lambda x, y: x+y, d)]
    except: pass
    return [x for y,x in enumerate(d) if x not in d[:y]]


def hosthqDict():
    d = [i['netloc'] for i in info() if 'quality' in i and i['quality'] == 'High']
    try: d = [i.lower() for i in reduce(lambda x, y: x+y, d)]
    except: pass
    return [x for y,x in enumerate(d) if x not in d[:y]]


def hostmqDict():
    d = [i['netloc'] for i in info() if 'quality' in i and i['quality'] == 'Medium']
    try: d = [i.lower() for i in reduce(lambda x, y: x+y, d)]
    except: pass
    return [x for y,x in enumerate(d) if x not in d[:y]]


def hostlqDict():
    d = [i['netloc'] for i in info() if 'quality' in i and i['quality'] == 'Low']
    try: d = [i.lower() for i in reduce(lambda x, y: x+y, d)]
    except: pass
    return [x for y,x in enumerate(d) if x not in d[:y]]


def hostcapDict():
    d = [i['netloc'] for i in info() if 'captcha' in i and i['captcha'] == True]
    try: d = [i.lower() for i in reduce(lambda x, y: x+y, d)]
    except: pass
    return [x for y,x in enumerate(d) if x not in d[:y]]


def hostprDict():
    d = [i['netloc'] for i in info() if 'class' in i and i['class'] == '']
    try: d = [i.lower() for i in reduce(lambda x, y: x+y, d)]
    except: pass
    return [x for y,x in enumerate(d) if x not in d[:y]]



def info():
    return [{
        'class': '',
        'netloc': ['oboom.com', 'rapidgator.net', 'rg.to', 'uploaded.net', 'uploaded.to', 'ul.to', 'filefactory.com'],
        'quality': 'High'
    }, {
        'class': '_180upload',
        'netloc': ['180upload.com'],
        'quality': 'High'
    }, {
        'class': 'allmyvideos',
        'netloc': ['allmyvideos.net'],
        'quality': 'Medium'
    }, {
        'class': 'allvid',
        'netloc': ['allvid.ch'],
        'quality': 'High'
    }, {
        'class': 'bestreams',
        'netloc': ['bestreams.net'],
        'quality': 'Low'
    }, {
        'class': 'castalba',
        'netloc': ['castalba.tv']
    }, {
        'class': 'clicknupload',
        'netloc': ['clicknupload.me', 'clicknupload.com'],
        'quality': 'High'
    }, {
        'class': 'cloudtime',
        'netloc': ['cloudtime.to'],
        'quality': 'Medium'
    }, {
        'class': 'cloudyvideos',
        'netloc': ['cloudyvideos.com'],
        'quality': 'High'
    }, {
        'class': 'cloudzilla',
        'netloc': ['cloudzilla.to'],
        'quality': 'Medium'
    }, {
        'class': 'daclips',
        'netloc': ['daclips.in'],
        'quality': 'Low'
    }, {
        'class': 'dailymotion',
        'netloc': ['dailymotion.com']
    }, {
        'class': 'datemule',
        'netloc': ['datemule.com']
    }, {
        'class': 'divxpress',
        'netloc': ['divxpress.com'],
        'quality': 'Medium'
    }, {
        'class': 'exashare',
        'netloc': ['exashare.com'],
        'quality': 'Low'
    }, {
        'class': 'fastvideo',
        'netloc': ['fastvideo.in', 'faststream.in', 'rapidvideo.ws'],
        'quality': 'Low'
    }, {
        'class': 'filehoot',
        'netloc': ['filehoot.com'],
        'quality': 'Low'
    }, {
        'class': 'filenuke',
        'netloc': ['filenuke.com', 'sharesix.com'],
        'quality': 'Low'
    }, {
        'class': 'filmon',
        'netloc': ['filmon.com']
    }, {
        'class': 'filepup',
        'netloc': ['filepup.net']
    }, {
        'class': 'googledocs',
        'netloc': ['docs.google.com', 'drive.google.com']
    }, {
        'class': 'googlephotos',
        'netloc': ['photos.google.com']
    }, {
        'class': 'googlepicasa',
        'netloc': ['picasaweb.google.com']
    }, {
        'class': 'googleplus',
        'netloc': ['plus.google.com']
    }, {
        'class': 'gorillavid',
        'netloc': ['gorillavid.com', 'gorillavid.in'],
        'quality': 'Low'
    }, {
        'class': 'grifthost',
        'netloc': ['grifthost.com'],
        'quality': 'High'
    }, {
        'class': 'hdcast',
        'netloc': ['hdcast.me']
    }, {
        'class': 'hugefiles',
        'netloc': ['hugefiles.net'],
        'quality': 'High',
        'captcha': True
    }, {
        'class': 'ipithos',
        'netloc': ['ipithos.to'],
        'quality': 'High'
    }, {
        'class': 'ishared',
        'netloc': ['ishared.eu'],
        'quality': 'High'
    }, {
        'class': 'letwatch',
        'netloc': ['letwatch.us'],
        'quality': 'Medium'
    }, {
        'class': 'mailru',
        'netloc': ['mail.ru', 'my.mail.ru', 'videoapi.my.mail.ru', 'api.video.mail.ru']
    }, {
        'class': 'mightyupload',
        'netloc': ['mightyupload.com'],
        'quality': 'High'
    }, {
        'class': 'movdivx',
        'netloc': ['movdivx.com'],
        'quality': 'Low'
    }, {
        'class': 'movpod',
        'netloc': ['movpod.net', 'movpod.in'],
        'quality': 'Low'
    }, {
        'class': 'movshare',
        'netloc': ['movshare.net'],
        'quality': 'Low'
    }, {
        'class': 'mrfile',
        'netloc': ['mrfile.me'],
        'quality': 'High'
    }, {
        'class': 'mybeststream',
        'netloc': ['mybeststream.xyz']
    }, {
        'class': 'nosvideo',
        'netloc': ['nosvideo.com'],
        'quality': 'Low'
    }, {
        'class': 'novamov',
        'netloc': ['novamov.com'],
        'quality': 'Low'
    }, {
        'class': 'nowvideo',
        'netloc': ['nowvideo.eu', 'nowvideo.sx'],
        'quality': 'Low'
    }, {
        'class': 'openload',
        'netloc': ['openload.io', 'openload.co'],
        'quality': 'High',
        'captcha': True
    }, {
        'class': 'p2pcast',
        'netloc': ['p2pcast.tv']
    }, {
        'class': 'primeshare',
        'netloc': ['primeshare.tv'],
        'quality': 'High'
    }, {
        'class': 'promptfile',
        'netloc': ['promptfile.com'],
        'quality': 'High'
    }, {
        'class': 'putstream',
        'netloc': ['putstream.com'],
        'quality': 'Medium'
    }, {
        'class': 'realvid',
        'netloc': ['realvid.net'],
        'quality': 'Low'
    }, {
        'class': 'sawlive',
        'netloc': ['sawlive.tv']
    }, {
        'class': 'shared2',
        'netloc': ['shared2.me'],
        'quality': 'High'
    }, {
        'class': 'sharerepo',
        'netloc': ['sharerepo.com'],
        'quality': 'Low'
    }, {
        'class': 'skyvids',
        'netloc': ['skyvids.net'],
        'quality': 'High'
    }, {
        'class': 'speedvideo',
        'netloc': ['speedvideo.net']
    }, {
        'class': 'stagevu',
        'netloc': ['stagevu.com'],
        'quality': 'Low'
    }, {
        'class': 'streamcloud',
        'netloc': ['streamcloud.eu'],
        'quality': 'Medium'
    }, {
        'class': 'streamin',
        'netloc': ['streamin.to'],
        'quality': 'Medium'
    }, {
        'class': 'thefile',
        'netloc': ['thefile.me'],
        'quality': 'Low'
    }, {
        'class': 'thevideo',
        'netloc': ['thevideo.me'],
        'quality': 'Low'
    }, {
        'class': 'turbovideos',
        'netloc': ['turbovideos.net'],
        'quality': 'High'
    }, {
        'class': 'tusfiles',
        'netloc': ['tusfiles.net'],
        'quality': 'High'
    }, {
        'class': 'up2stream',
        'netloc': ['up2stream.com'],
        'quality': 'Medium'
    }, {
        'class': 'uploadc',
        'netloc': ['uploadc.com', 'uploadc.ch', 'zalaa.com'],
        'quality': 'High'
    }, {
        'class': 'uploadrocket',
        'netloc': ['uploadrocket.net'],
        'quality': 'High',
        'captcha': True
    }, {
        'class': 'uptobox',
        'netloc': ['uptobox.com'],
        'quality': 'High'
    }, {
        'class': 'v_vids',
        'netloc': ['v-vids.com'],
        'quality': 'High'
    }, {
        'class': 'vaughnlive',
        'netloc': ['vaughnlive.tv', 'breakers.tv', 'instagib.tv', 'vapers.tv']
    }, {
        'class': 'veehd',
        'netloc': ['veehd.com']
    }, {
        'class': 'veetle',
        'netloc': ['veetle.com']
    }, {
        'class': 'vidbull',
        'netloc': ['vidbull.com'],
        'quality': 'Low'
    }, {
        'class': 'videomega',
        'netloc': ['videomega.tv'],
        'quality': 'High'
    }, {
        'class': 'videopremium',
        'netloc': ['videopremium.tv', 'videopremium.me']
    }, {
        'class': 'videoweed',
        'netloc': ['videoweed.es'],
        'quality': 'Low'
    }, {
        'class': 'vidlockers',
        'netloc': ['vidlockers.ag'],
        'quality': 'High'
    }, {
        'class': 'vidspot',
        'netloc': ['vidspot.net'],
        'quality': 'Medium'
    }, {
        'class': 'vidto',
        'netloc': ['vidto.me'],
        'quality': 'Medium'
    }, {
        'class': 'vidzi',
        'netloc': ['vidzi.tv'],
        'quality': 'Low'
    }, {
        'class': 'vimeo',
        'netloc': ['vimeo.com']
    }, {
        'class': 'vk',
        'netloc': ['vk.com']
    }, {
        'class': 'vodlocker',
        'netloc': ['vodlocker.com'],
        'quality': 'Low'
    }, {
        'class': 'xvidstage',
        'netloc': ['xvidstage.com'],
        'quality': 'Medium'
    }, {
        'class': 'youtube',
        'netloc': ['youtube.com'],
        'quality': 'Medium'
    }, {
        'class': 'zerocast',
        'netloc': ['zerocast.tv']
    }, {
        'class': 'zettahost',
        'netloc': ['zettahost.tv'],
        'quality': 'High'
    }, {
        'class': 'zstream',
        'netloc': ['zstream.to'],
        'quality': 'High'
    }]


