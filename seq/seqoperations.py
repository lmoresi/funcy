import itertools
from collections.abc import Iterable, Sized

from reseed import Reseed
from ..special import *

def shuffled(sequence, seed = None):
    sequence = [*sequence]
    Reseed.shuffle(sequence, seed = seed)
    return sequence

def chainiter(superseq):
    seqs = (s if isinstance(s, Iterable) else (s,) for s in superseq)
    return itertools.chain.from_iterable(seqs)

def productiter(superseq):
    seqs = [s if isinstance(s, Iterable) else (s,) for s in superseq]
    return itertools.product(*seqs)

def zipiter(superseq):
    seqs = []
    nIters = 0
    for s in superseq:
        if isinstance(s, Iterable):
            seqs.append(iter(s))
            nIters += 1
        else:
            seqs.append(itertools.repeat(s))
    if not nIters:
        raise StopIteration
    stopped = []
    everstopped = 0
    while True:
        out = []
        for i, (si, s) in enumerate(zip(seqs, superseq)):
            try:
                out.append(next(si))
            except StopIteration:
                out.append(None)
                stopped.append(i)
                everstopped += 1
        if everstopped == nIters:
            break
        else:
            if stopped:
                for i in stopped:
                    si = seqs[i] = iter(superseq[i])
                    out[i] = next(si)
                stopped.clear()
            yield tuple(out)
