#!/usr/bin/env python
'''
File: DrawHistogram.py
Author: Alejandro Gomez Espinosa
Email: gomez@physics.rutgers.edu
Description: My Draw histograms. Check for options at the end.
'''

#from ROOT import TFile, TH1F, THStack, TCanvas, TMath, gROOT, gPad
from ROOT import *
import time, os, math, sys
from array import array
import argparse
from collections import OrderedDict
try:
	from RUNA.RUNAnalysis.histoLabels import labels, labelAxis, finalLabels, setSelection
	from RUNA.RUNAnalysis.scaleFactors import * #scaleFactor as SF
	from RUNA.RUNAnalysis.cuts import selection 
	import RUNA.RUNAnalysis.CMS_lumi as CMS_lumi 
	import RUNA.RUNAnalysis.tdrstyle as tdrstyle
except ImportError:
	sys.path.append('../python')
	from histoLabels import labels, labelAxis, finalLabels
	from scaleFactors import * #scaleFactor as SF
	from cuts import selection 
	import CMS_lumi as CMS_lumi 
	import tdrstyle as tdrstyle




gROOT.Reset()
gROOT.SetBatch()
gROOT.ForceStyle()
tdrstyle.setTDRStyle()
gStyle.SetOptStat(0)

xline = array('d', [0,2000])
yline = array('d', [1,1])
line = TGraph(2, xline, yline)
line.SetLineColor(kRed)

jetMassHTlabY = 0.20
jetMassHTlabX = 0.85

boostedMassAveBins = array( 'd', [0, 4, 8, 12, 16, 20, 24, 29, 33, 38, 43, 48, 53, 58, 64, 69, 75, 81, 87, 94, 100, 107, 114, 122, 129, 137, 145, 154, 162, 171, 181, 190, 200, 211, 221, 233, 244, 256, 269, 282, 295, 310, 324, 340, 356, 372, 390, 408, 427, 447, 468, 489, 512, 536, 561, 587, 615 ] )
boostedMassAveBinSize = array( 'd', [ 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 10, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 17, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 29, 31, 32] )

def plotSystematics( inFileSample, Groom, name, xmin, xmax, rebinX, labX, labY, log):
	"""docstring for plot"""

	if 'low' in args.RANGE : massList = [ 90, 100, 110, 120, 130, 140, 150 ]
	else: massList = [ 170, 180, 190, 210, 220, 230, 240 ] 
	nomArray = []
	upArray = []
	downArray = []
	upOverNomArray = []
	downOverNomArray = []

	for xmass in massList:

		NominalFile = TFile.Open( inFileSample.replace( '100', str(xmass) ) )
		UpFile = TFile.Open( inFileSample.replace( '100', str(xmass)+args.unc+'Up'  ) )
		DownFile = TFile.Open( inFileSample.replace( '100', str(xmass)+args.unc+'Down'  ) )

		outputFileName = name+'_'+args.decay+'RPVSt'+str(xmass)+'_'+args.unc+args.version+'.'+args.ext 
		print 'Processing.......', outputFileName

		histos = {}
		histos[ 'Nominal' ] = NominalFile.Get( name+'_RPVStopStopToJets_'+args.decay+'_M-'+str(xmass) )
		histos[ 'Up' ] = UpFile.Get( name+'_RPVStopStopToJets_'+args.decay+'_M-'+str(xmass) )
		histos[ 'Down' ] = DownFile.Get( name+'_RPVStopStopToJets_'+args.decay+'_M-'+str(xmass) )

		if rebinX > 1: 
			for k in histos: histos[ k ].Rebin( rebinX )

		gausNom = TF1("gaus", "gaus", int(xmass)-30, int(xmass)+30)
		gausNom.SetParameter(1, xmass)
		histos[ 'Nominal' ].Fit(gausNom, 'MEIRLLF' )
		gausUp = TF1("gaus", "gaus", int(xmass)-30, int(xmass)+30)
		gausUp.SetParameter(1, xmass)
		histos[ 'Up' ].Fit(gausUp, 'MEIRLLF')
		gausDown = TF1("gaus", "gaus", int(xmass)-30, int(xmass)+30)
		gausDown.SetParameter(1, xmass)
		histos[ 'Down' ].Fit(gausDown, 'MEIRLLF')

		totalNumber = search( dictEvents, 'RPVStopStopToJets_UDD312_M-'+str(xmass) )[0]
		nomArray.append( gausNom.Integral( int(xmass)-30, int(xmass)+30 ) / totalNumber )
		upArray.append( gausUp.Integral( int(xmass)-30, int(xmass)+30 ) / totalNumber )
		downArray.append( gausDown.Integral( int(xmass)-30, int(xmass)+30 ) / totalNumber )
		upOverNomArray.append( ( gausUp.Integral( int(xmass)-30, int(xmass)+30 ) - gausNom.Integral( int(xmass)-30, int(xmass)+30 ) ) / gausNom.Integral( int(xmass)-30, int(xmass)+30 ) )
		downOverNomArray.append( ( gausDown.Integral( int(xmass)-30, int(xmass)+30 ) - gausNom.Integral( int(xmass)-30, int(xmass)+30 ) ) / gausNom.Integral( int(xmass)-30, int(xmass)+30 ) )

		binWidth = histos['Nominal'].GetBinWidth(1)

		legend=TLegend(0.60,0.75,0.90,0.90)
		legend.SetFillStyle(0)
		legend.SetTextSize(0.03)
		legend.AddEntry( histos[ 'Nominal' ], 'Nominal', 'l' )
		legend.AddEntry( histos[ 'Up' ], args.unc+'Up', 'l' )
		legend.AddEntry( histos[ 'Down' ], args.unc+'Down', 'l' )

		histos[ 'Nominal' ].SetLineWidth(2)
		histos[ 'Up' ].SetLineWidth(2)
		histos[ 'Down' ].SetLineWidth(2)
		histos[ 'Nominal' ].SetLineColor(kBlack)
		histos[ 'Up' ].SetLineColor(kBlue)
		histos[ 'Down' ].SetLineColor(kRed)
		histos[ 'Nominal' ].SetMaximum( 1.2* max( histos[ 'Nominal' ].GetMaximum(), histos[ 'Up' ].GetMaximum(), histos[ 'Down' ].GetMaximum() ) ) 
		if xmax: histos[ 'Nominal' ].GetXaxis().SetRangeUser( xmin, xmax )

		can = TCanvas('c1', 'c1',  10, 10, 750, 500 )
		if log: can.SetLogy()
		#histos['Sample1'].SetMinimum(10)
		histos['Nominal'].GetXaxis().SetRangeUser( xmass-70, xmass+70   )
		histos['Nominal'].Draw('histe') 
		histos['Up'].Draw('histe same')
		histos['Down'].Draw('histe same')
		gausNom.SetLineColor(kBlack)
		gausNom.Draw('same')
		gausUp.SetLineColor(kBlue)
		gausUp.Draw('same')
		gausDown.SetLineColor(kRed)
		gausDown.Draw('same')
		histos['Nominal'].GetYaxis().SetTitleOffset(0.9)
		histos['Nominal'].GetYaxis().SetTitle( 'Events / '+str(binWidth) )

		labelAxis( name, histos['Nominal'], Groom )
		legend.Draw()
		CMS_lumi.extraText = "Simulation Preliminary"
		CMS_lumi.relPosX = 0.12
		CMS_lumi.CMS_lumi(can, 4, 0)
		if not (labX and labY): labels( name, '' )
		else: labels( name, '', labX, labY )

		can.SaveAs( 'Plots/'+outputFileName )
		del can

	tdrStyle.SetPadRightMargin(0.05)
	tdrStyle.SetPadLeftMargin(0.15)
	can = TCanvas('c1', 'c1',  10, 10, 750, 750 )
	pad1 = TPad("pad1", "Fit",0,0.207,1.00,1.00,-1)
	pad2 = TPad("pad2", "Pull",0,0.00,1.00,0.30,-1);
	pad1.Draw()
	pad2.Draw()

	pad1.cd()
	#PT = TText(0.1, 0.1, sample )
	multiGraph = TMultiGraph()
	legend=TLegend(0.70,0.70,0.90,0.90)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.03)

	nomGraph = TGraph( len( massList ), array( 'd', massList), array( 'd', nomArray) )		
	nomGraph.SetLineColor( kBlack )
	nomGraph.SetLineWidth( 2 )
	multiGraph.Add( nomGraph )
	legend.AddEntry( nomGraph, 'Nominal', 'l' )

	upGraph = TGraph( len( massList ), array( 'd', massList), array( 'd', upArray) )		
	upGraph.SetLineColor( kBlue )
	upGraph.SetLineWidth( 2 )
	multiGraph.Add( upGraph )
	legend.AddEntry( upGraph, args.unc+'Up', 'l' )

	downGraph = TGraph( len( massList ), array( 'd', massList), array( 'd', downArray) )		
	downGraph.SetLineColor( kRed )
	downGraph.SetLineWidth( 2 )
	multiGraph.Add( downGraph )
	legend.AddEntry( downGraph, args.unc+'Down', 'l' )

	multiGraph.Draw("ALP")
	multiGraph.GetXaxis().SetTitle('Average pruned mass [GeV]')
	multiGraph.GetYaxis().SetTitle('Acceptance')
	multiGraph.GetYaxis().SetTitleOffset(0.95)
	legend.Draw()
	pad2.cd()
	pad2.SetGrid()
	pad2.SetTopMargin(0)
	pad2.SetBottomMargin(0.3)
	multiGraphRatio = TMultiGraph()

	upOverNomGraph = TGraph( len( massList ), array( 'd', massList), array( 'd', upOverNomArray) )		
	upOverNomGraph.SetMarkerStyle( 20 )
	upOverNomGraph.SetMarkerColor( kBlue )
	multiGraphRatio.Add( upOverNomGraph )
	downOverNomGraph = TGraph( len( massList ), array( 'd', massList), array( 'd', downOverNomArray) )		
	downOverNomGraph.SetMarkerStyle( 24 )
	downOverNomGraph.SetMarkerColor( kRed)
	multiGraphRatio.Add( downOverNomGraph )

	multiGraphRatio.Draw("AP")
	multiGraphRatio.GetYaxis().SetRangeUser(-0.1,0.1)
	multiGraphRatio.GetYaxis().SetNdivisions(505)
	multiGraphRatio.GetXaxis().SetTitle('Average pruned mass [GeV]')
	multiGraphRatio.GetXaxis().SetLabelSize(0.12)
	multiGraphRatio.GetXaxis().SetTitleSize(0.12)
	multiGraphRatio.GetYaxis().SetTitle('(Up(Down)-Nom)/Nom')
	#multiGraphRatio.GetYaxis().SetTitleOffset(0.95)
	multiGraphRatio.GetYaxis().SetLabelSize(0.12)
	multiGraphRatio.GetYaxis().SetTitleSize(0.12)
	multiGraphRatio.GetYaxis().SetTitleOffset(0.45)
	multiGraphRatio.GetYaxis().CenterTitle()
	can.SaveAs('Plots/'+name+'_'+args.decay+'RPVSt_'+args.RANGE+'_'+args.unc+args.version+'.'+args.ext)
	del can
	

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--proc', action='store', default='1D', dest='process', help='Process to draw, example: 1D, 2D, MC.' )
	parser.add_argument('-d', '--decay', action='store', default='UDD312', dest='decay', help='Decay, example: UDD312, UDD323.' )
	parser.add_argument('-v', '--version', action='store', default='Boosted', dest='version', help='Boosted or Resolved version, example: Boosted' )
	parser.add_argument('-g', '--grom', action='store', default='pruned', dest='grooming', help='Grooming Algorithm, example: Pruned, Filtered.' )
	parser.add_argument('-C', '--cut', action='store', default='_cutMassAsym', dest='cut', help='cut, example: cutDEta' )
	parser.add_argument('-s', '--single', action='store', default='all', dest='single', help='single histogram, example: massAve_cutDijet.' )
	parser.add_argument('-l', '--lumi', action='store', type=float, dest='lumi', default=2.6, help='Luminosity, example: 1.' )
	parser.add_argument('-r', '--range', action='store', default='low', dest='RANGE', help='Trigger used, example PFHT800.' )
	parser.add_argument('-e', '--extension', action='store', default='png', dest='ext', help='Extension of plots.' )
	parser.add_argument('-u', '--unc', action='store', default='JES', dest='unc',  help='Type of uncertainty' )

	try: args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)

	CMS_lumi.lumi_13TeV = str(args.lumi)+" fb^{-1}"
	
	plotList = [ 
		[ 'massAve', 0, 400, 2, 0.85, 0.45, False],
		#[ 'jet1Pt', 400, 1500, 2, 0.85, 0.45, False],
		#[ 'jet2Pt', 400, 1500, 2, 0.85, 0.45, False],
		#[ 'HT', 700, 2000, 5, 0.85, 0.45, False],

		]

	if 'all' in args.single: Plots = plotList 
	else: Plots = [ y for y in plotList if ( y[2] in args.single ) ]

	if 'Resolved' in args.version: args.grooming =  '' 
	if 'all' in args.grooming: Groommers = [ '', 'Trimmed', 'Pruned', 'Filtered', "SoftDrop" ]
	else: Groommers = [ args.grooming ]

	if 'all' in args.cut: 
		if 'Boosted' in args.version: listCuts = [ '_jet1Tau21', '_jet2Tau21', '_prunedMassAsym', '_deltaEtaDijet', '_jet1Tau31', '_jet2Tau31' ]
		else: listCuts = [ '_cutMassRes', '_cutDelta', '_cutEtaBand', '_cutDeltaR', '_cutCosTheta', '_cutDEta', '_cutMassPairing' ]
	else: listCuts = [ args.cut ]


	for i in Plots:
		for optGroom in Groommers:
			for cut in listCuts: plotSystematics( 'Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_RPVStopStopToJets_'+args.decay+'_M-100_'+args.RANGE+'_v05.root', optGroom, i[0]+args.cut, i[1], i[2], i[3], i[4], i[5], i[6] )
			
