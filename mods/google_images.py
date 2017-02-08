# -*- coding: utf-8 -*-
import isla
import urllib
import urllib2
import random
import re

@isla.bind("reply", "^image( me)? (.*)", i=True)
def google_search(self, c, e, msg, match):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (MeeGo; NokiaN9) AppleWebKit/534.13 (KHTML, like Gecko) NokiaBrowser/8.5.0 Mobile Safari/534.13')]
    response = opener.open('https://www.google.com/search?tbm=isch&hl=en&q='+urllib.quote(match.group(2).encode('utf-8'),safe='')).read()

    images = re.findall('imgurl=.+?(?=&amp)', response, re.DOTALL)

    if len(images) > 0:
        choice = random.choice(images)[7:]
        self.send(c,e,urllib.unquote(choice))

