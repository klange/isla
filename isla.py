#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
import importlib
import inspect
import json
import re
import sys
import traceback
import ssl
import sqlite3

import irc.bot
import irc.connection
import pyinotify

import bot

__version__ = '0.1.2'

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


class Brain(object):
    """
        The brain manages data in and out of a backing store.
        Brain storage should be used for any dynamic information that:
            1) Should be accessible across multiple instances.
            2) Must survive restarts.
            3) May be added or changed during runtime.

        TODO: support deleting
        (if you have data you add/remove from a lot, consider using a list, as
        values in a list are stored directly rather than being accessible through
        the key system; dictionaries that are updated will not have old keys
        removed at the moment)
    """

    schema = "CREATE TABLE IF NOT EXISTS brain (key text PRIMARY KEY, data blob)"
    read_query = "SELECT * FROM brain WHERE key=?"
    like_query = "SELECT * FROM brain WHERE key LIKE ?"
    write_query = "INSERT OR REPLACE INTO brain (key, data) VALUES (?,?)"
    keys_query = "SELECT key FROM brain"
    keys2_query = "SELECT key FROM brain WHERE key LIKE ?"

    def __init__(self, config_path):
        self.conn = sqlite3.connect(config_path)
        self.conn.isolation_level = None
        self.query(self.schema)

    def query(self, query, args=None):
        c = self.conn.cursor()
        if isinstance(args, list):
            return c.executemany(query, args)
        if args:
            return c.execute(query, args)
        else:
            return c.execute(query)

    def keys(self, matching=None):
        if matching:
            return [x[0] for x in self.query(self.keys2_query, (matching + '%',))]
        else:
            return [x[0] for x in self.query(self.keys_query)]

    def getdict(self, path):
        """
        Dictionary elements need to be recursively retrieved. If you know a value is set
        and is a dictionary, you can call this directly, but the safer thing to do
        would be to call get() which will handle alternative values. If an element does
        exist, getdict will return an empty dictionary, so it may be what you want in
        some instances.
        """
        results = [x for x in self.query(self.like_query, (path + ".%",))]
        if not results:
            return {}
        else:
            out = {}
            for k, v in results:
                _k = k.replace(path + '.', '', 1)
                if '.' in _k:
                    continue
                _v = json.loads(v)
                if isinstance(_v, dict):
                    out[_k] = self.getdict(k)
                else:
                    out[_k] = _v
            return out

    def get(self, path):
        """
        Get an individual element's value, from a path. If the element has not been set,
        a KeyError will be raised. If the element is a dictionary, it will be filled
        recurisvely.
        """
        results = [x for x in self.query(self.read_query, (path,))]
        if results:
            value = json.loads(results[0][1])
            if isinstance(value, dict):
                return self.getdict(path)
            else:
                return value
        else:
            value = self.getdict(path)
            if not value:
                raise KeyError(path)
            return value

    def _set(self, path, value):
        """
        Write a raw string into the database for a path.
        """
        self.query(self.write_query, (path, value))

    def set(self, path, value):
        """
        Set a value.
        Leading entries in path are not currently checked for existence.
        If value is a dict, each element in it will be (recursively) set.
        All other values are stored as JSON. If you need to store a dictionary
        in a way that is *not* accessible from the path hierarchy, consider
        putting it in a list, as then it won't be recursively stored. That
        may be useful if you're in-place updating the entire dict several times.
        """
        if isinstance(value, dict):
            self._set(path, "{}")
            for k, v in value.iteritems():
                self.set(path + '.' + k, v)
        else:
            self._set(path, json.dumps(value))

    def __contains__(self, key):
        results = [x for x in self.query(self.read_query, (key,))]
        return not not results


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
        if bot.config.nickserver_password:
            c.privmsg('NickServ', 'IDENTIFY {password}'.format(password=bot.config.nickserver_password))
        # Join autojoin channels
        for channel in bot.config.autojoin:
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

    def on_privmsg(self, c, e):
        msg = e.arguments[0].strip()
        self.match_bind('reply', c, e, msg)
        self.match_bind('hear', c, e, msg)

    def on_pubmsg(self, c, e):
        self.check_reload()

        at_me = False
        msg = e.arguments[0].strip()

        if msg.lower().startswith(c.get_nickname() + ":") or msg.lower().startswith(c.get_nickname() + ","):
            at_me = True
            msg = msg[len(c.get_nickname()) + 1:].strip()

        if at_me:
            self.match_bind('reply', c, e, msg)
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
        if e.target == c.get_nickname():
            e.target = e.source.nick
        c.privmsg(e.target, "{nick}: {msg}".format(nick=e.source.nick,msg=msg))

    def send(self, c, e, msg):
        if e.target == c.get_nickname():
            e.target = e.source.nick
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

    config = "config"
    if '--config' in sys.argv:
        config = sys.argv[sys.argv.index('--config')+1]
    _config = importlib.import_module(config)
    if 'ssl' in dir(_config) and _config.ssl:
        bot.isla = Isla([_config.server], _config.nick, _config.realname, connect_factory=irc.connection.Factory(wrapper=ssl.wrap_socket))
    else:
        bot.isla = Isla([_config.server], _config.nick, _config.realname)
    bot.brain = Brain(_config.brain_path if 'brain_path' in dir(_config) and _config.brain_path else 'brain.sqlite')
    bot.config = _config
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

