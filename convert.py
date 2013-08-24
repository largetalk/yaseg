import os
import json


if not os.path.exists('douban'):
    os.mkdir('douban')


for line in open('items.dat', 'rb'):
    dic = json.loads(line)
    with open('douban/%s.txt' % dic['nid'], 'wb+') as f:
        f.write(dic['title'].encode('utf8'))
        f.write('\r\n\r\n')
        f.write(dic['content'].encode('utf8'))
