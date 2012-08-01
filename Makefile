.SILENT: clean env doctest-cover test doc release upload
.PHONY: clean env doctest-cover test doc release upload

VERSION=2.7
PYPI=http://pypi.python.org/simple
DIST_DIR=dist

PYTHON=env/bin/python$(VERSION)
EASY_INSTALL=env/bin/easy_install-$(VERSION)
PYTEST=env/bin/py.test-$(VERSION)
NOSE=env/bin/nosetests-$(VERSION)
SPHINX=/usr/bin/python /usr/bin/sphinx-build

all: clean doctest-cover test release

debian:
	apt-get -y update
	apt-get -y dist-upgrade
	# How to Compile Python from Source
	# http://mindref.blogspot.com/2011/09/compile-python-from-source.html
	apt-get -y install libbz2-dev build-essential python \
		python-dev python-setuptools python-virtualenv \
		python-sphinx libfreetype6-dev libjpeg8-dev

env:
	# The following packages available for python < 3.0
	if [ "$$(echo $(VERSION) | sed 's/\.//')" -lt 30 ]; then \
		PYTHON_EXE=/usr/local/bin/python$(VERSION); \
		if [ ! -x $$PYTHON_EXE ]; then \
			PYTHON_EXE=/usr/bin/python$(VERSION); \
		fi;\
		VIRTUALENV_USE_SETUPTOOLS=1; \
		export VIRTUALENV_USE_SETUPTOOLS; \
		virtualenv --python=$$PYTHON_EXE \
			--no-site-packages env; \
		if [ "$$(echo $(VERSION) | sed 's/\.//')" -ge 30 ]; then \
			echo -n 'Upgrading distribute...'; \
			$(EASY_INSTALL) -i $(PYPI) -U -O2 distribute \
				> /dev/null 2>/dev/null; \
			echo 'done.'; \
		fi; \
		$(EASY_INSTALL) -i $(PYPI) -O2 coverage nose pytest \
			pytest-pep8 pytest-cov wheezy.caching wheezy.http; \
		$(PYTHON) setup.py develop -i $(PYPI); \
	fi;

clean:
	find src/ -type d -name __pycache__ | xargs rm -rf
	find src/ -name '*.py[co]' -delete
	rm -rf dist/ build/ MANIFEST src/*.egg-info .cache .coverage

release:
	if [ "$$(echo $(VERSION) | sed 's/\.//')" -lt 30 ]; then \
		$(PYTHON) setup.py -q bdist_egg; \
	fi

upload:
	REV=$$(hg head --template '{rev}');\
	if [ "$$(echo $(VERSION) | sed 's/\.//')" -eq 27 ]; then \
		$(PYTHON) setup.py -q egg_info --tag-build .$$REV \
			sdist register upload; \
		$(EASY_INSTALL) -i $(PYPI) sphinx; \
		$(PYTHON) env/bin/sphinx-build -D release=0.1.$$REV \
			-a -b html doc/ doc/_build/;\
		python setup.py upload_docs; \
	fi; \
	if [ "$$(echo $(VERSION) | sed 's/\.//')" -lt 30 ]; then \
		$(PYTHON) setup.py -q egg_info --tag-build .$$REV \
			bdist_egg --dist-dir=$(DIST_DIR) \
			rotate --match=$(VERSION).egg --keep=1 --dist-dir=$(DIST_DIR) \
			upload; \
	fi

test:
	# The can be run for python < 3.0
	if [ "$$(echo $(VERSION) | sed 's/\.//')" -lt 30 ]; then \
		$(PYTEST) -q -x --pep8 --doctest-modules \
			src/wheezy/captcha demos/; \
	fi

doctest-cover:
	# The can be run for python < 3.0
	if [ "$$(echo $(VERSION) | sed 's/\.//')" -lt 30 ]; then \
		$(NOSE) --stop --with-doctest --detailed-errors \
			--with-coverage --cover-package=wheezy.captcha; \
	fi

test-cover:
	$(PYTEST) -q --cov wheezy.caching \
		--cov-report term-missing \
		src/wheezy/captcha/tests

doc:
	$(SPHINX) -a -b html doc/ doc/_build/

test-demos:
	$(PYTEST) -q -x

run:
	$(PYTHON) demos/app.py

uwsgi:
	env/bin/uwsgi --http-socket 0.0.0.0:8080  --disable-logging \
		--virtualenv env --master --optimize 2 \
		--wsgi app:main --pythonpath demos
