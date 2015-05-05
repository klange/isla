# -*- coding: utf-8 -*-
import isla
import urllib
import urllib2
import json
import random

@isla.bind("reply", "^youtube( me)? (.*)", i=True)
def youtube_search(self, c, e, msg, match):
    images = 'http://gdata.youtube.com/feeds/api/videos'

    values = {
            'orderBy': 'relevance',
            'max-results': 15,
            'alt': 'json',
            'q': match.group(2).encode('utf-8'),
    }

    data = urllib.urlencode(values)
    req = images + '?' + data
    response = urllib2.urlopen(req)

    j = json.loads(response.read())
    videos = j['feed']['entry']

    video = random.choice(videos)

    for l in video['link']:
        if l['rel'] == 'alternate' and l['type'] == 'text/html':
            self.send(c,e,l['href'])

