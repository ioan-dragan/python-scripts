#!/usr/bin/env python 

import sys, os, time
import re
from os import path

folderList = []

def createProblemLists( fileLines ):
    fout = open ("ProblemList.txt","w")
    for ln in fileLines:
        spl = ln.split(" ")
        
        if spl[0][0].isalpha():
            fout.write(spl[0]+" \n")
            folderName = spl[0][:3]
            if folderName not in folderList : 
                folderList.append(folderName)
    fout.close()
    
    nout = open ("DirsFile.txt","w")
    for i in folderList:
        nout.write( i + " \n")
        
def loadFiles( inputFiles ):

    #load files one by one and preprocess them 
    for i in range(1, len(inputFiles)):
        # for each file in the command line read it and do the preprocessing 
        if not path.exists(inputFiles[i]) : 
            print " There is no such file to open " 
            sys.exit(1)
        
        fileIn = open(inputFiles[i],"r")
        #read all the lines from the file 
        # this way could be really slow
        lines = fileIn.readlines()
        #create problems
        createProblemLists(lines)
        #print inputFiles[i]
        
    #add the statistics from each of the problesm in the corresponding problem
    


def generateStatistics() : 
    print "generated statistics" 

if __name__ == '__main__':
    #load the files and create the list of problems with the according statistics 
    loadFiles(sys.argv)