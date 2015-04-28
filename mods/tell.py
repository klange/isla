# -*- coding: utf-8 -*-
import isla

@isla.bind("hear", ".*", i=True)
def monitor_channel(self, c, e, msg, match):
    nick = e.source.nick.lower()
    if nick in self.tells:
        for source, message in self.tells[nick].iteritems():
            self.reply(c,e,"{name} told me to tell you: \"{message}\"".format(name=source,message=message))
        del self.tells[nick]

@isla.bind("reply", "^tell +([-a-zA-Z0-9]*):? +(.*)$", i=True)
def receive_tell(self, c, e, msg, match):
    target = match.group(1).lower()
    message = match.group(2)
    if not target in self.tells:
        self.tells[target] = {}
    self.tells[target][e.source.nick] = message
    self.reply(c,e,"I'll let them know when they next speak up.")

if not 'tells' in dir(isla.bot.isla):
    isla.bot.isla.tells = {}
