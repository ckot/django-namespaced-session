django-namespaced-session
=========================

.. image:: https://travis-ci.org/ckot/django-namespaced-session.svg?branch=master
    :target: https://travis-ci.org/ckot/django-namespaced-session


.. image:: https://coveralls.io/repos/github/ckot/django-namespaced-session/badge.svg?branch=master
    :target: https://coveralls.io/github/ckot/django-namespaced-session?branch=master


This package makes it easier to work with dictionaries in sessions. It provides
a class which makes it easy to retrieve/create a path into request.session
by specified the path as a list.

For instance ['foos', foo_id, 'bars', bar_id] represents
request.session['foos'][foo_id]['bars'][bar_id]

Any int elements in path will be converted to strings

Once created you can work with the object, without needing to specify the path
anymore.


INSTALL
--------

::

    pip install django-namespaced-session


CONFIGURATION
-------------

Make sure 'django.contrib.sessions' is in INSTALLED_APPS.  This package isn't
a proper Django 'app' - simply a class you can import - so it doesn't need to
be added to INSTALLED_APPS itself.


USAGE
-----

::

    from namespaced_session.session import NamespacedSession
    
    def some_view(request, foo_id, bar_id):
        
        # returns an object which wraps session['foos'][foo_id]['bars'][bar_id]
        # initializes the path via defaultdict if the path doesn't exist
        nss = NamespacedSession(request,
                                ['foos', foo_id, 'bars', bar_id])
        
        # returns the dict stored at session['foos'][foo_id]['bars'][bar_id]
        sess_info = nss.get_sess_info()
        
        # sets session['foos'][foo_id]['bars'][bar_id]['some_field'] = some_value
        nss.update({'some_field': some_value})
        
        # sets session['foos'][foo_id]['bars'][bar_id]["baz"] = 2
        nss.set(["baz"], 2)
        
        # sets session['foos'][foo_id]['bars'][bar_id]['boo']['qux'] = {"quux": 1}
        nss.set(["boo", "qux"], {"quux": 1})
        
        # returns {"qux": {"quux": 1}}
        nss.get(["boo"])
        
        # deletes "qux" key from "boo". sessions['foos'][foo_id]['bars'][bar_id]['boo']
        # is now an empty dict
        nss.delete(["boo", "qux"])
        
        # sets session['foos'][foo_id]['bars'][bar_id] to an empty dict
        nss.clear()
        
        # sets request.session.modified = True and also calls request.session.save()
        # this is called automatically by all methods which modify the session
        # probably should remove the call to request.session.save() for efficiency reasons
        nss.save()
        
        # clears contents stored at session['foos'][foo_id]['bars'][bar_id] and then, working
        # backwards from 'bars' all the way down to 'foos', if the
        # key's value is an empty dict, will delete that key. deletion will
        # stop at the first key whose value is not an empty dict
        nss.destroy()
