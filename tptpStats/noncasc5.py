#!/usr/bin/env python 

# {Script used in order to generate .tex statistics from different results
# obtained from running Vampire in different modes. }
# Copyright (C) {2014} {Ioan Dragan}

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

class Problem: 
    name = None 
    terminationReason = None
    timeStatistics = None
    strategy = None
    
    
    def __init__ (self, name, terminationReason, timeStatistics, strategy):
        self.name = name
        self.terminationReason = []
        self.terminationReason.append(terminationReason) 
        self.timeStatistics=[]
        self.timeStatistics.append(timeStatistics)
        self.strategy = []
        self.strategy.append(strategy)
    
    def addNewStatistics(self, terminationReason, timeStatistics, strategy): 
        self.terminationReason.append(terminationReason)
        self.timeStatistics.append(timeStatistics)
        self.strategy.append(strategy)
        #print terminationReason+" "+timeStatistics 
    #more functionality can be added here for the Problem class 

_problemList = list()

def existsProblem(name):
    for i in range(0, len(_problemList)):
        if(name == _problemList[i].name):
            return i

    return -1
from os import path
def getUpTermination(fileList, index):
    #print "getUpTermination"
    return "ERROR"
# % SZS status
# % Proof not found in
# % Success in time 

def getProblemStat(fileLines, idx):
    timeStat = ""
    termReason = ""
    i = idx + 1
    
    while i < len(fileLines) and not( fileLines[i].startswith("STRATEGY_NO")) :
        #print splittedLine 
        line = fileLines[i]
        if line.startswith("Termination reason: "):
            term = line.split(":")
            termReason = term[1].strip("\n")
            
        if line.startswith("Time elapsed: "):
            timeS = line.split(":")
            timeStat = timeS[1]
            
        i = i + 1
    return (timeStat.strip(), termReason)

def createProblemStatistics(fileLines, counter):
    prbName = ""
    termReason = ""
    timeStat = ""
    strateg = ""
    cascModeOn = True
    for i in fileLines:
        if i.startswith("STRATEGY_NO"):
            strategy = i.split("ARGS=")
            strateg = strategy[1].strip()
            if "--mode casc" in strateg:
                print "CASC MODE FOUND"
            else :
                cascModeOn = False
                print "NONCASC"
                
        break
    if counter >= 6:
        counter = counter - 5;
    done = 0
    print str(counter)+"  <= Counter"
    for i,index in zip(fileLines, range(len(fileLines))): 
        termReason = ""
        timeStat = ""
        prbName = ""
            
        if i.startswith("STRATEGY_NO"):
            # write down statistics
            
            if ( (len(fileLines)-index) > 2): 
                (timeStat,termReason) = getProblemStat(fileLines, index)
 
            term = timeStat.split(" ")
            if len(term) < 2:
                termReason = "NOT_FOUND"
                timeStat = "360"
            else:
                timeStat = term[0]
    #        # it means we have a new problem
    #        # now get the name of the problem
            splittedLine = i.split(" ")
    #        #print splittedLine 
    #        
            prbName = splittedLine[3].strip()
            prbName = prbName.strip("%")
            if prbName == "" :
                print "failed at line : "+str(index)
                #print "failed Line from file:  "+ fileLines[index]
                for j in range(index, len(fileLines)):
                    if " on " in fileLines[j] and not (fileLines[j].startswith("STRATEGY_NO")):
                        spl = fileLines[j].split(" on ")
                        prbName = spl[1].strip("\n")+".p"
                        print prbName
                        break
                sys.exit(1)
            print "add stat: ",prbName, termReason, timeStat
            
            idx = existsProblem(prbName)
            if not(idx==-1) :
                while(len(_problemList[idx].terminationReason) < counter-1):
                    _problemList[idx].addNewStatistics("NOT_FOUND", "360","none")
                    
                _problemList[idx].addNewStatistics(termReason, timeStat,strateg)
            else:
                if counter > 1:
                    print "ERROR"
                    _problemList.append(Problem(prbName, "NOT_FOUND","360",str(counter)))
                    newIdx = existsProblem(prbName)
                    while(len(_problemList[newIdx].terminationReason) < counter-1):
                        _problemList[newIdx].addNewStatistics("NOT_FOUND", "360","none")
                    _problemList[newIdx].addNewStatistics(termReason,timeStat, strateg)
                else :    
                    _problemList.append(Problem(prbName,termReason,timeStat,strateg))
                
    #    if cascModeOn == False:
    #        if i.startswith("Termination reason: "):
    #            term = i.split(":")
    #            termReason = term[1].strip("\n")
    #            done = done + 1
    #        if i.startswith("Time elapsed: "):
    #            timeS = i.split(":")
    #            timeStat = timeS[1]
    #            done = done + 1
    #
    #idx = existsProblem(prbName)
    #
    #if not(idx==-1):
    #    _problemList[idx].addNewStatistics(termReason, timeStat,strateg)
    #else:
    #    #_problemList.append(Problem(prbName,termReason,timeStat,strategy))
    #        if counter == 1:
    #            _problemList.append(Problem(prbName,termReason,timeStat,strateg))
    #        else:
    #            _problemList.append(Problem(prbName, "NOT_FOUND","360","none"))
    #            newIdx = existsProblem(prbName)
    #            for t in range(1,counter-1):
    #                _problemList[newIdx].addNewStatistics("NOT_FOUND", "360","none")
    #                            
    #            _problemList[newIdx].addNewStatistics(termReason, timeStat,strateg)
    #            
def write(fout, array):
    for i in range(0, len(array)):
        fout.write( " & " + str(array[i]) )
    fout.write("\\\\ \n")
    fout.write("\hline \n")
    
    
def getTime(line):
    time = line.split(" ")
    if len(time)==1:
        return float(time[0].strip("%"))
    return float(time[1])

def printStat(FILE, howMany):
    
    fout = open("Statistics"+FILE+".tex","w")
    # create the header of the latex file
    fout.write("\documentclass{article}\n")
    fout.write("\usepackage{graphicx}\n")
    fout.write("\usepackage{longtable}\n")
    fout.write("\\begin{document}\n")
    
    # create a table containing all the infor regarding satisfiability 
    fout.write("% this is an autogenerated statistics file\n")
    # creat the table header
    #fout.write("\\begin{table}[!ht] \n")
    #fout.write("\\begin{tabular}{|l|")
    
    if len(_problemList) ==0 :
        print "No problem information has been read"
        return
    #longable test
    fout.write("\\begin{longtable}[c]{|c|")
    
    for i in range(0,len(_problemList[0].strategy)):
        fout.write("c|")
    fout.write("}\n \hline \n")
    
    fout.write("\caption{Long table caption.\label{long}}\\\\ \n")
    fout.write("\endfirsthead \n")
    counter = 1 
    for prb in _problemList:
        #if counter%44 == 0 :
        #    fout.write("\end{tabular}\n")
        #    fout.write("\end{table}\n")
        #    
        #    fout.write("\\begin{table}[!ht]\n")
        #    fout.write("\\begin{tabular}{|l|")
        #    for i in range(0,len(_problemList[0].strategy)):
        #        fout.write("c|")
        #    fout.write("} \n \hline\n")
        #counter=counter+1
        fout.write(prb.name)
        #print prb.name
        #print prb.terminationReason
        for i in range(0, len(prb.terminationReason)):
            #print prb.terminationReason[i]
            if("Satisfiable" in prb.terminationReason[i]):
                fout.write("& S:"+prb.timeStatistics[i])
                
            elif ("Refutation not found" in prb.terminationReason[i]):
                fout.write("& RNF:"+prb.timeStatistics[i])
                
            elif ("Refutation" in prb.terminationReason[i] or "Theorem" in prb.terminationReason[i]):
                fout.write(" & R:"+prb.timeStatistics[i])
            elif (prb.terminationReason[i]=="GaveUp"):
                fout.write(" & G:"+prb.timeStatistics[i])
            elif prb.terminationReason[i]=="ERROR":
                fout.write(" & ERROR")
            elif prb.terminationReason[i]=="NOT_FOUND":
                fout.write(" & NF")
            else :
                fout.write(" & T:"+prb.timeStatistics[i])
                
        #for tReason in prb.terminationReason:
        #    fout.write(" & "+tReason )
        
        fout.write("\\\\ \n")

        #print prb.timeStatistics
        #fout.write(prb.timeStatistics[0]+ " \\\\ \n")
        #print prb.strategy[0]
        fout.write("\hline \n")
    # end the document
    fout.write("\end{longtable}\n")
    #fout.write("\end{tabular}\n")
    #fout.write("\end{table}\n")
    #
    # generate more statistics and write them down in the file
    
    fout.write("\\begin{table}[!ht] \n")
    fout.write("\\begin{tabular}{|l|")
    
    avgSatTime = []
    avgUnsatTime = []
    noSatProb = []
    noRefProb = []
    
    for i in range(0,howMany-1):
        avgSatTime.append(0)
        avgUnsatTime.append(0)
        noSatProb.append(0)
        noRefProb.append(0)
        
    # update statistics for this set of strategies
    print "PRINTING "
    #for prb in _problemList:
    #    print prb.name
    #    print prb.terminationReason
        
    for prb in _problemList:
        for idx in range(0,len(prb.terminationReason)):
        # for idx in range(0,howMany-1):
            #print prb.terminationReason
            if "Satisfiable" in prb.terminationReason[idx]:
                #print prb.name
                noSatProb[idx] = noSatProb[idx]+1
                avgSatTime[idx] = avgSatTime[idx] + getTime(prb.timeStatistics[idx])
                
            if prb.terminationReason[idx] == "Theorem" or ("Refutation" in prb.terminationReason[idx] and "not found" not in prb.terminationReason[idx])   :
                
                noRefProb[idx] = noRefProb[idx]+1
                avgUnsatTime[idx] = avgUnsatTime[idx] + getTime(prb.timeStatistics[idx])
                
    for i in range(0,len(_problemList[0].strategy)):
        fout.write("c|")
        
    fout.write("}\n \hline \n")
    
    for idx in range(0, len(avgSatTime)):
        if ( noSatProb[idx] != 0 or avgSatTime[idx] != 0 ):
            avgSatTime[idx] = float(avgSatTime[idx]/noSatProb[idx])
        if ( noRefProb[idx] != 0 or avgUnsatTime[idx] != 0 ):
            avgUnsatTime[idx] = float(avgUnsatTime[idx]/noRefProb[idx])
            
    fout.write("AvgSatTime ")
    write(fout, avgSatTime)
    
    fout.write("AvgUnsatTime ")
    write(fout, avgUnsatTime)
    
    fout.write(" noSatProb ")
    write(fout, noSatProb)
    
    fout.write(" noRefProb ")
    write(fout, noRefProb)
    
    # close the table containing general statistics    
    fout.write("\end{tabular}\n")
    fout.write("\end{table}\n")
    
    
    fout.write("\end{document}")
    
    fout.close()
    
    fout = open (FILE+"GENERAL.tex","w")
    fout.write("\documentclass{article}\n")
    fout.write("\usepackage{graphicx}\n")
    fout.write("\\begin{document}\n")
    
    # create a table containing all the infor regarding satisfiability 
    fout.write("% this is an autogenerated statistics file\n")
     # generate more statistics and write them down in the file
    
    fout.write("\\begin{table}[!ht] \n")
    fout.write("\\begin{tabular}{|l|")

        
    for i in range(0,len(_problemList[0].strategy)):
        fout.write("c|")
        
    fout.write("}\n \hline \n")
    
    fout.write("strateg &")
    write(fout, _problemList[0].strategy)
    fout.write("AvgSatTime ")
    write(fout, avgSatTime)
    
    fout.write("AvgUnsTime ")
    write(fout, avgUnsatTime)
    
    fout.write(" noSatProb ")
    write(fout, noSatProb)
    
    fout.write(" noRefProb ")
    write(fout, noRefProb)
    
    
     # close the table containing general statistics    
    fout.write("\end{tabular}\n")
    fout.write("\end{table}\n")
    
    fout.write("Total number of problems: "+str(len(_problemList))+"\n")
    fout.write("\end{document}")
    fout.close

def fillErrorPlaces(counter):
    for i in range(0, len(_problemList)):
        #print _problemList[i].timeStatistics
        print counter
        if len(_problemList[i].timeStatistics) < counter:
            #print _problemList[i].timeStatistics
            #print "update stats" + str(counter)
            print _problemList[i].name
            _problemList[i].addNewStatistics("NOT_FOUND", "240.0","strat"+str(counter))
            #print _problemList[i].timeStatistics
            
def loadFiles( inputFiles ):
    counter = 1
    #load files one by one and preprocess them 
    for i in range(1, len(inputFiles)):
        print i
        # for each file in the command line read it and do the preprocessing 
        if not path.exists(inputFiles[i]) : 
            print " There is no such file to open " 
            sys.exit(1)
        
        fileIn = open(inputFiles[i],"r")
        #read all the lines from the file 
        # this way could be really slow
        lines = fileIn.readlines()
        #create problems
        createProblemStatistics(lines)
        fillErrorPlaces(counter)
        counter = counter + 1
        if counter == 5:
            counter = 1
        #print inputFiles[i]
        
    #add the statistics from each of the problesm in the corresponding problem

def scriptLoadFile(filename, counter):
    if not path.exists(filename) : 
        print " There is no such file to open " 
        sys.exit(1)
        
    fileIn = open(filename,"r")
    #read all the lines from the file 
    # this way could be really slow
    lines = None
    lines = fileIn.readlines()
    #create problems
    createProblemStatistics(lines,counter)
    #fillErrorPlaces(counter)
    
def generateTwoStat(directory, flag):
    
    if not path.exists(directory):
        print "Directory not exsistent"
        sys.exit(1)
    dirName = ""
    for i in range(5,10):
        splDir = directory.strip().split("/")
        dirName = splDir[len(splDir)-2].split(".")[0]
        filename = dirName+"_vampire_"+dirName+"."+str(i)+".out"
        if not path.exists(directory+filename):
            print " no such file" + filename
            sys.exit()
        else :
            print "generating statistics file "+ str(i)+ "out of 5"
            print filename + "  "+ str(i-4)
            scriptLoadFile(directory+filename, (i)+1)
    if flag == True:
        printStat(dirName+"_CASC", 6)


    
def walkTroughDirs(root):
    for subdir, dirs, files in os.walk(root):
        if subdir.endswith(".RES"):
            print subdir
            generateTwoStat(subdir+"/", False)
    printStat("GeneralStatNonCasc",6) 

if __name__ == '__main__':
    #load the files and create the list of problems with the according statistics
    #loadFiles(sys.argv)
    if int(sys.argv[2]) == 0 : 
        generateTwoStat(sys.argv[1], True)

    else :
        walkTroughDirs(sys.argv[1])
