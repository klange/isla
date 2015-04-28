# -*- coding: utf-8 -*-
import datetime

import isla
from util.timedelta import td_format

@isla.bind("hear", ".*", i=True)
def monitor_channel(self, c, e, msg, match):
    nick = e.source.nick.lower()
    if nick in self.tells:
        for source, message in self.tells[nick].iteritems():
            self.reply(c,e,"{name} told me to tell you: \"{message}\"".format(name=source,message=message))
        del self.tells[nick]
    self.lastsaw[nick] = datetime.datetime.now()

@isla.bind("reply", "^tell +([-a-zA-Z0-9]*):? +(.*)$", i=True)
def receive_tell(self, c, e, msg, match):
    target = match.group(1).lower()
    if target == c.get_nickname():
        self.reply(c,e,"Okay? Thanks for letting me know.")
        return
    message = match.group(2)
    if not target in self.tells:
        self.tells[target] = {}
    self.tells[target][e.source.nick] = message
    self.reply(c,e,"I'll let them know when they next speak up.")

@isla.bind("reply", "^when did you last see ([-a-zA-Z0-9]*)\??$", i=True)
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
