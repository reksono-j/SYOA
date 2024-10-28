class Singleton(type):
    _instances = {}
    
    def __call(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances
    
# Possible TODO: Maybe move this to another folder so I don't to duplicate