#!/usr/bin/env python 

import sys, os, time
import re 
from os import path

class Problem: 
    name = None 
    terminationReason = None
    time = None
    satClauses = None
    satVariables = None
    satCalls = None 
    satTime = None 
    strategy = None 
    fileName = None
    
    vSplitClauses = None
    vSplitRefutations = None
    vSplitComponents = None
    
    def __init__(self , name, filename):
        self.name = name
        self.terminationReason = list() 
        self.time = list() 
        self.satClauses = list()
        self.satVariables = list() 
        self.satCalls = list() 
        self.satTime = list()
        self.strategy = list()
        self.fileName = filename
        self.vSplitClauses = list()
        self.vSplitComponents = list()
        self.vSplitRefutations = list()
        
    def addTerminationReason(self, termination):
        self.terminationReason.append(termination)
    def addTotalTime(self, time):
        self.time.append(time)
    def addSatClauses(self, satClauses): 
        self.satClauses.append(satClauses)
    def addSatVariables(self, variables): 
        self.satVariables.append(variables)
    def addSatCalls(self, satCalls): 
        self.satCalls.append(satCalls)
    def addSatTime(self, satTime):
        self.satTime.append(satTime)
    def addStrategy(self, strategy): 
        self.strategy.append(strategy)
    
    def addVSplitClauses(self, vs):
        self.vSplitClauses.append(vs)
    def addVSplitRefutations(self, vsr):
        self.vSplitRefutations.append(vsr)
    def addVSplitComponents(self, vsc):
        self.vSplitComponents.append(vsc)
    
_listOfProblems = []

_timeRef = [0,0,0,0,0]
_totalRef = [0,0,0,0,0]
_differenceCounter = [0,0,0,0,0]
total = 0

def collectSingleProblemStatistics(fileLines, problemIndex):
    '''
    get sat stats 
    get satus 
    get total time 
    '''
    time = "-1"
    satClauses = "0"
    satVariables = "0"
    satCalls = "0"
    satTimeSpent = "0"
    strategy = ""
    terminationReason = "PRB\\_NR"
    checkReason = ""
    
    vSplitClauses = "0"
    vSplitComponents = "0"
    vSplitRefutations = "0"
    
    for i in fileLines: 
        if i.startswith("STRATEGY"): 
            problemName = i.strip().split(" ")[3].split("/")[1]
            if not(problemName==_listOfProblems[problemIndex].name): 
                print "trying to add statistics to the wrong problem!"
                print problemName + " vs " + _listOfProblems[problemIndex].name
                exit(1)
        # collect total time elapsed for this strategy
        elif "Time elapsed" in i: 
            time = i.strip().split(":")[1].strip().split(" ")[0]
            #print time
        elif "SAT solver time" in i : 
            splittedBySemicolumn = i.strip().split(":")[1].strip()
            satTimeSpent = splittedBySemicolumn
        elif i.startswith("TWLsolver") or i.startswith("Lingeling"): 
            splittedBySemicolumn = i.strip().split(":")[1].strip()
            if "Lingeling solver time" in i: 
              satTimeSpent = splittedBySemicolumn.strip(" s")  
            elif "elapsed time" in i: 
                satTimeSpent = splittedBySemicolumn
            elif "clauses" in i: 
                satClauses = splittedBySemicolumn
            elif "variables" in i : 
                satVariables = splittedBySemicolumn
            elif "calls for" in i : 
                satCalls = splittedBySemicolumn
        elif "Termination reason" in i : 
            splittedBySemicolumn = i.strip().split(":")[1].strip()
            terminationReason = splittedBySemicolumn
        elif "Thanks to" in i : 
            checkReason = i
        elif i.startswith("Split"):
            splittedBySemicolumn = i.strip().split(":")[1].strip()
            if "clauses" in i:
                vSplitClauses = splittedBySemicolumn
            elif "components" in i:
                vSplitComponents = splittedBySemicolumn
        elif i.startswith("Sat splitting ref"):
            splittedBySemicolumn = i.strip().split(":")[1].strip()
            vSplitRefutations = splittedBySemicolumn            
        
    _listOfProblems[problemIndex].addSatCalls(satCalls)
    _listOfProblems[problemIndex].addSatVariables(satVariables)
    _listOfProblems[problemIndex].addSatClauses(satClauses)
    _listOfProblems[problemIndex].addSatTime(satTimeSpent)
    _listOfProblems[problemIndex].addTerminationReason(terminationReason)
    _listOfProblems[problemIndex].addTotalTime(time)
    _listOfProblems[problemIndex].addVSplitComponents(vSplitComponents)
    _listOfProblems[problemIndex].addVSplitClauses(vSplitClauses)
    _listOfProblems[problemIndex].addVSplitRefutations(vSplitRefutations)
'''
Collect statistics for the file_0 of each problem
We should collect from all the five files, so that we have statistics from all
strategies 
'''
def getProblemStatistics(directory, filename,problemIndex): 
    for i in range(0,5):
        lines = []
        fileToOpen=directory+filename[:len(filename)-1]+str(i)
        if not path.exists(fileToOpen):
            lines = []
        else:
            of = open(fileToOpen,"r")
            lines = of.readlines()
        print problemIndex
        collectSingleProblemStatistics(lines, problemIndex)
        _listOfProblems[problemIndex].addStrategy(str(i))


def insertNewProblem(dir, file): 
    fin = open(dir+file,"r")
    lines = fin.readlines()
    print file
    print dir
    for i in lines: 
        if i.startswith("STRATEGY"): 
            problemName = i.strip().split(" ")[3].split("/")[1]
            prb = Problem(problemName,dir+file[:len(file)-1])
            _listOfProblems.append(prb)
            return len(_listOfProblems)-1
'''
Create the statistics for current directory
'''
def generateStatisticsForDir(directory):
    listOfFiles = []
    numberOfFiles = 0
    if not path.exists(directory):
        print "Directory not exsistent"
        sys.exit(1)
    else :
        for subdir, dirs, files in os.walk(directory):
            listOfFiles = files
    
    numberOfFiles = len(listOfFiles)
    
    for i in listOfFiles:
        if(i.endswith("0")):
            problemIndex = insertNewProblem(directory,i)
            #print _listOfProblems[problemIndex].name
            getProblemStatistics(directory,i,problemIndex)
    
    dirName = ""

def writeTableHeader(fout,columns,flag=False):
    fout.write("\n\\begin{tabular}{")
    for i in range(columns):
        fout.write("|c")
    fout.write("|c|")
    fout.write("}\n\\hline\n")
    if flag==False:
        fout.write("& Vamp & L & L S & L I & L I S\\\\\n\\hline\n")
    
def writeTableEnd(fout):
    fout.write("\\end{tabular}\n\n")
    
def writeReason(fout, termR, time, strat, flag=False):
    global _totalRef
    global _timeRef
    if "Refutation" in termR and not("Refutation not found" in termR):
        fout.write("R:"+time)
        if flag==True:
            _timeRef[strat] = _timeRef[strat] + float(time)
            _totalRef[strat] = _totalRef[strat]+1
        return
    if "Refutation" in termR and "not found" in termR:
        fout.write("RNF ")
        return 
    if termR == "": 
        fout.write("ERROR")
        return
    if "Time limit" in termR : 
        fout.write("TO")
        return
    if "Unknown" in termR: 
        fout.write("UKN")
        return
    if "Memory limit" in termR: 
        fout.write("MEM")
        return
    fout.write(termR+time)
    return

'''     
write table with all the statistics from problems 
each table will be 40 lines
'''
def writeGeneralTable(fout, flag=True):
    
    writeTableHeader(fout, len(_listOfProblems[0].terminationReason))
    for i in range(len(_listOfProblems)): 
        if(i%40==0) and not(i==0):
            writeTableEnd(fout)
            writeTableHeader(fout,len(_listOfProblems[0].terminationReason))
        prb = _listOfProblems[i]
        
        fout.write(prb.name+" & ")
        l = len(prb.terminationReason)-1
        for j in range(l): 
            writeReason(fout,prb.terminationReason[j], prb.time[j], j,flag)
            fout.write("& ")
        writeReason(fout, prb.terminationReason[l], prb.time[l],l, flag)
        fout.write("\\\\\n\\hline\n")
    writeTableEnd(fout)
    
    #print also statistics count
    
    fout.write("\n\\begin{tabular}{|c|c|c|c|c|c|}\n\\hline\n")
    fout.write("Avg Time &")
    for i in range(4):
        fout.write(str(float(_timeRef[i]/_totalRef[i]))+" &")
    fout.write(str(float(_timeRef[4]/_totalRef[4]))+" \\\\\n\\hline\n")
    fout.write("Total Solved & ")
    for i in range(4):
        fout.write(str(float(_totalRef[i]))+" &")
    fout.write(str(float(_totalRef[4])))
    fout.write("\\\\\n\\hline\n\\end{tabular}\n")
    fout.write("%%Total number of problems: "+str(len(_listOfProblems)) )
    
def getLetter(number):
    if number == 0 : 
        return "Vamp"
    elif number == 1 : 
        return "L"
    elif number == 2 : 
        return "L S"
    elif number == 3 : 
        return "L I"
    else: 
        return "L I S" 

def isWinner(termReason):
    if "Refutation" in termReason and not("not found" in termReason): 
        return "Sol:"
    if "Satisfiable" in termReason or "CounterSatisfiable" in termReason or "Theorem" in termReason or "Unsatisfiable" in termReason:
        return "Sol:"
    return ""

def writeSatStatistics(listOfProblems,fout): 
    totalProblems= len(listOfProblems)
    writeTableHeader(fout,9, True)
    fout.write("name & Cls & Vars & Calls & SplR & SplCl & SplCo & SatTime & Time \\\\\n\\hline\n")

    for i in range(totalProblems): 
        if i%7 == 0 and not(i==0): 
            writeTableEnd(fout)
            writeTableHeader(fout,9, True)
            fout.write("name & Cls & Vars & Calls & SplR & SplCl & SplCo & SatTime & Time \\\\\n\\hline\n")
        prb = listOfProblems[i] 
        fout.write("\\hline\n"+prb.name+"&&&&&&&& \\\\\n\\hline\n")
        for j in range(5):
            fout.write(isWinner(prb.terminationReason[j]))
            fout.write(getLetter(j))
            fout.write(" & ")
            fout.write(prb.satClauses[j] +" &")
            fout.write(prb.satVariables[j] +" &")
            fout.write(prb.satCalls[j]+" & ")
            fout.write(prb.vSplitRefutations[j]+" & ")
            fout.write(prb.vSplitClauses[j] + " & ")
            fout.write(prb.vSplitComponents[j] + " & ")
            fout.write(prb.satTime[j]+" &")
            fout.write(prb.time[j]+"\\\\\n\\hline\n")
            
    fout.write("\\hline\n\\end{tabular}\n")

def keepIt(prb): 
    global _differenceCounter
    global total
    #check if can be solved only by us 
    t0 = prb.terminationReason[0]

    if "Time limit" in t0 or ("Refutation" in t0 and "not found" in t0) or "Memory limit" in t0:
        counter = 0
        for i in range(1,5):
            if "Refutation" in prb.terminationReason[i] and not("not found" in prb.terminationReason[i]):
                counter = counter + 1 
                _differenceCounter[i]= _differenceCounter[i]+1
        if not(counter==0): 
            total=total+1
            return True

    if "Refutation" in t0 and not("not found" in t0):
        counter = 0
        for i in range(1,5):
            if "Time limit" in prb.terminationReason[i] or "Memory limit" in prb.terminationReason[i] or "Refutation not found" in prb.terminationReason[i]:
                counter= counter+1
        
        if counter == 4:
            _differenceCounter[0]=_differenceCounter[0]+1 
            total = total+1
            return True
    return False

def printBegin(fout): 
    fout.write("\documentclass{article}\n")
    fout.write("\usepackage{graphicx}\n")
    fout.write("\usepackage{longtable}\n")
    fout.write("\\begin{document}\n")
    
    # create a table containing all the infor regarding satisfiability 
    fout.write("% this is an autogenerated statistics file\n")

def printEnd(fout):
    fout.write("\n\\end{document}\n")
    
def createReportFile(reportFileName):
    fout = open(reportFileName,"a")
    printBegin(fout)
    
    writeGeneralTable(fout)
    
    writeSatStatistics(_listOfProblems,fout)

    diffProblems = []
    for i in _listOfProblems: 
        if keepIt(i)==True: 
            diffProblems.append(i)
    fout.write("\n")
    fout.write("%%sat statistics for the diff files")
    writeSatStatistics(diffProblems,fout)
    fout.write("%%Total of :"+str(total)+" different problems\n%%")
    for i in _differenceCounter:
        fout.write(str(i)+" ")
    printEnd(fout)
    fout.close()
    
    # now single files 
    fout = open(reportFileName[:len(reportFileName)-4]+"_general.tex","w")
    printBegin(fout)
    writeGeneralTable(fout,False)
    printEnd(fout)
    fout.close()
    
    #print general Sat Statistics
    
    fout= open(reportFileName[:len(reportFileName)-4]+"_generalSAT.tex","w")
    printBegin(fout)
    writeSatStatistics(_listOfProblems,fout)
    printEnd(fout)
    fout.close()
    # write diff statistics 
    fout= open(reportFileName[:len(reportFileName)-4]+"_diffSAT.tex","w")
    printBegin(fout)
    writeSatStatistics(diffProblems,fout)
    fout.write("%%Total of :"+str(total)+" different problems\n%%")    
    for i in _differenceCounter:
        fout.write(str(i)+" ")
    printEnd(fout)
    fout.close()
    '''
    fout = open(reportFileName+"_just_sat","a")
    
    fout.close()
    '''
'''
Walk trough all the subdirectories that end with RES
these are the directories created by us
'''
def goTroughDirs(root):
    for subdir, dirs, files in os.walk(root):
        if subdir.endswith(".RES"):
            print "Genearating statistics for "+subdir
            generateStatisticsForDir(subdir+"/")                
 
   
if __name__ == '__main__':
    goTroughDirs(sys.argv[1])
    # now create the report files 
    createReportFile(sys.argv[2])
'''    
    for i in _listOfProblems:
        i.printPrb() 
'''
