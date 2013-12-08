import httplib2, re, time, datetime, steamdb, psycopg2,sys 
from bs4 import BeautifulSoup
def main(argv=None):
	if argv is None:
			argv = sys.argv

	app_id = argv[1]
	pat = re.compile('genre_release*\n(.+?)*\n</div>')
	http = httplib2.Http()
	headers, body = http.request("http://steamsales.rhekua.com/view.php?steam_type=app&steam_id=" + str(app_id))

	soup = BeautifulSoup(body)

	name = soup.find(attrs={"id":"leftcol_content_header"})
	name = re.search("^Sale history for (.*)",name.string)
	gamedict = ({"app_id":app_id, "name":name.group(1)})

	#steamdb.addGames(gamedict)
	dates = soup.find_all(attrs={"class": "genre_release"})
	prices = soup.find_all(attrs={"class":"tab_price"})
	saledict = []
	for i in range(len(dates)):
		rng =  re.findall("(\d{4}-\d{2}-\d{2})",dates[i].string)
		start =  time.mktime(datetime.datetime.strptime(rng[0], "%Y-%m-%d").timetuple()) #start
		end = time.mktime(datetime.datetime.strptime(rng[1], "%Y-%m-%d").timetuple()) #stop
		rng = re.findall("\$(\d*\.\d{2})", str(prices[i]))
		base = int(float(rng[0])*100)  #base
		sale = int(float(rng[1])*100)  #sale price
		saledict.append({"game_fk":app_id, "start":psycopg2.TimestampFromTicks(start), "end":psycopg2.TimestampFromTicks(end), "base_price":base, "sale_price":sale})

	steamdb.addSales(saledict)
	for i in steamdb.getSales(app_id):
		print(i["start_time"].day)

if __name__ == "__main__":
    main()