import logging

dotpy = '.py'

def initlogging():
    'Initialise the logging module to send debug (and higher levels) to stderr.'
    logging.basicConfig(format = "%(asctime)s %(levelname)s %(message)s", level = logging.DEBUG)

def _rootcontext(e):
    while True:
        c = getattr(e, '__context__', None)
        if c is None:
            return e
        e = c

def invokeall(callables):
    '''Invoke every callable, even if one or more of them fail. This is mostly useful for synchronising with futures.
    If all succeeded return their return values as a list, otherwise raise all exceptions thrown as a chain.'''
    values = []
    failure = None
    for c in callables:
        try:
            obj = c()
        except Exception as e:
            _rootcontext(e).__context__ = failure
            failure = e
        else:
            values.append(obj)
    if failure is None:
        return values
    raise failure

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
