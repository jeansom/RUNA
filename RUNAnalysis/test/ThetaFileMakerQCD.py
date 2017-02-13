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
def ThetaFileMaker( chan, chanCuts, bins, minBin, maxBin, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleAlpha, scaleAlphaErr, tau21, prelimFit, fitBins, isMC=True ):
    gStyle.SetOptStat(0)
    # Setting basic distributions
    # Setting basic distributions
    weight = "(36600*puWeight*lumiWeight/15*2.74297e-01)"

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

    # W norm up
    MakeFitPlots( EstMassWJUp, FMassWJUp, binsMass, "prunedMassAve", Xcut[0], var_arrayMass, presel+"&"+chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "",  "outputs/"+directory+method+"/MassWJUp"+chan, False ) # Creates the 2D plot, ratio, and ratio fit
    MakeEstPlots( EstMassWJUp, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/MassWJUp"+chan, isMC, False ) # Makes the actual estimation

    # W norm dn
    MakeFitPlots( EstMassWJDn, FMassWJDn, binsMass, "prunedMassAve", Xcut[0], var_arrayMass, presel+"&"+chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "", "outputs/"+directory+method+"/MassWJDn"+chan, False ) # Creates the 2D plot, ratio, and ratio fit
    MakeEstPlots( EstMassWJDn, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/MassWJDn"+chan, isMC, False ) # Makes the actual estimation

    # T norm up
    MakeFitPlots( EstMassTTUp, FMassTTUp, binsMass, "prunedMassAve", Xcut[0], var_arrayMass, presel+"&"+chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "", "outputs/"+directory+method+"/MassTTUp"+chan, False ) # Creates the 2D plot, ratio, and ratio fit
    MakeEstPlots( EstMassTTUp, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/MassTTUp"+chan, isMC, False ) # Makes the actual estimation

    # T norm dn
    MakeFitPlots( EstMassTTDn, FMassTTDn, binsMass, "prunedMassAve", Xcut[0], var_arrayMass, presel+"&"+chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "", "outputs/"+directory+method+"/MassTTDn"+chan, False ) # Creates the 2D plot, ratio, and ratio fit
    MakeEstPlots( EstMassTTDn, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/MassTTDn"+chan, isMC, False ) # Makes the actual estimation

    # T alpha up
    MakeFitPlots( EstMassTTAlphaUp, FMassTTAlphaUp, binsMass, "prunedMassAve", Xcut[0], var_arrayMass, presel+"&"+chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "", "outputs/"+directory+method+"/MassTTAlphaUp"+chan, False ) # Creates the 2D plot, ratio, and ratio fit
    MakeEstPlots( EstMassTTAlphaUp, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/MassTTAlphaUp"+chan, isMC, False ) # Makes the actual estimation

    # T alpha dn
    MakeFitPlots( EstMassTTAlphaDn, FMassTTAlphaDn, binsMass, "prunedMassAve", Xcut[0], var_arrayMass, presel+"&"+chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "", "outputs/"+directory+method+"/MassTTAlphaDn"+chan, False ) # Creates the 2D plot, ratio, and ratio fit
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
    chan__DATA = TH1D( chan+"__DATA", chan+"__DATA", bins, minBin, maxBin )
    chan__QCD = TH1D( chan+"__QCD", chan+"__QCD", bins, minBin, maxBin )
    chan__TTBAR = TH1D( chan+"__TTBAR", chan+"__TTBar", bins, minBin, maxBin )
    chan__QCD__Fit__up = TH1D( chan+"__QCD__Fit"+chan+"__up", chan+"__QCD__Fit"+chan+"__up", bins, minBin, maxBin )
    chan__QCD__Fit__down = TH1D( chan+"__QCD__Fit"+chan+"__down", chan+"__QCD__Fit"+chan+"`__down", bins, minBin, maxBin )
    chan__TTBAR__TTScale__up = TH1D( chan+"__TTBAR__TTScale__up", chan+"__TTBAR__TTScale__up", bins, minBin, maxBin )
    chan__TTBAR__TTScale__down = TH1D( chan+"__TTBAR__TTScale__down", chan+"__TTBAR__TTScale__down", bins, minBin, maxBin )
    chan__QCD__TTScale__up = TH1D( chan+"__QCD__TTScale__up", chan+"__QCD__TTScale__up", bins, minBin, maxBin )
    chan__QCD__TTScale__down = TH1D( chan+"__QCD__TTScale__down", chan+"__QCD__TTScale__down", bins, minBin, maxBin )
    chan__TTBAR__TTAlphaScale__up = TH1D( chan+"__TTBAR__TTAlphaScale__up", chan+"__TTBAR__TTAlphaScale__up", bins, minBin, maxBin )
    chan__TTBAR__TTAlphaScale__down = TH1D( chan+"__TTBAR__TTAlphaScale__down", chan+"__TTBAR__TTAlphaScale__down", bins, minBin, maxBin )
    chan__QCD__TTAlphaScale__up = TH1D( chan+"__QCD__TTAlphaScale__up", chan+"__QCD__TTAlphaScale__up", bins, minBin, maxBin )
    chan__QCD__TTAlphaScale__down = TH1D( chan+"__QCD__TTAlphaScale__down", chan+"__QCD__TTAlphaScale__down", bins, minBin, maxBin )
#    if not("b2" in chan or "t2" in chan) or True:
    chan__WJETS = TH1D( chan+"__WJETS", chan+"__WJETS", bins, minBin, maxBin )
    chan__WJETS__WJScale__up = TH1D( chan+"__WJETS__WJScale__up", chan+"__WJETS__WJScale__up", bins, minBin, maxBin )
    chan__WJETS__WJScale__down = TH1D( chan+"__WJETS__WJScale__down", chan+"__WJETS__WJScale__down", bins, minBin, maxBin )
    chan__QCD__WJScale__up = TH1D( chan+"__QCD__WJScale__up", chan+"__QCD__WJScale__up", bins, minBin, maxBin )
    chan__QCD__WJScale__down = TH1D( chan+"__QCD__WJScale__down", chan+"__QCD__WJScale__down", bins, minBin, maxBin )

#    chan__WJETS__A = TH1D( chan+"__WJETS__A", chan+"__WJETS__A", bins, minBin, maxBin )
#    chan__WJETS__WJScale__up__A = TH1D( chan+"__WJETS__WJScale__up__A", chan+"__WJETS__WJScale__up__A", bins, minBin, maxBin )
#    chan__WJETS__WJScale__down__A = TH1D( chan+"__QCD__TTScale__down__A", chan+"__QCD__TTScale__down__A", bins, minBin, maxBin )

    for i in EstMass.hists_EST: # Adds the plus histograms into the nominal bkg est
        chan__QCD.Add( i, 1. )
    for i in EstMass.hists_EST_SUB: # Subtracts the minus histograms from the nominal bkg est DOES NOT ADD THE SIGNAL MINUS REGIONS BACK IN
        chan__QCD.Add( i, -1. )

    for i in EstMass.hists_EST_UP: # Adds the plus histograms into the fit error up bkg est
        chan__QCD__Fit__up.Add( i, 1. )
    for i in Est.hists_EST_SUB_UP: # Subtracts the minus histograms from the fit error up bkg est DOES NOT ADD THE SIGNAL MINUS REGIONS BACK IN
        chan__QCD__Fit__up.Add( i, -1. )
    
    for i in EstMass.hists_EST_DN: # Adds the plus histograms into the fit error down bkg est
        chan__QCD__Fit__down.Add( i, 1. )
    for i in Est.hists_EST_SUB_DN: # Subtracts the minus histograms from the fit error down bkg est DOES NOT ADD THE SIGNAL MINUS REGIONS BACK IN
        chan__QCD__Fit__down.Add( i, -1. )

    for i in EstMassWJUp.hists_EST: # Adds the plus histograms into the W norm. up bkg est
        chan__QCD__WJScale__up.Add( i, 1. )
    for i in EstWJUp.hists_EST_SUB: # Subtracts the minus histograms from the W norm up bkg est DOES NOT ADD THE SIGNAL MINUS REGIONS BACK IN
        chan__QCD__WJScale__up.Add( i, -1. )

    for i in EstMassWJDn.hists_EST: # Adds the plus histograms into the W norm down bkg est
        chan__QCD__WJScale__down.Add( i, 1. )
    for i in EstMassWJDn.hists_EST_SUB: # Subtracts the minus histograms from the W norm down bkg est DOES NOT ADD THE SIGNAL MINUS REGIONS BACK IN
        chan__QCD__WJScale__down.Add( i, -1. )

    for i in EstMassTTUp.hists_EST: # Adds the plus histograms into the T norm up bkg est
        chan__QCD__TTScale__up.Add( i, 1. )
    for i in EstMassTTUp.hists_EST_SUB: # Subtracts the minus histograms from the T norm up bkg est DOES NOT ADD THE SIGNAL MINUS REGIONS BACK IN
        chan__QCD__TTScale__up.Add( i, -1. )

    for i in EstMassTTDn.hists_EST: # Adds the plus histograms into the T norm down bkg est
        chan__QCD__TTScale__down.Add( i, 1. )
    for i in EstMassTTDn.hists_EST_SUB: # Subtracts the minus histograms from the T norm down bkg est DOES NOT ADD THE SIGNAL MINUS REGIONS BACK IN
        chan__QCD__TTScale__down.Add( i, -1. )

    for i in EstMassTTAlphaUp.hists_EST: # Adds the plus histograms into the alpha up bkg est
        chan__QCD__TTAlphaScale__up.Add( i, 1. )
    for i in EstMassTTAlphaUp.hists_EST_SUB: # Subtracts the minus histograms from the alpha up bkg est DOES NOT ADD THE SIGNAL MINUS REGIONS BACK IN
        chan__QCD__TTAlphaScale__up.Add( i, -1. )

    for i in EstMassTTAlphaDn.hists_EST: # Adds the plus histograms into the alpha down bkg est
        chan__QCD__TTAlphaScale__down.Add( i, 1. )
    for i in EstMassTTAlphaDn.hists_EST_SUB: # Subtracts the minus histograms from the alpha down bkg est DOES NOT ADD THE SIGNAL MINUS REGIONS BACK IN
        chan__QCD__TTAlphaScale__down.Add( i, -1. )

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
    tau21 = '.60'
    prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
elif "CMVAv2M" in method:
    zerobtag = "(jet1btagCMVAv2<0.4432&jet2btagCMVAv2<0.4432)"
    onebtag = "((jet1btagCMVAv2<0.4432&jet2btagCMVAv2>0.4432)||(jet1btagCMVAv2>0.4432&jet2btagCMVAv2<0.4432))"
    twobtag = "(jet1btagCMVAv2>0.4432&jet2btagCMVAv2>0.4432)"
    jet1btag = "((jet1btagCMVAv2>0.4432&jet2btagCMVAv2<0.4432))"
    jet2btag = "((jet1btagCMVAv2<0.4432&jet2btagCMVAv2>0.4432))"
    tau21 = '.60'
    if "BCD" in method:
        prelimFit = [ 4.88e-01, -7.53e-01, -1.62e-07, 0, 0 ]
elif "CMVAv2T" in method:
    zerobtag = "(jet1btagCMVAv2<0.9432&jet2btagCMVAv2<0.9432)"
    onebtag = "((jet1btagCMVAv2<0.9432&jet2btagCMVAv2>0.9432)||(jet1btagCMVAv2>0.9432&jet2btagCMVAv2<0.9432))"
    twobtag = "(jet1btagCMVAv2>0.9432&jet2btagCMVAv2>0.9432)"
    jet1btag = "((jet1btagCMVAv2>0.9432&jet2btagCMVAv2<0.9432))"
    jet2btag = "((jet1btagCMVAv2<0.9432&jet2btagCMVAv2>0.9432))"
    tau21 = '.60'
    prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
else:
    print "Method not found: " +method
    sys.exit(0)

prelimFit = [ 2.28, 7.00e-01, -2.13e-07, 0, 0 ]

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
    if 'CMVAv2M' in method  and 'BCD' in method:
        scaleTT = -3.185742746170277
        scaleTTErr = 0.42278115765072877 
    
        scaleW = -1.2073601041511757
        scaleWErr = 0.33091212974591744
        scaleTTAlpha = 1.3021375313658075
        scaleTTAlphaErr = 0.2705877405580508
    elif 'CMVAv2M' in method  and 'CBD' in method:
        scaleTT = -2.3255419637053003
        scaleTTErr = 0.43127906364109836
        scaleW = -1.5920138087416715
        scaleWErr = 0.42468830360248355
        scaleTTAlpha = 1.0329314734165136
        scaleTTAlphaErr = 0.27493854736972434
    elif 'CSVv2M' in method  and 'BCD' in method:
        scaleTT = -2.7106548869462617
        scaleTTErr = 0.38755407332482683
        scaleW = -1.3462520245584724
        scaleWErr = 0.3336517099549743
        scaleTTAlpha = 0.8775585031141873
        scaleTTAlphaErr = 0.21546440726373328
    elif 'CSVv2M' in method  and 'CBD' in method:
        scaleTT = -0.9130354595971122
        scaleTTErr = 0.5810981065498508
        scaleW = -1.6220527381449101
        scaleWErr = 0.4278069505107658
        scaleTTAlpha = 0.24127780944242616
        scaleTTAlphaErr = 0.4295862763365301
    elif 'CMVAv2T' in method  and 'BCD' in method:
        scaleTT = -3.185742746170277
        scaleTTErr = 0.42278115765072877     
        scaleW = -1.2073601041511757
        scaleWErr = 0.33091212974591744
        scaleTTAlpha = 1.3021375313658075
        scaleTTAlphaErr = 0.2705877405580508
    elif 'CMVAv2R' in method  and 'CBD' in method:
        scaleTT = -2.3255419637053003
        scaleTTErr = 0.43127906364109836
        scaleW = -1.5920138087416715
        scaleWErr = 0.42468830360248355
        scaleTTAlpha = 1.0329314734165136
        scaleTTAlphaErr = 0.27493854736972434
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
    elif "CSVv2" in method and "CBD" in method:
        prelimFit = [ 2.19, 1.02, -3.92e-07 ]
    elif "CMVAv2" in method and "BCD" in method:
        prelimFit = [ 8.15e-01, -1.23, -6.56e-08, 0, 0]
    elif "CMVAv2" in method and "CBD" in method:
        prelimFit = [ 2.26, 1.01, -4.13e-07, 0, 0]
    else:
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]

    ThetaFileMaker( "b0t0", zerobtag+"&"+zeroTop, bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, tau21, prelimFit, 25, isMC )
if int(channel) == 1:
    fitBins = 25
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
        #prelimFit = [ 7.45e-01, 4.41e-02, -3.56e-07 ]
        prelimFit = [ 2.27, 7.04e-01, -2.12e-07 ]
    else:
        prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
    ThetaFileMaker( "b1t0", onebtag+"&"+zeroTop, bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, tau21, prelimFit, fitBins, isMC )
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
    ThetaFileMaker( "b2t0", twobtag+"&"+zeroTop, bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, tau21, prelimFit, 25, isMC )
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
    ThetaFileMaker( "b0t1", zerobtag+"&"+oneTop, bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, tau21, prelimFit, 25, isMC )
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
        #prelimFit = [ 9.28e-01, -4.07e+01, 1.74e-06, 0, 0 ]
    ThetaFileMaker( "b1t1", onebtag+"&"+oneTop, bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, tau21, prelimFit, 25, isMC )
#    ThetaFileMaker( "b1t1", "( ("+jet1Top+"&"+jet2btag+")||("+jet2Top+"&"+jet1btag+") )", bins, 60, 350, Xcut, Ycut, isMC )
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
    ThetaFileMaker( "b2t1", twobtag+"&"+oneTop, bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, tau21, prelimFit, 25, isMC )
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
    ThetaFileMaker( "b0t2", zerobtag+"&"+twoTop, bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, tau21, prelimFit, 25, isMC )
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
    ThetaFileMaker( "b1t2", onebtag+"&"+twoTop, bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, tau21, prelimFit, 25, isMC )
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
    ThetaFileMaker( "b2t2", twobtag+"&"+twoTop, bins, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, tau21, prelimFit, 25, isMC )
