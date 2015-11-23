import os
import webapp2 as webapp

from google.appengine.ext.webapp import template

from utils import find_platform, get_platform, platforms, get_revision, get_platform_string


class DownloadHandler(webapp.RequestHandler):
    def get(self, platform_name):
        platform = get_platform(platform_name)
        if not platform:
            return self.redirect('http://www.youtube.com/e/o_asQwJqWCI?autoplay=1&start=16')

        self.redirect(platform.get_last_snapshot_url())

class RevisionHandler(webapp.RequestHandler):
    def get(self, platform_name):
        platform = get_platform_string(platform_name, self.request)
        last_revision = get_revision(platform)
        if last_revision:
            self.response.out.write(last_revision)
        else:
            self.error('404');

class IndexHandler(webapp.RequestHandler):
    def get(self):
        platform_name = self.request.get('platform')
        platform = get_platform_string(platform_name, self.request)

        template_values = {
            'platform': platform,
            'platforms': platforms
        }
        path = os.path.join(os.path.dirname(__file__), 'index.html')

        self.response.out.write(template.render(path, template_values))


app = webapp.WSGIApplication([
    ('/', IndexHandler),
    ('/dl/(.*)', DownloadHandler),
    ('/rev/(.*)', RevisionHandler),
])
