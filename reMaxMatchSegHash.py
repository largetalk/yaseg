#coding:utf-8



class RMMSEG(object):
    wordlist = 'Mandarin.fre'

    def __init__(self, maxlen=5):
        self._dict = {}
        self._len = maxlen
        with open(self.wordlist, 'rb') as f:
            line = f.readline()
            while line:
                fre, word, _ = line.strip().split(' ')
                if isinstance(word, basestring):
                    word = word.decode('gbk')

                self._dict[word] = fre

                line = f.readline()


    def seg(self, sentence):
        sentence = sentence.replace(' ', '')
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
            if sentence[begin:end] in self._dict or begin + 1 == end:
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
print w.decode('utf-8') in seg._dict
print seg.seg('中文分词在中文信息处理中是最最基础的，无论机器翻译亦或信息检索还是其他相关应用，如果涉及中文，都离不开中文分词，因此中文分词具有极高的地位')
print seg.seg('''中国古代每经大的变乱，人口基数就会出现一次大的损耗。所谓兴亡百姓苦，中国民众剪而复生，宁是冲到了今天14亿人的大关，期间损耗人数往往以千万计。需要特别言明的是：
        一、人口损耗并非就是人口死亡，损耗数字可能源于死亡、掳掠、迁徙、隐匿等多种原因，而死亡亦包括正常死亡、人为屠杀、从军战死、饥馑疾病等原因。损耗中被掠、移民以及户口隐匿难以统计现象，与死亡人数常常相当。
        二、一段时间内原有人口的永久消失是建立在多种原因上的，即使在最艰难的社会时期，人口的自然增长还是存在的，只是出生率赶不上死亡率，因而人口基数呈下降趋势。不可以单纯的想象，现有2000万人，20年后只有1500万人，于是得出20年内死了500万人的结论。
        三、人口损耗数字随着年代的推移逐渐增加，是因为随着时代的发展中国人口总数一直在上升，而不是年代越后人们越嗜杀。。不过战争武器的愈发先进确实导致了一些战争杀戮行为更具破坏性。''')
