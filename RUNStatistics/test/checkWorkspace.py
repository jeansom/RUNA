#!/usr/bin/env python
################################################################################################
### Modify script from 
### https://gitlab.cern.ch/CMSDIJET/StatisticalTools/blob/master/scripts/checkWorkspace.py
#################################################################################################

import sys, os, copy, re
from ROOT import * 
from array import array

gROOT.SetBatch()

def main():

     inputFileWorkspace = TFile("Rootfiles/workspace_RPVSt100.root") 

     workspace = inputFileWorkspace.Get("myWS")
     workspace.Print()

     mjj = workspace.var("massAve")
     mjj.Print()

     data = workspace.data("data_obs")
     signal = workspace.data("signal")
     signalUp = workspace.data("signal_JESUp")
     signalDown = workspace.data("signal_JESDown")
     data.Print()
     signal.Print()

     data_TH1_fineBinning = data.createHistogram("data_TH1_fineBinning",mjj)    
     signal_TH1_fineBinning = signal.createHistogram("signal_TH1_fineBinning",mjj)    
     #signalUp_TH1_fineBinning = signalUp.createHistogram("signalUp_TH1_fineBinning",mjj)    
     #signalDown_TH1_fineBinning = signalDown.createHistogram("signalDown_TH1_fineBinning",mjj)    
     print "data_TH1_fineBinning integral = ", data_TH1_fineBinning.Integral()
     print "signal_TH1_fineBinning integral = ", signal_TH1_fineBinning.Integral()

     canvas = TCanvas()
     data_TH1_fineBinning.Rebin(10)    
     data_TH1_fineBinning.Draw()    
     signal_TH1_fineBinning.Rebin(10)
     signal_TH1_fineBinning.Draw("same")    
     #signalUp_TH1_fineBinning.Draw("sames")    
     #signalDown_TH1_fineBinning.Draw("sames")    
     c1.SaveAs("test.png")

if __name__ == '__main__':
    main()
