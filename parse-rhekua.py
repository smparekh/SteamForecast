import httplib2, re, time, datetime
from bs4 import BeautifulSoup

pat = re.compile('genre_release*\n(.+?)*\n</div>')
http = httplib2.Http()
headers, body = http.request("http://steamsales.rhekua.com/view.php?steam_type=app&steam_id=8190")

soup = BeautifulSoup(body)

name = soup.find(attrs={"id":"leftcol_content_header"})
name = re.search("^Sale history for (.*)",name.string)
print name.group(1)

dates = soup.find_all(attrs={"class": "genre_release"})
prices = soup.find_all(attrs={"class":"tab_price"})
for i in range(len(dates)):
	rng =  re.findall("(\d{4}-\d{2}-\d{2})",dates[i].string)
	print time.mktime(datetime.datetime.strptime(rng[0], "%Y-%m-%d").timetuple()) #start
	print time.mktime(datetime.datetime.strptime(rng[1], "%Y-%m-%d").timetuple()) #stop

	rng = re.findall("\$(\d*\.\d{2})", str(prices[i]))
	print rng[0]  #base
	print rng[1]  #sale price