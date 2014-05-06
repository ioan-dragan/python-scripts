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
    if counter > 6:
        counter = counter - 5;
    done = 0
    print str(counter)+"  <= Counter"
    for i,index in zip(fileLines, range(len(fileLines))): 
        if i.startswith("STRATEGY_NO"):
            # write down statistics
            if done != 0:
                idx = existsProblem(prbName)
                if timeStat == "":
                    timeStat= "600.0"
                if termReason == "":
                    termReason = "ERROR"
                    termReason = getUpTermination(fileLines, i)
                    # try to recover so that we get better statistics 
                    # go from the current index upwords in the file until we reach the STRATEGY_NO
                    # if we have not that much than we can safely assume ERROR termReason = getUpTermination(fileLines, i)

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
                #if not(idx==-1):
                #    _problemList[idx].addNewStatistics(termReason, timeStat,strateg)
                #else:
                #    if counter == 1:
                #        _problemList.append(Problem(prbName,termReason,timeStat,strateg))
                #    else:
                #        #print "ERROR"
                #        _problemList.append(Problem(prbName, "NOT_FOUND","360","none"))
                #        newIdx = existsProblem(prbName)
                #        for t in range(1,counter-1):
                #            _problemList[newIdx].addNewStatistics("NOT_FOUND", "360","none")
                #            
                #        _problemList[newIdx].addNewStatistics(termReason, timeStat,strateg)
                #    
                termReason = ""
                timeStat = ""
                strateg = ""
                prbName = ""
            # it means we have a new problem
            # now get the name of the problem
            splittedLine = i.split(" ")
            #print splittedLine 
            
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
                
        if cascModeOn == False:
            if i.startswith("Termination reason: "):
                term = i.split(":")
                termReason = term[1].strip("\n")
                done = done + 1
            if i.startswith("Time elapsed: "):
                timeS = i.split(":")
                timeStat = timeS[1]
                done = done + 1
                #idx = existsProblem(prbName);
                #
                #if not(idx==-1):
                #    _problemList[idx].addNewStatistics(termReason, timeStat,strateg)
                #else:
                #    _problemList.append(Problem(prbName,termReason,timeStat,strateg))
                #    
        else:  
  
            if i.startswith("% SZS status"):
                stat = i.split(" ")
                termReason = stat[3]
    
            if i.startswith("% Proof not found"):
                time = i.split(" ")
                timeStat = time[6].strip("%")
                #idx = existsProblem(prbName);
            done = done + 1 
                #if not(idx==-1):
                #    _problemList[idx].addNewStatistics(termReason, timeStat,strateg)
                #else:
                #    _problemList.append(Problem(prbName,termReason,timeStat,strateg))
                ##print timeStat
            
            if i.startswith("% Success in time"):
                time = i.split(" ")
                timeStat = time[4].strip("%")
                done = done + 1
                #print timeStat
                #idx = existsProblem(prbName)
                #if not(idx==-1):
                #    _problemList[idx].addNewStatistics(termReason, timeStat,strateg)
                #else:
                #    _problemList.append(Problem(prbName,termReason,timeStat,strategy))
            #if done == 2 :
            #    
            #    idx = existsProblem(prbName);
            #    print prbName
            #    print timeStat
            #    
            #    
            #    if not(idx==-1):
            #        _problemList[idx].addNewStatistics(termReason, timeStat,strateg)
            #    else:
            #        _problemList.append(Problem(prbName,termReason,timeStat,strategy))
            #    done = 0

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
        if "CounterSatisfiable" in str(array[i]):
            fout.write(" & CounterSAT ")
        else: 
            fout.write( " & " + str(array[i]) )
    fout.write("\\\\ \n")
    fout.write("\hline \n")
    
    
def getTime(line):
    time = line.split(" ")
    if len(time)==1:
        return float(time[0].strip("%"))
    return float(time[1])

def printStat(FILE, howMany):
    
    fout = open("StatisticsCASC"+FILE+".tex","w")
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
            #print idx
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
    for i in range(0,5):
        splDir = directory.strip().split("/")
        dirName = splDir[len(splDir)-2].split(".")[0]
        filename = dirName+"_vampire_"+dirName+"."+str(i)+".out"
        if not path.exists(directory+filename):
            print " no such file" + filename
        else :
            print "generating statistics file "+ str(i)+ "out of 5"
            print filename + "  "+ str(i)
            scriptLoadFile(directory+filename, (i)+1)
    if flag == True:
        printStat(dirName+"_CASC", 6)
    '''
    dirname+"_vampire_"+dirname+"0-9.out"
    '''
def generateGeneralStat(directory, files):
    if not path.exists(directory):
        print "Dir not found"
        sys.exit(1)
    
    dirName = directory.split("/")[1]
    
    count = 1
    
    for f in files:
        if not path.exists(directory+"/"+f):
            print "File not existent"
            sys.exit(1)
        else:
            if "0" in f or "1" in f or "2" in f or "3" in f or "4" in f:
                print f+"  counter "+str(count)
                scriptLoadFile(directory+"/"+f, count)
                count = count + 1
    
                   
            #if str(i) in f:
            #    scriptLoadFile(directory+"/"+f)
            #
    
def printThisProblem(prb):
    if "Timeout" in prb.terminationReason[0]: 
        for idx in range(1,len(prb.terminationReason)):
            if not('' == prb.terminationReason[idx]) and not("GaveUp" in prb.terminationReason[idx]) and not("Timeout" in prb.terminationReason[idx]) and not("ERROR" in prb.terminationReason[idx]) and not("NOT_FOUND" in prb.terminationReason[idx]): 
                print "Take care at this: "+prb.terminationReason[idx]
                return True
    return False

def getRank(filename):
    
    prbRoot = "/home/ioan/Documents/TPTP-v6.0.0/Problems/"
    folderName = filename[:3]
    
    fin = open(prbRoot+folderName+"/"+filename,"r")
    line = fin.readline()
    
    while(not ("% Rating " in line)):
        if "% Status" in line:
            print line
        
        line = fin.readline()
    
    spl = line.split(":")
    rank = spl[1].split(",")[0].split(" ")[1]
    print rank
    fin.close()
    
    return rank 

def writeHeader(fout, length):
    fout.write("\documentclass{article}\n")
    fout.write("\usepackage{graphicx}\n")
    fout.write("\usepackage{longtable}\n")
    fout.write("%% This is an autogenerated file! \n")
    fout.write("\\begin{document}\n")
    fout.write("\\begin{table}[!ht] \n")
    fout.write("\\begin{tabular}{|l|")
    
    for i in range(0, length):
        fout.write(" c |")
    fout.write("}\n \hline \n")
    
    
def writeEnd(fout):
    fout.write("\\end{tabular}\n \\end{table} \n \\end{document}")
    
#def createDiffFile(filename):
#    fout = open(filename,"w")
#    
#    fout.write("\n")
#    
#    writeHeader(fout, len(_problemList[0].terminationReason)+1)
#    for i in _problemList:
#        if printThisProblem(i): 
#            print i.name
#            rank = getRank(i.name)
#            fout.write(i.name+" ")
#            print rank
#            fout.write("& "+rank+" ")
#            #print i.terminationReason
#            write(fout, i.terminationReason)
#    
#    writeEnd(fout)
#    fout.close()
#    
_countReasons = [0,0,0,0,0]


def updateStat(reasons):
    
    for i in range(0, len(reasons)):
        if not("Timeout" in reasons[i]) and not("NOT_FOUND" in reasons[i] ) and not("Refutation not found" in reasons[i]) and not("Memory limit" in reasons[i]):    
            _countReasons[i] = _countReasons[i] + 1   
  
def createDiffFile(filename):
    fout = open(filename,"w")
    
    fout.write("\n")
    writeHeader(fout, len(_problemList[0].terminationReason)+1)
    for i in _problemList:
        if printThisProblem(i): 
            print i.name
            fout.write(i.name+" ")
            rank = getRank(i.name)
            fout.write("& "+ rank +" ")
            #print i.terminationReason
            write(fout, i.terminationReason)
            updateStat(i.terminationReason)
    fout.write("\n Total & - ")
    
    for i in _countReasons:
        fout.write("& "+str(i)+" ")
        
    fout.write("\n \\\\ \hline \n")
    
    writeEnd(fout)
    fout.close()
    
    print _countReasons
    
    
    
def walkTroughDirs(root):
    for subdir, dirs, files in os.walk(root):
        if subdir.endswith(".RES"):
            print subdir
            generateTwoStat(subdir+"/", False)
            #generateGeneralStat(subdir, files)
    printStat("GeneralStatCasc",6) 
    createDiffFile("DiffFileCasc.tex")

if __name__ == '__main__':
    #load the files and create the list of problems with the according statistics
    #loadFiles(sys.argv)
    if int(sys.argv[2]) == 0 : 
        generateTwoStat(sys.argv[1], True)
    #generate statistics 
    #printStat("test", 11)
    #if(len(sys.argv)>1):
    #    sp = sys.argv[1].split("/")
    #    extra = sp[len(sp)-1].split("_")
    #    extraName = extra[0]
    #    printStat(extraName, len(sys.argv))
    else :
        walkTroughDirs(sys.argv[1])
