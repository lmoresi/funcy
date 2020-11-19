def seqlength(obj):
    try:
        return obj._seqLength()
    except AttributeError:
        return len(obj)
