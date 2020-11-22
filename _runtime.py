# from functools import wraps
#
# GLOBEKWARGS = dict()
#
# def global_resolve(func):
#     @wraps(func)
#     def wrapper(self, *args, **kwargs):
#         globeargs = GLOBEKWARGS.setdefault(None, [])
#         GLOBEKWARGS.update(kwargs)
#         globeargs.extend(args[::-1])
#         try:
#             return func()
#         finally:
#             pass
#     return wrapper
