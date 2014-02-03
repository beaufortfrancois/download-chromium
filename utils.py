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


WINDOWS     = ChromiumPlatform('Win',              'Chromium for Windows x86', 'chrome-win32.zip')
WINDOWS_X64 = ChromiumPlatform('Win_x64',          'Chromium for Windows x64', 'chrome-win32.zip')
MAC         = ChromiumPlatform('Mac',              'Chromium for Mac',         'chrome-mac.zip')
LINUX       = ChromiumPlatform('Linux',            'Chromium for Linux x86',   'chrome-linux.zip')
LINUX_X64   = ChromiumPlatform('Linux_x64',        'Chromium for Linux x64',   'chrome-linux.zip')
LINUX_CROS  = ChromiumPlatform('Linux_ChromiumOS', 'Chromium OS for Linux',    'chrome-linux.zip')
ANDROID     = ChromiumPlatform('Android',          'Chromium for Android',     'chrome-android.zip')


def find_platform(string):
    if re.search('Android', string):
        return ANDROID
    elif re.search('Win', string):
        if re.search('Win64|WOW64', string):
            return WINDOWS_X64
        else:
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
        return [p for p in platforms if p.name.lower() == name.lower()][0]
    except IndexError:
        return None
