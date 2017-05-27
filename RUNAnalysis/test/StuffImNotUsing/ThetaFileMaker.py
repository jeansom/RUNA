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

def ThetaFileMaker( chan, chanCuts, bins, minBin, maxBin, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, isMC=True ):
    gStyle.SetOptStat(0)
    # Setting basic distributions
    weight = "36600*puWeight*lumiWeight"

    TTScaleStr = "((1+.2*"+str(scaleTT)+")*1.06*exp((-0.0005*HT/2)*(1+.2*"+str(scaleAlpha)+")))"
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

    DATA = DIST( "DATA", "80XRootFiles/RUNBoostedAnalysis_JetHT_Run2015D-16Dec2015-v1_v76x_v2p0_v05.root", "BoostedAnalysisPlots/RUNATree", "1" )
    QCD = DIST( "QCD", "80XRootFiles/RUNBoostedAnalysis_QCD_PtAllv01.root", "BoostedAnalysisPlots/RUNATree", weight )
    SIG = DIST( "SIG", "80XRootFiles/RUNBoostedAnalysis_RPVStopStopToJets_UDD323_M-100v01.root", "BoostedAnalysisPlots/RUNATree", weight )
    TTJets = DIST( "TTJets", "80XRootFiles/RUNBoostedAnalysis_TTv01.root", "BoostedAnalysisPlots/RUNATree", weight+"*((1.06 + .5*"+str(scaleTT)+" )*exp(-0.0005*HT/2))" )
    TTJetsUp = DIST( "TTJetsUp", "80XRootFiles/RUNBoostedAnalysis_TTv01.root", "BoostedAnalysisPlots/RUNATree", weight+"*((1.06 + 0.5*"+str(scaleTT)+" + 0.5*scale"+str(scaleTTErr)+")*exp(-0.0005*HT/2))" )
    TTJetsDn = DIST( "TTJetsDn", "80XRootFiles/RUNBoostedAnalysis_TTv01.root", "BoostedAnalysisPlots/RUNATree", weight+"*((1.06 + 0.5*"+str(scaleTT)+" - 0.5*scale"+str(scaleTTErr)+")*exp(-0.0005*HT/2))" )
#    TTJets = DIST( "TTJets", "80XRootFiles/RUNBoostedAnalysis_TTv01.root", "BoostedAnalysisPlots/RUNATree", weight+"*((1))" )
#    TTJetsUp = DIST( "TTJetsUp", "80XRootFiles/RUNBoostedAnalysis_TTv01.root", "BoostedAnalysisPlots/RUNATree", weight+"*((1 + .5))" )
#    TTJetsDn = DIST( "TTJetsDn", "80XRootFiles/RUNBoostedAnalysis_TTv01.root", "BoostedAnalysisPlots/RUNATree", weight+"*((1 - 0.5))" )
    WJets = DIST( "WJets", "80XRootFiles/RUNBoostedAnalysis_WJetsToQQ_HT-600ToInfv01.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*(1 + .5*"+str(scaleW)+"))" )
    WJetsUp = DIST( "WJetsUp", "80XRootFiles/RUNBoostedAnalysis_WJetsToQQ_HT-600ToInfv01.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*(1 + 0.5*"+str(scaleW)+" + 0.5*"+str(scaleWErr)+"))" )
    WJetsDn = DIST( "WJetsDn", "80XRootFiles/RUNBoostedAnalysis_WJetsToQQ_HT-600ToInfv01.root", "BoostedAnalysisPlots/RUNATree", "("+weight+"*(1 + 0.5*"+str(scaleW)+" - 0.5*"+str(scaleWErr)+"))" )
    WW = DIST( "WW", "80XRootFiles/RUNBoostedAnalysis_WWTo4Q_13TeV-powhegv01.root", "BoostedAnalysisPlots/RUNATree", weight )
    ZZ = DIST( "ZZ", "80XRootFiles/RUNBoostedAnalysis_ZZTo4Q_13TeV_amcatnloFXFX_madspin_pythia8v01.root", "BoostedAnalysisPlots/RUNATree", weight )
    ZJets = DIST( "ZJets", "80XRootFiles/RUNBoostedAnalysis_ZJetsToQQ_HT600toInf_13TeV-madgraphv01.root", "BoostedAnalysisPlots/RUNATree", weight )
    Sig = DIST( "Sig", "80XRootFiles/RUNBoostedAnalysis_RPVStopStopToJets_UDD323_M-100v01.root", "BoostedAnalysisPlots/RUNATree", weight )

    # Creating Alphabet objects to run estimate on    
    if isMC: 
        print "here i am"
        Dists = [ QCD, TTJets, WJets, WW, ZZ, ZJets ]
    else: 
        print "here2"
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
#    if chan is "b0t2": chanCutsTemp = zerobtag+"&"+oneTop
#    elif chan is "b1t2": chanCutsTemp = onebtag+"&"+oneTop
#    elif chan is "b2t1": chanCutsTemp = twobtag+"&"+zeroTop
#    elif chan is "b2t2": chanCutsTemp = twobtag+"&"+zeroTop
#    chanCutsTemp = chanCuts
    if "t0" in chan: chanCutsTemp = zeroTop
    elif "t1" in chan: chanCutsTemp = oneTop
    elif "t2" in chan: chanCutsTemp = twoTop
    #chanCutsTemp = "jet1btagCSVv2>-999999999999999999999"

    MakeFitPlots( EstMass, FMass, binsMass, "prunedMassAve", Xcut[0], var_arrayMass, presel+"&"+chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "", "outputs/"+directory+method+"/Mass"+chan, False )
    MakeEstPlots( EstMass, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/Mass"+chan, False )

    MakeFitPlots( EstMassWJUp, FMassWJUp, binsMass, "prunedMassAve", Xcut[0], var_arrayMass, presel+"&"+chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "",  "outputs/"+directory+method+"/MassWJUp"+chan, False )
    MakeEstPlots( EstMassWJUp, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/MassWJUp"+chan, False )

    MakeFitPlots( EstMassWJDn, FMassWJDn, binsMass, "prunedMassAve", Xcut[0], var_arrayMass, presel+"&"+chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "", "outputs/"+directory+method+"/MassWJDn"+chan, False )
    MakeEstPlots( EstMassWJDn, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/MassWJDn"+chan, False )

    MakeFitPlots( EstMassTTUp, FMassTTUp, binsMass, "prunedMassAve", Xcut[0], var_arrayMass, presel+"&"+chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "", "outputs/"+directory+method+"/MassTTUp"+chan, False )
    MakeEstPlots( EstMassTTUp, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/MassTTUp"+chan, False )

    MakeFitPlots( EstMassTTDn, FMassTTDn, binsMass, "prunedMassAve", Xcut[0], var_arrayMass, presel+"&"+chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "", "outputs/"+directory+method+"/MassTTDn"+chan, False )
    MakeEstPlots( EstMassTTDn, "prunedMassAve", "Average Mass", binBoundaries, presel+"&"+chanCuts+"&"+anticuts, presel+"&"+chanCuts+"&"+cuts, "prunedMassAve", "", "outputs/"+directory+method+"/MassTTDn"+chan, False )

    # Makes root file with basic fits
    FITFILE = TFile( "outputs/"+directory+method+"/LIM_FIT"+chan+".root", "RECREATE" )
    FITFILE.cd()
    
    FIT_Points = (EstMass.G).Clone("G_"+chan)
    FIT = (EstMass.Fit.fit).Clone("Fit_"+chan)
    FIT_Up = (EstMass.Fit.ErrUp).Clone("FitUp_"+chan)
    FIT_Dn = (EstMass.Fit.ErrDn).Clone("FitDn_"+chan)

    FIT_Points.Write()
    FIT.Write()
    FIT_Up.Write()
    FIT_Dn.Write()

    FITFILE.Write()
    FITFILE.Save()

    # Makes histograms
    chan__DATA = TH1D( chan+"__DATA", chan+"__DATA", bins, minBin, maxBin )
    chan__QCD = TH1D( chan+"__QCD", chan+"__QCD", bins, minBin, maxBin )
    chan__TTBAR = TH1D( chan+"__TTBAR", chan+"__TTBar", bins, minBin, maxBin )
    chan__QCD__Fit__up = TH1D( chan+"__QCD__Fit"+chan+"__up", chan+"__QCD__Fit"+chan+"__up", bins, minBin, maxBin )
    chan__QCD__Fit__down = TH1D( chan+"__QCD__Fit"+chan+"__down", chan+"__QCD__Fit"+chan+"`__down", bins, minBin, maxBin )
    chan__TTBAR__TTScale__up = TH1D( chan+"__TTBAR__TTScale__up", chan+"__TTBAR__TTScale__up", bins, minBin, maxBin )
    chan__TTBAR__TTScale__down = TH1D( chan+"__TTBAR__TTScale__down", chan+"__TTBAR__TTScale__down", bins, minBin, maxBin )
    chan__QCD__TTScale__up = TH1D( chan+"__QCD__TTScale__up", chan+"__QCD__TTScale__up", bins, minBin, maxBin )
    chan__QCD__TTScale__down = TH1D( chan+"__QCD__TTScale__down", chan+"__QCD__TTScale__down", bins, minBin, maxBin )
    if not("b2" in chan or "t2" in chan) or True:
        chan__WJETS = TH1D( chan+"__WJETS", chan+"__WJETS", bins, minBin, maxBin )
        chan__WJETS__WJScale__up = TH1D( chan+"__WJETS__WJScale__up", chan+"__WJETS__WJScale__up", bins, minBin, maxBin )
        chan__WJETS__WJScale__down = TH1D( chan+"__WJETS__WJScale__down", chan+"__WJETS__WJScale__down", bins, minBin, maxBin )
    chan__QCD__WJScale__up = TH1D( chan+"__QCD__WJScale__up", chan+"__QCD__WJScale__up", bins, minBin, maxBin )
    chan__QCD__WJScale__down = TH1D( chan+"__QCD__WJScale__down", chan+"__QCD__WJScale__down", bins, minBin, maxBin )

    chan__WJETS__A = TH1D( chan+"__WJETS__A", chan+"__WJETS__A", bins, minBin, maxBin )
    chan__WJETS__WJScale__up__A = TH1D( chan+"__WJETS__WJScale__up__A", chan+"__WJETS__WJScale__up__A", bins, minBin, maxBin )
    chan__WJETS__WJScale__down__A = TH1D( chan+"__QCD__TTScale__down__A", chan+"__QCD__TTScale__down__A", bins, minBin, maxBin )

    for i in EstMass.hists_EST:
        chan__QCD.Add( i, 1. )
    for i in EstMass.hists_EST_UP:
        chan__QCD__Fit__up.Add( i, 1. )
    for i in EstMass.hists_EST_DN:
        chan__QCD__Fit__down.Add( i, 1. )

    for i in EstMassWJUp.hists_EST:
        chan__QCD__WJScale__up.Add( i, 1. )

    for i in EstMassWJDn.hists_EST:
        chan__QCD__WJScale__down.Add( i, 1. )

    for i in EstMassTTUp.hists_EST:
        chan__QCD__TTScale__up.Add( i, 1. )

    for i in EstMassTTDn.hists_EST:
        chan__QCD__TTScale__down.Add( i, 1. )

    #quickplot( DATA.File, DATA.Tree, chan__DATA, "prunedMassAve", presel+"&"+cuts+"&"+chanCuts, DATA.weight )
    for i in EstMass.hists_MSR:
        chan__DATA.Add(i)
    if isMC:
        for i in EstMass.hists_MSR_SUB:
            chan__DATA.Add(i)

    quickplot( TTJets.File, TTJets.Tree, chan__TTBAR, "prunedMassAve", presel+"&"+cuts+"&"+chanCuts, TTJets.weight )
    quickplot( TTJetsUp.File, TTJetsUp.Tree, chan__TTBAR__TTScale__up, "prunedMassAve", presel+"&"+cuts+"&"+chanCuts, TTJetsUp.weight )
    quickplot( TTJetsDn.File, TTJetsDn.Tree, chan__TTBAR__TTScale__down, "prunedMassAve", presel+"&"+cuts+"&"+chanCuts, TTJetsDn.weight )

    quickplot( WJets.File, WJets.Tree, chan__WJETS__A, "prunedMassAve", presel+"&"+cuts+"&"+chanCuts, WJets.weight )
    quickplot( WJetsUp.File, WJetsUp.Tree, chan__WJETS__WJScale__up__A, "prunedMassAve", presel+"&"+cuts+"&"+chanCuts, WJetsUp.weight )
    quickplot( WJetsDn.File, WJetsDn.Tree, chan__WJETS__WJScale__down__A, "prunedMassAve", presel+"&"+cuts+"&"+chanCuts, WJetsDn.weight )
    
    quickplot( WJets.File, WJets.Tree, chan__WJETS, "prunedMassAve", presel+"&"+Xcut[0]+"<"+Xcut[1]+"&"+chanCuts, WJets.weight )
    quickplot( WJetsUp.File, WJetsUp.Tree, chan__WJETS__WJScale__up, "prunedMassAve", presel+"&"+Xcut[0]+"<"+Xcut[1]+"&"+chanCuts, WJetsUp.weight )
    quickplot( WJetsDn.File, WJetsDn.Tree, chan__WJETS__WJScale__down, "prunedMassAve", presel+"&"+Xcut[0]+"<"+Xcut[1]+"&"+chanCuts, WJetsDn.weight )
    
    if( chan__WJETS.Integral() > 0 and chan__WJETS__A.Integral() > 0  ): chan__WJETS.Scale( chan__WJETS__A.Integral()/chan__WJETS.Integral() )
    elif( chan__WJETS__A.Integral() == 0 ): chan__WJETS.Scale(0)
    if( chan__WJETS__WJScale__up.Integral() > 0 and chan__WJETS__WJScale__up__A.Integral() > 0  ): chan__WJETS__WJScale__up.Scale( chan__WJETS__WJScale__up__A.Integral()/chan__WJETS__WJScale__up.Integral() )
    elif( chan__WJETS__WJScale__up__A.Integral() == 0 ): chan__WJETS__WJScale__up.Scale(0)
    if( chan__WJETS__WJScale__down.Integral() > 0 and chan__WJETS__WJScale__down__A.Integral() > 0  ): chan__WJETS__WJScale__down.Scale( chan__WJETS__WJScale__down__A.Integral()/chan__WJETS__WJScale__down.Integral() )
    elif( chan__WJETS__WJScale__down__A.Integral() == 0 ): chan__WJETS__WJScale__down.Scale(0)

    #### Opens file for writing
    FILE = TFile( "outputs/"+directory+method+"/LIM_FEED"+chan+".root", "RECREATE" )
    FILE.cd()
    #### Write plots to file    
    chan__DATA.Write()
    chan__QCD.Write()
    chan__TTBAR.Write()
    chan__QCD__Fit__up.Write()
    chan__QCD__Fit__down.Write()
    chan__TTBAR__TTScale__up.Write()
    chan__TTBAR__TTScale__down.Write()
    chan__QCD__TTScale__up.Write()
    chan__QCD__TTScale__down.Write()
    chan__WJETS.Write()
    chan__WJETS__WJScale__up.Write()
    chan__WJETS__WJScale__down.Write()
    ### Writes file
    FILE.Write()
    FILE.Save()
    
    C = TCanvas( "C", "", 800, 800 )

    chan__DATA.Draw("hist")
    C.SaveAs("outputs/"+directory+method+"/"+chan+"__DATA.png")
    chan__QCD.Draw("hist")
    C.SaveAs("outputs/"+directory+method+"/"+chan+"__QCD.png")
    chan__TTBAR.Draw("hist")
    C.SaveAs("outputs/"+directory+method+"/"+chan+"__TTBAR.png")
    chan__WJETS.Draw("hist")
    C.SaveAs("outputs/"+directory+method+"/"+chan+"__WJets.png")
    chan__QCD__Fit__up.Draw("hist")
    C.SaveAs("outputs/"+directory+method+"/"+chan+"__QCD__Fit__up.png")
    chan__QCD__Fit__down.Draw("hist")
    C.SaveAs("outputs/"+directory+method+"/"+chan+"__QCD__Fit__down.png")
    chan__TTBAR__TTScale__up.Draw("hist")
    C.SaveAs("outputs/"+directory+method+"/"+chan+"__TTBAR__TTScale__up.png")
    chan__TTBAR__TTScale__down.Draw("hist")
    C.SaveAs("outputs/"+directory+method+"/"+chan+"__TTBAR__TTScale__down.png")
    chan__QCD__TTScale__up.Draw("hist")
    C.SaveAs("outputs/"+directory+method+"/"+chan+"__QCD__TTScale__up.png")
    chan__QCD__TTScale__down.Draw("hist")
    C.SaveAs("outputs/"+directory+method+"/"+chan+"__QCD__TTScale__down.png")
    chan__WJETS__WJScale__up.Draw("hist")
    C.SaveAs("outputs/"+directory+method+"/"+chan+"__WJETS__WJScale__up.png")
    chan__WJETS__WJScale__down.Draw("hist")
    C.SaveAs("outputs/"+directory+method+"/"+chan+"__WJETS__WJScale__down.png")
    chan__QCD__WJScale__up.Draw("hist")
    C.SaveAs("outputs/"+directory+method+"/"+chan+"__QCD__WJScale__up.png")
    chan__QCD__WJScale__down.Draw("hist")
    C.SaveAs("outputs/"+directory+method+"/"+chan+"__QCD__WJScale__down.png")





parser = argparse.ArgumentParser()
parser.add_argument( '-c', '--channel', action='store', dest='channel', default=1, help='Channel')
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

if "/" in directory:
    os.mkdir("outputs/"+directory)
    os.mkdir("outputs/"+directory+method)
else:
    os.mkdir("outputs/"+directory+method)

if "CSVv2" in method:
    zerobtag = "(jet1btagCSVv2<0.8484&jet2btagCSVv2<0.8484)"
    onebtag = "((jet1btagCSVv2<0.8484&jet2btagCSVv2>0.8484)||(jet1btagCSVv2>0.8484&jet2btagCSVv2<0.8484))"
    twobtag = "(jet1btagCSVv2>0.8484&jet2btagCSVv2>0.8484)"
    jet1btag = "((jet1btagCSVv2>0.8484&jet2btagCSVv2<0.8484))"
    jet2btag = "((jet1btagCSVv2<0.8484&jet2btagCSVv2>0.8484))"
elif "CMVAv2" in method:
    zerobtag = "(jet1btagCMVAv2<0.4432&jet2btagCMVAv2<0.4432)"
    onebtag = "((jet1btagCMVAv2<0.4432&jet2btagCMVAv2>0.4432)||(jet1btagCMVAv2>0.4432&jet2btagCMVAv2<0.4432))"
    twobtag = "(jet1btagCMVAv2>0.4432&jet2btagCMVAv2>0.4432)"
    jet1btag = "((jet1btagCMVAv2>0.4432&jet2btagCMVAv2<0.4432))"
    jet2btag = "((jet1btagCMVAv2<0.4432&jet2btagCMVAv2>0.4432))"
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

if int(channel) == 0:
    ThetaFileMaker( "b0t0", zerobtag+"&"+zeroTop, 29, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, isMC )
if int(channel) == 1:
    ThetaFileMaker( "b1t0", onebtag+"&"+zeroTop, 29, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, isMC )
if int(channel) == 2:
    ThetaFileMaker( "b2t0", twobtag+"&"+zeroTop, 29, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, isMC )
if int(channel) == 3:
    ThetaFileMaker( "b0t1", zerobtag+"&"+oneTop, 29, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, isMC )
if int(channel) == 4:
    ThetaFileMaker( "b1t1", onebtag+"&"+oneTop, 29, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, isMC )
#    ThetaFileMaker( "b1t1", "( ("+jet1Top+"&"+jet2btag+")||("+jet2Top+"&"+jet1btag+") )", 29, 60, 350, Xcut, Ycut, isMC )
if int(channel) == 5:
    ThetaFileMaker( "b2t1", twobtag+"&"+oneTop, 29, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, isMC )
if int(channel) == 6:
    ThetaFileMaker( "b0t2", zerobtag+"&"+twoTop, 29, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, isMC )
if int(channel) == 7:
    ThetaFileMaker( "b1t2", onebtag+"&"+twoTop, 29, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, isMC )
if int(channel) == 8:
    ThetaFileMaker( "b2t2", twobtag+"&"+twoTop, 29, 60, 350, Xcut, Ycut, scaleTT, scaleTTErr, scaleW, scaleWErr, isMC )
