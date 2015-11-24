# Hache

Dead-simple, hastily hacked-together on-disk memozier for next-day project deadline.

## Usage

1. Create a directory named `hache_cache` where all of the cached results will live

```python
from hache import hache

@hache
def f(x, y, z):
  ...  # really intensive computation/network request

```

## Pitfalls
* `sha1` overhead for each function call (is hashing really necessary?)
* I/O overhead for each function call (use a ramdisk?)
* I *think* this works as expected *il manque des tests*.
