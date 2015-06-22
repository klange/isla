# -*- coding: utf-8 -*-
import isla

def in_channel(user, users):
    return user.lower() in [x.lower() for x in users]

@isla.bind("reply", "^queue add (.*)$", i=True)
def queue_add(self, c, e, msg, match):
    user = match.group(1)
    if e.target in self.channels:
        if not in_channel(match.group(1), self.channels[e.target].users()):
            self.reply(c,e,"{person} is not in this channel".format(person=user))
            return
        key = 'queue.{server}.{channel}'.format(server=isla.bot.config.server_shortname, channel=e.target.lower())
        queue = [] if key not in isla.bot.brain else isla.bot.brain.get(key)
        if user in queue:
            self.reply(c,e,"{person} is already in the queue")
            return
        after = queue[-1] if len(queue) else None
        queue.append(user)
        isla.bot.brain.set(key, queue)
        self.reply(c,e,"{person} is now in line{after}.".format(person=user,after=(" after " + after if after else "")))
    else:
        self.reply(c,e,"Not in a channel?")

@isla.bind("reply", "^queue show$", i=True)
def queue_show(self, c, e, msg, match):
    if e.target in self.channels:
        key = 'queue.{server}.{channel}'.format(server=isla.bot.config.server_shortname, channel=e.target.lower())
        queue = [] if key not in isla.bot.brain else isla.bot.brain.get(key)
        if not queue:
            self.reply(c,e,"Queue for {channel} is empty.".format(channel=e.target))
        else:
            self.reply(c,e,"Current queue for {channel} is: {queue}".format(queue=", ".join(queue), channel=e.target))
    else:
        self.reply(c,e,"Not in a channel?")

@isla.bind("reply", "^queue next$", i=True)
def queue_next(self, c, e, msg, match):
    if e.target in self.channels:
        key = 'queue.{server}.{channel}'.format(server=isla.bot.config.server_shortname, channel=e.target.lower())
        queue = [] if key not in isla.bot.brain else isla.bot.brain.get(key)
        if not queue:
            self.reply(c,e,"Queue for {channel} is empty.".format(channel=e.target))
        else:
            front = queue.pop(0)
            isla.bot.brain.set(key, queue)
            self.reply(c,e,"{person} is next in line for {channel}".format(person=front,channel=e.target))
    else:
        self.reply(c,e,"Not in a channel?")
