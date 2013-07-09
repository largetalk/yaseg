class Word:  
    def __init__(self,text = '',freq = 0):  
        self.text = text  
        self.freq = freq  
        self.length = len(text)  
  
class Chunk:  
    def __init__(self,w1,w2 = None,w3 = None):  
        self.words = []  
        self.words.append(w1)  
        if w2:  
            self.words.append(w2)  
        if w3:  
            self.words.append(w3)  
      
    #计算chunk的总长度  
    def totalWordLength(self):  
        length = 0  
        for word in self.words:  
            length += len(word.text)  
        return length  
      
    #计算平均长度  
    def averageWordLength(self):  
        return float(self.totalWordLength()) / float(len(self.words))  
      
    #计算标准差  
    def standardDeviation(self):  
        average = self.averageWordLength()  
        sum = 0.0  
        for word in self.words:  
            tmp = (len(word.text) - average)  
            sum += float(tmp) * float(tmp)  
        return sum  
      
    #自由语素度  
    def wordFrequency(self):  
        sum = 0  
        for word in self.words:  
            sum += word.freq  
        return sum  
  
class ComplexCompare:  
      
    def takeHightest(self,chunks,comparator):  
        i = 1  
        for j in range(1, len(chunks)):  
            rlt = comparator(chunks[j], chunks[0])  
            if rlt > 0:  
                i = 0  
            if rlt >= 0:  
                chunks[i], chunks[j] = chunks[j], chunks[i]  
                i += 1  
        return chunks[0:i]  
      
    #以下四个函数是mmseg算法的四种过滤原则，核心算法  
    def mmFilter(self,chunks):  
        def comparator(a,b):  
            return a.totalWordLength() - b.totalWordLength()  
        return self.takeHightest(chunks,comparator)  
      
    def lawlFilter(self,chunks):  
        def comparator(a,b):  
            return a.averageWordLength() - b.averageWordLength()  
        return self.takeHightest(chunks,comparator)  
      
    def svmlFilter(self,chunks):  
        def comparator(a,b):  
            return b.standardDeviation() - a.standardDeviation()  
        return self.takeHightest(chunks, comparator)  
      
    def logFreqFilter(self,chunks):  
        def comparator(a,b):  
            return a.wordFrequency() - b.wordFrequency()  
        return self.takeHightest(chunks, comparator)  
   
   
#加载词组字典和字符字典  
dictWord = {}  
maxWordLength = 0  
      
def loadDictChars(filepath):  
    global maxWordLength  
    fsock = file(filepath)  
    for line in fsock.readlines():  
        freq, word = line.split(' ')  
        word = unicode(word.strip(), 'utf-8')  
        dictWord[word] = (len(word), int(freq))  
        maxWordLength = maxWordLength < len(word) and len(word) or maxWordLength  
    fsock.close()  
      
def loadDictWords(filepath):  
    global maxWordLength  
    fsock = file(filepath)  
    for line in fsock.readlines():  
        word = unicode(line.strip(), 'utf-8')  
        dictWord[word] = (len(word), 0)  
        maxWordLength = maxWordLength < len(word) and len(word) or maxWordLength  
    fsock.close()  
  
#判断该词word是否在字典dictWord中      
def getDictWord(word):  
    result = dictWord.get(word)  
    if result:  
        return Word(word,result[1])  
    return None  
      
#开始加载字典  
def run():  
    from os.path import join, dirname  
    loadDictChars(join(dirname(__file__), 'data', 'chars.dic'))  
    loadDictWords(join(dirname(__file__), 'data', 'words.dic'))  
  
class Analysis:  
      
    def __init__(self,text):  
        if isinstance(text,unicode):  
            self.text = text  
        else:  
            self.text = text.encode('utf-8')  
        self.cacheSize = 3  
        self.pos = 0  
        self.textLength = len(self.text)  
        self.cache = []  
        self.cacheIndex = 0  
        self.complexCompare = ComplexCompare()  
          
        #简单小技巧，用到个缓存，不知道具体有没有用处  
        for i in range(self.cacheSize):  
            self.cache.append([-1,Word()])  
          
        #控制字典只加载一次  
        if not dictWord:  
            run()  
      
    def __iter__(self):  
        while True:  
            token = self.getNextToken()  
            if token == None:  
                raise StopIteration  
            yield token  
              
    def getNextChar(self):  
        return self.text[self.pos]  
          
    #判断该字符是否是中文字符（不包括中文标点）    
    def isChineseChar(self,charater):  
        return 0x4e00 <= ord(charater) < 0x9fa6  
          
    #判断是否是ASCII码  
    def isASCIIChar(self, ch):  
        import string  
        if ch in string.whitespace:  
            return False  
        if ch in string.punctuation:  
            return False  
        return ch in string.printable  
      
    #得到下一个切割结果  
    def getNextToken(self):  
        while self.pos < self.textLength:  
            if self.isChineseChar(self.getNextChar()):  
                token = self.getChineseWords()  
            else :  
                token = self.getASCIIWords()+'/'  
            if len(token) > 0:  
                return token  
        return None  
      
    #切割出非中文词  
    def getASCIIWords(self):  
        # Skip pre-word whitespaces and punctuations  
        #跳过中英文标点和空格  
        while self.pos < self.textLength:  
            ch = self.getNextChar()  
            if self.isASCIIChar(ch) or self.isChineseChar(ch):  
                break  
            self.pos += 1  
        #得到英文单词的起始位置      
        start = self.pos  
          
        #找出英文单词的结束位置  
        while self.pos < self.textLength:  
            ch = self.getNextChar()  
            if not self.isASCIIChar(ch):  
                break  
            self.pos += 1  
        end = self.pos  
          
        #Skip chinese word whitespaces and punctuations  
        #跳过中英文标点和空格  
        while self.pos < self.textLength:  
            ch = self.getNextChar()  
            if self.isASCIIChar(ch) or self.isChineseChar(ch):  
                break  
            self.pos += 1  
              
        #返回英文单词  
        return self.text[start:end]  
      
    #切割出中文词，并且做处理，用上述4种方法  
    def getChineseWords(self):  
        chunks = self.createChunks()  
        if len(chunks) > 1:  
            chunks = self.complexCompare.mmFilter(chunks)  
        if len(chunks) > 1:  
            chunks = self.complexCompare.lawlFilter(chunks)  
        if len(chunks) > 1:  
            chunks = self.complexCompare.svmlFilter(chunks)  
        if len(chunks) > 1:  
            chunks = self.complexCompare.logFreqFilter(chunks)  
        if len(chunks) == 0 :  
            return ''  
          
        #最后只有一种切割方法  
        word = chunks[0].words  
        token = ""  
        length = 0  
        for x in word:  
            if x.length <> -1:  
                token += x.text + "/"  
                length += len(x.text)  
        self.pos += length  
        return token  
      
    #三重循环来枚举切割方法，这里也可以运用递归来实现  
    def createChunks(self):  
        chunks = []  
        originalPos = self.pos  
        words1 = self.getMatchChineseWords()  
          
        for word1 in words1:  
            self.pos += len(word1.text)  
            if self.pos < self.textLength:  
                words2 = self.getMatchChineseWords()  
                for word2 in words2:  
                    self.pos += len(word2.text)  
                    if self.pos < self.textLength:  
                        words3 = self.getMatchChineseWords()  
                        for word3 in words3:  
                            print word3.length,word3.text  
                            if word3.length == -1:  
                                chunk = Chunk(word1,word2)  
                                print "Ture"  
                            else :  
                                chunk = Chunk(word1,word2,word3)  
                            chunks.append(chunk)  
                    elif self.pos == self.textLength:  
                        chunks.append(Chunk(word1,word2))  
                    self.pos -= len(word2.text)  
            elif self.pos == self.textLength:  
                chunks.append(Chunk(word1))  
            self.pos -= len(word1.text)  
                                  
        self.pos = originalPos  
        return chunks  
      
    #运用正向最大匹配算法结合字典来切割中文文本    
    def getMatchChineseWords(self):  
        #use cache,check it   
        for i in range(self.cacheSize):  
            if self.cache[i][0] == self.pos:  
                return self.cache[i][1]  
              
        originalPos = self.pos  
        words = []  
        index = 0  
        while self.pos < self.textLength:  
            if index >= maxWordLength :  
                break  
            if not self.isChineseChar(self.getNextChar()):  
                break  
            self.pos += 1  
            index += 1  
              
            text = self.text[originalPos:self.pos]  
            word = getDictWord(text)  
            if word:  
                words.append(word)  
                  
        self.pos = originalPos  
        #没有词则放置个‘X’，将文本长度标记为-1  
        if not words:  
            word = Word()  
            word.length = -1  
            word.text = 'X'  
            words.append(word)  
          
        self.cache[self.cacheIndex] = (self.pos,words)  
        self.cacheIndex += 1  
        if self.cacheIndex >= self.cacheSize:  
            self.cacheIndex = 0  
        return words  
