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
def ThetaFileMaker( chan, chanCuts, bins, minBin, maxBin, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleAlpha, scaleAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, fitBins, HT, isMC=True, log=True ):
    gStyle.SetOptStat(0)
    # Setting basic distributions
    weight = "(36555.21/15*lumiWeight*puWeight)"

    # The T and W scales
    TTNorm = "( (1.06)*(1+.2*"+str(scaleTT)+"))" # The scale that determines the nominal TTBar normalization
    TTNormUp = "( (1.06)*(1+.2*" + str(scaleTT) + "+.2*" + str(scaleTTErr) + ") )" # Upper TTBar normalization
    TTNormDn = "( (1.06)*(1+.2*" + str(scaleTT) + "-.2*" + str(scaleTTErr) + ") )" # Lower TTBar normalization

    TTAlpha = "exp( (-0.0005*(HT/2))*(1-.2*" + str(scaleAlpha) + ") )" # The scale that determines the nominal alpha NOTE: subtracting = adding because -0.0005
    TTAlphaUp = "exp( (-0.0005*(HT/2))*(1-.2*" + str(scaleAlpha) + "-.2*" + str(scaleAlphaErr) + ") )" # Upper alpha NOTE: subtracting = adding because -0.0005
    TTAlphaDn = "exp( (-0.0005*(HT/2))*(1-.2*" + str(scaleAlpha) + "+.2*" + str(scaleAlphaErr) + ") )" # Lower alpha NOTE: subtracting = adding because -0.0005

    TTScaleStrNorm = "(1.06*exp( (-0.0005*(HT/2)) ))"
    TTScaleStr = "(" + TTNorm + "*" + TTAlpha + ")" # Total string to scale TT by, norm*alpha
    TTScaleErrUpStr = "(" + TTNormUp + "*" + TTAlpha + ")" # String for scaling TT with norm up, normUp*alpha
    TTScaleErrDnStr = "(" + TTNormDn + "*" + TTAlpha + ")" # String for scaling TT with norm dn, normDn*alpha
    AlphaScaleUpStr = "(" + TTNorm + "*" + TTAlphaUp + ")" # Total string to scale TT by with alpha up, norm*alphaUp
    AlphaScaleDnStr = "(" + TTNorm + "*" + TTAlphaDn + ")" # Total string to scale TT by with alpha dn, norm*alphaDn

    WScaleStr = "(1+.2*"+str(scaleW)+")" # The scale that determines the nominal W normalization
    WScaleUpStr = "(1+.2*"+str(scaleW)+"+.2*"+str(scaleWErr)+")" # Upper W normalization
    WScaleDnStr = "(1+.2*"+str(scaleW)+"-.2*"+str(scaleWErr)+")" # Lower W normalization

    TopScaleStr = "(1+.2*"+str(scaleTop)+")"
    TopScaleUpStr = "(1+.2*"+str(scaleTop)+"+2*"+str(scaleTopErr)+")"
    TopScaleDnStr = "(1+.2*"+str(scaleTop)+"-2*"+str(scaleTopErr)+")"

    # Create the distributions
    DATA = DIST( "DATA", "80XRootFilesUpdated/RUNAnalysis_JetHT_Run2016_80X_V2p3_v06_cut15.root", "BoostedAnalysisPlotsPuppi/RUNATree", "1" )
    QCD = []
    for i in [ "QCDPt170to300", "QCDPt300to470", "QCDPt470to600", "QCDPt600to800", "QCDPt800to1000", "QCDPt1000to1400", "QCDPt1400to1800", "QCDPt1800to2400", "QCDPt2400to3200", "QCDPt3200toInf" ]:
        QCD.append( DIST( i, "80XRootFilesUpdated/RUNAnalysis_"+i+"_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor(i)) ) )

    TTJetsNorm = DIST( "TTJets", "80XRootFilesUpdated/RUNAnalysis_TT_PtRewt_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "("+weight+"*"+TTScaleStrNorm+")" )
    TTJets = DIST( "TTJets", "80XRootFilesUpdated/RUNAnalysis_TT_PtRewt_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "("+weight+"*"+TTScaleStr+")" )
    TTJetsUp = DIST( "TTJetsUp", "80XRootFilesUpdated/RUNAnalysis_TT_PtRewt_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "("+weight+"*"+TTScaleErrUpStr+")" )
    TTJetsDn = DIST( "TTJetsDn", "80XRootFilesUpdated/RUNAnalysis_TT_PtRewt_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "("+weight+"*"+TTScaleErrDnStr+")"  )
    TTJetsAlphaUp = DIST( "TTJetsUp", "80XRootFilesUpdated/RUNAnalysis_TT_PtRewt_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "("+weight+"*"+AlphaScaleUpStr+")")
    TTJetsAlphaDn = DIST( "TTJetsDn", "80XRootFilesUpdated/RUNAnalysis_TT_PtRewt_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree",  "("+weight+"*"+AlphaScaleDnStr+")" )

    WJetsNorm = DIST( "WJets", "80XRootFilesUpdated/RUNAnalysis_WJetsToQQ_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree",  "("+weight+")" )
    WJets = DIST( "WJets", "80XRootFilesUpdated/RUNAnalysis_WJetsToQQ_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree",  "("+weight+"*"+WScaleStr+")" )
    WJetsUp = DIST( "WJetsUp", "80XRootFilesUpdated/RUNAnalysis_WJetsToQQ_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "("+weight+"*"+WScaleUpStr+")" )
    WJetsDn = DIST( "WJetsDn", "80XRootFilesUpdated/RUNAnalysis_WJetsToQQ_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "("+weight+"*"+WScaleDnStr+")" )

    TopNorm = DIST( "TopNorm", "80XRootFilesUpdated/RUNAnalysis_ST_t-channel_topantitop_4f_inclusiveDecays_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree",  "("+weight+")" )
    Top = DIST( "Top", "80XRootFilesUpdated/RUNAnalysis_ST_t-channel_topantitop_4f_inclusiveDecays_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree",  "("+weight+"*"+TopScaleStr+")" )
    TopUp = DIST( "TopUp", "80XRootFilesUpdated/RUNAnalysis_ST_t-channel_topantitop_4f_inclusiveDecays_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "("+weight+"*"+TopScaleUpStr+")" )
    TopDn = DIST( "TopDn", "80XRootFilesUpdated/RUNAnalysis_ST_t-channel_topantitop_4f_inclusiveDecays_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "("+weight+"*"+TopScaleDnStr+")" )

    Sig120 = DIST( "Sig", "80XRootFilesUpdated/Signals/RUNAnalysis_RPVStopStopToJets_UDD323_M-120_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "puWeight*689.799/746680*100" )
    Sig280 = DIST( "Sig", "80XRootFilesUpdated/Signals/RUNAnalysis_RPVStopStopToJets_UDD323_M-240_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "puWeight*26.476/153653*100" )

    # Creating Alphabet objects to run estimate on    
    if isMC: # If running over the MC
        Dists = QCD
        DistsSub = []
    else:  # Otherwise
        Dists = [DATA] # Use data 
        DistsSub = [ Top, WJets, TTJets ] # Nominal distributions to subtract

    DistSig = [Sig120, Sig280]

    ## Defining Cuts
    presel = tau21
    cuts = Xcut[0]+"<"+Xcut[1]+"&"+Ycut[0]+"<"+Ycut[1]
    anticuts = Xcut[0]+">"+Xcut[1]+"&"+Ycut[0]+"<"+Ycut[1]
    cutsB = Xcut[0]+"<"+Xcut[1]+"&"+Ycut[0]+">"+Ycut[1]
    cutsD = Xcut[0]+">"+Xcut[1]+"&"+Ycut[0]+">"+Ycut[1]
    cut = [ float(Xcut[1]), "<" ] # For defining B vs D regions
    
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
    
    #### Makes list with bins for fit
    binsMass = []
    binWidth = fitBins
    NBins = int(((350-50))/binWidth)
    var_arrayMass = [ "prunedMassAve", Xcut[0], NBins, 50., 350., Xcut[2], Xcut[3], Xcut[4] ] # For making B,D plot
    for i in xrange( 0, NBins ):
        binsMass.append( [ var_arrayMass[3]+binWidth*i, var_arrayMass[3]+binWidth*(i+1) ] )

    #### Form of fit
    FMass = SigmoidFit(prelimFit,60, 350,"Mass","SEMR") # Nominal fit
    FMass1 = SigmoidFit(prelimFit,60, 350,"Mass1","SEMR") # Nominal fit again, used if staying blinded

    FMassWJUp = SigmoidFit(prelimFit,60, 350,"Mass","SEMR") # Fit W norm. up
    FMassWJDn = SigmoidFit(prelimFit,60, 350,"Mass","SEMR") # Fit W norm. dn

    FMassTTUp = SigmoidFit(prelimFit,60, 350,"Mass","SEMR") # Fit T norm. up
    FMassTTDn = SigmoidFit(prelimFit,60, 350,"Mass","SEMR") # Fit T norm. dn
    FMassTTAlphaUp = SigmoidFit(prelimFit,60, 350,"Mass","SEMR") # Fit T alpha up
    FMassTTAlphaDn = SigmoidFit(prelimFit,60, 350,"Mass","SEMR") # Fit T alpha dn
    FMassTopUp = SigmoidFit(prelimFit,60, 350,"Mass","SEMR") # Fit T alpha up
    FMassTopDn = SigmoidFit(prelimFit,60, 350,"Mass","SEMR") # Fit T alpha dn

    # Bins for final estimation plot, bin width int(bins)
    binBoundaries = []
    dBin = float(bins)
    i = minBin
    while i<maxBin+1:
        binBoundaries.append(i)
        i=i+dBin

    # Use alternate channel's fits when low statistics
    if "t2" in chan: chanCutsTemp = presel+"&"+twoTop
    else: chanCutsTemp = presel+"&"+chanCuts

    # Nominal
    MakeFitPlots( EstMass, FMass, binsMass, "prunedMassAve", Xcut[0], var_arrayMass, chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "", "outputs/"+directory+method+"/Mass"+chan, binBoundaries, True, False ) # Creates the 2D plot, ratio, and ratio fit
    MakeEstPlots( EstMass, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/Mass"+chan, True, isMC, False, log ) # Makes the actual estimation

    # W norm up
    MakeFitPlots( EstMassWJUp, FMassWJUp, binsMass, rho, Xcut[0], var_arrayMass, chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "",  "outputs/"+directory+method+"/MassWJUp"+chan, binBoundaries, True, False ) # Creates the 2D plot, ratio, and ratio fit
    MakeEstPlots( EstMassWJUp, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/MassWJUp"+chan, True, isMC, False, log ) # Makes the actual estimation

    # W norm dn
    MakeFitPlots( EstMassWJDn, FMassWJDn, binsMass, rho, Xcut[0], var_arrayMass, chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "", "outputs/"+directory+method+"/MassWJDn"+chan, binBoundaries, True, False ) # Creates the 2D plot, ratio, and ratio fit
    MakeEstPlots( EstMassWJDn, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/MassWJDn"+chan, True, isMC, False, log ) # Makes the actual estimation

    # T norm up
    MakeFitPlots( EstMassTTUp, FMassTTUp, binsMass, rho, Xcut[0], var_arrayMass, chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "", "outputs/"+directory+method+"/MassTTUp"+chan, binBoundaries, True, False ) # Creates the 2D plot, ratio, and ratio fit
    MakeEstPlots( EstMassTTUp, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/MassTTUp"+chan, True, isMC, False, log ) # Makes the actual estimation

    # T norm dn
    MakeFitPlots( EstMassTTDn, FMassTTDn, binsMass, rho, Xcut[0], var_arrayMass, chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "", "outputs/"+directory+method+"/MassTTDn"+chan, binBoundaries, True, False ) # Creates the 2D plot, ratio, and ratio fit
    MakeEstPlots( EstMassTTDn, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/MassTTDn"+chan, True, isMC, False, log ) # Makes the actual estimation

    # T alpha up
    MakeFitPlots( EstMassTTAlphaUp, FMassTTAlphaUp, binsMass, rho, Xcut[0], var_arrayMass, chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "", "outputs/"+directory+method+"/MassTTAlphaUp"+chan, binBoundaries, True, False ) # Creates the 2D plot, ratio, and ratio fit
    MakeEstPlots( EstMassTTAlphaUp, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/MassTTAlphaUp"+chan, True, isMC, False, log ) # Makes the actual estimation

    # T alpha dn
    MakeFitPlots( EstMassTTAlphaDn, FMassTTAlphaDn, binsMass, rho, Xcut[0], var_arrayMass, chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "", "outputs/"+directory+method+"/MassTTAlphaDn"+chan, binBoundaries, True, False ) # Creates the 2D plot, ratio, and ratio fit
    MakeEstPlots( EstMassTTAlphaDn, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/MassTTAlphaDn"+chan, True, isMC, False, log ) # Makes the actual estimation

    MakeFitPlots( EstMassTopUp, FMassTopUp, binsMass, rho, Xcut[0], var_arrayMass, chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "", "outputs/"+directory+method+"/MassTopUp"+chan, binBoundaries, True, False ) # Creates the 2D plot, ratio, and ratio fit
    MakeEstPlots( EstMassTopUp, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/MassTopUp"+chan, True, isMC, False, log ) # Makes the actual estimation

    MakeFitPlots( EstMassTopDn, FMassTopDn, binsMass, rho, Xcut[0], var_arrayMass, chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "", "outputs/"+directory+method+"/MassTopDn"+chan, binBoundaries, True, False ) # Creates the 2D plot, ratio, and ratio fit
    MakeEstPlots( EstMassTopDn, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/MassTopDn"+chan, True, isMC, False, log ) # Makes the actual estimation

    # Makes root file with basic fits

    FITFILE = TFile( "outputs/"+directory+method+"/LIM_FIT"+chan+".root", "RECREATE" )
    FITFILE.cd()
    
    FIT_Points = (EstMass.G).Clone("G_"+chan) # Ratio plot
#    FIT = (EstMass.Fit.fit).Clone("Fit_"+chan) # Fit of ratio 
#    FIT_Up = (EstMass.Fit.ErrUp).Clone("FitUp_"+chan) # Fit err up
#    FIT_Dn = (EstMass.Fit.ErrDn).Clone("FitDn_"+chan) # Fit err dn

    FIT_Points.Write()
#    FIT.Write()
#    FIT_Up.Write()
#    FIT_Dn.Write()

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
    for i in EstMass.hists_EST_UP: 
        chan__QCD__Fit__up.Add( i, 1. )
    for i in EstMass.hists_EST_SUB_UP: 
        chan__QCD__Fit__up.Add( i, -1. )
    removeNegativeBins(chan__QCD__Fit__up)
    for i in EstMass.hists_EST_DN: 
        chan__QCD__Fit__down.Add( i, 1. )
    for i in EstMass.hists_EST_SUB_DN: 
        chan__QCD__Fit__down.Add( i, -1. )
    removeNegativeBins(chan__QCD__Fit__down)
    for i in EstMassWJUp.hists_EST: 
        chan__QCD__WJScale__up.Add( i, 1. )
    for i in EstMassWJUp.hists_EST_SUB: 
        chan__QCD__WJScale__up.Add( i, -1. )
    removeNegativeBins(chan__QCD__WJScale__up)
    for i in EstMassWJDn.hists_EST: 
        chan__QCD__WJScale__down.Add( i, 1. )
    for i in EstMassWJDn.hists_EST_SUB:
        chan__QCD__WJScale__down.Add( i, -1. )
    removeNegativeBins(chan__QCD__WJScale__down)
    for i in EstMassTTUp.hists_EST: 
        chan__QCD__TTScale__up.Add( i, 1. )
    for i in EstMassTTUp.hists_EST_SUB: 
        chan__QCD__TTScale__up.Add( i, -1. )
    removeNegativeBins(chan__QCD__TTScale__up)
    for i in EstMassTTDn.hists_EST:
        chan__QCD__TTScale__down.Add( i, 1. )
    for i in EstMassTTDn.hists_EST_SUB:
        chan__QCD__TTScale__down.Add( i, -1. )
    removeNegativeBins(chan__QCD__TTScale__down)
    for i in EstMassTTAlphaUp.hists_EST:
        chan__QCD__TTAlphaScale__up.Add( i, 1. )
    for i in EstMassTTAlphaUp.hists_EST_SUB:
        chan__QCD__TTAlphaScale__up.Add( i, -1. )
    removeNegativeBins(chan__QCD__TTAlphaScale__up)
    for i in EstMassTTAlphaDn.hists_EST:
        chan__QCD__TTAlphaScale__down.Add( i, 1. )
    for i in EstMassTTAlphaDn.hists_EST_SUB:
        chan__QCD__TTAlphaScale__down.Add( i, -1. )
    removeNegativeBins(chan__QCD__TTAlphaScale__down)
    for i in EstMassTTAlphaUp.hists_EST:
        chan__QCD__TopScale__up.Add( i, 1. )
    for i in EstMassTTAlphaUp.hists_EST_SUB:
        chan__QCD__TopScale__up.Add( i, -1. )
    removeNegativeBins(chan__QCD__TopScale__up)
    for i in EstMassTTAlphaDn.hists_EST:
        chan__QCD__TopScale__down.Add( i, 1. )
    for i in EstMassTTAlphaDn.hists_EST_SUB:
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
if "T" in args.log:
    log = True
else:
    log = False
os.mkdir("outputs/"+directory+method)

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
    scaleArray = {'TopScale': [(-0.7250048992454996, 0.9271283495324534)], 'WJScale': [(-0.8888615417517887, 0.9478155202667431)], '__nll': [-13239.090718238278], 'TTAlphaScale': [(-0.14481072740234513, 0.9747820320286127)], 'TTScale': [(-0.6096666511137068, 0.7844218149587794)]}
    scaleTT = scaleArray['TTScale'][0][0]
    scaleTTErr = scaleArray['TTScale'][0][1]
    scaleW = scaleArray['WJScale'][0][0]
    scaleWErr = scaleArray['WJScale'][0][1]
    scaleTTAlpha = scaleArray[ 'TTAlphaScale' ][0][0]
    scaleTTAlphaErr = scaleArray[ 'TTAlphaScale' ][0][1]
    scaleTop = scaleArray[ 'TopScale' ][0][0]
    scaleTopErr = scaleArray[ 'TopScale' ][0][1]

prelimFit = [ 1.733,.7634,-3.516e-07,0,0 ]
tau21 = "(jet1Tau21-DDT)<0&(jet2Tau21-DDT)<0"

# Sets preliminary fit depending on channel/method and runs ThetaFileMaker
if int(channel) == 1:
    ThetaFileMaker( "b0t0T", zerobtag+"&"+zeroTop, 10, 60., 350., Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, 25, HT, isMC, log )
if int(channel) == 3:
    ThetaFileMaker( "b1t0T", onebtag+"&"+zeroTop, 10, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, 25, HT, isMC, log )
if int(channel) == 4:
    ThetaFileMaker( "b2t0", twobtag+"&"+zeroTop, 10, 60., 350., Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, 25, HT, isMC, log )
if int(channel) == 5:
    ThetaFileMaker( "b0t1", zerobtag+"&"+oneTop, 10, 60, 250, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, 25, HT, isMC, log )
if int(channel) == 6:
    ThetaFileMaker( "b1t1", onebtag+"&"+oneTop, 10, 60, 250, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, 25, HT, isMC, log )
if int(channel) == 7:
    ThetaFileMaker( "b2t1", twobtag+"&"+oneTop, 10, 60, 250, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, 25, HT, isMC, log )
if int(channel) == 8:
    ThetaFileMaker( "b0t2", zerobtag+"&"+twoTop, 10, 100, 250, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, 25, HT, isMC, log )
if int(channel) == 9:
    ThetaFileMaker( "b1t2", onebtag+"&"+twoTop, 10, 100, 250, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, 25, HT, isMC, log )
if int(channel) == 10:
    ThetaFileMaker( "b2t2", twobtag+"&"+twoTop, 10, 100, 250, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, 25, HT, isMC, log )
if int(channel) == 11:
    ThetaFileMaker( "pres", "(abs(jet1Pt)>-999)", 10, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, scaleTTAlpha, scaleTTAlphaErr, scaleTop, scaleTopErr, tau21, prelimFit, 25, HT, isMC, log )
