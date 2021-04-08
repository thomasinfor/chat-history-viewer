import json
import re

def combine():
	filename='./site/index.html'
	with open(filename,'r') as f:
		original=f.read()

	out=""
	i=0
	for match in re.finditer('<script src=".*"></script>',original):
		url=match.group()[13:-11]
		l,r=match.span()
		with open('./site/'+url,'r') as f:
			out+=f'{original[i:l]}<script type="text/javascript">\n{f.read()}\n</script>'
			i=r
	out+=original[i:]

	with open('./site/single.html','w+') as f:
		f.write(out)

if __name__=='__main__':
	combine()