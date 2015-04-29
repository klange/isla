# -*- coding: utf-8 -*-
import datetime
import random

import isla
from util.timedelta import td_format

tell_messages = [
    "{name} wanted you to know: \"{message}\"",
    "{name} told me to tell you: \"{message}\"",
    "by the way, {name} said: \"{message}\"",
]

@isla.bind("hear", ".*", i=True)
def monitor_channel(self, c, e, msg, match):
    nick = e.source.nick.lower()
    if nick in self.tells:
        for source, message in self.tells[nick].iteritems():
            self.reply(c,e,random.choice(tell_messages).format(name=source,message=message))
        del self.tells[nick]
    self.lastsaw[nick] = datetime.datetime.now()

self_tell_replies = [
    ":P",
    "Okay? Thanks for letting me know.",
    "???",
    "Error. I didn't quite catch that.",
]

tell_replies = [
    "I'll let them know when they next speak up.",
    "I'll try to remember.",
    "Will do.",
    "Roger that.",
]

@isla.bind("reply", "^tell +([-_a-zA-Z0-9]*):? +(.*)$", i=True)
def receive_tell(self, c, e, msg, match):
    target = match.group(1).lower()
    if target == c.get_nickname():
        self.reply(c,e,random.choice(self_tell_replies))
        return
    message = match.group(2)
    if not target in self.tells:
        self.tells[target] = {}
    self.tells[target][e.source.nick] = message
    self.reply(c,e,random.choice(tell_replies))

@isla.bind("reply", "^when did you last see ([-_a-zA-Z0-9]*)\??$", i=True)
def last_saw(self, c, e, msg, match):
    target = match.group(1)
    if not target.lower() in self.lastsaw:
        self.reply(c,e,"I've not seen {person}.".format(person=target))
    else:
        now = datetime.datetime.now()
        delta = now - self.lastsaw[target.lower()]
        time = td_format(delta)
        self.reply(c,e,"I last saw {person} {time} ago".format(person=target,time=time))

if not 'tells' in dir(isla.bot.isla):
    isla.bot.isla.tells = {}
if not 'lastsaw' in dir(isla.bot.isla):
    isla.bot.isla.lastsaw = {}
