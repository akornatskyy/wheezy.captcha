"""
"""

from wheezy.http import HTTPResponse
from wheezy.http import WSGIApplication
from wheezy.http import accept_method
from wheezy.http import bootstrap_http_defaults
from wheezy.http import not_found
from wheezy.http.middleware import http_cache_middleware_factory

from shared import cache
from shared import captcha
from shared import captcha_handler


@accept_method(('GET', 'POST'))
def welcome(request):
    message, error = '', ''
    if request.method == 'POST':
        errors = {}
        if not captcha.validate(request, errors, gettext=lambda s: s):
            error = errors['turing_number'][-1]
        else:
            message = 'Well done!'
    challenge_code = captcha.get_challenge_code(request)
    response = HTTPResponse()
    response.write("""
<html><head><style>
span {color: green;}
span.error {color:red;}
input[type=text] {width:200;text-transform: uppercase;}
#captcha {display:block; width:200; height:75}
</style></head><body>
<html><body>
<h2>Captcha Verification: wheezy.http demo</h2>
<span><b>%s</b></span>
<form method="post">
<p>Please enter the text from image:</p>
<p>
    <label for="turing_number">
        <img id="captcha" src="/captcha.jpg?c=%s" />
        <input type="hidden" name="c" value="%s" />
    </label>
    <input id="turing_number" name="turing_number" type="text"
        maxlength="4" autocomplete="off" />
    <span class="error">%s</span>
</p>
<p><input type="submit" value="Verify"></p>
</form>
<script>
window.onload=function()
{
    c = document.getElementById('captcha');
    c.onclick = function() {
        this.src=this.src.replace(/&r=\d+/g,'') + '&r=' + \
            Math.floor(Math.random() * 100 + 1);
    };
}
</script>
</body></html>
    """ % (message, challenge_code, challenge_code, error))
    return response


def router_middleware(request, following):
    path = request.path
    if path == '/':
        response = welcome(request)
    elif path.startswith('/captcha.jpg'):
        response = captcha_handler(request)
    else:
        response = not_found()
    return response


options = {
    'http_cache': cache
}
main = WSGIApplication([
    bootstrap_http_defaults,
    http_cache_middleware_factory,
    lambda ignore: router_middleware
], options)


if __name__ == '__main__':
    from wsgiref.handlers import BaseHandler
    from wsgiref.simple_server import make_server
    try:
        print('Visit http://localhost:8080/')
        BaseHandler.http_version = '1.1'
        make_server('', 8080, main).serve_forever()
    except KeyboardInterrupt:
        pass
    print('\nThanks!')
