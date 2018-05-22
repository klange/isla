# -*- coding: utf-8 -*-
import random
import isla

rolled_nothing = [
    "I rolled nothing.",
    "Zero.",
    "Error. I didn't quite catch that.",
]

no_sided = [
    "How does one roll a no-sided die?",
    "Zero.",
    "Error. I didn't quite catch that.",
]

lots_of_dice = [
    "Cowardly refusing to roll more than 100 dice.",
    "I can't hold that many dice.",
    "I think I lost one...",
]

big_dice = [
    "I'm not sure I can read the numbers on these...",
    "Refusing to roll a sphere.",
    "At what does a dice turn into a sphere?",
]

@isla.bind("reply", "^roll ([0-9]+)?d([0-9]+)$", i=True)
def roll_dice(self, c, e, msg, match):
    count = 1 if not match.group(1) else int(match.group(1))
    sides = int(match.group(2))

    if count == 0:
        self.reply(c,e,random.choice(rolled_nothing))
    elif sides == 0:
        self.reply(c,e,random.choice(no_sided))
    elif count > 100:
        self.reply(c,e,random.choice(lots_of_dice))
    elif sides > 100000:
        self.reply(c,e,random.choice(big_dice))
    else:
        results = []
        _sum = 0
        for x in xrange(count):
            t = random.randrange(1,sides+1)
            results.append(str(t))
            _sum += t
        if count == 1:
            self.reply(c,e,"{d}".format(d=_sum))
        else:
            self.reply(c,e,"{t} = {d}".format(t="+".join(results),d=_sum))

