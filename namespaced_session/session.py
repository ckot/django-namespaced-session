from __future__ import absolute_import, unicode_literals

"""
functions from Martijn Pieters's answer to;

http://stackoverflow.com/questions/23011146/recursive-access-to-dictionary-and-modification
"""

def get_nested_default(dct, path):
    return reduce(lambda dct, k: dct.setdefault(k, {}), path, dct)

def set_nested(dct, path, value):
    get_nested_default(dct, path[:-1])[path[-1]] = value

def stringify_keys(path):
    return [str(part) for part in path]

class NamespacedSession(object):
    def __init__(self, request, path):
        self._path = stringify_keys(path)
        self._request = request
        # self._value = None
        self._initialize_path_if_not_exists()

    def _initialize_path_if_not_exists(self):
        self._value = get_nested_default(self._request.session, self._path)
        self.save()

    def get_sess_info(self):
        return get_nested_default(self._request.session, self._path)

    def save(self):
        self._request.session.modified = True
        self._request.session.save()

    def get(self, path):
        """returns value at path in nss"""
        pth = self._path[:]
        pth.extend(stringify_keys(path))
        return get_nested_default(self._request.session, pth)

    def set(self, path, value):
        """sets value at path within nss"""
        pth = self._path[:]
        pth.extend(stringify_keys(path))
        set_nested(self._request.session, pth, value)
        # self._value = get_nested_default(self._dct, self._path)
        self.save()

    def update(self, value):
        """performs a dict update at base path of nss"""
        orig = get_nested_default(self._request.session, self._path)
        orig.update(value)
        set_nested(self._request.session, self._path, orig)
        # self._value = get_nested_default(self._session, self._path)
        self.save()

    def clear(self):
        """empties the dict stored in the nss"""
        set_nested(self._request.session, self._path, {})
        # self._value = get_nested_default(self._dct, self._path)
        self.save()

    def delete(self, path):
        """deletes the key which is the last element in path"""
        head = path[:-1]
        key = str(path[-1])
        if len(head):
            pth = self._path[:]
            pth.extend(stringify_keys(head))
            del get_nested_default(self._request.session, pth)[key]
        else:
            del get_nested_default(self._request.session, self._path)[key]
        self.save()

    def destroy(self):
        """deletes the data stored at the path and then iteravely deletes
        the path into the session object until it finds a key with an non-
        empty dict
        """
        self.clear()
        del get_nested_default(self._request.session,
                               self._path[:-1])[self._path[-1]]
        self._path.pop()
        while len(self._path):
            curr_val = get_nested_default(self._request.session, self._path)
            if not len(curr_val):
                # found an empty dict. delete it
                parent = get_nested_default(self._request.session,
                                            self._path[:-1])
                del parent[self._path[-1]]
                # remote tail from path
                self._path.pop()
            else:
                # dict isn't empty. stop iteration
                break
        self.save()
