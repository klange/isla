# -*- coding: utf-8 -*-
import random

import isla

@isla.bind("reply", "^join (.*)$", i=True)
def join_channel(self, c, e, msg, match):
    if "friends" in dir(isla.bot.config) and e.source.nick in isla.bot.config.friends:
        c.join(match.group(1).lower())

help_replies = [
    "Hm?",
    "What I can do for you?",
    "What's up?",
    "Eh?",
]

@isla.bind("reply", "^help[.?!]?$", i=True)
def help(self, c, e, msg, match):
    self.reply(c,e,random.choice(help_replies))