""" ``comp`` module.
"""

try:  # pragma: nocover
    from PIL import Image, ImageFilter
    from PIL.ImageColor import getrgb
    from PIL.ImageDraw import Draw
    from PIL.ImageFont import truetype
except ImportError:  # pragma: nocover
    import Image  # noqa
    import ImageFilter  # noqa
    from ImageColor import getrgb  # noqa
    from ImageDraw import Draw  # noqa
    from ImageFont import truetype  # noqa


# PIL, Pillow < 10
if hasattr(Draw(Image.new("RGB", (0, 0))), "textsize"):

    def textsize(draw, c, font):
        return draw.textsize(c, font=font)

else:

    def textsize(draw, text, font):
        _, _, w, h = draw.textbbox((0, 0), text, font)
        return w, h
