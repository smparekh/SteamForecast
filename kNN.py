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

    # Read Release Day, Release Year and Current Year from file
    rlsLine = infile.readline()
    rlsLine = rlsLine.strip()
    rlsLine = rlsLine.split(",")
    rlsDate = int(rlsLine[0])
    rlsYear = int(rlsLine[1])
    curYear = int(rlsLine[2])
    #print rlsDate, ", ", rlsYear, ", ", curYear

    # Create empty matrices
    numRows = curYear #2 #max(inYears)
    numCols = 366
    

    trainDates = np.zeros((numRows-1, numCols), dtype=np.int)
    testDates = np.zeros((1, numCols), dtype=np.int)
    saleDates = np.zeros((numRows, numCols), dtype=np.int)

    # Read file
    for line in infile.readlines():
        #print line
        line = line.strip()
        inDateYear = line.split(",")
        #print inDateYear[0]
        #print inDateYear[1]
        
        # Use the current year for testing
        if (int(inDateYear[1]) == curYear):
            testDates[0, int(inDateYear[0])-1] = 1
        # Use past years for training
        elif (int(inDateYear[1]) < curYear):
            trainDates[int(inDateYear[1])-1, int(inDateYear[0])-1] = 1

    # Get current day and label anything past today as unknown -1
    curDay = int(datetime.datetime.now().timetuple().tm_yday)
    testDates[0, curDay:] = -1
    #print trainDates
    #print testDates
    #print len(inDates)
    #print len(inYears)
    
    # Label anything before release day as unknown -1
    trainDates[rlsYear-1, 0:rlsDate] = -1
    k = int(kstr)
    k_year = 999
    k_day = k

    # Create some more empty matrices
    predVector = np.zeros((1, 366), dtype=np.int)
    numSale = np.zeros((1, 366), dtype=np.int)
    nnumSale = np.zeros((1,366), dtype=np.int)
    #print saleDates
    # Go through training data and create a prediction vector
    for i in range(0,365):
        if (i-k_day < 0):
            saleRange = trainDates[0:k_year,0:i+k_day+1]
        elif (i+k_day+1 <= 365):
            saleRange = trainDates[0:k_year,i-k_day:i+k_day+1]
        else:
            saleRange = trainDates[0:k_year,i-k_day:]
    
        #print 'Current Day:', curDay
        #print trainDates, testDates
        
        yesSale = (saleRange==1).sum()
        noSale = (saleRange==0).sum()
        numSale[0,i] = yesSale
        nnumSale[0,i] = noSale
        #print 'Sale Days:', yesSale, '| Non sale days:', noSale
        # Predict a sale based on # of sale days surrounding that day in the past
        if (yesSale >= noSale):
            predVector[0,i] = 1
        else:
            predVector[0,i] = 0
        #print 'Results:', results[0, curDay], testDates[0, curDay]

    good = 0;
    falsepos = 0; #type 1 error
    miss = 0; #type 2 error
    trueneg = 0;

    #print predVector
    # See how the algorithm did, find number of correct, false positives and incorrect predictions
    for i in range(0,365):
        if (predVector[0,i] == 1 and testDates[0,i] == 1):
            good = good + 1
        elif ((predVector[0,i] == 0 and testDates[0,i] == 1)): 
            miss = miss + 1
        elif ((predVector[0,i] == 1 and testDates[0,i] == 0)):
            falsepos = falsepos + 1;
        elif (predVector[0,i] == 0 and testDates[0,i] == 0):
            trueneg = trueneg + 1;

    #print predVector, testDates
    # results = np.equal(predVector, testDates)
    # print (results==True).sum(), (results==False).sum()
    print "True Pos: %s True Neg: %s TypeI Err: %s TypeII Err: %s" % (good, trueneg,falsepos,miss)
    # print numSale
    # print nnumSale
    # print trainDates#, testDates
    # print results

    infile.close()

def genFile(app_id):
    f = open(str(app_id)+".txt", "w")

    game = steamdb.getGame(app_id)
    release_date = game[0]["release_date"]
    # print str(datetime.datetime.now().year - release_date.year +1)
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
