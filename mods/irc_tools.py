# -*- coding: utf-8 -*-
import random

import isla

@isla.bind("reply", "^join (.*)$", i=True)
def join_channel(self, c, e, msg, match):
    if "friends" in dir(isla.bot.config) and e.source.nick in isla.bot.config.friends:
        c.join(match.group(1).lower())

@isla.bind("reply", "^leave$", i=True)
def leave_channel(self, c, e, msg, match):
    if "friends" in dir(isla.bot.config) and e.source.nick in isla.bot.config.friends:
        c.part(e.target)

@isla.bind("reply", "^list channels$", i=True)
def leave_channel(self, c, e, msg, match):
    if "friends" in dir(isla.bot.config) and e.source.nick in isla.bot.config.friends:
        self.reply(c,e,"I am in: {channels}".format(channels=", ".join(self.channels)))

help_replies = [
    "Hm?",
    "What I can do for you?",
    "What's up?",
    "Eh?",
]

@isla.bind("reply", "^help[.?!]?$", i=True)
def help(self, c, e, msg, match):
    self.reply(c,e,random.choice(help_replies))

@isla.bind("reply", "^beself[.!]?$", i=True)
def beself(self, c, e, msg, match):
    c.nick(isla.bot.config.nick)
