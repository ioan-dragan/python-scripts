#!/usr/bin/env python 

# Copyright (C) 2014  Ioan Dragan

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

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
