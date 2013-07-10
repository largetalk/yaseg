#coding:utf-8

import marisa_trie
import os


class RMMSEG(object):
    wordlist = 'Mandarin.fre'

    def __init__(self, maxlen=5):
        #self._trie = datrie.Trie([u'\u4e00', u'\u9fff']) #chinese unicode range
        self._len = maxlen
        if os.path.exists('_trie.dat'):
            self._trie = marisa_trie.Trie().load('_trie.dat')
        else:
            words = []
            with open(self.wordlist, 'rb') as f:
                for line in f:
                    freq, word, _ = line.strip().split(' ')
                    if isinstance(word, basestring):
                        word = word.decode('gbk')
                    words.append(word)

            self._trie = marisa_trie.Trie(words)
            self._trie.save('_trie.dat')


    def seg(self, sentence):
        if len(sentence) == 0:
            return ''
        if isinstance(sentence, basestring):
            sentence = sentence.decode('utf-8')

        def safe_begin(end):
            begin = end - self._len
            if begin < 0:
                begin = 0
            return begin

        end = len(sentence)  
        begin = safe_begin(end)

        result = []

        while begin < end:
            if sentence[begin:end] in self._trie or begin + 1 == end:
                result.append(sentence[begin:end])
                end = begin
                begin = safe_begin(end)
                continue
            else:
                begin += 1

        result.reverse()
        return '/'.join(result)


seg = RMMSEG()
w = '极高的地位'
print w.decode('utf-8') in seg._trie
print seg.seg('中文分词在中文信息处理中是最最基础的，无论机器翻译亦或信息检索还是其他相关应用，如果涉及中文，都离不开中文分词，因此中文分词具有极高的地位')

