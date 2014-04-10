'''
    {Script used in order to generate .tex statistics from different results
    obtained from running Vampire in different modes. }
    Copyright (C) {2014} {Ioan Dragan}

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

'''

#!/usr/bin/env python 

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

    #more functionality can be added here for the Problem class 

_problemList = []

def existsProblem(name):
    for i in range(0, len(_problemList)):
        if(name == _problemList[i].name):
            return i
    return -1
from os import path
# % SZS status
# % Proof not found in
# % Success in time 
def createProblemStatistics(fileLines):
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
    
    done = 0
    for i in fileLines: 
        if i.startswith("STRATEGY_NO"):
            # it means we have a new problem
            # now get the name of the problem
            splittedLine = i.split(" ")
            prbName = splittedLine[3]
            
            strategy = i.split("ARGS=")
            strateg = strategy[1].strip("\n")
            st = strateg.split(" ")
            strateg = st[1]
            done = 0
        if cascModeOn == False:
            if i.startswith("Termination reason: "):
                term = i.split(":")
                termReason = term[1].strip("\n")
            if i.startswith("Time elapsed: "):
                timeS = i.split(":")
                timeStat = timeS[1]
                idx = existsProblem(prbName);
            
                if not(idx==-1):
                    _problemList[idx].addNewStatistics(termReason, timeStat,strateg)
                else:
                    _problemList.append(Problem(prbName,termReason,timeStat,strateg))
                    
        else: 
  
            if i.startswith("% SZS status"):
                stat = i.split(" ")
                termReason = stat[3]
                done = done + 1        

            
            if i.startswith("% Proof not found"):
                time = i.split(" ")
                timeStat = time[6]
                done = done + 1
                #idx = existsProblem(prbName);
            
                #if not(idx==-1):
                #    _problemList[idx].addNewStatistics(termReason, timeStat,strateg)
                #else:
                #    _problemList.append(Problem(prbName,termReason,timeStat,strateg))
                ##print timeStat
            
            if i.startswith("% Success in time"):
                time = i.split(" ")
                timeStat = time[4]
                done = done + 1
                #print timeStat
                #idx = existsProblem(prbName)
                #if not(idx==-1):
                #    _problemList[idx].addNewStatistics(termReason, timeStat,strateg)
                #else:
                #    _problemList.append(Problem(prbName,termReason,timeStat,strategy))
            if done == 2 :
                
                idx = existsProblem(prbName);
                
                if not(idx==-1):
                    _problemList[idx].addNewStatistics(termReason, timeStat,strateg)
                else:
                    _problemList.append(Problem(prbName,termReason,timeStat,strategy))
                done = 0

def write(fout, array):
    for i in range(0, len(array)):
        fout.write( " & " + str(array[i]) )
    fout.write("\\\\ \n")
    fout.write("\hline \n")
    
    
def getTime(line):
    time = line.split(" ")
    if len(time)==1:
        return float(time[0])
    return float(time[1])

def printStat(FILE, howMany):
    
    fout = open("Statistics"+FILE+".tex","w")
    # create the header of the latex file
    fout.write("\documentclass{article}\n")
    fout.write("\usepackage{graphicx}\n")
    fout.write("\\begin{document}\n")
    
    # create a table containing all the infor regarding satisfiability 
    fout.write("% this is an autogenerated statistics file\n")
    # creat the table header
    fout.write("\\begin{table}[!ht] \n")
    fout.write("\\begin{tabular}{|l|")
    
    if len(_problemList) ==0 :
        print "No problem information has been read"
        return
    
    for i in range(0,len(_problemList[0].strategy)):
        fout.write("c|")
    fout.write("}\n \hline \n")
    
    counter = 1 
    for prb in _problemList:
        if counter%44 == 0 :
            fout.write("\end{tabular}\n")
            fout.write("\end{table}\n")
            
            fout.write("\\begin{table}[!ht]\n")
            fout.write("\\begin{tabular}{|l|")
            for i in range(0,len(_problemList[0].strategy)):
                fout.write("c|")
            fout.write("} \n \hline\n")
        counter=counter+1
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
                fout.write("& R:"+prb.timeStatistics[i])
            elif (prb.terminationReason[i]=="GaveUp"):
                fout.write("& G:"+prb.timeStatistics[i])
            else :
                fout.write("& T:"+prb.timeStatistics[i])
                
        #for tReason in prb.terminationReason:
        #    fout.write(" & "+tReason )
        
        fout.write("\\\\ \n")
        #print prb.timeStatistics
        #fout.write(prb.timeStatistics[0]+ " \\\\ \n")
        #print prb.strategy[0]
        fout.write("\hline \n")
    # end the document
    fout.write("\end{tabular}\n")
    fout.write("\end{table}\n")
    
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
    for prb in _problemList:
        for idx in range(0,len(prb.terminationReason)):
            
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
    
    fout.write(" noThmProb ")
    write(fout, noSatProb)
    
    fout.write(" noRefProb ")
    write(fout, noRefProb)
    
    # close the table containing general statistics    
    fout.write("\end{tabular}\n")
    fout.write("\end{table}\n")
    
    
    fout.write("\end{document}")
    
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
        createProblemStatistics(lines)

        #print inputFiles[i]
        
    #add the statistics from each of the problesm in the corresponding problem
    


def generateStatistics() : 
    print "generated statistics" 

if __name__ == '__main__':
    #load the files and create the list of problems with the according statistics 
    loadFiles(sys.argv)
    #generate statistics 
    generateStatistics()
    if(len(sys.argv)>1):
        sp = sys.argv[1].split("/")
        extra = sp[len(sp)-1].split("_")
        extraName = extra[0]
        printStat(extraName, len(sys.argv))
    
