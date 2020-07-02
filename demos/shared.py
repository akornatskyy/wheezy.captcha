"""
"""

from wheezy.caching.memory import MemoryCache
from wheezy.captcha.http import CaptchaContext
from wheezy.captcha.image import background
from wheezy.captcha.image import captcha
from wheezy.captcha.image import curve
from wheezy.captcha.image import noise
from wheezy.captcha.image import offset
from wheezy.captcha.image import rotate
from wheezy.captcha.image import smooth
from wheezy.captcha.image import text
from wheezy.captcha.image import warp


cache = MemoryCache()

captcha_image = captcha(drawings=[
    background(),
    text(
        fonts=[
            'fonts/CourierNew-Bold.ttf',
            'fonts/LiberationMono-Bold.ttf'
        ],
        drawings=[
            warp(),
            rotate(),
            offset()
        ]),
    curve(),
    noise(),
    smooth()
])


captcha = CaptchaContext(captcha_image, cache)
captcha_handler = captcha.create_handler(quality=65)
