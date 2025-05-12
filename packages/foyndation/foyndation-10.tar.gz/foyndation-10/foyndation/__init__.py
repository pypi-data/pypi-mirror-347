import logging

dotpy = '.py'

def initlogging():
    'Initialise the logging module to send debug (and higher levels) to stderr.'
    logging.basicConfig(format = "%(asctime)s %(levelname)s %(message)s", level = logging.DEBUG)

def rmsuffix(text, suffix):
    'Return text with suffix removed, or `None` if text does not end with suffix.'
    if text.endswith(suffix):
        return text[:-len(suffix)]

def singleton(t):
    '''The decorated class is replaced with a no-arg instance.
    Can also be used to replace a factory function with its result.'''
    return t()

def solo(v):
    'Assert exactly one object in the given sequence and return it.'
    x, = v
    return x
