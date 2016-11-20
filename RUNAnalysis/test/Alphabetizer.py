#
import os
import math
from array import array
import optparse
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
import RUNA.RUNAnalysis.Plotting
from RUNA.RUNAnalysis.Plotting import *

# Setting basic distributions
weight = "2666*puWeight*lumiWeight"

DATA = DIST( "DATA", "RootFiles/RUNAnalysis_JetHT_Run2015D-16Dec2015-v1_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", "1" )
QCD = DIST( "QCD", "RootFiles/RUNAnalysis_QCDPtAll_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", weight+"*.77" )
SIG = DIST( "SIG", "RootFiles/RUNAnalysis_RPVStopStopToJets_UDD323_M-100_RunIISummer16MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", weight )
TTJets = DIST( "TTJets", "RootFiles/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", weight )
WJets = DIST( "WJets", "RootFiles/RUNAnalysis_WJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", weight )
WW = DIST( "WW", "RootFiles/RUNAnalysis_WWTo4Q_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", weight )
WZ = DIST( "WZ", "RootFiles/RUNAnalysis_WZ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", weight )
ZZ = DIST( "ZZ", "RootFiles/RUNAnalysis_ZZTo4Q_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", weight )
ZJets = DIST( "ZJets", "RootFiles/RUNAnalysis_ZJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", weight )

# Creating Alphabet objects to run estimate on

DistsQCD = [ QCD ]
Dists = [ QCD, TTJets, WJets, WW, WZ, ZZ, ZJets ]
DistsData = [ DATA ]
DistsSub = [ WW, WZ, ZZ, ZJets, WJets, TTJets ]
DistsNothing = []

## Average mass binned fit
EstMass = Alphabet( "BkgEstMass", Dists, DistsNothing )
EstMassData = Alphabet( "BkgEstMassData", DistsData, DistsSub )
EstMass1 = Alphabet( "BkgEstMass1", Dists, DistsNothing )

var_arrayMass = [ "prunedMassAve", "prunedMassAsym", 12, 50., 350., 20, 0., 1. ] # For making B,D plot

#### Makes list with bins for fit
binsMass = []
binWidth = 25
NBins = int(((var_arrayMass[4] - var_arrayMass[3]))/binWidth)
#diff = (float(500))/20

for i in xrange( 0, NBins ):
    binsMass.append( [ var_arrayMass[3]+binWidth*i, var_arrayMass[3]+binWidth*(i+1) ] )
print binsMass

#### Form of fit
FMass = SigmoidFit([ 1.733,.7634,-3.516e-07,0,0 ],60,350,"Mass","MIRS")
FMass1 = SigmoidFit([ 1.7,.76,-3.5e-07,0,0 ],60,350,"Mass1","SEMR")
#FMass = SigmoidFit([ 1.829,.3742,-3.046e-07,0,0 ],60,350,"Mass","MIRS")
#FMass1 = SigmoidFit([ 1.829,.3742,-3.046e-07,0,0 ],60,350,"Mass1","SEMR")

#FMass = CubicFit([ 0,0,0,0,0 ],50,350,"Mass","SEMR")
#FMass1 = CubicFit([ -0.1,-0.1,-0.1,-0.1,-0.1 ],50,350,"Mass1","SEMR")

## HT binned fit
EstHT = Alphabet( "BkgEstHT", Dists, DistsSub )
EstHTData = Alphabet( "BkgEstHTData", DistsData, DistsSub )
EstHT1 = Alphabet( "BkgEstHT1", Dists, DistsSub )

var_arrayHT = [ "HT", "prunedMassAsym", 35, 900., 10000., 20, 0., 1. ] # For making B,D plot

#### Makes list with bins for fit
binsHT = []
diff = (float(var_arrayHT[4] - var_arrayHT[3]))/var_arrayHT[2]
for i in xrange( 0, var_arrayHT[2] ):
    binsHT.append( [ var_arrayHT[3]+diff*i, var_arrayHT[3]+diff*(i+1) ] )

#### Form of fit
FHT = CubicFit([.7432,-0.0007489,3.731e-07,-5.84e-11],900,10000,"quadraticfitHT","")
FHT1 = CubicFit([0,0,0,0],900,10000,"quadraticfitHT1","")

# Setting cuts
#presel = "jet1Tau21<0.6&jet2Tau21<0.6&(subjet11btagCSVv2>0.800||subjet12btagCSVv2>0.800)&(subjet21btagCSVv2>0.800||subjet22btagCSVv2>0.800)"
presel = "jet1Tau21<0.45&jet2Tau21<0.45"

tag = presel + "&prunedMassAsym<0.1&deltaEtaDijet<1.5" # Defines A region
antitag = presel + "&prunedMassAsym>0.1&deltaEtaDijet<1.5" # Defines C region
tagB = presel + "&prunedMassAsym<0.1&deltaEtaDijet>1.5"
tagD = presel + "&prunedMassAsym>0.1&deltaEtaDijet>1.5"
cut = [ 0.1, "<" ] # For defining B vs D regions
center = 0 # Where to center 2D plot

# Bins for final estimation plot
binBoundaries = []
for i in xrange( 60, 351 ):
    if i%5 == 0: binBoundaries.append(i)

MakeFitPlots( EstMass, FMass, binsMass, "prunedMassAve", "Pruned Mass Asymmetry", var_arrayMass, presel, "deltaEtaDijet>1.5", tagB, tagD, cut, center, EstMass1, FMass1, False )
#MakeEstPlots( EstMass, "prunedMassAve", "Average Mass", binBoundaries, antitag, tag, "prunedMassAve", EstMass1, False )

#MakeFitPlots( EstHT, FHT, binsHT, "HT", "Pruned Mass Asymmetry", var_arrayHT, presel, "deltaEtaDijet>1.0", cut, center, "", "", False )
#MakeEstPlots( EstHT, "prunedMassAve", "Average Mass", binBoundaries, antitag, tag, "HT", "", False )
