`wheezy.captcha`_ is a `python`_ package written in pure Python
code. It is a lightweight captcha library that provides integration
with (one of below must be installed):

* `PIL`_ - Python Imaging Library 1.1.7.
* `Pillow`_ - Python Imaging Library (fork).

It is optimized for performance, well tested and documented.

Resources:

* `source code`_, `examples`_ and `issues`_ tracker are available
  on `bitbucket`_
* `documentation`_, `readthedocs`_
* `eggs`_ on `pypi`_

Install
-------

`wheezy.captcha`_ requires `python`_ version 2.4 to 2.7 or 3.2+.
It is independent of operating system. You can install it from `pypi`_
site using `setuptools`_ (you need specify extra requirements per
imaging library of your choice)::

    $ easy_install wheezy.captcha
    $ easy_install wheezy.captcha[PIL]
    $ easy_install wheezy.captcha[Pillow]

If you are using `virtualenv`_::

    $ virtualenv env
    $ env/bin/easy_install wheezy.captcha

If you run into any issue or have comments, go ahead and add on
`bitbucket`_.

.. _`bitbucket`: http://bitbucket.org/akorn/wheezy.captcha
.. _`doctest`: http://docs.python.org/library/doctest.html
.. _`documentation`: http://packages.python.org/wheezy.captcha
.. _`eggs`: http://pypi.python.org/pypi/wheezy.captcha
.. _`examples`: http://bitbucket.org/akorn/wheezy.captcha/src/tip/demos
.. _`issues`: http://bitbucket.org/akorn/wheezy.captcha/issues
.. _`pil`: http://www.pythonware.com/products/pil/
.. _`pillow`: https://pypi.python.org/pypi/Pillow
.. _`pypi`: http://pypi.python.org
.. _`python`: http://www.python.org
.. _`readthedocs`: http://readthedocs.org/builds/wheezycaptcha
.. _`setuptools`: http://pypi.python.org/pypi/setuptools
.. _`source code`: http://bitbucket.org/akorn/wheezy.captcha/src
.. _`virtualenv`: http://pypi.python.org/pypi/virtualenv
.. _`wheezy.captcha`: http://pypi.python.org/pypi/wheezy.captcha
