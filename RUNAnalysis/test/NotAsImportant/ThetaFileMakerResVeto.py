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
def ThetaFileMaker( chan, chanCuts, bins, minBin, maxBin, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleAlpha, scaleAlphaErr, tau21, prelimFit, fitBins, HT, isMC=True ):
    gStyle.SetOptStat(0)
    # Setting basic distributions
    # Setting basic distributions
#    weight = "(36600*puWeight*lumiWeight/15*2.74297e-01)"
    weight = "(29014.91*lumiWeight*puWeight)"

    # The T and W scales
    TTNorm = "( (1.06)*(1+.2*"+str(scaleTT)+"))" # The scale that determines the nominal TTBar normalization
    TTNormUp = "( (1.06)*(1+.2*" + str(scaleTT) + "+.2*" + str(scaleTTErr) + ") )" # Upper TTBar normalization
    TTNormDn = "( (1.06)*(1+.2*" + str(scaleTT) + "-.2*" + str(scaleTTErr) + ") )" # Lower TTBar normalization

#    TTAlpha = "exp( (-0.0005*(genPartPt1+genPartPt2))*(1-.2*" + str(scaleAlpha) + ") )" # The scale that determines the nominal alpha NOTE: subtracting = adding because -0.0005
#    TTAlphaUp = "exp( (-0.0005*(genPartPt1+genPartPt2))*(1-.2*" + str(scaleAlpha) + "-.2*" + str(scaleAlphaErr) + ") )" # Upper alpha NOTE: subtracting = adding because -0.0005
#    TTAlphaDn = "exp( (-0.0005*(genPartPt1+genPartPt2))*(1-.2*" + str(scaleAlpha) + "+.2*" + str(scaleAlphaErr) + ") )" # Lower alpha NOTE: subtracting = adding because -0.0005
    TTAlpha = "exp( (-0.0005*(HT/2))*(1-.2*" + str(scaleAlpha) + ") )" # The scale that determines the nominal alpha NOTE: subtracting = adding because -0.0005
    TTAlphaUp = "exp( (-0.0005*(HT/2))*(1-.2*" + str(scaleAlpha) + "-.2*" + str(scaleAlphaErr) + ") )" # Upper alpha NOTE: subtracting = adding because -0.0005
    TTAlphaDn = "exp( (-0.0005*(HT/2))*(1-.2*" + str(scaleAlpha) + "+.2*" + str(scaleAlphaErr) + ") )" # Lower alpha NOTE: subtracting = adding because -0.0005

    TTScaleStr = "(" + TTNorm + "*" + TTAlpha + ")" # Total string to scale TT by, norm*alpha
    TTScaleErrUpStr = "(" + TTNormUp + "*" + TTAlpha + ")" # String for scaling TT with norm up, normUp*alpha
    TTScaleErrDnStr = "(" + TTNormDn + "*" + TTAlpha + ")" # String for scaling TT with norm dn, normDn*alpha
    AlphaScaleUpStr = "(" + TTNorm + "*" + TTAlphaUp + ")" # Total string to scale TT by with alpha up, norm*alphaUp
    AlphaScaleDnStr = "(" + TTNorm + "*" + TTAlphaDn + ")" # Total string to scale TT by with alpha dn, norm*alphaDn

    WScaleStr = "(1+.2*"+str(scaleW)+")" # The scale that determines the nominal W normalization
    WScaleUpStr = "(1+.2*"+str(scaleW)+"+.2*"+str(scaleWErr)+")" # Upper W normalization
    WScaleDnStr = "(1+.2*"+str(scaleW)+"-.2*"+str(scaleWErr)+")" # Lower W normalization

    # Create the distributions
    DATA = DIST( "DATA", "ResVetoRootFiles/ResVeto_RUNAnalysis_JetHT_Run2016_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", "1" )
    QCD = DIST( "QCD", "ResVetoRootFiles/ResVeto_RUNAnalysis_QCDHTAll_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", ".85*"+weight )
#    SIG = DIST( "SIG", "ResVetoRootFiles/", "BoostedAnalysisPlots/RUNATree", weight )

    TTJets = DIST( "TTJets", "ResVetoRootFiles/ResVeto_RUNAnalysis_TT_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*"+TTScaleStr+")" )
    TTJetsUp = DIST( "TTJetsUp", "ResVetoRootFiles/ResVeto_RUNAnalysis_TT_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*"+TTScaleErrUpStr+")" )
    TTJetsDn = DIST( "TTJetsDn", "ResVetoRootFiles/ResVeto_RUNAnalysis_TT_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*"+TTScaleErrDnStr+")"  )
    TTJetsAlphaUp = DIST( "TTJetsUp", "ResVetoRootFiles/ResVeto_RUNAnalysis_TT_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*"+AlphaScaleUpStr+")")
    TTJetsAlphaDn = DIST( "TTJetsDn", "ResVetoRootFiles/ResVeto_RUNAnalysis_TT_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree",  "("+weight+"*"+AlphaScaleDnStr+")" )

    WJets = DIST( "WJets", "ResVetoRootFiles/ResVeto_RUNAnalysis_WJetsToQQ_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree",  "("+weight+"*"+WScaleStr+")" )
    WJetsUp = DIST( "WJetsUp", "ResVetoRootFiles/ResVeto_RUNAnalysis_WJetsToQQ_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*"+WScaleUpStr+")" )
    WJetsDn = DIST( "WJetsDn", "ResVetoRootFiles/ResVeto_RUNAnalysis_WJetsToQQ_80X_V2p3_v06.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*"+WScaleDnStr+")" )

#    WW = DIST( "WW", "ResVetoRootFiles/ResVeto_RUNAnalysis_WWTo4Q_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlotsPuppi/RUNATree", weight )
#    WZ = DIST( "WZ", "ResVetoRootFiles/ResVeto_RUNAnalysis_WZ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlotsPuppi/RUNATree", weight )
#    ZZ = DIST( "ZZ", "ResVetoRootFiles/ResVeto_RUNAnalysis_ZZTo4Q_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlotsPuppi/RUNATree", weight )
#    ZJets = DIST( "ZJets", "ResVetoRootFiles/ResVeto_RUNAnalysis_ZJetsToQQ_RunIIFall15MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlotsPuppi/RUNATree", weight )
#    Sig = DIST( "Sig", "ResVetoRootFiles/RUNAnalysis_RPVStopStopToJets_UDD323_M-100_RunIISummer16MiniAODv2_v76x_v2p0_v05.root", "BoostedAnalysisPlotsPuppi/RUNATree", weight )

    # Creating Alphabet objects to run estimate on    
    if isMC: # If running over the MC
        Dists = [ QCD, TTJets, WJets ] # Use the MC distributions
#        Dists = [ QCD ] # Use the MC distributions
    else:  # Otherwise
        Dists = [DATA] # Use data 
    DistsSub = [ WJets, TTJets ] # Nominal distributions to subtract
#    DistsSub = [ ] # Nominal distributions to subtract

    ## Defining Cuts
    presel = tau21+"&"+HT #"jet1Tau21<"+tau21+"&jet2Tau21<"+tau21
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
#    NBins = int(20)
#    binWidth = int(250)
#    var_arrayMass = [ "prunedMassAve", Xcut[0], NBins, 50., 350., Xcut[2], Xcut[3], Xcut[4] ] # For making B,D plot
    var_arrayMass = [ "prunedMassAve", Xcut[0], NBins, 50., 350., Xcut[2], Xcut[3], Xcut[4] ] # For making B,D plot
    
    for i in xrange( 0, NBins ):
        binsMass.append( [ var_arrayMass[3]+binWidth*i, var_arrayMass[3]+binWidth*(i+1) ] )
#    prelimFit = [0,0,0,0,0,0,0]
        
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
#    if chan is "b0t2": chanCutsTemp = zerobtag+"&"+oneTop
#    elif chan is "b1t2": chanCutsTemp = onebtag+"&"+oneTop
#    elif chan is "b2t1": chanCutsTemp = twobtag+"&"+zeroTop
#    elif chan is "b2t2": chanCutsTemp = twobtag+"&"+zeroTop
#    else: chanCutsTemp = chanCuts
    chanCutsTemp = chanCuts
    # Nominal
    MakeFitPlots( EstMass, FMass, binsMass, "prunedMassAve", Xcut[0], var_arrayMass, presel+"&"+chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "", "outputs/"+directory+method+"/Mass"+chan, binBoundaries, False ) # Creates the 2D plot, ratio, and ratio fit
    MakeEstPlots( EstMass, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/Mass"+chan, isMC, False ) # Makes the actual estimation

    # W norm up
    MakeFitPlots( EstMassWJUp, FMassWJUp, binsMass, "prunedMassAve", Xcut[0], var_arrayMass, presel+"&"+chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "",  "outputs/"+directory+method+"/MassWJUp"+chan, binBoundaries, False ) # Creates the 2D plot, ratio, and ratio fit
    MakeEstPlots( EstMassWJUp, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/MassWJUp"+chan, isMC, False ) # Makes the actual estimation

    # W norm dn
    MakeFitPlots( EstMassWJDn, FMassWJDn, binsMass, "prunedMassAve", Xcut[0], var_arrayMass, presel+"&"+chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "", "outputs/"+directory+method+"/MassWJDn"+chan, binBoundaries, False ) # Creates the 2D plot, ratio, and ratio fit
    MakeEstPlots( EstMassWJDn, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/MassWJDn"+chan, isMC, False ) # Makes the actual estimation

    # T norm up
    MakeFitPlots( EstMassTTUp, FMassTTUp, binsMass, "prunedMassAve", Xcut[0], var_arrayMass, presel+"&"+chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "", "outputs/"+directory+method+"/MassTTUp"+chan, binBoundaries, False ) # Creates the 2D plot, ratio, and ratio fit
    MakeEstPlots( EstMassTTUp, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/MassTTUp"+chan, isMC, False ) # Makes the actual estimation

    # T norm dn
    MakeFitPlots( EstMassTTDn, FMassTTDn, binsMass, "prunedMassAve", Xcut[0], var_arrayMass, presel+"&"+chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "", "outputs/"+directory+method+"/MassTTDn"+chan, binBoundaries, False ) # Creates the 2D plot, ratio, and ratio fit
    MakeEstPlots( EstMassTTDn, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/MassTTDn"+chan, isMC, False ) # Makes the actual estimation

    # T alpha up
    MakeFitPlots( EstMassTTAlphaUp, FMassTTAlphaUp, binsMass, "prunedMassAve", Xcut[0], var_arrayMass, presel+"&"+chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "", "outputs/"+directory+method+"/MassTTAlphaUp"+chan, binBoundaries, False ) # Creates the 2D plot, ratio, and ratio fit
    MakeEstPlots( EstMassTTAlphaUp, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/MassTTAlphaUp"+chan, isMC, False ) # Makes the actual estimation

    # T alpha dn
    MakeFitPlots( EstMassTTAlphaDn, FMassTTAlphaDn, binsMass, "prunedMassAve", Xcut[0], var_arrayMass, presel+"&"+chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "", "outputs/"+directory+method+"/MassTTAlphaDn"+chan, binBoundaries, False ) # Creates the 2D plot, ratio, and ratio fit
    MakeEstPlots( EstMassTTAlphaDn, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/MassTTAlphaDn"+chan, isMC, False ) # Makes the actual estimation

    # Makes root file with basic fits
    FITFILE = TFile( "outputs/"+directory+method+"/LIM_FIT"+chan+".root", "RECREATE" )
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
#    if not("b2" in chan or "t2" in chan) or True:
    chan__WJETS = EstMass.hists_EST[0].Clone(chan+"__WJETS")
    chan__WJETS.Reset()
    chan__WJETS__WJScale__up = EstMass.hists_EST[0].Clone(chan+"__WJETS__WJScale__up")
    chan__WJETS__WJScale__up.Reset()
    chan__WJETS__WJScale__down = EstMass.hists_EST[0].Clone(chan+"__WJETS__WJScale__down")
    chan__WJETS__WJScale__down.Reset()
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
    for i in EstMass.hists_MSR: # Adds the signal region plots together
        chan__DATA.Add(i)

    quickplot( TTJets.File, TTJets.Tree, chan__TTBAR, "prunedMassAve", presel+"&"+cuts+"&"+chanCuts, TTJets.weight ) # Makes nominal T plot
    quickplot( TTJetsUp.File, TTJetsUp.Tree, chan__TTBAR__TTScale__up, "prunedMassAve", presel+"&"+cuts+"&"+chanCuts, TTJetsUp.weight ) # Makes T norm up plot
    quickplot( TTJetsDn.File, TTJetsDn.Tree, chan__TTBAR__TTScale__down, "prunedMassAve", presel+"&"+cuts+"&"+chanCuts, TTJetsDn.weight ) # Makes T norm down plot
    quickplot( TTJetsAlphaUp.File, TTJetsAlphaUp.Tree, chan__TTBAR__TTAlphaScale__up, "prunedMassAve", presel+"&"+cuts+"&"+chanCuts, TTJetsAlphaUp.weight ) # Makes T alpha up plot
    quickplot( TTJetsAlphaDn.File, TTJetsAlphaDn.Tree, chan__TTBAR__TTAlphaScale__down, "prunedMassAve", presel+"&"+cuts+"&"+chanCuts, TTJetsAlphaDn.weight ) # Makes T alpha down plot

#    quickplot( WJets.File, WJets.Tree, chan__WJETS__A, "prunedMassAve", presel+"&"+cuts+"&"+chanCuts, WJets.weight )
#    quickplot( WJetsUp.File, WJetsUp.Tree, chan__WJETS__WJScale__up__A, "prunedMassAve", presel+"&"+cuts+"&"+chanCuts, WJetsUp.weight )
#    quickplot( WJetsDn.File, WJetsDn.Tree, chan__WJETS__WJScale__down__A, "prunedMassAve", presel+"&"+cuts+"&"+chanCuts, WJetsDn.weight )
    
    quickplot( WJets.File, WJets.Tree, chan__WJETS, "prunedMassAve", presel+"&"+cuts+"&"+chanCuts, WJets.weight ) # Makes nominal W plot
    quickplot( WJetsUp.File, WJetsUp.Tree, chan__WJETS__WJScale__up, "prunedMassAve", presel+"&"+cuts+"&"+chanCuts, WJetsUp.weight ) # Makes W norm up plot
    quickplot( WJetsDn.File, WJetsDn.Tree, chan__WJETS__WJScale__down, "prunedMassAve", presel+"&"+cuts+"&"+chanCuts, WJetsDn.weight ) # Makes W norm down plot
    
#    if( chan__WJETS.Integral() > 0 and chan__WJETS__A.Integral() > 0  ): chan__WJETS.Scale( chan__WJETS__A.Integral()/chan__WJETS.Integral() )
#    elif( chan__WJETS__A.Integral() == 0 ): chan__WJETS.Scale(0)
#    if( chan__WJETS__WJScale__up.Integral() > 0 and chan__WJETS__WJScale__up__A.Integral() > 0  ): chan__WJETS__WJScale__up.Scale( chan__WJETS__WJScale__up__A.Integral()/chan__WJETS__WJScale__up.Integral() )
#    elif( chan__WJETS__WJScale__up__A.Integral() == 0 ): chan__WJETS__WJScale__up.Scale(0)
#    if( chan__WJETS__WJScale__down.Integral() > 0 and chan__WJETS__WJScale__down__A.Integral() > 0  ): chan__WJETS__WJScale__down.Scale( chan__WJETS__WJScale__down__A.Integral()/chan__WJETS__WJScale__down.Integral() )
#    elif( chan__WJETS__WJScale__down__A.Integral() == 0 ): chan__WJETS__WJScale__down.Scale(0)

    #### Opens theta root file for writing
    FILE = TFile( "outputs/"+directory+method+"/LIM_FEED"+chan+".root", "RECREATE" )
    FILE.cd()
    #### Write plots to file    
    chan__DATA.Write()
    chan__QCD.Write()
    chan__TTBAR.Write()
#    chan__QCD__Fit__up.Write() # Skips QCD Plots cause otherwise theta fails
#    chan__QCD__Fit__down.Write()
    chan__TTBAR__TTScale__up.Write()
    chan__TTBAR__TTScale__down.Write()
    chan__TTBAR__TTAlphaScale__up.Write()
    chan__TTBAR__TTAlphaScale__down.Write()
    chan__QCD__TTScale__up.Write()
    chan__QCD__TTScale__down.Write()
    chan__QCD__TTAlphaScale__up.Write()
    chan__QCD__TTAlphaScale__down.Write()
    chan__WJETS.Write()
    chan__WJETS__WJScale__up.Write()
    chan__WJETS__WJScale__down.Write()
    ### Writes file
    FILE.Write()
    FILE.Save()
    
    C = TCanvas( "C", "", 800, 800 )

    # Plots and saves all the theta files

    chan__DATA.Draw("hist")
    C.SaveAs("outputs/"+directory+method+"/"+chan+"__DATA.png")
#    chan__QCD.Draw("hist")
#    C.SaveAs("outputs/"+directory+method+"/"+chan+"__QCD.png")
#    chan__QCD__Fit__up.Draw("hist")
#    C.SaveAs("outputs/"+directory+method+"/"+chan+"__QCD__Fit__up.png")
#    chan__QCD__Fit__down.Draw("hist")
#    C.SaveAs("outputs/"+directory+method+"/"+chan+"__QCD__Fit__down.png")

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

    chan__QCD__WJScale__up.SetLineColor(kRed)
    chan__QCD__WJScale__up.Draw("hist")
    chan__QCD.Draw("hist same")
    chan__QCD__WJScale__down.SetLineColor(kRed)
    chan__QCD__WJScale__down.Draw("hist same")
    C.SaveAs("outputs/"+directory+method+"/"+chan+"__QCD__WJScale.png")

parser = argparse.ArgumentParser()
parser.add_argument( '-c', '--channel', action='store', dest='channel', default=1, help='Channel to run the estimation for')
parser.add_argument( '-m', '--method', action='store', dest='method', default="CBDCMVAv2MC", help='Method, B*(C/D)..., CMVA..., MC, Data...')
parser.add_argument( '-d', '--directory', action='store', dest='directory', default = "", help='Directory to save output in')
parser.add_argument( '-b', '--bins', action='store', dest='bins', default = 10, help='bin width for final estimation')
parser.add_argument( '-j', '--HT', action='store', dest='HT', default = "abs(HT)>-999", help='HT bin')
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
#if "/" in directory:
#    os.mkdir("outputs/"+directory)
#    os.mkdir("outputs/"+directory+method)
#else:
os.mkdir("outputs/"+directory+method)
#prelimFit = [0,0,0,0,0]
#prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
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

scaleArray = {}
if 'After' in method:
    if 'CMVAv2M' in method  and 'BCD' in method:
        scaleArray = {'TTScale': [(0.4865024809268377, 0.5507220047276107)], 'WJScale': [(-0.6348616467878898, 0.7201322020309675)], '__nll': [-208907.84769622053], 'TTAlphaScale': [(0.506890239078416, 0.2647946318216192)]}
        scaleTT = scaleArray['TTScale'][0][0]
        scaleTTErr = scaleArray['TTScale'][0][1]
        scaleW = scaleArray['WJScale'][0][0]
        scaleWErr = scaleArray['WJScale'][0][1]
        scaleTTAlpha = scaleArray[ 'TTAlphaScale' ][0][0]
        scaleTTAlphaErr = scaleArray[ 'TTAlphaScale' ][0][1]
    elif 'CMVAv2M' in method  and 'CBD' in method:
        scaleArray = {'TTScale': [(0.4866936904810206, 0.506171773786062)], 'WJScale': [(-0.0900780508617558, 0.7424838437565096)], '__nll': [-208965.33125107642], 'TTAlphaScale': [(0.26820503154876274, 0.9928584621512084)]}
        scaleTT = scaleArray['TTScale'][0][0]
        scaleTTErr = scaleArray['TTScale'][0][1]
        scaleW = scaleArray['WJScale'][0][0]
        scaleWErr = scaleArray['WJScale'][0][1]
        scaleTTAlpha = scaleArray[ 'TTAlphaScale' ][0][0]
        scaleTTAlphaErr = scaleArray[ 'TTAlphaScale' ][0][1]
    elif 'CSVv2M' in method  and 'BCD' in method:
        scaleArray = {'TTScale': [(0.3324390151360559, 0.6288875371154341)], 'WJScale': [(-0.6143987832966422, 0.7209964750228495)], '__nll': [-212162.262151059], 'TTAlphaScale': [(0.37914999326973486, 0.9759900872451395)]}
        scaleTT = scaleArray['TTScale'][0][0]
        scaleTTErr = scaleArray['TTScale'][0][1]
        scaleW = scaleArray['WJScale'][0][0]
        scaleWErr = scaleArray['WJScale'][0][1]
        scaleTTAlpha = scaleArray[ 'TTAlphaScale' ][0][0]
        scaleTTAlphaErr = scaleArray[ 'TTAlphaScale' ][0][1]
    elif 'CSVv2M' in method  and 'CBD' in method:
        if 'not1' in method:
            scaleArray = {'TTScale': [(0.5320057340507436, 0.5951743976448869)], 'WJScale': [(-0.5173549554281323, 0.846699757449402)], '__nll': [-89761.33517250503], 'TTAlphaScale': [(0.21453961072229255, 0.9876010610787747)]}
        elif 't1or2' in method:
            scaleArray = {'TTScale': [(0.4229557215949402, 0.7034626331063345)], 'WJScale': [(-0.6669036320440132, 0.8375321845733996)], '__nll': [-94230.03251294263], 'TTAlphaScale': [(0.48407728506571246, 0.8990781789954703)]}
        elif '11reg' in method:
            scaleArray = {'TTScale': [(0.4605362349315474, 0.5116115744868042)], 'WJScale': [(-0.7843545751297061, 0.8272868942461518)], '__nll': [-93888.66166299707], 'TTAlphaScale': [(0.14975059785032485, 0.9816886681742449)]}
        else: scaleArray = {'TTScale': [(0.49556163386463226, 0.5079691504416144)], 'WJScale': [(-0.04531001144487323, 0.7449090048436569)], '__nll': [-212199.86987062535], 'TTAlphaScale': [(0.22245862833561958, 0.9676588305845684)]}
        scaleTT = scaleArray['TTScale'][0][0]
        scaleTTErr = scaleArray['TTScale'][0][1]
        scaleW = scaleArray['WJScale'][0][0]
        scaleWErr = scaleArray['WJScale'][0][1]
        scaleTTAlpha = scaleArray[ 'TTAlphaScale' ][0][0]
        scaleTTAlphaErr = scaleArray[ 'TTAlphaScale' ][0][1]

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

    
# Sets preliminary fit depending on channel/method and runs ThetaFileMaker
if int(channel) == 0:
    if "CSVv2" in method and "BCD" in method:
        prelimFit = [ 5.94e-01, -6.48e-01, -3.51e-08 ]
        
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
        if "After" in method:
            prelimFit = [ 7.05e-01, -9.83e-01, -8.60e-08 ]
    elif "CSVv2" in method and "CBD" in method:
        prelimFit = [ 2.19, 1.02, -3.92e-07 ]
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
    elif "CMVAv2" in method and "BCD" in method:        
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
    elif "CMVAv2" in method and "CBD" in method:
        
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
    else:
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
    tau21 = "(0.45<jet1Tau21&jet1Tau21<0.60&0.45<jet2Tau21&jet2Tau21<0.60)"
    ThetaFileMaker( "b0t0L", zerobtag+"&"+zeroTop, bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, tau21, prelimFit, 25, HT, isMC )
if int(channel) == 1:
    if "CSVv2" in method and "BCD" in method:
        prelimFit = [ 5.94e-01, -6.48e-01, -3.51e-08 ]
        
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
        if "After" in method:
            prelimFit = [ 7.05e-01, -9.83e-01, -8.60e-08 ]
    elif "CSVv2" in method and "CBD" in method:
        prelimFit = [ 2.19, 1.02, -3.92e-07 ]
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
    elif "CMVAv2" in method and "BCD" in method:        
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
    elif "CMVAv2" in method and "CBD" in method:
        
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
    else:
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
    tau21 = "(jet1Tau21<0.45&jet2Tau21<0.45)"
    ThetaFileMaker( "b0t0T", zerobtag+"&"+zeroTop, bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, tau21, prelimFit, 25, HT, isMC )
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
    tau21 = "(0.45<jet1Tau21&jet1Tau21<0.60&0.45<jet2Tau21&jet2Tau21<0.60)"
    ThetaFileMaker( "b1t0L", onebtag+"&"+zeroTop, bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, tau21, prelimFit, fitBins, HT, isMC )
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
    ThetaFileMaker( "b1t0T", onebtag+"&"+zeroTop, bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, tau21, prelimFit, fitBins, HT, isMC )
if int(channel) == 4:
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
    tau21 = "(jet1Tau21<0.45&jet2Tau21<0.45)"
    ThetaFileMaker( "b2t0", twobtag+"&"+zeroTop, bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, tau21, prelimFit, 25, HT, isMC )
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
    ThetaFileMaker( "b0t1", zerobtag+"&"+oneTop, bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, tau21, prelimFit, 25, HT, isMC )
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
        prelimFit = [ 7.45e-01, 4.41e-02, -3.56e-07 ]
    elif "CMVAv2" in method and "CBD" in method:
        #prelimFit = [ 2.10, 9.60e-01, -3.18e-07 ]
        #prelimFit = [ 7.45e-01, 4.41e-02, -3.56e-07 ]
        prelimFit = [ 3.80, 2.47, -4.60e-07 ]
    else:
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
        #prelimFit = [ 9.28e-01, -4.07e+01, 1.74e-06, 0, 0 ]
    prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
    tau21 = "(jet1Tau21<0.60&jet2Tau21<0.60)"
    ThetaFileMaker( "b1t1", onebtag+"&"+oneTop, bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, tau21, prelimFit, fitBins, HT, isMC )
#    ThetaFileMaker( "b1t1", "( ("+jet1Top+"&"+jet2btag+")||("+jet2Top+"&"+jet1btag+") )", bins, 60, 350, Xcut, Ycut, isMC )
if int(channel) == 7:
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
    ThetaFileMaker( "b2t1", twobtag+"&"+oneTop, bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, tau21, prelimFit, 25, HT, isMC )
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
    ThetaFileMaker( "b0t2", zerobtag+"&"+twoTop, bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, tau21, prelimFit, 25, HT, isMC )
if int(channel) == 9:
    fitBins = 25
    if "CSVv2" in method and "BCD" in method:
        #prelimFit = [ -1.60, 9.68e-01, -6.51e-09 ]
        prelimFit = [ 7.45e-01, 4.41e-02, -3.56e-07 ]
    elif "CSVv2" in method and "CBD" in method:
        prelimFit = [ 2.21, 9.56, -3.36e-07 ]
    elif "CMVAv2" in method and "BCD" in method:
        fitBins = 50
        #prelimFit = [ 9.80e-02, -7.53e-03, -2.59e-08 ]
        prelimFit = [ 7.45e-01, 4.41e-02, -3.56e-07 ]
    elif "CMVAv2" in method and "CBD" in method:
        #prelimFit = [ 2.10, 9.60e-01, -3.18e-07 ]
        prelimFit = [ 7.45e-01, 4.41e-02, -3.56e-07 ]
    else:
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
    '''
    if "CSVv2" in method and "BCD" in method:
        prelimFit =  [ 8.92e-01, -1.61, -4.75e-07 ]
    elif "CSVv2" in method and "CBD" in method:
        prelimFit = [ 3.30, 2.11, -7.62e-07 ]
    elif "CMVAv2" in method and "BCD" in method:
        prelimFit = [ 9.28e-01, -4.07e+01, 1.74e-06 ]
    elif "CMVAv2" in method and "CBD" in method:
        prelimFit = [ 2.75, 1.98, -6.32e-07 ]
    else:
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
        '''    
    prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
    tau21 = "(jet1Tau21<0.60&jet2Tau21<0.60)"
    ThetaFileMaker( "b1t2", onebtag+"&"+twoTop, bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, tau21, prelimFit, fitBins, HT, isMC )
if int(channel) == 10:
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
#    prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
    tau21 = "(jet1Tau21<0.60&jet2Tau21<0.60)"
    ThetaFileMaker( "b2t2", twobtag+"&"+twoTop, bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, tau21, prelimFit, 25, HT, isMC )
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
    ThetaFileMaker( "b0t12", zerobtag+"&(jet1Tau32<0.51||jet2Tau32<0.51)", bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, tau21, prelimFit, 25, HT, isMC )
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
    tau21 = "(jet1Tau21<0.60&jet2Tau21<0.60)"
    ThetaFileMaker( "b1t12", onebtag+"&(jet1Tau32<0.51||jet2Tau32<0.51)", bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, tau21, prelimFit, 25, HT, isMC )
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
    tau21 = "(jet1Tau21<0.60&jet2Tau21<0.60)"
    ThetaFileMaker( "b2t12", twobtag+"&(jet1Tau32<0.51||jet2Tau32<0.51)", bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, tau21, prelimFit, 25, HT, isMC )
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
    tau21 = 'jet1Tau21<0.60&jet2Tau21<0.60'
    ThetaFileMaker( "pres", "(jet1btagCSVv2<0.8484&jet2btagCSVv2<0.8484&( (jet1Tau32>0.67&jet2Tau32<0.67)||(jet1Tau32<0.67&jet2Tau32>0.67)))", bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, tau21, prelimFit, 25, HT, isMC )
