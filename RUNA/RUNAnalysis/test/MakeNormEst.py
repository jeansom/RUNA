#
import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy
from RUNA.RUNAnalysis.Plotting_Header import *
FILE = TFile.Open( "LIM_FEED/LIM_FEED_SIGMOID_1213.root" )

b0t0_QCD = FILE.Get("b0t0__QCD")
b0t0_QCD_up = FILE.Get("b0t0__QCD__Fit__up")
b0t0_QCD_dn = FILE.Get("b0t0__QCD__Fit_down")
b0t0_DATA = FILE.Get("bot0__DATA")
b0t0_TT = FILE.Get("b0t0__TTBAR")
b0t0_WJ = FILE.Get("b0t0__WJETS")

QCD = []
QCD_up = []
QCD_dn = []
DATA = []
TT = []
WJ = []
Plots = []
QCDTTWJ = []
Bkg = []

n = 0
for bt in [ "b0t0", "b0t1", "b0t2", "b1t0", "b1t1", "b1t2", "b2t0", "b2t1", "b2t2" ]:
    QCD.append( (FILE.Get( bt+"__QCD" ) ))
    QCD_up.append( (FILE.Get( bt+"__QCD__Fit__up" ) ))
    QCD_dn.append( (FILE.Get( bt+"__QCD__Fit__down" ) ))
    DATA.append( (FILE.Get( bt+"__DATA" ) ))
    TT.append( (FILE.Get( bt+"__TTBAR" ) ))
    WJ.append( (FILE.Get( bt+"__WJETS" ) ) )

    Plots.append( QCD[n] )
#    Plots.append( TT[n] )
#    Plots.append( WJ[n] )

    n=n+1


Canvas = TCanvas( "C", "", 800, 800 )
Canvas.cd()
C = TPad( "C", "", 0,0.05,1,1 )
L = TPad( "L", "", 0,0,1.,0.1 )
C.Draw()
L.Draw()

#C.Divide( 3,3,0,0 )

#plot = TPad( "plot", "", 0, 0.1, 1., 1 )
#leg = TPad( "leg", "", 0,0,1.0,0.1 )
#plot.Draw()
#leg.Draw()
#plot.cd()
#plot.SetLogy()
n = 0

for i in  [ kRed, kMagenta, kBlue, kCyan, kGreen, kRed+3, kMagenta+3, kBlue+3, kCyan+3 ]:
    QCD[n].SetLineColor( i )
    QCD[n].SetLineWidth(2)
    QCD[n].SetTitle("")
    QCD[n].Scale( 1/QCD[n].Integral(0,100000) )
#    QCD[n].SetFillColor( )
#    QCD_up[n].SetLineColor(i)
#    QCD_dn[n].SetLineColor(i)
    DATA[n].SetLineColor(kBlack)
    DATA[n].SetMarkerColor(kBlack)
    DATA[n].SetMarkerStyle(20)
    TT[n].SetLineColor( kBlack )
    TT[n].SetFillColor( kRed )
    WJ[n].SetLineColor( kBlack )
    WJ[n].SetFillColor( 8 )

    BkgI = THStack( "All_Bkgs", "" )
    BkgI.Add(WJ[n])
    BkgI.Add(TT[n])
    BkgI.Add(QCD[n])
    QCDTTWJ.append(BkgI)

    BkgII = QCD[n].Clone()
    BkgII.Add( TT[n] )
    BkgII.Add( WJ[n] )
    Bkg.append( BkgII )
#    Plots.append([ QCDTTWJ[n], DATA[n] ])
#    Plots.append( QCDTTWJ[n] )
#    Plots.append( DATA[n] )

    n=n+1
FindAndSetMax( Plots, False )
n = 0
#plot = []
#leg = []
C.cd()
for i in [ "Zero Btags, Zero Top Tags","One Btags, Zero Top Tags","Two Btags, Zero Top Tags", "Zero Btags, One Top Tag","One Btags, One Top Tag","Two Btags, One Top Tag", "Zero Btags, Two Top Tags","One Btags, Two Top Tags","Two Btags, Two Top Tags" ]:
#    print n
#    plot.append( TPad( "plot"+str(n), "", 0,0,1.0, 0.95 ) )
#    leg.append( TPad( "leg"+str(n), "", 0,.9,1,1 ))
#    print gPad.GetX1()
#    print C.GetSelectedPad()
#    print C.GetSelectedPad()
#    print C.GetSelectedPad()

#    plot[n].Draw()
#    leg[n].Draw()
#    plot[n].cd()
#    Bkg[n].SetTitle(i)
#    Bkg[n].Draw( "hist" )
 #   QCDTTWJ[n].Draw("hist")
 #   QCDTTWJ[n].SetTitle(i)
 #   QCDTTWJ[n].GetXaxis().SetTitle( "Pruned Average Mass" )
 #   QCDTTWJ[n].GetYaxis().SetTitle( "N Events" )
 #   QCDTTWJ[n].Draw("hist")
 #   DATA[n].Draw("same E0")
 #   n=n+1
    for j in xrange(len(QCDTTWJ)):
        QCD[j].Draw("same hist")
#        DATA[i].Draw("same E0")
L.cd()
legend = TLegend( 0, 0, 1, 1 )
n=0
for bt in [ "b0t0", "b0t1", "b0t2", "b1t0", "b1t1", "b1t2", "b2t0", "b2t1", "b2t2" ]:
    legend.AddEntry( QCD[n], bt, "l" )
    n=n+1
#legend.AddEntry( DATA[n-1], "Data", "P" )
legend.SetNColumns(3)
legend.Draw()

Canvas.SaveAs( "outputs/AllChanPlot.png" )
