import lib,jieba

chat=lib.read_json('./result/all.json')

cnt=dict()

def add(x):
    if x in cnt:
        cnt[x]+=1
    else:
        cnt[x]=1

for x in chat:
    if x['type']=='text':
        words=jieba.cut(x['msg'],cut_all=False)
        # print(list(words))
        for w in words:
            add(w)

all=[[x,cnt[x]] for x in cnt]
all.sort(key=lambda x:x[1])
for [msg,n] in all[-100:]:
    print(n,'\t\t',msg)

print(len(all))