# -*- coding: utf-8 -*-
"""Provides some simple status responders."""
import datetime
import os

import isla
from util.timedelta import td_format

__version__ = '1.0.0'

@isla.bind("reply", "^version\??$", i=True)
def version(self, c, e, msg, match):
    """version? - Displays core isla version number."""
    self.reply(c,e,"My core software is version {version}.".format(version=isla.__version__))

@isla.bind("reply", "^uptime\??$", i=True)
def uptime(self, c, e, msg, match):
    """uptime? - Displays isla up time."""
    started = datetime.datetime.fromtimestamp(os.stat('/proc/self').st_ctime)
    now = datetime.datetime.now()
    delta = now - started

    self.reply(c,e,"Up {time}".format(time=td_format(delta)))

@isla.bind("reply", "^git sha\??$", i=True)
def git_sha(self, c, e, msg, match):
    """git sha? - Displays the current isla git sha"""
    import subprocess
    sha = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
    tag = subprocess.check_output(['git', 'describe', '--tags']).strip()
    dirty = 1 - subprocess.call("git status -s | grep -q '^.M'", shell=True)
    self.reply(c,e, "SHA: {sha}{dirty} Tag: {tag}".format(sha=sha,tag=tag,dirty="-dirty" if dirty else ""))

@isla.bind("reply", "^list modules$", i=True)
def list_modules(self, c, e, msg, match):
    """list modules - Displays a list of loaded modules."""
    self.reply(c,e,"Active modules: " + ", ".join(isla.bot.isla.mods))

@isla.bind("reply", "^module version ([a-zA-Z0-9_]+)$", i=True)
def module_version(self, c, e, msg, match):
    """module version [module] - Displays the version information for a module."""
    if not len(match.group(1)): # Ug.
        return
    mod = match.group(1)
    if not mod in isla.bot.isla.mods:
        self.reply(c,e,"No module by that name found.")
        return
    module = isla.bot.isla.mods[mod]
    if '__version__' in dir(module):
        self.reply(c,e,"{module} {version}".format(module=mod, version=module.__version__))
    else:
        self.reply(c,e,"{module} has no version information.".format(module=mod))

def _find_methods(module):
    out = []
    for bind in isla.bot.isla.binds:
        for thing in isla.bot.isla.binds[bind]:
            p, m = thing
            if p == "mods." + module:
                _, func  = isla.bot.isla.binds[bind][thing]
                out += [(bind, m, func)]
    return out

@isla.bind("reply", "^module methods ([a-zA-Z0-9_]+)$", i=True)
def module_methods(self, c, e, msg, match):
    """module methods [module] - List methods available from a module."""
    if not len(match.group(1)): # Ug.
        return
    mod = match.group(1)
    if not mod in isla.bot.isla.mods:
        self.reply(c,e,"No module by that name found.")
        return

    binds = _find_methods(mod)
    results = [x.__name__ for _, _, x in binds]

    self.reply(c,e,"{module} has the following methods: {methods}".format(module=mod,methods=", ".join(results)))

@isla.bind("reply", "^module help ([a-zA-Z0-9_]+)$", i=True)
def module_help(self, c, e, msg, match):
    """module help [module] - Provides help information for a module, if available."""
    if not len(match.group(1)): # Ug.
        return
    mod = match.group(1)
    if not mod in isla.bot.isla.mods:
        self.reply(c,e,"No module by that name found.")
        return
    module = isla.bot.isla.mods[mod]
    if '__doc__' in dir(module) and module.__doc__:
        self.reply(c,e,"{module}: {help}".format(module=mod, help=module.__doc__.strip()))
    else:
        self.reply(c,e,"{module} has no help information.".format(module=mod))

@isla.bind("reply", "^module help ([a-zA-Z0-9_]+) ([a-zA-Z0-9_]+)$", i=True)
def module_help_method(self, c, e, msg, match):
    """module help [module] [method] - Provides help for individual module methods, if available."""
    if not len(match.group(1)) or not len(match.group(2)):
        return
    mod = match.group(1)
    if not mod in isla.bot.isla.mods:
        self.reply(c,e,"No module by that name found.")
        return
    module = isla.bot.isla.mods[mod]
    method = match.group(2)
    if not method in dir(module):
        self.reply(c,e,"{module} has no such method '{method}'.".format(module=mod,method=method))
        return
    m = module.__dict__[method]
    if '__doc__' in dir(m) and m.__doc__:
        self.reply(c,e,"{module}.{method}: {doc}".format(module=mod,method=method,doc=m.__doc__))
    else:
        self.reply(c,e,"{module}.{method}: No help available.".format(module=mod,method=method))
