django-namespaced-session
=========================

A Django app which makes it easier to work with dictionaries in sessions.


Basically this allows you to have 2 windows/tabs in the same browser (which
will share a django session) to work with 2 instances of some app where
some identifers are shared and others are different.

For example, in my case, normal users (students) are only mapped to a single
subject_id, while staff users can have multiple subject_ids associated with
their user_id and they may want to test side-by-side  running the same task_id
using different subject_ids.  so in my case, to allow them to do this with
2 windows of the same browser that share the same session, I store the
information as:

session['tasks'][task_id]['subjects'][subject_id]


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

    from namespaced_session import get_namespaced_session

    def some_view(request, foo_id, bar_id):

        sess = get_namespaced_session(request.session,
                                      [{'foos': foo_id},
                                       {'bars': bar_id}])
        # this will retrieve an object which wraps
        # session['foos'][foo_id]['bars'][bar_id]
        # initializing session['foos'][foo_id]['bars'][bar_id] to
        # an empty dict if it doesn't already exist
        # the session will be saved if it needs to be initialized

        sess.update({'some_field': some_value})
        # this will update the dictionary stored at:
        # session['foos'][foo_id]['bars'][bar_id]
        # and the session will be saved

        sess.delete()
        # this will delete everything under
        # session['foos'][foo_id]
        # if there isn't anything else under session['foos'] that
        # will be removed as well
        # the session will be saved
