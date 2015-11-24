import os
import pickle
import time
from hashlib import sha1

CACHE_DIR = 'cache'


def hache(function):
    _function = function

    def _cache_load(hash):
        with open('{}/{}' .format(CACHE_DIR, hash), 'rb') as f:
            result = pickle.load(f)

        return result

    def _cache_contains(hash):
        files = os.listdir(CACHE_DIR)
        return hash in files

    def _cache_store(hash, obj):
        with open('{}/{}'.format(CACHE_DIR, hash), 'wb') as f:
            pickle.dump(obj, f)

    def _cached_function(*args):
        prehash = bytes(str(args), 'utf-8')
        hash = sha1(prehash).hexdigest()

        if _cache_contains(hash):
            result = _cache_load(hash)
        else:
            result = _function(*args)
            _cache_store(hash, result)

        return result

    return _cached_function


@hache
def f(x, y, z):
    time.sleep(2)
    return 'NO!'


@hache
def g(x, y, z):
    return 'YES!'
if __name__ == '__main__':
    print(f(1, 2, 3))


