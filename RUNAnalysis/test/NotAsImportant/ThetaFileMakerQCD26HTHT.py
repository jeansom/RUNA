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
import RUNA.RUNAnalysis.scaleFactors
from RUNA.RUNAnalysis.scaleFactors import *

def ThetaFileMaker( chan, scaleName, chanCuts, bins, minBin, maxBin, Xcut, Ycut, tau21, prelimFit, fitBins, HT, Dists, DistsSub, DistSig, isMC=True, log=True ):
    gStyle.SetOptStat(0)
    # Setting basic distributions

    ## Defining Cuts
    presel = tau21
    cuts = Xcut[0]+"<"+Xcut[1]+"&"+Ycut[0]+"<"+Ycut[1]
    anticuts = Xcut[0]+">"+Xcut[1]+"&"+Ycut[0]+"<"+Ycut[1]
    cutsB = Xcut[0]+"<"+Xcut[1]+"&"+Ycut[0]+">"+Ycut[1]
    cutsD = Xcut[0]+">"+Xcut[1]+"&"+Ycut[0]+">"+Ycut[1]
    cut = [ float(Xcut[1]), "<" ] # For defining B vs D regions
    
    ## Average mass binned fit
    EstMass = Alphabet( "BkgEstMass", Dists, DistsSub, DistSig ) # Nominal

    #### Makes list with bins for fit
    binsMass = []
    binWidth = 205
    NBins = int(((5000-900))/binWidth)
    var_arrayMass = [ "HT", Xcut[0], NBins, 900., 5000., Xcut[2], Xcut[3], Xcut[4] ] # For making B,D plot
    for i in xrange( 0, NBins ):
        binsMass.append( [ var_arrayMass[3]+binWidth*i, var_arrayMass[3]+binWidth*(i+1) ] )

    #### Form of fit
    FMass = SigmoidFit(prelimFit,900, 5000,"Mass","SEMR") # Nominal fit
    FMass1 = SigmoidFit(prelimFit, 900, 5000,"Mass1","SEMR") # Nominal fit again, used if staying blinded

    # Bins for final estimation plot, bin width int(bins)
    binBoundaries = []
    dBin = 100
    i = 900
    while i<3001:
        binBoundaries.append(i)
        i=i+dBin

    rhoBinBoundaries = []
    dBin = float(205)
    i = 900
    while i < 5001:
        rhoBinBoundaries.append(i)
        i = i+dBin

    # Use alternate channel's fits when low statistics
    if "t2" in chan: chanCutsTemp = presel+"&"+twoTop
    elif "b2t1" in chan: chanCutsTemp = presel+"&"+onebtag+"&"+oneTop
    else: chanCutsTemp = presel+"&"+chanCuts

    # Nominal
    MakeFitPlots( EstMass, FMass, binsMass, "HT", Xcut[0], var_arrayMass, chanCutsTemp, Ycut[0]+">"+Ycut[1], cut, 0, "", "", "outputs/"+directory+method+"/Mass"+chan+"_"+scaleName, binBoundaries, True, False ) # Creates the 2D plot, ratio, and ratio fit
    MakeEstPlots( EstMass, "HT", "HT", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/Mass"+chan+"_"+scaleName, rhoBinBoundaries, True, isMC, False, log ) # Makes the actual estimation

    # Makes root file with basic fits
    FITFILE = TFile( "outputs/"+directory+method+"/LIM_FIT"+chan+"_"+scaleName+".root", "RECREATE" )
    FITFILE.cd()
    
    FIT_Points = (EstMass.G).Clone("G_"+chan) # Ratio plot
    FIT = (EstMass.Fit.fit).Clone("Fit_"+chan) # Fit of ratio 
    FIT_Up = (EstMass.Fit.ErrUp).Clone("FitUp_"+chan) # Fit err up
    FIT_Dn = (EstMass.Fit.ErrDn).Clone("FitDn_"+chan) # Fit err dn

    FIT_Points.Write()
    FIT.Write()
    FIT_Up.Write()
    FIT_Dn.Write()

    FITFILE.Write()
    FITFILE.Save()

    # Makes histograms for the theta root file
    chan__DATA = EstMass.hists_EST[0].Clone(chan+"__DATA"+scaleName)
    chan__DATA.Reset()
    chan__QCD = EstMass.hists_EST[0].Clone(chan+"__QCD"+scaleName)
    chan__QCD.Reset()
    chan__TTBAR = EstMass.hists_EST[0].Clone(chan+"__TTBAR"+scaleName)
    chan__TTBAR.Reset()
    chan__WJETS = EstMass.hists_EST[0].Clone(chan+"__WJETS"+scaleName)
    chan__WJETS.Reset()
    chan__TOP = EstMass.hists_EST[0].Clone(chan+"__TOP"+scaleName)
    chan__TOP.Reset()

    for i in EstMass.hists_EST: # Adds the plus histograms into the nominal bkg est
        chan__QCD.Add( i, 1. )
    for i in EstMass.hists_EST_SUB: # Subtracts the minus histograms from the nominal bkg est DOES NOT ADD THE SIGNAL MINUS REGIONS BACK IN
        chan__QCD.Add( i, -1. )
    removeNegativeBins(chan__QCD)
    for i in EstMass.hists_MSR: # Adds the signal region plots together
        chan__DATA.Add(i)

    if len(DistsSub) > 2:
        quickplot( TTJets.File, TTJets.Tree, chan__TTBAR, "prunedMassAve", presel+"&"+cuts+"&"+chanCuts, TTJets.weight ) # Makes nominal T plot
        quickplot( WJets.File, WJets.Tree, chan__WJETS, "prunedMassAve", presel+"&"+cuts+"&"+chanCuts, WJets.weight ) # Makes nominal W plot
        quickplot( Top.File, Top.Tree, chan__TOP, "prunedMassAve", presel+"&"+cuts+"&"+chanCuts, Top.weight ) # Makes nominal W plot

    #### Opens theta root file for writing
    FILE = TFile( "outputs/"+directory+method+"/LIM_FEED"+chan+"_"+scaleName+".root", "RECREATE" )
    FILE.cd()
    #### Write plots to file    
    chan__DATA.Write()
    chan__QCD.Write()
    chan__TTBAR.Write()
    chan__TOP.Write()
    chan__WJETS.Write()
    ### Writes file
    FILE.Write()
    FILE.Save()
    
parser = argparse.ArgumentParser()
parser.add_argument( '-c', '--channel', action='store', dest='channel', default=1, help='Channel to run the estimation for')
parser.add_argument( '-s', '--scale', action='store', dest='scale', default=1, help='scale array')
parser.add_argument( '-m', '--method', action='store', dest='method', default="CBDCMVAv2MC", help='Method, B*(C/D)..., CMVA..., MC, Data...')
parser.add_argument( '-d', '--directory', action='store', dest='directory', default = "", help='Directory to save output in')
parser.add_argument( '-b', '--bins', action='store', dest='bins', default = 10, help='bin width for final estimation')
parser.add_argument( '-j', '--HT', action='store', dest='HT', default = "abs(HT)>-999", help='HT bin')
parser.add_argument( '-l', '--log', action='store', dest='log', default = "True", help='log')
parser.set_defaults(plot=True)
try:
    args = parser.parse_args()
except:
    parser.print_help()
    sys.exit(0)

channel = args.channel
plot = args.plot
method = args.method
directory = args.directory
bins = args.bins
HT = args.HT
scale = int(args.scale)
if "T" in args.log:
    log = True
else:
    log = False

os.mkdir("outputs/"+directory+method)

if scale == 1:
    scaleName = "_TTScale_Up"
    scaleArray = {'TopScale': [(0,0)], 'WJScale': [(0,0)], 'TTAlphaScale': [(0,0)], 'TTScale': [(0,1)]}
elif scale == 2:
    scaleName = "_TTScale_Dn"
    scaleArray = {'TopScale': [(0,0)], 'WJScale': [(0,0)], 'TTAlphaScale': [(0,0)], 'TTScale': [(0,-1)]}
elif scale == 3:
    scaleName = "_TTAlphaScale_Up"
    scaleArray = {'TopScale': [(0,0)], 'WJScale': [(0,0)], 'TTAlphaScale': [(0,1)], 'TTScale': [(0,0)]}
elif scale == 4:
    scaleName = "_TTAlphaScale_Dn"
    scaleArray = {'TopScale': [(0,0)], 'WJScale': [(0,0)], 'TTAlphaScale': [(0,-1)], 'TTScale': [(0,0)]}
elif scale == 5:
    scaleName = "_WJetsScale_Up"
    scaleArray = {'TopScale': [(0,0)], 'WJScale': [(0,1)], 'TTAlphaScale': [(0,0)], 'TTScale': [(0,0)]}
elif scale == 6:
    scaleName = "_WJetsScale_Dn"
    scaleArray = {'TopScale': [(0,0)], 'WJScale': [(0,-1)], 'TTAlphaScale': [(0,0)], 'TTScale': [(0,0)]}
elif scale == 7:
    scaleName = "_TopScale_Up"
    scaleArray = {'TopScale': [(0,1)], 'WJScale': [(0,0)], 'TTAlphaScale': [(0,0)], 'TTScale': [(0,0)]}
elif scale == 8:
    scaleName = "_TopScale_Dn"
    scaleArray = {'TopScale': [(0,-1)], 'WJScale': [(0,0)], 'TTAlphaScale': [(0,0)], 'TTScale': [(0,0)]}
elif scale == 9:
    scaleName = "_After"
    scaleArray = {'TopScale': [(0,0)], 'WJScale': [(0,0)], 'TTAlphaScale': [(0,0)], 'TTScale': [(0,0)]}
else:
    scaleName = ""
    scaleArray = {'TopScale': [(0,0)], 'WJScale': [(0,0)], 'TTAlphaScale': [(0,0)], 'TTScale': [(0,0)]}

# Sets the TT, W, and Alpha scales, plus their errors
scaleTT = scaleArray['TTScale'][0][0]
scaleTTErr = scaleArray['TTScale'][0][1]
scaleW = scaleArray['WJScale'][0][0]
scaleWErr = scaleArray['WJScale'][0][1]
scaleAlpha = scaleArray[ 'TTAlphaScale' ][0][0]
scaleAlphaErr = scaleArray[ 'TTAlphaScale' ][0][1]
scaleTop = scaleArray[ 'TopScale' ][0][0]
scaleTopErr = scaleArray[ 'TopScale' ][0][1]

zerobtag = "(jet1btagCSVv2<0.8484&jet2btagCSVv2<0.8484)"
onebtag = "((jet1btagCSVv2<0.8484&jet2btagCSVv2>0.8484)||(jet1btagCSVv2>0.8484&jet2btagCSVv2<0.8484))"
twobtag = "(jet1btagCSVv2>0.8484&jet2btagCSVv2>0.8484)"
jet1btag = "((jet1btagCSVv2>0.8484&jet2btagCSVv2<0.8484))"
jet2btag = "((jet1btagCSVv2<0.8484&jet2btagCSVv2>0.8484))"

zeroTop = "(jet1Tau32>0.67&jet2Tau32>.67)"
oneTop = "((jet1Tau32<=0.67&jet2Tau32>=0.67)||(jet1Tau32>0.67&jet2Tau32<0.67))"
twoTop = "(jet1Tau32<0.67&jet2Tau32<0.67)"
jet1Top = "((jet1Tau32>0.67&jet2Tau32<0.67))"
jet2Top = "((jet1Tau32<0.67&jet2Tau32>0.67))"

if "CBD" in method:
    Xcut = [ "prunedMassAsym", "0.1", 20, 0., 1. ]
    Ycut = [ "deltaEtaDijet", "1.5", 20, 0., 5. ]
elif "BCD" in method:
    Ycut = [ "prunedMassAsym", "0.1", 20, 0., 1. ]
    Xcut = [ "deltaEtaDijet", "1.5", 20, 0., 5. ]
else:
    print "Method not found: " +method
    sys.exit(0)

# The T and W scales
TTNorm = "( (1.06)*(1+.2*" + str(scaleTT) + "+.2*" + str(scaleTTErr) + ") )" # TTBar normalization
TTAlpha = "exp( (-0.0005*(HT/2))*(1-.2*" + str(scaleAlpha) + "-.2*" + str(scaleAlphaErr) + ") )" # Alpha NOTE: subtracting = adding because -0.0005

TTScaleStrNorm = "(1.06*exp( (-0.0005*(HT/2)) ))"
TTScaleStr = "(" + TTNorm + "*" + TTAlpha + ")" # Total string to scale TT by, norm*alpha
WScaleStr = "(1+.2*"+str(scaleW)+"+.2*"+str(scaleWErr)+")" # W scale
TopScaleStr = "(1+.2*"+str(scaleTop)+"+2*"+str(scaleTopErr)+")"

# Create the distributions
weight = "(36555.21/15)"

DATA = DIST( "DATA", "80XRootFilesUpdated/RUNAnalysis_JetHT_Run2016_80X_V2p3_v06_cut15.root", "BoostedAnalysisPlotsPuppi/RUNATree", "1" )
QCD = []
#for i in [ "QCDPt170to300", "QCDPt300to470", "QCDPt470to600", "QCDPt600to800", "QCDPt800to1000", "QCDPt1000to1400", "QCDPt1400to1800", "QCDPt1800to2400", "QCDPt2400to3200", "QCDPt3200toInf" ]:
for i in [ "QCDPt300to470", "QCDPt470to600", "QCDPt600to800", "QCDPt800to1000", "QCDPt1000to1400", "QCDPt1400to1800", "QCDPt1800to2400", "QCDPt2400to3200", "QCDPt3200toInf" ]:
    QCD.append( DIST( i, "80XRootFilesUpdated/RUNAnalysis_"+i+"_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*"+weight+"*"+str(scaleFactor(i)) ) )
TTJetsNorm = DIST( "TTJets", "80XRootFilesUpdated/RUNAnalysis_TT_PtRewt_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "("+weight+"*puWeight*lumiWeight*"+TTScaleStrNorm+")" )
TTJets = DIST( "TTJets", "80XRootFilesUpdated/RUNAnalysis_TT_PtRewt_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "("+weight+"*puWeight*lumiWeight*"+TTScaleStr+")" )
WJetsNorm = DIST( "WJets", "80XRootFilesUpdated/RUNAnalysis_WJetsToQQ_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree",  "("+weight+"*puWeight*lumiWeight)" )
WJets = DIST( "WJets", "80XRootFilesUpdated/RUNAnalysis_WJetsToQQ_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree",  "("+weight+"*puWeight*lumiWeight*"+WScaleStr+")" )
TopNorm = DIST( "TopNorm", "80XRootFilesUpdated/RUNAnalysis_ST_t-channel_topantitop_4f_inclusiveDecays_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree",  "("+weight+"*puWeight*lumiWeight)" )
Top = DIST( "Top", "80XRootFilesUpdated/RUNAnalysis_ST_t-channel_topantitop_4f_inclusiveDecays_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree",  "("+weight+"*puWeight*lumiWeight*"+TopScaleStr+")" )
Sig120 = DIST( "Sig", "80XRootFilesUpdated/Signals/RUNAnalysis_RPVStopStopToJets_UDD323_M-120_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "puWeight*"+weight+"*"+str(scaleFactor('RPVStopStopToJets_UDD323_M-120')) )
Sig280 = DIST( "Sig", "80XRootFilesUpdated/Signals/RUNAnalysis_RPVStopStopToJets_UDD323_M-240_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "puWeight*"+weight+"*"+str(scaleFactor('RPVStopStopToJets_UDD323_M-280')) )
QCDHT = DIST( "QCDHT", "80XRootFilesUpdated/RUNAnalysis_QCDHTAll_80X_V2p4_v07p1.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*lumiWeight")

if "MC" in method:
    isMC = True
    Dists = [QCDHT]
    DistsSub = []
elif "DATA" in method:
    isMC = False
    Dists = [DATA]
    DistsSub = [Top, WJets, TTJets]
else:
    print "Method not found: " +method
    sys.exit(0)

prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
#prelimFit = [-1,-1,-1,-1,-1]
tau21 = "(jet1Tau21<0.90&jet2Tau21<0.90)"

name = ""
chanCuts = ""

if int(channel) == 0:
    name = "b0t0"
    chanCuts = zerobtag+"&"+zeroTop
elif int(channel) == 1:
    name = "b1t0"
    chanCuts = onebtag+"&"+zeroTop
elif int(channel) == 2:
    name = "b2t0"
    chanCuts = twobtag+"&"+zeroTop
elif int(channel) == 3:
    name = "b0t1"
    chanCuts = zerobtag+"&"+oneTop
elif int(channel) == 4:
    name = "b1t1"
    chanCuts = onebtag+"&"+oneTop
elif int(channel) == 5:
    name = "b2t1"
    chanCuts = twobtag+"&"+oneTop
elif int(channel) == 6:
    name = "b0t2"
    chanCuts = zerobtag+"&"+twoTop
elif int(channel) == 7:
    name = "b1t2"
    chanCuts = onebtag+"&"+twoTop
elif int(channel) == 8:
    name = "b2t2"
    chanCuts = twobtag+"&"+twoTop
elif int(channel) == 9:
    name = "pres"
    chanCuts = "1"

ThetaFileMaker( name, scaleName, chanCuts, 10, 60, 350, Xcut, Ycut, tau21, prelimFit, 25, HT, Dists, DistsSub, [], isMC, log )
