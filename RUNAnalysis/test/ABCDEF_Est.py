#
import os
import math
from array import array
import optparse
import argparse
import ROOT
from ROOT import *
import scipy

import RUNA.RUNAnalysis.Plotting_Header
from RUNA.RUNAnalysis.Plotting_Header import *
import RUNA.RUNAnalysis.scaleFactors
from RUNA.RUNAnalysis.scaleFactors import *
import RUNA.RUNAnalysis.CMS_lumi as CMS_lumi
import RUNA.RUNAnalysis.ABCDEF_Functions
from RUNA.RUNAnalysis.ABCDEF_Functions import *
import RUNA.RUNAnalysis.ABCDEF_Ester
from RUNA.RUNAnalysis.ABCDEF_Ester import *
import RUNA.RUNAnalysis.ABCDEF_Draw
from RUNA.RUNAnalysis.ABCDEF_Draw import *

# Runs New Estimate 2.0, messy and complicated, has memory problems probably because of arrays
### F: Function to fit
### NAME: name
### NAMEF: other name
### deta: other eta bins
### useFile: If you just ran with the same parameters, cuts..., the arrays were saved in a python file, so you can just use that instead of rerunning
def RunEst(F, NAME, NAMEF, masses, deta, useFile):
    # Defines some histos
    EST = TH1F("EST", "", 60, 50, 350)
    ESTSUB = TH1F("ESTSUB", "", 60, 50, 350)
    EST.SetStats(0)
    EST.SetFillColor(kAzure-4)
    EST.SetLineColor(kBlack)
    EST.GetYaxis().SetTitle("Events / 5 GeV")
    EST.GetXaxis().SetLabelSize(0)
    EST.GetXaxis().SetTitle("")
    EST.GetYaxis().SetTitleOffset(1.365)

    DATA = TH1F("DATA", "", 60, 50, 350)
    DATASUB = []
    DATA.SetStats(0)
    DATA.SetLineColor(kBlack)
    DATA.SetMarkerColor(kBlack)
    DATA.SetMarkerStyle(8)
    DATA.GetXaxis().SetTitle("Average Soft Drop Mass [GeV]")
    DATA.GetYaxis().SetTitle("Events / 5 GeV")
    DATA.GetXaxis().SetTitleOffset(1.3)
    DATA.GetYaxis().SetTitleOffset(1.365)
    
    # makes histos, make sure to check cuts here
    for i in Dists:
        quickplot(i.File, "BoostedAnalysisPlots/RUNATree", DATA, "prunedMassAve", "jet1Tau21<0.45&jet2Tau21<0.45&numJets==2&deltaEtaDijet<1.5&prunedMassAsym<0.1", i.weight)
        quickplot(i.File, "BoostedAnalysisPlots/RUNATree", EST, "prunedMassAve", "jet1Tau21<0.45&jet2Tau21<0.45&numJets==2&deltaEtaDijet<1.5&prunedMassAsym>0.1", i.weight)
    for i in DistsSub:
        DATASUB.append(TH1F("DATASUB", "", 60, 50, 350))
        quickplot(i.File, "BoostedAnalysisPlots/RUNATree", DATASUB[-1], "prunedMassAve", "jet1Tau21<0.45&jet2Tau21<0.45&numJets==2&deltaEtaDijet<1.5&prunedMassAsym<0.1", i.weight)
        quickplot(i.File, "BoostedAnalysisPlots/RUNATree", ESTSUB, "prunedMassAve", "jet1Tau21<0.45&jet2Tau21<0.45&numJets==2&deltaEtaDijet<1.5&prunedMassAsym>0.1", i.weight)

    EST.Add(ESTSUB,-1)

    DATA.Sumw2()
    if len(DATASUB)==3:
        DATASUB[0].SetFillColor(6)
        DATASUB[1].SetFillColor(8)
        DATASUB[2].SetFillColor(2)
    
    # Get B/D
    if not useFile: ABCDEF_Est(Dists, DistsSub, masses, deta)
    from ABCDEF_Est_output import ML, EHL, ELL, VL, TL, TEHL, TELL
    Bins, BinnedTF, BinnedTFT = [], [], []

    
    for i in xrange(len(ML)): 
        AppendMultiple( [Bins, BinnedTF, BinnedTFT], [(float((ML[i][0]+ML[i][1])/2)), VL[i], TL[i]] )
    EXL, EXH = [], []
    for M in ML: AppendMultiple( [EXL, EXH], [(float((M[1]-M[0])/2.)), (float((M[1]-M[0])/2.))] )

    # Transfer factors
    G = TGraphAsymmErrors((len(Bins)), scipy.array(Bins), scipy.array(BinnedTF), scipy.array(EXL), scipy.array(EXH), scipy.array(ELL), scipy.array(EHL))
    G2 = TGraphAsymmErrors((len(Bins)), scipy.array(Bins), scipy.array(BinnedTFT), scipy.array(EXL), scipy.array(EXH), scipy.array(TELL), scipy.array(TEHL))
    CFUP = TGraph( len(Bins), scipy.array(Bins), numpy.add( BinnedTF, EHL ) )
    CFDN = TGraph( len(Bins), scipy.array(Bins), numpy.subtract( BinnedTF, ELL ) )

    G.SetMarkerSize(1.5)
    G2.SetMarkerSize(1.5)
    G2.SetMarkerColor(kBlue)
    G2.SetLineColor(kBlue)
    G2.SetLineWidth(2)
    G.SetMarkerStyle(21)
    G.SetTitle("")
    G.GetXaxis().SetTitle("Average Mass")
    G.GetYaxis().SetTitle("R_{p/f}")
    G.GetYaxis().SetTitleOffset(1.3)

    D = "exp( [1] + [2]*x*x )"
    Q = "(1/([0] + "+D+"))"
    fitR = TFitResultPtr(G.Fit(F,"SEMREX0ROB"))
    FitUp, FitDn = FitErrors( Bins, F, fitR )
    
    chi2 = DrawG(G, G2, F, FitUp, FitDn, NAME, NAMEF)

    # Make final estimate
    ESTUP = EST.Clone("ESTUP")
    ESTDN = EST.Clone("ESTDN")
    A = EST.Clone("A")
    RATIO = DATA.Clone("AOverC")
    RATIO.Divide(A)
    for bin in xrange(1, A.GetNbinsX()+1):
        A.SetBinContent(bin, EST.GetBinContent(bin))
    for i in xrange(1, EST.GetNbinsX()+1):
        mass = EST.GetXaxis().GetBinCenter(i)
        EST.SetBinContent(i, EST.GetBinContent(i)*F.Eval(mass))
        ESTUP.SetBinContent(i, ESTUP.GetBinContent(i)*FitUp.Eval(mass))
        ESTDN.SetBinContent(i, ESTDN.GetBinContent(i)*FitDn.Eval(mass))

    StackEst = THStack("stack","")
    for i in DATASUB:
        StackEst.Add(i)
        ESTUP.Add(i)
        ESTDN.Add(i)
    StackEst.Add(EST)
    Pull2 = DATA.Clone("Pull2")
    Pull2.Add(EST,-1)
    Pull = DATA.Clone("Pull")
    Pull.Divide(EST)

    Boxes, sBoxes, pBoxes = PullErrors(EST, Pull2, DATA, ESTUP, ESTDN, A)

    # Draws and save estimate
    DrawEst( StackEst, EST, DATA, Boxes, pBoxes, sBoxes, Pull, Pull2, NAME, NAMEF )
    N = EST.Clone("N")
    for i in DATASUB:
        N.Add(i)
    return chi2, F, EST

# Defines distributions
weight = "(36555.21/15*lumiWeight*puWeight)"
TTScaleStr = "1.06*exp(-0.0005*HT/2)"
WScaleStr = "1"
TopScaleStr = "1"

rootFiles = "80XRootFilesUpdated/"

DATA = DIST( "DATA", "v08/RUNAnalysis_JetHT_Run2016_80X_V2p4_v08_cut15_pruned.root", "BoostedAnalysisPlots/RUNATree", "1" )

QCDHT = DIST( "QCDHT", "v08/RUNAnalysis_QCDHTAll_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", ".62*puWeight*36555.21/15*lumiWeight")
QCDPT = DIST( "QCDPT", "v08/RUNAnalysis_QCDPtAll_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", ".62*puWeight*36555.21/15*lumiWeight")
TTJets = DIST( "TTJets", rootFiles+"/RUNAnalysis_TT_PtRewt_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*"+TTScaleStr+")" )
WJets = DIST( "WJets", rootFiles+"/RUNAnalysis_WJetsToQQ_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree",  "("+weight+"*"+WScaleStr+")" )
Top = DIST( "Top", rootFiles+"/RUNAnalysis_ST_t-channel_topantitop_4f_inclusiveDecays_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree",  "("+weight+"*"+TopScaleStr+")" )

Dists = [QCDPT]
DistsSub = []
FILE = TFile( "TCutPlots/TFs.root", "RECREATE" )
FILE.cd()
masses = []
i = 50
while i < 200:
    masses.append([i,i+25])
    i=i+25
masses.append([200,275])
masses.append([275,350])

D = "exp( [1] + [2]*x*x*x )"
Q = "(1/([0] + "+D+"))"

Fsigmoidcube = TF1("sigmoidcube", Q, 50, 350)
Fsigmoidcube.SetParameters(2., 1., 0.)

detaBins = [ [1.5,1.99999], [2.0, 2.9999], [3.0, 5.0] ]

chi2sigcube, FSigCube, EstSigCube = RunEst(Fsigmoidcube, "Sigmoid (x^{3})", "sigmoidcube", masses, detaBins, False)






# Ran Est with other functions, made comparison plots
# Has memory problems, I wouldn't recommend running. Write separate script instead?
'''
Fatan = TF1("atan", "[0]+[1]*atan([2]*x-[3])", 50, 350)
Fatan.SetParameters(0., 0., 0., 0.)

Flogistic = TF1("logistic", "[0]/(1 + exp(-[1]*(x-[2])))", 50, 350)
Flogistic.SetParameters(0.6, 0.006, 150.)

D = "exp( [1] + [2]*x*x )"
Q = "(1/([0] + "+D+"))"

Fsigmoidsquare = TF1("sigmoidsquare", Q, 50, 350)
Fsigmoidsquare.SetParameters(2., 1., 0.)

chi2atan, FAtan, EstAtan = RunEst(Fatan, "Arctan", "arctan", masses, detaBins, True)
chi2log, FLog, EstLog = RunEst(Flogistic, "Logistic", "logistic", masses, detaBins, True)
chi2sigsqu, FSigSqu, EstSigSqu = RunEst(Fsigmoidsquare, "Sigmoid (x^{2})", "sigmoidsquare", masses, detaBins, True)

EstAtan.SetLineColor(kBlack)
EstAtan.SetLineWidth(2)
EstAtan.SetFillColor(0)
EstSigCube.SetLineColor(kGreen)
EstSigCube.SetFillColor(0)
EstSigCube.SetLineWidth(2)
EstSigSqu.SetLineColor(kBlue)
EstSigSqu.SetFillColor(0)
EstSigSqu.SetLineWidth(2)
EstLog.SetLineColor(kRed)
EstLog.SetFillColor(0)
EstLog.SetLineWidth(2)

C = TCanvas("C4", "", 800, 800)
EstAtan.GetXaxis().SetTitle("Average Soft Drop Mass")
EstAtan.GetYaxis().SetTitle("Events / 5")
EstAtan.Draw("hist")
EstSigCube.Draw("samehist")
EstSigSqu.Draw("samehist")
EstLog.Draw("samehist")

leg = TLegend(.5,.70,.89,.89)
leg.SetLineColor(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.AddEntry(EstAtan, "Estimate with arctan fit", "L")
leg.AddEntry(EstSigSqu, "Estimate with Sigmoid (x^{2}) fit", "L")
leg.AddEntry(EstSigCube, "Estimate with Sigmoid (x^{3}) fit", "L")
leg.AddEntry(EstLog, "Estimate with logistic fit", "L")
leg.Draw("same")
CMS_lumi.extraText = "Simulation Preliminary"
CMS_lumi.relPosX = 0.14
CMS_lumi.CMS_lumi(C, 4, 0)
C.SaveAs("TCutPlots/FitEstComp.png")

C2 = TCanvas("C2", "", 650, 650)
C2.cd()
FAtan.SetLineColor(kBlack)
FAtan.SetLineWidth(2)
FSigCube.SetLineColor(kGreen)
FSigCube.SetLineWidth(2)
FSigSqu.SetLineColor(kBlue)
FSigSqu.SetLineWidth(2)
FLog.SetLineColor(kRed)
FLog.SetLineWidth(2)
FAtan.Draw()
FSigCube.Draw("same")
FSigSqu.Draw("same")
FLog.Draw("same")
leg = TLegend(.11,.70,.40,.89)
leg.SetNColumns(1)
leg.SetLineColor(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.AddEntry(FAtan, "Arctan Fit, " +chi2atan, "PL")
leg.AddEntry(FSigSqu, "Sigmoid (x^{2}) Fit, "+chi2sigsqu, "PL")
leg.AddEntry(FSigCube, "Sigmoid (x^{3}) Fit, "+chi2sigcube, "PL")
leg.AddEntry(FLog, "Logistic Fit, "+chi2log, "PL")
leg.Draw("same")
C2.SaveAs("TCutPlots/FitComp.png")
'''
