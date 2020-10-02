"""
"""

from wheezy.core.collections import attrdict
from wheezy.core.descriptors import attribute
from wheezy.html.ext.template import WhitespaceExtension, WidgetExtension
from wheezy.http import WSGIApplication
from wheezy.http.middleware import http_cache_middleware_factory
from wheezy.routing import url
from wheezy.template import Engine
from wheezy.template.ext.core import CoreExtension
from wheezy.template.loader import DictLoader
from wheezy.web.handlers.base import BaseHandler
from wheezy.web.middleware import (
    bootstrap_defaults,
    path_routing_middleware_factory,
)
from wheezy.web.templates import WheezyTemplate

from wheezy.captcha.mixin import CaptchaMixin

from shared import cache, captcha, captcha_handler


class WelcomeHandler(BaseHandler, CaptchaMixin):

    captcha_context = captcha

    @attribute
    def model(self):
        return attrdict({"message": "", "turing_number": ""})

    def get(self, message=""):
        self.model.message = message
        return self.render_response(
            "welcome", captcha=self.captcha_widget, m=self.model
        )

    def post(self):
        if not self.validate_captcha():
            return self.get()
        return self.get("Well done!")


templates = {
    "welcome": """@require(m, captcha, path_for, errors)
<html><head><style>
span {color: green;}
span.error {color:red;}
input[type=text] {width:200;text-transform: uppercase;}
#captcha {display:block; width:200; height:75}
</style></head><body>
<h2>Captcha Verification: wheezy.web demo</h2>
@if m.message:
<span><b>@m.message</b></span>
@end
<form method="post">
<p>Please enter the text from image:</p>
<p>
    <label for="turing_number">
        @captcha(path_for('captcha'))
    </label>
    @m.turing_number.textbox(maxlength='4', autocomplete='off')
    @m.turing_number.error()
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
</body></html>"""
}

engine = Engine(
    loader=DictLoader(templates),
    extensions=[CoreExtension(), WidgetExtension(), WhitespaceExtension()],
)

all_urls = [
    ("", WelcomeHandler),
    url("captcha.jpg", captcha_handler, name="captcha"),
]

options = {"http_cache": cache, "render_template": WheezyTemplate(engine)}
main = WSGIApplication(
    [
        bootstrap_defaults(url_mapping=all_urls),
        http_cache_middleware_factory,
        path_routing_middleware_factory,
    ],
    options,
)


if __name__ == "__main__":
    from wsgiref.handlers import BaseHandler
    from wsgiref.simple_server import make_server

    try:
        print("Visit http://localhost:8080/")
        BaseHandler.http_version = "1.1"
        make_server("", 8080, main).serve_forever()
    except KeyboardInterrupt:
        pass
    print("\nThanks!")
