import json
import os
import webapp2 as webapp

from google.appengine.ext.webapp import template

from utils import build_types, get_build_type, get_platform, platforms, get_revision, get_platform_string


class DownloadHandler(webapp.RequestHandler):
    def get(self, platform_name):
        build_type = str(self.request.get('type'))
        platform = get_platform(platform_name)
        if not platform:
            return self.redirect('https://www.youtube.com/embed/o_asQwJqWCI?t=16&autoplay=1')

        self.redirect(platform.get_last_build_url(build_type))

class RevisionHandler(webapp.RequestHandler):
    def get(self, platform_name):
        build_type = self.request.get('type')
        platform = get_platform_string(platform_name, self.request)
        data = get_revision(platform, build_type)
        if (data and data['content']):
            self.response.out.write(json.dumps(data))
        else:
            self.error('404');

class IndexHandler(webapp.RequestHandler):
    def get(self):
        build_type_name = self.request.get('type')
        build_type = get_build_type(build_type_name)
        platform_name = self.request.get('platform')
        platform = get_platform_string(platform_name, self.request)

        template_values = {
            'build_type': build_type,
            'build_types': build_types,
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
