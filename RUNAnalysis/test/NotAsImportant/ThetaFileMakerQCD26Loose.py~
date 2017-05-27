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
from RUNA.RUNAnalysis.scaleFactors import *

# Runs the full background estimation and creates a root file that theta can run over
# SHOULD SPLIT UP TO DO EACH BKG EST SEPARATELY, AKA TTUP, TTAlphaUP...
#### chan: The channel to run the background estimation for (ex: b0t0, b1t0...)
#### chanCuts: The cuts that define chan
#### bins: bin width for the final estimation plot
#### minBin: minimum value for the final estimation plot
#### maxBin: maximum value for the final estimation plot
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
def ThetaFileMaker( chan, chanCuts, bins, minBin, maxBin, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleAlpha, scaleAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, fitBins, HT, fit=False, isMC=True, log=True ):
    gStyle.SetOptStat(0)
    # Setting basic distributions
    # Setting basic distributions
    weight = "(36555.21/15*lumiWeight*puWeight)"

    print scaleTT
    print scaleTTErr

    # The T and W scales
    TTNorm = "( (1.06)*(1+.2*"+str(scaleTT)+"))" # The scale that determines the nominal TTBar normalization
    TTNormUp = "( (1.06)*(1+.2*" + str(scaleTT) + "+.2*" + str(scaleTTErr) + ") )" # Upper TTBar normalization
    TTNormDn = "( (1.06)*(1+.2*" + str(scaleTT) + "-.2*" + str(scaleTTErr) + ") )" # Lower TTBar normalization

#    TTAlpha = "exp( (-0.0005*(genPartonPt1+genPartonPt2))*(1-.2*" + str(scaleAlpha) + ") )" # The scale that determines the nominal alpha NOTE: subtracting = adding because -0.0005
#    TTAlphaUp = "exp( (-0.0005*(genPartonPt1+genPartonPt2))*(1-.2*" + str(scaleAlpha) + "-.2*" + str(scaleAlphaErr) + ") )" # Upper alpha NOTE: subtracting = adding because -0.0005
#    TTAlphaDn = "exp( (-0.0005*(genPartonPt1+genPartonPt2))*(1-.2*" + str(scaleAlpha) + "+.2*" + str(scaleAlphaErr) + ") )" # Lower alpha NOTE: subtracting = adding because -0.0005
    TTAlpha = "exp( (-0.0005*(HT/2))*(1-.2*" + str(scaleAlpha) + ") )" # The scale that determines the nominal alpha NOTE: subtracting = adding because -0.0005
    TTAlphaUp = "exp( (-0.0005*(HT/2))*(1-.2*" + str(scaleAlpha) + "-.2*" + str(scaleAlphaErr) + ") )" # Upper alpha NOTE: subtracting = adding because -0.0005
    TTAlphaDn = "exp( (-0.0005*(HT/2))*(1-.2*" + str(scaleAlpha) + "+.2*" + str(scaleAlphaErr) + ") )" # Lower alpha NOTE: subtracting = adding because -0.0005

#    TTScaleStrNorm = "(1.06*exp( (-0.0005*(genPartonPt1+genPartonPt2)) ))"
    TTScaleStrNorm = "(1.06*exp( (-0.0005*(HT/2)) ))"
    TTScaleStr = "(" + TTNorm + "*" + TTAlpha + ")" # Total string to scale TT by, norm*alpha
    TTScaleErrUpStr = "(" + TTNormUp + "*" + TTAlpha + ")" # String for scaling TT with norm up, normUp*alpha
    TTScaleErrDnStr = "(" + TTNormDn + "*" + TTAlpha + ")" # String for scaling TT with norm dn, normDn*alpha
    AlphaScaleUpStr = "(" + TTNorm + "*" + TTAlphaUp + ")" # Total string to scale TT by with alpha up, norm*alphaUp
    AlphaScaleDnStr = "(" + TTNorm + "*" + TTAlphaDn + ")" # Total string to scale TT by with alpha dn, norm*alphaDn

    print TTScaleStr

    WScaleStr = "(1+.2*"+str(scaleW)+")" # The scale that determines the nominal W normalization
    WScaleUpStr = "(1+.2*"+str(scaleW)+"+.2*"+str(scaleWErr)+")" # Upper W normalization
    WScaleDnStr = "(1+.2*"+str(scaleW)+"-.2*"+str(scaleWErr)+")" # Lower W normalization

    TopScaleStr = "(1+.2*"+str(scaleTop)+")"
    TopScaleUpStr = "(1+.2*"+str(scaleTop)+"+2*"+str(scaleTopErr)+")"
    TopScaleDnStr = "(1+.2*"+str(scaleTop)+"-2*"+str(scaleTopErr)+")"

#    rootFileFolder = "80XRootFilesUpdated/UngroomedMass/ugm_"
    rootFileFolder = "80XRootFilesUpdated/"
    # Create the distributions
    DATA = DIST( "DATA", rootFileFolder+"RUNAnalysis_JetHT_Run2016_80X_V2p3_v06_cut15.root", "BoostedAnalysisPlotsPuppi/RUNATree", "1" )
    QCD = DIST( "QCD", rootFileFolder+"RUNAnalysis_QCDHTAll_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*"+weight )
    QCD1000to1400 = DIST( "QCD1000to1400", rootFileFolder+"RUNAnalysis_QCDPt1000to1400_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_1000to1400" )))
    QCD1400to1800 = DIST( "QCD1400to1800", rootFileFolder+"RUNAnalysis_QCDPt1400to1800_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_1400to1800" )))
    QCD170to300 = DIST( "QCD170to300", rootFileFolder+"RUNAnalysis_QCDPt170to300_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_170to300" )))
    QCD1800to2400 = DIST( "QCD1800to2400", rootFileFolder+"RUNAnalysis_QCDPt1800to2400_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_1800to2400" )))
    QCD2400to3200 = DIST( "QCD2400to3200", rootFileFolder+"RUNAnalysis_QCDPt2400to3200_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_2400to3200" )))
    QCD300to470 = DIST( "QCD300to470", rootFileFolder+"RUNAnalysis_QCDPt300to470_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_300to470" )))
    QCD3200toInf = DIST( "QCD3200toInf", rootFileFolder+"RUNAnalysis_QCDPt3200toInf_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_3200toInf" )))
    QCD470to600 = DIST( "QCD470to600", rootFileFolder+"RUNAnalysis_QCDPt470to600_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_470to600" )))
    QCD600to800 = DIST( "QCD600to800", rootFileFolder+"RUNAnalysis_QCDPt600to800_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_600to800" )))
    QCD800to1000 = DIST( "QCD800to1000", rootFileFolder+"RUNAnalysis_QCDPt800to1000_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor("QCD_Pt_800to1000" )))
    TTJetsNorm = DIST( "TTJets", rootFileFolder+"RUNAnalysis_TT_PtRewt_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "("+weight+"*"+TTScaleStrNorm+")" )
    TTJets = DIST( "TTJets", rootFileFolder+"RUNAnalysis_TT_PtRewt_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "("+weight+"*"+TTScaleStr+")" )
    TTJetsUp = DIST( "TTJetsUp", rootFileFolder+"RUNAnalysis_TT_PtRewt_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "("+weight+"*"+TTScaleErrUpStr+")" )
    TTJetsDn = DIST( "TTJetsDn", rootFileFolder+"RUNAnalysis_TT_PtRewt_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "("+weight+"*"+TTScaleErrDnStr+")"  )
    TTJetsAlphaUp = DIST( "TTJetsUp", rootFileFolder+"RUNAnalysis_TT_PtRewt_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "("+weight+"*"+AlphaScaleUpStr+")")
    TTJetsAlphaDn = DIST( "TTJetsDn", rootFileFolder+"RUNAnalysis_TT_PtRewt_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree",  "("+weight+"*"+AlphaScaleDnStr+")" )

    WJetsNorm = DIST( "WJets", rootFileFolder+"RUNAnalysis_WJetsToQQ_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree",  "("+weight+")" )
    WJets = DIST( "WJets", rootFileFolder+"RUNAnalysis_WJetsToQQ_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree",  "("+weight+"*"+WScaleStr+")" )
    WJetsUp = DIST( "WJetsUp", rootFileFolder+"RUNAnalysis_WJetsToQQ_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "("+weight+"*"+WScaleUpStr+")" )
    WJetsDn = DIST( "WJetsDn", rootFileFolder+"RUNAnalysis_WJetsToQQ_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "("+weight+"*"+WScaleDnStr+")" )

    TopNorm = DIST( "TopNorm", rootFileFolder+"RUNAnalysis_ST_t-channel_topantitop_4f_inclusiveDecays_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree",  "("+weight+")" )
    Top = DIST( "Top", rootFileFolder+"RUNAnalysis_ST_t-channel_topantitop_4f_inclusiveDecays_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree",  "("+weight+"*"+TopScaleStr+")" )
    TopUp = DIST( "TopUp", rootFileFolder+"RUNAnalysis_ST_t-channel_topantitop_4f_inclusiveDecays_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "("+weight+"*"+TopScaleUpStr+")" )
    TopDn = DIST( "TopDn", rootFileFolder+"RUNAnalysis_ST_t-channel_topantitop_4f_inclusiveDecays_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "("+weight+"*"+TopScaleDnStr+")" )

    Sig120 = DIST( "Sig", rootFileFolder+"/Signals/RUNAnalysis_RPVStopStopToJets_UDD323_M-120_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "puWeight*689.799/746680*100" )
    Sig280 = DIST( "Sig", rootFileFolder+"/Signals/RUNAnalysis_RPVStopStopToJets_UDD323_M-240_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "puWeight*26.476/153653*100" )

    # Creating Alphabet objects to run estimate on    
    if isMC: # If running over the MC
        Dists = [ QCD170to300, QCD300to470, QCD470to600, QCD600to800, QCD800to1000, QCD1000to1400, QCD1400to1800, QCD1800to2400, QCD2400to3200, QCD3200toInf ] # Use the MC distributions
#        Dists = [QCD]
        DistsSub = []
#        Dists = [ QCD170to300, QCD300to470, QCD470to600, QCD600to800, QCD800to1000, QCD1000to1400, QCD1400to1800, QCD1800to2400, QCD2400to3200, QCD3200toInf ] # Use the MC distributions
    else:  # Otherwise
        Dists = [DATA] # Use data 
        DistsSub = [ Top, WJets, TTJets ] # Nominal distributions to subtract
#    DistsSub = [ ] # Nominal distributions to subtract
    DistSig = [Sig120, Sig280]
    print DistsSub
    ## Defining Cuts
    rho = "(log((jet1PrunedMass*jet1PrunedMass)/(jet1Pt))+log((jet2PrunedMass*jet2PrunedMass)/(jet2Pt)))"
    presel = tau21#+"&"+HT+"&(0>"+rho+"&-20<"+rho+")" #"jet1Tau21<"+tau21+"&jet2Tau21<"+tau21
    cuts = Xcut[0]+"<"+Xcut[1]+"&"+Ycut[0]+"<"+Ycut[1]
    anticuts = Xcut[0]+">"+Xcut[1]+"&"+Ycut[0]+"<"+Ycut[1]
    cutsB = Xcut[0]+"<"+Xcut[1]+"&"+Ycut[0]+">"+Ycut[1]
    cutsD = Xcut[0]+">"+Xcut[1]+"&"+Ycut[0]+">"+Ycut[1]
    cut = [ float(Xcut[1]), "<" ] # For defining B vs D regions
    print DistsSub
    ## Average mass binned fit
    EstMass = Alphabet( "BkgEstMass", Dists, DistsSub, DistSig ) # Nominal
    EstMassWJUp = Alphabet( "BkgEstMassWJUp", Dists, [Top, WJetsUp, TTJets], DistSig ) # W norm. up
    EstMassWJDn = Alphabet( "BkgEstMassWJDn", Dists, [Top, WJetsDn, TTJets], DistSig ) # W norm. dn
    EstMassTTUp = Alphabet( "BkgEstMassTTUp", Dists, [Top, WJets, TTJetsUp], DistSig ) # T norm. up
    EstMassTTDn = Alphabet( "BkgEstMassTTDn", Dists, [Top, WJets, TTJetsDn], DistSig ) # T norm. dn
    EstMassTTAlphaUp = Alphabet( "BkgEstMassTTAlphaUp", Dists, [Top, WJets, TTJetsAlphaUp], DistSig ) # T alpha up
    EstMassTTAlphaDn = Alphabet( "BkgEstMassTTAlphaDn", Dists, [Top, WJets, TTJetsAlphaDn], DistSig ) # T alpha dn
    EstMassTopUp = Alphabet( "BkgEstMassTTAlphaUp", Dists, [TopUp, WJets, TTJets], DistSig ) # T alpha up
    EstMassTopDn = Alphabet( "BkgEstMassTTAlphaDn", Dists, [TopDn, WJets, TTJets], DistSig ) # T alpha dn
    
    TTBarO = TH1F("TTBarO", "", 29, 60, 350 )
    quickplot( TTJets.File, TTJets.Tree, TTBarO, "prunedMassAve", presel+"&"+cuts+"&"+chanCuts, TTScaleStrNorm+"*"+weight ) # Makes nominal T plot
    quickplot( WJets.File, WJets.Tree, TTBarO, "prunedMassAve", presel+"&"+cuts+"&"+chanCuts, weight ) # Makes nominal T plot
    

    #### Makes list with bins for fit
    binsMass = []
#    binWidth = 0.03125
    binWidth = 0.5
    NBins = int(((0+80))/binWidth)
    var_arrayMass = [ rho, Xcut[0], NBins, -40, 40., Xcut[2], Xcut[3], Xcut[4] ]
    binsMass = []
    bin = -40
    while bin < 40:
        binsMass.append( [bin, bin+10] )
        bin=bin+10
    '''
    binsMass.append([-100,-15])
    binsMass.append([-15,-10])
    binsMass.append([-10,-5.5])
#     for i in xrange( 0, 16 ):
#        binsMass.append( [ -5.5+0.0625*i, -5.5+0.0625*(i+1) ] )
    for i in xrange( 0, 4 ):
        binsMass.append( [ -5.5+0.0625*4*i, -5.5+0.0625*4*(i+1) ] )
    if "b0t0" in chan:
        for i in xrange( 0, 8 ):
            binsMass.append( [ (-4.5)+0.0625*i, (-4.5)+0.0625*(i+1) ] )
        for i in xrange( 0, 4 ):
            binsMass.append( [ -4+0.125*i, -4+0.125*(i+1) ] )
        for i in xrange( 0, 2 ):
            binsMass.append( [ -3.5+0.25*i, -3.5+0.25*(i+1) ] )       
        binsMass.append( [-3., 0.] )
    elif "b1t0" in chan:
        for i in xrange( 0, 8 ):
            binsMass.append( [ (-4.5)+0.0625*i, (-4.5)+0.0625*(i+1) ] )
        binsMass.append( [-4, -3.75] )
        binsMass.append( [-3.75, -3.5] )
        binsMass.append( [-3.5, -3.] )
        binsMass.append( [-3., 0.] )
    elif "b2t0" in chan:
        binsMass.append( [-4.5, -4.25] )
        binsMass.append( [-4.25, -4] )
        binsMass.append( [-4, -3.5] )
        binsMass.append( [-3.5, -3.] )
        binsMass.append( [-3., 0.] )
    elif "b0t1" in chan:
        for i in xrange( 0, 8 ):
            binsMass.append( [ (-4.5)+0.0625*i, (-4.5)+0.0625*(i+1) ] )
        binsMass.append( [-4, -3.75] )
        binsMass.append( [-3.75, -3.5] )
        binsMass.append( [-3.5, -3.] )
        binsMass.append( [-3., 0.] )
    elif "b1t1" in chan:
        binsMass.append( [-4.5, -4.25] )
        binsMass.append( [-4.25, -4] )
        binsMass.append( [-4, -3.5] )
        binsMass.append( [-3.5, -3.] )
        binsMass.append( [-3., 0.] )
    elif "b2t1" in chan:
        binsMass.append( [-4.5, -4.25] )
        binsMass.append( [-4.25, -4] )
        binsMass.append( [-4, -3.5] )
        binsMass.append( [-3.5, -3.] )
        binsMass.append( [-3., 0.] )
    elif "t2" in chan:
        binsMass.append( [-4.5, -4.25] )
        binsMass.append( [-4.25, -4] )
        binsMass.append( [-4, -3.5] )
        binsMass.append( [-3.5, -3.] )        
        binsMass.append( [-3., 0.] )
    else:
        for i in xrange( 0, 8 ):
            binsMass.append( [ (-4.5)+0.0625*i, (-4.5)+0.0625*(i+1) ] )
        for i in xrange( 0, 4 ):
            binsMass.append( [ -4+0.125*i, -4+0.125*(i+1) ] )
        for i in xrange( 0, 2 ):
            binsMass.append( [ -3.5+0.25*i, -3.5+0.25*(i+1) ] )       
        binsMass.append( [-3., 0.] )
        '''
    prelimFit = [-1,-1,-1,-1,-1]

    #### Form of fit
    FMass = QuadraticFit(prelimFit,-40,40,"Mass","SEMR") # Nominal fit
    FMass1 = QuadraticFit(prelimFit,-40,40,"Mass1","SEMR") # Nominal fit again, used if staying blinded

    FMassWJUp = QuadraticFit(prelimFit,-500,0,"Mass","SEMR") # Fit W norm. up
    FMassWJDn = QuadraticFit(prelimFit,-500,0,"Mass","SEMR") # Fit W norm. dn

    FMassTTUp = QuadraticFit(prelimFit,-500,0,"Mass","SEMR") # Fit T norm. up
    FMassTTDn = QuadraticFit(prelimFit,-500,0,"Mass","SEMR") # Fit T norm. dn
    FMassTTAlphaUp = QuadraticFit(prelimFit,-500,0,"Mass","SEMR") # Fit T alpha up
    FMassTTAlphaDn = QuadraticFit(prelimFit,-500,0,"Mass","SEMR") # Fit T alpha dn
    FMassTopUp = QuadraticFit(prelimFit,-500,0,"Mass","SEMR") # Fit T alpha up
    FMassTopDn = QuadraticFit(prelimFit,-500,0,"Mass","SEMR") # Fit T alpha dn

    # Bins for final estimation plot, bin width int(bins)
    '''
    minBin = 0
    maxBin = 1
    '''
    binBoundaries = []
    dBin = float(bins)
#    dBin = 0.05
    i = minBin
    print minBin
    print maxBin
    while i<=maxBin:
        binBoundaries.append(i)
        i=i+dBin
    # Use alternate channel's fits when low statistics
    if "t2" in chan: chanCutsTemp = presel+"&"+twoTop
    elif chan is "b2t1": chanCutsTemp = presel+"&"+onebtag+"&"+oneTop
    else: chanCutsTemp = presel+"&"+chanCuts

    # Nominal
    print log
    MakeFitPlots( EstMass, FMass, binsMass, "#rho", Xcut[0], var_arrayMass, chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "", "outputs/"+directory+method+"/Mass"+chan, binBoundaries, fit, False ) # Creates the 2D plot, ratio, and ratio fit
    MakeEstPlots( EstMass, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "HT", "", "outputs/"+directory+method+"/Mass"+chan, TTBarO, fit, isMC, False, log ) # Makes the actual estimation

    # W norm up
    MakeFitPlots( EstMassWJUp, FMassWJUp, binsMass, "#rho", Xcut[0], var_arrayMass, chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "",  "outputs/"+directory+method+"/MassWJUp"+chan, binBoundaries, fit, False ) # Creates the 2D plot, ratio, and ratio fit
    MakeEstPlots( EstMassWJUp, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/MassWJUp"+chan, TTBarO, fit, isMC, False, log ) # Makes the actual estimation

    # W norm dn
    MakeFitPlots( EstMassWJDn, FMassWJDn, binsMass, "#rho", Xcut[0], var_arrayMass, chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "", "outputs/"+directory+method+"/MassWJDn"+chan, binBoundaries, fit, False ) # Creates the 2D plot, ratio, and ratio fit
    MakeEstPlots( EstMassWJDn, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/MassWJDn"+chan, TTBarO, fit, isMC, False, log ) # Makes the actual estimation

    # T norm up
    MakeFitPlots( EstMassTTUp, FMassTTUp, binsMass, "#rho", Xcut[0], var_arrayMass, chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "", "outputs/"+directory+method+"/MassTTUp"+chan, binBoundaries, fit, False ) # Creates the 2D plot, ratio, and ratio fit
    MakeEstPlots( EstMassTTUp, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/MassTTUp"+chan, TTBarO, fit, isMC, False, log ) # Makes the actual estimation

    # T norm dn
    MakeFitPlots( EstMassTTDn, FMassTTDn, binsMass, "#rho", Xcut[0], var_arrayMass, chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "", "outputs/"+directory+method+"/MassTTDn"+chan, binBoundaries, fit, False ) # Creates the 2D plot, ratio, and ratio fit
    MakeEstPlots( EstMassTTDn, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/MassTTDn"+chan, TTBarO, fit, isMC, False, log ) # Makes the actual estimation

    # T alpha up
    MakeFitPlots( EstMassTTAlphaUp, FMassTTAlphaUp, binsMass, "#rho", Xcut[0], var_arrayMass, chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "", "outputs/"+directory+method+"/MassTTAlphaUp"+chan, binBoundaries, fit, False ) # Creates the 2D plot, ratio, and ratio fit
    MakeEstPlots( EstMassTTAlphaUp, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/MassTTAlphaUp"+chan, TTBarO, fit, isMC, False, log ) # Makes the actual estimation

    # T alpha dn
    MakeFitPlots( EstMassTTAlphaDn, FMassTTAlphaDn, binsMass, "#rho", Xcut[0], var_arrayMass, chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "", "outputs/"+directory+method+"/MassTTAlphaDn"+chan, binBoundaries, fit, False ) # Creates the 2D plot, ratio, and ratio fit
    MakeEstPlots( EstMassTTAlphaDn, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/MassTTAlphaDn"+chan, TTBarO, fit, isMC, False, log ) # Makes the actual estimation

    MakeFitPlots( EstMassTopUp, FMassTopUp, binsMass, "#rho", Xcut[0], var_arrayMass, chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "", "outputs/"+directory+method+"/MassTopUp"+chan, binBoundaries, fit, False ) # Creates the 2D plot, ratio, and ratio fit
    MakeEstPlots( EstMassTopUp, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/MassTopUp"+chan, TTBarO, fit, isMC, False, log ) # Makes the actual estimation

    MakeFitPlots( EstMassTopDn, FMassTopDn, binsMass, "#rho", Xcut[0], var_arrayMass, chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "", "outputs/"+directory+method+"/MassTopDn"+chan, binBoundaries, fit, False ) # Creates the 2D plot, ratio, and ratio fit
    MakeEstPlots( EstMassTopDn, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/MassTopDn"+chan, TTBarO, fit, isMC, False, log ) # Makes the actual estimation

    # Makes root file with basic fits

    FITFILE = TFile( "outputs/"+directory+method+"/LIM_FIT"+chan+".root", "RECREATE" )
    FITFILE.cd()
    
    FIT_Points = (EstMass.G).Clone("G_"+chan) # Ratio plot

    FIT_Points.Write()

    FITFILE.Write()
    FITFILE.Save()

    # Makes histograms for the theta root file
    chan__DATA = EstMass.hists_EST[0].Clone(chan+"__DATA")
    chan__DATA.Reset()
    chan__QCD = EstMass.hists_EST[0].Clone(chan+"__QCD")
    chan__QCD.Reset()
    chan__TTBAR = EstMass.hists_EST[0].Clone(chan+"__TTBAR")
    chan__TTBAR.Reset()
    chan__QCD__Fit__up = EstMass.hists_EST[0].Clone(chan+"__QCD__Fit__up")
    chan__QCD__Fit__up.Reset()
    chan__QCD__Fit__down = EstMass.hists_EST[0].Clone(chan+"__QCD__Fit__down")
    chan__QCD__Fit__down.Reset()
    chan__TTBAR__TTScale__up = EstMass.hists_EST[0].Clone(chan+"__TTBAR__TTScale__up")
    chan__TTBAR__TTScale__up.Reset()
    chan__TTBAR__TTScale__down = EstMass.hists_EST[0].Clone(chan+"__TTBAR__TTScale__down")
    chan__TTBAR__TTScale__down.Reset()
    chan__QCD__TTScale__up = EstMass.hists_EST[0].Clone(chan+"__QCD__TTScale__up")
    chan__QCD__TTScale__up.Reset()
    chan__QCD__TTScale__down = EstMass.hists_EST[0].Clone(chan+"__QCD__TTScale__down")
    chan__QCD__TTScale__down.Reset()
    chan__TTBAR__TTAlphaScale__up = EstMass.hists_EST[0].Clone(chan+"__TTBAR__TTAlphaScale__up")
    chan__TTBAR__TTAlphaScale__up.Reset()
    chan__TTBAR__TTAlphaScale__down = EstMass.hists_EST[0].Clone(chan+"__TTBAR__TTAlphaScale__down")
    chan__TTBAR__TTAlphaScale__down.Reset()
    chan__QCD__TTAlphaScale__up = EstMass.hists_EST[0].Clone(chan+"__QCD__TTAlphaScale__up")
    chan__QCD__TTAlphaScale__up.Reset()
    chan__QCD__TTAlphaScale__down = EstMass.hists_EST[0].Clone(chan+"__QCD__TTAlphaScale__down")
    chan__QCD__TTAlphaScale__down.Reset()
    chan__QCD__TopScale__up = EstMass.hists_EST[0].Clone(chan+"__QCD__TopScale__up")
    chan__QCD__TopScale__up.Reset()
    chan__QCD__TopScale__down = EstMass.hists_EST[0].Clone(chan+"__QCD__TopScale__down")
    chan__QCD__TopScale__down.Reset()

    chan__WJETS = EstMass.hists_EST[0].Clone(chan+"__WJETS")
    chan__WJETS.Reset()
    chan__WJETS__WJScale__up = EstMass.hists_EST[0].Clone(chan+"__WJETS__WJScale__up")
    chan__WJETS__WJScale__up.Reset()
    chan__WJETS__WJScale__down = EstMass.hists_EST[0].Clone(chan+"__WJETS__WJScale__down")
    chan__WJETS__WJScale__down.Reset()
    chan__TOP = EstMass.hists_EST[0].Clone(chan+"__TOP")
    chan__TOP.Reset()
    chan__TOP__TopScale__up = EstMass.hists_EST[0].Clone(chan+"__TOP__TopScale__up")
    chan__TOP__TopScale__up.Reset()
    chan__TOP__TopScale__down = EstMass.hists_EST[0].Clone(chan+"__TOP__TopScale__down")
    chan__TOP__TopScale__down.Reset()
    chan__QCD__WJScale__up = EstMass.hists_EST[0].Clone(chan+"__QCD__WJScale__up")
    chan__QCD__WJScale__up.Reset()
    chan__QCD__WJScale__down = EstMass.hists_EST[0].Clone(chan+"__QCD__WJScale__down")
    chan__QCD__WJScale__down.Reset()

    for i in EstMass.hists_EST: # Adds the plus histograms into the nominal bkg est
        chan__QCD.Add( i, 1. )
    for i in EstMass.hists_EST_SUB: # Subtracts the minus histograms from the nominal bkg est DOES NOT ADD THE SIGNAL MINUS REGIONS BACK IN
        chan__QCD.Add( i, -1. )
    removeNegativeBins(chan__QCD)
    for i in EstMass.hists_EST_UP: # Adds the plus histograms into the fit error up bkg est
        chan__QCD__Fit__up.Add( i, 1. )
    for i in EstMass.hists_EST_SUB_UP: # Subtracts the minus histograms from the fit error up bkg est DOES NOT ADD THE SIGNAL MINUS REGIONS BACK IN
        chan__QCD__Fit__up.Add( i, -1. )
    removeNegativeBins(chan__QCD__Fit__up)
    for i in EstMass.hists_EST_DN: # Adds the plus histograms into the fit error down bkg est
        chan__QCD__Fit__down.Add( i, 1. )
    for i in EstMass.hists_EST_SUB_DN: # Subtracts the minus histograms from the fit error down bkg est DOES NOT ADD THE SIGNAL MINUS REGIONS BACK IN
        chan__QCD__Fit__down.Add( i, -1. )
    removeNegativeBins(chan__QCD__Fit__down)
    for i in EstMassWJUp.hists_EST: # Adds the plus histograms into the W norm. up bkg est
        chan__QCD__WJScale__up.Add( i, 1. )
    for i in EstMassWJUp.hists_EST_SUB: # Subtracts the minus histograms from the W norm up bkg est DOES NOT ADD THE SIGNAL MINUS REGIONS BACK IN
        chan__QCD__WJScale__up.Add( i, -1. )
    removeNegativeBins(chan__QCD__WJScale__up)
    for i in EstMassWJDn.hists_EST: # Adds the plus histograms into the W norm down bkg est
        chan__QCD__WJScale__down.Add( i, 1. )
    for i in EstMassWJDn.hists_EST_SUB: # Subtracts the minus histograms from the W norm down bkg est DOES NOT ADD THE SIGNAL MINUS REGIONS BACK IN
        chan__QCD__WJScale__down.Add( i, -1. )
    removeNegativeBins(chan__QCD__WJScale__down)
    for i in EstMassTTUp.hists_EST: # Adds the plus histograms into the T norm up bkg est
        chan__QCD__TTScale__up.Add( i, 1. )
    for i in EstMassTTUp.hists_EST_SUB: # Subtracts the minus histograms from the T norm up bkg est DOES NOT ADD THE SIGNAL MINUS REGIONS BACK IN
        chan__QCD__TTScale__up.Add( i, -1. )
    removeNegativeBins(chan__QCD__TTScale__up)
    for i in EstMassTTDn.hists_EST: # Adds the plus histograms into the T norm down bkg est
        chan__QCD__TTScale__down.Add( i, 1. )
    for i in EstMassTTDn.hists_EST_SUB: # Subtracts the minus histograms from the T norm down bkg est DOES NOT ADD THE SIGNAL MINUS REGIONS BACK IN
        chan__QCD__TTScale__down.Add( i, -1. )
    removeNegativeBins(chan__QCD__TTScale__down)
    for i in EstMassTTAlphaUp.hists_EST: # Adds the plus histograms into the alpha up bkg est
        chan__QCD__TTAlphaScale__up.Add( i, 1. )
    for i in EstMassTTAlphaUp.hists_EST_SUB: # Subtracts the minus histograms from the alpha up bkg est DOES NOT ADD THE SIGNAL MINUS REGIONS BACK IN
        chan__QCD__TTAlphaScale__up.Add( i, -1. )
    removeNegativeBins(chan__QCD__TTAlphaScale__up)
    for i in EstMassTTAlphaDn.hists_EST: # Adds the plus histograms into the alpha down bkg est
        chan__QCD__TTAlphaScale__down.Add( i, 1. )
    for i in EstMassTTAlphaDn.hists_EST_SUB: # Subtracts the minus histograms from the alpha down bkg est DOES NOT ADD THE SIGNAL MINUS REGIONS BACK IN
        chan__QCD__TTAlphaScale__down.Add( i, -1. )
    removeNegativeBins(chan__QCD__TTAlphaScale__down)
    for i in EstMassTTAlphaUp.hists_EST: # Adds the plus histograms into the alpha up bkg est
        chan__QCD__TopScale__up.Add( i, 1. )
    for i in EstMassTTAlphaUp.hists_EST_SUB: # Subtracts the minus histograms from the alpha up bkg est DOES NOT ADD THE SIGNAL MINUS REGIONS BACK IN
        chan__QCD__TopScale__up.Add( i, -1. )
    removeNegativeBins(chan__QCD__TopScale__up)
    for i in EstMassTTAlphaDn.hists_EST: # Adds the plus histograms into the alpha down bkg est
        chan__QCD__TopScale__down.Add( i, 1. )
    for i in EstMassTTAlphaDn.hists_EST_SUB: # Subtracts the minus histograms from the alpha down bkg est DOES NOT ADD THE SIGNAL MINUS REGIONS BACK IN
        chan__QCD__TopScale__down.Add( i, -1. )
    removeNegativeBins(chan__QCD__TopScale__down)

    for i in EstMass.hists_MSR: # Adds the signal region plots together
        chan__DATA.Add(i)

    quickplot( TTJets.File, TTJets.Tree, chan__TTBAR, "prunedMassAve", presel+"&"+cuts+"&"+chanCuts, TTJets.weight ) # Makes nominal T plot
    quickplot( TTJetsUp.File, TTJetsUp.Tree, chan__TTBAR__TTScale__up, "prunedMassAve", presel+"&"+cuts+"&"+chanCuts, TTJetsUp.weight ) # Makes T norm up plot
    quickplot( TTJetsDn.File, TTJetsDn.Tree, chan__TTBAR__TTScale__down, "prunedMassAve", presel+"&"+cuts+"&"+chanCuts, TTJetsDn.weight ) # Makes T norm down plot
    quickplot( TTJetsAlphaUp.File, TTJetsAlphaUp.Tree, chan__TTBAR__TTAlphaScale__up, "prunedMassAve", presel+"&"+cuts+"&"+chanCuts, TTJetsAlphaUp.weight ) # Makes T alpha up plot
    quickplot( TTJetsAlphaDn.File, TTJetsAlphaDn.Tree, chan__TTBAR__TTAlphaScale__down, "prunedMassAve", presel+"&"+cuts+"&"+chanCuts, TTJetsAlphaDn.weight ) # Makes T alpha down plot

    quickplot( WJets.File, WJets.Tree, chan__WJETS, "prunedMassAve", presel+"&"+cuts+"&"+chanCuts, WJets.weight ) # Makes nominal W plot
    quickplot( WJetsUp.File, WJetsUp.Tree, chan__WJETS__WJScale__up, "prunedMassAve", presel+"&"+cuts+"&"+chanCuts, WJetsUp.weight ) # Makes W norm up plot
    quickplot( WJetsDn.File, WJetsDn.Tree, chan__WJETS__WJScale__down, "prunedMassAve", presel+"&"+cuts+"&"+chanCuts, WJetsDn.weight ) # Makes W norm down plot
    quickplot( Top.File, Top.Tree, chan__TOP, "prunedMassAve", presel+"&"+cuts+"&"+chanCuts, Top.weight ) # Makes nominal W plot
    quickplot( TopUp.File, TopUp.Tree, chan__TOP__TopScale__up, "prunedMassAve", presel+"&"+cuts+"&"+chanCuts, TopUp.weight ) # Makes W norm up plot
    quickplot( TopDn.File, TopDn.Tree, chan__TOP__TopScale__down, "prunedMassAve", presel+"&"+cuts+"&"+chanCuts, TopDn.weight ) # Makes W norm down plot

    #### Opens theta root file for writing
    FILE = TFile( "outputs/"+directory+method+"/LIM_FEED"+chan+".root", "RECREATE" )
    FILE.cd()
    #### Write plots to file    
    chan__DATA.Write()
    chan__QCD.Write()
    chan__TTBAR.Write()
    chan__TTBAR__TTScale__up.Write()
    chan__TTBAR__TTScale__down.Write()
    chan__TTBAR__TTAlphaScale__up.Write()
    chan__TTBAR__TTAlphaScale__down.Write()
    chan__QCD__TTScale__up.Write()
    chan__QCD__TTScale__down.Write()
    chan__QCD__TTAlphaScale__up.Write()
    chan__QCD__TTAlphaScale__down.Write()
    chan__QCD__TopScale__up.Write()
    chan__QCD__TopScale__down.Write()
    chan__QCD__WJScale__up.Write()
    chan__QCD__WJScale__down.Write()
    chan__WJETS.Write()
    chan__WJETS__WJScale__up.Write()
    chan__WJETS__WJScale__down.Write()
    chan__TOP.Write()
    chan__TOP__TopScale__up.Write()
    chan__TOP__TopScale__down.Write()

    ### Writes file
    FILE.Write()
    FILE.Save()
    
    C = TCanvas( "C", "", 800, 800 )

    # Plots and saves all the theta files

    chan__DATA.Draw("hist")
    C.SaveAs("outputs/"+directory+method+"/"+chan+"__DATA.png")

    chan__TTBAR__TTScale__up.SetLineColor(kRed)
    chan__TTBAR__TTScale__up.Draw("hist")
    chan__TTBAR.Draw("hist same")
    chan__TTBAR__TTScale__down.SetLineColor(kRed)
    chan__TTBAR__TTScale__down.Draw("hist same")
    C.SaveAs("outputs/"+directory+method+"/"+chan+"__TTBAR__TTScale.png")

    chan__QCD__TTScale__up.Draw("hist")
    chan__QCD.Draw("hist same")
    chan__QCD__TTScale__down.Draw("hist same")
    C.SaveAs("outputs/"+directory+method+"/"+chan+"__QCD__TTScale.png")

    chan__TTBAR__TTAlphaScale__up.SetLineColor(kRed)
    chan__TTBAR__TTAlphaScale__up.Draw("hist")
    chan__TTBAR.Draw("hist same")
    chan__TTBAR__TTAlphaScale__down.SetLineColor(kRed)
    chan__TTBAR__TTAlphaScale__down.Draw("hist same")
    C.SaveAs("outputs/"+directory+method+"/"+chan+"__TTBAR__TTAlphaScale.png")


    chan__QCD__TTAlphaScale__up.SetLineColor(kRed)
    chan__QCD__TTAlphaScale__up.Draw("hist")
    chan__QCD.Draw("hist same")
    chan__QCD__TTAlphaScale__down.SetLineColor(kRed)
    chan__QCD__TTAlphaScale__down.Draw("hist same")
    C.SaveAs("outputs/"+directory+method+"/"+chan+"__QCD__TTAlphaScale.png")

    chan__WJETS__WJScale__up.SetLineColor(kRed)
    chan__WJETS__WJScale__up.Draw("hist")
    chan__WJETS.Draw("hist same")
    chan__WJETS__WJScale__down.SetLineColor(kRed)
    chan__WJETS__WJScale__down.Draw("hist same")
    C.SaveAs("outputs/"+directory+method+"/"+chan+"__WJETS.png")

    chan__TOP__TopScale__up.SetLineColor(kRed)
    chan__TOP__TopScale__up.Draw("hist")
    chan__TOP.Draw("hist same")
    chan__TOP__TopScale__down.SetLineColor(kRed)
    chan__TOP__TopScale__down.Draw("hist same")
    C.SaveAs("outputs/"+directory+method+"/"+chan+"__TOP.png")

    chan__QCD__WJScale__up.SetLineColor(kRed)
    chan__QCD__WJScale__up.Draw("hist")
    chan__QCD.Draw("hist same")
    chan__QCD__WJScale__down.SetLineColor(kRed)
    chan__QCD__WJScale__down.Draw("hist same")
    C.SaveAs("outputs/"+directory+method+"/"+chan+"__QCD__WJScale.png")

    chan__QCD__TopScale__up.SetLineColor(kRed)
    chan__QCD__TopScale__up.Draw("hist")
    chan__QCD.Draw("hist same")
    chan__QCD__TopScale__down.SetLineColor(kRed)
    chan__QCD__TopScale__down.Draw("hist same")
    C.SaveAs("outputs/"+directory+method+"/"+chan+"__QCD__TopScale.png")

parser = argparse.ArgumentParser()
parser.add_argument( '-c', '--channel', action='store', dest='channel', default=1, help='Channel to run the estimation for')
parser.add_argument( '-m', '--method', action='store', dest='method', default="CBDCMVAv2MC", help='Method, B*(C/D)..., CMVA..., MC, Data...')
parser.add_argument( '-d', '--directory', action='store', dest='directory', default = "", help='Directory to save output in')
parser.add_argument( '-b', '--bins', action='store', dest='bins', default = 10, help='bin width for final estimation')
parser.add_argument( '-j', '--HT', action='store', dest='HT', default = "abs(HT)>-999", help='HT bin')
parser.add_argument( '-l', '--log', action='store', dest='log', default = "True", help='log')
parser.add_argument( '-f', '--fit', action='store', dest='fit', default = "False", help='fit')
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
HT = args.HT
if "T" in args.fit:
    fit = True
else:
    fit = False
if "T" in args.log:
    log = True
else:
    log = False
os.mkdir("outputs/"+directory+method)

prelimFit = [ 2.28, 7.00e-01, -2.13e-07, 0, 0 ]

# Sets the cuts depending on the method
if "CSVv2M" in method:
    zerobtag = "(jet1btagCSVv2<0.8484&jet2btagCSVv2<0.8484)"
    onebtag = "((jet1btagCSVv2<0.8484&jet2btagCSVv2>0.8484)||(jet1btagCSVv2>0.8484&jet2btagCSVv2<0.8484))"
    twobtag = "(jet1btagCSVv2>0.8484&jet2btagCSVv2>0.8484)"
    jet1btag = "((jet1btagCSVv2>0.8484&jet2btagCSVv2<0.8484))"
    jet2btag = "((jet1btagCSVv2<0.8484&jet2btagCSVv2>0.8484))"
#    tau21 = '.60'
    prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
elif "CMVAv2M" in method:
    zerobtag = "(jet1btagCMVAv2<0.4432&jet2btagCMVAv2<0.4432)"
    onebtag = "((jet1btagCMVAv2<0.4432&jet2btagCMVAv2>0.4432)||(jet1btagCMVAv2>0.4432&jet2btagCMVAv2<0.4432))"
    twobtag = "(jet1btagCMVAv2>0.4432&jet2btagCMVAv2>0.4432)"
    jet1btag = "((jet1btagCMVAv2>0.4432&jet2btagCMVAv2<0.4432))"
    jet2btag = "((jet1btagCMVAv2<0.4432&jet2btagCMVAv2>0.4432))"
#    tau21 = '.60'
    if "BCD" in method:
        prelimFit = [ 4.88e-01, -7.53e-01, -1.62e-07, 0, 0 ]
else:
    print "Method not found: " +method
    sys.exit(0)

prelimFit = [ 2.28, 7.00e-01, -2.13e-07, 0, 0 ]
zeroTop = "(jet1Tau32>0.67&jet2Tau32>.67)"
oneTop = "((jet1Tau32<=0.67&jet2Tau32>=0.67)||(jet1Tau32>0.67&jet2Tau32<0.67))"
twoTop = "(jet1Tau32<0.67&jet2Tau32<0.67)"
jet1Top = "((jet1Tau32>0.67&jet2Tau32<0.67))"
jet2Top = "((jet1Tau32<0.67&jet2Tau32>0.67))"

if "CBD" in method:
    Xcut = [ "prunedMassAsym", "0.1", 20, 0., 1. ]
#    Xcut = [ "jet1Tau21", "0.60", 20, 0., 1. ]
    Ycut = [ "deltaEtaDijet", "1.5", 20, 0., 5. ]
#    Ycut = [ "jet2Tau21", "0.60", 20, 0., 1. ]
elif "BCD" in method:
    Ycut = [ "prunedMassAsym", "0.1", 20, 0., 1. ]
    Xcut = [ "deltaEtaDijet", "1.5", 20, 0., 5. ]
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
scaleTop = 0
scaleTopErr = 0
scaleArray = {}
if 'After' in method:
    if 'CSVv2M' in method  and 'CBD' in method:
        scaleArray = {'TopScale': [(-1.358384112038593, 0.9562625564509293)], 'WJScale': [(0.44521423809651406, 0.9109671334433451)], '__nll': [-103934.48098326874], 'TTAlphaScale': [(0.14777210777173444, 0.977137906057747)], 'TTScale': [(0.6606219478868756, 0.6767263856444332)]}
        scaleTT = scaleArray['TTScale'][0][0]
        scaleTTErr = scaleArray['TTScale'][0][1]
        scaleW = scaleArray['WJScale'][0][0]
        scaleWErr = scaleArray['WJScale'][0][1]
        scaleTTAlpha = scaleArray[ 'TTAlphaScale' ][0][0]
        scaleTTAlphaErr = scaleArray[ 'TTAlphaScale' ][0][1]
        scaleTop = scaleArray[ 'TopScale' ][0][0]
        scaleTopErr = scaleArray[ 'TopScale' ][0][1]

    else:
        scaleTT = 0
        scaleTTErr = 1
        scaleW = 0
        scaleWErr = 1
        scaleTTAlpha = 0
        scaleTTAlphaErr = 1
        scaleTop = 0
        scaleTopErr = 1
else:
    scaleTT = 0
    scaleTTErr = 1
    scaleW = 0
    scaleWErr = 1
    scaleTTAlpha = 0
    scaleTTAlphaErr = 1
    scaleTop = 0
    scaleTopErr = 1

fitBinsPt = 0.1
# Sets preliminary fit depending on channel/method and runs ThetaFileMaker

if int(channel) == 1:
    if "CSVv2" in method and "BCD" in method:
        prelimFit = [ 6.00e-01, -9.99e-01, -10.04e-08 ]
        if "After" in method:
            prelimFit = [ 7.05e-01, -9.83e-01, -8.60e-08 ]
    elif "CSVv2" in method and "CBD" in method:
        prelimFit = [ 2.19, 1.02, -3.92e-07 ]
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
    elif "CMVAv2" in method and "BCD" in method:        
        prelimFit = [5.94e-01, -9.53e-01, -10.65e-08]
    elif "CMVAv2" in method and "CBD" in method:
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
    else:
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
    tau21 = "(jet1Tau21<0.45&jet2Tau21<0.45)"
    ThetaFileMaker( "b0t0T", zerobtag+"&"+zeroTop, 10, 60., 350., Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, fitBinsPt, HT, fit, isMC, log )

'''
if int(channel) == 2:
    fitBins = 25
    if "CSVv2" in method and "BCD" in method:
        fitBins = 25
        #prelimFit = [ -1.60, 9.68e-01, -6.51e-09 ]
        prelimFit = [ 7.45e-01, 4.41e-02, -3.56e-07 ]
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
    elif "CSVv2" in method and "CBD" in method:
        prelimFit = [ 2.21, 9.56, -3.36e-07 ]
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
    elif "CMVAv2" in method and "BCD" in method:
        fitBins = 25
        #prelimFit = [ 9.80e-02, -7.53e-03, -2.59e-08 ]
        prelimFit = [ 7.45e-01, 4.41e-02, -3.56e-07 ]
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
        if "After" in method:
            prelimFit = [8.35e-01, -1.27, -2.52e-07 ]
    elif "CMVAv2" in method and "CBD" in method:
        fitBins = 25
        #prelimFit = [ 2.10, 9.60e-01, -3.18e-07 ]
        #prelimFit = [ 7.45e-01, 4.41e-02, -3.56e-07 ]
        prelimFit = [ 2.27, 7.04e-01, -2.12e-07 ]
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
    else:
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
    tau21 = "(0.45<jet1Tau21&jet1Tau21<0.45&0.45<jet2Tau21&jet2Tau21<0.45)"
#    ThetaFileMaker( "b1t0L", onebtag+"&"+zeroTop, bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, fitBins, HT, fit, isMC, log )
    ThetaFileMaker( "b1t0L", onebtag+"&"+zeroTop, bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, fitBinsPt, HT, fit, isMC, log )
'''

if int(channel) == 3:
    fitBins = 25
    if "CSVv2" in method and "BCD" in method:
        fitBins = 25
        #prelimFit = [ -1.60, 9.68e-01, -6.51e-09 ]
        prelimFit = [ 7.45e-01, 4.41e-02, -3.56e-07 ]
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
    elif "CSVv2" in method and "CBD" in method:
        prelimFit = [ 2.21, 9.56, -3.36e-07 ]
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
    elif "CMVAv2" in method and "BCD" in method:
        fitBins = 25
        #prelimFit = [ 9.80e-02, -7.53e-03, -2.59e-08 ]
        prelimFit = [ 7.45e-01, 4.41e-02, -3.56e-07 ]
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
        if "After" in method:
            prelimFit = [8.35e-01, -1.27, -2.52e-07 ]
    elif "CMVAv2" in method and "CBD" in method:
        fitBins = 25
        #prelimFit = [ 2.10, 9.60e-01, -3.18e-07 ]
        #prelimFit = [ 7.45e-01, 4.41e-02, -3.56e-07 ]
        prelimFit = [ 2.27, 7.04e-01, -2.12e-07 ]
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
    else:
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
    tau21 = "(jet1Tau21<0.45&jet2Tau21<0.45)"
    bins = 10
#    ThetaFileMaker( "b1t0T", onebtag+"&"+zeroTop, bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, fitBins, HT, fit, isMC, log )
    ThetaFileMaker( "b1t0T", onebtag+"&"+zeroTop, bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, fitBinsPt, HT, fit, isMC, log )
if int(channel) == 4:
    fitBins = 25
    if "CSVv2" in method and "BCD" in method:
        prelimFit = [ 9.24e-01, -1.69, -1.80e-06 ]
    elif "CSVv2" in method and "CBD" in method:
        prelimFit = [ 3.56, 5.01e-01, -8.09e-07 ]
        if not isMC: prelimFit = [1.43, 2.43, -1.18e-05]
    elif "CMVAv2" in method and "BCD" in method:
        prelimFit = [ 9.62e-01, -4.76e-01, -2.66e-06  ]
    elif "CMVAv2" in method and "CBD" in method:
        prelimFit = [ 7.51e-01,1.14,-9.41e-08 ]
        if not isMC: prelimFit = [1.63, 4.85e-01,-1.06e-07]
    else:
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
    tau21 = "(jet1Tau21<0.60&jet2Tau21<0.60)"
    bins = 10
#    ThetaFileMaker( "b2t0", twobtag+"&"+zeroTop, bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, fitBins, HT, fit, isMC, log )
    ThetaFileMaker( "b2t0", twobtag+"&"+zeroTop, bins, 60., 350., Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, fitBinsPt, HT, fit, isMC, log )
if int(channel) == 5:
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
    prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
    tau21 = "(jet1Tau21<0.60&jet2Tau21<0.60)"
    bins = 10
#    ThetaFileMaker( "b0t1", zerobtag+"&"+oneTop, bins, 60, 250, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, 25, HT, fit, isMC, log )
    ThetaFileMaker( "b0t1", zerobtag+"&"+oneTop, bins, 60, 250, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, fitBinsPt, HT, fit, isMC, log )
if int(channel) == 6:
    fitBins = 25
    if "CSVv2" in method and "BCD" in method:
        #prelimFit = [ -1.60, 9.68e-01, -6.51e-09 ]
        prelimFit = [ 7.45e-01, 4.41e-02, -3.56e-07 ]
    elif "CSVv2" in method and "CBD" in method:
        prelimFit = [ 2.21, 9.56, -3.36e-07 ]
    elif "CMVAv2" in method and "BCD" in method:
        fitBins = 50
        #prelimFit = [ 9.80e-02, -7.53e-03, -2.59e-08 ]
        prelimFit = [6.87e-01, -1.06, -1.43e-07]
    elif "CMVAv2" in method and "CBD" in method:
        #prelimFit = [ 2.10, 9.60e-01, -3.18e-07 ]
        #prelimFit = [ 7.45e-01, 4.41e-02, -3.56e-07 ]
        prelimFit = [ 3.80, 2.47, -4.60e-07 ]
    else:
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
        #prelimFit = [ 9.28e-01, -4.07e+01, 1.74e-06, 0, 0 ]
    prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
    tau21 = "(jet1Tau21<0.60&jet2Tau21<0.60)"
    bins = 10
#    ThetaFileMaker( "b1t1", onebtag+"&"+oneTop, bins, 60, 250, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, fitBins, HT, fit, isMC, log )
    ThetaFileMaker( "b1t1", onebtag+"&"+oneTop, bins, 60, 250, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, fitBinsPt, HT, fit, isMC, log )
#    ThetaFileMaker( "b1t1", "( ("+jet1Top+"&"+jet2btag+")||("+jet2Top+"&"+jet1btag+") )", bins, 60, 250, Xcut, Ycut, isMC, log )
if int(channel) == 7:
    fitBins = 25
    if "CSVv2" in method and "BCD" in method:
        prelimFit = [9.41e-01, -1.04e+01, -1.33e-05]
    elif "CSVv2" in method and "CBD" in method:
        prelimFit = [ 3.56, 5.01e-01, -8.09e-07 ]
    elif "CMVAv2" in method and "BCD" in method:
        prelimFit = [6.83e-01, -9.04e-01, -2.31e-07 ]
    elif "CMVAv2" in method and "CBD" in method:
        if not isMC: fitBins = 50
        prelimFit = [ 2.09, 1.01, -2.45e-07 ]
    else:
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
    prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
    tau21 = "(jet1Tau21<0.60&jet2Tau21<0.60)"
    bins = 10
#    ThetaFileMaker( "b2t1", twobtag+"&"+oneTop, bins, 60, 250, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, fitBins, HT, fit, isMC, log )
    ThetaFileMaker( "b2t1", twobtag+"&"+oneTop, bins, 60, 250, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, fitBinsPt, HT, fit, isMC, log )

if int(channel) == 8:
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
    prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
    tau21 = "(jet1Tau21<0.60&jet2Tau21<0.60)"
    bins = 10
#    tau21 = "(abs(jet1Pt)>-999)"
#    ThetaFileMaker( "b0t2", zerobtag+"&"+twoTop, bins, 60, 250, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, 25, HT, fit, isMC, log )
    ThetaFileMaker( "b0t2", zerobtag+"&"+twoTop, bins, 100, 250, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, fitBinsPt, HT, fit, isMC, log )
if int(channel) == 9:
    fitBins = 25
    if "CSVv2" in method and "BCD" in method:
        #prelimFit = [ -1.60, 9.68e-01, -6.51e-09 ]
        prelimFit = [ 6.93e-01, -1.05, -1.13e-07 ]
    elif "CSVv2" in method and "CBD" in method:
        prelimFit = [ 2.21, 9.56, -3.36e-07 ]
    elif "CMVAv2" in method and "BCD" in method:
#        fitBins = 50
        #prelimFit = [ 9.80e-02, -7.53e-03, -2.59e-08 ]
        prelimFit = [6.87e-01, -1.06, -1.43e-07] 
    elif "CMVAv2" in method and "CBD" in method:
        #prelimFit = [ 2.10, 9.60e-01, -3.18e-07 ]
        prelimFit = [ 7.45e-01, 4.41e-02, -3.56e-07 ]
        if not isMC: prelimFit = [1.76,1.53,-4.96e-07]
    else:
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
    tau21 = "(jet1Tau21<0.60&jet2Tau21<0.60)"
    bins = 10
#    tau21 = "(abs(jet1Pt)>-999)"
#    ThetaFileMaker( "b1t2", onebtag+"&"+twoTop, bins, 60, 250, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, fitBins, HT, fit, isMC, log )
    ThetaFileMaker( "b1t2", onebtag+"&"+twoTop, bins, 100, 250, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, fitBinsPt, HT, fit, isMC, log )
if int(channel) == 10:
    fitBins = 25
    if "CSVv2" in method and "BCD" in method:
        #prelimFit = [ -1.60, 9.68e-01, -6.51e-09 ]
        prelimFit = [ 6.93e-01, -1.05, -1.13e-07 ]
    elif "CSVv2" in method and "CBD" in method:
        prelimFit = [ 2.21, 9.56, -3.36e-07 ]
    elif "CMVAv2" in method and "BCD" in method:
#        fitBins = 50
        #prelimFit = [ 9.80e-02, -7.53e-03, -2.59e-08 ]
        prelimFit = [6.87e-01, -1.06, -1.43e-07] 
    elif "CMVAv2" in method and "CBD" in method:
        #prelimFit = [ 2.10, 9.60e-01, -3.18e-07 ]
        prelimFit = [ 7.45e-01, 4.41e-02, -3.56e-07 ]
        if not isMC: prelimFit = [1.76,1.53,-4.96e-07]
    else:
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
    tau21 = "(jet1Tau21<0.60&jet2Tau21<0.60)"
    bins = 10
#    tau21 = "(abs(jet1Pt)>-999)"
#    ThetaFileMaker( "b2t2", twobtag+"&"+twoTop, bins, 60, 250, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, fitBins, HT, fit, isMC, log )
    ThetaFileMaker( "b2t2", twobtag+"&"+twoTop, bins, 100, 250, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, fitBinsPt, HT, fit, isMC, log )
#    ThetaFileMaker( "b0t0T", zerobtag+"&"+zeroTop, bins, 60., 350., Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, fitBinsPt, HT, fit, isMC, log )
if int(channel) == 11:
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
    prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
    tau21 = "(jet1Tau21<0.60&jet2Tau21<0.60)"
    bins = 10
    ThetaFileMaker( "b12t2", "(("+onebtag+"&"+twoTop +")||("+twobtag+"&"+twoTop+"))", bins, 60, 250, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, 25, HT, fit, isMC, log )
if int(channel) == 12:
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
    prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
    tau21 = "(jet1Tau21<0.45&jet2Tau21<0.45)"
    ThetaFileMaker( "b1t12", onebtag+"&(jet1Tau32<0.51||jet2Tau32<0.51)", bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, 25, HT, fit, isMC, log )
if int(channel) == 13:
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
    prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
    tau21 = "(jet1Tau21<0.45&jet2Tau21<0.45)"
    ThetaFileMaker( "b2t12", twobtag+"&(jet1Tau32<0.51||jet2Tau32<0.51)", bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, 25, HT, fit, isMC, log )
if int(channel) == 14:
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
    prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
    jet1Rho = "log((jet1PrunedMass*jet1PrunedMass)/(jet1Pt))"
    jet2Rho = "log((jet2PrunedMass*jet2PrunedMass)/(jet2Pt))"
    jet1Tau21DDT = "(jet1Tau21 + 4.35e-02*"+jet1Rho+")"
    jet2Tau21DDT = "(jet2Tau21 + 4.35e-02*"+jet2Rho+")"
    tau21 = "("+jet1Tau21DDT+"<0.74&"+jet2Tau21DDT+"<0.74)"
#    tau21 = 'prunedMassAsym<0.1&deltaEtaDijet<1.5'
#    tau21 = 'abs(jet1Pt)>-999'
    ThetaFileMaker( "pres", "(abs(jet1Pt)>-999)", 10, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, 25, HT, fit, isMC, log )
if int(channel) == 15:
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
    prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
    tau21 = 'jet1Tau21<0.45&jet2Tau21<0.45&numPV>20'
    ThetaFileMaker( "pres", "(abs(jet1Pt)>-999)", 10, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, 25, HT, fit, isMC, log )
