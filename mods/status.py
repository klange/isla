# -*- coding: utf-8 -*-
import datetime
import os

import isla
from util.timedelta import td_format

@isla.bind("reply", "^version\??$", i=True)
def version(self, c, e, msg, match):
    self.reply(c,e,"My core software is version {version}.".format(version=isla.__version__))

@isla.bind("reply", "^uptime\??$", i=True)
def uptime(self, c, e, msg, match):
    started = datetime.datetime.fromtimestamp(os.stat('/proc/self').st_ctime)
    now = datetime.datetime.now()
    delta = now - started

    self.reply(c,e,"Up {time}".format(time=td_format(delta)))

@isla.bind("reply", "^git sha\??$", i=True)
def git_sha(self, c, e, msg, match):
    import subprocess
    sha = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
    tag = subprocess.check_output(['git', 'describe', '--tags']).strip()
    dirty = 1 - subprocess.call("git status -s | grep -q '^.M'", shell=True)
    self.reply(c,e, "SHA: {sha}{dirty} Tag: {tag}".format(sha=sha,tag=tag,dirty="-dirty" if dirty else ""))


