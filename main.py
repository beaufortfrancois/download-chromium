import os
import webapp2 as webapp

from google.appengine.ext.webapp import template

from utils import find_platform, get_platform, platforms


class DownloadHandler(webapp.RequestHandler):
    def get(self, platform_name):
        platform = get_platform(platform_name)
        if not platform:
            return self.redirect('http://www.youtube.com/e/o_asQwJqWCI?autoplay=1&start=16')

        self.redirect(platform.get_last_snapshot_url())

class IndexHandler(webapp.RequestHandler):
    def get(self):
        platform_name = self.request.get('platform')
        if platform_name:
            platform = get_platform(platform_name)
        else:
            user_agent = self.request.headers['User-Agent']
            platform = find_platform(user_agent)

        template_values = {
            'platform': platform,
            'platforms': platforms,
        }
        path = os.path.join(os.path.dirname(__file__), 'index.html')

        self.response.out.write(template.render(path, template_values))


app = webapp.WSGIApplication([
    ('/', IndexHandler),
    ('/dl/(.*)', DownloadHandler),
])
