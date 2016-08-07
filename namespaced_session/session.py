from __future__ import absolute_import, unicode_literals

def get_nested_default(dct, path):
    return reduce(lambda dct, k: dct.setdefault(k, {}), path, dct)

def set_nested(dct, path, value):
    get_nested_default(dct, path[:-1])[path[-1]] = value

class NamespacedSession(object):

    def __init__(self, session, path):
        self._path = [str(part) for part in path]
        self._dct = session
        self._value = None
        self._initialize_path_if_not_exists()

    def _initialize_path_if_not_exists(self):
        self._value = get_nested_default(self._dct, self._path)
        self._dct.save()

    def get_sess_info(self):
        return self._value

    def update(self, value):
        set_nested(self._dct, self._path, value)
        self._value = get_nested_default(self._dct, self._path)
        self._dct.save()

    def delete(self):
        self._value = None
        del get_nested_default(self._dct, self._path[:-1])[self._path[-1]]
        self._path.pop()
        while len(self._path):
            curr_val = get_nested_default(self._dct, self._path)
            if not len(curr_val):
                # found an empty dict. delete it
                parent = get_nested_default(self._dct, self._path[:-1])
                del parent[self._path[-1]]
                # remote tail from path
                self._path.pop()
            else:
                # dict isn't empty. stop iteration
                break
        self._dct.save()
