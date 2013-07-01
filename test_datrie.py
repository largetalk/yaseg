#coding:utf-8

import datrie
import string

t1 = datrie.Trie(string.ascii_lowercase)
t1[u'abc'] = 1
t1[u'bcd'] = 2
t1[u'b'] = 3
assert not u'cd' in t1
assert not u'a' in t1
assert u'abc' in t1
assert not u'abcd' in t1
print t1.items()
print '========================'

t2 = datrie.Trie([u'\u4e00', u'\u9fff']) #chinese unicode range
w1 = '地位'.decode('utf-8')
w2 = '的地位'.decode('utf-8')
w3 = '极高的地位'.decode('utf-8')
w4 = '极高'.decode('utf-8')
w5 = '的'.decode('utf-8')

t2[w2] = 1
t2[w4] = 2
t2[w5] = 3
print 'w1 %s in t2 is '%w1, w1 in t2
print 'w3 %s in t2 is '%w3, w3 in t2

assert not w1 in t2
assert w2 in t2
assert not w3 in t2
print t2.items()


