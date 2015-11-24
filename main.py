import os
import pickle
import time
from hashlib import sha1

CACHE_DIR = 'cache'

def hache(function):
    ''' produce a cacheing version of the given function. This amounts to a
    persistent memoizer.'''

    _function = function

    def _cache_load(hash):
        '''unpickle the object stored in the cache at the given hash
        hash: hash whose contents to read'''

        with open('{}/{}' .format(CACHE_DIR, hash), 'rb') as f:
            result = pickle.load(f)

        return result

    def _cache_contains(hash):
        '''return true if the cache contains a file whose name is `hash`
        hash: hash to look up'''

        files = os.listdir(CACHE_DIR)
        return hash in files

    def _cache_store(filename, obj):
        '''pickle the given object in the given filename
        filename: filename (i.e. key) at which to store the object'''

        with open('{}/{}'.format(CACHE_DIR, filename), 'wb') as f:
            pickle.dump(obj, f)

    def _cacheing_function(*args):
        '''a cacheing version of the original function.
        `args`, along with the original function's __name__ name are
        stringified and hashed.
        If the function call hashes to something in the store, the contents of
        the file at that name are unpickled and returned. Otherwise, the
        function will be evaluated and the results stored for the next time.'''

        prehash = bytes(str(args) + _function.__name__, 'utf-8')
        hash = sha1(prehash).hexdigest()

        if _cache_contains(hash):
            result = _cache_load(hash)
        else:
            result = _function(*args)
            _cache_store(hash, result)

        return result

    return _cacheing_function


if __name__ == '__main__':
    @hache
    def f(x, y, z):
        time.sleep(5)
        return 'Wait?'

    @hache
    def g(x, y, z):
        time.sleep(5)
        return 'No need to wait :)'

    for _ in range(10):
        print(g(1, 2, 3))

    for _ in range(10):
        print(f(1, 2, 3))

