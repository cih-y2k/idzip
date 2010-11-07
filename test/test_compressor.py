
from __future__ import with_statement

from nose.tools import eq_
import struct
import os

from cStringIO import StringIO
from idzip import compressor

def test_compress_empty():
    _eq_compress("empty.txt")
    _eq_compress("empty.txt", mtime=1234)
    _eq_compress("empty.txt", mtime=1289163286)


def test_compress_one_chunk():
    _eq_compress("one_chunk.txt")


def _eq_compress(basename, mtime=0):
    output = StringIO()
    with open("test/data/%s" % basename, "rb") as input:
        input.seek(0, os.SEEK_END)
        in_size = input.tell()
        input.seek(0)

        compressor.compress(input, in_size, output, basename, mtime)

    with open("test/data/%s.dz" % basename, "rb") as dzfile:
        expected = dzfile.read()
    got = output.getvalue()

    _eq_bytes(expected[:4], got[:4])
    eq_(mtime, struct.unpack("<I", got[4:8])[0])
    _eq_bytes(expected[8:], got[8:])


def _eq_bytes(a, b):
    i = 0
    for i, (ac, bc) in enumerate(zip(a, b)):
        if ac != bc:
            break

    context_size = 10
    assert a == b, "at %s: %r != %r" % (i,
            a[i:i+context_size], b[i:i+context_size])
