django-namespaced-session
=========================

.. image:: https://travis-ci.org/travis-ci/travis-web.svg?branch=master
    :target: https://travis-ci.org/travis-ci/travis-web

.. image:: https://coveralls.io/repos/github/ckot/django-namespaced-session/badge.svg?branch=master
:target: https://coveralls.io/github/ckot/django-namespaced-session?branch=master


A Django app which makes it easier to work with dictionaries in sessions.

This package provides a class which makes it easy to retrieve/create a path
into request.session by specified the path as a list/tuple.

for instance ['foos', foo_id, 'bars', bar_id] represents
request.session['foos'][foo_id]['bars'][bar_id]

any int elements in path will be converted to strings

once created you work with the object (which wraps the dict stored at path),
so you can perform updates or delete without needing to specify the path anymore


INSTALL
--------

::

    pip install django-namespaced-session


CONFIGURATION
-------------

Make sure 'django.contrib.sessions' is in INSTALLED_APPS



USAGE
-----

::

    from namespaced_session.session import NamespacedSession

    def some_view(request, foo_id, bar_id):

        # returns an object which wraps session['foos'][foo_id]['bars'][bar_id]
        sess = NamespacedSession(request.session,
                                 ['foos', foo_id, 'bars', bar_id])

        # returns the dict stored at session['foos'][foo_id]['bars'][bar_id]
        sess_info = sess.get_sess_info()

        # sets session['foos'][foo_id]['bars'][bar_id]['some_field'] = some_value
        sess.update({'some_field': some_value})

        # deletes session['foos'][foo_id]['bars'][bar_id] and then, working
        # backwards from 'bars' all the way down to 'foos', if the
        # key's value is an empty dict, will delete that key. deletion will
        # stop at the first key whose value is not an empty dict
        sess.delete()
