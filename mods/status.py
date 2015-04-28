# -*- coding: utf-8 -*-
import datetime
import os

import isla

@isla.bind("reply", "^version\??$", i=True)
def version(self, c, e, msg, match):
    self.reply(c,e,"My core software is version {version}.".format(version=isla.__version__))


def td_format(td_object):
    seconds = int(td_object.total_seconds())
    periods = [
        ('year',        60*60*24*365),
        ('month',       60*60*24*30),
        ('day',         60*60*24),
        ('hour',        60*60),
        ('minute',      60),
        ('second',      1)
    ]
    strings=[]
    for period_name,period_seconds in periods:
        if seconds > period_seconds:
            period_value , seconds = divmod(seconds,period_seconds)
            if period_value == 1:
                strings.append("%s %s" % (period_value, period_name))
            else:
                strings.append("%s %ss" % (period_value, period_name))
    return ", ".join(strings)

@isla.bind("reply", "^uptime\??$", i=True)
def uptime(self, c, e, msg, match):
    started = datetime.datetime.fromtimestamp(os.stat('/proc/self').st_ctime)
    now = datetime.datetime.now()
    delta = now - started

    self.reply(c,e,"Up {time}".format(time=td_format(delta)))

