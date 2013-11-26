import httplib2, re
from bs4 import BeautifulSoup

pat = re.compile('genre_release*\n(.+?)*\n</div>')
http = httplib2.Http()
headers, body = http.request("http://steamsales.rhekua.com/view.php?steam_type=app&steam_id=8190")

soup = BeautifulSoup(body)
dates = soup.find_all(attrs={"class": "genre_release"})
for i in dates:
	print re.findall("(\d{4}-\d{2}-\d{2})",i.string)
