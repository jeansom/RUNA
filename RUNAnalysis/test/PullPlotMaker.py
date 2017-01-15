#
import os
import math
from array import array
import optparse
import argparse
import ROOT
from ROOT import *
import scipy
import random
from scipy.stats import chisqprob

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
import RUNA.RUNAnalysis.Plotting
from RUNA.RUNAnalysis.Plotting import *

def PullPlotMaker( chan, chanCuts, bins, minBin, maxBin, Xcut, Ycut, isMC=True ):
    gStyle.SetOptStat(0)
    # Setting basic distributions
    weight = "2666*puWeight*lumiWeight"
    DATA = DIST( "DATA", "RootFiles/RUNAnalysis_JetHT_Run2015D-16Dec2015-v1_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", "1" )
    QCD = DIST( "QCD", "RootFiles/RUNAnalysis_QCDPtAll_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", weight )
    SIG = DIST( "SIG", "RootFiles/RUNAnalysis_RPVStopStopToJets_UDD323_M-100_RunIISummer16MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", weight )
    TTJets = DIST( "TTJets", "RootFiles/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", weight+"*((1.06)*exp(-0.0005*HT/2))" )
    TTJetsUp = DIST( "TTJetsUp", "RootFiles/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", weight+"*((1.06 + .5)*exp(-0.0005*HT/2))" )
    TTJetsDn = DIST( "TTJetsDn", "RootFiles/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", weight+"*((1.06 - 0.5)*exp(-0.0005*HT/2))" )
#    TTJets = DIST( "TTJets", "RootFiles/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", weight+"*((1))" )
#    TTJetsUp = DIST( "TTJetsUp", "RootFiles/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", weight+"*((1 + .5))" )
#    TTJetsDn = DIST( "TTJetsDn", "RootFiles/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", weight+"*((1 - 0.5))" )
    WJets = DIST( "WJets", "RootFiles/RUNAnalysis_WJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*(1))" )
    WJetsUp = DIST( "WJetsUp", "RootFiles/RUNAnalysis_WJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*(1 + 0.5))" )
    WJetsDn = DIST( "WJetsDn", "RootFiles/RUNAnalysis_WJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*(1 - 0.5))" )
    WW = DIST( "WW", "RootFiles/RUNAnalysis_WWTo4Q_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", weight )
    WZ = DIST( "WZ", "RootFiles/RUNAnalysis_WZ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", weight )
    ZZ = DIST( "ZZ", "RootFiles/RUNAnalysis_ZZTo4Q_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", weight )
    ZJets = DIST( "ZJets", "RootFiles/RUNAnalysis_ZJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", weight )
    Sig = DIST( "Sig", "RootFiles/RUNAnalysis_RPVStopStopToJets_UDD323_M-100_RunIISummer16MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", weight )

    # Creating Alphabet objects to run estimate on    
    if isMC: 
        Dists = [ QCD, TTJets, WJets, WW, WZ, ZZ, ZJets ]
    else: 
        Dists = [DATA]
    DistsSub = [ WJets, TTJets ]
    print random.random()
    print str(Dists)
    ## Defining Cuts
    presel = "jet1Tau21<0.6&jet2Tau21<0.6"
    cuts = "prunedMassAsym<0.1&deltaEtaDijet<1.0"
    anticuts = Xcut[0]+">"+Xcut[1]+"&"+Ycut[0]+"<"+Ycut[1]
    cutsB = Xcut[0]+"<"+Xcut[1]+"&"+Ycut[0]+">"+Ycut[1]
    cutsD = "prunedMassAsym>0.1&deltaEtaDijet>1.0"
    cut = [ float(Xcut[1]), "<" ] # For defining B vs D regions
    
    ## Average mass binned fit
    EstMass = Alphabet( "BkgEstMass", Dists, DistsSub )
    EstMassWJUp = Alphabet( "BkgEstMassWJUp", Dists, [WJetsUp, TTJets] )
    EstMassWJDn = Alphabet( "BkgEstMassWJDn", Dists, [WJetsDn, TTJets] )
    EstMassTTUp = Alphabet( "BkgEstMassTTUp", Dists, [WJets, TTJetsUp] )
    EstMassTTDn = Alphabet( "BkgEstMassTTDn", Dists, [WJets, TTJetsDn] )

    
    #### Makes list with bins for fit
    binsMass = []
    binWidth = 25
#    if "b1t1" in chan or "b1t2" in chan:
#        binWidth = 50
    NBins = int(((350-50))/binWidth)
    var_arrayMass = [ "prunedMassAve", Xcut[0], NBins, 50., 350., Xcut[2], Xcut[3], Xcut[4] ] # For making B,D plot
    
    for i in xrange( 0, NBins ):
        binsMass.append( [ var_arrayMass[3]+binWidth*i, var_arrayMass[3]+binWidth*(i+1) ] )
#    print binsMass
        
    #### Form of fit
    FMass = SigmoidFit([ 1.733,.7634,-3.516e-07,0,0 ],60,350,"Mass","SEMR")
    FMass1 = SigmoidFit([ 1.733,.7634,-3.516e-07,0,0 ],60,350,"Mass1","SEMR")
    FMassWJUp = SigmoidFit([ 1.733,.7634,-3.516e-07,0,0 ],60,350,"Mass","SEMR")
    FMassWJDn = SigmoidFit([ 1.733,.7634,-3.516e-07,0,0 ],60,350,"Mass","SEMR")
    FMassTTUp = SigmoidFit([ 1.733,.7634,-3.516e-07,0,0 ],60,350,"Mass","SEMR")
    FMassTTDn = SigmoidFit([ 1.733,.7634,-3.516e-07,0,0 ],60,350,"Mass","SEMR")

#    FMass = LinearFit([0,0,0,0,0],60,350,"Mass","SEMR")
#    FMass1 = LinearFit([0,0,0,0,0],60,350,"Mass1","SEMR")
#    FMassWJUp = LinearFit([0,0,0,0,0],60,350,"Mass","SEMR")
#    FMassWJDn = LinearFit([0,0,0,0,0],60,350,"Mass","SEMR")
#    FMassTTUp = LinearFit([0,0,0,0,0],60,350,"Mass","SEMR")
#    FMassTTDn = LinearFit([0,0,0,0,0],60,350,"Mass","SEMR")


#    FMass = SigmoidFit([0.1,0.1,0.1,0.1,0.1],60,350,"Mass","SEMR")
#    FMass1 = SigmoidFit([0.1,0.1,0.1,0.1,0.1],60,350,"Mass1","SEMR")
#    FMassWJUp = SigmoidFit([0.1,0.1,0.1,0.1,0.1],60,350,"Mass","SEMR")
#    FMassWJDn = SigmoidFit([0.1,0.1,0.1,0.1,0.1],60,350,"Mass","SEMR")
#    FMassTTUp = SigmoidFit([0.1,0.1,0.1,0.1,0.1],60,350,"Mass","SEMR")
#    FMassTTDn = SigmoidFit([0.1,0.1,0.1,0.1,0.1],60,350,"Mass","SEMR")

    # Bins for final estimation plot
    binBoundaries = []
    for i in xrange( 60, 351 ):
        if i%10 == 0: binBoundaries.append(i)

    # Use alternate channel's fits when low statistics
    if chan is "b0t2": chanCutsTemp = zerobtag+"&"+oneTop
    elif chan is "b1t2": chanCutsTemp = onebtag+"&"+oneTop
    elif chan is "b2t1": chanCutsTemp = twobtag+"&"+zeroTop
    elif chan is "b2t2": chanCutsTemp = twobtag+"&"+zeroTop
    else: chanCutsTemp = chanCuts
#    if "t0" in chan: chanCutsTemp = zeroTop
#    elif "t1" in chan: chanCutsTemp = oneTop
#    elif "t2" in chan: chanCutsTemp = twoTop
    #chanCutsTemp = "jet1btagCSVv2>-999999999999999999999"
    Pull = TH1D()
    MakeFitPlots( EstMass, FMass, binsMass, "prunedMassAve", Xcut[0], var_arrayMass, presel+"&"+chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "", "outputs/Mass"+chan, False )
    pBoxes = MakeEstPlots( EstMass, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/Mass"+chan, False, Pull )
    print(Pull)
    fitMetric = Pull.Clone()
    fitMetric.Reset()

    for i in range(1, Pull.GetNbinsX()+1):
        error = pBoxes[i].GetY1() - pBoxes[i].GetY2()
        fitMetric.SetBinContent( i, Pull.GetBinContent(i)/abs(error) )

    return fitMetric


parser = argparse.ArgumentParser()
parser.add_argument( '-c', '--channel', action='store', dest='channel', default=1, help='Channel')
try:
    args = parser.parse_args()
    print "here"
except:
    parser.print_help()
    sys.exit(0)

channel = args.channel
print channel

zerobtag = "(jet1btagCSVv2<0.800&jet2btagCSVv2<0.800)"
onebtag = "((jet1btagCSVv2<0.800&jet2btagCSVv2>0.800)||(jet1btagCSVv2>0.800&jet2btagCSVv2<0.800))"
twobtag = "(jet1btagCSVv2>0.800&jet2btagCSVv2>0.800)"
jet1btag = "((jet1btagCSVv2>0.800&jet2btagCSVv2<0.800))"
jet2btag = "((jet1btagCSVv2<0.800&jet2btagCSVv2>0.800))"

zeroTop = "(jet1Tau32>0.51&jet2Tau32>.51)"
oneTop = "((jet1Tau32<=0.51&jet2Tau32>=0.51)||(jet1Tau32>0.51&jet2Tau32<0.51))"
twoTop = "(jet1Tau32<0.51&jet2Tau32<0.51)"
jet1Top = "((jet1Tau32>0.51&jet2Tau32<0.51))"
jet2Top = "((jet1Tau32<0.51&jet2Tau32>0.51))"

Xcut = [ "prunedMassAsym", "0.1", 20, 0., 1. ]
Ycut = [ "deltaEtaDijet", "1.0", 20, 0., 5. ]
isMC = True

PullPlots = []
PullPlots.append( [ PullPlotMaker( "b0t0", zerobtag+"&"+zeroTop, 29, 60, 350, Xcut, Ycut, isMC ), "Zero btags, Zero top-tags" ] )
PullPlots.append( [ PullPlotMaker( "b1t0", onebtag+"&"+zeroTop, 29, 60, 350, Xcut, Ycut, isMC ), "One btag, Zero top-tags" ] )
PullPlots.append( [ PullPlotMaker( "b2t0", twobtag+"&"+zeroTop, 29, 60, 350, Xcut, Ycut, isMC ), "Two btags, Zero top-tags" ] )
PullPlots.append( [ PullPlotMaker( "b0t1", zerobtag+"&"+oneTop, 29, 60, 350, Xcut, Ycut, isMC ), "Zero btags, One top-tag" ] )
PullPlots.append( [ PullPlotMaker( "b1t1", onebtag+"&"+oneTop, 29, 60, 350, Xcut, Ycut, isMC ), "One btag, One top-tag" ] )
PullPlots.append( [ PullPlotMaker( "b2t1", twobtag+"&"+oneTop, 29, 60, 350, Xcut, Ycut, isMC ), "Two btags, One top-tag" ] )
PullPlots.append( [ PullPlotMaker( "b0t2", zerobtag+"&"+twoTop, 29, 60, 350, Xcut, Ycut, isMC ), "Zero btags, Two top-tags" ] )
PullPlots.append( [ PullPlotMaker( "b1t2", onebtag+"&"+twoTop, 29, 60, 350, Xcut, Ycut, isMC ), "One btag, Two top-tags" ] )
PullPlots.append( [ PullPlotMaker( "b2t2", twobtag+"&"+twoTop, 29, 60, 350, Xcut, Ycut, isMC ), "Two btags, Two top-tags" ] )

C = TCanvas( "C", "", 800, 800 )
C.Divide(3,3)
for i in xrange(len(PullPlots)):
    C.cd(i)
    PullPlots[i][0].Draw()
    
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.01)
    latex.SetTextAlign(13)
    latex.DrawLatex( .6, .8, PullPlots[i][1] )
    latex.DrawLatex( .63, .76, "Int. Pull/Uncertainty: " + PullPlots[i][0].Integral() )

C.SaveAs( "outputs/PullPlotMetric.png" )

