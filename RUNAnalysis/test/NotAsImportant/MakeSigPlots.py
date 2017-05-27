#!/usr/bin/env python

import os
import math
from array import array
import optparse
from ROOT import *
import scipy

from RUNA.RUNAnalysis.Plotting_Header import *
import RUNA.RUNAnalysis.CMS_lumi as CMS_lumi

gROOT.SetBatch()
gStyle.SetOptStat(0)
zerobtag = "(jet1btagCSVv2<0.8484&jet2btagCSVv2<0.8484)"
onebtag = "((jet1btagCSVv2<0.8484&jet2btagCSVv2>0.8484)||(jet1btagCSVv2>0.8484&jet2btagCSVv2<0.8484))"
twobtag = "(jet1btagCSVv2>0.8484&jet2btagCSVv2>0.8484)"

zerotop = "(jet1Tau32>0.51&jet2Tau32>0.51)"
onetop = "((jet1Tau32>0.51&jet2Tau32<0.51)||(jet1Tau32<0.51&jet2Tau32>0.51))"
twotop = "(jet1Tau32<0.51&jet2Tau32<0.51)"

tau21L = "(jet1Tau21<0.60&jet1Tau21>0.45)&(jet2Tau21<0.60&jet2Tau21>0.45)"
tau21T = "(jet1Tau21<0.45&jet2Tau21<0.45)"
tau21N = "(jet1Tau21<0.60&jet2Tau21<0.60)"

#pres = "((!(deltaEtaDijet<1.1||prunedMassAsym<0.1||(jet1Pt+jet2Pt-(jet1PrunedMass+jet2PrunedMass)/2)>200)))&(deltaEtaDijet<1.0&prunedMassAsym<0.1)&"
pres = "(deltaEtaDijet<1.0&prunedMassAsym<0.1)&"

cuts = [ [ "b0t0tau21L", pres+zerobtag+"&"+zerotop+"&"+tau21L ], 
         [ "b0t0tau21T", pres+zerobtag+"&"+zerotop+"&"+tau21T ],
         [ "b1t0tau21L", pres+onebtag+"&"+zerotop+"&"+tau21L ], 
         [ "b1t0tau21T", pres+onebtag+"&"+zerotop+"&"+tau21T ],
         [ "b2t0", pres+twobtag+"&"+zerotop+"&"+tau21N ],
         [ "b0t1", pres+zerobtag+"&"+onetop+"&"+tau21N ],
         [ "b1t1", pres+onebtag+"&"+onetop+"&"+tau21N ],
         [ "b2t1", pres+twobtag+"&"+onetop+"&"+tau21N ],
         [ "b0t2", pres+zerobtag+"&"+twotop+"&"+tau21N ],
         [ "b1t2", pres+onebtag+"&"+twotop+"&"+tau21N ],
         [ "b2t2", pres+twobtag+"&"+twotop+"&"+tau21N ]
         ]

def SigPlots( rootFile, mass, color ):
    hMassSig = []
    C = TCanvas("C", "", 800, 800)
    C.Divide(3, 4)
    latex = TLatex()
    for x in xrange(len(cuts)):
        C.cd(x+1)
        hMassSig.append(TH1F("SIG_prunedMassAve_"+cuts[x][0], "", 20, 0, 400))
        quickplot( rootFile, "BoostedAnalysisPlots/RUNATree", hMassSig[x], "prunedMassAve", cuts[x][1], "100*puWeight*lumiWeight" )
        hMassSig[x].GetXaxis().SetTitle("Pruned Average Mass [GeV]")
        hMassSig[x].GetYaxis().SetTitle("N Events/20 GeV")
        hMassSig[x].SetLineColor(color)
        hMassSig[x].Draw()
        latex = TLatex()
        latex.SetNDC()
        latex.SetTextSize(0.07)
        latex.SetTextAlign(13)
        latex.DrawLatex( .12, .88, cuts[x][0] )
        CMS_lumi.extraText = "Simulation Preliminary"
        CMS_lumi.relPosX = 0.13
        CMS_lumi.CMS_lumi( gPad, 4, 0 )
    C.cd(x+2)
    latex.SetNDC()
    latex.SetTextSize(0.1)
    latex.SetTextAlign(12)
    latex.DrawLatex( .1, .5, "RPV Stop UDD323 M-" + mass )
    C.SaveAs("TCutPlots/SigMassAve"+mass+".png")
    
#    hMassSig = TH1F("SIG_prunedMassAve", "", 40, 0, 400 )
    hABCDSig = TH2F("SIG_ABCD", "", 20, 0., 1., 20, 0., 5. )
#    hABCDQCD = TH2F("SIG_QCD", "", 20, 0., 1., 20, 0., 5. )
    
    
    quick2dplot( rootFile, "BoostedAnalysisPlots/RUNATree", hABCDSig, "prunedMassAsym", "deltaEtaDijet", "jet1Tau21<0.60&jet2Tau21<0.60", "36600*puWeight*lumiWeight/15" )

#quick2dplot( "", "BoostedAnalysisPlots/RUNATree", hABCDQCD, "prunedMassAve", "jet1Tau21<0.60&jet2Tau21<0.60", "36600*puWeight*lumiWeight/15" )
    
    C1 = TCanvas("C1", "", 800, 800 )
    C1.cd()
    L1 = TLine( .1, 0, .1, 5)
    L1.SetLineWidth(2)
    L2 = TLine( 0, 1.0, 1, 1.0)
    L2.SetLineWidth(2)
    hABCDSig.GetXaxis().SetTitle("Pruned Mass Asymmetry")
    hABCDSig.GetYaxis().SetTitle("Delta Eta Dijet")
    hABCDSig.GetYaxis().SetTitleOffset(1.2)
    hABCDSig.SetLineColor(color)
    CMS_lumi.extraText = "Simulation Preliminary"
    CMS_lumi.relPosX = 0.14
#hABCDQCD.SetLineColor(kBlue)
    hABCDSig.Draw("CONT3")
    L1.Draw("same")
    L2.Draw("same")
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.03)
    latex.SetTextAlign(12)
    latex.DrawLatex( .50, .8, "RPV Stop UDD323 M-" + mass )

    total = 0
    A = 0
    B = 0
    C = 0
    D = 0
    for binX in xrange(1, hABCDSig.GetXaxis().GetNbins()+1 ):
        for binY in xrange(1, hABCDSig.GetYaxis().GetNbins()+1 ):
            total = total + hABCDSig.GetBinContent(binX, binY)
            massAsym = hABCDSig.GetXaxis().GetBinCenter(binX)<0.1
            dEta = hABCDSig.GetYaxis().GetBinCenter(binY)<1.0
            if massAsym and dEta: A = A+hABCDSig.GetBinContent(binX, binY)
            if massAsym and (not dEta): B = B+hABCDSig.GetBinContent(binX, binY)
            if (not massAsym) and dEta: C = C+hABCDSig.GetBinContent(binX, binY)
            if (not massAsym) and (not dEta): D = D+hABCDSig.GetBinContent(binX, binY)
            
    int = TLatex()
    int.SetNDC()
    int.SetTextSize(0.02)
    int.DrawLatex( .40, .55, "Fraction A: " + '{:0.2e}'.format(float(A/total)) )
    int.DrawLatex( .40, .60, "Fraction B: " + '{:0.2e}'.format(float(B/total)) )
    int.DrawLatex( .60, .55, "Fraction C: " + '{:0.2e}'.format(float(C/total)) )
    int.DrawLatex( .60, .60, "Fraction D: " + '{:0.2e}'.format(float(D/total)) )

    
    CMS_lumi.CMS_lumi( C1, 4, 0 )
#hABCDQCD.Draw("CONT3")
    
    C1.SaveAs("TCutPlots/ABCDSig"+mass+".png")

    return [ hMassSig, hABCDSig ]

M180 = SigPlots( "80XRootFilesUpdated/RUNAnalysis_RPVStopStopToJets_UDD323_M-180_80X_V2p3_v06_ResVeto.root", "180", kRed )
M200 = SigPlots( "80XRootFilesUpdated/RUNAnalysis_RPVStopStopToJets_UDD323_M-200_80X_V2p3_v06_ResVeto.root", "200", kGreen )
M220 = SigPlots( "80XRootFilesUpdated/RUNAnalysis_RPVStopStopToJets_UDD323_M-220_80X_V2p3_v06_ResVeto.root", "220", kViolet )
M300 = SigPlots( "80XRootFilesUpdated/RUNAnalysis_RPVStopStopToJets_UDD323_M-300_80X_V2p3_v06_ResVeto.root", "300", kBlue )
#M180 = SigPlots( "80XRootFilesUpdated/RUNAnalysis_RPVStopStopToJets_UDD323_M-180_80X_V2p3_v06.root", "180", kRed )
#M200 = SigPlots( "80XRootFilesUpdated/RUNAnalysis_RPVStopStopToJets_UDD323_M-200_80X_V2p3_v06.root", "200", kGreen )
#M220 = SigPlots( "80XRootFilesUpdated/RUNAnalysis_RPVStopStopToJets_UDD323_M-220_80X_V2p3_v06.root", "220", kViolet )
#M300 = SigPlots( "80XRootFilesUpdated/RUNAnalysis_RPVStopStopToJets_UDD323_M-300_80X_V2p3_v06.root", "300", kBlue )

#hMassSignal = []
#for i in xrange(len(M180[0])):
#    hMassSignal.append(M180[0][i].Clone())
#    hMassSignal[i].Reset

#for i in xrange(len(M180[0])):
#    hMassSignal[i].Add(M180[0][i].Clone())
#    hMassSignal[i].Add(M200[0][i].Clone())
#    hMassSignal[i].Add(M220[0][i].Clone())
#    hMassSignal[i].Add(M300[0][i].Clone())


cuts = [ [ "b0t0tau21L", zerobtag+"&"+zerotop+"&"+tau21L ], 
         [ "b0t0tau21T", zerobtag+"&"+zerotop+"&"+tau21T ],
         [ "b1t0tau21L", onebtag+"&"+zerotop+"&"+tau21L ], 
         [ "b1t0tau21T", onebtag+"&"+zerotop+"&"+tau21T ],
         [ "b2t0", twobtag+"&"+zerotop+"&"+tau21N ],
         [ "b0t1", zerobtag+"&"+onetop+"&"+tau21N ],
         [ "b1t1", onebtag+"&"+onetop+"&"+tau21N ],
         [ "b2t1", twobtag+"&"+onetop+"&"+tau21N ],
         [ "b0t2", zerobtag+"&"+twotop+"&"+tau21N ],
         [ "b1t2", onebtag+"&"+twotop+"&"+tau21N ],
         [ "b2t2", twobtag+"&"+twotop+"&"+tau21N ]
         ]

C = TCanvas("C","",800,800)
C.Divide(3,4)
C.cd(1)
M180[0][0].DrawNormalized("hist")
for x in xrange(len(cuts)):
    C.cd(x+1)
    if M180[0][x].Integral() != 0: M180[0][x].Scale(1/M180[0][x].Integral())
    if M200[0][x].Integral() != 0:     M200[0][x].Scale(1/M200[0][x].Integral())
    if M220[0][x].Integral() != 0:     M220[0][x].Scale(1/M220[0][x].Integral())
    if M300[0][x].Integral() != 0:     M300[0][x].Scale(1/M300[0][x].Integral())

    FindAndSetMax( [M180[0][x],M200[0][x],M220[0][x],M300[0][x]], False )

    M180[0][x].DrawNormalized("samehist")
    M200[0][x].DrawNormalized("samehist")
    M220[0][x].DrawNormalized("samehist")
    M300[0][x].DrawNormalized("samehist")
#    hMassSignal[x].GetXaxis().SetTitle("Pruned Average Mass [GeV]")
#    hMassSignal[x].GetYaxis().SetTitle("N Events/10 GeV")
#    hMassSignal[x].Draw()
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.07)
    latex.SetTextAlign(13)
    latex.DrawLatex( .12, .88, cuts[x][0] )
    CMS_lumi.extraText = "Simulation Preliminary"
    CMS_lumi.relPosX = 0.13
    CMS_lumi.CMS_lumi( gPad, 4, 0 )
C.cd(x+2)
latex.SetNDC()
latex.SetTextSize(0.07)
latex.SetTextAlign(12)
latex.DrawLatex( .05, .5, "RPV Stop UDD323 M-180, 200, 220, 300" )
#C.SaveAs("TCutPlots/SigMassAve_ResVeto.png")
C.SaveAs("TCutPlots/SigMassAve.png")

ABCD = M180[1].Clone()
ABCD.Reset()
ABCD.Add(M180[1])
ABCD.Add(M200[1])
ABCD.Add(M220[1])
ABCD.Add(M300[1])

C1 = TCanvas("C1", "", 800, 800 )
C1.cd()
L1 = TLine( .1, 0, .1, 5)
L1.SetLineWidth(2)
L2 = TLine( 0, 1.0, 1, 1.0)
L2.SetLineWidth(2)
ABCD.GetXaxis().SetTitle("Pruned Mass Asymmetry")
ABCD.GetYaxis().SetTitle("Delta Eta Dijet")
ABCD.GetYaxis().SetTitleOffset(1.2)
CMS_lumi.extraText = "Simulation Preliminary"
CMS_lumi.relPosX = 0.14
#hABCDQCD.SetLineColor(kBlue)
ABCD.Draw("CONT3")
#M180[1].Draw("CONT3")
#M200[1].Draw("CONT3same")
#M220[1].Draw("CONT3same")
#M300[1].Draw("CONT3same")
L1.Draw("same")
L2.Draw("same")
latex = TLatex()
latex.SetNDC()
latex.SetTextSize(0.03)
latex.SetTextAlign(12)
latex.DrawLatex( .23, .8, "RPV Stop UDD323 M-180, 200, 220, 300" )
CMS_lumi.CMS_lumi( C1, 4, 0 )
#hABCDQCD.Draw("CONT3")

total = 0
A = 0
B = 0
C = 0
D = 0
for binX in xrange(1, ABCD.GetXaxis().GetNbins()+1 ):
    for binY in xrange(1, ABCD.GetYaxis().GetNbins()+1 ):
        total = total + ABCD.GetBinContent(binX, binY)
        massAsym = ABCD.GetXaxis().GetBinCenter(binX)<0.1
        dEta = ABCD.GetYaxis().GetBinCenter(binY)<1.0
        if massAsym and dEta: A = A+ABCD.GetBinContent(binX, binY)
        if massAsym and (not dEta): B = B+ABCD.GetBinContent(binX, binY)
        if (not massAsym) and dEta: C = C+ABCD.GetBinContent(binX, binY)
        if (not massAsym) and (not dEta): D = D+ABCD.GetBinContent(binX, binY)
        
int = TLatex()
int.SetNDC()
int.SetTextSize(0.02)
int.DrawLatex( .40, .55, "Fraction A: " + '{:0.2e}'.format(float(A/total)) )
int.DrawLatex( .40, .60, "Fraction B: " + '{:0.2e}'.format(float(B/total)) )
int.DrawLatex( .60, .55, "Fraction C: " + '{:0.2e}'.format(float(C/total)) )
int.DrawLatex( .60, .60, "Fraction D: " + '{:0.2e}'.format(float(D/total)) )

C1.SaveAs("TCutPlots/ABCDSig.png")

