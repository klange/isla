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
def list_channel(self, c, e, msg, match):
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

blacklist = [
    "▄▄▄▄▄",
    "SUPERNETS",
    "supernets",
    "HAPPY APRIL FLOODS DAY",
    "nigger",
]

avoid_kicking = [
    "klange",
    "discord",
]

@isla.bind("reply", "^show blacklist$", i=True)
def show_blacklist(self, c, e, msg, match):
    if "friends" in dir(isla.bot.config) and e.source.nick in isla.bot.config.friends:
        self.reply(c,e,"Blacklisted phrases are: {}".format(", ".join(blacklist)))

@isla.bind("hear", ".*", i=True)
def monitor_channel(self, c, e, msg, match):
    if any([x in msg for x in blacklist]):
        nick = e.source.nick.lower()
        if nick in avoid_kicking:
            return
        c.kick(e.target, nick, "message contained blacklisted phrase")

