"""
"""

from string import ascii_uppercase

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

if __name__ == "__main__":
    import random
    import string

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
    image = captcha_image(random.sample(ascii_uppercase + string.digits, 4))
    image.save("sample.jpg", "JPEG", quality=75)
