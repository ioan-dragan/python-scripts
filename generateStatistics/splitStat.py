#!/usr/bin/env python 

import sys, os, time
import re 
from os import path
from operator import indexOf

def splitFile(fileLines):
    
    fout = None
    problemLines = []
    
    for i in fileLines:
        if i.startswith("STRATEGY"): 
            if not(fout is None):
                fout.writelines(problemLines)
                fout.close()
                problemLines = []
            interm= i.strip().split(" ")[3]
            print interm
            strategy = i.strip().split(" ")[1]
            problemName = "Ghost"
            if interm.endswith("%"):
                problemName = interm.strip("%")
            else:
                newInterm = interm.split("/")[1]
                problemName = newInterm
            
            fout = open(problemName+"."+strategy,"w")
            problemLines.append(i)
        else: 
            problemLines.append(i)
            

    fout.writelines(problemLines)
    fout.close()
    
def splitFolder(folder):
    listOfFiles = []
    for subdir, dirs, files in os.walk(folder):
        listOfFiles=files

    for i in listOfFiles: 
        fop = open(folder+i,"r")
        print "splitting : "+str(i)
        lines = fop.readlines()
        fop.close()
        splitFile(lines)
        
if __name__ == '__main__':
    folderName = sys.argv[1]
    
    splitFolder(folderName)
    
    
