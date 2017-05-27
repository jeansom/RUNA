#
import os
import math
from array import array
import optparse
import argparse
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
import RUNA.RUNAnalysis.scaleFactors
from RUNA.RUNAnalysis.scaleFactors import *
import RUNA.RUNAnalysis.CMS_lumi as CMS_lumi

zerobtag = "(jet1btagCSVv2<0.8484&jet2btagCSVv2<0.8484)"
onebtag = "((jet1btagCSVv2<0.8484&jet2btagCSVv2>0.8484)||(jet1btagCSVv2>0.8484&jet2btagCSVv2<0.8484))"
twobtag = "(jet1btagCSVv2>0.8484&jet2btagCSVv2>0.8484)"

zeroTop = "(jet1Tau32>0.67&jet2Tau32>.67)"
oneTop = "((jet1Tau32<=0.67&jet2Tau32>=0.67)||(jet1Tau32>0.67&jet2Tau32<0.67))"
twoTop = "(jet1Tau32<0.67&jet2Tau32<0.67)"
    # Create the distributions

weight = "(36555.21/15*lumiWeight*puWeight)"
TTScaleStr = "1.06*exp(-0.0005*HT/2)"
WScaleStr = "1"
TopScaleStr = "1"

DATA = DIST( "DATA", "80XRootFilesUpdated/RUNAnalysis_JetHT_Run2016_80X_V2p3_v06_cut15.root", "BoostedAnalysisPlotsPuppi/RUNATree", "1" )

QCD = []
for i in [ "QCDPt170to300", "QCDPt300to470", "QCDPt470to600", "QCDPt600to800", "QCDPt800to1000", "QCDPt1000to1400", "QCDPt1400to1800", "QCDPt1800to2400", "QCDPt2400to3200", "QCDPt3200toInf" ]:
    QCD.append( DIST( i, "80XRootFilesUpdated/RUNAnalysis_"+i+"_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*"+str(scaleFactor(i)) ) )
QCDHT = DIST( "QCDHT", "80XRootFilesUpdated/RUNAnalysis_QCDHTAll_80X_V2p4_v07p1.root", "BoostedAnalysisPlotsPuppi/RUNATree", ".85*puWeight*36555.21/15*lumiWeight")

TTJets = DIST( "TTJets", "80XRootFilesUpdated/RUNAnalysis_TT_PtRewt_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree", "("+weight+"*"+TTScaleStr+")" )
WJets = DIST( "WJets", "80XRootFilesUpdated/RUNAnalysis_WJetsToQQ_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree",  "("+weight+"*"+WScaleStr+")" )
Top = DIST( "Top", "80XRootFilesUpdated/RUNAnalysis_ST_t-channel_topantitop_4f_inclusiveDecays_80X_V2p3_v06.root", "BoostedAnalysisPlotsPuppi/RUNATree",  "("+weight+"*"+TopScaleStr+")" )

def DDTMeasure(CUT,CHAN,NAME,TITLE,log):
    Dists = [QCDHT]
    DistsSub = []
    
    Est = Alphabet( "Est", Dists, DistsSub, [] )
    presel = CUT+"&"+CHAN
    preselNOBT = CUT
    if "t2" in NAME:
        preselNOBT = preselNOBT+"&"+twoTop
    else:
        preselNOBT = presel
    anticuts = presel + "&(prunedMassAsym>0.1&deltaEtaDijet<1.5)"
    cuts = presel + "&(prunedMassAsym<0.1&deltaEtaDijet<1.5)"
    var_array = ["HT", "prunedMassAsym", 260, 900., 3500., 50, 0., 1.]
    Est.SetRegions( var_array, preselNOBT+"&deltaEtaDijet>1.5" )
    Est.TwoDPlot.SetStats(0)

    cut = [0.1, "<"]
    bins = []
    bin = 900
    while bin <=3500:
        bins.append( [bin, bin+10] )
        bin = bin+10
    truthbins = []

    binBoundaries = []
    dBin = 5.
    i = 60
    while i<=350:
        binBoundaries.append(i)
        i=i+dBin

    center = 0.

    F = QuadraticFit([0.,0.,0.],900.,3500.,"linearfit", "SEMR")
    Est.GetRates(cut, bins, truthbins, center, F, binBoundaries)

    mean = Est.G.GetMean(2)
    L = TLine(0, mean, 1, mean)
    
    C1 = TCanvas("C1"+NAME,"",800,600)
    C1.cd()
    Est.TwoDPlot.Draw("COLZ")
    Est.TwoDPlot.GetXaxis().SetTitle("HT")
    Est.TwoDPlot.GetYaxis().SetTitle("Pruned Mass Asymmetry")
    C1.SaveAs("outputs/41317/45/Est_2D_"+NAME+".png")
    C2 = TCanvas("C2"+NAME,"",800,800)
    C2.cd()
    Est.G.SetTitle(TITLE)
    Est.G.Draw("AP")
    Est.G.GetXaxis().SetTitle("HT")
    Est.G.GetXaxis().SetLimits(900.,3500.)
    Est.G.GetYaxis().SetTitle("R_{p/f}")
    Est.G.GetYaxis().SetTitleOffset(1.3)
    Est.G.Draw("AP")
#    Est.truthG.SetLineColor(kBlue)
#    Est.truthG.SetLineWidth(2)
#    Est.truthG.Draw("sameP")
    L.SetLineColor(kGray)
    L.SetLineWidth(2)
    L.Draw("same")
    Est.Fit.fit.Draw("same")
    Est.Fit.ErrUp.SetLineStyle(2)
    Est.Fit.ErrUp.SetLineColor(kRed)
    Est.Fit.ErrUp.Draw("same")
    Est.Fit.ErrDn.SetLineStyle(2)
    Est.Fit.ErrDn.SetLineColor(kRed)
    Est.Fit.ErrDn.Draw("same")

    chi2Test = TLatex( 0.2, 0.85, '#chi^{2}/ndF = '+ str( round( ComputeChi2(Est.G, Est.Fit.fit), 2 ) )+'/'+str( int( Est.Fit.fit.GetNDF() ) ) ) # chi2/ndf
    p0 = TLatex( 0.2, 0.80, 'p0 = '+ '{:0.2e}'.format(Est.Fit.fit.GetParameter( 0 )) +' #pm '+ '{:0.2e}'.format(Est.Fit.fit.GetParError( 0 ))) # p0
    p1 = TLatex( 0.2, 0.75, 'p1 = '+ '{:0.2e}'.format(Est.Fit.fit.GetParameter( 1 )) +' #pm '+ '{:0.2e}'.format(Est.Fit.fit.GetParError( 1 ))) # p1

    chi2Test.SetNDC()
    chi2Test.SetTextFont(42) ### 62 is bold, 42 is normal
    chi2Test.SetTextSize(0.04)
    p0.SetNDC()
    p0.SetTextFont(42) ### 62 is bold, 42 is normal
    p0.SetTextSize(0.04)
    p1.SetNDC()
    p1.SetTextFont(42) ### 62 is bold, 42 is normal
    p1.SetTextSize(0.04)

    chi2Test.Draw("same")
    p0.Draw("same")
    p1.Draw("same")
    C2.SaveAs("outputs/41317/45/Est_Fit_"+NAME+".png")

    fitBins = []
    bin = 900
    while bin < 3500:
        fitBins.append(bin)
        bin = bin+10

    Est.MakeEst( "prunedMassAve", binBoundaries, anticuts, cuts, True, fitBins )
    return Est

parser = argparse.ArgumentParser()
parser.add_argument( '-c', '--channel', action='store', dest='channel', default=1, help='Channel to run the estimation for')
try:
    args = parser.parse_args()
    print "here"
except:
    parser.print_help()
    sys.exit(0)

channel = args.channel

ccuts = ""

if "b0t0" in channel:
    ccuts = zerobtag+"&"+zeroTop
elif "b1t0" in channel:
    ccuts = onebtag+"&"+zeroTop
elif "b2t0" in channel:
    ccuts = twobtag+"&"+zeroTop
elif "b0t1" in channel:
    ccuts = zerobtag+"&"+oneTop
elif "b1t1" in channel:
    ccuts = onebtag+"&"+oneTop
elif "b2t1" in channel:
    ccuts = twobtag+"&"+oneTop
elif "b0t2" in channel:
    ccuts = zerobtag+"&"+twoTop
elif "b1t2" in channel:
    ccuts = onebtag+"&"+twoTop
elif "b2t2" in channel:
    ccuts = twobtag+"&"+twoTop
else:
    ccuts = "jet1Tau21>0."

binsMass = [ ]
i = 50
while i < 200:
    binsMass.append([i,i+5])
    i=i+5
i = 200
while i < 350:
    binsMass.append([i,i+25])
    i=i+25
CUT = "(jet1Tau21<0.45&jet2Tau21<0.45&numJets==2)"
Ests = []
log = False
for i in xrange(len(binsMass)):
    Ests.append(DDTMeasure(CUT+"&prunedMassAve>"+str(binsMass[i][0])+"&prunedMassAve<"+str(binsMass[i][1]), ccuts, "MassCut_"+str(i)+"_"+channel, str(binsMass[i])+"_"+channel, log))
print len(Ests)
V = Ests[0].hists_MSR[0].Clone("data_obs")
V.Reset()
for Est in Ests:
    for i in Est.hists_MSR:
        i.Sumw2()
        i.SetStats(0)
        V.Add(i)
print "V: " + str(V.Integral())
N = V.Clone("EST")
N1 = V.Clone("EST1")
N.Reset()
N1.Reset()
NStack = THStack("EST","")
for Est in Ests:
    for i in Est.hists_EST:
        N.Add(i)
        N1.Add(i)
    for i in Est.hists_EST_SUB:
        N.Add(i, -1)
        N1.Add(i, -1)
print "N: " + str(N.Integral())
removeNegativeBins(N)
removeNegativeBins(N1)
SUB = []
for i in xrange(len(Ests[0].hists_MSR_SUB)):
    S = N.Clone("Sub_"+str(i))
    S.Reset()
    SUB.append(S)
    S.SetLineColor(kBlack)
for Est in Ests:
    if len(Est.hists_MSR_SUB)==3:
        Est.hists_MSR_SUB[0].SetFillColor(6)
        Est.hists_MSR_SUB[1].SetFillColor(8)
        Est.hists_MSR_SUB[2].SetFillColor(2)        
        SUB[0].SetFillColor(6)
        SUB[1].SetFillColor(8)
        SUB[2].SetFillColor(2)
    j = 0
    for i in Est.hists_MSR_SUB:
        N.Add(i)
        SUB[j].Add(i)
        i.SetLineColor(kBlack)
for i in SUB:
    NStack.Add(i)
NStack.Add(N1)

NU = V.Clone("EST")
NU.Reset()
for Est in Ests:
    for i in Est.hists_EST_UP:
        NU.Add(i)
    for i in Est.hists_EST_SUB_UP:
        NU.Add(i, -1)
removeNegativeBins(NU)
for Est in Ests:
    for i in Est.hists_MSR_SUB:
        NU.Add(i)

ND = V.Clone("EST")
ND.Reset()
for Est in Ests:
    for i in Est.hists_EST_DN:
        ND.Add(i)
    for i in Est.hists_EST_SUB_DN:
        ND.Add(i, -1)
removeNegativeBins(ND)
for Est in Ests:
    for i in Est.hists_MSR_SUB:
        ND.Add(i)

A = N.Clone("EST_Antitag")
A.Reset()
for Est in Ests:
    for i in Est.hists_ATAG: # Adds all the C Plots together
        A.Add( i, 1. )

# Pretty up plots for saving
NU.SetLineColor( kBlack )
ND.SetLineColor( kBlack )
NU.SetLineStyle(2)
ND.SetLineStyle(2)
N1.SetLineColor( kBlack )
N1.SetFillColor( kAzure-4 )
N.SetLineColor( kBlack )
N.SetFillColor( kAzure-4 )

V.SetStats(0)
V.SetLineColor(kBlack)
V.SetMarkerColor(1)
V.SetMarkerStyle(20)

N1.GetYaxis().SetTitle("events")
N1.GetXaxis().SetTitle( "Average Mass" )

FindAndSetMax( [ N, NU, ND, V ], False ) # Set maximum and minimum of all the plots
Pull = V.Clone( "Pull_quad" ) # Ratio (actual - est)/sqrt(sigma_actual^2 + sigma_sys^2) plot
Pull.Add( N, -1 ) # Pull now is actual - est, still need to divide

Pull2 = V.Clone( "Pull2" ) # Ratio (actual - est)/sqrt(sigma_actual^2 + sigma_sys^2) plot
Pull2.Divide( N ) # Pull now is actual - est, still need to divide

Pull_norm = V.Clone( "Pull_norm" ) # Ratio (actual - est)/sigma_actual plot
Pull_norm.Add( N, -1 ) # Pull now is actual - est, still need to divide

Boxes = [] # Errors on estimation
sBoxes = [] # Systematic errors on estimation
pBoxes = [] # Errors on pull
maxy = 0.

for i in range(1, N.GetNbinsX()+1): # Loop through all bins in N (nominal estimation)
    P = Pull.GetBinContent(i)
    Ve = V.GetBinError(i)
    Pull.SetBinError(i, 1.) # Sets pull bin error 1
    Pull_norm.SetBinError(i, 1.) # Sets pull bin error 1
    if A.GetBinContent(i)==0: # If antitag region bin content is 0
        a = 0 # a, some some part of the error on the bkg est? = 0
    else:
        a = A.GetBinError(i)*N.GetBinContent(i)/A.GetBinContent(i) # otherwise, this expression
    u = NU.GetBinContent(i) - N.GetBinContent(i) # u, upper error on estimation
    d = N.GetBinContent(i) - ND.GetBinContent(i) # d, lower error on estimation
    x1 = Pull.GetBinCenter(i) - (0.5*Pull.GetBinWidth(i)) # Start of bin
    y1 = N.GetBinContent(i) - math.sqrt((d*d) + (a*a)) # Bottom of error on estimation
    s1 = N.GetBinContent(i) - a # Bottom of systematic error on estimation?
    if y1 < 0.: # Don't want the lower error to be negative, set to 0
        y1 = 0
    if s1 < 0: # Don't want the lower error to be negative, set to 0
        s1 = 0
    x2 = Pull.GetBinCenter(i) + (0.5*Pull.GetBinWidth(i)) # End of bin
    y2 = N.GetBinContent(i) + math.sqrt((u*u) + (a*a)) # Top of error on estimation
    s2 = N.GetBinContent(i) + a # Top of systematic error on estimation?
    if maxy < y2: # Don't want the upper error to be above the max, set to max
        maxy = y2
    if Ve > 1.: # If error on V (signal region plots) is > 1
        yP1 = -math.sqrt((d*d) + (a*a))/Ve # Bottom of pull error
        yP2 = math.sqrt((u*u) + (a*a))/Ve # Top of pull error
    else:
        yP1 = -math.sqrt((d*d) + (a*a)) # Bottom of pull error
        yP2 = math.sqrt((u*u) + (a*a)) # Top of pull error
    if Ve*Ve + yP1*yP1 > 1: # For quad pull
        Pull.SetBinContent( i, P / math.sqrt( Ve*Ve + yP1*yP1 ) ) # Filling quad pull
    if Ve > 1:
        Pull_norm.SetBinContent( i, P/Ve ) # Filling normal pull

    # TBoxes with the errors on the various plots
    tempbox = TBox(x1,y1,x2,y2)
    temppbox = TBox(x1,yP1,x2,yP2)
    tempsbox = TBox(x1,s1,x2,s2)
    Boxes.append(tempbox)
    sBoxes.append(tempsbox)
    pBoxes.append(temppbox)

# Pretty up pull plot
Pull2.GetXaxis().SetTitle("Average Mass [GeV]")
Pull2.SetStats(0)
Pull2.SetLineColor(1)
Pull2.SetFillColor(0)
Pull2.SetMarkerColor(1)
Pull2.SetMarkerStyle(20)
Pull2.GetYaxis().SetNdivisions(4)
Pull2.GetYaxis().SetTitle("#frac{Data}{Est}")
Pull2.GetYaxis().SetLabelSize(55/15*Pull_norm.GetYaxis().GetLabelSize())
Pull2.GetYaxis().SetTitleSize(4.5*Pull_norm.GetYaxis().GetTitleSize())
Pull2.GetYaxis().SetTitleOffset(0.25)
Pull2.GetYaxis().SetRangeUser(0,2.)
Pull2.GetXaxis().SetLabelSize(.12)
Pull2.GetXaxis().SetTitleSize(.14)

Pull_norm.GetXaxis().SetTitle("Average Mass [GeV]")
Pull_norm.SetStats(0)
Pull_norm.SetLineColor(1)
Pull_norm.SetFillColor(0)
Pull_norm.SetMarkerColor(1)
Pull_norm.SetMarkerStyle(20)
Pull_norm.GetYaxis().SetNdivisions(4)
Pull_norm.GetYaxis().SetTitle("#frac{Data - Est}{#sigma_{Data}}")
Pull_norm.GetYaxis().SetLabelSize(50/15*Pull_norm.GetYaxis().GetLabelSize())
Pull_norm.GetYaxis().SetTitleSize(3.8*Pull_norm.GetYaxis().GetTitleSize())
Pull_norm.GetYaxis().SetTitleOffset(0.25)
Pull_norm.GetYaxis().SetRangeUser(-5,5.)
Pull_norm.GetXaxis().SetLabelSize(.12)
Pull_norm.GetXaxis().SetTitleSize(.14)

# Pretty up errors
for i in Boxes:
    i.SetFillColor(12)
    i.SetFillStyle(3244)
for i in pBoxes:
    i.SetFillColor(9)
    i.SetFillStyle(3144)
for i in sBoxes:
    i.SetFillColor(12)
    i.SetFillStyle(3002)

leg = TLegend(.35,.70,.89,.89)
leg.SetNColumns(2)
leg.SetLineColor(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)

# Make the legend for the estimation plot
leg.AddEntry(V, "QCD MC", "PL")
leg.AddEntry( N1, "QCD Est from MC", "F")
if len(Est.hists_MSR_SUB)>2:
    leg.AddEntry( Est.hists_MSR_SUB[2], "t #bar{t} + Jets", "F")
    leg.AddEntry( Est.hists_MSR_SUB[1], "W + Jets", "F")
    leg.AddEntry( Est.hists_MSR_SUB[0], "Single Top", "F")
leg.AddEntry( Boxes[0], "total uncertainty", "F")
leg.AddEntry( sBoxes[0], "bkg statistical component", "F")

# A line at -2, -1, 0, 1, 2 for pull plot
minx = 60
maxx = 350
T0 = TLine(minx,0.,maxx,0.)
T0.SetLineColor(kRed)
T0.SetLineWidth(2)
T2 = TLine(minx,2.,maxx,2.)
T2.SetLineColor(kRed)
T2.SetLineStyle(2)
T2.SetLineWidth(2)
Tm2 = TLine(minx,-2.,maxx,-2.)
Tm2.SetLineColor(kRed)
Tm2.SetLineStyle(2)
Tm2.SetLineWidth(2)
T1 = TLine(minx,1.,maxx,1.)
T1.SetLineColor(kRed)
T1.SetLineStyle(3)
T1.SetLineWidth(2)
Tm1 = TLine(minx,-1.,maxx,-1.)
Tm1.SetLineColor(kRed)
Tm1.SetLineStyle(3)
Tm1.SetLineWidth(2)
C4 = TCanvas("C4", "", 800, 800)

# Draw all plots and save
plot = TPad("pad1", "The pad 80% of the height",0,0.20,1,1)
pull = TPad("pad2", "The pad 20% of the height",0,0.,1.0,0.20)
plot.Draw()
plot.SetBottomMargin(0)
plot.Draw()
pull.Draw()
plot.cd()

NStack.Draw("Hist")

if log: 
    print "here2"
    NStack.GetYaxis().SetRangeUser( 0.001, 5000 )
else: 
    NStack.GetYaxis().SetRangeUser( 0, 5000 )
    print "here"
NStack.GetXaxis().SetTitle("")
NStack.GetYaxis().SetTitle("Events / 10 GeV")
NStack.GetYaxis().SetTitleSize(NStack.GetYaxis().GetTitleSize()*1.3)
if log: NStack.SetMaximum( NStack.GetMaximum()*10 )
else: NStack.SetMaximum( NStack.GetMaximum()*2 )
NStack.GetXaxis().SetLabelSize(0)
NStack.GetYaxis().SetLabelSize(NStack.GetYaxis().GetLabelSize()*3/4)
NStack.Draw("Hist") # Draw estimate
V.SetLineWidth(2)
V.Draw("same E0") # Draw actual signal region

for i in Est.hists_SIG:
    i.Draw("histsame")
if log: plot.SetLogy()

# Draw errors
for i in Boxes:
    i.Draw("same")
for i in sBoxes:
    i.Draw("same")

CMS_lumi.extraText = "Simulation Preliminary"
CMS_lumi.relPosX = 0.13
CMS_lumi.CMS_lumi(plot, 4, 0)

leg.Draw()
plot.RedrawAxis()

# Draw and save pull plot
pull.cd()
pull.SetTopMargin(0)
pull.SetBottomMargin(0.3)
pull.Draw()
if not log: 
    Pull_norm.Draw()
        # Draw errors on pull
    for i in pBoxes:
        i.Draw("same")
    # Draw lines on pull plot
    T0.Draw("same")
    T2.Draw("same")
    Tm2.Draw("same")
    T1.Draw("same")
    Tm1.Draw("same")
        
    Pull_norm.Draw("same")
        
else: 
    Pull2.Draw()
    T1.Draw("same")    

C4.SaveAs("outputs/41317/45/Est_Plot_"+channel+".png")
