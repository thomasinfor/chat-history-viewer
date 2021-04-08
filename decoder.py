import re

def decode(IN,OUT=None):
	def uni_to_utf(x):
		return f"\\x{x[4:6]}"

	out,buff=[],''
	with open(IN,'r',encoding='utf-8') as f:
		for data in f.readlines():
			data=data.strip('\n\ufeff')
			new=''
			i=0
			while i<len(data):
				if re.match('\\\\u00([\\da-f]{2})',data[i:]):
					buff+=uni_to_utf(data[i:i+6])
					i+=6
				else:
					new+=eval(f"b'{buff}'").decode()+data[i]
					buff=''
					i+=1
			out.append(new)
	ret='\n'.join(out)+'\n'
	if OUT!=None:
		with open(OUT,'w',encoding='utf-8') as f:
			f.write(ret)
	else:
		return ret
if __name__=='__main__':
	pass