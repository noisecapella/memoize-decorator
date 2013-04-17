import collections
import functools
import os.path

import logging
logging.basicConfig()
_logger = logging.getLogger("memoize")

try:
    from cPickle import dumps, loads, dump, load
except:
    from pickle import dumps, loads, dump, load

# originally from http://wiki.python.org/moin/PythonDecoratorLibrary#Memoize

def memoize(version, filepath=None):
    def f(func):
        if filepath is None:
            try:
                func_name = func.im_class.__name__ + "." + func.__name__
            except AttributeError:
                func_name = func.__name__
            arg_filepath = func_name + ".memoize_cache"
        return memoize_inner(func, version=version, filepath=arg_filepath)
    return f

class memoize_inner(object):
    '''Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    '''
    def __init__(self, func, version, filepath):
        self.func = func
        self.version = version
        self.filepath = filepath
        self.cache = {}

        try:
            if os.path.exists(self.filepath):
                with open(self.filepath, 'rb') as f:
                    cache, version = load(f)
                    if version == self.version:
                        self.cache = cache
        except Exception, e:
            # oh well
            _logger.exception(e)

    def __call__(self, *args, **kwargs):
        return self.call(args, kwargs, False)

    def call_instance_method(self, *args, **kwargs):
        return self.call(args, kwargs, True)

    def call(self, args, kwargs, is_instance_method):
        try:
            if is_instance_method:
                key = (args[1:], kwargs)
            else:
                key = (args, kwargs)
            arg_hash = dumps(key)
        except Exception, e:
            # arguments are unpickleable
            _logger.exception(e)
            return self.func(*args, **kwargs)
        
        if arg_hash in self.cache:
            try:
                return loads(self.cache[arg_hash])
            except Exception, e:
                _logger.exception(e)
                return self.func(*args, **kwargs)

        # not in cache, create it
        ret = self.func(*args, **kwargs)
        try:
            ret_hash = dumps(ret)
        except Exception, e:
            _logger.exception(e)
            return ret

        self.cache[arg_hash] = ret_hash

        to_save = (self.cache, self.version)
        with open(self.filepath, 'wb') as f:
            dump(to_save, f)
            
        return ret

    def __repr__(self):
        '''Return the function's docstring.'''
        return self.func.__doc__
    def __get__(self, obj, objtype):
        '''Support instance methods.'''
        return functools.partial(self.call_instance_method, obj)

