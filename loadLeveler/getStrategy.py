#!/usr/bin/python
import os, sys, time
'''
Running this script generates the sat solver strategy to run

run script:

./getStrategy NO 
where NO is the job number (depending on this one can controll jobs on loadleveler)
'''

time_limit = "-t 240" 
mode = "--mode casc --ignore_missing on "
satSolver = ["--sat_solver twliteral", "--sat_solver lingeling", "--sat_solver lingeling --not-different on", "--sat_solver lingeling --sat_lingeling_incremental on", "--sat_solver lingeling --sat_lingeling_incremental on --not-different on"]

if __name__ == '__main__':
    if int(sys.argv[1]) < 5 :
        print mode+" "+time_limit+" "+satSolver[int(sys.argv[1])]+" "+"--include /u/users/invites/idragan/ComparisonSATSolvers/TPTP/TPTP-v6.0.0"
    else: 
        print time_limit+" "+satSolver[int(sys.argv[1])-5]+" "+"--include /u/users/invites/idragan/ComparisonSATSolvers/TPTP/TPTP-v6.0.0"
