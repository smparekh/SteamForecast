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
    numCols = 366
    trainDates = np.zeros((numRows-1, numCols), dtype=np.int)
    testDates = np.zeros((1, numCols), dtype=np.int)
    saleDates = np.zeros((numRows, numCols), dtype=np.int)

    for line in infile.readlines():
        #print line
        line = line.strip()
        inDateYear = line.split(",")
        #print inDateYear[0]
        #print inDateYear[1]
        inDates.append(int(inDateYear[0]))
        inYears.append(int(inDateYear[1]))
        if (int(inDateYear[1]) == curYear):
            testDates[0, int(inDateYear[0])-1] = 1
        elif (int(inDateYear[1]) < curYear):
            trainDates[int(inDateYear[1])-1, int(inDateYear[0])-1] = 1

    curDay = int(datetime.datetime.now().timetuple().tm_yday)
    testDates[curYear-2, curDay:] = -1
    #print len(inDates)
    #print len(inYears)
    
    trainDates[rlsYear-1, 0:rlsDate] = -1
    k = int(kstr)

    results = np.zeros((1, 366), dtype=np.int)
    numSale = np.zeros((1, 366), dtype=np.int)
    nnumSale = np.zeros((1,366), dtype=np.int)
    #print saleDates
    for i in range(0,365):
        if (i-k < 0):
            saleRange = trainDates[:, 0:i+k+1]
            saleTest = testDates[:, 0:i+k+1]
        elif (i+k+1 <= 365):
            saleRange = trainDates[:,i-k:i+k+1]
            saleTest = testDates[:,i-k:i+k+1]
        else:
            saleRange = trainDates[:,i-k:]
            saleTest = testDates[:,i-k:]
    
        #print 'Current Day:', curDay
        #print trainDates, testDates
        
        yesSale = (saleRange==1).sum()
        noSale = (saleRange==0).sum()
        numSale[0,i] = yesSale
        nnumSale[0,i] = noSale
        #print 'Sale Days:', yesSale, '| Non sale days:', noSale
        if (yesSale > noSale):
            results[0,i] = 1
        else:
            results[0,i] = 0
        #print 'Results:', results[0, curDay], testDates[0, curDay]
        
    #print results, testDates
    # print numSale
    # print nnumSale
    # print trainDates
    # print results
    
    infile.close()

def genFile(app_id):
    f = open(str(app_id)+".txt", "w")

    game = steamdb.getGame(app_id)
    release_date = game[0]["release_date"]
    print str(datetime.datetime.now().year - release_date.year +1)
    f.write(str(release_date.timetuple().tm_yday) + ",1," + str(datetime.datetime.now().year - release_date.year +1)+'\n')
    for i in steamdb.getSales(app_id):
        startTime = i["start_time"];
        delta = i["end_time"] - startTime
        for j in range(0,delta.days+1):
            curTime =  startTime + datetime.timedelta(days=j)
            f.write(str(curTime.timetuple().tm_yday) + "," + str((curTime.year - release_date.year)+1)+'\n')
    f.close();
if __name__ == "__main__": 
    main(sys.argv[1:])
