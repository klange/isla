#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
import importlib
import inspect
import re
import sys
import traceback

import irc.bot
import pyinotify

import bot
import config

__version__ = '0.1.1'

class SynchronousWatcher(pyinotify.ProcessEvent):
    def my_init(self, path):
        self.path = path
        self.watch = pyinotify.WatchManager()
        self.notifier = pyinotify.Notifier(self.watch, default_proc_fun=self)
        self.watch.add_watch(path, pyinotify.ALL_EVENTS, rec=True, auto_add=True)

    def check(self):
        self.results = set()
        if self.notifier.check_events(timeout=0):
            self.notifier.read_events()
        self.notifier.process_events()
        return self.results

    def process_IN_MODIFY(self, event):
        self.results.add(event.pathname)

    def process_IN_CLOSE_WRITE(self, event):
        self.results.add(event.pathname)

class Isla(irc.bot.SingleServerIRCBot):
    def __init__(self, *args, **kwargs):
        super(Isla, self).__init__(*args, **kwargs)

        self.binds = {}
        self.binds["reply"] = {}
        self.binds["hear"] = {}

        self.watcher = SynchronousWatcher(path="mods")

    def on_nicknameinuse(self, c, e):
        old = c.get_nickname()
        new = old + "_"
        print "Warning: Nick '{old}' in use, trying '{new}'".format(old=old,new=new)
        c.nick(new)

    def on_welcome(self, c, e):
        # Identify
        print "Notice: Hello world! Connected and identifying."
        c.privmsg('NickServ', 'IDENTIFY {password}'.format(password=config.nickserver_password))
        # Join autojoin channels
        for channel in self.autojoin:
            print "Notice: Autojoining channel {channel}".format(channel=channel)
            c.join(channel)

    def reload_module(self, module):
        # First, unbind everything with that name
        self.unbind_plugin(module)
        try:
            reload(self.mods[module])
        except:
            print "Exception while reloading {module}".format(module=module)
            traceback.print_exc(file=sys.stdout)

    def load_module(self, module):
        if name == "__init__": return
        try:
            bot.isla.mods[module] = importlib.import_module("mods.{name}".format(name=module))
        except:
            print "Exception while loading {module}".format(module=module)
            traceback.print_exc(file=sys.stdout)

    def check_reload(self):
        results = filter(lambda x: x.endswith('.py'), self.watcher.check())
        if results:
            print "Reloading modules..."
            for r in results:
                module = r.split("/")[-1].replace(".py","")
                if module in self.mods:
                    self.reload_module(module)
                else:
                    self.load_module(module)

    def unbind_plugin(self, plugin):
        for bind in self.binds:
            print "Unbinding {bind}".format(bind=bind)
            to_del = []
            for thing in self.binds[bind]:
                p, _ = thing
                print "Checking {thing}".format(thing=p)
                if p == "mods." + plugin:
                    to_del.append(thing)
            for t in to_del:
                print "Unbinding {bind}.{thing}".format(bind=bind,thing=t)
                del self.binds[bind][t]

    def on_pubmsg(self, c, e):
        self.check_reload()

        at_me = False
        msg = e.arguments[0].strip()

        if msg.startswith(c.get_nickname() + ":") or msg.startswith(c.get_nickname() + ","):
            at_me = True
            msg = msg[len(c.get_nickname()) + 1:].strip()

        if at_me:
            self.match_bind('reply', c, e, msg)
        else:
            self.match_bind('hear', c, e, msg)

    def match_bind(self, bind_type, c, e, msg):
        for k, v in self.binds[bind_type].iteritems():
            plugin, source = k
            match, func = v
            result = match.match(msg)
            if result:
                try:
                    func(self, c,e,msg,result)
                except:
                    print "Exception in plugin {mod}.{func} /{bind}/".format(mod=plugin,func=func.__name__,bind=source)
                    traceback.print_exc(file=sys.stdout)

    def get_version(self):
        return "isla [bot] {version}".format(version=__version__)

    def reply(self, c, e, msg):
        c.privmsg(e.target, "{nick}: {msg}".format(nick=e.source.nick,msg=msg))

    def send(self, c, e, msg):
        c.privmsg(e.target, msg)

    def action(self, c, e, msg):
        self.send(c, e, "\001ACTION {message}\001".format(message=msg))

    def bind(self, bind_type, plugin, match, func, i=False):
        print "Binding module {module} function {func}".format(module=plugin, func=func.__name__)
        if not bind_type in self.binds:
            raise ValueError("Invalid bind type: {type}".format(bind_type))
        flags = re.U | (re.I if i else 0)
        x = re.compile(match, flags)
        if x:
            self.binds[bind_type][(plugin,match)] = (x, func)
        else:
            raise ValueError("Bad regex: {match}".format(match))

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('UTF8')
    irc.buffer.DecodingLineBuffer.errors = 'replace'

    bot.isla = Isla([config.server], config.nick, config.realname)
    bot.isla.autojoin = config.autojoin
    bot.isla.mods = {}
    # Bind plugins
    r = re.compile("^mods\/(.*)\.py$")
    for mod in glob.glob("mods/*.py"):
        name = r.match(mod).group(1)
        bot.isla.load_module(name)
    bot.isla.start()

def bind(bind_type, match, i=False):
    def real_bind(func):
        bot.isla.bind(bind_type, inspect.getmodule(func).__name__, match, func, i)
        return func
    return real_bind

