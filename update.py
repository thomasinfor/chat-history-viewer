from lib import *
import os
from single_html import combine

orig='./origin/message_{}.json'
decoded='./decoded/decoded_{}.json'
i=1
msg=[]
while True:
    if not os.path.exists(orig.format(i)):
        break
    print(orig.format(i))
    if not os.path.exists(decoded.format(i)):
        decoder.decode(orig.format(i),decoded.format(i))
    msg=union(msg,MSG_parser(read_json(decoded.format(i))))
    i+=1

line=[]
for file in sorted(filter(lambda s:s[:13]=='line-original',os.listdir('./origin'))):
    file='./origin/'+file
    print(file)
    line=union(line,LINE_parser(read_txt(file)))

chat=union(msg,line)
dump(chat,'./result/all.json')
with open('./site/data.js','w+',encoding='utf-8') as f:
    f.write('const data=')
    f.write(dump(chat))
    f.write(';')
combine()