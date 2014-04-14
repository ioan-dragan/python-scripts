#!/usr/bin/python

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
