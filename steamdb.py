import psycopg2


def initDB():
	try:
		conn = psycopg2.connect("dbname='steamforecast' user='travis' host='192.241.188.75' password='derp'")
		conn.autocommit = True
		return conn
	except:
		print "I am unable to connect to the database"
		return

def closeDB(conn):
	conn.close()

def addGames(gamedict):
	conn = initDB()
	cur = conn.cursor()
	if(len(gamedict) == 2):
		cur.execute("""INSERT INTO games(app_id,name) VALUES (%(app_id)s, %(name)s)""", gamedict)
	else:
		cur.executemany("""INSERT INTO games(app_id,name) VALUES (%(app_id)s, %(name)s)""", gamedict)
	closeDB(conn)

def addSales(saledict):
	removeSales(saledict[0]["game_fk"])
	conn = initDB()
	cur = conn.cursor()
	cur.executemany("""INSERT INTO sales(start_time,end_time,base_price,sale_price,game_fk) VALUES(%(start)s, %(end)s, %(base_price)s, %(sale_price)s, %(game_fk)s)""",saledict)
	closeDB(conn)

def getSales(app_id):
	conn = initDB()
	cur = conn.cursor()
	cur.execute("""SELECT * FROM sales WHERE game_fk = %s""",[app_id])
	sales = cur.fetchall()
	closeDB(conn)
	return sales

def removeSales(app_id):
	conn = initDB()
	cur =conn.cursor()
	cur.execute("""DELETE FROM sales WHERE game_fk = %s""", [app_id])
	closeDB(conn)
