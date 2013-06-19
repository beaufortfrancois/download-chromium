import datetime
import os
import webapp2 as webapp

from google.appengine.ext import db 
from google.appengine.ext.webapp import template, util

from utils import find_platform, get_platform, WINDOWS, MAC, LINUX, LINUX_X64


class Download(db.Model):
    platform = db.StringProperty()
    is_hacked = db.BooleanProperty()
    date = db.DateTimeProperty(auto_now_add=True)

class PlatformNotDetected(db.Model):
    user_agent = db .StringProperty()


class DownloadHandler(webapp.RequestHandler):
    def get(self, platform_name):
        referer = self.request.headers.get('Referer')
        is_hacked = not bool(referer)
        platform = get_platform(platform_name)
        if not platform:
            return self.redirect('http://www.youtube.com/e/o_asQwJqWCI?autoplay=1&start=16')

        download = Download(platform=platform.name, is_hacked=is_hacked)
        download.put()
        self.redirect(platform.get_last_snapshot_url())

class TrendsHandler(webapp.RequestHandler):
    def get(self):
        try:
            days = int(self.request.get('days', 7))
        except ValueError:
            days = 7

        win_count = Download.all().filter('date >', (datetime.datetime.now() - datetime.timedelta(days=days))).filter('platform =', WINDOWS.name).count(limit=None)
        mac_count = Download.all().filter('date >', (datetime.datetime.now() - datetime.timedelta(days=days))).filter('platform =', MAC.name).count(limit=None)
        linux_count = Download.all().filter('date >', (datetime.datetime.now() - datetime.timedelta(days=days))).filter('platform =', LINUX.name).count(limit=None)
        linux_x64_count = Download.all().filter('date >', (datetime.datetime.now() - datetime.timedelta(days=days))).filter('platform =', LINUX_X64.name).count(limit=None)
        count = win_count + mac_count + linux_count

        template_values = {
            'win_count': win_count,
            'mac_count': mac_count,
            'linux_count': linux_count,
            'linux_x64_count': linux_x64_count,
            'days': days,
            'count': count,
        }
        path = os.path.join(os.path.dirname(__file__), 'trends.html')
        self.response.out.write(template.render(path, template_values))

class IndexHandler(webapp.RequestHandler):
    def get(self):
        user_agent = self.request.headers['User-Agent']
        platform = find_platform(user_agent)
        if not platform and PlatformNotDetected.all().filter('user_agent =', user_agent).count() == 0:
            platform_not_detected = PlatformNotDetected(user_agent=user_agent)
            platform_not_detected.put()

        template_values = {
            'platform': platform,
        }
        path = os.path.join(os.path.dirname(__file__), 'index.html')

        self.response.out.write(template.render(path, template_values))


app = webapp.WSGIApplication([
    ('/', IndexHandler),
    ('/dl/(.*)', DownloadHandler),
    ('/trends/', TrendsHandler),
])
