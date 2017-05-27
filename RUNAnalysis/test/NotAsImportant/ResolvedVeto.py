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

def EventSkip( resTree, resTreeDirectory, resTreeName, oldTree, newTree, treeDirectory, treeName ):
    resFile, resTree, resNumEntries = getTree( resTree, resTreeDirectory + "/" + treeName )
    
    skipEvent = []
    muPtRes = []
    for i in xrange(resNumEntries):
#        print resTree.event
        resTree.GetEntry(i)
        deltaEta = resTree.deltaEta
        massAsym = resTree.massAsym
        delta1 = resTree.delta1
        delta2 = resTree.delta2

        jet1Pt = resTree.jetsPt[0]
        jet2Pt = resTree.jetsPt[1]
        jet3Pt = resTree.jetsPt[2]
        jet4Pt = resTree.jetsPt[3]
        HT = resTree.HT

        passResPres = (jet1Pt>80) and (jet2Pt>80) and (jet3Pt>80) and (jet4Pt>80) and (HT>850)
        passResCuts = (delta1>200) and (delta2>200) and (massAsym<0.1) and (deltaEta<1.0)
        passRes = passResPres and passResCuts
        if passRes:
            skipEvent.append(resTree.event)
            muPtRes.append(resTree.MET)
    oldFile, oldTree, numEntries = getTree( oldTree, treeDirectory + "/" + treeName )

    newFile = TFile(newTree, "RECREATE")
    newFile.cd()
    dir = treeDirectory.split("/")
    directory = ""
    newFile.mkdir(treeDirectory)
    newFile.cd(treeDirectory)
    newTree = oldTree.CloneTree(0)
    
    muPtBoos = []
    for i in xrange(numEntries):
        oldTree.GetEntry(i)
        if not(oldTree.event in skipEvent): 
            newTree.Fill()
        if (oldTree.event in skipEvent):
            muPtBoos.append(oldTree.MET)
#    newTree.Print()
    newTree.AutoSave()


#    for i in xrange(len(muPtRes)):
#        if muPtRes[i]!=muPtBoos[i]: print "False!"
#        print str(muPtRes[i]) + " " + str(muPtBoos[i])
    
parser = argparse.ArgumentParser()
parser.add_argument( '-r', '--resTree', action='store', dest='resTree', default="", help='Resolved Tree')
parser.add_argument( '-i', '--resTreeDirectory', action='store', dest='resTreeDirectory', default="", help='Directory with resolved tree')
parser.add_argument( '-a', '--resTreeName', action='store', dest='resTreeName', default="", help='Resolved Tree Name')
parser.add_argument( '-o', '--oldTree', action='store', dest='oldTree', default="", help='Old Tree')
parser.add_argument( '-n', '--newTree', action='store', dest='newTree', default="", help='New Tree')
parser.add_argument( '-d', '--treeDirectory', action='store', dest='treeDirectory', default="", help='Directory with tree')
parser.add_argument( '-t', '--treeName', action='store', dest='treeName', default="", help='Name of tree')
parser.set_defaults(plot=True)
try:
    args = parser.parse_args()
#    print "here"
except:
    parser.print_help()
    sys.exit(0)

EventSkip( args.resTree, args.resTreeDirectory, args.resTreeName, args.oldTree, args.newTree, args.treeDirectory, args.treeName )
