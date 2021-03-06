# Streaming Pickle Reloaded

This is a fork of [streaming-pickle](https://github.com/pgbovine/streaming-pickle) (as of when it lived on [Google Code](https://code.google.com/archive/p/streaming-pickle/) ), which, as one might guess, is a streaming version of Pickle.  [Pickle](https://docs.python.org/3/library/pickle.html) is the built in serialization library in Python.  

This project was forked from streaming-pickle to support Python 3, in order to upgrade a specific internal project I was working on.  This version is NOT backwards compatible with Python 2.x.  The fork consisted of adding tests (sPickle_test.py), and then mostly rewriting sPickle.py.

The API (see "Public Functions" below) should contain everything as of the time it was forked, but the streaming format is changed.  But then Pickle's format isn't guaranteed to stay the same between Python releases either.  So you should only use this (or Pickle, for that matter) for data that doesn't need to live longer than a Python release.  

Pickle lets you serialize objects, including lists of objects.  However, if you have an iterable of objects that is big enough that you don't want to keep them all in memory at once, a streaming format like this might be useful.  It also might be useful if you want to send some objects to a downstream process before the following objects are available.  As with Pickle, sender and receiver should be on the same version of Python.  

This reads and writes to file-like objects, so it could be used to stream over a socket, but networking is up to you.  The same caution as with Pickle applies: you shouldn't de-serialize data from untrusted sources.

## Public Functions:

* `s_dump(iterable_to_pickle, file_obj)` - Dump contents of an iterable `iterable_to_pickle` to `file_obj`, a file
    that is opened in write+binary mode.
* `s_dump_elt(elt, file_obj)` Dump a single element to an open file.
* `s_load(file_obj)` - Load contents from `file_obj`, open in read+binary mode, returning a generator that yields one
  element at a time

## Usage example:

```python
>>> from sPickle import *
>>> with open('a_file.whatever', 'wb') as f:
...     s_dump(['one', 'two', 'three'], f)
...     s_dump_elt('four', f)
...
>>> with open('a_file.whatever', 'rb') as f:
...     for element in s_load(f):
...         print(element)
...
one
two
three
four
```
