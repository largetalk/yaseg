#coding:utf-8
import jieba
from gensim import corpora, models, similarities
import os
import random
from pprint import pprint
import collections

RESULT_DIR = 'douban_result'

PUNCTUATION_TABLE = [
    # start,  stop
    (0x2000, 0x206f), # General Punctuation
    (0x3000, 0x303f), # CJK Symbols and Punctuation
    (0x4e00, 0x9fa5),
    (0xff00, 0xffef), # Halfwidth and Fullwidth Forms
    (0x00, 0x40), # ascii special charactors
    (0x5b, 0x60), # ascii special charactors
    (0x7b, 0xff), # ascii special charactors
]

PUNCTUATION_RANGE = reduce(lambda x, y: x.union(y), [range(start, stop+1) for start, stop in PUNCTUATION_TABLE], set())

import string  
import re  
  
regex = re.compile(ur"[^\u4e00-\u9f5aa-zA-Z0-9]")
    

class DoubanDoc(object):
    def __init__(self, root_dir='douban'):
        self.root_dir = root_dir

    def __iter__(self):
        for name in os.listdir(self.root_dir):
            if os.path.isfile(os.path.join(self.root_dir, name)):
                data = open(os.path.join(self.root_dir, name), 'rb').read()
                title = data[:data.find('\r\n')]
                yield (name, title, data)

def get_dictionary():
    if os.path.exists(os.path.join(RESULT_DIR, 'douban_note.dict')):
        return corpora.Dictionary.load(os.path.join(RESULT_DIR, 'douban_note.dict'))
    texts = []
    for name, title, data in DoubanDoc():
        def etl(s): #remove 标点和特殊字符
            s = regex.sub('', s)
            return s

        seg = filter(lambda x: len(x) > 0, map(etl, jieba.cut(data, cut_all=False)))
        #print seg
        #for x in seg:
        #    print x
        #import pdb
        #pdb.set_trace()
        #1/0
        texts.append(seg)

    # remove words that appear only once
    all_tokens = sum(texts, [])
    tokens_counter = collections.Counter(all_tokens)
    texts = [[word for word in text if tokens_counter[word] != 1] for text in texts]

    dictionary = corpora.Dictionary(texts)
    dictionary.save(os.path.join(RESULT_DIR, 'douban_note.dict'))
    return dictionary

class DoubanCorpus(object):
    def __init__(self, root_dir='douban', dictionary=get_dictionary()):
        self.root_dir = root_dir
        self.dictionary = dictionary

    def __iter__(self):
        for name, title, data in DoubanDoc(self.root_dir):
            yield self.dictionary.doc2bow(jieba.cut(data, cut_all=False))

def get_corpus():
    if os.path.exists(os.path.join(RESULT_DIR, 'douban_note.mm')):
        return corpora.MmCorpus(os.path.join(RESULT_DIR, 'douban_note.mm'))
    corpus = list(DoubanCorpus())
    corpora.MmCorpus.serialize(os.path.join(RESULT_DIR, 'douban_note.mm'), corpus)
    return corpus

def get_lsi(dictionary=get_dictionary(), corpus=get_corpus()):
    if os.path.exists(os.path.join(RESULT_DIR, 'douban_note.lsi')):
        return models.LsiModel.load(os.path.join(RESULT_DIR, 'douban_note.lsi'))
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=30)
    lsi.save(os.path.join(RESULT_DIR, 'douban_note.lsi'))
    return lsi

def get_index(lsi, corpus):
    if os.path.exists(os.path.join(RESULT_DIR, 'douban_note.idx')):
        return similarities.MatrixSimilarity.load(os.path.join(RESULT_DIR, 'douban_note.idx'))
    index = similarities.MatrixSimilarity(lsi[corpus])
    index.save(os.path.join(RESULT_DIR, 'douban_note.idx'))
    return index

def random_doc():
    name = random.choice(os.listdir('douban'))
    data = open('douban/%s'%name, 'rb').read()
    print 'random choice ', name
    return name, data

def main():
    dictionary = get_dictionary()
    corpus = get_corpus()
    lsi = get_lsi(dictionary, corpus)
    i = 0
    for t in lsi.print_topics(30):
        print '[topic #%s]: '%i, t
        i+=1

    index = get_index(lsi, corpus)
    _, doc = random_doc()
    vec_bow = dictionary.doc2bow(jieba.cut(doc, cut_all=False))
    vec_lsi = lsi[vec_bow]
    print 'topic probability:'
    pprint(vec_lsi)
    sims = sorted(enumerate(index[vec_lsi]), key=lambda item: -item[1])
    print 'top 10 similary notes:'
    #pprint(sims[:10])
    files = os.listdir('douban')
    def read_title(fn):
        data = open(os.path.join('douban', fn), 'rb').read()
        title = data[:data.find('\r\n')]
        return title

    for item in sims[:10]:
        print files[item[0]], '     ', item[1], '   ', read_title(files[item[0]])

    s = "','".join([ files[i[0]][:-4] for i in sims[:10]])
    print '{"nid":{$in : [\'%s\']}}' % s



if __name__ == '__main__':
    main()

    
