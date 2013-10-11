.SILENT: clean env doctest-cover qa test doc release upload po
.PHONY: clean env doctest-cover qa test doc release upload po

VERSION=2.7
PYPI=http://pypi.python.org/simple
DIST_DIR=dist

PYTHON=env/bin/python$(VERSION)
EASY_INSTALL=env/bin/easy_install-$(VERSION)
PYTEST=env/bin/py.test-$(VERSION)
NOSE=env/bin/nosetests-$(VERSION)
SPHINX=env/bin/python$(VERSION) env/bin/sphinx-build

all: clean po doctest-cover test release

debian:
	apt-get -y update
	apt-get -y dist-upgrade
	# How to Compile Python from Source
	# http://mindref.blogspot.com/2011/09/compile-python-from-source.html
	apt-get -y install libbz2-dev build-essential python \
		python-dev python-setuptools python-virtualenv \
		python-sphinx gettext libfreetype6-dev libjpeg8-dev

env:
	PYTHON_EXE=/usr/local/bin/python$(VERSION) ; \
	if [ ! -x $$PYTHON_EXE ]; then \
		PYTHON_EXE=/opt/local/bin/python$(VERSION) ; \
		if [ ! -x $$PYTHON_EXE ]; then \
			PYTHON_EXE=/usr/bin/python$(VERSION) ; \
		fi ; \
	fi ; \
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
	if [ "$$(echo $(VERSION) | sed 's/\.//')" -lt 30 ]; then \
		$(EASY_INSTALL) -i $(PYPI) -O2 PIL; \
	else \
		$(EASY_INSTALL) -i $(PYPI) -O2 pillow; \
	fi ; \
	$(PYTHON) setup.py develop -i $(PYPI)

clean:
	find src/ -type d -name __pycache__ | xargs rm -rf
	find src/ -name '*.py[co]' -delete
	find i18n/ -name '*.mo' -delete
	rm -rf dist/ build/ MANIFEST src/*.egg-info .cache .coverage

release:
	$(PYTHON) setup.py -q bdist_egg

upload:
	REV=$$(hg head --template '{rev}');\
	sed -i "s/'0.1'/'0.1.$$REV'/" src/wheezy/captcha/__init__.py ; \
	if [ "$$(echo $(VERSION) | sed 's/\.//')" -eq 27 ]; then \
		$(PYTHON) setup.py -q egg_info --tag-build .$$REV \
			sdist register upload; \
		$(EASY_INSTALL) -i $(PYPI) sphinx; \
		$(PYTHON) env/bin/sphinx-build -D release=0.1.$$REV \
			-a -b html doc/ doc/_build/;\
		python setup.py upload_docs; \
	fi; \
	$(PYTHON) setup.py -q egg_info --tag-build .$$REV \
		bdist_egg --dist-dir=$(DIST_DIR) \
		rotate --match=$(VERSION).egg --keep=1 --dist-dir=$(DIST_DIR) \
		upload

qa:
	if [ "$$(echo $(VERSION) | sed 's/\.//')" -eq 27 ]; then \
		flake8 --max-complexity 10 demos doc src setup.py && \
		pep8 demos doc src setup.py ; \
	fi

test:
	$(PYTEST) -q -x --pep8 --doctest-modules \
		src/wheezy/captcha demos/

doctest-cover:
	$(NOSE) --stop --with-doctest --detailed-errors \
		--with-coverage --cover-package=wheezy.captcha

test-cover:
	$(PYTEST) -q --cov wheezy.caching \
		--cov-report term-missing \
		src/wheezy/captcha/tests

doc:
	$(SPHINX) -a -b html doc/ doc/_build/

test-demos:
	$(PYTEST) -q -x

po:
	xgettext --join-existing --sort-by-file --omit-header \
		--add-comments \
		-o i18n/captcha.po src/wheezy/captcha/*.py
	cp i18n/captcha.po i18n/en/LC_MESSAGES
	for l in `ls --hide *.po i18n`; do \
		/bin/echo -n "$$l => "; \
		msgfmt -v i18n/$$l/LC_MESSAGES/captcha.po \
			-o i18n/$$l/LC_MESSAGES/captcha.mo; \
	done

run:
	$(PYTHON) demos/app.py

uwsgi:
	env/bin/uwsgi --http-socket 0.0.0.0:8080  --disable-logging \
		--virtualenv env --master --optimize 2 \
		--wsgi app:main --pythonpath demos
