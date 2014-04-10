'''
    {description}
    Copyright (C) {2014}  {Ioan Dragan}

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
