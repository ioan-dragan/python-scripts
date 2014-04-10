#!/usr/bin/env python 

import sys, os, time
import re
from os import path

folderList = []

def getProblems( arg ):
    fin = open ("ProblemList.txt","r")
    lines = fin.readlines()
    
    for ln in lines:
        if ln.startswith(arg):
            print ln.strip()+".p"
    fin.close()    

if __name__ == '__main__':
    #load the files and create the list of problems with the according statistics 
    getProblems(sys.argv[1])