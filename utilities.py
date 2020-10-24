from wordhash import w_hash

def is_numeric(arg):
    try:
        _ = arg + 1
        return True
    except:
        return False
