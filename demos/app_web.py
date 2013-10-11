"""
"""

from wheezy.http import HTTPResponse
from wheezy.http import WSGIApplication
from wheezy.web.handlers.base import BaseHandler
from wheezy.http.middleware import http_cache_middleware_factory
from wheezy.web.middleware import bootstrap_defaults
from wheezy.web.middleware import http_error_middleware_factory
from wheezy.web.middleware import path_routing_middleware_factory


from shared import cache
from shared import captcha
from shared import captcha_handler


class WelcomeHandler(BaseHandler):

    def get(self, message='', error=''):
        challenge_code = captcha.get_challenge_code(self.request)
        response = HTTPResponse()
        response.write("""
    <html><body><form method="post">
    <h2>Captcha Verification</h2>
    <span style="color: green"><b>%s</b></span>
    <p>Please enter the text from image:</p>
    <p>
        <label for="turing_number">
            <img id="captcha" src="/captcha.jpg?c=%s"
                style="display:block; width:200; height:75"
                onclick="this.src='/captcha.jpg?c=%s&r=' + \
                       Math.floor(Math.random()*100+1)"/>
            <input type="hidden" name="c" value="%s" />
        </label>
        <input id="turing_number" name="turing_number" type="text"
            maxlength="4" style="width:200;text-transform: uppercase;"
            autocomplete="off" />
        <span style="color:red">%s</span>
    </p>
    <p><input type="submit" value="Verify"></p>
    </form></body></html>
        """ % (message, challenge_code, challenge_code, challenge_code, error))
        return response

    def post(self):
        if not captcha.validate(self.request, self.errors,
                                gettext=lambda s: s):
            return self.get(error=self.errors['turing_number'][-1])
        else:
            return self.get('Well done!')


all_urls = [
    ('', WelcomeHandler),
    ('captcha.jpg', captcha_handler)
]

options = {
    'http_cache': cache
}
main = WSGIApplication([
    bootstrap_defaults(url_mapping=all_urls),
    http_cache_middleware_factory,
    http_error_middleware_factory,
    path_routing_middleware_factory
], options)


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    try:
        print('Visit http://localhost:8080/')
        make_server('', 8080, main).serve_forever()
    except KeyboardInterrupt:
        pass
    print('\nThanks!')
