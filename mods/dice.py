# -*- coding: utf-8 -*-
import random
import isla

@isla.bind("reply", "^roll ([0-9]+)?d([0-9]+)$", i=True)
def roll_dice(self, c, e, msg, match):
    count = 1 if not match.group(1) else int(match.group(1))
    sides = int(match.group(2))

    if count == 0:
        self.reply(c,e,"I rolled nothing.")
    elif sides == 0:
        self.reply(c,e,"How does one roll a no-sided die?")
    elif count > 100:
        self.reply(c,e,"Cowardly refusing to roll more than 100 dice.")
    elif sides > 100000:
        self.reply(c,e,"Refusing to roll a sphere.")
    else:
        _sum = 0
        for x in xrange(count):
            _sum += random.randrange(1,sides+1)
        self.reply(c,e,"{d}".format(d=_sum))

