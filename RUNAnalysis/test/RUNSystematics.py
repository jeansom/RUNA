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

boostedMassAveBins = array( 'd', [ 0, 3, 6, 9, 12, 16, 19, 23, 26, 30, 34, 39, 43, 47, 52, 57, 62, 67, 72, 78, 83, 89, 95, 102, 108, 115, 122, 129, 137, 144, 153, 161, 170, 179, 188, 197, 207, 218, 228, 240, 251, 263, 275, 288, 301, 315, 329, 344, 359, 375, 391, 408, 425, 443, 462, 482, 502 ] )
boostedMassAveBinSize = array( 'd', [ 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 10, 10, 10, 11, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 18, 19, 19, 20, 21] )

def plotSystematics( inFileSample, Groom, name, xmin, xmax, rebinX, labX, labY, log):
	"""docstring for plot"""

	if 'low' in args.RANGE : 
		massList = [ 80, 90, 100, 110, 120, 130, 140, 150 ]
		massWindow = 30 
	else: 
		massList = [ 170, 180, 190, 210, 220, 230, 240, 300, 350 ] 
		massWindow = 30 

	nomArray = []
	nomArrayErr = []
	upArray = []
	upArrayErr = []
	downArray = []
	downArrayErr = []
	upOverNomArray = []
	downOverNomArray = []

	for xmass in massList:

		gStyle.SetOptFit(1)
		NominalFile = TFile.Open( inFileSample.replace( '100', str(xmass) ) )
		UpFile = TFile.Open( inFileSample.replace( '100', str(xmass)+args.unc+'Up'  ) )
		DownFile = TFile.Open( inFileSample.replace( '100', str(xmass)+args.unc+'Down'  ) )

		outputFileName = name+'_'+args.decay+'RPVSt'+str(xmass)+'_'+args.unc+args.boosted+'_'+args.version+'.'+args.ext 
		print 'Processing.......', outputFileName

		histos = {}
		histos[ 'Up' ] = UpFile.Get( name+'_RPVStopStopToJets_'+args.decay+'_M-'+str(xmass) )
		histos[ 'Down' ] = DownFile.Get( name+'_RPVStopStopToJets_'+args.decay+'_M-'+str(xmass) )
		histos[ 'Nominal' ] = NominalFile.Get( name+'_RPVStopStopToJets_'+args.decay+'_M-'+str(xmass) )

		scale = 1 / (scaleFactor( 'RPVStopStopToJets_UDD312_M-'+str(xmass) )*args.lumi )
		for k in histos: 
			histos[ k ].Scale( scale )
			histos[ k ] = histos[ k ].Rebin( rebinX )

		#histos[ 'Up' ] = histos[ 'Up' ].Rebin( len( boostedMassAveBins )-1, histos[ 'Up' ].GetName(), boostedMassAveBins )
		#histos[ 'Down' ] = histos[ 'Down' ].Rebin( len( boostedMassAveBins )-1, histos[ 'Down' ].GetName(), boostedMassAveBins )
		#histos[ 'Nominal' ] = histos[ 'Nominal' ].Rebin( len( boostedMassAveBins )-1, histos[ 'Nominal' ].GetName(), boostedMassAveBins )

		#if rebinX > 1: 
		#for k in histos: histos[ k ] = histos[ k ].Rebin( len( boostedMassAveBins )-1, histos[ k ].GetName(), boostedMassAveBins )

		'''
		####### Fits for Nominal/Up/Down
		gausNom = TF1("gausNom", "gaus", 0, 400 )
		gausNom.SetParameter(1, xmass)
		for i in range(0,5): histos[ 'Nominal' ].Fit(gausNom, 'MIR', '', int(xmass)-massWindow, int(xmass)+massWindow )
		gausNomIntegralError = gausNom.IntegralError(0, 400)
		gausUp = TF1("gausUp", "gaus", 0, 400 )
		gausUp.SetParameter(1, xmass)
		for i in range(0,5): histos[ 'Up' ].Fit(gausUp, 'MIR', '', int(xmass)-massWindow, int(xmass)+massWindow )
		gausUpIntegralError = gausUp.IntegralError(0, 400)
		gausDown = TF1("gausDown", "gaus", 0, 400 )
		gausDown.SetParameter(1, xmass)
		for i in range(0,5): histos[ 'Down' ].Fit(gausDown, 'MIR', '', int(xmass)-massWindow, int(xmass)+massWindow )
		gausDownIntegralError = gausDown.IntegralError(0, 400)
		'''

		binWidth = histos['Nominal'].GetBinWidth(1)
		#totalNumber = scaleFactor( 'RPVStopStopToJets_UDD312_M-'+str(xmass) ) * args.lumi
		totalNumber = search( dictEvents, 'RPVStopStopToJets_UDD312_M-'+str(xmass) )[0]
		errTotalNumber = TMath.Sqrt( totalNumber )
		'''
		nomArray.append( gausNom.Integral( 0, 400 ) / binWidth / totalNumber )
		nomArrayErr.append( gausNomIntegralError / binWidth  / totalNumber )
		upArray.append( gausUp.Integral( 0, 400 ) / binWidth / totalNumber )
		upArrayErr.append( gausUpIntegralError / binWidth / totalNumber )
		downArray.append( gausDown.Integral( 0, 400 ) / binWidth / totalNumber )
		downArrayErr.append( gausDownIntegralError / binWidth / totalNumber )
		upOverNomArray.append( ( gausUp.Integral( 0, 400 ) - gausNom.Integral( 0, 400 ) ) / gausNom.Integral( 0, 400 ) )
		downOverNomArray.append( ( gausDown.Integral( 0, 400 ) - gausNom.Integral( 0, 400 ) ) / gausNom.Integral( 0, 400 ) )
		'''
		errorIntNom = Double(0)
		intNom = histos['Nominal'].IntegralAndError( 0, 40, errorIntNom )
		nomArray.append( intNom / totalNumber )
		nomArrayErr.append( intNom * TMath.Sqrt( TMath.Power( errorIntNom/intNom, 2 ) + TMath.Power( errTotalNumber/totalNumber, 2 ) ) )

		errorIntUp = Double(0)
		intUp = histos['Up'].IntegralAndError( 0, 40, errorIntUp )
		upArray.append( intUp / totalNumber )
		upArrayErr.append( intUp * TMath.Sqrt( TMath.Power( errorIntUp/intUp, 2 ) + TMath.Power( errTotalNumber/totalNumber, 2 ) ) )

		errorIntDown = Double(0)
		intDown = histos['Down'].IntegralAndError( 0, 40, errorIntDown )
		downArray.append( intDown / totalNumber )
		downArrayErr.append( intDown * TMath.Sqrt( TMath.Power( errorIntDown/intDown, 2 ) + TMath.Power( errTotalNumber/totalNumber, 2 ) ) )

		upOverNomArray.append( ( intUp - intNom ) / intNom )
		downOverNomArray.append( ( intDown - intNom ) / intNom )


		legend=TLegend(0.70,0.75,0.90,0.90)
		legend.SetFillStyle(0)
		legend.SetTextSize(0.03)
		legend.AddEntry( histos[ 'Nominal' ], 'Nominal', 'lp' )
		legend.AddEntry( histos[ 'Up' ], args.unc+' Up', 'lp' )
		legend.AddEntry( histos[ 'Down' ], args.unc+' Down', 'lp' )

		histos[ 'Nominal' ].SetLineWidth(2)
		histos[ 'Up' ].SetLineWidth(2)
		histos[ 'Down' ].SetLineWidth(2)
		histos[ 'Nominal' ].SetLineColor(kBlack)
		histos[ 'Up' ].SetLineColor(kBlue)
		histos[ 'Down' ].SetLineColor(kRed)
		histos[ 'Nominal' ].SetMaximum( 1.2* max( histos[ 'Nominal' ].GetMaximum(), histos[ 'Up' ].GetMaximum(), histos[ 'Down' ].GetMaximum() ) ) 
		if xmax: histos[ 'Nominal' ].GetXaxis().SetRangeUser( xmin, xmax )

		can1 = TCanvas('c'+str(xmass), 'c'+str(xmass),  10, 10, 750, 500 )
		if log: can1.SetLogy()
		#histos['Sample1'].SetMinimum(10)
		histos['Nominal'].GetXaxis().SetRangeUser( xmass-70, xmass+70   )
		histos['Nominal'].Draw('histes') 
		histos['Up'].Draw('histe sames')
		histos['Down'].Draw('histe sames')
		histos['Nominal'].GetYaxis().SetTitleOffset(0.9)
		histos['Nominal'].GetYaxis().SetTitle( 'Events / '+str(binWidth) )
		'''
		gausNom.SetLineColor(kBlack)
		gausNom.Draw('sames')
		gausUp.SetLineColor(kBlue)
		gausUp.Draw('sames')
		gausDown.SetLineColor(kRed)
		gausDown.Draw('sames')

		can1.Update()
		st1 = histos['Nominal'].GetListOfFunctions().FindObject("stats")
		st1.SetX1NDC(.12);
		st1.SetX2NDC(.32);
		st1.SetY1NDC(.76);
		st1.SetY2NDC(.91);
		#st1.SetTextColor(4);
		st2 = histos['Up'].GetListOfFunctions().FindObject("stats")
		st2.SetX1NDC(.12);
		st2.SetX2NDC(.32);
		st2.SetY1NDC(.61);
		st2.SetY2NDC(.76);
		st2.SetTextColor(kBlue);
		st3 = histos['Down'].GetListOfFunctions().FindObject("stats")
		st3.SetX1NDC(.12);
		st3.SetX2NDC(.32);
		st3.SetY1NDC(.46);
		st3.SetY2NDC(.61);
		st3.SetTextColor(kRed);
		can1.Modified()
		'''

		labelAxis( name, histos['Nominal'], Groom )
		legend.Draw()
		CMS_lumi.extraText = "Simulation Preliminary"
		CMS_lumi.relPosX = 0.12
		CMS_lumi.CMS_lumi(can1, 4, 0)
		if not (labX and labY): labels( name, '' )
		else: labels( name, '', labX, labY )

		can1.SaveAs( 'Plots/'+outputFileName )
		del can1

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

	zeroList = [0]*len(nomArray)
	#nomGraph = TGraphErrors( len( massList ), array( 'd', massList), array( 'd', nomArray), array('d', zeroList ), array( 'd', nomArrayErr) )
	nomGraph = TGraph( len( massList ), array( 'd', massList), array( 'd', nomArray) )		
	nomGraph.SetMarkerStyle( 21 )
	nomGraph.SetLineColor( kBlack )
	nomGraph.SetLineWidth( 2 )
	multiGraph.Add( nomGraph )
	legend.AddEntry( nomGraph, 'Nominal', 'l' )

	#upGraph = TGraphErrors( len( massList ), array( 'd', massList), array( 'd', upArray), array('d', zeroList ), array( 'd', upArrayErr) )
	upGraph = TGraph( len( massList ), array( 'd', massList), array( 'd', upArray) )		
	upGraph.SetMarkerStyle( 22 )
	upGraph.SetLineColor( kBlue )
	upGraph.SetLineWidth( 2 )
	multiGraph.Add( upGraph )
	legend.AddEntry( upGraph, args.unc+'Up', 'l' )

	#downGraph = TGraphErrors( len( massList ), array( 'd', massList), array( 'd', downArray), array('d', zeroList ), array( 'd', downArrayErr) )
	downGraph = TGraph( len( massList ), array( 'd', massList), array( 'd', downArray) )		
	downGraph.SetMarkerStyle( 23 )
	downGraph.SetLineColor( kRed )
	downGraph.SetLineWidth( 2 )
	multiGraph.Add( downGraph )
	legend.AddEntry( downGraph, args.unc+'Down', 'l' )

	multiGraph.Draw("AP")
	multiGraph.GetXaxis().SetTitle('Average pruned mass [GeV]')
	multiGraph.GetYaxis().SetTitle('Acceptance')
	multiGraph.GetYaxis().SetTitleOffset(0.95)
	legend.Draw()
	pad2.cd()
	pad2.SetGrid()
	pad2.SetTopMargin(0)
	pad2.SetBottomMargin(0.3)
	multiGraphRatio = TMultiGraph()

	for m in range(len(massList)): 	print massList[m], round(upOverNomArray[m],3), round(downOverNomArray[m],3)
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
	can.SaveAs('Plots/'+name+'_'+args.decay+'RPVSt_'+args.RANGE+'_'+args.unc+args.boosted+'_'+args.version+'.'+args.ext)
	del can
	

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--proc', action='store', default='1D', dest='process', help='Process to draw, example: 1D, 2D, MC.' )
	parser.add_argument('-d', '--decay', action='store', default='UDD312', dest='decay', help='Decay, example: UDD312, UDD323.' )
	parser.add_argument('-b', '--boosted', action='store', default='Boosted', dest='boosted', help='Boosted or Resolved boosted, example: Boosted' )
	parser.add_argument('-v', '--version', action='store', default='v05', dest='version', help='Version of files: v05.' )
	parser.add_argument('-g', '--grom', action='store', default='pruned', dest='grooming', help='Grooming Algorithm, example: Pruned, Filtered.' )
	parser.add_argument('-C', '--cut', action='store', default='_deltaEtaDijet', dest='cut', help='cut, example: cutDEta' )
	parser.add_argument('-l', '--lumi', action='store', type=float, dest='lumi', default=2606, help='Luminosity, example: 1.' )
	parser.add_argument('-r', '--range', action='store', default='low', dest='RANGE', help='Trigger used, example PFHT800.' )
	parser.add_argument('-e', '--extension', action='store', default='png', dest='ext', help='Extension of plots.' )
	parser.add_argument('-u', '--unc', action='store', default='JES', dest='unc',  help='Type of uncertainty' )

	try: args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)

	CMS_lumi.lumi_13TeV = ''#str( round( ( args.lumi / 1000 ), 2 ) )+" fb^{-1}"
	
	if 'Resolved' in args.boosted: args.grooming =  '' 
	if 'all' in args.grooming: Groommers = [ '', 'Trimmed', 'Pruned', 'Filtered', "SoftDrop" ]
	else: Groommers = [ args.grooming ]


	for optGroom in Groommers: plotSystematics( 'Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_RPVStopStopToJets_'+args.decay+'_M-100_'+args.RANGE+'_'+args.version+'.root', optGroom, 'massAve'+args.cut, 0, 400, 10, 0.85, 0.45, False )
			
