def singleton(cls):
    __instance = {}
    def wrapper(*args, **kwargs):
        if cls not in __instance:
            __instance[cls] = cls(*args, **kwargs)
            return __instance[cls]
        else:
            return __instance[cls]
    return wrapper