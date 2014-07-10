#!/usr/bin/env python 

import sys, os, time
import re 
from os import path
from operator import indexOf

class Problem: 
    name = None 
    terminationReason = None
    proofAttempts = None
    time = None
    satClauses = None
    satVariables = None
    satCalls = None 
    satTime = None 
    strategy = None 
    fileName = None
    
    comparisonStrategy = None
    
    vSplitClauses = None
    vSplitRefutations = None
    vSplitComponents = None
    
    def __init__(self , name, filename):
        self.name = name
        self.terminationReason = list()
        self.proofAttempts = list() 
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
        self.comparisonStrategy = ""
        
    def addTerminationReason(self, termination):
        self.terminationReason.append(termination)
    
    def addProofAttempt(self,pattemptList):
        self.proofAttempts.append(pattemptList)
        
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
    def addCompStrategy(self,strat):
        self.comparisonStrategy = strat
        
    def resetStats(self):
        self.proofAttempts = list() 
        self.satClauses = list()
        self.satVariables = list() 
        self.satCalls = list() 
        self.satTime = list()
        self.strategy = list()
        self.vSplitClauses = list()
        self.vSplitComponents = list()
        self.vSplitRefutations = list()
        self.comparisonStrategy = ""
        
    def printMe(self):
        print self.name
        print self.terminationReason
        print self.time
        print self.satClauses
        print self.satVariables
        print self.satCalls
        print self.satTime
        print self.strategy
        print self.fileName
        print self.vSplitClauses
        print self.vSplitComponents
        print self.vSplitRefutations
        
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
    time = "0"
    satClauses = "0"
    satVariables = "0"
    satCalls = "0"
    satTimeSpent = "0"
    strategy = ""
    terminationReason = "TOI"
    checkReason = ""
    
    vSplitClauses = "0"
    vSplitComponents = "0"
    vSplitRefutations = "0"
    
    proofAttemptList = []
    currentProofStat = []
    first = True
    problemName = ""
    for x in fileLines:
        i=x.strip()
        if i.startswith("STRATEGY"): 
            interm= i.strip().split(" ")[3]
            problemName = ""
            if interm.endswith("%"):
                problemName = interm.strip("%")
            else:
                newInterm = interm.split("/")[1]
                problemName = newInterm
            if not(problemName==_listOfProblems[problemIndex].name): 
                print "trying to add statistics to the wrong problem!"
                print problemName + " vs " + _listOfProblems[problemIndex].name
                #exit(1)
        # collect total time elapsed for this strategy
        elif "% Success in time" in i: 
            if i.endswith("%"):
                continue;
            temp = i.strip().split(" ")
            time = temp[len(temp)-2]
            
        elif "% Proof not found in time" in i:
            if i.endswith("%"):
                continue
            temp = i.strip().split(" ")
            time = temp[len(temp)-2]
            #[].strip().split(" ")[0]
            #print time
        elif i.startswith("% TWLsolver") or i.startswith("% Lingeling"): 
            if i.endswith("%"):
                #print i
                continue;
            splittedBySemi = i.strip().split(":")
            splittedBySemicolumn = ""
            if len(splittedBySemi) <= 1: 
                print splittedBySemi
            else: 
                splittedBySemicolumn= splittedBySemi[1].strip()
            
            if "solver time" in i : 
                satTimeSpent = splittedBySemicolumn
            elif "elapsed time" in i:
                satTimeSpent = splittedBySemicolumn
            elif "clauses" in i: 
                satClauses = splittedBySemicolumn
            elif "variables" in i : 
                satVariables = splittedBySemicolumn
            elif "calls for" in i : 
                satCalls = splittedBySemicolumn
        elif i.startswith("SAT solver time :"): 
            splittedBySemi = i.strip().split(":")
            splittedBySemicolumn = "0"
            if len(splittedBySemi)<=1: 
                print splittedBySemi 
            else:   
                splittedBySemicolumn = splittedBySemi[1].strip()
                satTimeSpent = splittedBySemicolumn
        elif i.startswith("% SZS status ") : 
            if i.endswith("%"):
                print i
                continue;
            splitted = i.strip().split(" ")
            terminationReason = splitted[len(splitted)-3]
        elif "Thanks to" in i : 
            checkReason = i
        elif i.startswith("% Split"):
            if i.endswith("%") : 
               print i 
               continue
               
            splittedBySemicolumn = i.strip().split(":")[1].strip()
            if "clauses" in i:
                vSplitClauses = splittedBySemicolumn
            elif "components" in i:
                vSplitComponents = splittedBySemicolumn
        elif i.startswith("% Sat splitting refutation"):
            if i.endswith("%"):
                print i
                continue
            splittedBySemicolumn = i.strip().split(":")[1].strip()
            vSplitRefutations = splittedBySemicolumn            
        if i.startswith("%"):
            currentProofStat.append(i.strip("\n"))
            #print i
        elif " on " in i and problemName[:len(problemName)-2] in i and not(i.startswith("%")):
            if first == True:
                # it means that we do not have yet a proof attempt 
                currentProofStat.append(i)
                first = False
            else : 
                proofAttemptList.append(currentProofStat)
                currentProofStat = []
                currentProofStat.append(i)
                
                
    proofAttemptList.append(currentProofStat)
                
            
        
    _listOfProblems[problemIndex].addSatCalls(satCalls)
    _listOfProblems[problemIndex].addSatVariables(satVariables)
    _listOfProblems[problemIndex].addSatClauses(satClauses)
    _listOfProblems[problemIndex].addSatTime(satTimeSpent)
    _listOfProblems[problemIndex].addTerminationReason(terminationReason)
    if time == "0" : 
        time = "240.123"
        
    _listOfProblems[problemIndex].addTotalTime(time)
    _listOfProblems[problemIndex].addVSplitComponents(vSplitComponents)
    _listOfProblems[problemIndex].addVSplitClauses(vSplitClauses)
    _listOfProblems[problemIndex].addVSplitRefutations(vSplitRefutations)
    _listOfProblems[problemIndex].addProofAttempt(proofAttemptList)
    _listOfProblems[problemIndex].addCompStrategy("")
    #print "For problem "+_listOfProblems[problemIndex].name+" for strateg: "+str(len(_listOfProblems[problemIndex].strategy))+" we have "+str(len(proofAttemptList)) 
    # _listOfProblems[problemIndex].printMe()
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
        #print directory+filename+" with failing strategy "+str(i)
        collectSingleProblemStatistics(lines, problemIndex)
        _listOfProblems[problemIndex].addStrategy(str(i))


def insertNewProblem(dir, file): 
    
    if not path.exists(dir+file):
        print dir+file
        sys.exit()
        
    fin = open(dir+file,"r")
    
    lines = fin.readlines()

    if len(lines)==0:
        print "check this file: "+dir+file
        return -1    
    for i in lines: 
        if i.startswith("STRATEGY"): 
            interm= i.strip().split(" ")[3]
            problemName = ""
            if interm.endswith("%"):
                problemName = interm.strip("%")
            else:
                newInterm = interm.split("/")[1]
                problemName = newInterm
            #problemName = i.strip().split(" ")[3].split("/")[1]
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
            print i
            problemIndex = insertNewProblem(directory,i)
            #print problemIndex
            #print _listOfProblems[problemIndex].name
            if not(problemIndex == -1) : 
                getProblemStatistics(directory,i,problemIndex)
    
    dirName = ""

def writeTableHeader(fout,columns,flag=False):
    fout.write("\n\\begin{table}\n\\begin{tabular}{")
    for i in range(columns):
        fout.write("|c")
    fout.write("|c|")
    fout.write("}\n\\hline\n")
    if flag==False:
        fout.write("& Vamp & L & L S & L I & L I S\\\\\n\\hline\n")
    
def writeTableEnd(fout):
    fout.write("\\end{tabular}\n\\end{table}\n")
    
def writeReason(fout, termR, time, strat, flag=False):
    global _totalRef
    global _timeRef
    if "Theorem" in termR : 
        fout.write("TH:"+time)
        if flag == True: 
            _timeRef[strat] = _timeRef[strat]+float(time)
            _totalRef[strat] = _totalRef[strat]+1
        return
    if "Unsatisfiable" in termR : 
        fout.write("US:"+time)
        if flag == True: 
            if "%" in time: 
                return
            if not(time.isalpha()):
                _timeRef[strat] = _timeRef[strat]+float(time)
                _totalRef[strat] = _totalRef[strat]+1
        return
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
    if "Timeout" in termR: 
        fout.write("TO")
        return 
    if "Unknown" in termR: 
        fout.write("UKN")
        return
    if "Memory limit" in termR: 
        fout.write("MEM")
        return
    if "GaveUp" in termR: 
        fout.write("GU")
        return 
    fout.write(termR.strip("%")+time.strip("%"))
    return

'''     
write table with all the statistics from problems 
each table will be 40 lines
'''
def writeGeneralTable(fout, flag=True):
    print len(_listOfProblems)
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
    
    fout.write("\n\\begin{table}\n\\begin{tabular}{|c|c|c|c|c|c|}\n\\hline\n")
    fout.write("Avg Time &")
    for i in range(4):
        #fout.write(str(float(_timeRef[i]))+" &")
        fout.write(str(float(_timeRef[i]/_totalRef[i]))+" &")
    fout.write(str(float(_timeRef[4]/_totalRef[4]))+" \\\\\n\\hline\n")
    fout.write("Total Solved & ")
    for i in range(4):
        fout.write(str(float(_totalRef[i]))+" &")
    fout.write(str(float(_totalRef[4])))
    fout.write("\\\\\n\\hline\n\\end{tabular}\n\\end{table}\n")
    fout.write("\n%%Total number of problems: "+str(len(_listOfProblems)) )
    
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
    writeTableHeader(fout,8, True)
    fout.write("name & Cls & Vars & Calls & SplR & SplCl & SplCo & SatTime & Time \\\\\n\\hline\n")

    for i in range(totalProblems): 
        if i%5 == 0 and not(i==0): 
            writeTableEnd(fout)
            writeTableHeader(fout,8, True)
            fout.write("name & Cls & Vars & Calls & SplR & SplCl & SplCo & SatTime & Time \\\\\n\\hline\n")
            
        prb = listOfProblems[i] 
        strategy = prb.comparisonStrategy.split(" on ")[0].replace("_","\\_").strip("\n")
        
        '''
        If one wants the strategy on a single line comment from below to the next marker 
        #$$#
        '''
        chunks = 0
        
        csize = 65
        if len(strategy)>csize: 
            chunks = len(strategy)/csize
        strat = []
        
        if chunks >= 1 : 
            for i in range(chunks):
                strat.append(strategy[i*csize:i*csize+csize])
            strat.append(strategy[chunks*csize:])
        else : 
            strat.append(strategy)
            
        fout.write("\\hline\n"+prb.name+"& \multicolumn{8}{c|}{\\small{"+strat[0]+"}} \\\\\n")
        if chunks >=1:
            for i in range(1,chunks+1):
                fout.write(" & \multicolumn{8}{c|}{\\small{"+strat[i]+"}} \\\\\n")
                
        fout.write("\\hline\n")
        
        '''
        the next marker 
        #$$# 
        
        and uncomment the following : 
        
        fout.write("\\hline\n"+prb.name+"& & & & & & & & \\\\\n\\hline")
        fout.write("\n%%\multicolumn{9}{c|}{\\small{"+strategy+"}} \\\\\n")
        fout.write("\\hline\n")
        '''
        
        #fout.write("\\hline\n"+prb.name+"&&&&&&&& \\\\\n\\hline\n")
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
            
    fout.write("\\hline\n\\end{tabular}\n\\end{table}")

def keepIt(prb): 
    global _differenceCounter
    global total
    #check if can be solved only by us 
    t0 = prb.terminationReason[0]

    if not("Theorem" in t0) and not("Unsatisfiable" in t0):
        counter = 0
        for i in range(1,5):
            if "Theorem" in prb.terminationReason[i] or "Unsatisfiable" in prb.terminationReason[i]:
                counter = counter + 1 
                _differenceCounter[i]= _differenceCounter[i]+1
        if not(counter==0): 
            total=total+1
            return True

    counter = 0
    if "Theorem" in t0 or "Unsatisfiable" in t0:
        counter = 0
        for i in range(1,5):
            if not("Theorem" in prb.terminationReason[i]) and not("Unsatisfiable" in prb.terminationReason[i]):
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
    
    # create a table containing all the info regarding satisfiability 
    fout.write("% this is an autogenerated statistics file\n")

def printEnd(fout):
    fout.write("\n\\end{document}\n")
    
def getWinStrateg(problem, winner):
    for i in problem.proofAttempts[winner]:
        for item in i : 
            if "% Termination reason: Refutation" == item.strip(): 
                for x in i: 
                    if not(x.startswith("% ")):
                        return x.split(" on ")[0].strip()
    print "ERROR in finding the winning strategy!"
    print problem.name
    print problem.fileName
    sys.exit()
    
def isInList(lista, elem):
    for i in lista: 
        if elem.strip() == i.strip(): 
            return True
    print ('will add %r ' % (elem))
    return False 

def getStrategiesForComparison(problem):
    
    comparisonStrateg = []
    
    # for all the problems
    for i in range(5):
        if "Theorem" in problem.terminationReason[i] or "Unsatisfiable" in problem.terminationReason[i]:
            winStrateg = getWinStrateg(problem, i)
            if isInList(comparisonStrateg, winStrateg)==False: 
                comparisonStrateg.append(winStrateg)
            winStrateg = "" 
    return comparisonStrateg

def getStrategyIndex(problem, strategy, index):
    if len(problem.proofAttempts)==0: 
        return -1
    for idx,i in enumerate(problem.proofAttempts[index]): 
        for j in i: 
            if strategy.strip() in j.strip(): 
                return idx
    return -1 

def getStats(lines):
    
    satClauses = "0"
    satVariables = "0"
    satCalls = "0"
    satTimeSpent = "0"
    vSplitClauses = "0"
    vSplitComponents = "0"
    vSplitRefutations = "0"
    
    for i in lines: 

        if i.endswith("%"): 
            continue
        if i.startswith("% TWLsolver") or i.startswith("% Lingeling"): 
            splittedBySemicolumn = i.strip().split(":")[1].strip()
            if "solver time" in i : 
                satTimeSpent = splittedBySemicolumn.strip(" s")
            elif "elapsed time" in i: 
                satTimeSpent = splittedBySemicolumn
            elif "clauses" in i: 
                satClauses = splittedBySemicolumn
            elif "variables" in i : 
                satVariables = splittedBySemicolumn
            elif "calls for" in i : 
                satCalls = splittedBySemicolumn
        elif "SAT solver time" in i : 
            splittedBySemicolumn = i.strip().split(":")[1].strip()
            satTimeSpent = splittedBySemicolumn.strip(" s")            
        elif i.startswith("% Split"):
            splittedBySemicolumn = i.strip().split(":")[1].strip()
            if "clauses" in i:
                vSplitClauses = splittedBySemicolumn
            elif "components" in i:
                print i
                vSplitComponents = splittedBySemicolumn
        elif i.startswith("% Sat splitting refutation"): 
            splittedBySemicolumn = i.strip().split(":")[1].strip()
            print i 
            vSplitRefutations = splittedBySemicolumn

    print "splC "+vSplitComponents+" splr "+vSplitRefutations

    return (satClauses,satVariables,satCalls,satTimeSpent,vSplitClauses,vSplitComponents,vSplitRefutations)

def getProblemStatisticsForStrategy(problem, strategy):
    newStratProblem = Problem(problem.name, problem.fileName)
    #newStratProblem.resetStats()
    for i in problem.terminationReason:
        newStratProblem.addTerminationReason(i)
    
    for i in problem.time: 
        newStratProblem.addTotalTime(i)
        
    satClauses = "-"
    satVariables = "-"
    satCalls = "-"
    satTimeSpent = "-"
    vSplitClauses = "-"
    vSplitComponents = "-"
    vSplitRefutations = "-"
    
    for strat in range(5):
        #print strat
        index = getStrategyIndex(problem, strategy, strat)
        if index!=-1:
            proofAtt = problem.proofAttempts[strat]
            currProof = proofAtt[index]
            #print currProof
            (satClauses,satVariables,satCalls,satTimeSpent,vSplitClauses,vSplitComponents,vSplitRefutations)= getStats(currProof)
            #print (satClauses,satVariables,satCalls,satTimeSpent,vSplitClauses,vSplitComponents,vSplitRefutations)
        newStratProblem.addSatCalls(satCalls)
        newStratProblem.addSatVariables(satVariables)
        newStratProblem.addSatClauses(satClauses)
        newStratProblem.addSatTime(satTimeSpent)
        newStratProblem.addVSplitComponents(vSplitComponents)
        newStratProblem.addVSplitClauses(vSplitClauses)
        newStratProblem.addVSplitRefutations(vSplitRefutations)
        newStratProblem.addCompStrategy(strategy)
    
    return newStratProblem

def writeOneToOneComparisons(problems, out):
    newStatisticsList = list()
    
    # go trough all the problems
    for prb in problems: 
        #go trough all strategies
        listOfStrategiesToCompare = getStrategiesForComparison(prb)
        for strategy in listOfStrategiesToCompare: 
            print (' %r we add this ' %(strategy))
            newStat = getProblemStatisticsForStrategy(prb, strategy)
            newStatisticsList.append(newStat)
    
    writeSatStatistics(newStatisticsList, out)

    
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
    fout.write("%%Total of :"+str(total)+" different problems\n%% ")
    for i in _differenceCounter:
        fout.write(str(i)+"  ")
    
    printEnd(fout)
    fout.close()
    
    # now single files 
    fout = open(reportFileName[:len(reportFileName)-4]+"_general.tex","w")
    printBegin(fout)
    writeGeneralTable(fout,False)
    printEnd(fout)
    fout.close()
    
    #print general Sat Statistics
    '''
    fout= open(reportFileName[:len(reportFileName)-4]+"_generalSAT.tex","w")
    printBegin(fout)
    writeSatStatistics(_listOfProblems,fout)
    printEnd(fout)
    fout.close()
    '''
    # write diff statistics 
    fout= open(reportFileName[:len(reportFileName)-4]+"_diffSAT.tex","w")
    printBegin(fout)
    writeOneToOneComparisons(diffProblems,fout)
    #writeSatStatistics(diffProblems,fout)
    writeTableHeader(fout, 5)
    fout.write("%%Total of :"+str(total)+" different problems\n &")    
    x = 0 
    for i in _differenceCounter:
        fout.write(str(i)+" ")
        if x < 4 : 
            fout.write("&")
        x=x+1
    fout.write("\\\\\n\\hline\n")
    fout.write("\\end{tabular}\n")
    fout.write("\\caption{Total of "+str(total)+" different problems }")
    fout.write("\\end{table}")

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
def goTroughDirs(root, end):
    for subdir, dirs, files in os.walk(root):
        if subdir.endswith(end+".RES"):
            print "Genearating statistics for "+subdir
            generateStatisticsForDir(subdir+"/")                
 
def goTD(root):
    print root
    generateStatisticsForDir(root)    
    print "done generating"
   
if __name__ == '__main__':
    
    if len(sys.argv) == 2 :
        print "eqwual 2"
        en = sys.argv[1].split("/")
        end = en[len(en)-1].split(".")[0]
        print end
        goTD(sys.argv[1])
        
        createReportFile(end+".tex")
        sys.exit(1)
    
    if len(sys.argv) > 3:
        print "mai mare ca trei"
        goTroughDirs(sys.argv[1], sys.argv[3])
    else:
        goTroughDirs(sys.argv[1],"")
    # now create the report files 
    createReportFile(sys.argv[2])
'''    
    for i in _listOfProblems:
        i.printPrb() 
'''
