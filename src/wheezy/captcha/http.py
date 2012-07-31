
"""
"""

import random

from wheezy.http import HTTPResponse


class FileAdapter():

    def __init__(self, response):
        self.response = response

    def write(self, b):
        self.response.write_bytes(b)


def captcha_factory(image, chars='ABCDEFGHJKLMNPQRSTUVWXYZ23456789',
                    max_chars=4):
    def handler(request):
        turing_number = random.sample(chars, max_chars)
        response = HTTPResponse('image/jpg')
        image(turing_number).save(
            FileAdapter(response), 'JPEG', quality=65)
        return response
    return handler
