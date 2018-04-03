import random
import re

from google.appengine.api import urlfetch


LAST_REVISION_TEMPLATE = 'https://commondatastorage.googleapis.com/chromium-browser-%(build_type)s/%(platform)s/LAST_CHANGE'
LAST_BUILD_TEMPLATE = 'https://commondatastorage.googleapis.com/chromium-browser-%(build_type)s/%(platform)s/%(revision)s/%(zip_name)s'

build_types = []

class ChromiumBuildType(object):
    def __init__(self, name, pretty_name):
        self.name = name
        self.pretty_name = pretty_name
        build_types.append(self)

    def __repr__(self):
        return self.name

SNAPSHOTS    = ChromiumBuildType('snapshots',   'Latest')
#TODO: Clean up build types once we're sure it's not needed anymore
#CONTINUOUS   = ChromiumBuildType('continuous', 'Last Known Good Revision')

def get_build_type(name):
    try:
        return [b for b in build_types if b.name.lower() == name.lower()][0]
    except IndexError:
        return SNAPSHOTS

platforms = []

class ChromiumPlatform(object):
    def __init__(self, name, pretty_name, zip_name):
        self.name = name
        self.pretty_name = pretty_name
        self.zip_name = zip_name
        platforms.append(self)

    def __repr__(self):
        return self.name

    def get_last_build_url(self, build_type):
        if not build_type:
            build_type = SNAPSHOTS

        revision = get_revision(self.name, build_type)['content']

        return LAST_BUILD_TEMPLATE % {
            'build_type': build_type,
            'platform': self.name,
            'revision': revision,
            'zip_name': self.zip_name,
        }


WINDOWS     = ChromiumPlatform('Win',                   'Chromium for Windows x86', 'chrome-win32.zip')
WINDOWS_X64 = ChromiumPlatform('Win_x64',               'Chromium for Windows x64', 'chrome-win32.zip')
MAC         = ChromiumPlatform('Mac',                   'Chromium for Mac',         'chrome-mac.zip')
LINUX       = ChromiumPlatform('Linux',                 'Chromium for Linux x86',   'chrome-linux.zip')
LINUX_X64   = ChromiumPlatform('Linux_x64',             'Chromium for Linux x64',   'chrome-linux.zip')
LINUX_CROS  = ChromiumPlatform('Linux_ChromiumOS_Full', 'Chromium OS for Linux',    'chrome-linux.zip')
ANDROID     = ChromiumPlatform('Android',               'Chromium for Android',     'chrome-android.zip')


def find_platform(user_agent_string):
    if re.search('Android', user_agent_string):
        return ANDROID
    elif re.search('Win64', user_agent_string):
        return WINDOWS_X64
    elif re.search('Win', user_agent_string):
        return WINDOWS
    elif re.search('Mac', user_agent_string):
        return MAC
    elif re.search('Linux', user_agent_string):
        if re.search('_64', user_agent_string):
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

def get_platform_string(platform_name, request):
    if platform_name:
        platform = get_platform(platform_name)
    else:
        user_agent = request.headers['User-Agent']
        platform = find_platform(user_agent)
    return platform

def get_revision(name, build_type):
    last_revision_url = LAST_REVISION_TEMPLATE % {'platform': name, 'build_type': build_type}
    last_revision_url += '?%s' % random.random()
    try:
        result = urlfetch.fetch(last_revision_url)
        return {
          'content': result.content if result.status_code == 200 else None,
          'last-modified': result.headers['last-modified']
        }
    except IndexError:
        return {
          'content': None,
          'last-modified': None
        }
