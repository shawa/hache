# Hache

Dead-simple, hastily hacked-together on-disk memozier for next-day project deadline.

## Usage

1. Create a directory named `hache_cache` where all of the cached results will live

```python
from hache import hache

@hache
def f(x, y, z):
    time.sleep(6)
    return x + y + z



for _ in range(10):
  print(f(1, 2, 3))  # now takes much shorter than 1 minute
```

The first call is evaluated and cached to disk.
Following calls are redirected to reading the result from disk as opposed to doing the `really intensive computation`.


## Pitfalls
* `sha1` overhead for each function call (is hashing really necessary?)
* I/O overhead for each function call (use a ramdisk? sqlite?)
* Only functions which return pickleable objects can be `hache`d.
* Takes into account only the functions' `__name__` property to differentiate between them. That is to say that if you define another function (i.e. method of a different object, nested etc) the behaviour of this thing is undefined.
* I *think* this works as expected, *mais il manque des tests*.
