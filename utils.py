import re

from google.appengine.api import urlfetch


LAST_REVISION_TEMPLATE = 'https://commondatastorage.googleapis.com/chromium-browser-snapshots/%(platform)s/LAST_CHANGE'
LAST_SNAPSHOT_TEMPLATE = 'https://commondatastorage.googleapis.com/chromium-browser-snapshots/%(platform)s/%(revision)s/%(zip_name)s'


platforms = []


class ChromiumPlatform(object):
    def __init__(self, name, pretty_name, zip_name):
        self.name = name
        self.pretty_name = pretty_name
        self.zip_name = zip_name
        self.last_revision_url = LAST_REVISION_TEMPLATE % {'platform' : self.name}
        platforms.append(self)

    def __repr__(self):
        return self.name

    def get_last_snapshot_url(self):
        revision = urlfetch.fetch(self.last_revision_url).content

        return LAST_SNAPSHOT_TEMPLATE % {
            'platform': self.name,
            'revision': revision,
            'zip_name': self.zip_name,
        }


LINUX     = ChromiumPlatform('Linux',     'Linux',   'chrome-linux.zip')
LINUX_X64 = ChromiumPlatform('Linux_x64', 'Linux',   'chrome-linux.zip')
WINDOWS   = ChromiumPlatform('Win',       'Windows', 'chrome-win32.zip')
MAC       = ChromiumPlatform('Mac',       'Mac',     'chrome-mac.zip')


def find_platform(string):
    if re.search('Win', string):
        return WINDOWS
    elif re.search('Mac', string):
        return MAC
    elif re.search('Linux', string):
        if re.search('_64', string):
            return LINUX_X64
        else:
            return LINUX
    else:
        return None


def get_platform(name):
    try:
        return [p for p in platforms if p.name == name][0]
    except IndexError:
        return None
