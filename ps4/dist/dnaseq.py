#!/usr/bin/env python2.7

import unittest
from dnaseqlib import *
import itertools
from tqdm import tqdm

### Utility classes ###

# Maps integer keys to a set of arbitrary values.
class Multidict:
    # Initializes a new multi-value dictionary, and adds any key-value
    # 2-tuples in the iterable sequence pairs to the data structure.
    def __init__(self, pairs=[]):
        self.d = {}
        for k, v in pairs:
            self.put(k, v)

    # Associates the value v with the key k.
    def put(self, k, v):
        if k not in self.d:
            self.d[k] = [v]
        else:
            self.d[k] = self.d[k] + [v]
    
    # Gets any values that have been associated with the key k; or, if
    # none have been, returns an empty sequence.
    def get(self, k):
        if k not in self.d:
            return []
        return self.d[k]

# Given a sequence of nucleotides, return all k-length subsequences
# and their hashes.  (What else do you need to know about each
# subsequence?)
def subsequenceHashes(seq, k):
    # 获取初始的子序列
    subseq = ''.join(itertools.islice(seq, k))
    current_hash = RollingHash(subseq)
    yield (current_hash.current_hash(), (subseq, 0))
    
    # 逐步获取下一个字符并更新哈希值
    pos = 0
    for char in seq:
        pos += 1
        current_hash.slide(subseq[0], char)
        subseq = subseq[1:] + char
        yield (current_hash.current_hash(), (subseq, pos))

# Similar to subsequenceHashes(), but returns one k-length subsequence
# every m nucleotides.  (This will be useful when you try to use two
# whole data files.)
def intervalSubsequenceHashes(seq, k, m):
    try:
        pos = 0
        while True:
            subseq = ''
            for _ in range(k):
                subseq += next(seq)
            current_hash = RollingHash(subseq)
            yield (current_hash.current_hash(), (subseq, pos))
            for _ in range(m - k):
                next(seq)
            pos += m
    except StopIteration:
        return

    
# Searches for commonalities between sequences a and b by comparing
# subsequences of length k.  The sequences a and b should be iterators
# that return nucleotides.  The table is built by computing one hash
# every m nucleotides (for m >= k).
def getExactSubmatches(a, b, k, m):
    a_dict = Multidict(intervalSubsequenceHashes(a, k, m))
    for key, value in tqdm(subsequenceHashes(b, k)):
        for subseq in a_dict.get(key):
            if subseq[0] == value[0]:
                yield (subseq[1], value[1])
        

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: {0} [file_a.fa] [file_b.fa] [output.png]'.format(sys.argv[0]))
        sys.exit(1)

    # The arguments are, in order: 1) Your getExactSubmatches
    # function, 2) the filename to which the image should be written,
    # 3) a tuple giving the width and height of the image, 4) the
    # filename of sequence A, 5) the filename of sequence B, 6) k, the
    # subsequence size, and 7) m, the sampling interval for sequence
    # A.
    compareSequences(getExactSubmatches, sys.argv[3], (500,500), sys.argv[1], sys.argv[2], 8, 100)
