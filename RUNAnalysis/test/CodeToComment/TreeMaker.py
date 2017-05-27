#!/usr/bin/env python

import sys,os,time
import argparse
from collections import OrderedDict
from multiprocessing import Process
from ROOT import *
from array import array
from random import randint
from ROOT import TFile, TTree, TDirectory, gDirectory, gROOT, TH1F, TH2F, TMath
from RUNA.RUNAnalysis.commonFunctions import *
gROOT.Reset()

def TreeMaker( oldTree, newTree, treeDirectory, treeName ):
    oldFile, oldTree, numEntries = getTree( oldTree, treeDirectory + "/" + treeName )

    newFile = TFile(newTree, "RECREATE")
    newFile.cd()
    dir = treeDirectory.split("/")
    directory = ""
    print dir
#    for i in dir:
#        directory = directory + "/" + i
#        print directory
    newFile.mkdir(treeDirectory)
    newFile.cd(treeDirectory)
    newTree = oldTree.CloneTree(0)
    
    for i in xrange(numEntries):
        oldTree.GetEntry(i)
        if i%15 == 0: newTree.Fill()
    newTree.Print()
    newTree.AutoSave()

parser = argparse.ArgumentParser()
parser.add_argument( '-o', '--oldTree', action='store', dest='oldTree', default="", help='Old Tree')
parser.add_argument( '-n', '--newTree', action='store', dest='newTree', default="", help='New Tree')
parser.add_argument( '-d', '--treeDirectory', action='store', dest='treeDirectory', default="", help='Directory with tree')
parser.add_argument( '-t', '--treeName', action='store', dest='treeName', default="", help='Name of tree')
parser.set_defaults(plot=True)
try:
    args = parser.parse_args()
    print "here"
except:
    parser.print_help()
    sys.exit(0)

TreeMaker( args.oldTree, args.newTree, args.treeDirectory, args.treeName )
