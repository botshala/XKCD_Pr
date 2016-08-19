import sys
import json
import requests
def fetch(domain):
	grid={}
	re=''
	try:
		re=requests.get("https://xkcd.com/info.0.json")
	except:
		print("Failed")
		return 
	obj=json.loads(re.text)
	total_comics=obj["num"]
	while total_comics >0:
		print(total_comics)
		try:
			re=requests.get(("http://xkcd.com/%d/info.0.json")%total_comics)
		except:
			print("Probably Network connection Error ")
			continue
		try:
			obj=json.loads(re.text)
		except:
			total_comics=total_comics-1
			continue
		title=obj["title"]
		img_url=obj["img"]
		print(title+" : "+img_url)
		grid[title]=img_url
		grid[total_comics]=img_url
		total_comics=total_comics-1;
		#print(grid)
	text=json.dumps(grid)
	f=open(domain+"/xkcd.txt",'w')
	f.write(text)
	f.close()




if __name__=="__main__":
	if len(sys.argv)<2:
		print("Tell me the domain name plzzz")
	else:
		fetch(sys.argv[1])