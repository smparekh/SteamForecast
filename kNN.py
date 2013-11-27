#!/usr/bin/python
import sys, getopt, string
import numpy as np
from datetime import datetime

def main(argv):
    inputfile = ''
    kstr = ''
    try:
        opts, args = getopt.getopt(argv, 'hi:k:')
    except getopt.GetoptError:
        print 'Usage: kNN.py -i <inputfile> -k <k for knn>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: kNN.py -i <inputfile> -k <k for knn>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-k"):
            kstr = arg
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
        saleDates[int(inDateYear[1])-1][int(inDateYear[0])-1] = 1
    curDay = datetime.now().timetuple().tm_yday
    saleDates[int(inDateYear[1])-1][int(curDay):] = -1
    #print len(inDates)
    #print len(inYears)
    
    saleDates[rlsYear-1][0:rlsDate] = -1
    k = int(kstr)
    #print saleDates
    saleRange = saleDates[:,curDay-k:curDay+k];
    print 'Current Day: ',curDay;
    print saleRange
    print (saleRange==1).sum(), (saleRange==0).sum()
    infile.close()

if __name__ == "__main__": 
    main(sys.argv[1:])

