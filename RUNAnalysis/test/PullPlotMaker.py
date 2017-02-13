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

# Makes root files with variations on pulls saved, has methods to make plots
# SHOULD SPLIT UP INTO TWO SETS OF CODE
# THETAFILEMAKERQCD.PY ALSO MAKES THE PULL PLOT FILES, JUST MORE SLOWLY
#### chan: channel to run bkg est for, ex: b0t0
#### chanCuts: cuts which define chan
#### bins: bin width for final estimation
#### minBin: minimum value for final bkg est
#### maxBin: maximum value for final bkg est
#### Xcut: The cut defining the X axis for the ABCD plot (A vs C, B vs D?)
#### Ycut: The cut defining the Y axis for the ABCD plot (A vs B, C vs D?)
#### scaleTT: The amount theta says to scale the TT norm. by, if pre-theta, 0
#### scaleTTErr: The amount theta says to scale the TT norm. error by, if pre-theta, 1
#### scaleW: The amount theta says to scale the W norm. by, if pre-theta, 0
#### scaleWErr: The amount theta says to scale the W norm. error by, if pre-theta, 1
#### scaleAlpha: The amount theta says to scale alpha by, if pre-theta, 0
#### scaleAlphaErr: The amount theta says to scale the alpha error by, if pre-theta, 1
#### tau21: tau21 cut
#### prelimFit: the preliminary values for the fit
#### fitBins: bin size for the fit
#### isMC: MC or data
def PullPlotMaker( chan, chanCuts, bins, minBin, maxBin, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleAlpha, scaleAlphaErr, tau21, prelimFit, fitBins, isMC=True ):
    gStyle.SetOptStat(0)
    #gRoot.cd()
    # Setting basic distributions
    weight = "(36600*puWeight*lumiWeight)"

    # The T and W scales
    TTNorm = "exp( (0.0615*2)*(1+.2*"+str(scaleTT)+"))" # The scale that determines the nominal TTBar normalization
    TTNormUp = "exp( (0.0615*2)*(1+.2*" + str(scaleTT) + "+.2*" + str(scaleTTErr) + ") )" # Upper TTBar normalization
    TTNormDn = "exp( (0.0615*2)*(1+.2*" + str(scaleTT) + "-.2*" + str(scaleTTErr) + ") )" # Lower TTBar normalization

    TTAlpha = "exp( (-0.0005*(genPartPt1+genPartPt2))*(1-.2*" + str(scaleAlpha) + ") )" # The scale that determines the nominal alpha NOTE: subtracting = adding because -0.0005
    TTAlphaUp = "exp( (-0.0005*(genPartPt1+genPartPt2))*(1-.2*" + str(scaleAlpha) + "-.2*" + str(scaleAlphaErr) + ") )" # Upper alpha NOTE: subtracting = adding because -0.0005
    TTAlphaDn = "exp( (-0.0005*(genPartPt1+genPartPt2))*(1-.2*" + str(scaleAlpha) + "+.2*" + str(scaleAlphaErr) + ") )" # Lower alpha NOTE: subtracting = adding because -0.0005

    TTScaleStr = "(" + TTNorm + "*" + TTAlpha + ")" # Total string to scale TT by, norm*alpha
    TTScaleErrUpStr = "(" + TTNormUp + "*" + TTAlpha + ")" # String for scaling TT with norm up, normUp*alpha
    TTScaleErrDnStr = "(" + TTNormDn + "*" + TTAlpha + ")" # String for scaling TT with norm dn, normDn*alpha
    AlphaScaleUpStr = "(" + TTNorm + "*" + TTAlphaUp + ")" # Total string to scale TT by with alpha up, norm*alphaUp
    AlphaScaleDnStr = "(" + TTNorm + "*" + TTAlphaDn + ")" # Total string to scale TT by with alpha dn, norm*alphaDn

    WScaleStr = "(1+.2*"+str(scaleW)+")" # The scale that determines the nominal W normalization
    WScaleUpStr = "(1+.2*"+str(scaleW)+"+.2*"+str(scaleWErr)+")" # Upper W normalization
    WScaleDnStr = "(1+.2*"+str(scaleW)+"-.2*"+str(scaleWErr)+")" # Lower W normalization

    # Create the distributions
    DATA = DIST( "DATA", "80XRootFiles/RUNAnalysis_JetHT_Run2016_80X_V2p4_v05_cut.root", "BoostedAnalysisPlots/RUNATree", "1" )
    QCD = DIST( "QCD", "80XRootFiles/RUNAnalysis_QCDPtAll_Moriond17_80X_V2p4_v05.root", "BoostedAnalysisPlots/RUNATree", weight+"*.77" ) # .77 = k-factor
    SIG = DIST( "SIG", "80XRootFiles/RUNBoostedAnalysis_RPVStopStopToJets_UDD323_M-100v01.root", "BoostedAnalysisPlots/RUNATree", weight )

    TTJets = DIST( "TTJets", "80XRootFiles/RUNBoostedAnalysis_TT_TuneCUETP8M2T4_13TeV-powheg-pythia8v04.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*"+TTScaleStr+")" ) # nominal TT distribution
    TTJetsUp = DIST( "TTJetsUp", "80XRootFiles/RUNBoostedAnalysis_TT_TuneCUETP8M2T4_13TeV-powheg-pythia8v04.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*"+TTScaleErrUpStr+")" ) # TT distribution, TT norm. scaled up
    TTJetsDn = DIST( "TTJetsDn", "80XRootFiles/RUNBoostedAnalysis_TT_TuneCUETP8M2T4_13TeV-powheg-pythia8v04.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*"+TTScaleErrDnStr+")"  ) # TT distribution, TT norm. scaled down
    TTJetsAlphaUp = DIST( "TTJetsUp", "80XRootFiles/RUNBoostedAnalysis_TT_TuneCUETP8M2T4_13TeV-powheg-pythia8v04.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*"+AlphaScaleUpStr+")") # TT distribution, TT alpha scaled up
    TTJetsAlphaDn = DIST( "TTJetsDn", "80XRootFiles/RUNBoostedAnalysis_TT_TuneCUETP8M2T4_13TeV-powheg-pythia8v04.root", "BoostedAnalysisPlots/RUNATree",  "("+weight+"*"+AlphaScaleDnStr+")" ) # TT distribution, TT alpha scaled down

    WJets = DIST( "WJets", "80XRootFiles/RUNBoostedAnalysis_WJetsToQQ_HT-600ToInfv04.root", "BoostedAnalysisPlots/RUNATree",  "("+weight+"*"+WScaleStr+")" ) # nominal W distribution
    WJetsUp = DIST( "WJetsUp", "80XRootFiles/RUNBoostedAnalysis_WJetsToQQ_HT-600ToInfv04.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*"+WScaleUpStr+")" ) # W distribution, normalization scaled up
    WJetsDn = DIST( "WJetsDn", "80XRootFiles/RUNBoostedAnalysis_WJetsToQQ_HT-600ToInfv04.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*"+WScaleDnStr+")" ) # W distribution, normalization scaled down

#    WW = DIST( "WW", "80XRootFiles/RUNBoostedAnalysis_WWTo4Q_13TeV-powhegv01.root", "BoostedAnalysisPlots/RUNATree", weight )
#    ZZ = DIST( "ZZ", "80XRootFiles/RUNBoostedAnalysis_ZZTo4Q_13TeV_amcatnloFXFX_madspin_pythia8v01.root", "BoostedAnalysisPlots/RUNATree", weight )
#    ZJets = DIST( "ZJets", "80XRootFiles/RUNBoostedAnalysis_ZJetsToQQ_HT600toInf_13TeV-madgraphv01.root", "BoostedAnalysisPlots/RUNATree", weight )
#    Sig = DIST( "Sig", "80XRootFiles/RUNBoostedAnalysis_RPVStopStopToJets_UDD323_M-100v01.root", "BoostedAnalysisPlots/RUNATree", "puWeight*36600*159991" )

    # Creating Alphabet objects to run estimate on    
    if isMC: 
#        Dists = [ QCD, TTJets, WJets, WW, ZZ, ZJets ]
        Dists = [ QCD, TTJets, WJets ]
    else: 
        Dists = [DATA]
    DistsSub = [ WJets, TTJets ]
    print random.random()
    print str(Dists)
    ## Defining Cuts
    presel = "jet1Tau21<"+tau21+"&jet2Tau21<"+tau21
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

    # Creating Alphabet objects to run estimate on    
    if isMC: # If running over the MC
        Dists = [ QCD, TTJets, WJets ] # Use the MC distributions
    else:  # Otherwise
        Dists = [DATA] # Use data 
    DistsSub = [ WJets, TTJets ] # Nominal distributions to subtract

    ## Defining Cuts
    presel = "jet1Tau21<"+tau21+"&jet2Tau21<"+tau21
    cuts = "prunedMassAsym<0.1&deltaEtaDijet<1.0"
    anticuts = Xcut[0]+">"+Xcut[1]+"&"+Ycut[0]+"<"+Ycut[1]
    cutsB = Xcut[0]+"<"+Xcut[1]+"&"+Ycut[0]+">"+Ycut[1]
    cutsD = "prunedMassAsym>0.1&deltaEtaDijet>1.0"
    cut = [ float(Xcut[1]), "<" ] # For defining B vs D regions
    
    ## Average mass binned fit
    EstMass = Alphabet( "BkgEstMass", Dists, DistsSub ) # Nominal
    EstMassWJUp = Alphabet( "BkgEstMassWJUp", Dists, [WJetsUp, TTJets] ) # W norm. up
    EstMassWJDn = Alphabet( "BkgEstMassWJDn", Dists, [WJetsDn, TTJets] ) # W norm. dn
    EstMassTTUp = Alphabet( "BkgEstMassTTUp", Dists, [WJets, TTJetsUp] ) # T norm. up
    EstMassTTDn = Alphabet( "BkgEstMassTTDn", Dists, [WJets, TTJetsDn] ) # T norm. dn
    EstMassTTAlphaUp = Alphabet( "BkgEstMassTTAlphaUp", Dists, [WJets, TTJetsAlphaUp] ) # T alpha up
    EstMassTTAlphaDn = Alphabet( "BkgEstMassTTAlphaDn", Dists, [WJets, TTJetsAlphaDn] ) # T alpha dn
    
    #### Makes list with bins for fit
    binsMass = []
    binWidth = fitBins
    NBins = int(((350-50))/binWidth)
    var_arrayMass = [ "prunedMassAve", Xcut[0], NBins, 50., 350., Xcut[2], Xcut[3], Xcut[4] ] # For making B,D plot
    
    for i in xrange( 0, NBins ):
        binsMass.append( [ var_arrayMass[3]+binWidth*i, var_arrayMass[3]+binWidth*(i+1) ] )

        
    #### Form of fit
    FMass = SigmoidFit(prelimFit,60,350,"Mass","SEMR") # Nominal fit
    FMass1 = SigmoidFit(prelimFit,60,350,"Mass1","SEMR") # Nominal fit again, used if staying blinded

    FMassWJUp = SigmoidFit(prelimFit,60,350,"Mass","SEMR") # Fit W norm. up
    FMassWJDn = SigmoidFit(prelimFit,60,350,"Mass","SEMR") # Fit W norm. dn

    FMassTTUp = SigmoidFit(prelimFit,60,350,"Mass","SEMR") # Fit T norm. up
    FMassTTDn = SigmoidFit(prelimFit,60,350,"Mass","SEMR") # Fit T norm. dn
    FMassTTAlphaUp = SigmoidFit(prelimFit,60,350,"Mass","SEMR") # Fit T alpha up
    FMassTTAlphaDn = SigmoidFit(prelimFit,60,350,"Mass","SEMR") # Fit T alpha dn

    # Bins for final estimation plot, bin width int(bins)
    binBoundaries = []
    dBin = int(bins)
    for i in xrange( minBin, maxBin+1 ):
        if i%dBin == 0: binBoundaries.append(i)


    # Use alternate channel's fits when low statistics
    if chan is "b0t2": chanCutsTemp = zerobtag+"&"+oneTop
    elif chan is "b1t2": chanCutsTemp = onebtag+"&"+oneTop
    elif chan is "b2t1": chanCutsTemp = twobtag+"&"+zeroTop
    elif chan is "b2t2": chanCutsTemp = twobtag+"&"+zeroTop
    else: chanCutsTemp = chanCuts

    # Nominal
    MakeFitPlots( EstMass, FMass, binsMass, "prunedMassAve", Xcut[0], var_arrayMass, presel+"&"+chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "", "outputs/"+directory+method+"/Mass"+chan, False ) # Creates the 2D plot, ratio, and ratio fit
    MakeEstPlots( EstMass, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/Mass"+chan, isMC, False ) # Makes the actual estimation

parser = argparse.ArgumentParser()
parser.add_argument( '-c', '--channel', action='store', dest='channel', default=1, help='Channel to run the estimation for')
parser.add_argument( '-p_t', '--plot_true', action='store_true', dest='plot', help='Create plots')
parser.add_argument( '-p_f', '--plot_false', action='store_false', dest='plot', help='Don\'t create plots')
parser.add_argument( '-m', '--method', action='store', dest='method', default="CBDCMVAv2MC", help='Method, B*(C/D)..., CMVA..., MC, Data...')
parser.add_argument( '-d', '--directory', action='store', dest='directory', default = "", help='Directory to save output in')
parser.add_argument( '-b', '--bins', action='store', dest='bins', default = 10, help='bin width for final estimation')
parser.set_defaults(plot=True)
try:
    args = parser.parse_args()
    print "here"
except:
    parser.print_help()
    sys.exit(0)

channel = args.channel
plot = args.plot
method = args.method
directory = args.directory
bins = args.bins
os.mkdir("outputs/"+directory+method)

# Sets the cuts depending on the method
if "CSVv2M" in method:
    zerobtag = "(jet1btagCSVv2<0.8484&jet2btagCSVv2<0.8484)"
    onebtag = "((jet1btagCSVv2<0.8484&jet2btagCSVv2>0.8484)||(jet1btagCSVv2>0.8484&jet2btagCSVv2<0.8484))"
    twobtag = "(jet1btagCSVv2>0.8484&jet2btagCSVv2>0.8484)"
    jet1btag = "((jet1btagCSVv2>0.8484&jet2btagCSVv2<0.8484))"
    jet2btag = "((jet1btagCSVv2<0.8484&jet2btagCSVv2>0.8484))"
    tau21 = '.6'
elif "CMVAv2M" in method:
    zerobtag = "(jet1btagCMVAv2<0.4432&jet2btagCMVAv2<0.4432)"
    onebtag = "((jet1btagCMVAv2<0.4432&jet2btagCMVAv2>0.4432)||(jet1btagCMVAv2>0.4432&jet2btagCMVAv2<0.4432))"
    twobtag = "(jet1btagCMVAv2>0.4432&jet2btagCMVAv2>0.4432)"
    jet1btag = "((jet1btagCMVAv2>0.4432&jet2btagCMVAv2<0.4432))"
    jet2btag = "((jet1btagCMVAv2<0.4432&jet2btagCMVAv2>0.4432))"
    tau21 = '.6'
elif "CMVAv2T" in method:
    zerobtag = "(jet1btagCMVAv2<0.9432&jet2btagCMVAv2<0.9432)"
    onebtag = "((jet1btagCMVAv2<0.9432&jet2btagCMVAv2>0.9432)||(jet1btagCMVAv2>0.9432&jet2btagCMVAv2<0.9432))"
    twobtag = "(jet1btagCMVAv2>0.9432&jet2btagCMVAv2>0.9432)"
    jet1btag = "((jet1btagCMVAv2>0.9432&jet2btagCMVAv2<0.9432))"
    jet2btag = "((jet1btagCMVAv2<0.9432&jet2btagCMVAv2>0.9432))"
    tau21 = '.6'
else:
    print "Method not found: " +method
    sys.exit(0)

zeroTop = "(jet1Tau32>0.51&jet2Tau32>.51)"
oneTop = "((jet1Tau32<=0.51&jet2Tau32>=0.51)||(jet1Tau32>0.51&jet2Tau32<0.51))"
twoTop = "(jet1Tau32<0.51&jet2Tau32<0.51)"
jet1Top = "((jet1Tau32>0.51&jet2Tau32<0.51))"
jet2Top = "((jet1Tau32<0.51&jet2Tau32>0.51))"

if "CBD" in method:
    Xcut = [ "prunedMassAsym", "0.1", 20, 0., 1. ]
    Ycut = [ "deltaEtaDijet", "1.0", 20, 0., 5. ]
elif "BCD" in method:
    Ycut = [ "prunedMassAsym", "0.1", 20, 0., 1. ]
    Xcut = [ "deltaEtaDijet", "1.0", 20, 0., 5. ]
else:
    print "Method not found: " +method
    sys.exit(0)

if "MC" in method:
    isMC = True
elif "DATA" in method:
    isMC = False
else:
    print "Method not found: " +method
    sys.exit(0)

# Sets the TT, W, and Alpha scales, plus their errors
scaleTT = 0
scaleTTErr = 1
scaleW = 0
scaleWErr = 1
scaleTTAlpha = 0
scaleTTAlphaErr = 1

if 'After' in method:
    if 'CMVAv2' in method and 'BCD' in method:
        scaleTT = -2.4667173367494852
        scaleTTErr = 0.38251758104877376
        scaleW = -1.8645455346423288
        scaleWErr - 0.7210119122518508
        scaleAlpha = -0.013778219076773901
        scaleAlphaErr = 0.7623667756548729    
    elif 'CMVAv2' in method and 'CBD' in method:
        scaleTT = -1.6060278678358686
        scaleTTErr = 0.3978168955525405
        scaleW = -2.072689703006841
        scaleWErr = 0.7652224357046922
        scaleAlpha = -0.2801095559029134
        scaleAlphaErr = 0.9512591967628117
    elif 'CSVv2' in method and 'BCD' in method:
        scaleTT = -2.903936289359435
        scaleTTErr = 0.4236081552096973
        scaleW = -2.0419129304547856
        scaleWErr = 0.7304271932966462
        scaleAlpha = -0.21637014532343724
        scaleAlphaErr = 0.9681008876403856
    elif 'CSVv2' in method and 'CBD' in method:
        scaleTT = -0.9130354595971122
        scaleTTErr = 0.5810981065498508
        scaleW = -1.6220527381449101
        scaleWErr = 0.4278069505107658
        scaleTTAlpha = 0.24127780944242616
        scaleTTAlphaErr = 0.4295862763365301
    else:
        scaleTT = 0
        scaleTTErr = 1
        scaleW = 0
        scaleWErr = 1
        scaleTTAlpha = 0
        scaleTTAlphaErr = 1
else:
    scaleTT = 0
    scaleTTErr = 1
    scaleW = 0
    scaleWErr = 1
    scaleTTAlpha = 0
    scaleTTAlphaErr = 1

gStyle.SetOptFit(kFALSE)
gStyle.SetOptStat(0)

# Sets the preliminary fit depending on the channel/method and runs PullPlotMaker
prelimFit = [0,0,0]
fitBins = 25
PullPlots = []
PullPlots2 = []
if int(channel) == 0:
    if "CSVv2" in method and "BCD" in method:
        prelimFit = [ 5.94e-01, -6.48e-01, -3.51e-08 ]
    elif "CSVv2" in method and "CBD" in method:
        prelimFit = [ 2.19, 1.02, -3.92e-07 ]
    elif "CMVAv2" in method and "BCD" in method:
        prelimFit = [ 8.15e-01, -1.23, -6.56e-08, 0, 0]
    elif "CMVAv2" in method and "CBD" in method:
        prelimFit = [ 2.26, 1.01, -4.13e-07, 0, 0]
    else:
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]

    PullPlotMaker( "b0t0", zerobtag+"&"+zeroTop, bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, tau21, prelimFit,  fitBins, isMC )
if int(channel) == 1:
    if "CSVv2" in method and "BCD" in method:
        #prelimFit = [ -1.60, 9.68e-01, -6.51e-09 ]
        prelimFit = [ 7.45e-01, 4.41e-02, -3.56e-07 ]
    elif "CSVv2" in method and "CBD" in method:
        prelimFit = [ 2.21, 9.56, -3.36e-07 ]
    elif "CMVAv2" in method and "BCD" in method:
        #prelimFit = [ 9.80e-02, -7.53e-03, -2.59e-08 ]
        prelimFit = [ 7.45e-01, 4.41e-02, -3.56e-07 ]
    elif "CMVAv2" in method and "CBD" in method:
        fitBins = 50
        #prelimFit = [ 2.10, 9.60e-01, -3.18e-07 ]
        prelimFit = [ 7.45e-01, 4.41e-02, -3.56e-07 ]
    else:
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]

    PullPlotMaker( "b1t0", onebtag+"&"+zeroTop, bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, tau21, prelimFit,  fitBins, isMC )
if int(channel) == 2:
    if "CSVv2" in method and "BCD" in method:
        prelimFit = [ 9.24e-01, -1.69, -1.80e-06 ]
    elif "CSVv2" in method and "CBD" in method:
        prelimFit = [ 3.56, 5.01e-01, -8.09e-07 ]
    elif "CMVAv2" in method and "BCD" in method:
        prelimFit = [ 9.62e-01, -4.76e-01, -2.66e-06  ]
    elif "CMVAv2" in method and "CBD" in method:
        prelimFit = [ 2.09, 1.01, -2.45e-07 ]
    else:
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]

    PullPlotMaker( "b2t0", twobtag+"&"+zeroTop, bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, tau21, prelimFit,  fitBins, isMC )
if int(channel) == 3:
    if "CSVv2" in method and "BCD" in method:
        prelimFit = [ 7.03e-01, -9.82e-01, -8.68e-08 ]
    elif "CSVv2" in method and "CBD" in method:
        prelimFit = [ 2.41, 1.96, -4.60e-07 ]
    elif "CMVAv2" in method and "BCD" in method:
        prelimFit = [ 8.11e-01, -1.28, -1.21e-07 ]
    elif "CMVAv2" in method and "CBD" in method:
        #prelimFit = [ 2.55, 2.00, -4.83e-07 ]
        prelimFit = [ 3.51, 2.40, -1.03e-06 ]
    else:
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]

    PullPlotMaker( "b0t1", zerobtag+"&"+oneTop, bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, tau21, prelimFit,  fitBins, isMC )
if int(channel) == 4:
    if "CSVv2" in method and "BCD" in method:
        #prelimFit = [ -1.60, 9.68e-01, -6.51e-09 ]
        prelimFit = [ 7.45e-01, 4.41e-02, -3.56e-07 ]
    elif "CSVv2" in method and "CBD" in method:
        prelimFit = [ 2.21, 9.56, -3.36e-07 ]
    elif "CMVAv2" in method and "BCD" in method:
        #prelimFit = [ 9.80e-02, -7.53e-03, -2.59e-08 ]
        prelimFit = [ 7.45e-01, 4.41e-02, -3.56e-07 ]
    elif "CMVAv2" in method and "CBD" in method:
        #prelimFit = [ 2.10, 9.60e-01, -3.18e-07 ]
        #prelimFit = [ 7.45e-01, 4.41e-02, -3.56e-07 ]
        prelimFit = [ 3.80, 2.47, -4.60e-07 ]
    else:
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]

    PullPlotMaker( "b1t1", onebtag+"&"+oneTop, bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, tau21, prelimFit,  fitBins, isMC )
if int(channel) == 5:
    if "CSVv2" in method and "BCD" in method:
        prelimFit = [ 9.24e-01, -1.69, -1.80e-06 ]
    elif "CSVv2" in method and "CBD" in method:
        prelimFit = [ 3.56, 5.01e-01, -8.09e-07 ]
    elif "CMVAv2" in method and "BCD" in method:
        prelimFit = [ 9.62e-01, -4.76e-01, -2.66e-06  ]
    elif "CMVAv2" in method and "CBD" in method:
        prelimFit = [ 2.09, 1.01, -2.45e-07 ]
    else:
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]

    PullPlotMaker( "b2t1", twobtag+"&"+oneTop, bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, tau21, prelimFit,  fitBins, isMC )
if int(channel) == 6:
    if "CSVv2" in method and "BCD" in method:
        prelimFit = [ 7.03e-01, -9.82e-01, -8.68e-08 ]
    elif "CSVv2" in method and "CBD" in method:
        prelimFit = [ 2.41, 1.96, -4.60e-07 ]
    elif "CMVAv2" in method and "BCD" in method:
        prelimFit = [ 8.11e-01, -1.28, -1.21e-07 ]
    elif "CMVAv2" in method and "CBD" in method:
        prelimFit = [ 2.55, 2.00, -4.83e-07 ]
    else:
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]

    PullPlotMaker( "b0t2", zerobtag+"&"+twoTop, bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, tau21, prelimFit,  fitBins, isMC )
if int(channel) == 7:
    if "CSVv2" in method and "BCD" in method:
        #prelimFit = [ -1.60, 9.68e-01, -6.51e-09 ]
        prelimFit = [ 7.45e-01, 4.41e-02, -3.56e-07 ]
    elif "CSVv2" in method and "CBD" in method:
        prelimFit = [ 2.21, 9.56, -3.36e-07 ]
    elif "CMVAv2" in method and "BCD" in method:
        #prelimFit = [ 9.80e-02, -7.53e-03, -2.59e-08 ]
        prelimFit = [ 7.45e-01, 4.41e-02, -3.56e-07 ]
    elif "CMVAv2" in method and "CBD" in method:
        #prelimFit = [ 2.10, 9.60e-01, -3.18e-07 ]
        prelimFit = [ 7.45e-01, 4.41e-02, -3.56e-07 ]
    else:
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]

    PullPlotMaker( "b1t2", onebtag+"&"+twoTop, bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, tau21, prelimFit,  fitBins, isMC )
if int(channel) == 8:
    if "CSVv2" in method and "BCD" in method:
        prelimFit = [ 9.24e-01, -1.69, -1.80e-06 ]
    elif "CSVv2" in method and "CBD" in method:
        prelimFit = [ 3.56, 5.01e-01, -8.09e-07 ]
    elif "CMVAv2" in method and "BCD" in method:
        prelimFit = [ 9.62e-01, -4.76e-01, -2.66e-06  ]
    elif "CMVAv2" in method and "CBD" in method:
        prelimFit = [ 2.09, 1.01, -2.45e-07 ]
    else:
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]

    PullPlotMaker( "b2t2", twobtag+"&"+twoTop, bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, tau21, prelimFit,  fitBins, isMC )

if plot:
    PullPlots.append( [ TFile.Open("outputs/"+directory+"0"+method+"/Massb0t0pull.root"), "Zero btags, Zero top-tags" ] )
    PullPlots.append( [ TFile.Open("outputs/"+directory+"1"+method+"/Massb1t0pull.root"), "One btag, Zero top-tags" ] )
    PullPlots.append( [ TFile.Open("outputs/"+directory+"2"+method+"/Massb2t0pull.root"), "Two btags, Zero top-tags" ] )
    PullPlots.append( [ TFile.Open("outputs/"+directory+"3"+method+"/Massb0t1pull.root"), "Zero btags, One top-tag" ] )
    PullPlots.append( [ TFile.Open("outputs/"+directory+"4"+method+"/Massb1t1pull.root"), "One btag, One top-tag" ] )
    PullPlots.append( [ TFile.Open("outputs/"+directory+"5"+method+"/Massb2t1pull.root"), "Two btags, One top-tag" ] )
    PullPlots.append( [ TFile.Open("outputs/"+directory+"6"+method+"/Massb0t2pull.root"), "Zero btags, Two top-tags" ] )
    PullPlots.append( [ TFile.Open("outputs/"+directory+"7"+method+"/Massb1t2pull.root"), "One btag, Two top-tags" ] )
    PullPlots.append( [ TFile.Open("outputs/"+directory+"8"+method+"/Massb2t2pull.root"), "Two btags, Two top-tags" ] )

    directory2 = directory.replace("After","Before")
    method2 = method.replace("After","")

    PullPlots2.append( [ TFile.Open("outputs/"+directory2+"0"+method2+"/Massb0t0pull.root"), "Zero btags, Zero top-tags" ] )
    PullPlots2.append( [ TFile.Open("outputs/"+directory2+"1"+method2+"/Massb1t0pull.root"), "One btag, Zero top-tags" ] )
    PullPlots2.append( [ TFile.Open("outputs/"+directory2+"2"+method2+"/Massb2t0pull.root"), "Two btags, Zero top-tags" ] )
    PullPlots2.append( [ TFile.Open("outputs/"+directory2+"3"+method2+"/Massb0t1pull.root"), "Zero btags, One top-tag" ] )
    PullPlots2.append( [ TFile.Open("outputs/"+directory2+"4"+method2+"/Massb1t1pull.root"), "One btag, One top-tag" ] )
    PullPlots2.append( [ TFile.Open("outputs/"+directory2+"5"+method2+"/Massb2t1pull.root"), "Two btags, One top-tag" ] )
    PullPlots2.append( [ TFile.Open("outputs/"+directory2+"6"+method2+"/Massb0t2pull.root"), "Zero btags, Two top-tags" ] )
    PullPlots2.append( [ TFile.Open("outputs/"+directory2+"7"+method2+"/Massb1t2pull.root"), "One btag, Two top-tags" ] )
    PullPlots2.append( [ TFile.Open("outputs/"+directory2+"8"+method2+"/Massb2t2pull.root"), "Two btags, Two top-tags" ] )

    ###### FIT METRIC DIV 9 REGIONS WITH FIT ######

    C = TCanvas( "C", "", 800, 800 )
    C.Divide(3,3)
    C.SetTitle( "Pull/Error" )

    T0 = TLine(60,0,350,0)
    T0.SetLineColor(kGreen+3)
    
    T1 = TLine(60,1,350,1)
    T1.SetLineColor(kGreen+3)
    T1.SetLineStyle(3)
    Tm1 = TLine(60,-1,350,-1)
    Tm1.SetLineColor(kGreen+3)
    Tm1.SetLineStyle(3)
    
    T2 = TLine(60,2,350,2)
    T2.SetLineColor(kGreen+3)
    T2.SetLineStyle(2)
    Tm2 = TLine(60,-2,350,-2)
    Tm2.SetLineColor(kGreen+3)
    Tm2.SetLineStyle(2)
    sum1 = 0
    FitMet = [] # Array with the TH1Ds of the pull/sys err
    Fits = [] # Array with the fits of the above TH1Ds
    Results = [] # Array with the fit results of the above fits
    for i in xrange(len(PullPlots)): # Loops through all the regions
        C.cd(i+1)

        FitMet.append(TH1D("h"+str(i),"", PullPlots[i][0].Get("fitMetric_div").GetNbinsX(), 60, 350 ) ) # Appends an empty TH1D for the pull plot
        for bin in range(0, FitMet[i].GetNbinsX()+1): # Loops through the bins in the plot
            FitMet[i].SetBinContent( bin, PullPlots[i][0].Get("fitMetric_div").GetBinContent(bin) ) # And fills

        # Some stuff to pretty it up
        FitMet[i].GetXaxis().SetNdivisions(504)
        FitMet[i].GetYaxis().SetLabelSize(.06)
        FitMet[i].GetXaxis().SetLabelSize(.06)
        FitMet[i].GetYaxis().SetTitleSize(0)
        FitMet[i].GetXaxis().SetTitle("Average Pruned Mass [GeV]")
        FitMet[i].GetXaxis().SetTitleSize(0.06)
        FitMet[i].SetFillColor(kBlue)

        # Now fit the pull plot
        FitMet[i].Sumw2()
        Fits.append(TF1("f"+str(i), "[0] + [1]*x", 60, 350 )) # Appends a TF1 for the fit
        Fits[i].SetLineColor(kRed)
        Results.append(FitMet[i].Fit("f"+str(i), "S", "", 60, 350)) # Fits the pull plot and appends the result

        # Draw all the plots and fits and legends
        FitMet[i].Draw("hist")
        Fits[i].Draw("same")
        FitMet[i].GetYaxis().SetRangeUser(-5,5)
        T2.Draw("same")
        T1.Draw("same")
        T0.Draw("same")
        Tm1.Draw("same")
        Tm2.Draw("same")
        latex = TLatex()
        latex.SetNDC()
        latex.SetTextSize(0.05)
        latex.SetTextAlign(13)
        latex.DrawLatex( .2, 1, PullPlots[i][1] )
        latex.DrawLatex( .2, .95, "#color[2]{Linear Fit: " + str( "%.4f" % Results[i].Parameter(1)) + "*x + " + str( "%.4f" % Results[i].Parameter(0)) + "}" )
        latex.DrawLatex( .2, .90, "Integral: " + "{0:.5f}".format(FitMet[i].Integral()) )
        sum1 = sum1+FitMet[i].Integral()

    print sum1
    # Saves the plot with all 9 regions drawn
    C.SaveAs( "outputs/"+directory+method+"/PullPlotDivMetric"+method+".png" )

    ###### FIT METRIC QUAD WITH FIT 9 REGION FITS, BEFORE AND AFTER #######

    C5 = TCanvas( "C", "", 800, 800 )
    C5.Divide(3,3)
    C5.SetTitle( "Pull/Error" )

    sum5 = 0
    FitMet = [] # The quad pull plots after theta fitting
    FitMet2 = [] # The quad pull plots before theta fitting
    Fits = [] # Array with the fits for AFTER theta
    Results = [] # Results for above fit
    for i in xrange(len(PullPlots)): # Loop through the 9 regions pull plots
        C5.cd(i+1)

        FitMet.append(TH1D("h"+str(i),"", PullPlots[i][0].Get("fitMetric_quad").GetNbinsX(), 60, 350 ) ) # Appends an empty TH1D for the pull plot after
        for bin in range(0, FitMet[i].GetNbinsX()+1): # Loops through the bins in the pull plot
            FitMet[i].SetBinContent( bin, PullPlots[i][0].Get("fitMetric_quad").GetBinContent(bin) ) # And fills

        FitMet2.append(TH1D("h"+str(i),"", PullPlots2[i][0].Get("fitMetric_quad").GetNbinsX(), 60, 350 ) ) # Appends an empty TH1D for the pull plot before
        for bin in range(0, FitMet2[i].GetNbinsX()+1): # Loops through the bins in the pull plot
            FitMet2[i].SetBinContent( bin, PullPlots2[i][0].Get("fitMetric_quad").GetBinContent(bin) ) # And fills

        # Some stuff to pretty it up
        FitMet[i].GetXaxis().SetNdivisions(504)
        FitMet[i].GetYaxis().SetLabelSize(.06)
        FitMet[i].GetXaxis().SetLabelSize(.06)
        FitMet[i].GetYaxis().SetTitleSize(0)
        FitMet[i].GetXaxis().SetTitle("Average Pruned Mass [GeV]")
        FitMet[i].GetXaxis().SetTitleSize(0.06)
        FitMet[i].SetFillColor(kBlue)
        FitMet[i].SetLineColor(kBlue)
        FitMet[i].SetFillStyle(3315)
        FitMet[i].SetLineWidth(2)
        gStyle.SetHatchesSpacing(1)

        # Now fit the pull plot after
        FitMet[i].Sumw2()
        Fits.append(TF1("f"+str(i), "[0] + [1]*x", 60, 350 )) # Appends a TF1 for the fit
        Fits[i].SetLineColor(kRed)
        Results.append(FitMet[i].Fit("f"+str(i), "S", "", 60, 350)) # Fits the pull plot and appends the results

        # Draw all the plots and legends
        FitMet[i].Draw("hist")
#        Fits[i].Draw("same") # Don't draw the fit
        FitMet2[i].SetFillColor(kRed)
        FitMet2[i].SetLineColor(kRed)
        FitMet2[i].SetFillStyle(3004)
        FitMet2[i].SetLineWidth(2)
        FitMet2[i].Draw("same hist")
        FitMet[i].GetYaxis().SetRangeUser(-5,5)
        T2.Draw("same")
        T1.Draw("same")
        T0.Draw("same")
        Tm1.Draw("same")
        Tm2.Draw("same")
        latex = TLatex()
        latex.SetNDC()
        latex.SetTextSize(0.05)
        latex.SetTextAlign(13)
        latex.DrawLatex( .2, 1, PullPlots[i][1] )
#        latex.DrawLatex( .2, .95, "#color[2]{Before Theta: Integral="+"{0:.5f}".format(FitMet2[i].Integral())+"}" )
#        latex.DrawLatex( .2, .90, "#color[4]{After Theta: Integral="+"{0:.5f}".format(FitMet[i].Integral())+"}" )
        latex.DrawLatex( .2, .90, "#color[2]{Linear Fit: " + str( "%.4f" % Results[i].Parameter(1)) + "*x + " + str( "%.4f" % Results[i].Parameter(0)) + "}" )
        latex.DrawLatex( .2, .95, "Integral: " + "{0:.5f}".format(FitMet[i].Integral()) )
        sum5 = sum5+FitMet[i].Integral()

    print sum5
    # Saves the plot with all 9 regions drawn
    C5.SaveAs( "outputs/"+directory+method+"/PullPlotQuadMetric"+method+".png" )

    ###### FIT METRIC NORM WITH FIT  ######

    C6 = TCanvas( "C", "", 800, 800 )
    C6.Divide(3,3)
    C6.SetTitle( "Pull/Error" )

    sum6 = 0
    FitMet = [] # Array with the TH1Ds of the normal pull
    Fits = [] # Array with the fits of the above TH1Ds
    Results = [] # Array with the fit results of the above fits
    for i in xrange(len(PullPlots)): # Loops through all the region
        C6.cd(i+1)

        FitMet.append(TH1D("h"+str(i),"", PullPlots[i][0].Get("Pull_norm").GetNbinsX(), 60, 350 ) ) # Appends an empty TH1D for the pull plot
        for bin in range(0, FitMet[i].GetNbinsX()+1): # Loops through all the bins in the plot
            FitMet[i].SetBinContent( bin, PullPlots[i][0].Get("Pull_norm").GetBinContent(bin) ) # And fills

        # Some stuff to pretty it up
        FitMet[i].GetXaxis().SetNdivisions(504)
        FitMet[i].GetYaxis().SetLabelSize(.06)
        FitMet[i].GetXaxis().SetLabelSize(.06)
        FitMet[i].GetYaxis().SetTitleSize(0)
        FitMet[i].GetXaxis().SetTitle("Average Pruned Mass [GeV]")
        FitMet[i].GetXaxis().SetTitleSize(0.06)
        FitMet[i].SetFillColor(kBlue)

        # Now fit the pull plot
        FitMet[i].Sumw2()
        Fits.append(TF1("f"+str(i), "[0] + [1]*x", 60, 350 )) # Appends a TF1 for the fit
        Fits[i].SetLineColor(kRed)
        Results.append(FitMet[i].Fit("f"+str(i), "S", "", 60, 350)) # Fits the pull plot and appends the result
        FitMet[i].Draw("hist")
        Fits[i].Draw("same")

        # Draw all the plots and fits and legends
        FitMet[i].GetYaxis().SetRangeUser(-20,20)
        T2.Draw("same")
        T1.Draw("same")
        T0.Draw("same")
        Tm1.Draw("same")
        Tm2.Draw("same")
        latex = TLatex()
        latex.SetNDC()
        latex.SetTextSize(0.05)
        latex.SetTextAlign(13)
        latex.DrawLatex( .2, 1, PullPlots[i][1] )
        latex.DrawLatex( .2, .95, "#color[2]{Linear Fit: " + str( "%.4f" % Results[i].Parameter(1)) + "*x + " + str( "%.4f" % Results[i].Parameter(0)) + "}" )
        latex.DrawLatex( .2, .90, "Integral: " + "{0:.5f}".format(FitMet[i].Integral()) )
        sum6 = sum6+FitMet[i].Integral()

    print sum6
    # Saves the plot with all 9 regions drawn
    C6.SaveAs( "outputs/"+directory+method+"/PullPlotNormMetric"+method+".png" )

    ###### SUM OF NORM PULL  ######

    C2 = TCanvas( "C2", "", 800, 800 )
    C2.cd()
    allPull = PullPlots[0][0].Get("Pull_norm").Clone() # Plot to hold the sum of all the pull plots
    allPull.Reset()
    for i in xrange(len(PullPlots)): # Loop through 9 regions
        allPull.Add(PullPlots[i][0].Get("Pull_norm").Clone()) # Add the pull plots together

    # Make it prettier
    allPull.GetXaxis().SetNdivisions(504)
    allPull.GetYaxis().SetLabelSize(.03)
    allPull.GetYaxis().SetTitleSize(0)
    allPull.GetXaxis().SetTitle( "Average Pruned Mass [GeV]" )
    
    # Draw plot and a legend
    allPull.Draw()
    latex2 = TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.05)
    latex.SetTextAlign(13)
    latex.DrawLatex( .4, .8, "Sum of pull plots" )
    
    C2.SaveAs("outputs/"+directory+method+"/sumPull.png")
    
    ###### AVERAGE OF NORM PULL  ######

    C3 = TCanvas( "C3", "", 800, 800 )
    C3.cd()
    avePull = PullPlots[0][0].Get("Pull_norm").Clone() # Plot to hold the average of all the pull plots
    avePull.Reset()
    for i in xrange(len(PullPlots)): # Loop through 9 regions
        avePull.Add(PullPlots[i][0].Get("Pull_norm").Clone()) # Add the pull plots together

    for i in range(1, avePull.GetNbinsX()+1 ): # Loop through bins in avePull plot
        bin = avePull.GetBinContent(i)
        avePull.SetBinContent( i, bin/9 ) # Set bin content = bin content/9

    # Make it prettier
    avePull.GetXaxis().SetNdivisions(504)
    avePull.GetYaxis().SetLabelSize(.03)
    avePull.GetYaxis().SetTitleSize(0)
    avePull.GetXaxis().SetTitle( "Average Pruned Mass [GeV]" )
    avePull.SetFillColor(kBlue)

    # Draw plot, lines, legend
    avePull.Draw("hist")
#T2.Draw("same")
    T1.Draw("same")
    T0.Draw("same")
    Tm1.Draw("same")
    Tm2.Draw("same")
    latex2 = TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.03)
    latex.SetTextAlign(13)
    latex.DrawLatex( .4, .35, "Average Pull" )
    latex.DrawLatex( .4, .3, "CMVAv2 btag Cut, C*(B/D)" )
#latex.DrawLatex( .4, .25, "Integral: " + "{0:.5f}".format(avePull.Integral()) )
    
    C3.SaveAs("outputs/"+directory+method+"/avePull.png")
    
    ###### FIT METRIC QUAD PULL WITH FIT ######

    C4 = TCanvas( "C4", "", 800, 800 )
    C4.Divide(3,3)
    C4.SetTitle( "Pull/Error" )
    
    # Lines for plot
    T0 = TLine(60,0,350,0)
    T0.SetLineColor(kGreen+3)
    
    T1 = TLine(60,1,350,1)
    T1.SetLineColor(kGreen+3)
    T1.SetLineStyle(3)
    Tm1 = TLine(60,-1,350,-1)
    Tm1.SetLineColor(kGreen+3)
    Tm1.SetLineStyle(3)
    
    T2 = TLine(60,2,350,2)
    T2.SetLineColor(kGreen+3)
    T2.SetLineStyle(2)
    Tm2 = TLine(60,-2,350,-2)
    Tm2.SetLineColor(kGreen+3)
    Tm2.SetLineStyle(2)

    sum7 = 0
    P = [] # Array for pull plots 
    PFit = [] # Array for pull plot fits
    PResult = [] # Array for pull plot fit results
    for i in xrange(len(PullPlots)): # Loop through 9 region pulls
        gStyle.SetOptStat(0)
        C4.cd(i+1)
        P.append(TH1D("h"+str(i),"", PullPlots[i][0].Get("fitMetric_quad").GetNbinsX(), 60, 350 ) ) # Appends an empty TH1D for the pull plot
        for bin in range(0, P[i].GetNbinsX()+1): # Loops through the bins in the plot
            P[i].SetBinContent( bin, PullPlots[i][0].Get("fitMetric_quad").GetBinContent(bin) ) # And fills

        # Now fit the pull plot
        PFit.append(TF1("f"+str(i), "[0] + [1]*x", 60, 350 )) # Appends a TF1 for the fit
        PResult.append(P[i].Fit("f"+str(i), "S", "", 60, 350)) # Fits the pull plot and appends the result
    #    PFit = (P[i].GetFunction(f1)).Clone()

        # Pretty everything up
        PFit[i].SetLineColor(kRed)
        P[i].GetXaxis().SetNdivisions(504)
        P[i].GetYaxis().SetLabelSize(.06)
        P[i].GetXaxis().SetLabelSize(.06)
        P[i].GetYaxis().SetTitleSize(0)
        P[i].GetXaxis().SetTitle("Average Pruned Mass [GeV]")
        P[i].GetXaxis().SetTitleSize(.06)
        P[i].SetFillColor(kBlue)

        # Draw all plots, fits, legends...
        P[i].Draw("hist")
        P[i].GetYaxis().SetRangeUser(-20,20)
        PFit[i].Draw("same")
        T2.Draw("same")
        T1.Draw("same")
        T0.Draw("same")
        Tm1.Draw("same")
        Tm2.Draw("same")
        latex = TLatex()
        latex.SetNDC()
        latex.SetTextSize(0.05)
        latex.SetTextAlign(13)
        latex.DrawLatex( .2, 1, PullPlots[i][1] )
        latex.DrawLatex( .2, .95, "#color[2]{Linear Fit: " + str( "%.4f" % PResult[i].Parameter(1)) + "*x + " + str( "%.4f" % PResult[i].Parameter(0)) + "}" )
        #    latex.DrawLatex( .23, .90, "#color[2]{m: " + str( "%.4f" % PResult[i].Parameter(1)) + "}" )
        #    latex.DrawLatex( .23, .85, "#color[2]{b: " + str( "%.4f" % PResult[i].Parameter(0)) + "}" )
        latex.DrawLatex( .2, .90, "Integral: " + "{0:.5f}".format(P[i].Integral()) )
        sum7 = sum7+P[i].Integral()

    print sum7
    
    print "sum1: " + str(sum1)
    print "sum5: " + str(sum5)
    print "sum6: " + str(sum6)

    C4.SaveAs( "outputs/"+directory+method+"/PullPlotQuadFit"+method+".png" )
    
    ###### FIT METRIC DISTRIBUTION QUAD WITH FIT  ######

    C7 = TCanvas( "C", "", 800, 800 )
    sum6 = 0
    FitMet = [] # The quad pull plots after theta fitting
    FitMet2 = [] # The quad pull plots before theta fitting
    Fits = [] # Array for the gaussian fits, unnecessary?
    Results = [] # Results for above fits, unnecessary?
    for i in xrange(len(PullPlots)): # Loops through the 9 regions
        FitMet.append(TH1D("h0"+str(i),"", PullPlots[i][0].Get("fitMetric_quad").GetNbinsX(), 60, 350 ) ) # Appends an empty TH1D for the pull plot after theta
        for bin in range(0, FitMet[i].GetNbinsX()+1): # Loops through the bins
            FitMet[i].SetBinContent( bin, PullPlots[i][0].Get("fitMetric_quad").GetBinContent(bin) ) # and fills

        FitMet2.append(TH1D("h1"+str(i),"", PullPlots2[i][0].Get("fitMetric_quad").GetNbinsX(), 60, 350 ) ) # Appends an empty TH1D for the pull plot before theta
        for bin in range(0, FitMet2[i].GetNbinsX()+1): # Loops through the binds
            FitMet2[i].SetBinContent( bin, PullPlots2[i][0].Get("fitMetric_quad").GetBinContent(bin) ) # and fills

    pullDistBefore = TH1D( "pullDistBefore", "", 20, -10, 10 ) # TH1D for pull distribution before
    pullDistAfter = TH1D( "pullDistAfter", "", 20, -10, 10 ) # TH1D for pull distribution after

    for i in xrange(len(FitMet)): # Loop through pull plots for all regions
        for bin in range(0, FitMet[i].GetNbinsX()+1): # Fill pull distribution before
            pullDistAfter.Fill( FitMet[i].GetBinContent(bin) )
        for bin in range(0, FitMet2[i].GetNbinsX()+1): # Fill pull distribution after
            pullDistBefore.Fill( FitMet2[i].GetBinContent(bin) )

    # Pretty stuff up
    pullDistBefore.GetXaxis().SetTitle("#sigma")
    pullDistBefore.GetYaxis().SetTitle("Bins")

    pullDistAfter.GetXaxis().SetTitle("#sigma")
    pullDistAfter.GetYaxis().SetTitle("Bins")
    pullDistAfter.GetYaxis().SetLabelOffset(.0004)
    pullDistAfter.GetXaxis().SetLabelOffset(.0004)
    pullDistAfter.GetYaxis().SetLabelSize(.03)
    pullDistAfter.GetXaxis().SetLabelSize(.03)
    
    pullDistAfter.GetYaxis().SetTitleOffset(1.2)
#    pullDistAfter.GetXaxis().SetTitleOffset(1.4)

    pullDistAfter.GetYaxis().SetTitleSize(0.04)
    pullDistAfter.GetXaxis().SetTitleSize(0.04)

    # Fit pull distributions before and after and save results
    FitResultBefore = pullDistBefore.Fit( "gaus", "S", "", -10, 10 )
    FitBefore = pullDistBefore.GetFunction("gaus").Clone()
    FitResultAfter = pullDistAfter.Fit( "gaus", "S", "", -10, 10 )
    FitAfter = pullDistAfter.GetFunction("gaus").Clone()
    
    # Prettier again
    pullDistAfter.SetLineColor(kBlue)
    pullDistAfter.SetLineWidth(2)
    gStyle.SetHatchesSpacing(1)
    
    pullDistBefore.SetLineColor(kRed)
    pullDistBefore.SetLineWidth(2)
    
    FindAndSetMax( [pullDistAfter, pullDistBefore], False)
    
    # Draw everything, and save
    pullDistAfter.Draw("hist")
    pullDistBefore.Draw("hist same")
    
    FitBefore.SetLineColor(kRed)
    FitAfter.SetLineColor(kBlue)
    FitBefore.SetLineStyle(2)
    FitAfter.SetLineStyle(2)
    
    FitBefore.Draw("same")
    FitAfter.Draw("same")

    T0 = TLine(0,0,0,pullDistAfter.GetMaximum())
    T0.SetLineWidth(2)
    T0.SetLineColor(19)
#    T0.SetLineStyle(3)
#    T0.Draw("same")
    
    CMS_lumi.extraText = "Preliminary"
    CMS_lumi.relPosX = 0.15
    CMS_lumi.CMS_lumi(C7, 4, 0)
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.03)
    latex.SetTextAlign(13)
    latex.DrawLatex( .12, .85, "#color[2]{Before Theta}" )
    latex.DrawLatex( .15, .81, "#color[2]{#mu: " + str("%.4f" % FitResultBefore.Parameter(1)) + "}" )
    latex.DrawLatex( .15, .78, "#color[2]{#sigma: " + str("%.4f" % FitResultBefore.Parameter(2)) + "}" )
    
    latex.DrawLatex( .12, .73, "#color[4]{After Theta}" )
    latex.DrawLatex( .15, .70, "#color[4]{#mu: " + str("%.4f" % FitResultAfter.Parameter(1)) + "}" )
    latex.DrawLatex( .15, .67, "#color[4]{#sigma: " + str("%.4f" % FitResultAfter.Parameter(2)) + "}" )

    C7.SaveAs( "outputs/"+directory+method+"/PullPlotQuadMetricAll"+method+".png" )

    ###### DIST OF PULLS WITH FIT 9 REGIONS  ######

    C8 = TCanvas( "C", "", 800, 800 )
    C8.Divide(3,3)
    sum6 = 0
    FitMet = [] # Pull plots after theta fitting
    FitMet2 = [] # Pull plots before theta fitting
    Fits = [] # Array with the gaussian fits, unnecessary!
    Results = [] # Results for above fits, unnecessary!
    for i in xrange(len(PullPlots)): # Loop through 9 regions
        C8.cd(i+1)

        FitMet.append(TH1D("h0"+str(i),"", PullPlots[i][0].Get("Pull_norm").GetNbinsX(), 60, 350 ) ) # Appends an empty TH1D for the pull plot after
        for bin in range(0, FitMet[i].GetNbinsX()+1): # Loops through bins
            FitMet[i].SetBinContent( bin, PullPlots[i][0].Get("Pull_norm").GetBinContent(bin) ) # And fills

        FitMet2.append(TH1D("h1"+str(i),"", PullPlots2[i][0].Get("Pull_norm").GetNbinsX(), 60, 350 ) ) # Appends an empty TH1D for the pull plot before
        for bin in range(0, FitMet2[i].GetNbinsX()+1): # Loops through bins
            FitMet2[i].SetBinContent( bin, PullPlots2[i][0].Get("Pull_norm").GetBinContent(bin) ) # And fills

    pullDistBefore = [] # Array for pull distributions before theta
    pullDistAfter = [] # Array for pull distributions after theta
    FitResultBefore = [] # Array for gaussian fit results before theta
    FitBefore = [] # Array for gaussian fits before theta
    FitResultAfter = [] # Array for gaussian fit results after theta
    FitAfter = [] # Array for gaussian fits after theta

    for i in xrange(len(FitMet)): # Loop through pull plots
        C8.cd(i+1)
        pullDistBefore.append(TH1D( "pullDistBefore" + str(i), "", 20, -10, 10 ))
        pullDistAfter.append(TH1D( "pullDistAfter[i]" + str(i), "", 20, -10, 10 ))

        for bin in range(0, FitMet[i].GetNbinsX()+1): # Loop through bins in after theta pull plots
            pullDistAfter[i].Fill( FitMet[i].GetBinContent(bin) ) # Fills pull distribution after
        for bin in range(0, FitMet2[i].GetNbinsX()+1): # Loop through bins in after theta pull plots
            pullDistBefore[i].Fill( FitMet2[i].GetBinContent(bin) ) # Fills pull distribution after

        # Pretties up dists
        pullDistBefore[i].GetXaxis().SetTitle("#sigma")
        pullDistBefore[i].GetYaxis().SetTitle("Bins")
        
        pullDistAfter[i].GetXaxis().SetTitle("#sigma")
        pullDistAfter[i].GetYaxis().SetTitle("Bins")
        pullDistAfter[i].GetYaxis().SetLabelOffset(.0004)
        pullDistAfter[i].GetXaxis().SetLabelOffset(.0004)
        pullDistAfter[i].GetYaxis().SetLabelSize(.03)
        pullDistAfter[i].GetXaxis().SetLabelSize(.03)
        
        pullDistAfter[i].GetYaxis().SetTitleOffset(1.2)
#    pullDistAfter[i].GetXaxis().SetTitleOffset(1.4)
        
        pullDistAfter[i].GetYaxis().SetTitleSize(0.04)
        pullDistAfter[i].GetXaxis().SetTitleSize(0.04)
        
        # Fits before and after distributions, saves fits and results
        FitResultBefore.append(pullDistBefore[i].Fit( "gaus", "S", "", -10, 10 ))
        FitBefore.append(pullDistBefore[i].GetFunction("gaus").Clone())
        FitResultAfter.append(pullDistAfter[i].Fit( "gaus", "S", "", -10, 10 ))
        FitAfter.append(pullDistAfter[i].GetFunction("gaus").Clone())
        
        # Pretties up again
        pullDistAfter[i].SetLineColor(kBlue)
        pullDistAfter[i].SetLineWidth(2)
        gStyle.SetHatchesSpacing(1)
        
        pullDistBefore[i].SetLineColor(kRed)
        pullDistBefore[i].SetLineWidth(2)
        
        FindAndSetMax( [pullDistAfter[i], pullDistBefore[i]], False)
        
        # Draws and saves
        pullDistAfter[i].Draw("hist")
#        pullDistBefore[i].Draw("hist")
        
        FitBefore[i].SetLineColor(kRed)
        FitAfter[i].SetLineColor(kBlue)
        FitBefore[i].SetLineStyle(2)
        FitAfter[i].SetLineStyle(2)
        
#        FitBefore[i].Draw("same")
        FitAfter[i].Draw("same hist")
        
        T0 = TLine(0,0,0,pullDistAfter[i].GetMaximum())
        T0.SetLineWidth(2)
        T0.SetLineColor(19)
        #    T0.SetLineStyle(3)
        #    T0.Draw("same")
        
        CMS_lumi.extraText = "Preliminary"
        CMS_lumi.relPosX = 0.15
        CMS_lumi.CMS_lumi( gPad, 4, 0)
        latex = TLatex()
        latex.SetNDC()
        latex.SetTextSize(0.03)
        latex.SetTextAlign(13)
        latex.DrawLatex( .12, .88, PullPlots[i][1] )
#        latex.DrawLatex( .12, .85, "#color[2]{Before Theta}" )
#        latex.DrawLatex( .15, .81, "#color[2]{#mu: " + str("%.4f" % FitResultBefore[i].Parameter(1)) + "}" )
#        latex.DrawLatex( .15, .78, "#color[2]{#sigma: " + str("%.4f" % FitResultBefore[i].Parameter(2)) + "}" )
        
        latex.DrawLatex( .12, .85, "#color[4]{Before Theta}" )
        latex.DrawLatex( .15, .81, "#color[4]{#mu: " + str("%.4f" % FitResultAfter[i].Parameter(1)) + "}" )
        latex.DrawLatex( .15, .78, "#color[4]{#sigma: " + str("%.4f" % FitResultAfter[i].Parameter(2)) + "}" )
        
    C8.SaveAs( "outputs/"+directory+method+"/PullPlotDist"+method+".png" )
