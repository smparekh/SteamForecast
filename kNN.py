#!/usr/bin/python
import sys, getopt, string, steamdb
import numpy as np
import datetime

def main(argv):
    np.set_printoptions(threshold='nan')
    inputfile = ''
    kstr = ''
    wstr = '0'
    ystr = '-1'
    try:
        opts, args = getopt.getopt(argv, 'hi:k:g:w:y:')
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
        elif opt in ("-w"):
            wstr = arg
        elif opt in ("-g", "--genfile"):
            inputfile = genFile(arg)
            sys.exit()
        elif opt in ("-y"):
            ystr = arg
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
       
	saleDates[int(inDateYear[1])-1, int(inDateYear[0])-1] = 1 
        # Use the current year for testing
        if (int(inDateYear[1]) == curYear):
            testDates[0, int(inDateYear[0])-1] = 1
        # Use past years for training
        elif (int(inDateYear[1]) < curYear):
            trainDates[int(inDateYear[1])-1, int(inDateYear[0])-1] = 1

    # Get current day and label anything past today as unknown -1
    curDay = int(datetime.datetime.now().timetuple().tm_yday)
    testDates[0, curDay:] = -1
    saleDates[0, :rlsDate] = -1
    saleDates[curYear-1, curDay:] = -1
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
    
    weight = genWeightVector(curYear-1, float(wstr))
    numyear = int(ystr)
    if(numyear< 0):
        numyear = curYear - 1
    useYear = genUseYearVector(curYear-1, numyear)
    for i in range(0,366):
        if (i-k_day < 0):
            trainSaleRange = trainDates[0:k_year,0:i+k_day+1]
            testSaleRange = testDates[0,:i]
        elif (i+k_day+1 <= 365):
            trainSaleRange = trainDates[0:k_year,i-k_day:i+k_day+1]
            testSaleRange = testDates[0,i-k_day:i]
        else:
            trainSaleRange = trainDates[0:k_year,i-k_day:]
            testSaleRange = testDates[0,i-k_day:i]
    
        #print 'Current Day:', curDay
        #print trainDates, testDates
        # print testSaleRange, i
        yes = np.zeros((numRows, 1), dtype=np.double)
        no = np.zeros((numRows, 1), dtype=np.double)
        for j in range(0,trainSaleRange.shape[0]):
            # print j, trainSaleRange.shape[0]
            yes[j] = (trainSaleRange[j,:]==1).sum() * weight[j] * useYear[j]
            no[j] = (trainSaleRange[j,:]==0).sum() * weight[j] * useYear[j]
        yes[j+1] = (testSaleRange==1).sum()
        no[j+1] = (testSaleRange==0).sum()
        yesSale = yes.sum()
        noSale = no.sum()
        numSale[0,i] = yesSale
        nnumSale[0,i] = noSale
        # print yes.sum(), yesSale, no.sum(), noSale
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
    for i in range(0,366):
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
    y = numyear +1 
    calculatek = 2*k*y+y-k-1
    print "calculated k: %s" %(calculatek)
    # print numSale
    # print nnumSale
    # print trainDates#, testDates
    # print result
    f1 = open('results.txt', 'w+')

    row_labels = ['0', '1', '2', '3']
    print >> f1, '    '
    for i in range(0,366):
    	print >> f1, '%04s' % (i),
    print >> f1
    for row_label, row in zip(row_labels, saleDates):
	print >> f1, '%s [%s]' % (row_label, ' '.join('%04s' % i for i in row))
    for preds in predVector:
        print >> f1 ,'  [%s]' % (' '.join('%04s' % i for i in preds))
    infile.close()
    f1.close()

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

def genWeightVector(lastyear, wconstant):
    #print lastyear
    weight = np.zeros((lastyear,1),dtype=np.double)
    for i in range(0, lastyear):
        weight[i] = 1 + ((i - lastyear+1) * wconstant)
        if(weight[i] < 0):
            weight[i] = 0
    return weight

def genUseYearVector(lastyear, nyears):
    years = np.zeros((lastyear,1),dtype=np.int)
    for i in range(0,lastyear):
        if(i > lastyear - nyears -1):
            years[i] = 1
    return years

if __name__ == "__main__": 
    main(sys.argv[1:])
