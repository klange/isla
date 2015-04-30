# -*- coding: utf-8 -*-
import datetime
import random

import isla

hello_replies = [
    "Hello.",
    "Hi.",
    "Hello!",
]

@isla.bind("reply", "^hello[.!]?$", i=True)
def reply_hello(self, c, e, msg, match):
    self.reply(c,e,random.choice(hello_replies))

annoyed_replies = [
    "Eh...",
    "Oi.",
]

@isla.bind("reply", "^good girl\.?$", i=True)
def good_girl(self, c, e, msg, match):
    self.reply(c,e,random.choice(annoyed_replies))

stabbing_replies = [
    "stabs {person}",
    "shanks {person}",
    "slits {person}'s throat",
]

friend_replies = [
    "Eh, why would I stab {person}, they are my friend!",
    "I don't want to stab {person}!",
]

@isla.bind("reply", "^stab (.*)$", i=True)
def stabby_stabby(self, c, e, msg, match):
    if len(match.group(1)):
        if "friends" in dir(isla.config) and match.group(1).lower() in isla.config.friends:
            self.reply(c,e,random.choice(friend_replies).format(person=match.group(1)))
        else:
            self.action(c,e,random.choice(stabbing_replies).format(person=match.group(1)))

night_replies = [
    "It's too early...",
    "I'm not awake yet...",
    "Come back in a few hours...",
]

evening_replies = [
    "It's too late for 'Good morning'.",
    "It's too late for that.",
    "Hello.",
]

morning_replies = [
    "Good morning.",
    "...",
    "おはよう",
]

@isla.bind("reply", "^(good )?morning[.!]?$", i=True)
def good_morning(self, c, e, msg, match):
    h = datetime.datetime.now().hour
    if h < 4:
        self.reply(c,e,random.choice(night_replies))
    elif h > 12:
        self.reply(c,e,random.choice(evening_replies))
    else:
        self.reply(c,e,random.choice(morning_replies))

@isla.bind("reply", "^jump[.!]?$", i=True)
def jump_webm(self, c, e, msg, match):
    self.reply(c,e,"http://a.pomf.se/lepwja.webm")

@isla.bind("reply", "^smile[.!]?$", i=True)
def smile(self, c, e, msg, match):
    self.reply(c,e,"http://i.imgur.com/TefCf8e.png")

