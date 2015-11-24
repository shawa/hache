import os
import pickle

CACHE_DIR = 'hache_cache'


def hache(function):
    ''' produce a cacheing version of the given function. This amounts to a
    persistent memoizer.'''

    _function = function

    def _cache_load(key):
        '''unpickle the object stored in the cache at the given key
        key: key whose files contents to unpickle'''

        with open('{}/{}' .format(CACHE_DIR, key), 'rb') as f:
            result = pickle.load(f)

        return result

    def _cache_contains(key):
        '''return true if the cache contains a file whose name is `key`
        key: key to look up'''

        file_names = os.listdir(CACHE_DIR)
        return key in file_names

    def _cache_store(key, obj):
        '''pickle the given object in the given key
        key: key (i.e. filename) at which to store the object'''

        with open('{}/{}'.format(CACHE_DIR, key), 'wb') as f:
            pickle.dump(obj, f)

    def _compute_key(*args, **kwargs):
        return hex(hash(_function.__name__ + str(args) + str(kwargs)))

    def _cacheing_function(*args, **kwargs):
        '''a cacheing version of the original function.
        `args`, along with the original function's __name__ name are
        stringified and hashed.
        If the function call hashes to something in the store, the contents of
        the file at that name are unpickled and returned. Otherwise, the
        function will be evaluated and the results stored for the next time.'''

        key = _compute_key(args, kwargs)

        if _cache_contains(key):
            result = _cache_load(key)
        else:
            result = _function(*args, **kwargs)
            _cache_store(key, result)

        return result

    return _cacheing_function
