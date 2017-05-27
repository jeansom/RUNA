#
import os
import math
from array import array
import optparse
import argparse
import ROOT
from ROOT import *
import scipy

import RUNA.RUNAnalysis.Alphabet_Header
from RUNA.RUNAnalysis.Alphabet_Header import *
import RUNA.RUNAnalysis.Plotting_Header
from RUNA.RUNAnalysis.Plotting_Header import *
import RUNA.RUNAnalysis.Converters
from RUNA.RUNAnalysis.Converters import *
import RUNA.RUNAnalysis.Distribution_Header
from RUNA.RUNAnalysis.Distribution_Header import *
import RUNA.RUNAnalysis.Alphabet
from RUNA.RUNAnalysis.Alphabet import *
import RUNA.RUNAnalysis.scaleFactors
from RUNA.RUNAnalysis.scaleFactors import *
import RUNA.RUNAnalysis.CMS_lumi as CMS_lumi
import RUNA.RUNAnalysis.ABCDEF_EstMaker
from RUNA.RUNAnalysis.ABCDEF_EstMaker import *

weight = "(36555.21/15*lumiWeight*puWeight)"
TTScaleStr = "1.06*exp(-0.0005*HT/2)"
WScaleStr = "1"
TopScaleStr = "1"

rootFiles = "80XRootFilesUpdated/"

DATA = DIST( "DATA", rootFiles+"/RUNAnalysis_JetHT_Run2016_80X_V2p3_v06_cut15.root", "BoostedAnalysisPlotsPuppi/RUNATree", "1" )

QCDHT = DIST( "QCDHT", "v08/RUNAnalysis_QCDHTAll_80X_V2p4_v08.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".62*puWeight*36555.21/15*lumiWeight")
QCDPT = DIST( "QCDPT", "v08/RUNAnalysis_QCDPtAll_80X_V2p4_v08.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".66*puWeight*36555.21/15*lumiWeight")
QCD = []
for i in [ "QCDPt170to300", "QCDPt300to470", "QCDPt470to600", "QCDPt600to800", "QCDPt800to1000", "QCDPt1000to1400", "QCDPt1400to1800", "QCDPt1800to2400", "QCDPt2400to3200", "QCDPt3200toInf" ]:
    QCD.append( DIST( i, rootFiles + "/RUNAnalysis_"+i+"_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*"+weight+"*"+str(scaleFactor(i))))
TTJets = DIST( "TTJets", rootFiles+"/RUNAnalysis_TT_PtRewt_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "("+weight+"*"+TTScaleStr+")" )
WJets = DIST( "WJets", rootFiles+"/RUNAnalysis_WJetsToQQ_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree",  "("+weight+"*"+WScaleStr+")" )
Top = DIST( "Top", rootFiles+"/RUNAnalysis_ST_t-channel_topantitop_4f_inclusiveDecays_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree",  "("+weight+"*"+TopScaleStr+")" )

Dists = [QCDHT]
#DistsSub = [Top,WJets,TTJets]
DistsSub = []
FILE = TFile( "TCutPlots/TFs.root", "RECREATE" )
FILE.cd()

EST = TH1F("EST", "", 60, 50, 350)
ESTSUB = TH1F("ESTSUB", "", 60, 50, 350)
EST.SetStats(0)
EST.SetFillColor(kAzure-4)
EST.SetLineColor(kBlack)
#EST.GetXaxis().SetTitle("Average Soft Drop Mass [GeV]")
EST.GetYaxis().SetTitle("Events / 5 GeV")
#EST.GetXaxis().SetTitleOffset(1.3)
EST.GetXaxis().SetLabelSize(0)
EST.GetXaxis().SetTitle("")
EST.GetYaxis().SetTitleOffset(1.365)
for i in Dists:
    quickplot(i.File, "BoostedAnalysisPlotsPuppi/RUNATree", EST, "prunedMassAve", "jet1Tau21<0.45&jet2Tau21<0.45&numJets==2&deltaEtaDijet<1.5&prunedMassAsym>0.1", i.weight)
for i in DistsSub:
    quickplot(i.File, "BoostedAnalysisPlotsPuppi/RUNATree", ESTSUB, "prunedMassAve", "jet1Tau21<0.45&jet2Tau21<0.45&numJets==2&deltaEtaDijet<1.5&prunedMassAsym>0.1", i.weight)
EST.Add(ESTSUB,-1)
DATA = TH1F("DATA", "", 60, 50, 350)
DATASUB = []
DATA.SetStats(0)
DATA.SetLineColor(kBlack)
DATA.SetMarkerColor(kBlack)
DATA.SetMarkerStyle(8)
DATA.GetXaxis().SetTitle("Average Soft Drop Mass [GeV]")
DATA.GetYaxis().SetTitle("Events / 10 GeV")
DATA.GetXaxis().SetTitleOffset(1.3)
DATA.GetYaxis().SetTitleOffset(1.365)
for i in Dists:
    quickplot(i.File, "BoostedAnalysisPlotsPuppi/RUNATree", DATA, "prunedMassAve", "jet1Tau21<0.45&jet2Tau21<0.45&numJets==2&deltaEtaDijet<1.5&prunedMassAsym<0.1", i.weight)
for i in DistsSub:
    DATASUB.append(TH1F("DATASUB", "", 60, 50, 350))
    quickplot(i.File, "BoostedAnalysisPlotsPuppi/RUNATree", DATASUB[-1], "prunedMassAve", "jet1Tau21<0.45&jet2Tau21<0.45&numJets==2&deltaEtaDijet<1.5&prunedMassAsym<0.1", i.weight)

for bin in xrange(1, DATA.GetNbinsX()+1):
    DATA.SetBinContent(bin, DATA.GetBinContent(bin))

if len(DATASUB)==3:
    DATASUB[0].SetFillColor(6)
    DATASUB[1].SetFillColor(8)
    DATASUB[2].SetFillColor(2)

AL, CL, VL, TL, TEHL, TELL1, EHL, ELL, ML = ABCDEF_Est()
Bins = []
BinnedTF = []
BinnedTFT = []
for i in xrange(len(ML)):
    Bins.append(float((ML[i][0]+ML[i][1])/2))
    BinnedTF.append(VL[i])
    BinnedTFT.append(TL[i])

EXL = []
EXH = []
for M in ML:
    EXL.append(float((M[1]-M[0])/2.))
    EXH.append(float((M[1]-M[0])/2.))
print Bins
G = TGraphAsymmErrors((len(Bins)), scipy.array(Bins), scipy.array(BinnedTF), scipy.array(EXL), scipy.array(EXH), scipy.array(ELL), scipy.array(EHL))
G2 = TGraphAsymmErrors((len(Bins)), scipy.array(Bins), scipy.array(BinnedTFT), scipy.array(EXL), scipy.array(EXH), scipy.array(TELL1), scipy.array(TEHL))
CFUP = TGraph( len(Bins), scipy.array(Bins), numpy.add( BinnedTF, EHL ) )
CFDN = TGraph( len(Bins), scipy.array(Bins), numpy.subtract( BinnedTF, ELL ) )
G.Write("BOverDMass")
G2.Write("BOverDMassOld")
G.SetMarkerSize(1.5)
G2.SetMarkerSize(1.5)
G2.SetMarkerColor(kBlue)
G2.SetLineColor(kBlue)
G2.SetLineWidth(2)
G.SetMarkerStyle(21)
G.SetTitle("")
G.GetXaxis().SetTitle("Average Mass")
G.GetYaxis().SetTitle("R_{p/f}")
#F = TF1("f", "[0]/(1 + exp(-[1]*(x - [2])))",50,350)
D = "exp( [1] + [2]*x*x )"
Q = "(1/([0] + "+D+"))"
F = TF1("f", "[0]+[1]*atan([2]*x-[3])", 50, 350)
F.SetParameters(0.4,0.1,0.,150.)

fitR = TFitResultPtr(G.Fit(F,"SEMR"))
listBinCenter = []
fitErrors = []
fitValues = []
for i in Bins:
    binCenter = float(i)
    listBinCenter.append(float(binCenter))
    err = array('d',[0])
    fitR.GetConfidenceIntervals( 1, 1, 1, array('d', [binCenter]), err, 0.683, False )
    fitErrors.append(float(err[0]))
    fitValues.append(float(F.Eval(binCenter)))

FitUp = TGraph( len(fitValues), array('d', listBinCenter ), numpy.add( fitValues, fitErrors ) )
FitDn = TGraph( len(fitValues), array('d', listBinCenter ), numpy.subtract( fitValues, fitErrors ) )

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
FILE.Write()
FILE.Save()
StackEst = THStack("stack","")
for i in DATASUB:
    StackEst.Add(i)
StackEst.Add(EST)
for i in DATASUB:
    ESTUP.Add(i)
    ESTDN.Add(i)

Pull2 = DATA.Clone("Pull2")
Pull2.Add(EST,-1)

Boxes = []
sBoxes = []
pBoxes = []
maxy = 0.

for i in range(1, EST.GetNbinsX()+1):
    P = Pull2.GetBinContent(i)
    Ve = DATA.GetBinError(i)
    Pull2.SetBinError(i,1.)
    u = ESTUP.GetBinContent(i)-EST.GetBinContent(i)
    d = EST.GetBinContent(i)-ESTDN.GetBinContent(i)
    if A.GetBinContent(i)==0: 
        a = 0
    else:
        a = A.GetBinError(i)*EST.GetBinContent(i)/A.GetBinContent(i) # othe
    print d
    print u
    y1 = EST.GetBinContent(i) - math.sqrt((d*d)+(a*a))
    y2 = EST.GetBinContent(i) + math.sqrt((u*u)+(a*a))
    x1 = EST.GetBinCenter(i) - (0.5*EST.GetBinWidth(i))
    x2 = EST.GetBinCenter(i) + (0.5*EST.GetBinWidth(i))

    s1 = EST.GetBinContent(i) - a
    if s1 < 0: s1 = 0
    s2 = EST.GetBinContent(i) + a
    if maxy < y2:
        maxy = y2
    if Ve > 1.:
        yP1 = -math.sqrt((d*d) + (a*a))/Ve # Bottom of pull error
        yP2 = math.sqrt((u*u) + (a*a))/Ve # Top of pull error
    else:
        yP1 = -math.sqrt((d*d) + (a*a)) # Bottom of pull error
        yP2 = math.sqrt((u*u) + (a*a)) # Top of pull error
    if Ve > 1:
        Pull2.SetBinContent( i, P/Ve ) # Filling normal pull


    tempbox = TBox(x1, y1, x2, y2)
    Boxes.append(tempbox)
    tempbox = TBox(x1,y1,x2,y2)
    temppbox = TBox(x1,yP1,x2,yP2)
    tempsbox = TBox(x1,s1,x2,s2)
    Boxes.append(tempbox)
    sBoxes.append(tempsbox)
    pBoxes.append(temppbox)
Pull2.GetXaxis().SetTitle("Average Mass [GeV]")
Pull2.SetStats(0)
Pull2.SetLineColor(1)
Pull2.SetFillColor(0)
Pull2.SetMarkerColor(1)
Pull2.SetMarkerStyle(20)
Pull2.GetYaxis().SetNdivisions(4)
Pull2.GetYaxis().SetTitle("#frac{QCD MC - Est}{#sigma_{MC}}")
Pull2.GetYaxis().SetLabelSize(55/15*Pull2.GetYaxis().GetLabelSize())
Pull2.GetYaxis().SetTitleSize(3.5*Pull2.GetYaxis().GetTitleSize())
Pull2.GetYaxis().SetTitleOffset(0.20)
Pull2.GetYaxis().SetRangeUser(-5,5.)
Pull2.GetXaxis().SetLabelSize(.12)
Pull2.GetXaxis().SetTitleSize(.12)

for i in Boxes:
    i.SetFillColor(12)
    i.SetFillStyle(3244)
for i in pBoxes:
    i.SetFillColor(9)
    i.SetFillStyle(3144)
for i in sBoxes:
    i.SetFillColor(12)
    i.SetFillStyle(3002)

import RUNA.RUNAnalysis.Plotting_Header
from RUNA.RUNAnalysis.Plotting_Header import *

FindAndSetMax([StackEst,DATA],False)

C = TCanvas("C", "", 650, 650)
C.cd()
plot = TPad("pad1", "The pad 80% of the height",0,0.3,1,1)
pull = TPad("pad2", "The pad 20% of the height",0,0.20,1.0,0.30)
pull2 = TPad("pad3", "The pad 20% of the height",0,0.,1.0,0.20)
plot.Draw()
plot.SetBottomMargin(0)
pull.SetTopMargin(0)
pull.SetBottomMargin(0.)
pull2.SetTopMargin(0)
pull2.SetBottomMargin(0.3)
plot.Draw()
pull.Draw()
pull2.Draw()
plot.cd()

StackEst.Draw("hist")
StackEst.GetXaxis().SetTitle("")
StackEst.GetYaxis().SetTitle("Events / 5 GeV")
StackEst.GetXaxis().SetLabelSize(0)

for i in Boxes:
    i.Draw("same")
for i in sBoxes:
    i.Draw("same")

DATA.Sumw2()
DATA.SetLineWidth(2)
DATA.Draw("sameE0")

leg = TLegend(.35,.70,.89,.89)
leg.SetNColumns(2)
leg.SetLineColor(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)

leg.AddEntry(DATA, "QCD MC", "PL")
leg.AddEntry(EST, "QCD Est from QCD MC", "F")
leg.Draw("same")

CMS_lumi.extraText = "Simulation Preliminary"
CMS_lumi.relPosX = 0.14
CMS_lumi.CMS_lumi(plot, 4, 0)

plot.RedrawAxis()

pull.cd()
Pull = DATA.Clone("Pull")
Pull.Divide(EST)
Pull.GetXaxis().SetTitle("")
Pull.SetLineColor(1)
Pull.SetFillColor(0)
Pull.SetMarkerColor(1)
Pull.SetMarkerStyle(20)
Pull.GetYaxis().SetNdivisions(4)
Pull.GetYaxis().SetTitle("#frac{MC}{Est}")
Pull.GetYaxis().SetLabelSize(55/15*Pull.GetYaxis().GetLabelSize())
Pull.GetYaxis().SetTitleSize(5.5*Pull.GetYaxis().GetTitleSize())
Pull.GetYaxis().SetTitleOffset(0.25)
Pull.GetYaxis().SetRangeUser(0,2.)
Pull.GetXaxis().SetLabelSize(.12)
Pull.GetXaxis().SetTitleSize(.14)
T01=TLine(50,1,350,1)
T01.SetLineColor(kRed)
Pull.Draw()
T01.Draw("same")
Pull.Draw("same")
pull2.cd()
Pull2.Draw()
for i in pBoxes:
    i.Draw("same")
T0 = TLine(50,0.,350,0.)
T0.SetLineColor(kRed)
T0.SetLineWidth(2)
T2 = TLine(50,2.,350,2.)
T2.SetLineColor(kRed)
T2.SetLineStyle(2)
T2.SetLineWidth(2)
Tm2 = TLine(50,-2.,350,-2.)
Tm2.SetLineColor(kRed)
Tm2.SetLineStyle(2)
Tm2.SetLineWidth(2)
T1 = TLine(50,1.,350,1.)
T1.SetLineColor(kRed)
T1.SetLineStyle(3)
T1.SetLineWidth(2)
Tm1 = TLine(50,-1.,350,-1.)
Tm1.SetLineColor(kRed)
Tm1.SetLineStyle(3)
Tm1.SetLineWidth(2)

T0.Draw("same")
T2.Draw("same")
Tm2.Draw("same")
T1.Draw("same")
Tm1.Draw("same")
Pull2.Draw("same")

C.SaveAs("TCutPlots/EstEtaBins.png")

C2 = TCanvas("C2", "", 650, 650)
C2.cd()

chi2Test = '#chi^{2}/ndF = '+ str( round( ComputeChi2(G, F), 2 ) )+'/'+str( int( F.GetNDF() ))


G.Draw("AP")
FitUp.SetLineColor(kRed)
FitUp.SetLineStyle(2)
FitUp.SetLineWidth(2)
FitDn.SetLineColor(kRed)
FitDn.SetLineColor(kRed)
FitDn.SetLineStyle(2)
FitDn.SetLineWidth(2)
FitUp.Draw("PC")
FitDn.Draw("PC")
F.SetLineColor(kRed)
F.SetLineWidth(2)
F.Draw("same")
G2.Draw("PL")
leg = TLegend(.11,.70,.40,.89)
leg.SetNColumns(1)
leg.SetLineColor(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.AddEntry(G, "Extrapolated B/D", "PL")
leg.AddEntry(G2, "Old B/D", "PL")
leg.AddEntry(F, "Arctan Fit, " + chi2Test, "L")
leg.Draw("same")
CMS_lumi.CMS_lumi(C2, 4, 0)
C2.RedrawAxis()
C2.SaveAs("TCutPlots/TFEtaBins.png")

C3 = TCanvas( "C3", "", 800, 800 )
C3.cd()
FILE1 = TFile.Open("TCutPlots/TFs.root")
N = FILE1.Get("EST")
#for i in DATASUB:
#    N.Add(i)
FILE = TFile.Open("outputs/5217/MCBCD/9_0CBDMC/Masspres_prunedMassAveEst.root")
ESTOLD = FILE.Get("EST")
ESTOLD.SetLineColor(kRed)
N.SetLineColor(kAzure-4)
N.SetFillColor(0)
N.GetXaxis().SetTitle("Average Mass [GeV]")
FindAndSetMax([N, ESTOLD], False)
N.Draw("hist")
DATA.Draw("E0same")
ESTOLD.Draw("histsame")
leg2 = TLegend(.35,.70,.89,.89)
leg2.SetNColumns(2)
leg2.SetLineColor(0)
leg2.SetFillColor(0)
leg2.SetFillStyle(0)
leg2.AddEntry(N, "New Estimate", "L")
leg2.AddEntry(ESTOLD, "Old Estimate", "L")
leg2.Draw("same")

C3.SaveAs("TCutPlots/EstComp.png")
