#!/usr/bin/env python 

import sys, os, time
import re 
from os import path
from operator import indexOf

import numpy as np 
import matplotlib.pyplot as plt

import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_pdf import PdfPages


def readFile(filename):
    fin = open(filename, "r")
    lines = fin.readlines()
    fin.close()

    fin.close()
    vamp =[] 
    l = [] 
    ls = []
    li = []
    lis = []
    
    normal = 10.0
    
    for ln in lines:
        i = ln.rstrip().split(",")
        
        vamp.append(float(i[0])/normal)
        l.append(float(i[1])/normal)
        ls.append(float(i[2])/normal)
        li.append(float(i[3])/normal)
        lis.append(float(i[4])/normal)

    return (vamp, l, ls, li, lis)

def getUpperDiag(vamp, lv):

    uv = []
    ul = []
    sv = []
    sl = []

    for i in range(len(vamp)):
        if float(lv[i]) > float(vamp[i]):
            uv.append(vamp[i])
            ul.append(lv[i])
        else: 
            sv.append(vamp[i])
            sl.append(lv[i])
    return (uv, ul, sv, sl)

def createSingleFigure(uv, ul , sv, sl, lingText):
    f, gen = plt.subplots(figsize=(6.5,6.5))
    gen.set(xlim=(0,6.5), ylim=(0,6.5))
    gen.scatter(uv, ul, c = "black", marker = '+')
    gen.plot(gen.get_xlim(), gen.get_ylim(), ls = "--", c=".8")

    gen.scatter(sv, sl, c = ".8", marker = ".")
    gen.set_xlabel('Default sat solver')
    gen.set_ylabel(lingText)
    plt.show()

'''
Plot four figures separately so that we can create single files. Also takes into account about above and below diagonal 
and prints different symbols 
'''
def plotDifferent(filename):
    (vamp, l, ls, li, lis) = readFile(filename)
    
    (uv, ul, sv, sl) = getUpperDiag(vamp, l)

    plt.close('all')
    createSingleFigure(uv, ul, sv, sl, 'Lingeling "almost"')

    (uv, ul, sv, sl) = getUpperDiag(vamp, ls)
    createSingleFigure(uv, ul, sv, sl, 'Lingeling "almost" similar')

    (uv, ul, sv, sl) = getUpperDiag(vamp, li)
    createSingleFigure(uv, ul, sv, sl, 'Lingeling incremental')

    (uv, ul, sv, sl) = getUpperDiag(vamp, lis)
    createSingleFigure(uv, ul, sv, sl, 'Lingeling incremental similar')


'''
Using this function we plot a big figure with 4 subfigs 
'''
def plotResults(filename):
    
    fin = open(filename, "r")
    lines = fin.readlines() 
    fin.close()
    vamp =[] 
    l = [] 
    ls = []
    li = []
    lis = []
    
    normal = 10.0
    
    for ln in lines:
        i = ln.rstrip().split(",")
        
        vamp.append(float(i[0])/normal)
        l.append(float(i[1])/normal)
        ls.append(float(i[2])/normal)
        li.append(float(i[3])/normal)
        lis.append(float(i[4])/normal)

    maxim = max(vamp)+5
    
    plt.close('all')
    fig = plt.figure() 
    gs = gridspec.GridSpec(2,2)
    ax = fig.add_subplot(gs[0])
    al = fig.add_subplot(gs[1])
    als = fig.add_subplot(gs[2])
    alis = fig.add_subplot(gs[3])

    #Performance of Default SAT solver\ncompared to Lingeling "almost"\nin Vampire'
    (uv, ul, sv, sl) = getUpperDiag(vamp, l)
    ax.set_xlabel('(a) Vampire with default SAT solver')
    ax.set_ylabel('Vampire with \nLingeling "almost"')
    ax.set(xlim = (0,6.5), ylim = (0,6.5))
    ax.scatter(uv, ul, c = "black", marker = '+')
    ax.plot(ax.get_xlim(), ax.get_ylim(), ls = "--", c=".8")
    ax.scatter(sv, sl, c = "black", marker = '.')

    (uv, ul, sv, sl) = getUpperDiag(vamp, ls)
    al.set_xlabel('(b) Vampire with default SAT solver')
    al.set_ylabel('Vampire with \nLingeling "almost" similar')
    al.set(xlim = (0,6.5), ylim = (0,6.5))
    al.plot(al.get_xlim(), al.get_ylim(), ls = "--", c=".8")
    al.scatter(uv, ul, c = "black", marker = '+')
    al.scatter(sv, sl, c = "black", marker = '.')

    (uv, ul, sv, sl) = getUpperDiag(vamp, li)
    als.set_xlabel('(c) Vampire with default SAT solver')
    als.set_ylabel('Vampire with \nLingeling incremental')
    als.set(xlim = (0,6.5), ylim = (0,6.5))
    als.plot(als.get_xlim(), als.get_ylim(), ls = "--", c=".8")
    als.scatter(uv, ul, c = "black", marker = '+')
    als.scatter(sv, sl, c = "black", marker = '.')

    #als.scatter(vamp, li, c = "red", marker = '+')

    (uv, ul, sv, sl) = getUpperDiag(vamp, lis)
    alis.set_xlabel('(d) Vampire with default SAT solver')
    alis.set_ylabel('Vampire with \nLingeling incremental similar')
    alis.set(xlim = (0,6.5), ylim = (0,6.5))
    alis.plot(alis.get_xlim(), alis.get_ylim(), ls = "--", c=".8")
    alis.scatter(uv, ul, c = "black", marker = '+')
    alis.scatter(sv, sl, c = "black", marker = '.')
    
    gs.tight_layout(fig, rect=[0,0,1,1])

    
    f, gen = plt.subplots(figsize=(6.5,6.5))
    gen.set(xlim=(0,6.5), ylim=(0,6.5))
    gen.scatter(vamp, l, c = "red", marker = '+')
    gen.scatter(vamp, ls, c = "red", marker = '+')
    gen.scatter(vamp, li, c = "red", marker = '+')
    gen.scatter(vamp, lis, c = "red", marker = '+')
    gen.plot(gen.get_xlim(), gen.get_ylim(), ls = "--", c=".3")
    gen.set_xlabel('Vampire with default SAT solver')
    gen.set_ylabel('Vampire with \nLingeling variations')
    
    plt.show()

if __name__ == '__main__':
    plotResults(sys.argv[1])
    #plotDifferent(sys.argv[1])