cms
***

Django application

Install
=======

Virtual Environment
-------------------

Note: replace ``patrick`` with your name (checking in the ``example`` folder
to make sure a file has been created for you)::

  mkvirtualenv dev_cms
  pip install -r requirements/local.txt

  echo "export DJANGO_SETTINGS_MODULE=example.dev_patrick" >> $VIRTUAL_ENV/bin/postactivate
  echo "unset DJANGO_SETTINGS_MODULE" >> $VIRTUAL_ENV/bin/postdeactivate

  add2virtualenv .
  deactivate

Testing
=======

Using ``pytest-django``::

  workon dev_cms
  find . -name '*.pyc' -delete
  py.test

To stop on first failure::

  py.test -x

Usage
=====

::

  workon dev_cms

  py.test -x && \
      touch temp.db && rm temp.db && \
      django-admin.py syncdb --noinput && \
      django-admin.py migrate --all --noinput && \
      django-admin.py demo_data_login && \
      django-admin.py init_app_cms && \
      django-admin.py demo_data_cms && \
      django-admin.py runserver

Release
=======

https://github.com/pkimber/docs
