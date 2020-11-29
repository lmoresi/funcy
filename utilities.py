from wordhash import w_hash

def is_numeric(arg):
    try:
        _ = arg + 1
        return True
    except:
        return False

def kwargstr(**kwargs):
    outs = []
    for key, val in sorted(kwargs.items()):
        if not type(val) is str:
            try:
                val = val.namestr
            except AttributeError:
                try:
                    val = val.__name__
                except AttributeError:
                    val = str(val)
        outs.append(': '.join((key, val)))
    return '{' + ', '.join(outs) + '}'

def process_scalar(scal):
    return scal.dtype.type(scal)

def unpack_tuple(ks, vs):
    for k, v in zip(ks, vs):
        if type(k) is tuple:
            for sk, sv in unpack_tuple(k, v):
                yield sk, sv
        else:
            yield k, v
