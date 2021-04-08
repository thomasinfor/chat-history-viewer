import re,json
from datetime import datetime

def read_txt(fn):
    with open(fn,'r',encoding='utf-8') as f:
        return f.read()

def read_json(fn):
    with open(fn,'r',encoding='utf-8') as f:
        return json.load(f)

def LINE_parser(s):
    def isdate(x):
        return len(re.findall(r'\d{4}/\d+/\d+[(（]..[）)]',x))==1
    def padding(x,l):
        return '0'*(l-len(x))+x
    chat=[]
    for line in s.split('\n'):
        line=line.strip(' \n\ufeff')
        if len(line)==0:
            continue;
        elif isdate(line):
            yyyy,mm,dd=line.split('/')
            dd=dd.split('(')[0].split('（')[0]
            yyyy,mm,dd=padding(yyyy,2),padding(mm,2),padding(dd,2)
        else:
            if len(line.split('\t'))==3:
                time,user,msg=line.split('\t')
                if len(time)==4:
                    time='0'+time
                if time[:2]=='24':
                    time='00'+time[2:]
                chat.append({
                    'time':f'{yyyy}-{mm}-{dd} {time}',
                    'user':user, 'type':'text', 'msg':msg, 'app':'LINE'
                })
            else:
                if len(chat)!=0:
                    chat[-1]['msg']+='\n'+line
    return chat

NAME_MAP={'Thomas Wang': '王勻'}

def MSG_parser(orig):
    def get_time(x):
        return datetime.fromtimestamp(x//1000).strftime("%Y-%m-%d %H:%M")
    def user_map(u):
        if u in NAME_MAP:
            return NAME_MAP[u]
        else:
            return u
    orig['messages'].sort(key=lambda x:x['timestamp_ms'])
    chat=[]
    for line in orig['messages']:
        # print(line)
        # empty
        if len(line)==3 or (len(line)==4 and 'ip' in line):
            continue;
        cnt=0
        # sticker
        if 'sticker' in line:
            chat.append({
                'type':'sticker', 'sticker':line['sticker']['uri']
            })
            cnt+=1
        # share
        if line['type']=='Share':
            if bool(re.findall('((sent an attachment.)|(sent a link.))$',line['content'])) and 'share' in line:
                chat.append({
                    'type':'text', 'msg':line['share']['link']
                })
                cnt+=1
            else:
                chat.append({
                    'type':'text', 'msg':line['content']
                })
                cnt+=1
        # videos
        if line['type']=='Generic' and 'videos' in line:
            chat.append({
                'type':'video', 'videos':[i["uri"] for i in line['videos']]
            })
            cnt+=1
        # audios
        if line['type']=='Generic' and 'audio_files' in line:
            chat.append({
                'type':'audio', 'audios':[i["uri"] for i in line['audio_files']]
            })
            cnt+=1
        # photos
        if line['type']=='Generic' and 'photos' in line:
            chat.append({
                'type':'photo', 'photos':[i["uri"] for i in line['photos']]
            })
            cnt+=1
        # gifs
        if line['type']=='Generic' and 'gifs' in line:
            chat.append({
                'type':'gif', 'gifs':[i["uri"] for i in line['gifs']]
            })
            cnt+=1
        # files
        if line['type']=='Generic' and 'files' in line:
            chat.append({
                'type':'file', 'files':[i["uri"] for i in line['files']]
            })
            cnt+=1
        # calls
        if line['type']=='Call':
            chat.append({
                'type':'call',
                'duration':-1 if 'missed' in line else line['call_duration']
            })
            cnt+=1
        # text
        if line['type']=='Generic' and 'content' in line:
            if cnt==0:
                chat.append({
                    'type':'text', 'msg':line['content']
                })
                cnt+=1
            else:
                chat[-1]['msg']=line['content']
        if cnt!=1:
            print(line)
        # general settings:
        # reactions
        if 'reactions' in line:
            chat[-1]['reactions']=line['reactions']
        chat[-1]['time']=get_time(line['timestamp_ms'])
        chat[-1]['user']=user_map(str(line['sender_name']))
        chat[-1]['app']='MSG'
    # chat.sort(key=lambda x:x['time'])
    return chat

def union(a,b,OUT=None):
    if type(a)==str:
        with open(a,'r',encoding='utf-8') as f:
            a=json.load(f)
    if type(b)==str:
        with open(b,'r',encoding='utf-8') as f:
            b=json.load(f)
    ret=[]
    ia,ib=0,0
    while ia<len(a) and ib<len(b):
        if a[ia]==b[ib]:
            ret.append(a[ia])
            ia,ib=ia+1,ib+1
        elif a[ia]['time']<b[ib]['time']:
            ret.append(a[ia])
            ia+=1
        elif b[ib]['time']<a[ia]['time']:
            ret.append(b[ib])
            ib+=1
        else:
            j=ia
            while j<len(a) and a[j]['time']==b[ib]['time']:
                if a[j]==b[ib]:
                    break
                j+=1
            if j<len(a) and a[j]==b[ib]:
                ret.append(a[ia])
                ia+=1
            else:
                ret.append(b[ib])
                ib+=1
    ret=ret+a[ia:]+b[ib:]

    if OUT!=None:
        with open(OUT,'w+',encoding='utf-8') as f:
            f.write(json.dumps(ret,ensure_ascii=False,indent=2))
    else:
        return ret

def dump(x,fn=None):
    if fn is None:
        return json.dumps(x,ensure_ascii=False,indent=2)
    with open(fn,'w+',encoding='utf-8') as f:
        json.dump(x,f,ensure_ascii=False,indent=2)