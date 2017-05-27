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

resFileQCD, resTreeQCD, resNumEntriesQCD = getTree( "80XRootFilesUpdated/RUNAnalysis_QCDHTAll_80X_V2p3_v06.root", "ResolvedAnalysisPlots/RUNATree" ) 
boosFileQCD, boosTreeQCD, boosNumEntriesQCD = getTree( "80XRootFilesUpdated/RUNAnalysis_QCDHTAll_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree" ) 
resFileDATA, resTreeDATA, resNumEntriesDATA = getTree( "80XRootFilesUpdated/RUNAnalysis_JetHT_Run2016_80X_V2p3_v06_cut15.root", "ResolvedAnalysisPlots/RUNATree" ) 
boosFileDATA, boosTreeDATA, boosNumEntriesDATA = getTree( "80XRootFilesUpdated/RUNAnalysis_JetHT_Run2016_80X_V2p3_v06_cut15.root", "BoostedAnalysisPlots/RUNATree" ) 

print resNumEntriesQCD
print boosNumEntriesQCD
print resNumEntriesDATA
print boosNumEntriesDATA
#resNumEntriesQCD=10000
#boosNumEntriesQCD=10000
#resNumEntriesDATA=10000
#boosNumEntriesDATA=10000

#########################################

skipEventsQCD = []

print '-'*40
print '------> QCD, Resolved'
print '------> Number of events: '+str(resNumEntriesQCD)
d = 0
for i in xrange(resNumEntriesQCD):
    fraction = 10.*i/(1.*resNumEntriesQCD)
    if TMath.FloorNint(fraction) > d: print str(10*TMath.FloorNint(fraction))+'%' 
    d = TMath.FloorNint(fraction)
    resTreeQCD.GetEntry(i)
    deltaEta = resTreeQCD.deltaEta
    massAsym = resTreeQCD.massAsym
    delta1 = resTreeQCD.delta1
    delta2 = resTreeQCD.delta2
    
    jet1Pt = resTreeQCD.jetsPt[0]
    jet2Pt = resTreeQCD.jetsPt[1]
    jet3Pt = resTreeQCD.jetsPt[2]
    jet4Pt = resTreeQCD.jetsPt[3]
    HT = resTreeQCD.HT

    passResPres = (jet1Pt>80) and (jet2Pt>80) and (jet3Pt>80) and (jet4Pt>80) and (HT>900)
    passResCuts = (delta1>200) and (delta2>200) and (massAsym<0.1) and (deltaEta<1.0)
    passRes = passResPres and passResCuts
    if passRes:
        skipEventsQCD.append([resTreeQCD.run, resTreeQCD.event])

#########################################

skipEventsDATA = []

print '-'*40
print '------> DATA, Resolved'
print '------> Number of events: '+str(resNumEntriesDATA)
d = 0
for i in xrange(resNumEntriesDATA):
    fraction = 10.*i/(1.*resNumEntriesDATA)
    if TMath.FloorNint(fraction) > d: print str(10*TMath.FloorNint(fraction))+'%' 
    d = TMath.FloorNint(fraction)
    resTreeDATA.GetEntry(i)
    deltaEta = resTreeDATA.deltaEta
    massAsym = resTreeDATA.massAsym
    delta1 = resTreeDATA.delta1
    delta2 = resTreeDATA.delta2
    
    jet1Pt = resTreeDATA.jetsPt[0]
    jet2Pt = resTreeDATA.jetsPt[1]
    jet3Pt = resTreeDATA.jetsPt[2]
    jet4Pt = resTreeDATA.jetsPt[3]
    HT = resTreeDATA.HT

    passResPres = (jet1Pt>80) and (jet2Pt>80) and (jet3Pt>80) and (jet4Pt>80) and (HT>900)
    passResCuts = (delta1>200) and (delta2>200) and (massAsym<0.1) and (deltaEta<1.0)
    passRes = passResPres and passResCuts
    if passRes:
        skipEventsDATA.append([resTreeDATA.run, resTreeDATA.event])

#########################################

QCD_MASS_A = TH1D("QCD_Mass_A", "", 40, 0, 400)

print '-'*40
print '------> QCD, Boosted'
print '------> Number of events: '+str(boosNumEntriesQCD)
d = 0
for i in xrange(boosNumEntriesQCD):
    fraction = 10.*i/(1.*boosNumEntriesQCD)
    if TMath.FloorNint(fraction) > d: print str(10*TMath.FloorNint(fraction))+'%' 
    d = TMath.FloorNint(fraction)
    boosTreeQCD.GetEntry(i)
    massAve = boosTreeQCD.prunedMassAve
    deltaEta = boosTreeQCD.deltaEtaDijet
    massAsym = boosTreeQCD.prunedMassAsym
    jet1Tau21 = boosTreeQCD.jet1Tau21
    jet2Tau21 = boosTreeQCD.jet2Tau21
    jet1CSV = boosTreeQCD.jet1btagCSVv2
    jet2CSV = boosTreeQCD.jet2btagCSVv2
    jet1Tau32 = boosTreeQCD.jet1Tau32
    jet2Tau32 = boosTreeQCD.jet2Tau32

    PRES = (jet1Tau21<0.45 and jet2Tau21<0.45)
    A = (deltaEta<1.0 and massAsym<0.1)
    BTAG = (jet1CSV<0.8484 and jet2CSV<0.8484)
    TOPTAG = (jet1Tau32>0.67 and jet2Tau32>0.67)
    RESVETO = ([boosTreeQCD.run, boosTreeQCD.event] not in skipEventsQCD)
    
    if PRES and A and BTAG and TOPTAG and RESVETO:
        QCD_MASS_A.Fill(massAve, boosTreeQCD.puWeight*boosTreeQCD.lumiWeight*36555.21/15*.85)

#########################################

DATA_MASS_A = TH1D("DATA_Mass_A", "", 40, 0, 400)

print '-'*40
print '------> DATA, Boosted'
print '------> Number of events: '+str(boosNumEntriesDATA)
d = 0
for i in xrange(boosNumEntriesDATA):
    fraction = 10.*i/(1.*boosNumEntriesDATA)
    if TMath.FloorNint(fraction) > d: print str(10*TMath.FloorNint(fraction))+'%' 
    d = TMath.FloorNint(fraction)
    boosTreeDATA.GetEntry(i)
    massAve = boosTreeDATA.prunedMassAve
    deltaEta = boosTreeDATA.deltaEtaDijet
    massAsym = boosTreeDATA.prunedMassAsym
    jet1Tau21 = boosTreeDATA.jet1Tau21
    jet2Tau21 = boosTreeDATA.jet2Tau21
    jet1CSV = boosTreeDATA.jet1btagCSVv2
    jet2CSV = boosTreeDATA.jet2btagCSVv2
    jet1Tau32 = boosTreeDATA.jet1Tau32
    jet2Tau32 = boosTreeDATA.jet2Tau32

    PRES = (jet1Tau21<0.45 and jet2Tau21<0.45)
    A = (deltaEta<1.0 and massAsym<0.1)
    BTAG = (jet1CSV<0.8484 and jet2CSV<0.8484)
    TOPTAG = (jet1Tau32>0.67 and jet2Tau32>0.67)
    RESVETO = ([boosTreeDATA.run, boosTreeDATA.event] not in skipEventsDATA)
    
    if PRES and A and BTAG and TOPTAG and RESVETO:
        DATA_MASS_A.Fill(massAve, boosTreeDATA.puWeight*boosTreeDATA.lumiWeight*36555.21/15*.85)


FILE = TFile("TCutPlots/MassPlotsQCDDATAResVeto.root", "RECREATE")
FILE.cd()
DATA_MASS_A.Write()
QCD_MASS_A.Write()
FILE.Write()
FILE.Save()

C = TCanvas("C","",800,800)
DATA_MASS_A.SetLineColor(kBlack)
DATA_MASS_A.SetMarkerColor(1)
DATA_MASS_A.SetMarkerStyle(20)
QCD_MASS_A.SetLineWidth(2)
QCD_MASS_A.SetLineColor(kBlack)
QCD_MASS_A.SetFillColor(kAzure-4)
QCD_MASS_A.SetMaximum(max(DATA_MASS_A.GetMaximum(), QCD_MASS_A.GetMaximum() ))
QCD_MASS_A.Draw("hist")
DATA_MASS_A.Draw("E0Same")
C.SaveAs("TCutPlots/ResVetoMassPlot.png")
