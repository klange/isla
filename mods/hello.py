# -*- coding: utf-8 -*-
import isla

@isla.bind("reply", "^hello[.!]?$", i=True)
def reply_hello(self, c, e, msg, match):
    self.reply(c,e,"Hello!")

