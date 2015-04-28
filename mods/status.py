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

