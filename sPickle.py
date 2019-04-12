'''Streaming pickle implementation for efficiently serializing and
de-serializing an iterable (e.g., list)

Created on 2010-06-19 by Philip Guo
Mostly rewritten 2015-01-16 by Dustin King for Python 3.4

Not backwards compatible.
'''

from pickle import dumps, loads

def writeByteArray(byteArray, binaryFile):
    '''Write a bytearray or bytes object to a file, 
    escaping so that multiple bytearray's can be writen.
    filecontents  -> array contents
    \\ -> \
    \\n -> \n  
    \n -> end of byte array
    '''
    for byte in byteArray:
        if byte == b'\\'[0]:
            binaryFile.write(b'\\\\')
        elif byte == b'\n'[0]:
            binaryFile.write(b'\\\n')
        else:
            binaryFile.write(bytes([byte]))
    binaryFile.write(b'\n')


def writeByteArrayStream(byteArrays, binaryFile):
    for barray in byteArrays:
        writeByteArray(barray, binaryFile)

def readByteArrayStream(binaryFile):
    f = binaryFile
    buf = bytearray()
    byte = f.read(1)
    while byte != b'':
        if byte == b'\\':
            byte = f.read(1)
            if byte == b'\\':
                buf.append(b'\\'[0])
            elif byte == b'\n':
                buf.append(b'\n'[0])
            else:
                raise Exception('unexpected byte: ' + str(byte))
        elif byte == b'\n':
            yield bytes(buf)
            buf = bytearray()
        else:
            buf.append(byte[0])
        byte = f.read(1)

def pickleIterable(iterable):
    for item in iterable:
        yield dumps(item)

          

def s_dump(iterable_to_pickle, file_obj):
    '''dump contents of an iterable iterable_to_pickle to file_obj, a file
    opened in write mode'''
    writeByteArrayStream(pickleIterable(iterable_to_pickle), file_obj)

def s_dump_elt(elt, file_obj):
    writeByteArray(dumps(elt), file_obj)

def s_load(file_obj):
    '''load contents from file_obj, returning a generator that yields one
    element at a time'''
    for barray in readByteArrayStream(file_obj):
        yield loads(barray)

