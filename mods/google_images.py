# -*- coding: utf-8 -*-
import isla
import urllib
import urllib2
import json
import random

@isla.bind("reply", "^image( me)? (.*)", i=True)
def google_search(self, c, e, msg, match):
    images = 'http://ajax.googleapis.com/ajax/services/search/images'

    values = {
            'v': '1.0',
            'rsz': '8',
            'q': match.group(2).encode('utf-8'),
            'safe': 'active',
    }

    data = urllib.urlencode(values)
    req = images + '?' + data
    response = urllib2.urlopen(req)

    j = json.loads(response.read())
    images = j['responseData']['results']

    if len(images) > 0:
        self.send(c,e,random.choice(images)['unescapedUrl'])

