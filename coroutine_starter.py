from functools import wraps

def coroutine(func):
    '''Decorator: primes func by advancing it to first yield'''
    @wraps(func)
    def init_coroutine(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen
    return init_coroutine


