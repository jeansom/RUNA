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
from DrawHistogram import Rebin2D
try:
	from RUNA.RUNAnalysis.histoLabels import labels, labelAxis, finalLabels, setSelection
	from RUNA.RUNAnalysis.scaleFactors import * #scaleFactor as SF
	from RUNA.RUNAnalysis.commonFunctions import * 
	from RUNA.RUNAnalysis.cuts import selection 
	import RUNA.RUNAnalysis.CMS_lumi as CMS_lumi 
	import RUNA.RUNAnalysis.tdrstyle as tdrstyle
except ImportError:
	sys.path.append('../python')
	from histoLabels import labels, labelAxis, finalLabels
	from scaleFactors import * #scaleFactor as SF
	from commonFunctions import * 
	from cuts import selection 
	import CMS_lumi as CMS_lumi 
	import tdrstyle as tdrstyle

gROOT.Reset()
gROOT.SetBatch()
gROOT.ForceStyle()
tdrstyle.setTDRStyle()
gStyle.SetOptStat(0)

xline = array('d', [0,2000])
yline = array('d', [1, 1])
line = TGraph(2, xline, yline)
line.SetLineColor(kRed)

yline11 = array('d', [1.1, 1.1])
line11 = TGraph(2, xline, yline11)
line11.SetLineColor(kBlue)

yline09 = array('d', [0.9, 0.9])
line09 = TGraph(2, xline, yline09)
line09.SetLineColor(kBlue)

yline0 = array('d', [0,0])
line0 = TGraph(2, xline, yline0)
line0.SetLineColor(kRed)


def listOfCont( histo ):
 	"""docstring for listOfCont"""
	tmpListContent = []
	tmpListError = []
	for ibin in range( histo.GetNbinsX() ): 
		tmpListContent.append( histo.GetBinContent( ibin ) )
		tmpListError.append( histo.GetBinError( ibin ) )
	return tmpListContent, tmpListError

def BCDHisto( tmpHisto, BList, CList, DList ):
	"""docstring for BCDHisto"""

	tmpHisto.Reset()
	for jbin in range( len( BList ) ):
		Nominal_Side = BList[ jbin ]
		Side_Side = CList[ jbin ]
		Side_Nominal = DList[ jbin ]
		if Side_Side != 0: 
			Bkg = Nominal_Side*Side_Nominal/Side_Side
			#BkgError = TMath.Sqrt( Bkg ) 
			try: BkgError = Bkg * TMath.Sqrt( TMath.Power(( TMath.Sqrt( Nominal_Side ) / Nominal_Side ), 2) + TMath.Power(( TMath.Sqrt( Side_Nominal ) / Side_Nominal ), 2) + TMath.Power(( TMath.Sqrt( Side_Side ) / Side_Side ), 2) )
			except ZeroDivisionError: BkgError = 0
		else: 
			Bkg = 0
			BkgError = 0
		tmpHisto.SetBinContent( jbin, Bkg )
		tmpHisto.SetBinError( jbin, BkgError )
	return tmpHisto

def addSysBand( histo, uncSys, colour, additionalSys='' ):
	"""docstring for addSysBand"""
	
	hclone = histo.Clone()
	hclone.Reset()
	for i in range( 0, histo.GetNbinsX()+1 ):
		cont = histo.GetBinContent( i )
		contError = histo.GetBinError( i )
		hclone.SetBinContent( i, cont )
		if additionalSys:
			addCont = additionalSys.GetBinContent( i )
			addContError = additionalSys.GetBinError( i )
		totalErr = TMath.Sqrt( TMath.Power(((cont*uncSys) -cont), 2 ) +  TMath.Power( contError, 2 ) + ( TMath.Power( addContError, 2 ) if additionalSys else 0 ) )
		hclone.SetBinError( i, totalErr  )
	#hclone.SetFillStyle(3018)
	hclone.SetFillColor( colour )
	return hclone


def makePulls( histo1, histo2 ):
	"""docstring for makePulls"""

	histoPulls = histo1.Clone()
	histoPulls.Reset()
	pullsOnly = TH1F( 'pullsOnly', 'pullsOnly', 14, -3, 3 )
	for ibin in range(0, histo1.GetNbinsX() ):
		try: pull = ( histo1.GetBinContent( ibin ) - histo2.GetBinContent( ibin ) ) / histo1.GetBinError( ibin ) 
		except ZeroDivisionError: pull = 0
		histoPulls.SetBinContent( ibin, pull )
		histoPulls.SetBinError( ibin, 1 )
		pullsOnly.Fill( pull )

	return histoPulls, pullsOnly

def rebin( histo, binning ):
	"""docstring for rebin"""

	oldhisto = histo.Clone()
	if 'reso' in str(binning):  
		boostedMassAveBins = array( 'd', [ 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 170, 175, 180, 185, 190, 195, 200, 205, 210, 215, 220, 225, 230, 235, 240, 245, 250, 255, 260, 265, 270, 275, 280, 285, 290, 300, 310, 320, 330, 340, 350, 500, 510 ] )
		newhisto = oldhisto.Rebin( len( boostedMassAveBins )-1, oldhisto.GetName(), boostedMassAveBins )
	elif 'ratio' in str(binning): 
		boostedMassAveBins = array( 'd', [ 0, 25, 75, 150, 250, 450, 500 ] )
		#boostedMassAveBins = array( 'd', [ 0, 25, 50, 75, 100, 150, 200, 300, 400, 500 ] )
		newhisto = oldhisto.Rebin( len( boostedMassAveBins )-1, oldhisto.GetName(), boostedMassAveBins )
	else:
		newhisto = oldhisto.Rebin( binning )

	return newhisto
	
def substractHistos( histo1, histo2 ):
	"""docstring for  substractHistos"""
	
	finalHisto = histo1.Clone()
	finalHisto.Add( histo2, -1 )

	return finalHisto

def ratioPlots( histo1, histo2, graphOnly=False ):
	"""docstring for ratioPlots"""

	chi2 = 0
	ndf = 0
	#h1errFull = histo1.Clone()
	#h1errFull.Reset()
	#h1errh2 = histo1.Clone()
	#h1errh2.Reset()
	ratioList = []
	binCenterList = []
	ratioLogNErrXPlusList = []
	ratioLogNErrXMinusList = []

	for ibin in range( 0, histo1.GetNbinsX() ):
		binCenterList.append( histo1.GetXaxis().GetBinCenter( ibin ) )
		x = histo1.GetBinContent( ibin )
		xErr = histo1.GetBinError( ibin )
		y = histo2.GetBinContent( ibin )
		yErr = histo2.GetBinError( ibin )
		try: 
			ratio = x/y
			ratioErrX = ratio * TMath.Sqrt( TMath.Power( xErr/x, 2) + TMath.Power( yErr/y, 2)  )
			ratioErrY = ratio* yErr / y
			ratioLogNErrXPlus = TMath.Sqrt( TMath.Power( ( (x/(y-yErr)) - ratio ), 2 )  + TMath.Power( ( ((x+xErr)/y) - ratio ) , 2) ) 
			ratioLogNErrXMinus = TMath.Sqrt( TMath.Power( ( (x/(y+yErr)) - ratio ), 2 )  + TMath.Power( ( ((x-xErr)/y) - ratio ) , 2) ) 
		except ZeroDivisionError: 
			ratio = 0
			ratioErrX = 0
			ratioErrY = 0
			ratioLogNErrXPlus = 0
			ratioLogNErrXMinus = 0
		#print x, xErr, y, yErr, ratio, ratioErrX, ratioLogNErrX, ratioErrY, ratioLogNErrY
		#print x, xErr, y, yErr, ratio, ratioLogNErrXPlus, ratioLogNErrXMinus
		#h1errFull.SetBinContent( ibin, ratio )
		#h1errFull.SetBinError( ibin, ratioErrX )
		#h1errh2.SetBinContent( ibin, ratio )
		#h1errh2.SetBinError( ibin, ratioErrY )
		ratioList.append( ratio )
		ratioLogNErrXPlusList.append( ratioLogNErrXPlus )
		ratioLogNErrXMinusList.append( ratioLogNErrXMinus )
		'''
		if ibin < 35 :
			if (y>0):
				try: chi2 += ((y-x)*(y-x))/( (yErr*yErr) + (xErr*xErr) )
				except ZeroDivisionError: chi2 += 0
				ndf += 1
		'''

	'''
	histoAsymErrors = histo1.Clone()
	histoAsymErrors.Reset()
	histoAsymErrors.Sumw2(False)
	for ibin in range( histoAsymErrors.GetNbinsX() ):
		histoAsymErrors.SetBinContent( ibin, ratioList[ibin] )
	histoAsymErrors.SetBinErrorOption(TH1.kPoisson)
	'''

	zeroArray = array( 'd', ( [ 0 ] * (len( ratioList )) ) )
	if graphOnly: asymErrors = TGraph( len(ratioList), array('d', binCenterList), array('d', ratioList) ) 
	else: asymErrors = TGraphAsymmErrors( len(ratioList), array('d', binCenterList), array('d', ratioList), zeroArray, zeroArray, array('d',ratioLogNErrXMinusList), array('d', ratioLogNErrXPlusList) )

	#return h1errFull, h1errh2, chi2, ndf-1, asymErrors
	return asymErrors

def ABCDwithTF( histoB, function, fitResults, hextraHistoB ):
	"""docstring for ABCDwithTF: creates histogram with ABCD prediction using the transfer function """

	listFitValues = []
	listFitErrors = []
	listBinCenter = []
	histoBCD = histoB.Clone()
	histoBCD.Reset()
	histoRatioCD = histoB.Clone()
	histoRatioCD.Reset()
	histoBCDminusExtra = histoB.Clone()
	histoBCDminusExtra.Reset()

	for ibin in range( 1, histoBCD.GetNbinsX() ):

		### data 
		contB = histoB.GetBinContent( ibin )
		errorB = histoB.GetBinError( ibin )
		binCenter = histoB.GetBinCenter( ibin )
		factorCD = function.Eval( binCenter )
		contBCD = contB * factorCD

		err = array( 'd', [0] )   ### error in fit
		fitResults.GetConfidenceIntervals( 1, 1, 1, array('d',[binCenter]), err, 0.683, False ) 
		#print ibin, contB, errorB, binCenter, factorCD, contBCD, err[0]
		listFitValues.append( factorCD )
		listFitErrors.append( err[0] )
		listBinCenter.append( binCenter )

		try: errBCD = contBCD* TMath.Sqrt( TMath.Power( err[0]/factorCD, 2 ) + TMath.Power( errorB/contB, 2 ) )
		except ZeroDivisionError: errBCD = 1.8
		if contBCD == 0 : errBCD = 1.8

		histoBCD.SetBinContent( ibin, contBCD )
		histoBCD.SetBinError( ibin, errBCD )
		histoRatioCD.SetBinContent( ibin, factorCD )
		histoRatioCD.SetBinError( ibin, err[0] )

		if isinstance( hextraHistoB, TH1F ):
			contBextraHistoB = hextraHistoB.GetBinContent( ibin )
			errorBextraHistoB = hextraHistoB.GetBinError( ibin )
			contBCDextraHistoB = ( factorCD * contBextraHistoB  )
			try: errBCDextraHistoB = contBCDextraHistoB* TMath.Sqrt( TMath.Power( err[0]/factorCD, 2 ) + TMath.Power( errorBextraHistoB/contBextraHistoB, 2 ) )
			except ZeroDivisionError: errBCDextraHistoB = 1.8

			contBCDMinusextraHistoB = contBCD - contBCDextraHistoB
			errorBCDMinusextraHistoB = TMath.Sqrt( ( errBCD*errBCD ) + ( errBCDextraHistoB*errBCDextraHistoB ) )
			histoBCDminusExtra.SetBinContent( ibin, contBCDMinusextraHistoB )
			histoBCDminusExtra.SetBinError( ibin, errorBCDMinusextraHistoB )

	returnList = [ histoBCD, histoRatioCD, histoBCDminusExtra, listFitValues, listFitErrors, listBinCenter ]
	return returnList



def alternativeABCDCombined( nameInRoot, binning, minX, maxX, hDataB, hDataC, hDataD, hBkgB, hBkgC, hBkgD, hDataMinusResonantBkgB, hDataMinusResonantBkgC, hDataMinusResonantBkgD, typePlot, ttbarC, plot=True, rootFile=False, bkgSamples='', makeBkgPlots=False, hDataBbTag='' ):
	"""docstring for alternativeABCDcombined: fits ratio B/D and multiply by C"""
	
	############# Data
	hDataC = rebin( hDataC, binning ) 
	hDataD = rebin( hDataD, binning ) 
	hDataCD = hDataC.Clone()
	hDataCD.Reset()
	hDataCD.Divide( hDataC, hDataD, 1., 1., '' )

	#### data minus ttbar and wjets
	hDataMinusTTbarC = rebin( hDataMinusResonantBkgC, binning ) 
	hDataMinusTTbarD = rebin( hDataMinusResonantBkgD, binning ) 
	hDataMinusTTbarCD = hDataMinusTTbarC.Clone()
	hDataMinusTTbarCD.Reset()
	hDataMinusTTbarCD.Divide( hDataMinusTTbarC, hDataMinusTTbarD, 1., 1., '' )
	######################################################

	############## all bkgs
	hBkgC = rebin( hBkgC, binning ) 
	hBkgD = rebin( hBkgD, binning ) 
	hBkgCD = hBkgC.Clone()
	hBkgCD.Reset()
	hBkgCD.Divide( hBkgC, hBkgD, 1, 1, '' )
	if isinstance( ttbarC, TH1F ): httbarC = rebin( ttbarC, binning ) 
	######################################################

	################ Fit 
	#### for prunedMassAsymVsdeltaEtaDijet
	#fitFunction = '1/([0]+TMath::Exp([1]+([2]*x*x)))'  ## v1
	fitFunction = '1/([0]+TMath::Exp([1]+([2]*x*x*x)))'   ## v2
	#fitFunction = '1/([2]+TMath::Exp(-[0]*(x-[1])))'  ## v3
	#fitFunction = 'pol1'

	print ' |----> Fit to Bkg'
	fitBkgCD = TF1( 'fitBkgCD', fitFunction, 0, 500 )
	fitBkgCD.SetParameter( 0, 2 )
	#fitBkgCD.SetParameter( 1, 1 )  #### 1, 150
	#fitBkgCD.SetParameter( 2, 0.55 )
	for i in range(3):  fitBkgCDResult =  TFitResultPtr(hBkgCD.Fit( fitBkgCD, 'MIRS', '', minX, maxX ) )

	print ' |----> Fit to data'
	fitCD = TF1( 'fitCD', fitFunction, 0, 500 )
	for p in range(fitBkgCD.GetNpar() ): fitCD.SetParameter( p, fitBkgCD.GetParameter( p ) )
	fitCDResult =  TFitResultPtr(hDataCD.Fit( fitCD, 'MIRS', '', minX, maxX ) )

	print ' |----> Fit to data minus ttbar and wjets'
	fitWOttbarCD = TF1( 'fitWOttbarCD', fitFunction, 0, 500 )
	for p in range(fitBkgCD.GetNpar() ): fitWOttbarCD.SetParameter( p, fitBkgCD.GetParameter( p ) )
	fitWOttbarCDResult =  TFitResultPtr(hDataMinusTTbarCD.Fit( fitWOttbarCD, 'MIRS', '', minX, maxX ) )
	######################################################
	
	#### Create histogram with prediction
	dataABCDwithTFList = ABCDwithTF( hDataB, fitCD, fitCDResult, False )  
	hDataBCD = dataABCDwithTFList[0]
	hDataRatioCD = dataABCDwithTFList[1]
	mcbkgABCDwithTFList = ABCDwithTF( hBkgB, fitBkgCD, fitBkgCDResult, False )  
	hallBkgBCD = mcbkgABCDwithTFList[0]
	hBkgRatioCD = mcbkgABCDwithTFList[1]
	dataMinusttbarABCDwithTFList = ABCDwithTF( hDataMinusResonantBkgB, fitWOttbarCD, fitWOttbarCDResult, False )  
	hDataMinusTTbarBCD = dataMinusttbarABCDwithTFList[0]
	hDataMinusTTbarRatioCD = dataMinusttbarABCDwithTFList[1]
	listFitValues = dataMinusttbarABCDwithTFList[3]
	listFitErrors = dataMinusttbarABCDwithTFList[4]
	listBinCenter = dataMinusttbarABCDwithTFList[5] 
	hDatabTag = ( ABCDwithTF( hDataBbTag, fitWOttbarCD, fitWOttbarCDResult, False )[0] if hDataBbTag else '' )
	hBkgBCD = ABCDwithTF( hBkgB, fitWOttbarCD, fitWOttbarCDResult, False )[0]
	
	#### Create rootfile for limit setting
	if rootFile:
		tmpFile = TFile('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_JetHT_Run2016_ABCDBkg_V2p1_'+args.version+'.root', 'recreate' )
		hDataBCD.SetName( 'massAve_prunedMassAsymVsdeltaEtaDijet_JetHT_Run2016_ABCDProj' )
		hDataBCD.Write()
		hDataRatioCD.SetName( 'massAve_prunedMassAsymVsdeltaEtaDijet_JetHT_Run2016_RatioBD' )
		hDataRatioCD.Write()
		hDataMinusTTbarBCD.SetName( 'massAve_prunedMassAsymVsdeltaEtaDijet_DATAMinusTTbar_ABCDProj' )
		hDataMinusTTbarBCD.Write()
		hDataMinusTTbarRatioCD.SetName( 'massAve_prunedMassAsymVsdeltaEtaDijet_DATAMinusTTbar_RatioBD' )
		hDataMinusTTbarRatioCD.Write()
		hDataB.Write()
		tmpFile.Close()

	##### Plot bkg estimation
	if plot:
		fitCDUp = TGraph( len(listFitValues), array( 'd', listBinCenter ), np.add( listFitValues, listFitErrors ) ) 
		fitCDDown = TGraph( len(listFitValues), array( 'd', listBinCenter ), np.subtract( listFitValues, listFitErrors ) ) 

		canCD = TCanvas('canCD', 'canCD',  10, 10, 750, 500 )
		#if 'simple' in args.binning: tmpcanCD= canCD.DrawFrame(0,0,500,2)
		#else: tmpcanCD= canCD.DrawFrame(0,0,boostedMassAveBins[-1],2)
		if not args.final: gStyle.SetOptFit(1)
		hBkgCD.GetYaxis().SetTitle( 'Ratio B/D' )
		hBkgCD.GetYaxis().SetTitleOffset(0.75)
		hBkgCD.GetXaxis().SetTitle( 'Average '+args.grooming+' jet mass [GeV]' )
		hBkgCD.SetStats( True)
		hBkgCD.SetLineColor(kGreen+2)
		hBkgCD.GetXaxis().SetRangeUser( minX, maxX )
		hBkgCD.GetYaxis().SetRangeUser( 0, 1 )
		hBkgCD.Draw()
		#hDataCD.GetYaxis().SetTitle( 'Ratio B/D' )
		#hDataCD.GetYaxis().SetTitleOffset(0.75)
		#hDataCD.GetXaxis().SetTitle( 'Average '+args.grooming+' mass [GeV]' )
		hDataCD.SetStats( True)
		hDataCD.SetMarkerStyle(22)
		hDataCD.SetMarkerColor(kBlue)
		hDataCD.SetLineColor(kBlue)
		hDataCD.Draw("sames")
		hDataMinusTTbarCD.SetStats( True)
		hDataMinusTTbarCD.SetMarkerStyle(23)
		hDataMinusTTbarCD.SetMarkerColor(kRed)
		hDataMinusTTbarCD.Draw("sames")
		fitBkgCD.SetLineWidth(1)
		fitBkgCD.SetLineColor(kGreen+2)
		fitBkgCD.Draw("same")

		fitWOttbarCD.SetLineWidth(2)
		fitWOttbarCD.SetLineColor(kBlue)
		fitWOttbarCD.Draw("same")

		fitCD.SetLineWidth(2)
		fitCD.SetLineColor(kRed)
		fitCD.Draw("same")
		fitCDUp.SetLineColor(kRed)
		fitCDUp.SetLineStyle(2)
		fitCDUp.Draw('same pc')
		fitCDDown.SetLineStyle(2)
		fitCDDown.Draw('same pc')
		fitCDDown.SetLineColor(kRed)

		CMS_lumi.extraText = "Preliminary"
		CMS_lumi.relPosX = 0.13
		CMS_lumi.CMS_lumi(canCD, 4, 0)

		if args.final: 
			legend=TLegend(0.15,0.65,0.55,0.85)
			legend.SetTextSize(0.04)
		else: 
			legend=TLegend(0.35,0.15,0.70,0.35)
			legend.SetTextSize(0.035)
		legend.SetFillStyle(0)
		legend.AddEntry( hDataCD, 'Data (uncorrected)', 'pl' )
		legend.AddEntry( hDataMinusTTbarCD, 'Data minus resonant bkg.', 'pl' )
		legend.AddEntry( hBkgCD, 'QCD MC', 'lep' )
		legend.AddEntry( fitCD, 'Fit to data minus resonant bkg.', 'l' )
		legend.AddEntry( fitCDUp, 'Fit unc. to data minus resonant bkg.', 'l' )
		legend.AddEntry( fitBkgCD, 'Fit to MC', 'l' )
		legend.Draw("same")

		if not args.final:
			canCD.Update()
			st2 = hBkgCD.GetListOfFunctions().FindObject("stats")
			st2.SetX1NDC(.12)
			st2.SetX2NDC(.32)
			st2.SetY1NDC(.76)
			st2.SetY2NDC(.91)
			st2.SetTextColor(kGreen+2)
			st1 = hDataCD.GetListOfFunctions().FindObject("stats")
			st1.SetX1NDC(.32)
			st1.SetX2NDC(.52)
			st1.SetY1NDC(.76)
			st1.SetY2NDC(.91)
			st1.SetTextColor(kBlue)
			st3 = hDataMinusTTbarCD.GetListOfFunctions().FindObject("stats")
			st3.SetX1NDC(.52)
			st3.SetX2NDC(.72)
			st3.SetY1NDC(.76)
			st3.SetY2NDC(.91)
			st3.SetTextColor(kRed)
			canCD.Modified()

		outputFileNameCD = nameInRoot+'_'+typePlot+'_CD_'+args.grooming+'_QCD'+args.qcd+'_bkgShapeEstimationBoostedPlots'+args.version+'.'+args.extension
		canCD.SaveAs('Plots/'+outputFileNameCD)

	#################### bkg with TF
	stackHisto = THStack('stackHisto', 'stack')
	if isinstance( bkgSamples, list ):
		histoTTjets = hBkgC.Clone()
		histoWjets = hBkgC.Clone()
		for bkgSample in bkgSamples[1]:
			if 'TTJets' in bkgSample: histoTTjets = bkgSamples[1][ bkgSample ].Clone()
			if 'WJets' in bkgSample: histoWjets = bkgSamples[1][ bkgSample ].Clone()
		for bkgSample in bkgSamples[0]:
			if '_C' in bkgSample:
				histoBkgBCD = bkgSamples[0][ bkgSample ].Clone()	
				histoBkgBCD.Reset()
				histoBkgHybridBCD = bkgSamples[0][ bkgSample ].Clone()	
				histoBkgHybridBCD.Reset()

				for ibin in range( 1, histoBkgHybridBCD.GetNbinsX() ):
					### with transfer FUNCTION from data
					contB = bkgSamples[0][ bkgSample ].GetBinContent( ibin )
					errorB = bkgSamples[0][ bkgSample ].GetBinError( ibin )
					binCenter = bkgSamples[0][ bkgSample ].GetBinCenter( ibin )
					functionCD = fitCD.Eval( binCenter )
					contHybridBCD = contB * functionCD
					err = array( 'd', [0] )   ### error in fit
					fitCDResult.GetConfidenceIntervals( 1, 1, 1, array('d',[binCenter]), err, 0.683, False ) 
					try: errHybridBCD = contHybridBCD* TMath.Sqrt( TMath.Power( err[0]/functionCD, 2 ) + TMath.Power( errorB/contB, 2 ) )
					except ZeroDivisionError: errHybridBCD = 1.8
					if contHybridBCD == 0 : errHybridBCD = 1.8
					histoBkgHybridBCD.SetBinContent( ibin, contHybridBCD )
					histoBkgHybridBCD.SetBinError( ibin, errHybridBCD )

					#### with transfer FACTOR from data
					factorCD = hDataCD.GetBinContent( ibin )
					errFactorCD = hDataCD.GetBinError( ibin )
					contBCD = contB * factorCD
					#print contB, contBCD, factorCD, hDataCD.GetNbinsX(), bkgSamples[0][ bkgSample ].GetNbinsX()
					try: errBCD = contBCD* TMath.Sqrt( TMath.Power( errFactorCD/factorCD, 2 ) + TMath.Power( errorB/contB, 2 ) )
					except ZeroDivisionError: errBCD = 1.8
					if contBCD == 0 : errBCD = 1.8
					histoBkgBCD.SetBinContent( ibin, contBCD )
					histoBkgBCD.SetBinError( ibin, errBCD )

				if makeBkgPlots:
					hRatioAsymErr = ratioPlots( bkgSamples[1][ bkgSample.replace('_C','') ], histoBkgHybridBCD ) 
					makePlots( nameInRoot, bkgSamples[1][ bkgSample.replace('_C','') ], bkgSample.replace('_C',''), histoBkgHybridBCD, 'Hybrid '+bkgSample.replace('_C','')+' ABCD Pred.', 5, 60, 350, hRatioAsymErr, "MC SR/ABCD Pred", '', bkgSample+'_Log_altBCDHybrid', True, addUncBand=False )

					hRatioAsymErr = ratioPlots( bkgSamples[1][ bkgSample.replace('_C','') ], histoBkgBCD ) 
					makePlots( nameInRoot, bkgSamples[1][ bkgSample.replace('_C','') ], bkgSample.replace('_C',''), histoBkgBCD, ' '+bkgSample.replace('_C','')+' ABCD Pred.', 5, 60, 350, hRatioAsymErr, "MC SR/ABCD Pred", '', bkgSample+'_Log_altBCD', True, addUncBand=False)

					#stackHisto.Add( histoBkgHybridBCD )
	
		hDataBCD.Add( histoTTjets )
		hDataBCD.Add( histoWjets )

	return hDataBCD, hBkgBCD, hallBkgBCD, hDataMinusTTbarBCD, stackHisto, hDatabTag


def plotBkgEstimation( dataFile, bkgFiles, signalFiles, Groom, nameInRoot, xmin, xmax, rebinX, labX, labY, log, Norm=False ):
	"""docstring for plotBkgEstimation"""

	SRHistos = {}
	BCDHistos = {}
	unbinnedBCDHistos = {}
	for bkgSamples in bkgFiles:
		bkgNameHisto = ( nameInRoot+'_'+bkgSamples if args.miniTree else 'BoostedAnalysisPlots/'+nameInRoot )
		print bkgNameHisto
		SRHistos[ bkgSamples ] = bkgFiles[ bkgSamples ][0].Get( bkgNameHisto+'_A' )
		BCDHistos[ bkgSamples+'_B' ] = bkgFiles[ bkgSamples ][0].Get( bkgNameHisto+'_B' )
		unbinnedBCDHistos[ bkgSamples+'_B' ] = BCDHistos[ bkgSamples+'_B' ].Clone()
		BCDHistos[ bkgSamples+'_C' ] = bkgFiles[ bkgSamples ][0].Get( bkgNameHisto+'_C' )
		unbinnedBCDHistos[ bkgSamples+'_C' ] = BCDHistos[ bkgSamples+'_C' ].Clone()
		BCDHistos[ bkgSamples+'_D' ] = bkgFiles[ bkgSamples ][0].Get( bkgNameHisto+'_D' )
		unbinnedBCDHistos[ bkgSamples+'_D' ] = BCDHistos[ bkgSamples+'_D' ].Clone()
		if 'TTJets' in bkgSamples: TTbarScale = bkgFiles[ bkgSamples ][1]
		if 'simple' in args.binning:
			if rebinX > 1: 
				SRHistos[ bkgSamples ] = rebin( SRHistos[ bkgSamples ], rebinX )
				SRHistos[ bkgSamples ].SetFillColor( bkgFiles[ bkgSamples ][3] )
				BCDHistos[ bkgSamples+'_B' ] = rebin( BCDHistos[ bkgSamples+'_B' ], rebinX )
				BCDHistos[ bkgSamples+'_C' ] = rebin( BCDHistos[ bkgSamples+'_C' ], rebinX )
				#BCDHistos[ bkgSamples+'_C' ].SetFillColor( bkgFiles[ bkgSamples ][3] )
				#BCDHistos[ bkgSamples+'_C' ].SetLineWidth( 1 )
				#BCDHistos[ bkgSamples+'_C' ].SetLineStyle( 1 )
				BCDHistos[ bkgSamples+'_D' ] = rebin( BCDHistos[ bkgSamples+'_D' ], rebinX )
		else:
			SRHistos[ bkgSamples ] = rebin( SRHistos[ bkgSamples ], args.binning ) 
			BCDHistos[ bkgSamples+'_B' ] = rebin( BCDHistos[ bkgSamples+'_B' ], args.binning )
			BCDHistos[ bkgSamples+'_C' ] = rebin( BCDHistos[ bkgSamples+'_C' ], args.binning )
			BCDHistos[ bkgSamples+'_D' ] = rebin( BCDHistos[ bkgSamples+'_D' ], args.binning )
		if bkgFiles[ bkgSamples ][1] != 1: 
			scale = bkgFiles[ bkgSamples ][1] 
			SRHistos[ bkgSamples ].Scale( scale ) 
			BCDHistos[ bkgSamples+'_B' ].Scale( scale )
			BCDHistos[ bkgSamples+'_C' ].Scale( scale )
			BCDHistos[ bkgSamples+'_D' ].Scale( scale )
			unbinnedBCDHistos[ bkgSamples+'_B' ].Scale( scale )
			unbinnedBCDHistos[ bkgSamples+'_C' ].Scale( scale )
			unbinnedBCDHistos[ bkgSamples+'_D' ].Scale( scale )
	
	sigHistos = OrderedDict()
	dummySig=0
	for signalSamples in signalFiles:
		signalNameHisto = ( nameInRoot+'_RPVStopStopToJets_'+args.decay+'_M-'+str(signalSamples) if args.miniTree else 'BoostedAnalysisPlots/'+nameInRoot )
		sigHistos[ signalSamples ] = signalFiles[ signalSamples ][0].Get( signalNameHisto+'_A' )
		sigHistos[ signalSamples ] = rebin( sigHistos[ signalSamples ], rebinX )
		sigHistos[ signalSamples ].Scale( signalFiles[ signalSamples ][1] )
		sigHistos[ signalSamples ].SetLineColor( signalFiles[ signalSamples ][3] )
		sigHistos[ signalSamples ].SetLineWidth( 3 )
		sigHistos[ signalSamples ].SetLineStyle( 2+dummySig )
		sigHistos[ signalSamples ].GetXaxis().SetRangeUser( int(signalSamples)-30, int(signalSamples)+30 )
		dummySig+=8

	
	dataNameHisto = ( nameInRoot+'_JetHT_Run2016' if args.miniTree else 'BoostedAnalysisPlots/'+nameInRoot )
	hData =  dataFile.Get( dataNameHisto+'_A' )
	hData = rebin( hData, ( rebinX if 'simple' in args.binning else args.binning ) )
	hDataB =  dataFile.Get( dataNameHisto+'_B' )
	hunbinnedDataB = hDataB.Clone()
	hDataB = rebin( hDataB, ( rebinX if 'simple' in args.binning else args.binning ) )
	hDataC =  dataFile.Get( dataNameHisto+'_C' )
	hunbinnedDataC = hDataC.Clone()
	hDataC = rebin( hDataC, ( rebinX if 'simple' in args.binning else args.binning ) )
	hDataD =  dataFile.Get( dataNameHisto+'_D' )
	hunbinnedDataD = hDataD.Clone()
	hDataD = rebin( hDataD, ( rebinX if 'simple' in args.binning else args.binning ) )
	htmpDataCR =  BCDHisto( hData.Clone(), hDataC, hDataB, hDataD )  
	hDataCR = htmpDataCR.Clone()
	hDataCR.Reset()
	for ibin in range( htmpDataCR.GetNbinsX() ):
		binCont = htmpDataCR.GetBinContent( ibin )
		binErr = htmpDataCR.GetBinError( ibin )
		if binCont == 0:
			hDataCR.SetBinContent( ibin, 0 )
			hDataCR.SetBinError( ibin, 1.8 )
		else:
			hDataCR.SetBinContent( ibin, binCont )
			hDataCR.SetBinError( ibin, binErr )

	##### Data minus ttbar
	hDataMinusResonantBkgB = hunbinnedDataB.Clone()
	hDataMinusResonantBkgC = hDataC.Clone()
	hDataMinusResonantBkgD = hunbinnedDataD.Clone()

	hSR = hDataCR.Clone()
	hSR.Reset()
	for samples in SRHistos: hSR.Add( SRHistos[ samples ].Clone() )
	hBkgMinusqcdA = hDataB.Clone()	
	hBkgMinusqcdA.Reset()
	hBkgB = hDataB.Clone()	
	hBkgB.Reset()
	hBkgC = hDataB.Clone()	
	hBkgC.Reset()
	hBkgD = hDataB.Clone()	
	hBkgD.Reset()
	hunbinnedBkgMinusqcdB = hunbinnedDataB.Clone()	
	hunbinnedBkgMinusqcdB.Reset()
	hBkgMinusqcdC = hDataB.Clone()	
	hBkgMinusqcdC.Reset()
	hunbinnedBkgMinusqcdD = hunbinnedDataB.Clone()	
	hunbinnedBkgMinusqcdD.Reset()
	for isamples in BCDHistos:
		if '_A' in isamples: 
			if not 'QCD' in isamples: 
				hBkgMinusqcdA.Add( SRHistos[ isamples ].Clone() )
		if '_B' in isamples: 
			hBkgB.Add( BCDHistos[ isamples ].Clone() )
			if not 'QCD' in isamples: 
				hunbinnedBkgMinusqcdB.Add( unbinnedBCDHistos[ isamples ].Clone() )
				hDataMinusResonantBkgB.Add( unbinnedBCDHistos[ isamples ].Clone(), -1 )
		elif '_C' in isamples: 
			hBkgC.Add( BCDHistos[ isamples ].Clone() )
			if not 'QCD' in isamples: 
				hBkgMinusqcdC.Add( BCDHistos[ isamples ].Clone() )
				hDataMinusResonantBkgC.Add( BCDHistos[ isamples ].Clone(), -1 )
		elif '_D' in isamples: 
			hBkgD.Add( BCDHistos[ isamples ].Clone() )
			if not 'QCD' in isamples: 
				hunbinnedBkgMinusqcdD.Add( unbinnedBCDHistos[ isamples ].Clone() )
				hDataMinusResonantBkgD.Add( unbinnedBCDHistos[ isamples ].Clone(), -1 )

	
	####### ttbar sample btag
	hDataAbTag =  dataFile.Get( ( nameInRoot+'_JetHT_Run2016_btag_A' if args.miniTree else nameInRoot+'_btag_A' ) )
	hDataAbTag = rebin( hDataAbTag, 20 )
	hDataCbTag =  dataFile.Get( ( nameInRoot+'_JetHT_Run2016_btag_C' if args.miniTree else nameInRoot+'_btag_C' ) )
	hDataCbTag = rebin( hDataCbTag, 20 )

	hTTbarAbTag = bkgFiles[ 'TTJets' ][0].Get( ( nameInRoot+'_TTJets_btag_A' if args.miniTree else nameInRoot+'_btag_A' ) )
	hTTbarAbTag = rebin( hTTbarAbTag, 20 )
	hTTbarAbTag.Scale( TTbarScale )
	hTTbarCbTag = bkgFiles[ 'TTJets' ][0].Get( ( nameInRoot+'_TTJets_btag_C' if args.miniTree else nameInRoot+'_btag_C' ) )
	hTTbarCbTag = rebin( hTTbarCbTag, 20 )
	hTTbarCbTag.Scale( TTbarScale )
	hDataCbTag.Add( hTTbarCbTag, -1 )

	##### Data minus everything except qcd
	#hDataMinusqcdB = hunbinnedDataB.Clone()
	#hDataMinusqcdB.Add( hunbinnedBkgMinusqcdB, -1 )
	#hDataMinusqcdC = hunbinnedDataC.Clone()
	#hDataMinusqcdC.Add( hunbinnedBkgMinusqcdC, -1 )
	#hDataMinusqcdD = hunbinnedDataD.Clone()
	#hDataMinusqcdD.Add( hunbinnedBkgMinusqcdD, -1 )

	#tmphunbinnedBkgMinusQCDB = substractHistos( hunbinnedBkgB, unbinnedBCDHistos[ 'QCD'+args.qcd+'All_B' ] )
	#tmphunbinnedBkgMinusQCDC = substractHistos( hBkgC, BCDHistos[ 'QCD'+args.qcd+'All_C' ] )
	#tmphunbinnedBkgMinusQCDD = substractHistos( hunbinnedBkgD, unbinnedBCDHistos[ 'QCD'+args.qcd+'All_D' ] )
	
	#hDataMinusqcdB = substractHistos( hunbinnedDataB, hunbinnedBkgMinusqcdB )
	#hDataMinusqcdC = substractHistos( hDataC, hBkgMinusqcdC )
	#hDataMinusqcdD = substractHistos( hunbinnedDataD, hunbinnedBkgMinusqcdD )
	

	

	if 'simple' in args.binning: binWidth = round(hSR.GetBinWidth(1))
	else: binWidth = '#sigma_{mass}' 


	#hRatiohSRhDataCRerrFull, hRatiohSRhDataCRerrhData, hDataCRchi2, hDataCRndf, hRatiohSRhDataCRAsymErr = ratioPlots( hSR, hDataCR ) 
	#makePlots( nameInRoot, hSR, 'All MC Bkgs SR', hDataCR, 'DATA ABCD Pred', binWidth, xmin, xmax, hRatiohSRhDataCRAsymErr, "MC SR/ABCD Pred", '', 'DATA_Bkg')
	#hRatiohDataCRhSRerrhSR, hRatiohDataCRhSRerrFull, hDataCRchi2, hDataCRndf, hRatiohDataCRhSRAsymErr = ratioPlots( hDataCR, hSR ) 
	#makePlots( nameInRoot, hSR, 'All MC Bkgs SR', hDataCR, 'DATA ABCD Pred', binWidth, xmin, xmax, hRatiohDataCRhSRerrFull, "ABCD Pred/MC SR)", hRatiohDataCRhSRerrhSR, 'DATA_Bkg_Diff')

	#hRatiohBkgBhDataBerrDataB, hRatiohBkgBhDataBerrFull, hBkgBchi2, hBkgBndf, hRatiohBkgBAsymErr = ratioPlots( hDataB, hBkgB ) 
	#makePlots( nameInRoot, hBkgB, 'All MC Bkgs Region B', hDataB, 'DATA Region B', binWidth, xmin, xmax, hRatiohBkgBAsymErr, "DATA/MC", '', 'B', True)
	#hRatiohBkgChDataCerrDataB, hRatiohBkgChDataCerrFull, hBkgCchi2, hBkgCndf, hRatiohBkgCAsymErr = ratioPlots( hDataC, hBkgC ) 
	#makePlots( nameInRoot, hBkgC, 'All MC Bkgs Region C', hDataC, 'DATA Region C', binWidth, xmin, xmax, hRatiohBkgCAsymErr, "DATA/MC", '', 'C', True)
	#hRatiohBkgDhDataDerrDataB, hRatiohBkgDhDataDerrFull, hBkgDchi2, hBkgDndf, hRatiohBkgDAsymErr = ratioPlots( hDataD, hBkgD ) 
	#makePlots( nameInRoot, hBkgD, 'All MC Bkgs Region D', hDataD, 'DATA Region D', binWidth, xmin, xmax, hRatiohBkgDAsymErr, "DATA/MC", '', 'D', True)



	althDataCR, althBkgCR, althallBkgCR, althDataMinusResonantBkgCR, stackAlthBkgCR, hDatabTag = alternativeABCDCombined( 
			nameInRoot, 
			25, xmin, xmax, 
			hDataC, 
			hunbinnedDataB, 
			hunbinnedDataD, 
			BCDHistos[ 'QCD'+args.qcd+'All_C' ].Clone(), 
			unbinnedBCDHistos[ 'QCD'+args.qcd+'All_B' ].Clone(), 
			unbinnedBCDHistos[ 'QCD'+args.qcd+'All_D' ].Clone(), 
			hDataMinusResonantBkgC, 
			hDataMinusResonantBkgB, 
			hDataMinusResonantBkgD, 
			'combined', 
			None, 
			rootFile=True, 
			bkgSamples=[ BCDHistos, SRHistos ], 
			makeBkgPlots=args.bkgPlots,  
			hDataBbTag=hDataCbTag )   #### for prunedMassAsymVsdeltaEtaDijet

	#althRatiohDataAsymErr = ratioPlots( hData, althDataCR ) 
	#makePlots( nameInRoot, hData, 'DATA', althDataCR, 'DATA ABCD Pred.', binWidth, xmin, xmax, althRatiohDataAsymErr, "DATA/ABCD Pred", '', 'Log_altBCD', True)

	stackABCD = THStack( 'stackABCD', 'stackABCD' )
	stackABCD.Add( SRHistos[ 'Dibosons' ].Clone() )
	stackABCD.Add( SRHistos[ 'ZJetsToQQ' ].Clone() )
	stackABCD.Add( SRHistos[ 'WJetsToQQ' ].Clone() )
	stackABCD.Add( SRHistos[ 'TTJets' ].Clone() )

	hABCDOnly = althDataMinusResonantBkgCR.Clone()
	hABCDOnly.SetFillColor( kBlue )
	stackABCD.Add( hABCDOnly )
	addAllBkg = hABCDOnly.Clone()
	addAllBkg.Add( hBkgMinusqcdA )

	hABCDOnlySys = addSysBand( hABCDOnly, 1.10, kBlack, additionalSys=hDataC )
	httbarOnlySys = addSysBand( SRHistos[ 'TTJets' ].Clone(), 1.50, kBlack )
	hwjetsOnlySys = addSysBand( SRHistos[ 'WJetsToQQ' ].Clone(), 1.50, kBlack )
	hABCDOnlySys.Add( httbarOnlySys )
	hABCDOnlySys.Add( hwjetsOnlySys )
	hABCDOnlySys.SetLineColor( kBlue )
	hABCDOnlySys.SetLineWidth( 2 )
	hRatioSys = hABCDOnlySys.Clone()
	hRatioSys.Reset()
	for ibin in range( 0, hRatioSys.GetNbinsX()+1 ): 
		hRatioSys.SetBinContent( ibin, 1 )
		try: ratioErr = hABCDOnlySys.GetBinError(ibin) / hABCDOnlySys.GetBinContent(ibin)  
		except ZeroDivisionError: ratioErr=0
		hRatioSys.SetBinError( ibin, ratioErr )

	#makePlots( nameInRoot, addAllBkg, '#splitline{(DATA - tt & Wjets) ABCD Pred.}{plus MC tt & Wjets}', althDataCR, 'DATA ABCD Pred.', binWidth, xmin, xmax, ratioPlots(  addAllBkg, althDataCR, graphOnly=True ), "(DATA-tt&Wjets)/DATA", '', 'Log_diffAltBCD', True, addUncBand=False)

	makePlots( nameInRoot, 
			hData, 'DATA', 
			stackABCD, 'Bkg prediction', 
			binWidth, xmin, xmax, 
			ratioPlots(hData, addAllBkg), "Data/Bkg", 
			'', 'Log_altBCDPlusMCbkgs', 
			True, 
			addHisto=addAllBkg, 
			stackHistos=[ [ hABCDOnly, 'QCD from ABCD'], [ SRHistos[ 'TTJets' ].Clone(), 't #bar{t} + Jets' ], [ SRHistos[ 'WJetsToQQ' ].Clone(), 'W + Jets'], [ SRHistos[ 'ZJetsToQQ' ].Clone(), 'Z + Jets'], [ SRHistos[ 'Dibosons' ], 'Dibosons' ], [ hABCDOnlySys, 'Bkg. uncertainty' ] ], 
			addUncBand=[ hABCDOnlySys, hRatioSys ], 
			signalHistos=sigHistos)

	### althBkgCR is just QCD 
	stackHybridMCABCD = THStack( 'stackHybridMCABCD', 'stackHybridMCABCD' )
	stackHybridMCABCD.Add( SRHistos[ 'Dibosons' ] )
	stackHybridMCABCD.Add( SRHistos[ 'ZJetsToQQ' ].Clone() )
	stackHybridMCABCD.Add( SRHistos[ 'WJetsToQQ' ].Clone() )
	stackHybridMCABCD.Add( SRHistos[ 'TTJets' ].Clone() )
	althBkgCR.SetFillColor( kBlue )
	stackHybridMCABCD.Add( althBkgCR )
	althBkgCR.Add( SRHistos[ 'TTJets' ].Clone() )
	althBkgCR.Add( SRHistos[ 'WJetsToQQ' ].Clone() )
##
	makePlots( nameInRoot, 
			hSR, 'All SM Bkg from MC', 
			stackHybridMCABCD , 'MC Bkg prediction', 
			binWidth, xmin, xmax, 
			ratioPlots( hSR, althBkgCR ), "#frac{All SM Bkg}{All Bkgs with QCD ABCD}", 
			'', 'HybridBkg_Log_altBCD', 
			True, 
			addHisto=althBkgCR, 
			stackHistos=[ [ althBkgCR, 'QCD Hybrid ABCD from MC'], [ SRHistos[ 'TTJets' ].Clone(), 't #bar{t} + Jets' ], [ SRHistos[ 'WJetsToQQ' ].Clone(), 'W + Jets'], [ SRHistos[ 'ZJetsToQQ' ].Clone(), 'Z + Jets'], [ SRHistos[ 'Dibosons' ], 'Dibosons' ] ] 
			)

	### Full closure test
	stackMCABCD = THStack( 'stackMCABCD', 'stackMCABCD' )
	stackMCABCD.Add( SRHistos[ 'Dibosons' ] )
	stackMCABCD.Add( SRHistos[ 'ZJetsToQQ' ].Clone() )
	stackMCABCD.Add( SRHistos[ 'WJetsToQQ' ].Clone() )
	stackMCABCD.Add( SRHistos[ 'TTJets' ].Clone() )
	althallBkgCR.SetFillColor( kBlue )
	stackMCABCD.Add( althallBkgCR )
	althallBkgCR.Add( SRHistos[ 'TTJets' ].Clone() )
	althallBkgCR.Add( SRHistos[ 'WJetsToQQ' ].Clone() )
##
	makePlots( nameInRoot, 
			hSR, 'All SM Bkg from MC', 
			stackMCABCD , 'MC Bkg prediction', 
			binWidth, xmin, xmax, 
			ratioPlots( hSR, althallBkgCR ), "#frac{All SM Bkg}{All Bkgs with QCD ABCD}", 
			'', 'MCBkg_Log_altBCD', 
			True, 
			addHisto=althallBkgCR, 
			stackHistos=[ [ althallBkgCR, 'QCD ABCD from MC'], [ SRHistos[ 'TTJets' ].Clone(), 't #bar{t} + Jets' ], [ SRHistos[ 'WJetsToQQ' ].Clone(), 'W + Jets'], [ SRHistos[ 'ZJetsToQQ' ].Clone(), 'Z + Jets'], [ SRHistos[ 'Dibosons' ], 'Dibosons' ] ] 
			)

	#### with bTag
	hDatabTagPlusMC = hDatabTag.Clone()
	stackbTagABCD = THStack( 'stackbTagABCD', 'stackbTagABCD' )
	stackbTagABCD.Add( hTTbarAbTag )
	stackbTagABCD.Add( hDatabTag )
	hDatabTag.SetLineColor( kBlue )
	hDatabTag.SetLineWidth( 2 )
	hDatabTag.SetLineStyle( 2 )
	hTTbarAbTag.SetLineColor( kGreen+2 )
	hTTbarAbTag.SetLineWidth( 2 )

	hDatabTagPlusMC.Add( hTTbarAbTag )
	makePlots( nameInRoot, 
			hDataAbTag, 'DATA', 
			stackbTagABCD, 'DATA ABCD Pred.', 
			20, xmin, xmax, 
			ratioPlots( hDataAbTag, hDatabTagPlusMC ), "DATA/ABCD Pred", 
			'', 'bTag_scale'+str(TTbarScale), 
			False, 
			addHisto=hDatabTagPlusMC, 
			stackHistos=[ [ hDatabTag, 'ABCD QCD Prediction' ], [ hTTbarAbTag, 'MC t #bar{t} + Jets' ] ], 
			addUncBand=False, doFit=True )



def makePlots( nameInRoot, tmphisto1, labelh1, tmphisto2, labelh2, binWidth, xmin, xmax, ratio, labelRatio, ratio2, typePlot, log=False, reScale=False, addUncBand='', addHisto='', stackHistos='', doFit=False, signalHistos='' ):
	"""docstring for makePlots"""

	histo1 = tmphisto1.Clone()
	histo2 = tmphisto2.Clone()
	if 'DATA' in labelh1:  
		legend=TLegend(0.45,0.70,0.95,0.89)
		legend.SetNColumns(2)
	else:
		legend=TLegend(0.15,0.80,0.95,0.89)
		legend.SetNColumns(3)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.035)
	if 'DATA' in labelh1: legend.AddEntry( histo1, labelh1, 'ep' )
	else: legend.AddEntry( histo1, labelh1, 'l' )
	if signalHistos: 
		for sample in signalHistos: legend.AddEntry( signalHistos[sample], 'M_{#tilde{t}} = '+str(sample)+' GeV', 'l' )
	if isinstance(tmphisto2, THStack):
		for sh in stackHistos: legend.AddEntry( sh[0], sh[1], 'f' ) 
	else: legend.AddEntry( histo2, labelh2, 'pl' )

	histo1.GetYaxis().SetTitle('Events / '+(str(int(binWidth)) if 'simple' in args.binning else binWidth )+' GeV')
	histo1.GetYaxis().SetTitleOffset( 0.9 )
	histo1.GetXaxis().SetRangeUser( xmin, xmax )
	histo1.SetMaximum( 1.5* max( histo1.GetMaximum(), histo2.GetMaximum() ) )
	if 'MC' in labelh1: 
		histo1.SetLineColor(kRed-4)
		histo1.SetLineWidth(2)
	if not isinstance( histo2, THStack ):
		histo2.GetXaxis().SetRangeUser( xmin, xmax )
		histo2.SetLineColor(kBlue)
		histo2.SetLineWidth(2)
		if 'MC' in labelh2: histo2.SetLineStyle(2)
		else: histo2.SetLineStyle(1)

	tdrStyle.SetPadRightMargin(0.05)
	tdrStyle.SetPadLeftMargin(0.15)
	can = TCanvas('c1', 'c1',  10, 10, 750, 750 )
	gStyle.SetOptStat(0)
	pad1 = TPad("pad1", "Main",0,0.30,1.00,1.00,-1)
	pad2 = TPad("pad2", "Ratio",0,0.00,1.00,0.30,-1);
	pad1.Draw()
	pad2.Draw()

	pad1.cd()
	pad1.SetBottomMargin(0)
	if log: 
		pad1.SetLogy() 	
		#if not 'Region' in labelh1: histo1.SetMaximum( 500 )
		histo1.SetMinimum( 0.5 )
	else: 
		pad1.SetGrid()
	if 'DATA' in labelh1: 
		histo1.SetMarkerStyle(8)
		histo1.Draw("PE")
	else: histo1.Draw("histe")

	if isinstance( histo2, THStack ): 
		histo2.Draw('hist same')
		histo1.Draw("histe same")
	else: histo2.Draw('hist E0 same')
	
	if addUncBand and ( len(addUncBand)>0 ): 
		addUncBand[0].SetFillStyle(3005)
		addUncBand[0].Draw("same E2")
		addHisto.SetFillColor( 0 )
		addHisto.Draw("hist same")
		histo1.Draw("PE same")
	if signalHistos: 
		for sample in signalHistos: signalHistos[ sample ].Draw("hist same")

	if isinstance( histo2, THStack ): tmpHisto2 = addHisto
	else: tmpHisto2 = histo2.Clone()
	tmpHisto1 = histo1.Clone()
	try: 
		res = array( 'd', ( [ 0 ] * tmpHisto1.GetNbinsX() ) )
		chi2Ndf =  round( tmpHisto1.Chi2Test(tmpHisto2, 'WWCHI2/NDFP', res), 2 )
		chi2 =  round( tmpHisto1.Chi2Test(tmpHisto2, 'WWCHI2'), 2 )
		chi2Test = TLatex( 0.6, 0.70, '#chi^{2}/ndf Test = '+ str( int(chi2) )+'/'+str( int(chi2/chi2Ndf) ) )
		chi2Test.SetNDC()
		chi2Test.SetTextFont(42) ### 62 is bold, 42 is normal
		chi2Test.SetTextSize(0.035)
		if args.final: chi2Test.Draw()
	except ZeroDivisionError: print ' |---> chi2Test failed. ZeroDivisionError'

	if 'DATA' in labelh1: tmpLabel = 'DATA'
	else: tmpLabel = 'SR'
	numEvents = TLatex( 0.5, 0.75, 'events '+tmpLabel+'/Bkg = '+ str( round( tmpHisto1.Integral(),2 ) )+'/'+str( round( tmpHisto2.Integral(),2 ) ) )
	numEvents.SetNDC()
	numEvents.SetTextFont(42) ### 62 is bold, 42 is normal
	numEvents.SetTextSize(0.035)
	if args.final: numEvents.Draw()

	CMS_lumi.extraText = ("Preliminary" if 'DATA' in labelh1 else "Simulation Preliminary")
	CMS_lumi.relPosX = 0.13
	CMS_lumi.CMS_lumi(pad1, 4, 0)
	legend.Draw()
	pad1.RedrawAxis()

	pad2.cd()
	pad2.SetGrid()
	pad2.SetTopMargin(0)
	pad2.SetBottomMargin(0.3)
	tmpPad2= pad2.DrawFrame(xmin,0.1,xmax,1.9)
	tmpPad2.SetXTitle( 'Average '+args.grooming+' jet mass [GeV]' )
	tmpPad2.SetYTitle( labelRatio )
	tmpPad2.SetTitleSize(0.12, "x")
	tmpPad2.SetTitleSize( (0.09 if 'frac' in labelRatio else 0.12  ), 'y')
	tmpPad2.SetLabelSize(0.10, 'x')
	tmpPad2.SetLabelSize(0.12, 'y')
	tmpPad2.SetTitleOffset( (0.6 if 'frac' in labelRatio else 0.5), 'y')
	#tmpPad2.CenterTitle()
	#tmpPad2.SetTitleOffset(0.55)
	tmpPad2.SetNdivisions(505, 'x' )
	tmpPad2.SetNdivisions(505, 'y' )
	pad2.Modified()
	
	#labelAxis( nameInRoot, ratio, args.grooming )
	#ratio.GetXaxis().SetRangeUser( xmin, xmax )
	ratio.SetMarkerStyle(8)
	ratio.SetLineColor(kBlack)
	#ratio.SetMaximum( 2. )
	#ratio.SetMinimum( 0. )
	#if isinstance( ratio, TGraphAsymmErrors ): ratio.Draw('p')
	ratio.Draw('P')

	if signalHistos: 
		tmpSignalBkg = {}
		for sample in signalHistos: 
			tmpSignalBkg[ sample ] = signalHistos[sample].Clone()
			tmpSignalBkg[ sample ].SetFillColorAlpha( signalFiles[ sample ][3], 0.2 ) 
			tmpSignalBkg[ sample ].Add( addHisto )
			tmpSignalBkg[ sample ].Divide( addHisto )
			tmpSignalBkg[ sample ].Draw("hist same")
		whiteBox = TGraph(4, array('d', [xmin-10, xmax+10, xmax+10, xmin-10]), array('d', [0, 0, 1, 1]))
		whiteBox.SetFillColor(kWhite)
		whiteBox.Draw("F same")
		pad2.RedrawAxis()
		pad2.RedrawAxis('g')


	if addUncBand and ( len(addUncBand) > 1 ):
		addUncBand[1].SetFillStyle(3005)
		addUncBand[1].Draw( 'same E2' )
		ratio.Draw('same P')
	else:
		line11.Draw("same")
		line09.Draw("same")

	if doFit:
		tmpFit = TF1( 'tmpFit', 'pol0', 60, 300 )
		ratio.Fit( 'tmpFit', '', '', 60, 300 )
		tmpFit.SetLineColor( kGreen )
		tmpFit.SetLineWidth( 2 )
		tmpFit.Draw("same")
		chi2Test = TLatex( 0.7, 0.8, '#splitline{#chi^{2}/ndF = '+ str( round( tmpFit.GetChisquare(), 2 ) )+'/'+str( int( tmpFit.GetNDF() ) )+'}{p0 = '+ str( round( tmpFit.GetParameter( 0 ), 2 ) ) +' #pm '+str(  round( tmpFit.GetParError( 0 ), 2 ) )+'}' )
		chi2Test.SetNDC()
		chi2Test.SetTextFont(42) ### 62 is bold, 42 is normal
		chi2Test.SetTextSize(0.10)
		chi2Test.Draw('same')

	if isinstance( ratio2, TH1 ):
		ratio2.SetFillStyle(3004)
		ratio2.SetFillColor( kRed )
		ratio2.Draw('same E2')
	line.Draw("same")

	outputFileName = nameInRoot+'_'+typePlot+'_'+args.grooming+'_QCD'+args.qcd+'_bkgShapeEstimationBoostedPlots'+args.version+'.'+args.extension
	if not 'simple' in args.binning: outputFileName = outputFileName.replace( typePlot, typePlot+'_ResoBasedBin' )
	print 'Processing.......', outputFileName
	can.SaveAs( 'Plots/'+ outputFileName )
	del can

	if reScale:
		canRatio = TCanvas('canRatio', 'canRatio',  10, 10, 750, 500 )
		if 'simple' in args.binning: tmpCanRatio = canRatio.DrawFrame(0,0,500,3)
		else: tmpCanRatio = canRatio.DrawFrame(0,0, boostedMassAveBins[-1] ,3)
		gStyle.SetOptFit(1)
		tmpCanRatio.SetXTitle( 'Average '+args.grooming+' mass [GeV]' )
		tmpCanRatio.SetYTitle( labelRatio )
		canRatio.Modified()
		ratio.Draw('ps')
		line.Draw("same")
		ratioP0 = TF1( 'ratioP0', 'pol0', 0, 500 )
		for i in range(2): ratio.Fit( ratioP0, 'MIR' )
		ratioP0.SetLineWidth(2)
		ratioP0.SetLineColor(kBlue)
		ratioP0.Draw("same")
		ratioP1 = TF1( 'ratioP1', 'pol1', 0, 500 )
		ratio1 = ratio.Clone()
		for i in range(2): ratio1.Fit( ratioP1, 'MIR' )
		ratio1.Draw("ps")
		ratioP1.SetLineWidth(2)
		ratioP1.SetLineColor(kViolet)
		ratioP1.Draw("same")
		canRatio.Update()
		st1 = ratio.GetListOfFunctions().FindObject("stats")
		st1.SetX1NDC(.15)
		st1.SetX2NDC(.35)
		st1.SetY1NDC(.76)
		st1.SetY2NDC(.91)
		st1.SetTextColor(kBlue)
		st2 = ratio1.GetListOfFunctions().FindObject("stats")
		st2.SetX1NDC(.35)
		st2.SetX2NDC(.55)
		st2.SetY1NDC(.76)
		st2.SetY2NDC(.91)
		st2.SetTextColor(kViolet)
		canRatio.Modified()
		outputFileNameRatio = nameInRoot+'_'+typePlot+'_Ratio_'+args.grooming+'_QCD'+args.qcd+'_bkgShapeEstimationBoostedPlots'+args.version+'.'+args.extension
		if not 'simple' in args.binning: outputFileNameRatio = outputFileNameRatio.replace( typePlot, typePlot+'_ResoBasedBin' )
		canRatio.SaveAs('Plots/'+outputFileNameRatio)
		del canRatio


		tdrStyle.SetPadRightMargin(0.05)
		tdrStyle.SetPadLeftMargin(0.15)
		canReScale = TCanvas('canReScale', 'canReScale',  10, 10, 750, 750 )
		pad1 = TPad("pad1", "Fit",0,0.207,1.00,1.00,-1)
		pad2 = TPad("pad2", "Pull",0,0.00,1.00,0.30,-1);
		pad1.Draw()
		pad2.Draw()

		pad1.cd()
		if log: 
			pad1.SetLogy() 	
			histo1.SetMaximum( 500 )
		else: 
			pad1.SetGrid()
			histo1.SetMaximum( 400 )
		if 'DATA' in labelh1: 
			histo1.SetMarkerStyle(8)
			histo1.Draw("PE")
		else: histo1.Draw("histe")
		#histo1UncBand = addSysBand( histo1, 1.10, kRed )
		#legend.AddEntry( histo1UncBand, 'Syst. unc.', 'f' )
		#histo1UncBand.Draw("same E2")
		reScaleFactor = ratioP0.GetParameter( 0 ) 
		histo2.Scale( reScaleFactor )
		histo2.Draw('hist E0 same')
		#histo2UncBand = addSysBand( histo2, 1.10, kBlue )
		#histo2UncBand.Draw("same E2")

		#locFirstBin = boostedMassAveBins.index( firstBinData )
		tmpHisto1 = histo1.Clone()
		tmpHisto2 = histo2.Clone()
		res = array( 'd', ( [ 0 ] * tmpHisto1.GetNbinsX() ) )
		chi2Ndf =  round( tmpHisto1.Chi2Test(tmpHisto2, 'WWCHI2/NDFP', res), 2 )
		chi2 =  round( tmpHisto1.Chi2Test(tmpHisto2, 'WWCHI2'), 2 )
		chi2Test = TLatex( 0.6, 0.7, '#chi^{2}/ndF Test = '+ str( chi2 )+'/'+str( round(chi2/chi2Ndf) ) )
		chi2Test.SetNDC()
	#	#chi2Test = TLatex( 209, 2000, '#chi^{2}/ndF Test = '+ str( round(hSRchi2,2) )+'/'+str( hSRndf ) )
		chi2Test.SetTextFont(42) ### 62 is bold, 42 is normal
		chi2Test.SetTextSize(0.04)
		chi2Test.Draw()

		if 'DATA' in labelh1: tmpLabel = 'DATA'
		else: tmpLabel = 'SR'
		numEvents = TLatex( 0.6, 0.62, '#splitline{events '+tmpLabel+'/ABCD Pred = }{'+ str( round( histo1.Integral(),2 ) )+'/'+str( round( histo2.Integral(),2 ) )+'}' )
		numEvents.SetNDC()
		numEvents.SetTextFont(42) ### 62 is bold, 42 is normal
		numEvents.SetTextSize(0.04)
		numEvents.Draw()

		CMS_lumi.extraText = ("Preliminary" if 'DATA' in labelh2 else "Simulation Preliminary")
		CMS_lumi.relPosX = 0.13
		CMS_lumi.CMS_lumi(pad1, 4, 0)
		legend.Draw()

		pad2.cd()
		pad2.SetGrid()
		pad2.SetTopMargin(0)
		pad2.SetBottomMargin(0.3)
		if 'simple' in args.binning: TMPPad2= pad2.DrawFrame(0,0,500,2)
		else: TMPPad2= pad2.DrawFrame(0,0,boostedMassAveBins[-1],2)
		TMPPad2.SetXTitle( 'Average '+args.grooming+' mass [GeV]' )
		TMPPad2.SetYTitle( labelRatio )
		TMPPad2.SetTitleSize(0.12, "x")
		TMPPad2.SetTitleSize(0.12, 'y')
		TMPPad2.SetLabelSize(0.12, 'x')
		TMPPad2.SetLabelSize(0.12, 'y')
		TMPPad2.SetTitleOffset(0.5, 'y')
		#TMPPad2.CenterXTitle()
		#TMPPad2.SetTitleOffset(0.55)
		TMPPad2.SetNdivisions(505, 'x' )
		TMPPad2.SetNdivisions(505, 'y' )
		pad2.Modified()
		
		none1, none2, none3, none3, newRatio = ratioPlots( histo1, histo2 ) 
		#labelAxis( nameInRoot, newRatio, args.grooming )
		#newRatio.GetXaxis().SetRangeUser( xmin, xmax )
		newRatio.SetMarkerStyle(8)
		newRatio.SetLineColor(kBlack)
		newRatio.GetYaxis().SetNdivisions(505)
		#if isinstance( newRatio, TGraphAsymmErrors ): newRatio.Draw('ap')
		newRatio.Draw('P')
		line.Draw("same")
		line11.Draw("same")
		line09.Draw("same")

		outputFileName = outputFileName.replace( typePlot, typePlot+'_reScale_' )
		if not 'simple' in args.binning: outputFileName = outputFileName.replace( typePlot, typePlot+'_ResoBasedBin' )
		print 'Processing.......', outputFileName
		canReScale.SaveAs( 'Plots/'+ outputFileName )
		del canReScale
	'''
	can = TCanvas('c1', 'c1',  10, 10, 750, 500 )
	gStyle.SetOptStat(1)
	pullGaus = TF1( 'pullGaus', 'gaus', -3, 3 )
	hRatiohSRhCRerrFullPulls.Fit( 'pullGaus', 'MIR' )
	hRatiohSRhCRerrFullPulls.GetXaxis().SetTitle('Pulls')
	hRatiohSRhCRerrFullPulls.GetYaxis().SetTitle('Bins')
	hRatiohSRhCRerrFullPulls.Draw('PE')
	#can.Update()
	#gStyle.SetStatY(0.91)
	#gStyle.SetStatX(0.95)
	#gStyle.SetStatW(0.15)
	#gStyle.SetStatH(0.30) 
	#print hRatiohSRhCRerrFullPulls.GetListOfFunctions().FindObject("stats")
#	st1.SetX1NDC(.12);
#	st1.SetX2NDC(.32);
#	st1.SetY1NDC(.76);
#	st1.SetY2NDC(.91);
#	#st1.SetTextColor(4);
	can.Modified()
	outputFileNamePulls= nameInRoot+'_Pulls_Bkg_'+Groom+'_QCD'+args.qcd+'_bkgShapeEstimationBoostedPlots'+args.version+'.'+args.extension
	can.SaveAs('Plots/'+outputFileNamePulls)
	'''
def tmpPlotBkgEstimation( dataFile, Groom, nameInRoot, xmin, xmax, rebinX, labX, labY, log, Norm=False ):
	"""docstring for tmpPlotBkgEstimation"""

	hData_A =  dataFile.Get( 'BoostedAnalysisPlots/'+nameInRoot+'_A' )
	hData_A.Rebin( rebinX )
	hData_B =  dataFile.Get( 'BoostedAnalysisPlots/'+nameInRoot+'_B' )
	hData_B.Rebin( rebinX )
	hData_C =  dataFile.Get( 'BoostedAnalysisPlots/'+nameInRoot+'_C' )
	hData_C.Rebin( rebinX )
	hData_D =  dataFile.Get( 'BoostedAnalysisPlots/'+nameInRoot+'_D' )
	hData_D.Rebin( rebinX )
	
	tmpBC = hData_B.Clone()
	tmpBC.Reset()
	tmpBC.Multiply( hData_B, hData_C, 1, 1, '')
	tmpBCD = hData_B.Clone()
	tmpBCD.Reset()
	tmpBCD.Divide( tmpBC, hData_D, 1, 1, '')

	tmphSignalCR = hData_A.Clone()
	tmphSignalCR.Reset()
	tmphSignalCR.Divide( hData_A, tmpBCD, 1., 1., '' )

	binWidth = hData_A.GetBinWidth(1)

	legend3=TLegend(0.55,0.75,0.90,0.87)
	legend3.SetFillStyle(0)
	legend3.SetTextSize(0.03)
	legend3.AddEntry( hData_A, 'DATA - SR' , 'l' )
	legend3.AddEntry( tmpBCD, 'DATA - ABCD Pred', 'pl' )

	hData_A.SetLineColor(kRed-4)
	hData_A.SetLineWidth(2)
	hData_A.GetYaxis().SetTitle('Events / '+str(binWidth))
	hData_A.GetXaxis().SetRangeUser( xmin, xmax )
	hData_A.SetMaximum( 1.2* max( hData_A.GetMaximum(), tmpBCD.GetMaximum() ) )
	tmpBCD.SetLineColor(kBlue)
	tmpBCD.SetLineWidth(2)
	tmpBCD.SetLineStyle(2)

	tdrStyle.SetPadRightMargin(0.05)
	tdrStyle.SetPadLeftMargin(0.15)
	can = TCanvas('c2', 'c2',  10, 10, 750, 750 )
	pad1 = TPad("pad1", "Fit",0,0.207,1.00,1.00,-1)
	pad2 = TPad("pad2", "Pull",0,0.00,1.00,0.30,-1);
	pad1.Draw()
	pad2.Draw()

	pad1.cd()
	pad1.SetGrid()
	#if log: pad1.SetLogy() 	
	hData_A.Draw("histe")
	tmpBCD.Draw('histe same')

	CMS_lumi.extraText = "Preliminary"
	CMS_lumi.relPosX = 0.13
	CMS_lumi.CMS_lumi(pad1, 4, 0)
	legend3.Draw()
	#if not (labX and labY): labels( name, '', '' )
	#labels( name1, '', '' ) #, labX, labY )

	pad2.cd()
	pad2.SetGrid()
	pad2.SetTopMargin(0)
	pad2.SetBottomMargin(0.3)
	
	labelAxis( nameInRoot, hData_A, Groom )
	tmphSignalCR.GetXaxis().SetRangeUser( xmin, xmax )
	tmphSignalCR.SetMarkerStyle(8)
	tmphSignalCR.GetXaxis().SetTitleOffset(1.1)
	tmphSignalCR.GetXaxis().SetLabelSize(0.12)
	tmphSignalCR.GetXaxis().SetTitleSize(0.12)
	tmphSignalCR.GetYaxis().SetTitle("SR/ABCD Pred")
	tmphSignalCR.GetYaxis().SetLabelSize(0.12)
	tmphSignalCR.GetYaxis().SetTitleSize(0.12)
	tmphSignalCR.GetYaxis().SetTitleOffset(0.55)
	tmphSignalCR.SetMaximum( 2. )
	tmphSignalCR.SetMinimum( 0. )
	tmphSignalCR.GetYaxis().SetNdivisions(505)
	tmphSignalCR.Draw()
	line.Draw("same")

	outputFileName = nameInRoot+'_BkgPlusRPVSt'+str(args.mass)+'_'+Groom+'_QCD'+args.qcd+'_bkgShapeEstimationBoostedPlots'+args.version+'.'+args.extension
	print 'Processing.......', outputFileName
	can.SaveAs( 'Plots/'+ outputFileName )
	del can

def plotSimpleBkgEstimation( rootFile, bkg, nameInRoot, xmin, xmax, rebinX, labX, labY, log, Norm=False ):
	"""docstring for plotSimpleBkgEstimation"""

	outputFileName = nameInRoot+'_'+bkg+'_pruned_bkgShapeEstimationBoostedPlots'+args.version+'.'+args.extension
	print 'Processing.......', outputFileName

	bkgHistos = OrderedDict()
	bkgHistos[ nameInRoot+'_'+bkg+'_A' ] = rootFile.Get( nameInRoot+'_'+bkg+'_A' )
	bkgHistos[ nameInRoot+'_'+bkg+'_B' ] = rootFile.Get( nameInRoot+'_'+bkg+'_B' )
	bkgHistos[ nameInRoot+'_'+bkg+'_C' ] = rootFile.Get( nameInRoot+'_'+bkg+'_C' )
	bkgHistos[ nameInRoot+'_'+bkg+'_D' ] = rootFile.Get( nameInRoot+'_'+bkg+'_D' )

	histoBC = bkgHistos[ nameInRoot+'_'+bkg+'_A' ].Clone()
	histoBC.Reset()
	histoBC.Multiply( bkgHistos[ nameInRoot+'_'+bkg+'_B' ], bkgHistos[ nameInRoot+'_'+bkg+'_C' ], 1, 1, '')
	histoBCD = bkgHistos[ nameInRoot+'_'+bkg+'_A' ].Clone()
	histoBCD.Reset()
	histoBCD.Divide( histoBC, bkgHistos[ nameInRoot+'_'+bkg+'_D' ], 1, 1, '')

	hRatiohBkg = ratioPlots( bkgHistos[ nameInRoot+'_'+bkg+'_A' ], histoBCD ) 
	makePlots( nameInRoot, bkgHistos[ nameInRoot+'_'+bkg+'_A' ], bkg+' SR', histoBCD, bkg+' MC ABCD Pred.', 5, xmin, xmax, hRatiohBkg, "MC SR/ABCD Pred", '', bkg+'Bkg_Log', True)




def plot2DBkgEstimation( rootFile, dataFile, sample, Groom, nameInRoot, titleXAxis, titleXAxis2, Xmin, Xmax, rebinx, Ymin, Ymax, rebiny, legX, legY ):
	"""docstring for plot"""

	outputFileName = nameInRoot+'_'+sample+'_'+Groom+'_bkgShapeEstimationBoostedPlots'+args.version+'.'+args.extension
	print 'Processing.......', outputFileName

	bkgHistos = OrderedDict()
	if isinstance(rootFile, dict):
		for bkg in rootFile:
			bkgHistos[ bkg+'_A' ] = Rebin2D( rootFile[ bkg ][0].Get( nameInRoot+'_'+bkg+'_A' ), rebinx, rebiny )
			bkgHistos[ bkg+'_B' ] = Rebin2D( rootFile[ bkg ][0].Get( nameInRoot+'_'+bkg+'_B' ), rebinx, rebiny )
			bkgHistos[ bkg+'_C' ] = Rebin2D( rootFile[ bkg ][0].Get( nameInRoot+'_'+bkg+'_C' ), rebinx, rebiny )
			bkgHistos[ bkg+'_D' ] = Rebin2D( rootFile[ bkg ][0].Get( nameInRoot+'_'+bkg+'_D' ), rebinx, rebiny )

		hBkg = bkgHistos[ bkg+'_B' ].Clone()
		hBkg.Reset()
		for samples in bkgHistos:
			print samples
			hBkg.Add( bkgHistos[ samples ].Clone() )
	else: 
		bkgHistos[ sample+'_A' ] = Rebin2D( rootFile.Get( nameInRoot+'_'+sample+'_A' ), rebinx, rebiny )
		bkgHistos[ sample+'_B' ] = Rebin2D( rootFile.Get( nameInRoot+'_'+sample+'_B' ), rebinx, rebiny )
		bkgHistos[ sample+'_C' ] = Rebin2D( rootFile.Get( nameInRoot+'_'+sample+'_C' ), rebinx, rebiny )
		bkgHistos[ sample+'_D' ] = Rebin2D( rootFile.Get( nameInRoot+'_'+sample+'_D' ), rebinx, rebiny )

		hBkg = bkgHistos[ sample+'_B' ].Clone()
		for samples in bkgHistos:
			if sample+'_B' not in samples: hBkg.Add( bkgHistos[ samples ].Clone() )

	if isinstance( dataFile, TFile ):

		bkgHistos[ 'DATA_A' ] = Rebin2D( dataFile.Get( nameInRoot+'_DATA_A' ), rebinx, rebiny )
		bkgHistos[ 'DATA_B' ] = Rebin2D( dataFile.Get( nameInRoot+'_DATA_B' ), rebinx, rebiny )
		bkgHistos[ 'DATA_C' ] = Rebin2D( dataFile.Get( nameInRoot+'_DATA_C' ), rebinx, rebiny )
		bkgHistos[ 'DATA_D' ] = Rebin2D( dataFile.Get( nameInRoot+'_DATA_D' ), rebinx, rebiny )

		bkgHistos[ 'DATA_A' ].Add( bkgHistos[ 'TTJets_A' ], -1 )
		bkgHistos[ 'DATA_B' ].Add( bkgHistos[ 'TTJets_B' ], -1 )
		bkgHistos[ 'DATA_C' ].Add( bkgHistos[ 'TTJets_C' ], -1 )
		bkgHistos[ 'DATA_D' ].Add( bkgHistos[ 'TTJets_D' ], -1 )

		bkgHistos[ 'DATA_A' ].Add( bkgHistos[ 'WJetsToQQ_A' ], -1 )
		bkgHistos[ 'DATA_B' ].Add( bkgHistos[ 'WJetsToQQ_B' ], -1 )
		bkgHistos[ 'DATA_C' ].Add( bkgHistos[ 'WJetsToQQ_C' ], -1 )
		bkgHistos[ 'DATA_D' ].Add( bkgHistos[ 'WJetsToQQ_D' ], -1 )

		hBkg = bkgHistos[ 'DATA_A' ].Clone()
		hBkg.Reset()
		for samples in bkgHistos:
			if '_A' not in samples: 
				if 'DATA' in samples: hBkg.Add( bkgHistos[ samples ].Clone() )

	if 'DATA' in sample: CMS_lumi.extraText = "Preliminary"
	else: CMS_lumi.extraText = "Simulation Preliminary"
	hBkg.GetXaxis().SetTitle( titleXAxis )
	hBkg.GetYaxis().SetTitleOffset( 0.9 )
	hBkg.GetYaxis().SetTitle( titleXAxis2 )
	corrFactor = hBkg.GetCorrelationFactor()
	textBox=TLatex()
	textBox.SetNDC()
	textBox.SetTextSize(0.05) 
	textBox.SetTextFont(62) ### 62 is bold, 42 is normal
	textBox.SetTextAlign(31)

	if (Xmax or Ymax):
		hBkg.GetXaxis().SetRangeUser( Xmin, Xmax )
		hBkg.GetYaxis().SetRangeUser( Ymin, Ymax )

	tdrStyle.SetPadRightMargin(0.12)
	hBkg.SetMaximum( 1500 )
	hBkg.SetMinimum( 0.01 )
	can = TCanvas('c3', 'c3',  750, 500 )
	can.SetLogz()
	hBkg.Draw('colz')
	textBox.DrawLatex(0.85, 0.85, ( 'M_{#tilde{t}} = '+args.mass+' GeV' if 'RPV' in sample else sample ) )
	textBox1 = textBox.Clone()
	textBox1.DrawLatex(0.85, 0.8, 'Corr. Factor = '+str(round(corrFactor,2)))
	textBox2 = textBox.Clone()
	textBox2.SetTextSize(0.12)
	textBox2.DrawLatex(0.27, 0.4, 'B  D')
	textBox3 = textBox.Clone()
	textBox3.SetTextSize(0.12)
	textBox3.DrawLatex(0.27, 0.25, 'A  C')

	xline = array('d', [0,1])
	yline = array('d', [1.5, 1.5])
	line = TGraph(2, xline, yline)
	line.SetLineColor(kBlack)
	line.SetLineWidth(5)
	line.Draw("same")
	xline2 = array('d', [0.1,0.1])
	yline2 = array('d', [0, 5])
	line2 = TGraph(2, xline2, yline2)
	line2.SetLineColor(kBlack)
	line2.SetLineWidth(5)
	line2.Draw("same")

	CMS_lumi.relPosX = 0.13
	CMS_lumi.CMS_lumi(can, 4, 0)

	can.SaveAs( 'Plots/'+outputFileName )
	#can.SaveAs( 'Plots/'+outputFileName.replace(''+ext, 'gif') )
	del can


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--proc', action='store', default='1D', help='Process to draw, example: 1D, 2D, MC.' )
	parser.add_argument('-d', '--decay', action='store', default='UDD312', dest='decay', help='Decay, example: UDD312, UDD323.' )
	parser.add_argument('-b', '--binning', action='store', default='simple', help='Binning: resoBased or simple' )
	parser.add_argument('-v', '--version', action='store', default='v05', help='Version: v01, v02.' )
	parser.add_argument('-t', '--miniTree', action='store_true', default=False, help='miniTree: if plots coming from miniTree or RUNAnalysis.' )
	parser.add_argument('-g', '--grooming', action='store', default='pruned', help='Grooming Algorithm, example: Pruned, Filtered.' )
	parser.add_argument('-m', '--mass', action='store', default='100', help='Mass of Stop, example: 100' )
	parser.add_argument('-q', '--qcd', action='store', default='Pt', dest='qcd', help='Type of QCD binning, example: HT.' )
	parser.add_argument('-l', '--lumi', action='store', type=float, default=1787, help='Luminosity, example: 1.' )
	parser.add_argument('-e', '--extension', action='store', default='png', help='Extension of plots.' )
	parser.add_argument('-B', '--bkgPlots', action='store_true', default=False, help='Binning: resoBased or simple' )
	parser.add_argument('-f', '--final', action='store_true', default=False, help='Final distributions.' )

	try:
		args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)
	
	CMS_lumi.lumi_13TeV = str( round( (args.lumi/1000.), 1 ) )+" fb^{-1}"
	
	if 'Pt' in args.qcd: 
		#bkgLabel='(w QCD pythia8)'
		QCDSF = 0.67 #( 0.86 if 'Puppi' in args.grooming else 0.89 ) 
	else: 
		#bkgLabel='(w QCD madgraphMLM+pythia8)'
		QCDSF = 1

	if args.miniTree: 
		filePrefix = 'Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming
		scale = 1
	else: 
		filePrefix = 'Rootfiles/RUNAnalysis' 
		scale = args.lumi

	bkgFiles = OrderedDict() 
	signalFiles = {}
	#dataFile = TFile.Open(filePrefix+'_DATA_'+args.version+'.root')
	dataFile = TFile.Open(filePrefix+'_JetHT_Run2016_V2p1_'+args.version+'.root')
	signalFiles[ args.mass ] = [ TFile.Open(filePrefix+'_RPVStopStopToJets_'+args.decay+'_M-'+args.mass+'_80X_V2p1_'+args.version+'.root'), scale, 'M_{#tilde{t}} = '+args.mass+' GeV', kRed]
	#signalFiles[ '80' ] = [ TFile.Open(filePrefix+'_RPVStopStopToJets_'+args.decay+'_M-80_80X_V2p1_'+args.version+'.root'), scale, 'M_{#tilde{t}} = 80 GeV', kRed]
	#signalFiles[ '170' ] = [ TFile.Open(filePrefix+'_RPVStopStopToJets_'+args.decay+'_M-170_80X_V2p1_'+args.version+'.root'), scale, 'M_{#tilde{t}} = 170 GeV', kMagenta]
	#signalFiles[ '240' ] = [ TFile.Open(filePrefix+'_RPVStopStopToJets_'+args.decay+'_M-240_80X_V2p1_'+args.version+'.root'), scale, 'M_{#tilde{t}} = 240 GeV', 28]
	bkgFiles[ 'TTJets' ] = [ TFile.Open(filePrefix+'_TTJets_80X_V2p1_'+args.version+'.root'), scale, 't #bar{t} + Jets', kGreen+2 ]
    	bkgFiles[ 'ZJetsToQQ' ] = [ TFile.Open(filePrefix+'_ZJetsToQQ_80X_V2p1_'+args.version+'.root'), scale, 'Z + Jets', kOrange]
    	bkgFiles[ 'WJetsToQQ' ] = [ TFile.Open(filePrefix+'_WJetsToQQ_80X_V2p1_'+args.version+'.root'), scale, 'W + Jets', 38]
	bkgFiles[ 'Dibosons' ] = [ TFile.Open(filePrefix+'_Dibosons_80X_V2p1_'+args.version+'.root'), scale, 'WW (had)', kMagenta+2 ]
	#bkgFiles[ 'WWTo4Q' ] = [ TFile.Open(filePrefix+'_WWTo4Q_80X_V2p1_'+args.version+'.root'), scale , 'WW (had)', kMagenta+2 ]
	#bkgFiles[ 'ZZTo4Q' ] = [ TFile.Open(filePrefix+'_ZZTo4Q_80X_V2p1_'+args.version+'.root'), scale, 'ZZ (had)', kOrange+2 ]
	#bkgFiles[ 'WZ' ] = [ TFile.Open(filePrefix+'_WZ_80X_V2p1_'+args.version+'.root'), scale, 'WZ', kCyan ]
	bkgFiles[ 'QCD'+args.qcd+'All' ] = [ TFile.Open(filePrefix+'_QCD'+args.qcd+'All_80X_V2p1_'+args.version+'.root'), QCDSF*scale, 'QCD', kBlue ]


	massMinX = 55
	massMaxX = 400
	jetMassHTlabY = 0.20
	jetMassHTlabX = 0.85

	if '2D' in args.proc: 
		#for bkg in bkgFiles: plot2DBkgEstimation( bkgFiles[ bkg ][0], bkg, args.grooming, 'prunedMassAsymVsdeltaEtaDijet', 'Mass Asymmetry', '| #eta_{j1} - #eta_{j2} |', 0, 1, 1, 0, 5, 1, jetMassHTlabX, jetMassHTlabY)
		plot2DBkgEstimation( dataFile, '', 'DATA', args.grooming, ('' if args.miniTree else 'BoostedAnalysisPlots/')+'prunedMassAsymVsdeltaEtaDijet', 'Mass Asymmetry', '| #eta_{j1} - #eta_{j2} |', 0, 1, 1, 0, 5, 1, jetMassHTlabX, jetMassHTlabY)
		#plot2DBkgEstimation( bkgFiles, dataFile, 'DATAMinusResBkg', args.grooming, 'prunedMassAsymVsdeltaEtaDijet', 'Mass Asymmetry', '| #eta_{j1} - #eta_{j2} |', 0, 1, 1, 0, 5, 1, jetMassHTlabX, jetMassHTlabY)
		#for bkg in bkgFiles: plot2DBkgEstimation( bkgFiles, bkg, args.grooming, 'prunedMassAsymVsdeltaEtaDijet', 'Mass Asymmetry', '| #eta_{j1} - #eta_{j2} |', 0, 1, 1, 0, 5, 1, jetMassHTlabX, jetMassHTlabY)
		#for bkg in signalFiles: plot2DBkgEstimation( signalFiles[ bkg ][0], 'RPVStopStopToJets_'+args.decay+'_M-'+str(args.mass), args.grooming, 'prunedMassAsymVsdeltaEtaDijet', 'Mass Asymmetry', '| #eta_{j1} - #eta_{j2} |', 0, 1, 1, 0, 5, 1, jetMassHTlabX, jetMassHTlabY)

	elif 'simple' in args.proc:
		for bkg in bkgFiles: 
			plotSimpleBkgEstimation( bkgFiles[ bkg ][0], bkg, 'massAve_jet2Tau21VsprunedMassAsym', massMinX, massMaxX, 5, '', '', False )
			plotSimpleBkgEstimation( bkgFiles[ bkg ][0], bkg, 'massAve_jet2Tau21VsdeltaEtaDijet', massMinX, massMaxX, 5, '', '', False )
			plotSimpleBkgEstimation( bkgFiles[ bkg ][0], bkg, 'massAve_prunedMassAsymVsdeltaEtaDijet', massMinX, massMaxX, 5, '', '', False )
		plotSimpleBkgEstimation( dataFile, 'DATA', 'massAve_jet2Tau21VsprunedMassAsym', massMinX, massMaxX, 5, '', '', False )
		plotSimpleBkgEstimation( dataFile, 'DATA', 'massAve_jet2Tau21VsdeltaEtaDijet', massMinX, massMaxX, 5, '', '', False )
		plotSimpleBkgEstimation( dataFile, 'DATA', 'massAve_prunedMassAsymVsdeltaEtaDijet', massMinX, massMaxX, 5, '', '', False )

	else: 
		tmpListCuts = selection[ ( 'CHSpruned' if 'pruned' in args.grooming else 'PUPPIsoftDrop' ) ][-2:]
		nameVarABCD = 'massAve_'+tmpListCuts[0][0]+'Vs'+tmpListCuts[1][0]
		plotBkgEstimation( dataFile, bkgFiles, signalFiles, args.grooming, nameVarABCD, massMinX, massMaxX, 5, '', '', False )
