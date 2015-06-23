# -*- coding: utf-8 -*-
"""Violent action responses."""
import random

import isla

__version__ = '1.0.0'

stabbing_replies = [
    "stabs {person}",
    "shanks {person}",
    "slits {person}'s throat",
    "recites the first law: 'A robot may not injure a human being, or through inaction, allow a human being to come to harm.'",
]

friend_replies = [
    "Eh, why would I stab {person}, they are my friend!",
    "I don't want to stab {person}!",
]

unknown_replies = [
    "I don't know who that is.",
    "I can't find a {person} in this channel.",
    "I'm not sure who you mean by '{person}'.",
    "Error. I didn't quite catch that.",
]

no_self_harm = [
    "won't hurt herself.",
    "doesn't want to stab herself.",
    "ignores {person}."
]

def in_channel(user, users):
    return user.lower() in [x.lower() for x in users]

@isla.bind("reply", "^stab (.*)$", i=True)
def stabby_stabby(self, c, e, msg, match):
    if len(match.group(1)):
        if e.target in self.channels:
            if not in_channel(match.group(1), self.channels[e.target].users()):
                self.reply(c,e,random.choice(unknown_replies).format(person=match.group(1)))
                return
        if "friends" in dir(isla.bot.config) and match.group(1).lower() in isla.bot.config.friends:
            self.reply(c,e,random.choice(friend_replies).format(person=match.group(1)))
        elif match.group(1).lower() == c.get_nickname().lower():
            self.action(c,e,random.choice(no_self_harm).format(person=e.source.nick))
        else:
            self.action(c,e,random.choice(stabbing_replies).format(person=match.group(1)))

