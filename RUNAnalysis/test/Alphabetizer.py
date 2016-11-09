#
import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy

# Our functions:
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

# Samples
DATA = DIST( "DATA", "RootFiles/RUNAnalysis_JetHT_Run2015D-16Dec2015-v1_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", "1" )
QCD = DIST( "QCD", "RootFiles/RUNAnalysis_QCDPtAll_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", "2666*puWeight*lumiWeight*.77" )
SIG = DIST( "SIG", "RootFiles/RUNAnalysis_RPVStopStopToJets_UDD323_M-100_RunIISummer16MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", "2666*puWeight*lumiWeight" )
TTJets = DIST( "TTJets", "RootFiles/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", "2666*puWeight*lumiWeight" )
WJets = DIST( "WJets", "RootFiles/RUNAnalysis_WJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", "2666*puWeight*lumiWeight" )
WW = DIST( "WW", "RootFiles/RUNAnalysis_WWTo4Q_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", "2666*puWeight*lumiWeight" )
WZ = DIST( "WZ", "RootFiles/RUNAnalysis_WZ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", "2666*puWeight*lumiWeight" )
ZZ = DIST( "ZZ", "RootFiles/RUNAnalysis_ZZTo4Q_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", "2666*puWeight*lumiWeight" )
ZJets = DIST( "ZJets", "RootFiles/RUNAnalysis_ZJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", "2666*puWeight*lumiWeight" )

# Samples to run estimation on
Dists = [ QCD, TTJets, WJets, WW, WZ, ZZ, ZJets ]
DistsData = [ DATA ]
#Dists = [ QCD ]

# Initialize Alphabetizer Objects for differently binned transfer functions
EstMass = Alphabetizer( "BkgEstMass", Dists, [] ) # Average Mass binned
EstMass1 = Alphabetizer( "BkgEstMassData", DistsData, [] ) # For data ave mass binned bkg est

EstPt = Alphabetizer( "BkgEstPt", Dists, [] ) # Sum leading jet pt binned

EstHT = Alphabetizer( "BkgEstHT", Dists, [] ) # HT binned
EstHT1 = Alphabetizer( "BkgEstHTData", DistsData, [] ) # For data HT binned

# Cuts for defining ABCD regions
presel = "jet1Tau21<0.6&jet2Tau21<0.6&(subjet11btagCSVv2>0.800||subjet12btagCSVv2>0.800)&(subjet21btagCSVv2>0.800||subjet22btagCSVv2>0.800)"
#presel = "jet1Tau21<0.6&jet2Tau21<0.6"
tag = presel + "&prunedMassAsym<0.1&deltaEtaDijet<1.0"
antitag = presel + "&prunedMassAsym>0.1&deltaEtaDijet<1.0"

# Cuts for defining ABCD regions -- btag defined
#presel = "jet1Tau21<0.6&jet2Tau21<0.6&prunedMassAsym<0.1&deltaEtaDijet<1.0"
#btagCutJet1 = "(subjet11btagCSVv2>0.800||subjet12btagCSVv2>0.800)"
#btagCutJet2 = "(subjet21btagCSVv2>0.800||subjet22btagCSVv2>0.800)"
#tag = presel + "&" + btagCutJet1 + "&" + btagCutJet2
#antitag = presel + "&" + btagCutJet1 + "&!" + btagCutJet2

# for 2D ABCD plot
#var_arrayMass = [ "massAve", "floor((subjet11btagCSVv2-0.800))+floor((subjet12btagCSVv2-0.800))", 6, 50., 350., 8, -4., 4. ] # for b-tag defined ABCD - possible buggy
var_arrayMass = [ "massAve", "prunedMassAsym", 12, 50., 350., 20, 0., 1. ]
var_arrayPt = [ "jet1Pt+jet2Pt", "prunedMassAsym", 34, 100., 2000., 20, 0., 1. ]
var_arrayHT = [ "HT", "prunedMassAsym", 21, 900., 5100., 20, 0., 1. ]

#Defines B vs D regions
cut = [ 0.1, "<" ]

binsMass = [[50,75],[75,100],[100,125],[125,150],[150,175],[175,200],[200,225],[225,250],[250,275],[275,300],[300,325],[325,350]]
binsHT = [ [900,1100],[1100,1300],[1300,1500],[1500,1700],[1700,1900],[1900,2100], [2100,2300],[2300,2500],[2500,2700],[2700,2900],[2900,3100], [3100,3300],[3300,3500],[3500,3700],[3700,3900],[3900,4100],[4100,4300],[4300,4500],[4500,4700],[4700,4900],[4900,5100] ]
binsPt = [[600,650],[650,700],[700,750],[750,800],[800,850],[850,900],[900,950],[950,1000],[1050,1100],[1100,1150],[1150,1200],[1200,1250],[1250,1300],[1300,150],[1350,1400],[1400,1450],[1450,1500],[1500,1550],[1550,1600],[1600,1650],[1650,1700],[1700,1750],[1750,1800],[1800,1850],[1850,1900],[1900,1950],[1950,2000]]

truthbins = []
center = 0

# Transfer functions, initialized with Ale's values, option "R" runs on range
FMass = SigmoidFit([1.7, .76, -3.5e-07 ],50,350,"Mass","R")
FMass1 = SigmoidFit([1.7, .76, -3.5e-07 ],50,350,"Mass1","R")
#FMass = CubicFit([-0.01, -0.01, 0.0 ],50,350,"Mass","R")
FHT = CubicFit([-0.01, -0.01,0,0.],900,5000,"cubicfitHT","R")
FHT1 = CubicFit([-0.01, -0.01,0,0.],900,5000,"cubicfitHT1","R")
FPt = CubicFit([3.72297e-01, -1.14569e-04,-0.01,0.],600,2000,"cubicfitPt","R")


#for Est in [ [EstMass, FMass, binsMass, "MassAve", var_arrayMass], [EstPt, FPt, binsPt, "ptSum", var_arrayPt], [EstHT, FHT, binsHT, "HT", var_arrayHT] ]: # For looping over different Transfer functions -- DOESN'T WORK YET

# How to bin transfer function
# 6th and 7th list items for data background estimation
# Used to make the data_obs plot without unblinding
for Est in [ [EstMass1, FMass, binsMass, "MassAve", var_arrayMass, EstMass, FMass1 ] ]: # Ave Mass
#for Est in [ [EstPt, FPt, binsPt, "ptSum", var_arrayPt] ]: # Sum Pt
#for Est in [ [EstHT1, FHT, binsHT, "HT", var_arrayHT, EstHT, FHT1] ]: # HT

    Est[0].SetRegions( Est[4], presel+"&deltaEtaDijet>1.0")
    Est[5].SetRegions( Est[4], presel+"&deltaEtaDijet>1.0") # For data_obs plot with data bkg est

#    Est[0].SetRegions( Est[4], presel+"&!"+btagCutJet2)

    Est[0].TwoDPlot.SetStats(0)
    C1 = TCanvas("C1", "", 800, 600)
    C1.cd()
    Est[0].TwoDPlot.Draw("COLZ")
    Est[0].TwoDPlot.GetXaxis().SetTitle(Est[3]+" [GeV]")
    Est[0].TwoDPlot.GetYaxis().SetTitle("Pruned Mass Asymmetry")
    C1.SaveAs("outputs/"+Est[3]+"Est_2D.png")


    Est[0].GetRates(cut, Est[2], truthbins, center, Est[1])
    Est[5].GetRates(cut, Est[2], truthbins, center, Est[6]) # For data_obs plot with data bkg est
    leg = TLegend(0.11,0.6,0.4,0.8)
    leg.SetLineColor(0)
    leg.SetFillColor(4001)
    leg.SetTextSize(0.03)
    leg.AddEntry(Est[0].G, "events used in fit", "PLE")
    leg.AddEntry(Est[0].Fit.fit, "fit", "L")
    leg.AddEntry(Est[0].Fit.ErrUp, "fit errors", "L")
    leg.AddEntry
    C2 = TCanvas("C2", "", 800, 800)
    C2.cd()
    Est[0].G.SetTitle("")
    Est[0].G.Draw("AP")
    Est[0].G.GetXaxis().SetTitle(Est[3]+" (GeV)")
    Est[0].G.GetYaxis().SetTitle("R_{p/f}")
    Est[0].G.GetYaxis().SetTitleOffset(1.3)
    gStyle.SetOptFit()
    Est[0].Fit.fit.Draw("same")
    Est[0].Fit.ErrUp.SetLineStyle(2)
    Est[0].Fit.ErrUp.Draw("same")
    Est[0].Fit.ErrDn.SetLineStyle(2)
    Est[0].Fit.ErrDn.Draw("same")
    leg.Draw()
    C2.SaveAs("outputs/"+Est[3]+"Est_Fit.png")


    variable = "massAve"
    
    binBoundaries = [50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125,130,135,140,145,150,155,160,165,170,175,180,185,190,195,200,205,210,215,220,225,230,235,240,245,250,255,260,265,270,275,280,285,290,295,300,305,310,315,320,325,330,335,340,345,350]
#binBoundaries = [50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260,270,280,290,300,310,320,330,340,350]
#binBoundaries = [50,70,90,110,130,150,170,190,210,230,250,270,290,310,330,350]


    Est[0].MakeEstVariable(variable, binBoundaries, antitag, tag)
    Est[5].MakeEstVariable(variable, binBoundaries, antitag, tag) # For data_obs plot with data bkg est
    FILE = TFile("outputs/"+Est[3]+"Est.root", "RECREATE")
    FILE.cd()
    V = TH1F("data_obs", "", len(binBoundaries)-1, array('d',binBoundaries))
    VStack = THStack("data_obs", "")
    for i in (Est[5]).hists_MSR: # Makes data_obs from MC bkgs - no unblinding
        i.Sumw2()
        i.SetStats(0)
        V.Add(i)
        VStack.Add(i)
    
# the estimate is the sum of the histograms in self.hists_EST and self.hist_MSR_SUB
    N = TH1F("EST", "", len(binBoundaries)-1, array('d',binBoundaries))
    for i in Est[0].hists_EST:
        N.Add(i,1.)
# We can do the same thing for the Up and Down shapes:
    NU = TH1F("EST_CMS_scale_13TeVUp", "", len(binBoundaries)-1, array('d',binBoundaries)) 
    for i in Est[0].hists_EST_UP:
        NU.Add(i,1.)
    ND = TH1F("EST_CMS_scale_13TeVDown", "", len(binBoundaries)-1, array('d',binBoundaries)) 
    for i in Est[0].hists_EST_DN:
        ND.Add(i,1.)
    A =  TH1F("EST_Antitag", "", len(binBoundaries)-1, array('d',binBoundaries)) 
    for i in Est[0].hists_ATAG:
        A.Add(i,1.)

    for bin in range(0,len(binBoundaries)-1):
        if not A.GetBinContent(bin+1) > 0.:
            print A.GetBinError(bin+1)
    A.SetBinError(bin+1, 2.0)
    A.SetBinContent(bin+1, 0.001)
    N.SetBinContent(bin+1,0.0001)
    ND.SetBinContent(bin+1,0.00001)
    NU.SetBinContent(bin+1,0.001)

    FILE.Write()
    FILE.Save()

    vartitle = "Average Mass (GeV)"

    NU.SetLineColor(kBlack)
    ND.SetLineColor(kBlack)
    NU.SetLineStyle(2)
    ND.SetLineStyle(2)
    N.SetLineColor(kBlack)
    N.SetFillColor(kPink+3)



    V.SetStats(0)
    V.Sumw2()
    V.SetLineColor(1)
    V.SetFillColor(0)
    V.SetMarkerColor(1)
    V.SetMarkerStyle(20)
#V.SetLin(4)
    N.GetYaxis().SetTitle("events")
    N.GetXaxis().SetTitle(vartitle)

    FindAndSetMax([V,N, NU, ND])
    Pull = V.Clone("Pull")
    Pull.Add(N, -1.)

    Boxes = []
    sBoxes = []
    pBoxes = []
    maxy = 0.
    for i in range(1, N.GetNbinsX()+1):
        P = Pull.GetBinContent(i)
        Ve = V.GetBinError(i)
        if Ve > 1.:
            Pull.SetBinContent(i, P/Ve)
        Pull.SetBinError(i, 1.)
        if A.GetBinContent(i)==0:
            a = 0
        else:
            a = A.GetBinError(i)*N.GetBinContent(i)/A.GetBinContent(i)
        u = NU.GetBinContent(i) - N.GetBinContent(i)
        d = N.GetBinContent(i) - ND.GetBinContent(i)
        x1 = Pull.GetBinCenter(i) - (0.5*Pull.GetBinWidth(i))
        y1 = N.GetBinContent(i) - math.sqrt((d*d) + (a*a))
        s1 = N.GetBinContent(i) - a
        if y1 < 0.:
            y1 = 0
        if s1 < 0:
            s1 = 0
        x2 = Pull.GetBinCenter(i) + (0.5*Pull.GetBinWidth(i))
        y2 = N.GetBinContent(i) + math.sqrt((u*u) + (a*a))
        s2 = N.GetBinContent(i) + a
        if maxy < y2:
            maxy = y2
        if Ve > 1.:
            yP1 = -math.sqrt((d*d) + (a*a))/Ve
            yP2 = math.sqrt((u*u) + (a*a))/Ve
        else:
            yP1 = -math.sqrt((d*d) + (a*a))
            yP2 = math.sqrt((u*u) + (a*a))
        tempbox = TBox(x1,y1,x2,y2)
        temppbox = TBox(x1,yP1,x2,yP2)
        tempsbox = TBox(x1,s1,x2,s2)
        Boxes.append(tempbox)
        sBoxes.append(tempsbox)
        pBoxes.append(temppbox)

    Pull.GetXaxis().SetTitle("")
    Pull.SetStats(0)
    Pull.SetLineColor(1)
    Pull.SetFillColor(0)
    Pull.SetMarkerColor(1)
    Pull.SetMarkerStyle(20)
    Pull.GetXaxis().SetNdivisions(0)
    Pull.GetYaxis().SetNdivisions(4)
    Pull.GetYaxis().SetTitle("#frac{MC - Data Est}{#sigma_{MC}}")
    Pull.GetYaxis().SetLabelSize(85/15*Pull.GetYaxis().GetLabelSize())
    Pull.GetYaxis().SetTitleSize(4.2*Pull.GetYaxis().GetTitleSize())
    Pull.GetYaxis().SetTitleOffset(0.175)
    Pull.GetYaxis().SetRangeUser(-3.,3.)

    for i in Boxes:
        i.SetFillColor(12)
        i.SetFillStyle(3244)
    for i in pBoxes:
        i.SetFillColor(12)
        i.SetFillStyle(3144)
    for i in sBoxes:
        i.SetFillColor(38)
        i.SetFillStyle(3002)

    leg2 = TLegend(0.6,0.6,0.89,0.89)
    leg2.SetLineColor(0)
    leg2.SetFillColor(0)
    leg2.AddEntry(V, "MC Backgrounds", "PL")
    leg2.AddEntry(N, "Data background prediction", "F")
    leg2.AddEntry(Boxes[0], "total uncertainty", "F")
    leg2.AddEntry(sBoxes[0], "background statistical component", "F")


    T0 = TLine(800,0.,4509,0.)
    T0.SetLineColor(kBlue)
    T2 = TLine(800,2.,4509,2.)
    T2.SetLineColor(kBlue)
    T2.SetLineStyle(2)
    Tm2 = TLine(800,-2.,4509,-2.)
    Tm2.SetLineColor(kBlue)
    Tm2.SetLineStyle(2)
    
    T1 = TLine(800,1.,4509,1.)
    T1.SetLineColor(kBlue)
    T1.SetLineStyle(3)
    Tm1 = TLine(800,-1.,4509,-1.)
    Tm1.SetLineColor(kBlue)
    Tm1.SetLineStyle(3)
    
    C4 = TCanvas("C4", "", 800, 800)
#draw the lumi text on the canvas
    
    plot = TPad("pad1", "The pad 80% of the height",0,0.15,1,1)
    pull = TPad("pad2", "The pad 20% of the height",0,0,1.0,0.15)
    plot.Draw()
    pull.Draw()
    plot.cd()
    N.SetMinimum(0.01)
    V.SetMinimum(0.01)
    N.Draw("Hist")
    V.Draw("same E0")
    plot.SetLogy()
    for i in Boxes:
        i.Draw("same")
    for i in sBoxes:
        i.Draw("same")
    leg2.Draw()
    pull.cd()
    Pull.Draw("")
    for i in pBoxes:
        i.Draw("same")
    T0.Draw("same")
    T2.Draw("same")
    Tm2.Draw("same")
    T1.Draw("same")
    Tm1.Draw("same")
    Pull.Draw("same")
    C4.SaveAs("outputs/"+Est[3]+"Est_Plot.png")
    
    print str(N.Integral())
    print str(V.Integral())
