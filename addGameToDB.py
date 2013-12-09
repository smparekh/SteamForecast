import datetime, steamdb, parse_rhekua, sys, getopt, time


def main(argv):
    app_id = 0
    release_year = 0
    release_day = 0
    try:
        opts, args = getopt.getopt(argv, 'a:y:d:')
    except getopt.GetoptError:
        print '-a app_id -y release_year -d release_day'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-a", "--app_id"):
            app_id = arg
        elif opt in ("-y", "--release_year"):
            release_year = arg
        elif opt in ("-d", "--release_day"):
            release_day = arg

    if(not(app_id and release_year and release_day)):
        print 'invalid input'
        sys.exit(2)

    steamdb.removeGame(app_id)
    parse_rhekua.main(app_id)
    release_date = datetime.datetime(int(release_year),1,1) + datetime.timedelta(days=int(release_day))
    datebase_date = datetime.date(2010,06,28)
    if release_date < datebase_date:
        release_date = datebase_date
    steamdb.addReleaseDate(app_id,time.mktime(release_date.timetuple()))

if __name__ == "__main__": 
    main(sys.argv[1:])
