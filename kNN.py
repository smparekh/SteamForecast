#!/usr/bin/python
import sys, getopt, string, steamdb
import numpy as np
import datetime

def main(argv):
    inputfile = ''
    kstr = ''
    try:
        opts, args = getopt.getopt(argv, 'hi:k:g:')
    except getopt.GetoptError:
        print 'Usage: kNN.py -i <inputfile> -k <k for knn> --gen <app_id for file>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: kNN.py -i <inputfile> -k <k for knn> --gen <app_id for file>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-k"):
            kstr = arg
        elif opt in ("-g", "--genfile"):
            inputfile = genFile(arg)
            sys.exit()
    try:
        infile = open(inputfile, 'r')
    except IOError:
        print 'File not found, check name and existence.'
        sys.exit(2)
    print 'Parsing file: ', inputfile

    rlsLine = infile.readline()
    rlsLine = rlsLine.strip()
    rlsLine = rlsLine.split(",")
    rlsDate = int(rlsLine[0])
    rlsYear = int(rlsLine[1])
    curYear = int(rlsLine[2])
    #print rlsDate, ", ", rlsYear, ", ", curYear

    inDates = []
    inYears = []
    numRows = curYear #2 #max(inYears)
    numCols = 365
    saleDates = np.zeros((numRows, numCols), dtype=np.int)

    for line in infile.readlines():
        #print line
        line = line.strip()
        inDateYear = line.split(",")
        #print inDateYear[0]
        #print inDateYear[1]
        inDates.append(int(inDateYear[0]))
        inYears.append(int(inDateYear[1]))
        saleDates[int(inDateYear[1])-1, int(inDateYear[0])-1] = 1
    curDay = int(datetime.now().timetuple().tm_yday)
    saleDates[curYear-1, curDay:] = -1
    #print len(inDates)
    #print len(inYears)
    
    saleDates[rlsYear-1, 0:rlsDate] = -1
    k = int(kstr)
    
    #print saleDates
    if (curDay+k+1 <= 365):
        saleRange = saleDates[:,curDay-k:curDay+k+1]
    else:
        saleRange = saleDates[:,curDay-k:]
    print 'Current Day:', curDay
    print saleRange
    print 'Sale Days:', (saleRange==1).sum(), '| Non sale days:', (saleRange==0).sum()
    infile.close()

def genFile(app_id):
    f = open(str(app_id)+".txt", "w")

    for i in steamdb.getSales(app_id):
        startTime = i["start_time"];
        delta = i["end_time"] - startTime
        for j in range(0,delta.days+1):
            curTime =  startTime + datetime.timedelta(days=j)
            f.write(str(curTime.timetuple().tm_yday) + "," + str((curTime.year - startTime.year)+1)+'\n')
    f.close();
if __name__ == "__main__": 
    main(sys.argv[1:])
