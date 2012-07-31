"""
"""

from wheezy.captcha.image import captcha

from wheezy.captcha.image import background
from wheezy.captcha.image import noise
from wheezy.captcha.image import smooth
from wheezy.captcha.image import text

from wheezy.captcha.image import offset
from wheezy.captcha.image import rotate
from wheezy.captcha.image import warp


if __name__ == '__main__':
    import random
    import string
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
    image = captcha_image(random.sample(string.uppercase + string.digits, 4))
    image.save('sample.jpg', 'JPEG', quality=75)
