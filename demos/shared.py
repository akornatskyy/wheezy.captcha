"""
"""

from wheezy.caching.memory import MemoryCache
from wheezy.captcha.http import CaptchaContext
from wheezy.captcha.image import (
    background,
    captcha,
    curve,
    noise,
    offset,
    rotate,
    smooth,
    text,
    warp,
)

cache = MemoryCache()

captcha_image = captcha(
    drawings=[
        background(),
        text(
            fonts=[
                "fonts/CourierNew-Bold.ttf",
                "fonts/LiberationMono-Bold.ttf",
            ],
            drawings=[warp(), rotate(), offset()],
        ),
        curve(),
        noise(),
        smooth(),
    ]
)


captcha = CaptchaContext(captcha_image, cache)
captcha_handler = captcha.create_handler(quality=65)
