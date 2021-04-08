import json
from datetime import datetime,timedelta
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

path='./result/all-new.json'
with open(path,'r',encoding='utf-8') as f:
	chat=json.load(f)

def get_date(x):
	return datetime.strptime(x['time'].split(' ')[0],'%Y-%m-%d')
def min(a,b):
	return np.min([a,b])
group=14
def filter(x):
	if group==1:
		return x
	for i in range(len(x)):
		if i%group==0:
			x[i]=np.average(x[i:min(i+group,len(x))])
		else:
			x[i]=x[i-1]
	return x

cnt_words=0
date=[get_date(chat[0])]
end=get_date(chat[-1])
lines=[0]
app={'LINE':set(),'MSG':set()}
i=0
while date[-1]<=end:
	while i<len(chat) and get_date(chat[i])==date[-1]:
		app[chat[i]['app']].add(get_date(chat[i]))
		if 'msg' in chat[i]:
			cnt_words+=len(chat[i]['msg'])
		lines[-1]+=1
		i+=1
	if date[-1]!=end:
		date.append(date[-1]+timedelta(days=1))
		lines.append(0)
	else:
		break

print('total messages:',len(chat))
print('total words:',cnt_words)
print(f"from: {chat[0]['time']} to {chat[-1]['time']}")

fig,ax=plt.subplots(figsize=(10,6))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax.xaxis.set_minor_locator(mdates.MonthLocator())
ax.plot_date(date[0::group],filter(lines)[0::group],'-',xdate=True,linewidth=1)
ax.scatter([i for i in app['LINE']],[-5 for _ in range(len(app['LINE']))],c='g',s=1)
ax.scatter([i for i in app['MSG']],[-8 for _ in range(len(app['MSG']))],c='b',s=1)
ax.grid(True,'both')
plt.savefig('images/plot2.png')