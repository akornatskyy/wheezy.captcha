
"""
"""

from wheezy.http import HTTPResponse
from wheezy.http import WSGIApplication
from wheezy.http import accept_method
from wheezy.http import bootstrap_http_defaults
from wheezy.http import not_found

from wheezy.captcha.http import captcha_factory

from wheezy.captcha.image import captcha

from wheezy.captcha.image import background
from wheezy.captcha.image import noise
from wheezy.captcha.image import smooth
from wheezy.captcha.image import text

from wheezy.captcha.image import offset
from wheezy.captcha.image import rotate
from wheezy.captcha.image import warp


captcha_image = captcha(drawings=[
    background(),
    text(fonts=[
        'fonts/CourierNew-Bold.ttf',
        'fonts/LiberationMono-Bold.ttf'],
        drawings=[
            warp(),
            rotate(),
            offset()]),
    noise(),
    smooth()
])


captcha_handler = captcha_factory(captcha_image)


@accept_method('GET')
def welcome(request):
    response = HTTPResponse()
    response.write("""
<html><body><form action="/verify" method="post">
<h2>Captcha Verification</h2>
<p>Please enter the text from image:</p>
<p>
    <label for="turing_number">
        <img id="captcha" src="/captcha.jpg"
            style="display:block; width:200; height:75"
            onclick="this.src='/captcha.jpg?r=' + Math.floor(Math.random()*100+1)"/>
    </label>
    <input id="turing_number" name="turing_number" type="text"
        maxlength="4" style="width:200" />
</p>
<p><input type="submit" value="Verify"></p>
</form>
    """)
    return response


@accept_method('POST')
def verify(request):
    response = HTTPResponse()
    response.write("Not Implemented")
    return response


def router_middleware(request, following):
    path = request.path
    if path == '/':
        response = welcome(request)
    elif path.startswith('/verify'):
        response = verify(request)
    elif path.startswith('/captcha.jpg'):
        response = captcha_handler(request)
    else:
        response = not_found()
    return response


options = {}
main = WSGIApplication([
    bootstrap_http_defaults,
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
