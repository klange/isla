# -*- coding: utf-8 -*-
import isla

@isla.bind("reply", "^brain get ([a-zA-Z_\-\.]*)", i=True)
def brain_get(self, c, e, msg, match):
    if "friends" not in dir(isla.bot.config) or e.source.nick not in isla.bot.config.friends:
        return
    q = match.group(1)
    try:
        value = isla.bot.brain.get(q)
    except KeyError:
        self.send(c,e,"{q} is not set.".format(q=q))
        return
    self.send(c,e,"{q} = {v}".format(q=q, v=repr(value)))

@isla.bind("reply", "^brain dump( [a-zA-Z_\-\.]*)?$", i=True)
def brain_dump(self, c, e, msg, match):
    if "friends" not in dir(isla.bot.config) or e.source.nick not in isla.bot.config.friends:
        return
    query = match.group(1).strip() if match.group(1) else None
    self.send(c,e,", ".join(isla.bot.brain.keys(query)))


@isla.bind("reply", "^brain test set$")
def brain_test_set(self, c, e, msg, match):
    isla.bot.brain.set("foo.bar", {'a': 1, 'b': 'hello', 'c': {'test': 'foo','bar': 'baz'}})
    self.send(c,e,"okay!")
