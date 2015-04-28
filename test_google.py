import urllib
import urllib2
import json
import random

images = 'http://ajax.googleapis.com/ajax/services/search/images'

values = {
		'v': '1.0',
		'rsz': '8',
		'q': "ponies",
		'safe': 'active',
}

data = urllib.urlencode(values)
req = images + '?' + data
response = urllib2.urlopen(req)

j = json.loads(response.read())
images = j['responseData']['results']

if len(images) > 0:
	print random.choice(images)['unescapedUrl']
