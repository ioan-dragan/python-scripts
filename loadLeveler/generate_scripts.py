#!/usr/bin/python

# Copyright (C) {2014}  {Ioan Dragan}

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


op = open("DirsFile.txt","r")
opr = op.readlines()

submit = open("submit.cmd","a")
submit.write("#!/bin/bash")

for DIR in opr:
    dirName = DIR.strip()
    output = open(dirName+".cmd","w+")
    submit.write("llsubmit "+dirName+".cmd && \n")
    output.write( " #!/bin/sh \n")
    output.write( " # @ error = /u/users/invites/idragan/ComparisonSATSolvers/TPTP/Results_FOF_TPTP2T/"+dirName+".ERR/$(job_name).$(Process).err\n")
    output.write( " # @ output  = /u/users/invites/idragan/ComparisonSATSolvers/TPTP/Results_FOF_TPTP2T/"+dirName+".RES/"+dirName+"_$(job_name).$(Process).out\n")
    output.write( " # @ job_type = serial\n")
    output.write( " # @ class = large\n")
    output.write( " # @ user_priority = 20 \n")
    output.write( " # @ environment = COPY_ALL\n")
    output.write( " # @ job_name = vampire_"+dirName+"\n")
    output.write( " # @ notification = error\n")
    output.write( " # @ notify_user = ioan@complang.tuwien.ac.at \n")
    output.write( " # @ queue = 10\n")
    output.write( "\n\n")
    output.write( "PROBLEMS=`ls /u/users/invites/idragan/ComparisonSATSolvers/TPTP/scripts/getProblems.py "+dirName+"`\n")
    output.write( "#for LOADL_STEP_NUMBER in $(seq 0 9); do \n")
    output.write( "VAMPIRE_PARAMS=`/u/users/invites/idragan/ComparisonSATSolvers/TPTP/scripts/getStrategy.py ${LOADL_STEP_NUMBER}`\n")

    output.write( "\n" )
    output.write( "for PROB in ${PROBLEMS}; do\n")
    output.write( "    echo \"STRATEGY_NO ${LOADL_STEP_NUMBER} PROBLEM ${PROB} WITH ARGS=${VAMPIRE_PARAMS}\" \n")
    output.write( "    ./vampire_rel /u/users/invites/idragan/ComparisonSATSolvers/TPTP/Problems/TPTP-v6.0.0/"+dirName+"/${PROB} ${VAMPIRE_PARAMS}\n")
    output.write( "done\n")
    output.close()

