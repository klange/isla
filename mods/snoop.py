# -*- coding: utf-8 -*-
import random

import isla

urls = [
	"https://www.youtube.com/watch?v=TqT7TNQhAYs",
	"https://www.youtube.com/watch?v=o2TO5atI4rU",
	"https://www.youtube.com/watch?v=dBqMxvqLQuw",
	"https://www.youtube.com/watch?v=iPXKfGxeHIY",
	"https://www.youtube.com/watch?v=rnS-05XoXs4",
	"https://www.youtube.com/watch?v=uimCcRx00vw",
	"https://www.youtube.com/watch?v=eEoMI9BwHp4",
	"https://www.youtube.com/watch?v=wXzg0D-cKds",
]

@isla.bind("reply", "^(snoop anime)|(smoke weed)|(420)$", i=True)
def snoop_dogg(self, c, e, msg, match):
    self.reply(c,e,random.choice(urls))

