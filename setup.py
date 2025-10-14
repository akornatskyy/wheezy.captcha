#!/usr/bin/env python

import multiprocessing
import os
import re

from setuptools import setup

extra = {}
try:
    from Cython.Build import cythonize

    p = os.path.join("src", "wheezy", "captcha")
    extra["ext_modules"] = cythonize(
        [os.path.join(p, "*.py")],
        exclude=os.path.join(p, "__init__.py"),
        # https://github.com/cython/cython/issues/3262
        nthreads=0 if multiprocessing.get_start_method() == "spawn" else 2,
        compiler_directives={"language_level": 3},
        quiet=True,
    )
except ImportError:
    pass

README = open(os.path.join(os.path.dirname(__file__), "README.md")).read()
VERSION = (
    re.search(
        r'__version__ = "(.+)"',
        open("src/wheezy/captcha/__init__.py").read(),
    )
    .group(1)
    .strip()
)

install_requires = []

try:
    import uuid  # noqa
except ImportError:
    install_requires.append("uuid")

setup(
    name="wheezy.captcha",
    version=VERSION,
    python_requires=">=3.9",
    description="A lightweight captcha library",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/akornatskyy/wheezy.captcha",
    author="Andriy Kornatskyy",
    author_email="andriy.kornatskyy@live.com",
    license="MIT",
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="wsgi http captcha",
    packages=["wheezy", "wheezy.captcha"],
    package_dir={"": "src"},
    namespace_packages=["wheezy"],
    zip_safe=False,
    install_requires=install_requires,
    extras_require={"PIL": ["PIL"], "Pillow": ["Pillow>=10"]},
    platforms="any",
    **extra
)
