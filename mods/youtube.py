# -*- coding: utf-8 -*-
import isla
import urllib
import urllib2
import json
import random

from bs4 import BeautifulSoup

@isla.bind("reply", "^youtube( me)? (.*)", i=True)
def youtube_search(self, c, e, msg, match):
    images = 'https://www.youtube.com/results'

    values = {
            'search_query': match.group(2).encode('utf-8'),
    }

    data = urllib.urlencode(values)
    req = images + '?' + data
    response = urllib2.urlopen(req)

    b = BeautifulSoup(response.read())

    results = [x.get('href') for x in b.find_all("a", attrs={"aria-hidden":"true"}) if u'watch' in x.get('href')][:15]

    link = random.choice(results)

    self.send(c,e,"https://youtube.com" + link)


