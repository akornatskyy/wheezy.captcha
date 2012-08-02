
"""
"""

from wheezy.caching import MemoryCache

from wheezy.http import HTTPResponse
from wheezy.http import WSGIApplication
from wheezy.http import accept_method
from wheezy.http import bootstrap_http_defaults
from wheezy.http import not_found
from wheezy.http.middleware import http_cache_middleware_factory

from wheezy.captcha.http import CaptchaContext

from wheezy.captcha.image import captcha

from wheezy.captcha.image import background
from wheezy.captcha.image import noise
from wheezy.captcha.image import smooth
from wheezy.captcha.image import text

from wheezy.captcha.image import offset
from wheezy.captcha.image import rotate
from wheezy.captcha.image import warp


cache = MemoryCache()
cache_factory = lambda: cache

captcha_image = captcha(drawings=[
    background(),
    text(fonts=[
        'fonts/CourierNew-Bold.ttf',
        'fonts/LiberationMono-Bold.ttf'],
        drawings=[
            warp(),
            rotate(),
            offset()
        ]),
    noise(),
    smooth()
])


captcha = CaptchaContext(captcha_image, cache_factory)


@accept_method(('GET', 'POST'))
def welcome(request):
    message, error = '', ''
    if request.method == 'POST':
        errors = {}
        if not captcha.validate(request, errors):
            error = errors['turing_number'][-1]
        else:
            message = 'Well done!'
    challenge_code = captcha.get_challenge_code(request)
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


def router_middleware(request, following):
    path = request.path
    if path == '/':
        response = welcome(request)
    elif path.startswith('/captcha.jpg'):
        response = captcha.render(request)
    else:
        response = not_found()
    return response


options = {
    'http_cache_factory': cache_factory
}
main = WSGIApplication([
    bootstrap_http_defaults,
    http_cache_middleware_factory,
    lambda ignore: router_middleware
], options)


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    try:
        print('Visit http://localhost:8080/')
        make_server('', 8080, main).serve_forever()
    except KeyboardInterrupt:
        pass
    print('\nThanks!')
