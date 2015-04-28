# -*- coding: utf-8 -*-
import datetime

import isla

@isla.bind("reply", "^hello[.!]?$", i=True)
def reply_hello(self, c, e, msg, match):
    self.reply(c,e,"Hello!")

@isla.bind("reply", "^(good )?morning[.!]?$", i=True)
def good_morning(self, c, e, msg, match):
    h = datetime.datetime.now().hour
    if h < 4:
        self.reply(c,e,"It's too early...")
    elif h > 12:
        self.reply(c,e,"It's too late...")
    else:
        self.reply(c,e,"Good morning.")

