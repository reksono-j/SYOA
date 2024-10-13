

# https://plainenglish.io/blog/better-python-singleton-with-a-metaclass

class Singleton(type):
    _instances = {}
    
    def __call(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances