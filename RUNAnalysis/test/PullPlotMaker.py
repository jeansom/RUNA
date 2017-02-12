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

def PullPlotMaker( chan, chanCuts, bins, minBin, maxBin, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleAlpha, scaleAlphaErr, isMC=True ):
    gStyle.SetOptStat(0)
    #gRoot.cd()
    # Setting basic distributions
    weight = "(2666*puWeight*lumiWeight)"

    TTScaleStr = "((1+.2*"+str(scaleTT)+")*1.06*exp((-0.0005*HT/2)*(1+.2*"+str(scaleAlpha)+")))"
#    TTScaleStr = "(1)"
    TTScaleErrUpStr = "((1+.2*"+str(scaleTT)+"+.2*"+str(scaleTTErr)+")*1.06*exp((-0.0005*HT/2)*(1+.2*"+str(scaleAlpha)+")))"
    TTScaleErrDnStr = "((1+.2*"+str(scaleTT)+"-.2*"+str(scaleTTErr)+")*1.06*exp((-0.0005*HT/2)*(1+.2*"+str(scaleAlpha)+")))"
    AlphaScaleUpStr = "((1+.2*"+str(scaleTT)+")*1.06*exp((-0.0005*HT/2)*(1+.2*"+str(scaleAlpha)+"-.2*"+str(scaleAlphaErr)+")))"
    AlphaScaleDnStr = "((1+.2*"+str(scaleTT)+")*1.06*exp((-0.0005*HT/2)*(1+.2*"+str(scaleAlpha)+"+.2*"+str(scaleAlphaErr)+")))"

    WScaleStr = "(1+.2*"+str(scaleW)+")"
    WScaleUpStr = "(1+.2*"+str(scaleW)+"+.2*"+str(scaleWErr)+")"
    WScaleDnStr = "(1+.2*"+str(scaleW)+"-.2*"+str(scaleWErr)+")"

    print TTScaleStr
    print TTScaleErrUpStr
    print TTScaleErrDnStr
    print AlphaScaleUpStr
    print AlphaScaleDnStr
    print WScaleStr
    print WScaleUpStr
    print WScaleDnStr

    DATA = DIST( "DATA", "RootFiles/RUNAnalysis_JetHT_Run2015D-16Dec2015-v1_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", "1" )
    QCD = DIST( "QCD", "RootFiles/RUNAnalysis_QCDPtAll_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", "1*"+weight )
    SIG = DIST( "SIG", "RootFiles/RUNAnalysis_RPVStopStopToJets_UDD323_M-100_RunIISummer16MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", weight )

    TTJets = DIST( "TTJets", "RootFiles/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*"+TTScaleStr+")" )
    TTJetsUp = DIST( "TTJetsUp", "RootFiles/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*"+TTScaleErrUpStr+")" )
    TTJetsDn = DIST( "TTJetsDn", "RootFiles/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*"+TTScaleErrDnStr+")"  )
    TTJetsAlphaUp = DIST( "TTJetsUp", "RootFiles/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*"+AlphaScaleUpStr+")")
    TTJetsAlphaDn = DIST( "TTJetsDn", "RootFiles/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree",  "("+weight+"*"+AlphaScaleDnStr+")" )

    WJets = DIST( "WJets", "RootFiles/RUNAnalysis_WJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree",  "("+weight+"*"+WScaleStr+")" )
    WJetsUp = DIST( "WJetsUp", "RootFiles/RUNAnalysis_WJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*"+WScaleUpStr+")" )
    WJetsDn = DIST( "WJetsDn", "RootFiles/RUNAnalysis_WJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*"+WScaleDnStr+")" )

    WW = DIST( "WW", "RootFiles/RUNAnalysis_WWTo4Q_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", weight )
    WZ = DIST( "WZ", "RootFiles/RUNAnalysis_WZ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", weight )
    ZZ = DIST( "ZZ", "RootFiles/RUNAnalysis_ZZTo4Q_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", weight )
    ZJets = DIST( "ZJets", "RootFiles/RUNAnalysis_ZJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", weight )
    Sig = DIST( "Sig", "RootFiles/RUNAnalysis_RPVStopStopToJets_UDD323_M-100_RunIISummer16MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", weight )

    # Creating Alphabet objects to run estimate on    
    if isMC: 
        Dists = [ QCD, TTJets, WJets, WW, ZZ, ZJets, WW, ZZ, ZJets ]
    else: 
        Dists = [DATA]
    DistsSub = [ WJets, TTJets ]
    print random.random()
    print str(Dists)
    ## Defining Cuts
    presel = "jet1Tau21<0.60&jet2Tau21<0.60"
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
#    FMass = SigmoidFit([8.62e-01,-1.64,-5.98e-07],60,350,"Mass","SEMR")
#    FMass1 = SigmoidFit([8.62e-01,-1.64,-5.98e-07],60,350,"Mass1","SEMR")
#    FMassWJUp = SigmoidFit([8.62e-01,-1.64,-5.98e-07],60,350,"Mass","SEMR")
#    FMassWJDn = SigmoidFit([8.62e-01,-1.64,-5.98e-07],60,350,"Mass","SEMR")
#    FMassTTUp = SigmoidFit([8.62e-01,-1.64,-5.98e-07],60,350,"Mass","SEMR")
#    FMassTTDn = SigmoidFit([8.62e-01,-1.64,-5.98e-07],60,350,"Mass","SEMR")

    FMass = SigmoidFit([1.829,0.3742,-3.046e-07],60,350,"Mass","SEMR")
    FMass1 = SigmoidFit([1.829,0.3742,-3.046e-07],60,350,"Mass1","SEMR")
    FMassWJUp = SigmoidFit([1.829,0.3742,-3.046e-07],60,350,"Mass","SEMR")
    FMassWJDn = SigmoidFit([1.829,0.3742,-3.046e-07],60,350,"Mass","SEMR")
    FMassTTUp = SigmoidFit([1.829,0.3742,-3.046e-07],60,350,"Mass","SEMR")
    FMassTTDn = SigmoidFit([1.829,0.3742,-3.046e-07],60,350,"Mass","SEMR")

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
    MakeFitPlots( EstMass, FMass, binsMass, "prunedMassAve", Xcut[0], var_arrayMass, presel+"&"+chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "", "outputs/"+directory+method+"/Mass"+chan, False )
    MakeEstPlots( EstMass, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/Mass"+chan, False )



parser = argparse.ArgumentParser()
parser.add_argument( '-c', '--channel', action='store', dest='channel', default=1, help='Channel')
parser.add_argument( '-p_t', '--plot_true', action='store_true', dest='plot', help='Create plots')
parser.add_argument( '-p_f', '--plot_false', action='store_false', dest='plot', help='Don\'t create plots')
parser.add_argument( '-m', '--method', action='store', dest='method', default="CBDCMVAv2MC", help='Method')
parser.add_argument( '-d', '--directory', action='store', dest='directory', default = "", help='Directory')
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

os.mkdir("outputs/"+directory+method)

if "CSVv2" in method:
    zerobtag = "(jet1btagCSVv2<0.800&jet2btagCSVv2<0.800)"
    onebtag = "((jet1btagCSVv2<0.800&jet2btagCSVv2>0.800)||(jet1btagCSVv2>0.800&jet2btagCSVv2<0.800))"
    twobtag = "(jet1btagCSVv2>0.800&jet2btagCSVv2>0.800)"
    jet1btag = "((jet1btagCSVv2>0.800&jet2btagCSVv2<0.800))"
    jet2btag = "((jet1btagCSVv2<0.800&jet2btagCSVv2>0.800))"
elif "CMVAv2" in method:
    zerobtag = "(jet1btagCMVAv2<0.185&jet2btagCMVAv2<0.185)"
    onebtag = "((jet1btagCMVAv2<0.185&jet2btagCMVAv2>0.185)||(jet1btagCMVAv2>0.185&jet2btagCMVAv2<0.185))"
    twobtag = "(jet1btagCMVAv2>0.185&jet2btagCMVAv2>0.185)"
    jet1btag = "((jet1btagCMVAv2>0.185&jet2btagCMVAv2<0.185))"
    jet2btag = "((jet1btagCMVAv2<0.185&jet2btagCMVAv2>0.185))"
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

scaleTT = 0
scaleTTErr = 1
scaleW = 0
scaleWErr = 1
scaleTTAlpha = 0
scaleTTAlphaErr = 1

if 'After' in method:
    if 'CMVAv2' in method and 'BCD' in method:
        scaleTT = -2.466716391971068
        scaleTTErr = 0.3825145184217229
        scaleW = -1.8645456037163752
        scaleWErr = 0.7210115712655194
        scaleTTAlpha = -0.01377822965013209
        scaleTTAlphaErr = 0.7623511011898141

    elif 'CMVAv2' in method and 'CBD' in method:
        scaleTT = -1.6060224271846248
        scaleTTErr = 0.3977839360314497
        scaleW = -2.0726278342064495
        scaleWErr = 0.7652219328330052
        scaleTTAlpha = -0.2813896060154786
        scaleTTAlphaErr = 0.9512163689797521

    elif 'CSVv2' in method and 'BCD' in method:
        scaleTT = -2.9214826431317977
        scaleTTErr = 0.424184944651101
        scaleW = -2.0373530693054573
        scaleWErr = 0.7302188356753758
        scaleTTAlpha = -0.21399024680198586
        scaleTTAlphaErr = 0.975734998912118

    elif 'CSVv2' in method and 'CBD' in method:
        scaleTT = -1.526406709774644
        scaleTTErr = 0.41083568392446335
        scaleW = -2.104939936257965
        scaleWErr = 0.7675366397367553
        scaleTTAlpha = -0.2689103077995032
        scaleTTAlphaErr = 0.9536375736158587

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

print scaleTT
print scaleTTErr
print scaleW
print scaleWErr
print scaleTTAlpha
print scaleTTAlphaErr

PullPlots = []
PullPlots2 = []
if int(channel) == 0:
    PullPlotMaker( "b0t0", zerobtag+"&"+zeroTop, 29, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, isMC )
if int(channel) == 1:
    PullPlotMaker( "b1t0", onebtag+"&"+zeroTop, 29, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, isMC )
if int(channel) == 2:
    PullPlotMaker( "b2t0", twobtag+"&"+zeroTop, 29, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, isMC )
if int(channel) == 3:
    PullPlotMaker( "b0t1", zerobtag+"&"+oneTop, 29, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, isMC )
if int(channel) == 4:
    PullPlotMaker( "b1t1", onebtag+"&"+oneTop, 29, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, isMC )
if int(channel) == 5:
    PullPlotMaker( "b2t1", twobtag+"&"+oneTop, 29, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, isMC )
if int(channel) == 6:
    PullPlotMaker( "b0t2", zerobtag+"&"+twoTop, 29, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, isMC )
if int(channel) == 7:
    PullPlotMaker( "b1t2", onebtag+"&"+twoTop, 29, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, isMC )
if int(channel) == 8:
    PullPlotMaker( "b2t2", twobtag+"&"+twoTop, 29, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, isMC )
if int(channel) == 9:
    PullPlotMaker( "b0t0", zerobtag+"&"+zeroTop, 29, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, isMC )
    PullPlotMaker( "b1t0", onebtag+"&"+zeroTop, 29, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, isMC )
    PullPlotMaker( "b2t0", twobtag+"&"+zeroTop, 29, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, isMC )
    PullPlotMaker( "b0t1", zerobtag+"&"+oneTop, 29, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, isMC )
    PullPlotMaker( "b1t1", onebtag+"&"+oneTop, 29, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, isMC )
    PullPlotMaker( "b2t1", twobtag+"&"+oneTop, 29, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, isMC )
    PullPlotMaker( "b0t2", zerobtag+"&"+twoTop, 29, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, isMC )
    PullPlotMaker( "b1t2", onebtag+"&"+twoTop, 29, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, isMC )
    PullPlotMaker( "b2t2", twobtag+"&"+twoTop, 29, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, isMC )
if int(channel) == 10:
    PullPlotMaker( "pres", "abs(jet1Pt)>-999", 58, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, isMC )


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

#    PullPlots.append( [ TFile.Open("outputs/AfterThetaPull12617/221710CMVAv2MBCDDATAAfter/Massprespull.root") ] )
#    PullPlots2.append( [ TFile.Open("outputs/AfterThetaPull12617/221710CMVAv2MBCDDATA/Massprespull.root") ] )

    directory2 = directory.replace("After","Before")
    method2 = method.replace("After","Before")

    print directory2
    print method2

    PullPlots2.append( [ TFile.Open("outputs/"+directory2+"0"+method2+"/Massb0t0pull.root"), "Zero btags, Zero top-tags" ] )
    PullPlots2.append( [ TFile.Open("outputs/"+directory2+"1"+method2+"/Massb1t0pull.root"), "One btag, Zero top-tags" ] )
    PullPlots2.append( [ TFile.Open("outputs/"+directory2+"2"+method2+"/Massb2t0pull.root"), "Two btags, Zero top-tags" ] )
    PullPlots2.append( [ TFile.Open("outputs/"+directory2+"3"+method2+"/Massb0t1pull.root"), "Zero btags, One top-tag" ] )
    PullPlots2.append( [ TFile.Open("outputs/"+directory2+"4"+method2+"/Massb1t1pull.root"), "One btag, One top-tag" ] )
    PullPlots2.append( [ TFile.Open("outputs/"+directory2+"5"+method2+"/Massb2t1pull.root"), "Two btags, One top-tag" ] )
    PullPlots2.append( [ TFile.Open("outputs/"+directory2+"6"+method2+"/Massb0t2pull.root"), "Zero btags, Two top-tags" ] )
    PullPlots2.append( [ TFile.Open("outputs/"+directory2+"7"+method2+"/Massb1t2pull.root"), "One btag, Two top-tags" ] )
    PullPlots2.append( [ TFile.Open("outputs/"+directory2+"8"+method2+"/Massb2t2pull.root"), "Two btags, Two top-tags" ] )

    C7 = TCanvas( "C", "", 800, 800 )
    sum6 = 0
    FitMet = []
    FitMet2 = []
    Fits = []
    Results = []
    for i in xrange(len(PullPlots)):
#        C7.cd(i+1)

        FitMet.append(TH1D("h0"+str(i),"", PullPlots[i][0].Get("fitMetric_quad").GetNbinsX(), 60, 350 ) )
        for bin in range(0, FitMet[i].GetNbinsX()+1):
            FitMet[i].SetBinContent( bin, PullPlots[i][0].Get("fitMetric_quad").GetBinContent(bin) )

        FitMet2.append(TH1D("h1"+str(i),"", PullPlots2[i][0].Get("fitMetric_quad").GetNbinsX(), 60, 350 ) )
        for bin in range(0, FitMet2[i].GetNbinsX()+1):
            FitMet2[i].SetBinContent( bin, PullPlots2[i][0].Get("fitMetric_quad").GetBinContent(bin) )

    pullDistBefore = TH1D( "pullDistBefore", "", 20, -10, 10 )
    pullDistAfter = TH1D( "pullDistAfter", "", 20, -10, 10 )

    for i in xrange(len(FitMet)):
        for bin in range(0, FitMet[i].GetNbinsX()+1):
            pullDistAfter.Fill( FitMet[i].GetBinContent(bin) )
        for bin in range(0, FitMet2[i].GetNbinsX()+1):
            pullDistBefore.Fill( FitMet2[i].GetBinContent(bin) )

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

    FitResultBefore = pullDistBefore.Fit( "gaus", "S", "", -10, 10 )
    FitBefore = pullDistBefore.GetFunction("gaus").Clone()
    FitResultAfter = pullDistAfter.Fit( "gaus", "S", "", -10, 10 )
    FitAfter = pullDistAfter.GetFunction("gaus").Clone()
    
    pullDistAfter.SetLineColor(kBlue)
    pullDistAfter.SetLineWidth(2)
    gStyle.SetHatchesSpacing(1)
    
    pullDistBefore.SetLineColor(kRed)
    pullDistBefore.SetLineWidth(2)
    
    FindAndSetMax( [pullDistAfter, pullDistBefore], False)
    
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

    C7.SaveAs( "outputs/"+directory+method+"/PullPlotQuadMetric1"+method+".png" )

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
    FitMet = []
    Fits = []
    Results = []
    for i in xrange(len(PullPlots)):
        C.cd(i+1)

        FitMet.append(TH1D("h"+str(i),"", PullPlots[i][0].Get("fitMetric_div").GetNbinsX(), 60, 350 ) )
        for bin in range(0, FitMet[i].GetNbinsX()+1):
            FitMet[i].SetBinContent( bin, PullPlots[i][0].Get("fitMetric_div").GetBinContent(bin) )

        FitMet[i].GetXaxis().SetNdivisions(504)
        FitMet[i].GetYaxis().SetLabelSize(.06)
        FitMet[i].GetXaxis().SetLabelSize(.06)
        FitMet[i].GetYaxis().SetTitleSize(0)
        FitMet[i].GetXaxis().SetTitle("Average Pruned Mass [GeV]")
        FitMet[i].GetXaxis().SetTitleSize(0.06)
        FitMet[i].SetFillColor(kBlue)

        FitMet[i].Sumw2()
        Fits.append(TF1("f"+str(i), "[0] + [1]*x", 60, 350 ))
        Fits[i].SetLineColor(kRed)
        Results.append(FitMet[i].Fit("f"+str(i), "S", "", 60, 350))
        FitMet[i].Draw("hist")
        Fits[i].Draw("same")
        FitMet[i].GetYaxis().SetRangeUser(-3,3)
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

    C.SaveAs( "outputs/"+directory+method+"/PullPlotDivMetric"+method+".png" )

    C5 = TCanvas( "C", "", 800, 800 )
    C5.Divide(3,3)
    C5.SetTitle( "Pull/Error" )

    sum5 = 0
    FitMet = []
    FitMet2 = []
    Fits = []
    Results = []
    for i in xrange(len(PullPlots)):
        C5.cd(i+1)

        FitMet.append(TH1D("h"+str(i),"", PullPlots[i][0].Get("fitMetric_quad").GetNbinsX(), 60, 350 ) )
        for bin in range(0, FitMet[i].GetNbinsX()+1):
            FitMet[i].SetBinContent( bin, PullPlots[i][0].Get("fitMetric_quad").GetBinContent(bin) )

        FitMet2.append(TH1D("h"+str(i),"", PullPlots2[i][0].Get("fitMetric_quad").GetNbinsX(), 60, 350 ) )
        for bin in range(0, FitMet2[i].GetNbinsX()+1):
            FitMet2[i].SetBinContent( bin, PullPlots2[i][0].Get("fitMetric_quad").GetBinContent(bin) )

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
        FitMet[i].Sumw2()

        Fits.append(TF1("f"+str(i), "[0] + [1]*x", 60, 350 ))
        Fits[i].SetLineColor(kRed)
        Results.append(FitMet[i].Fit("f"+str(i), "S", "", 60, 350))
        FitMet[i].Draw("hist")
#        Fits[i].Draw("same")
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
        latex.DrawLatex( .2, .95, "#color[2]{Before Theta: Integral="+"{0:.5f}".format(FitMet2[i].Integral())+"}" )
        latex.DrawLatex( .2, .90, "#color[4]{After Theta: Integral="+"{0:.5f}".format(FitMet[i].Integral())+"}" )
#        latex.DrawLatex( .2, .90, "#color[2]{Linear Fit: " + str( "%.4f" % Results[i].Parameter(1)) + "*x + " + str( "%.4f" % Results[i].Parameter(0)) + "}" )
#        latex.DrawLatex( .2, .95, "Integral: " + "{0:.5f}".format(FitMet[i].Integral()) )
        sum5 = sum5+FitMet[i].Integral()

    print sum5

    C5.SaveAs( "outputs/"+directory+method+"/PullPlotQuadMetric"+method+".png" )

    C6 = TCanvas( "C", "", 800, 800 )
    C6.Divide(3,3)
    C6.SetTitle( "Pull/Error" )

    sum6 = 0
    FitMet = []
    Fits = []
    Results = []
    for i in xrange(len(PullPlots)):
        C6.cd(i+1)

        FitMet.append(TH1D("h"+str(i),"", PullPlots[i][0].Get("Pull_norm").GetNbinsX(), 60, 350 ) )
        for bin in range(0, FitMet[i].GetNbinsX()+1):
            FitMet[i].SetBinContent( bin, PullPlots[i][0].Get("Pull_norm").GetBinContent(bin) )

        FitMet[i].GetXaxis().SetNdivisions(504)
        FitMet[i].GetYaxis().SetLabelSize(.06)
        FitMet[i].GetXaxis().SetLabelSize(.06)
        FitMet[i].GetYaxis().SetTitleSize(0)
        FitMet[i].GetXaxis().SetTitle("Average Pruned Mass [GeV]")
        FitMet[i].GetXaxis().SetTitleSize(0.06)
        FitMet[i].SetFillColor(kBlue)
        FitMet[i].Sumw2()
        Fits.append(TF1("f"+str(i), "[0] + [1]*x", 60, 350 ))
        Fits[i].SetLineColor(kRed)
        Results.append(FitMet[i].Fit("f"+str(i), "S", "", 60, 350))
        FitMet[i].Draw("hist")
        Fits[i].Draw("same")

        FitMet[i].GetYaxis().SetRangeUser(-3,3)
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

    C6.SaveAs( "outputs/"+directory+method+"/PullPlotMetric"+method+".png" )


    C2 = TCanvas( "C2", "", 800, 800 )
    C2.cd()
    allPull = PullPlots[0][0].Get("Pull_norm").Clone()
    allPull.Reset()
    for i in xrange(len(PullPlots)):
        allPull.Add(PullPlots[i][0].Get("Pull_norm").Clone())

    allPull.GetXaxis().SetNdivisions(504)
    allPull.GetYaxis().SetLabelSize(.03)
    allPull.GetYaxis().SetTitleSize(0)
    allPull.GetXaxis().SetTitle( "Average Pruned Mass [GeV]" )
    
    allPull.Draw()
    latex2 = TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.05)
    latex.SetTextAlign(13)
    latex.DrawLatex( .4, .8, "Sum of pull plots" )
    
    C2.SaveAs("outputs/"+directory+method+"/sumPull.png")
    
    C3 = TCanvas( "C3", "", 800, 800 )
    C3.cd()
    avePull = PullPlots[0][0].Get("Pull_norm").Clone()
    avePull.Reset()
    for i in xrange(len(PullPlots)):
        avePull.Add(PullPlots[i][0].Get("Pull_norm").Clone())

    for i in range(1, avePull.GetNbinsX()+1 ):
        bin = avePull.GetBinContent(i)
        avePull.SetBinContent( i, bin/9 )

    avePull.GetXaxis().SetNdivisions(504)
    avePull.GetYaxis().SetLabelSize(.03)
    avePull.GetYaxis().SetTitleSize(0)
    avePull.GetXaxis().SetTitle( "Average Pruned Mass [GeV]" )
    avePull.SetFillColor(kBlue)
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
    
    C4 = TCanvas( "C4", "", 800, 800 )
    C4.Divide(3,3)
    C4.SetTitle( "Pull/Error" )
    
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
    P = []
    PFit = []
    PResult = []
    for i in xrange(len(PullPlots)):
        gStyle.SetOptStat(0)
        C4.cd(i+1)
        P.append(TH1D("h"+str(i),"", PullPlots[i][0].Get("fitMetric_div").GetNbinsX(), 60, 350 ) )
        for bin in range(0, P[i].GetNbinsX()+1):
            P[i].SetBinContent( bin, PullPlots[i][0].Get("fitMetric_div").GetBinContent(bin) )
        PFit.append(TF1("f"+str(i), "[0] + [1]*x", 60, 350 ))
        PResult.append(P[i].Fit("f"+str(i), "S", "", 60, 350))
    #    PFit = (P[i].GetFunction(f1)).Clone()
        PFit[i].SetLineColor(kRed)
        P[i].GetXaxis().SetNdivisions(504)
        P[i].GetYaxis().SetLabelSize(.06)
        P[i].GetYaxis().SetTitleSize(0)
        P[i].SetFillColor(kBlue)
        P[i].Draw("hist")
        P[i].GetYaxis().SetRangeUser(-3,3)
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
        latex.DrawLatex( .2, 1, "#color[4]{"+PullPlots[i][1]+"}" )
        latex.DrawLatex( .2, .95, "#color[2]{Linear Fit: " + str( "%.4f" % PResult[i].Parameter(1)) + "*x + " + str( "%.4f" % PResult[i].Parameter(0)) + "}" )
        #    latex.DrawLatex( .23, .90, "#color[2]{m: " + str( "%.4f" % PResult[i].Parameter(1)) + "}" )
        #    latex.DrawLatex( .23, .85, "#color[2]{b: " + str( "%.4f" % PResult[i].Parameter(0)) + "}" )
        latex.DrawLatex( .2, .90, "Integral: " + "{0:.5f}".format(P[i].Integral()) )
        sum7 = sum7+P[i].Integral()

    print sum7
    
    print "sum1: " + str(sum1)
    print "sum5: " + str(sum5)
    print "sum6: " + str(sum6)

    C4.SaveAs( "outputs/"+directory+method+"/PullPlotFit"+method+".png" )


    C8 = TCanvas( "C", "", 800, 800 )
    C8.Divide(3,3)
    sum6 = 0
    FitMet = []
    FitMet2 = []
    Fits = []
    Results = []
    for i in xrange(len(PullPlots)):
        C8.cd(i+1)

        FitMet.append(TH1D("h0"+str(i),"", PullPlots[i][0].Get("Pull_norm").GetNbinsX(), 60, 350 ) )
        for bin in range(0, FitMet[i].GetNbinsX()+1):
            FitMet[i].SetBinContent( bin, PullPlots[i][0].Get("Pull_norm").GetBinContent(bin) )

        FitMet2.append(TH1D("h1"+str(i),"", PullPlots2[i][0].Get("Pull_norm").GetNbinsX(), 60, 350 ) )
        for bin in range(0, FitMet2[i].GetNbinsX()+1):
            FitMet2[i].SetBinContent( bin, PullPlots2[i][0].Get("Pull_norm").GetBinContent(bin) )

    pullDistBefore = []
    pullDistAfter = []
    FitResultBefore = []
    FitBefore = []
    FitResultAfter = []
    FitAfter = []

    for i in xrange(len(FitMet)):
        C8.cd(i+1)
        pullDistBefore.append(TH1D( "pullDistBefore" + str(i), "", 20, -10, 10 ))
        pullDistAfter.append(TH1D( "pullDistAfter[i]" + str(i), "", 20, -10, 10 ))

        for bin in range(0, FitMet[i].GetNbinsX()+1):
            pullDistAfter[i].Fill( FitMet[i].GetBinContent(bin) )
        for bin in range(0, FitMet2[i].GetNbinsX()+1):
            pullDistBefore[i].Fill( FitMet2[i].GetBinContent(bin) )

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
        
        FitResultBefore.append(pullDistBefore[i].Fit( "gaus", "S", "", -10, 10 ))
        FitBefore.append(pullDistBefore[i].GetFunction("gaus").Clone())
        FitResultAfter.append(pullDistAfter[i].Fit( "gaus", "S", "", -10, 10 ))
        FitAfter.append(pullDistAfter[i].GetFunction("gaus").Clone())
        
        pullDistAfter[i].SetLineColor(kBlue)
        pullDistAfter[i].SetLineWidth(2)
        gStyle.SetHatchesSpacing(1)
        
        pullDistBefore[i].SetLineColor(kRed)
        pullDistBefore[i].SetLineWidth(2)
        
        FindAndSetMax( [pullDistAfter[i], pullDistBefore[i]], False)
        
        pullDistAfter[i].Draw("hist")
        pullDistBefore[i].Draw("hist same")
        
        FitBefore[i].SetLineColor(kRed)
        FitAfter[i].SetLineColor(kBlue)
        FitBefore[i].SetLineStyle(2)
        FitAfter[i].SetLineStyle(2)
        
        FitBefore[i].Draw("same")
        FitAfter[i].Draw("same")
        
        T0 = TLine(0,0,0,pullDistAfter[i].GetMaximum())
        T0.SetLineWidth(2)
        T0.SetLineColor(19)
        #    T0.SetLineStyle(3)
        #    T0.Draw("same")
        
        CMS_lumi.extraText = "Preliminary"
        CMS_lumi.relPosX = 0.15
        CMS_lumi.CMS_lumi( C8.GetPad(i+1), 4, 0)
        latex = TLatex()
        latex.SetNDC()
        latex.SetTextSize(0.03)
        latex.SetTextAlign(13)
        latex.DrawLatex( .12, .88, PullPlots[i][1] )
        latex.DrawLatex( .12, .85, "#color[2]{Before Theta}" )
        latex.DrawLatex( .15, .81, "#color[2]{#mu: " + str("%.4f" % FitResultBefore[i].Parameter(1)) + "}" )
        latex.DrawLatex( .15, .78, "#color[2]{#sigma: " + str("%.4f" % FitResultBefore[i].Parameter(2)) + "}" )
        
        latex.DrawLatex( .12, .73, "#color[4]{After Theta}" )
        latex.DrawLatex( .15, .70, "#color[4]{#mu: " + str("%.4f" % FitResultAfter[i].Parameter(1)) + "}" )
        latex.DrawLatex( .15, .67, "#color[4]{#sigma: " + str("%.4f" % FitResultAfter[i].Parameter(2)) + "}" )
        
    C8.SaveAs( "outputs/"+directory+method+"/PullPlotDist"+method+".png" )
    C8 = TCanvas( "C", "", 800, 800 )
    C8.Divide(3,3)
    sum6 = 0
    FitMet = []
    FitMet2 = []
    Fits = []
    Results = []
    for i in xrange(len(PullPlots)):
        C8.cd(i+1)

        FitMet.append(TH1D("h0"+str(i),"", PullPlots[i][0].Get("fitMetric_quad").GetNbinsX(), 60, 350 ) )
        for bin in range(0, FitMet[i].GetNbinsX()+1):
            FitMet[i].SetBinContent( bin, PullPlots[i][0].Get("fitMetric_quad").GetBinContent(bin) )

        FitMet2.append(TH1D("h1"+str(i),"", PullPlots2[i][0].Get("fitMetric_quad").GetNbinsX(), 60, 350 ) )
        for bin in range(0, FitMet2[i].GetNbinsX()+1):
            FitMet2[i].SetBinContent( bin, PullPlots2[i][0].Get("fitMetric_quad").GetBinContent(bin) )

    pullDistBefore = []
    pullDistAfter = []
    FitResultBefore = []
    FitBefore = []
    FitResultAfter = []
    FitAfter = []

    for i in xrange(len(FitMet)):
        C8.cd(i+1)
        pullDistBefore.append(TH1D( "pullDistBefore" + str(i), "", 20, -10, 10 ))
        pullDistAfter.append(TH1D( "pullDistAfter" + str(i), "", 20, -10, 10 ))

        for bin in range(0, FitMet[i].GetNbinsX()+1):
            pullDistAfter[i].Fill( FitMet[i].GetBinContent(bin) )
        for bin in range(0, FitMet2[i].GetNbinsX()+1):
            pullDistBefore[i].Fill( FitMet2[i].GetBinContent(bin) )

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
        
        FitResultBefore.append(pullDistBefore[i].Fit( "gaus", "S", "", -10, 10 ))
        FitBefore.append(pullDistBefore[i].GetFunction("gaus").Clone())
        FitResultAfter.append(pullDistAfter[i].Fit( "gaus", "S", "", -10, 10 ))
        FitAfter.append(pullDistAfter[i].GetFunction("gaus").Clone())
        
        pullDistAfter[i].SetLineColor(kBlue)
        pullDistAfter[i].SetLineWidth(2)
        gStyle.SetHatchesSpacing(1)
        
        pullDistBefore[i].SetLineColor(kRed)
        pullDistBefore[i].SetLineWidth(2)
        
        FindAndSetMax( [pullDistAfter[i], pullDistBefore[i]], False)
        
        pullDistAfter[i].Draw("hist")
        pullDistBefore[i].Draw("hist same")
        
        FitBefore[i].SetLineColor(kRed)
        FitAfter[i].SetLineColor(kBlue)
        FitBefore[i].SetLineStyle(2)
        FitAfter[i].SetLineStyle(2)
        
        FitBefore[i].Draw("same")
        FitAfter[i].Draw("same")
        
        T0 = TLine(0,0,0,pullDistAfter[i].GetMaximum())
        T0.SetLineWidth(2)
        T0.SetLineColor(19)
        #    T0.SetLineStyle(3)
        #    T0.Draw("same")
        
        CMS_lumi.extraText = "Preliminary"
        CMS_lumi.relPosX = 0.15
        CMS_lumi.CMS_lumi(C8, 4, 0)
        latex = TLatex()
        latex.SetNDC()
        latex.SetTextSize(0.03)
        latex.SetTextAlign(13)
        latex.DrawLatex( .12, .85, "#color[2]{Before Theta}" )
        latex.DrawLatex( .15, .81, "#color[2]{#mu: " + str("%.4f" % FitResultBefore[i].Parameter(1)) + "}" )
        latex.DrawLatex( .15, .78, "#color[2]{#sigma: " + str("%.4f" % FitResultBefore[i].Parameter(2)) + "}" )
        
        latex.DrawLatex( .12, .73, "#color[4]{After Theta}" )
        latex.DrawLatex( .15, .70, "#color[4]{#mu: " + str("%.4f" % FitResultAfter[i].Parameter(1)) + "}" )
        latex.DrawLatex( .15, .67, "#color[4]{#sigma: " + str("%.4f" % FitResultAfter[i].Parameter(2)) + "}" )
        
    C8.SaveAs( "outputs/"+directory+method+"/PullPlotQuadMetric"+method+".png" )
