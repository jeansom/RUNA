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
    # fit = True if you want to fit the transfer factor, fit = False otherwise
    fit = True


    gStyle.SetOptStat(0)

    ## Defining Cuts
    presel = tau21+"&"+HT
    cuts = Xcut[0]+"<"+Xcut[1]+"&"+Ycut[0]+"<"+Ycut[1]
    anticuts = Xcut[0]+">"+Xcut[1]+"&"+Ycut[0]+"<"+Ycut[1]
    cutsB = Xcut[0]+"<"+Xcut[1]+"&"+Ycut[0]+">"+Ycut[1]
    cutsD = Xcut[0]+">"+Xcut[1]+"&"+Ycut[0]+">"+Ycut[1]

    cut = [ float(Xcut[1]), "<" ] # For defining B vs D regions
    
    ## Average mass binned fit
    EstMass = Alphabet( "BkgEstMass", Dists, DistsSub, DistSig ) # Nominal

    #### Makes list with bins for fit
    binsMass = []
    binWidth = 2.5
    NBins = int(((350-50))/binWidth)
    var_arrayMass = [ "prunedMassAve", Xcut[0], NBins, 50., 350., Xcut[2], Xcut[3], Xcut[4] ] # For making B,D plot

    # If we fit, the bins can be bigger. Otherwise, they should be the same size as the bins in the est
    if fit:
        NBins = int(((350-50))/25)
        for i in xrange( 0, NBins ):
            binsMass.append( [ var_arrayMass[3]+25*i, var_arrayMass[3]+25*(i+1) ] )
    else:
        i = var_arrayMass[3]
        while i<200:
            binsMass.append( [ i, i+5] )
            i = i+5
        for i in xrange( 200, 350 ):
            if i%25 == 0: binsMass.append( [i, i+25] )

    #### Form of fit
    prelimFit = [2,1,0,0] # preliminary values for fit
#    prelimFit = [2.60, 1.94, -1.74e+01]
#    prelimFit = [ 0.2, -1.74, -8.9e-08 ] #??
    FMass = SigmoidFit(prelimFit,50, 350,"Mass","SEMR") # Nominal fit
    FMass1 = SigmoidFit(prelimFit,50, 350,"Mass1","SEMR") # Nominal fit again, used if staying blinded

    # Bins for final estimation plot, bin width int(bins)
    binBoundaries = []
    if "b0t0" in chan or "b1t0" in chan or "b2t0" in chan or "b0t1" in chan or "pres" in chan:
        dBin = float(10)
        i = minBin
        while i<maxBin+1:
            binBoundaries.append(i)
            i=i+dBin
    else:
        dBin = float(25)
        i = 75
        binBoundaries.append(60)
        maxBin = 350
        while i<maxBin+1:
            binBoundaries.append(i)
            i=i+dBin

    # Use alternate channel's fits when low statistics
    if "t2" in chan: chanCutsTemp = presel+"&"+twoTop
    elif "b2t1" in chan: chanCutsTemp = presel+"&"+onebtag+"&"+oneTop
    elif "b2t0" in chan: chanCutsTemp = presel+"&"+onebtag+"&"+zeroTop
    else: chanCutsTemp = presel+"&"+chanCuts
    
    # Used to fill the actual estimate, should be the same size as the bins in the final estimate
    rhoBinBoundaries = []
    for i in binsMass:
        rhoBinBoundaries.append(i[0])
    rhoBinBoundaries.append(binsMass[len(binsMass)-1][1])

    # Runs estimate
    MakeFitPlots( EstMass, FMass, binsMass, "prunedMassAve", Xcut[0], var_arrayMass, chanCutsTemp, Ycut[0]+">"+Ycut[1], cut, 0, "", "", "outputs/"+directory+method+"/Mass"+chan+"_"+scaleName, binBoundaries, fit, False ) # Creates the 2D plot, ratio, and ratio fit
    MakeEstPlots( EstMass, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/Mass"+chan+"_"+scaleName, binBoundaries, fit, isMC, False, log ) # Makes the actual estimation

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
    if len(DistsSub) == 1:
        quickplot( TTJets.File, TTJets.Tree, chan__TTBAR, "prunedMassAve", presel+"&"+cuts+"&"+chanCuts, TTJets.weight ) # Makes nominal T plot

    #### Opens theta root file for writing
    FILE = TFile( "outputs/"+directory+method+"/LIM_FEED"+chan+"_"+scaleName+".root", "RECREATE" )
    FILE.cd()
    #### Write plots to file    

    if not("up" in scaleName or "down" in scaleName): chan__DATA.Write()
    chan__QCD.Write()
    if len(DistsSub) > 2:
        chan__TTBAR.Write()
        chan__TOP.Write()
        chan__WJETS.Write()
    if len(DistsSub) == 1:
        chan__TTBAR.Write()

    ### Writes file
    FILE.Write()
    FILE.Save()
    
parser = argparse.ArgumentParser()
parser.add_argument( '-c', '--channel', action='store', dest='channel', default=1, help='Channel to run the estimation for')
parser.add_argument( '-s', '--scale', action='store', dest='scale', default=1, help='scale array')
parser.add_argument( '-m', '--method', action='store', dest='method', default="CBDCMVAv2MC", help='Method, B*(C/D)..., CMVA..., MC, Data...')
parser.add_argument( '-d', '--directory', action='store', dest='directory', default = "", help='Directory to save output in')
parser.add_argument( '-b', '--bins', action='store', dest='bins', default = 10, help='bin width for final estimation')
parser.add_argument( '-j', '--HT', action='store', dest='HT', default = "abs(HT)>-999", help='Any extra cuts')
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


##### DELETE BEFORE UPLOADING #####
if scale > 2 and scale < 9: sys.exit(0)
if int(channel) > 4: sys.exit(0)
os.mkdir("outputs/"+directory+method)

# Defines amount to scale each background by, the theta results. For scale == 9, MAKE SURE THE ERROR (2nd value in each array) IS 0
if scale == 1:
    scaleName = "__TTScale__up"
    scaleArray = {'TopScale': [(0,0)], 'WJScale': [(0,0)], 'TTAlphaScale': [(0,0)], 'TTScale': [(0,1)]}
elif scale == 2:
    scaleName = "__TTScale__down"
    scaleArray = {'TopScale': [(0,0)], 'WJScale': [(0,0)], 'TTAlphaScale': [(0,0)], 'TTScale': [(0,-1)]}
elif scale == 3:
    scaleName = "__TTAlphaScale__up"
    scaleArray = {'TopScale': [(0,0)], 'WJScale': [(0,0)], 'TTAlphaScale': [(0,1)], 'TTScale': [(0,0)]}
elif scale == 4:
    scaleName = "__TTAlphaScale__down"
    scaleArray = {'TopScale': [(0,0)], 'WJScale': [(0,0)], 'TTAlphaScale': [(0,-1)], 'TTScale': [(0,0)]}
elif scale == 5:
    scaleName = "__WJScale__up"
    scaleArray = {'TopScale': [(0,0)], 'WJScale': [(0,1)], 'TTAlphaScale': [(0,0)], 'TTScale': [(0,0)]}
elif scale == 6:
    scaleName = "__WJScale__down"
    scaleArray = {'TopScale': [(0,0)], 'WJScale': [(0,-1)], 'TTAlphaScale': [(0,0)], 'TTScale': [(0,0)]}
elif scale == 7:
    scaleName = "__TopScale__up"
    scaleArray = {'TopScale': [(0,1)], 'WJScale': [(0,0)], 'TTAlphaScale': [(0,0)], 'TTScale': [(0,0)]}
elif scale == 8:
    scaleName = "__TopScale__down"
    scaleArray = {'TopScale': [(0,-1)], 'WJScale': [(0,0)], 'TTAlphaScale': [(0,0)], 'TTScale': [(0,0)]}
elif scale == 9:
    scaleName = "__After"
    scaleArray = {'TopScale': [(0,0)], 'WJScale': [(0,0)], 'TTAlphaScale': [(0,0)], 'TTScale': [(0.8705862518949896, 0.)], '__nll': [-21212.33992820157]}
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

# Defines cuts
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
    print "here"
    Ycut = [ "prunedMassAsym", "0.1", 20, 0., 1. ]
    Xcut = [ "deltaEtaDijet", "1.5", 20, 0., 5. ]
else:
    print "Method not found: " +method
    sys.exit(0)

# The T and W scales
TTNorm = "( (1.06)*1.00*/1.00*(1+0.5*" + str(scaleTT) + "+0.5*" + str(scaleTTErr) + ") )" # TTBar normalization
TTAlpha = "exp( (-0.0005*(HT/2))*(1-.5*" + str(scaleAlpha) + "-.5*" + str(scaleAlphaErr) + ") )" # Alpha NOTE: subtracting = adding because -0.0005

TTScaleStrNorm = "(1.06*exp( (-0.0005*(HT/2)) ))"
TTScaleStr = "(" + TTNorm + "*" + TTAlpha + ")" # Total string to scale TT by, norm*alpha
WScaleStr = "(1+.5*"+str(scaleW)+"+.5*"+str(scaleWErr)+")" # W scale
TopScaleStr = "(1+.5*"+str(scaleTop)+"+.5*"+str(scaleTopErr)+")"

# Create the distributions
weight = "(36555.21/15)"

rootFiles = "80XRootFilesUpdated/"

DATA = DIST( "DATA", "v08/RUNAnalysis_JetHT_Run2016_80X_V2p4_v08_cut15_pruned.root", "BoostedAnalysisPlots/RUNATree", "1" )
QCDPt = DIST( "QCDPt", "v08/RUNAnalysis_QCDPtAll_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", ".62*puWeight*lumiWeight*"+weight )
TTJetsNorm = DIST( "TTJets", "v08/RUNAnalysis_TT_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*puWeight*lumiWeight*"+TTScaleStrNorm+")" )
TTJets = DIST( "TTJets", "v08/RUNAnalysis_TT_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*puWeight*lumiWeight*"+TTScaleStr+")" )
WJetsNorm = DIST( "WJets", "v08/RUNAnalysis_WJetsToQQ_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree",  "("+weight+"*puWeight*lumiWeight)" )
WJets = DIST( "WJets", "v08/RUNAnalysis_WJetsToQQ_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree",  "("+weight+"*puWeight*lumiWeight*"+WScaleStr+")" )
TopNorm = DIST( "TopNorm", rootFiles + "/RUNAnalysis_ST_t-channel_topantitop_4f_inclusiveDecays_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree",  "("+weight+"*puWeight*lumiWeight)" )
Top = DIST( "Top", rootFiles + "/RUNAnalysis_ST_t-channel_topantitop_4f_inclusiveDecays_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree",  "("+weight+"*puWeight*lumiWeight*"+TopScaleStr+")" )
Sig120 = DIST( "Sig", "v08/Signals/RUNAnalysis_RPVStopStopToJets_UDD323_M-120_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", "puWeight*"+weight+"*lumiWeight" )
Sig280 = DIST( "Sig", "v08/Signals/Signals/RUNAnalysis_RPVStopStopToJets_UDD323_M-240_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", "puWeight*"+weight+"*lumiWeight" )
QCDHT = DIST( "QCDHT", "v08/RUNAnalysis_QCDHTAll_80X_V2p4_v08.root", "BoostedAnalysisPlots/RUNATree", ".69*puWeight*36555.21/15*lumiWeight")

# Which samples to run over
if "MC" in method and "Pt" in method:
    isMC = True
    Dists = [ TTJetsNorm, QCDPt]
    DistsSub = [TTJets]
elif "MC" in method and "HT" in method:
    isMC = True
    Dists = [TTJetsNorm, QCDHT]
    DistsSub = [TTJets]
elif "DATA" in method:
    isMC = False
    Dists = [DATA]
    DistsSub = [Top, WJets, TTJets]
else:
    print "Method not found: " +method
    sys.exit(0)

prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ] #Prelim fit, but I change it later so this parameter is irrelevant. Ignore
tau21 = "(jet1Tau21<0.45&jet2Tau21<0.45)&"+HT

name = ""
chanCuts = ""
bins = 5

# Run over the correct channel
if int(channel) == 0:
    name = "b0t0"
    chanCuts = zerobtag+"&"+zeroTop+"&"+HT
elif int(channel) == 1:
    name = "b1t0"
    chanCuts = onebtag+"&"+zeroTop+"&"+HT
elif int(channel) == 2:
    name = "b2t0"
    chanCuts = twobtag+"&"+zeroTop+"&"+HT
elif int(channel) == 3:
    name = "b0t1"
    chanCuts = zerobtag+"&"+oneTop+"&"+HT
elif int(channel) == 4:
    name = "b1t1"
    chanCuts = onebtag+"&"+oneTop+"&"+HT
elif int(channel) == 5:
    name = "b2t1"
    bins = 15
    chanCuts = twobtag+"&"+oneTop+"&"+HT
elif int(channel) == 6:
    name = "b0t2"
    bins = 15
    chanCuts = zerobtag+"&"+twoTop+"&"+HT
elif int(channel) == 7:
    name = "b1t2"
    bins = 15
    chanCuts = onebtag+"&"+twoTop+"&"+HT
elif int(channel) == 8:
    name = "b2t2"
    bins = 15
    chanCuts = twobtag+"&"+twoTop+"&"+HT
elif int(channel) == 9:
    name = "pres"
    chanCuts = "1"+"&"+HT

ThetaFileMaker( name, scaleName, chanCuts, bins, 60, 350, Xcut, Ycut, tau21, prelimFit, 10, HT, Dists, DistsSub, [], isMC, log )
