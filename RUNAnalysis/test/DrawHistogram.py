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
	from RUNA.RUNAnalysis.scaleFactors import scaleFactor as SF
	from RUNA.RUNAnalysis.cuts import selection 
	import RUNA.RUNAnalysis.CMS_lumi as CMS_lumi 
	import RUNA.RUNAnalysis.tdrstyle as tdrstyle
except ImportError:
	sys.path.append('../python')
	from histoLabels import labels, labelAxis, finalLabels
	from scaleFactors import scaleFactor as SF
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

def plotSignalBkg( signalFiles, bkgFiles, Groom, nameInRoot, name, xmin, xmax, rebinX, labX, labY, log, PU, version, Norm=False ):
	"""docstring for plot"""

	outputFileName = name+'_'+Groom+'_'+args.decay+'RPVSt'+mass+'_PlusBkg_'+version+'AnalysisPlots.'+ext 
	print 'Processing.......', outputFileName

	legend=TLegend(0.60,0.60,0.90,0.87)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.04)

	signalHistos = {}
	binWidth = 0
	maxList = []
	if len(signalFiles) > 0:
		for sigSamples in signalFiles:
			#if 'mini' in process: signalHistos[ sigSamples ] = allHistosFile.Get( nameInRoot+'_RPVStopStopToJets_'+args.decay+'_M-'+str(mass) )
			#else: signalHistos[ sigSamples ] = signalFiles[ sigSamples ][0].Get( nameInRoot )
			signalHistos[ sigSamples ] = signalFiles[ sigSamples ][0].Get(  nameInRoot+'_RPVStopStopToJets_'+args.decay+'_M-'+str(mass))
			if rebinX > 1: signalHistos[ sigSamples ].Rebin( rebinX )
			if signalFiles[ sigSamples ][1] != 1: signalHistos[ sigSamples ].Scale( signalFiles[ sigSamples ][1] ) 
			legend.AddEntry( signalHistos[ sigSamples ], signalFiles[ sigSamples ][2], 'l' if Norm else 'f' )
			if Norm:
				signalHistos[ sigSamples ].SetLineColor( signalFiles[ sigSamples ][3] )
				signalHistos[ sigSamples ].SetLineWidth( 3 )
				signalHistos[ sigSamples ].Scale( 1 / signalHistos[ sigSamples ].Integral() )
				maxList.append( signalHistos[ sigSamples ].GetMaximum() )
			else:
				signalHistos[ sigSamples ].SetFillStyle( 1001 )
				signalHistos[ sigSamples ].SetFillColor( signalFiles[ sigSamples ][3] )
			binWidth = signalHistos[ sigSamples ].GetBinWidth( 1 )

	dummy = 0
	bkgHistos = OrderedDict()
	if len(bkgFiles) > 0:
		for bkgSamples in bkgFiles:
			dummy += 1
			#if 'mini' in process: bkgHistos[ bkgSamples ] = allHistosFile.Get( nameInRoot+'_'+bkgSamples )
			#else: bkgHistos[ bkgSamples ] = bkgFiles[ bkgSamples ][0].Get( nameInRoot )
			bkgHistos[ bkgSamples ] = bkgFiles[ bkgSamples ][0].Get( nameInRoot+'_'+bkgSamples )
			if rebinX > 1: bkgHistos[ bkgSamples ].Rebin( rebinX )
			if bkgFiles[ bkgSamples ][1] != 1: bkgHistos[ bkgSamples ].Scale( bkgFiles[ bkgSamples ][1] ) 
			legend.AddEntry( bkgHistos[ bkgSamples ], bkgFiles[ bkgSamples ][2], 'l' if Norm else 'f' )
			if Norm:
				bkgHistos[ bkgSamples ].SetLineColor( bkgFiles[ bkgSamples ][3] )
				bkgHistos[ bkgSamples ].SetLineWidth( 3 )
				bkgHistos[ bkgSamples ].SetLineStyle( 2 )
				bkgHistos[ bkgSamples ].Scale( 1 / bkgHistos[ bkgSamples ].Integral() )
				maxList.append( bkgHistos[ bkgSamples ].GetMaximum() )
			else:
				bkgHistos[ bkgSamples ].SetFillStyle( 1001 )
				bkgHistos[ bkgSamples ].SetFillColor( bkgFiles[ bkgSamples ][3] )
		

	CMS_lumi.extraText = "Preliminary Simulation"
	try: hBkg = bkgHistos[ 'QCDHTAll' ].Clone()
	except KeyError: hBkg = bkgHistos[ 'QCDPtAll' ].Clone()
	for samples in bkgHistos:
		if 'QCD' not in samples: hBkg.Add( bkgHistos[ samples ].Clone() )

	if not Norm:
		stackHisto = THStack('stackHisto', 'stack')
		for BkgSamples in bkgHistos: stackHisto.Add( bkgHistos[ BkgSamples ] )
		for SigSamples in signalHistos: stackHisto.Add( signalHistos[ SigSamples ] )

  		tdrStyle.SetPadRightMargin(0.05)
  		tdrStyle.SetPadLeftMargin(0.15)
		can = TCanvas('c1', 'c1',  10, 10, 750, 750 )
		pad1 = TPad("pad1", "Fit",0,0.207,1.00,1.00,-1)
		pad2 = TPad("pad2", "Pull",0,0.00,1.00,0.30,-1);
		pad1.Draw()
		pad2.Draw()

		pad1.cd()
		if log: pad1.SetLogy()
		#stackHisto.SetMinimum(10)
		stackHisto.Draw('hist')
		#stackHisto.GetYaxis().SetTitleOffset(1.2)
		if xmax: stackHisto.GetXaxis().SetRangeUser( xmin, xmax )

		tmpHisto = signalHistos[ 'Signal' ].Clone()
		tmpHisto.SetLineColor(kRed-4)
		tmpHisto.SetFillColor(0)
		tmpHisto.SetLineWidth(3)
		tmpHisto.SetLineStyle(2)
		tmpHisto.Draw("hist same")
		stackHisto.GetYaxis().SetTitle( 'Events / '+str(binWidth) )

		CMS_lumi.relPosX = 0.14
		CMS_lumi.CMS_lumi(pad1, 4, 0)
		legend.Draw()
		if not (labX and labY): 
			if 'mini' in process: finalLabels( 'RPVStopStopToJets_'+args.decay+'_M-'+str(mass) ) 
			else: labels( name, PU, camp )
		else: 
			if 'mini' in process: finalLabels( 'RPVStopStopToJets_'+args.decay+'_M-'+str(mass), labX, labY ) 
			else: labels( name, PU, camp, labX, labY )

		pad2.cd()
		pad2.SetGrid()
		pad2.SetTopMargin(0)
		pad2.SetBottomMargin(0.3)
		
		hSignal = signalHistos[ 'Signal' ].Clone()
		#hSignalBkg = signalHistos[ 'Signal' ].Clone()
		#hSignalBkg.Add( hBkg )
		#hSignal.Divide( hSignalBkg )

		hSignal.Reset()
		for ibin in range(0, hSignal.GetNbinsX()):
			binContSignal = signalHistos[ 'Signal' ].GetBinContent(ibin)
			binContBkg = hBkg.GetBinContent(ibin)
			try: value = binContSignal / TMath.Sqrt( binContSignal + binContBkg )
			#try: value = binContSignal / ( binContSignal + binContBkg )
			except ZeroDivisionError: continue
			hSignal.SetBinContent( ibin, value )
		
		labelAxis( name, hSignal, Groom )
		hSignal.GetYaxis().SetTitleOffset(1.2)
		hSignal.GetXaxis().SetLabelSize(0.12)
		hSignal.GetXaxis().SetTitleSize(0.12)
		#hSignal.GetYaxis().SetTitle("S / B")
		hSignal.GetYaxis().SetTitle("S / #sqrt{S+B}")
		hSignal.GetYaxis().SetLabelSize(0.12)
		hSignal.GetYaxis().SetTitleSize(0.12)
		hSignal.GetYaxis().SetTitleOffset(0.45)
		hSignal.GetYaxis().CenterTitle()
		#hSignal.SetMaximum(0.7)
		if xmax: hSignal.GetXaxis().SetRangeUser( xmin, xmax )
		hSignal.Draw("hist")

		can.SaveAs( 'Plots/'+outputFileName )
		del can

	else:

  		tdrStyle.SetPadRightMargin(0.05)
		can = TCanvas('c1', 'c1', 750, 500 )
		if log: can.SetLogy()
		signalHistos['Signal'].GetYaxis().SetTitleOffset(1.0)
		signalHistos['Signal'].GetYaxis().SetTitle( 'Normalized / '+str(binWidth) )
		if xmax: signalHistos['Signal'].GetXaxis().SetRangeUser( xmin, xmax )
		labelAxis( name, signalHistos['Signal'], Groom )
		signalHistos['Signal'].Draw('hist')
		for bkgSamples in bkgHistos: bkgHistos[ bkgSamples ].Draw('hist same')
		signalHistos['Signal'].SetMaximum( 1.1 * max( maxList ) )

		CMS_lumi.lumi_13TeV = ''
		CMS_lumi.relPosX = 0.14
		CMS_lumi.CMS_lumi(can, 4, 0)
		legend.Draw()
		if not (labX and labY): labels( '', PU, camp )
		else: labels( '', PU, camp, labX, labY )

		can.SaveAs( 'Plots/'+outputFileName )
		del can

def plot2DSignalBkg( bkgFiles, Groom, nameInRoot, name, titleXAxis, titleXAxis2, Xmin, Xmax, rebinx, Ymin, Ymax, rebiny, legX, legY, PU, version ):
	"""docstring for plot"""

	outputFileName = name+'_'+Groom+'_'+args.decay+'RPVSt'+mass+'_QCD'+qcd+'_PlusBkg_'+version+'AnalysisPlots.'+ext 
	print 'Processing.......', outputFileName

	bkgHistos = OrderedDict()
	tmpText = ''
	if len(bkgFiles) > 0:
		for bkgSamples in bkgFiles:
			tmpText = bkgSamples
			bkgHistos[ bkgSamples ] =  bkgFiles[ bkgSamples ][0].Get( nameInRoot+'_'+bkgSamples+'_Bkg' )
			bkgHistos[ bkgSamples ] = Rebin2D( bkgHistos[ bkgSamples ], rebinx, rebiny )
			if bkgFiles[ bkgSamples ][1] != 1: bkgHistos[ bkgSamples ].Scale( bkgFiles[ bkgSamples ][1] ) 

	CMS_lumi.extraText = "Preliminary Simulation"
	if 'QCD' in tmpText: 
		hBkg = bkgHistos[ 'QCDHT500to700' ].Clone()
		for samples in bkgHistos:
			if 'QCDHT500to700' not in samples: hBkg.Add( bkgHistos[ samples ].Clone() )
	else: hBkg = bkgHistos[ tmpText ].Clone()

	hBkg.GetXaxis().SetTitle( titleXAxis )
	hBkg.GetYaxis().SetTitleOffset( 0.9 )
	hBkg.GetYaxis().SetTitle( titleXAxis2 )

	if (Xmax or Ymax):
		hBkg.GetXaxis().SetRangeUser( Xmin, Xmax )
		hBkg.GetYaxis().SetRangeUser( Ymin, Ymax )

	tdrStyle.SetPadRightMargin(0.12)
	can = TCanvas('c1', 'c1',  750, 500 )
	can.SetLogz()
	hBkg.Draw('colz')

	CMS_lumi.extraText = "Preliminary Simulation"
	CMS_lumi.relPosX = 0.13
	CMS_lumi.CMS_lumi(can, 4, 0)
	if not (legX and legY): labels( name, PU, camp )
	else: labels( name, PU, camp, legX, legY )

	can.SaveAs( 'Plots/'+outputFileName )
	#can.SaveAs( 'Plots/'+outputFileName.replace(''+ext, 'gif') )
	del can

def Rebin2D( h1, rebinx, rebiny ):
	"""docstring for Rebin2D"""

	tmph1 = h1.Clone()
	nbinsx = h1.GetXaxis().GetNbins()
	nbinsy = h1.GetYaxis().GetNbins()
	xmin  = h1.GetXaxis().GetXmin()
	xmax  = h1.GetXaxis().GetXmax()
	ymin  = h1.GetYaxis().GetXmin()
	ymax  = h1.GetYaxis().GetXmax()
	nx = nbinsx/rebinx
	ny = nbinsy/rebiny
	h1.SetBins( nx, xmin, xmax, ny, ymin, ymax )

	for biny in range( 1, nbinsy):
		for binx in range(1, nbinsx):
			ibin1 = h1.GetBin(binx,biny)
			h1.SetBinContent( ibin1, 0 )
		
	for biny in range( 1, nbinsy):
		by = tmph1.GetYaxis().GetBinCenter( biny )
		iy = h1.GetYaxis().FindBin(by)
		for binx in range(1, nbinsx):
			bx = tmph1.GetXaxis().GetBinCenter(binx)
			ix  = h1.GetXaxis().FindBin(bx)
			bin = tmph1.GetBin(binx,biny)
			ibin= h1.GetBin(ix,iy)
			cu  = tmph1.GetBinContent(bin)
			h1.AddBinContent(ibin,cu)
	return h1

def plot2D( inFiles, sample, Groom, nameInRoot, name, titleXAxis, titleXAxis2, Xmin, Xmax, rebinx, Ymin, Ymax, rebiny, legX, legY, PU, version ):
	"""docstring for plot"""

	outputFileName = name+'_'+Groom+'_'+sample+'_'+camp+'_'+PU+'_'+version+'AnalysisPlots.'+ext 
	print 'Processing.......', outputFileName
	for samples in inFiles:
		h1 = inFiles[ samples ][0].Get( nameInRoot )
	#h1 = inFile.Get( 'AnalysisPlots'+Groom+'/'+name )
	#h1 = inFile.Get( 'TriggerEfficiency'+Groom+'/'+name )
	tmph1 = h1.Clone()
	
	### Rebinning
	nbinsx = h1.GetXaxis().GetNbins()
	nbinsy = h1.GetYaxis().GetNbins()
	xmin  = h1.GetXaxis().GetXmin()
	xmax  = h1.GetXaxis().GetXmax()
	ymin  = h1.GetYaxis().GetXmin()
	ymax  = h1.GetYaxis().GetXmax()
	nx = nbinsx/rebinx
	ny = nbinsy/rebiny
	h1.SetBins( nx, xmin, xmax, ny, ymin, ymax )

	for biny in range( 1, nbinsy):
		for binx in range(1, nbinsx):
			ibin1 = h1.GetBin(binx,biny)
			h1.SetBinContent( ibin1, 0 )
		
	for biny in range( 1, nbinsy):
		by = tmph1.GetYaxis().GetBinCenter( biny )
		iy = h1.GetYaxis().FindBin(by)
		for binx in range(1, nbinsx):
			bx = tmph1.GetXaxis().GetBinCenter(binx)
			ix  = h1.GetXaxis().FindBin(bx)
			bin = tmph1.GetBin(binx,biny)
			ibin= h1.GetBin(ix,iy)
			cu  = tmph1.GetBinContent(bin)
			h1.AddBinContent(ibin,cu)

	h1.Scale( inFiles[ samples ][1] )
	h1.GetXaxis().SetTitle( titleXAxis )
	h1.GetYaxis().SetTitleOffset( 1.0 )
	h1.GetYaxis().SetTitle( titleXAxis2 )

	if (Xmax or Ymax):
		h1.GetXaxis().SetRangeUser( Xmin, Xmax )
		h1.GetYaxis().SetRangeUser( Ymin, Ymax )

	tdrStyle.SetPadRightMargin(0.12)
	can = TCanvas('c1', 'c1',  750, 500 )
	can.SetLogz()
	if 'Boosted' in version: h1.SetMaximum(5000)
	h1.Draw('colz')

	CMS_lumi.extraText = "Preliminary Simulation"
	CMS_lumi.relPosX = 0.13
	CMS_lumi.CMS_lumi(can, 4, 0)
	if not (legX and legY): labels( name, PU, camp )
	else: labels( name, PU, camp, legX, legY )

	can.SaveAs( 'Plots/'+outputFileName )
	#can.SaveAs( 'Plots/'+outputFileName.replace(''+ext, 'gif') )
	del can


def plotCutFlow( signalFiles, bkgFiles, Groom, name, xmax, log, PU, Norm=False ):
	"""docstring for plot"""

	outputFileName = name+'_'+Groom+'_'+args.decay+'RPVSt'+mass+'_'+PU+'_Bkg_AnalysisPlots.'+ext 
	print 'Processing.......', outputFileName

	histos = {}
	if len(signalFiles) > 0:
		for samples in signalFiles:
			histos[ samples ] = signalFiles[ samples ][0].Get(name+'_RPVStopStopToJets_'+args.decay+'_M-'+str(mass))
			if signalFiles[ samples ][1] != 1: histos[ samples ].Scale( signalFiles[ samples ][1] ) 

	dummy = 0
	if len(bkgFiles) > 0:
		for samples in bkgFiles:
			dummy += 1
			histos[ samples ] = bkgFiles[ samples ][0].Get(name+'_'+samples)
			if bkgFiles[ samples ][1] != 1: histos[ samples ].Scale( bkgFiles[ samples ][1] ) 
			if (dummy == 1): hBkg = histos[ samples ].Clone()

	hSignal = histos[ 'Signal' ].Clone()
	hQCD = histos[ 'QCD'+qcd+'All' ].Clone()
	hTTJets = histos[ 'TTJets' ].Clone()
	hWJetsToQQ = histos[ 'WJetsToQQ' ].Clone()
	hWWTo4Q = histos[ 'WWTo4Q' ].Clone()
	#hZJets = histos[ 'ZJets' ].Clone()
	hZZTo4Q = histos[ 'ZZTo4Q' ].Clone()
	hWZ = histos[ 'WZ' ].Clone()

	for bin in range(0,  hSignal.GetNbinsX()):
		hSignal.SetBinContent(bin, 0.)
		hSignal.SetBinError(bin, 0.)
		hQCD.SetBinContent(bin, 0.)
		hQCD.SetBinError(bin, 0.)
		hTTJets.SetBinContent(bin, 0.)
		hTTJets.SetBinError(bin, 0.)
		hWJetsToQQ.SetBinContent(bin, 0.)
		hWJetsToQQ.SetBinError(bin, 0.)
		hWWTo4Q.SetBinContent(bin, 0.)
		hWWTo4Q.SetBinError(bin, 0.)
		#hZJets.SetBinContent(bin, 0.)
		#hZJets.SetBinError(bin, 0.)
		hZZTo4Q.SetBinContent(bin, 0.)
		hZZTo4Q.SetBinError(bin, 0.)
		hWZ.SetBinContent(bin, 0.)
		hWZ.SetBinError(bin, 0.)
	
	totalEventsSignal = histos[ 'Signal' ].GetBinContent(1)
	totalEventsQCD = histos[ 'QCD'+qcd+'All' ].GetBinContent(1)
	totalEventsTTJets = histos[ 'TTJets' ].GetBinContent(1)
	totalEventsWJetsToQQ = histos[ 'WJetsToQQ' ].GetBinContent(1)
	totalEventsWWTo4Q = histos[ 'WWTo4Q' ].GetBinContent(1)
	#totalEventsZJets = histos[ 'ZJets' ].GetBinContent(1)
	totalEventsZZTo4Q = histos[ 'ZZTo4Q' ].GetBinContent(1)
	totalEventsWZ = histos[ 'WZ' ].GetBinContent(1)
	#print totalEventsSignal, totalEventsQCD

	cutFlowSignalList = []
	cutFlowQCDList = []
	cutFlowTTJetsList = []
	cutFlowWJetsToQQList = []
	cutFlowWWTo4QList = []
	#cutFlowZJetsList = []
	cutFlowZZTo4QList = []
	cutFlowWZList = []

	for ibin in range(0, hQCD.GetNbinsX()+1):
	
		cutFlowSignalList.append( histos[ 'Signal' ].GetBinContent(ibin) )
		cutFlowQCDList.append( histos[ 'QCD'+qcd+'All' ].GetBinContent(ibin) )
		cutFlowTTJetsList.append( histos[ 'TTJets' ].GetBinContent(ibin) )
		cutFlowWJetsToQQList.append( histos[ 'WJetsToQQ' ].GetBinContent(ibin) )
		cutFlowWWTo4QList.append( histos[ 'WWTo4Q' ].GetBinContent(ibin) )
		#cutFlowZJetsList.append( histos[ 'ZJets' ].GetBinContent(ibin) )
		cutFlowZZTo4QList.append( histos[ 'ZZTo4Q' ].GetBinContent(ibin) )
		cutFlowWZList.append( histos[ 'WZ' ].GetBinContent(ibin) )

		hSignal.SetBinContent( ibin , histos[ 'Signal' ].GetBinContent(ibin) / totalEventsSignal )
		hQCD.SetBinContent( ibin , histos[ 'QCD'+qcd+'All' ].GetBinContent(ibin) / totalEventsQCD )
		hTTJets.SetBinContent( ibin , histos[ 'TTJets' ].GetBinContent(ibin) / totalEventsTTJets )
		hWJetsToQQ.SetBinContent( ibin , histos[ 'WJetsToQQ' ].GetBinContent(ibin) / totalEventsWJetsToQQ )
		hWWTo4Q.SetBinContent( ibin , histos[ 'WWTo4Q' ].GetBinContent(ibin) / totalEventsWWTo4Q )
		#hZJets.SetBinContent( ibin , histos[ 'ZJets' ].GetBinContent(ibin) / totalEventsZJets )
		hZZTo4Q.SetBinContent( ibin , histos[ 'ZZTo4Q' ].GetBinContent(ibin) / totalEventsZZTo4Q )
		hWZ.SetBinContent( ibin , histos[ 'WZ' ].GetBinContent(ibin) / totalEventsWZ )
		
	hSB = hSignal.Clone()
	hBkg = hQCD.Clone()
	hBkg.Add( hTTJets )
	hBkg.Add( hWJetsToQQ )
	hBkg.Add( hWWTo4Q )
	#hBkg.Add( hZJets )
	hBkg.Add( hZZTo4Q )
	hBkg.Add( hWZ )
	hSB.Divide( hBkg )
	hSB.GetXaxis().SetBinLabel( ibin, '')
	print "Signal", cutFlowSignalList
	print "QCD", cutFlowQCDList
	print "TTJets", cutFlowTTJetsList
	print "WJetsToQQ", cutFlowWJetsToQQList
	print "WWTo4Q", cutFlowWWTo4QList
	#print "ZJets", cutFlowZJetsList
	print "ZZTo4Q", cutFlowZZTo4QList
	print "WZ", cutFlowWZList
	#print 'total', [ cutFlowQCDList[i] + cutFlowTTJetsList[i] +cutFlowWJetsToQQList[i] + cutFlowWWTo4QList[i] + cutFlowZJetsList[i] + cutFlowZZTo4QList[i] + cutFlowWZList[i]  for i in range(len(cutFlowQCDList))]
	print 'total', [ cutFlowQCDList[i] + cutFlowTTJetsList[i] +cutFlowWJetsToQQList[i] + cutFlowWWTo4QList[i] + cutFlowZZTo4QList[i] + cutFlowWZList[i]  for i in range(len(cutFlowQCDList))]

	#hSB = hSignal.Clone()
	#hSB.Divide( hQCD )

	binWidth = histos['Signal'].GetBinWidth(1)

	legend=TLegend(0.60,0.67,0.90,0.87)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.03)

	hSignal.SetLineWidth(2)
	hSignal.SetLineColor(kRed-4)
	hQCD.SetLineWidth(2)
	hQCD.SetLineColor(kBlue-4)
	hTTJets.SetLineWidth(2)
	hTTJets.SetLineColor(kGreen-4)
	hWJetsToQQ.SetLineWidth(2)
	hWJetsToQQ.SetLineColor(kMagenta-4)
	hWWTo4Q.SetLineWidth(2)
	hWWTo4Q.SetLineColor(kMagenta-6)
	#hZJets.SetLineWidth(2)
	#hZJets.SetLineColor(kOrange-4)
	hZZTo4Q.SetLineWidth(2)
	hZZTo4Q.SetLineColor(kMagenta-6)

	can = TCanvas('c1', 'c1',  10, 10, 750, 750 )
	pad1 = TPad("pad1", "Fit",0,0.20,1.00,1.00,-1)
	pad2 = TPad("pad2", "Pull",0,0.00,1.00,0.30,-1);
	pad1.Draw()
	pad2.Draw()

	pad1.cd()
	if log: 
		pad1.SetLogy()
		outName = outputFileName.replace('_AnalysisPlots','_Log_AnalysisPlots')
		hSignal.GetYaxis().SetTitleOffset(0.9)
	else:
		outName = outputFileName 

	pad1.SetGridx()
	legend.AddEntry( hSignal, args.decay+'RPV #tilde{t} '+mass+' GeV' , 'l' )
	legend.AddEntry( hQCD, 'QCD', 'l' )
	legend.AddEntry( hTTJets, 't #bar{t} + Jets' , 'l' )
	legend.AddEntry( hWJetsToQQ, 'W + Jets' , 'l' )
	legend.AddEntry( hWWTo4Q, 'WW (had)' , 'l' )
	#legend.AddEntry( hZJets, 'Z + Jets' , 'l' )
	legend.AddEntry( hZZTo4Q, 'ZZ (had)' , 'l' )
	hSignal.GetYaxis().SetTitle( 'Percentage / '+str(binWidth) )
	hSignal.GetXaxis().SetRangeUser( 1, xmax )

	hSignal.SetMinimum(0.0001)
	hSignal.Draw()
	hQCD.Draw('same')
	hTTJets.Draw('same')
	hWJetsToQQ.Draw('same')
	hWWTo4Q.Draw('same')
	#hZJets.Draw('same')
	hZZTo4Q.Draw('same')

	legend.Draw()
	CMS_lumi.relPosX = 0.14
	CMS_lumi.CMS_lumi(pad1, 4, 0)
	#labels( name, '', '', '' )

	pad2.cd()
	pad2.SetGrid()
	pad2.SetTopMargin(0)
	pad2.SetBottomMargin(0.3)
	hSB.GetYaxis().SetTitle("S / B")
	hSB.GetYaxis().SetLabelSize(0.12)
	hSB.GetXaxis().SetLabelSize(0.12)
	hSB.GetYaxis().SetTitleSize(0.12)
	hSB.GetXaxis().SetTitleSize(0.12)
	hSB.GetYaxis().SetTitleOffset(0.45)
	#hSB.SetMaximum(0.7)
	hSB.GetXaxis().SetRangeUser( 1, xmax )
	hSB.Sumw2()
	hSB.Draw("hist")

	can.SaveAs( 'Plots/'+outName )
	del can

def plotSimple( inFile, sample, Groom, name, xmax, labX, labY, log, PU, Norm=False ):
	"""docstring for plot"""

	outputFileName = name+'_'+sample+'_AnalysisPlots.'+ext 
	print 'Processing.......', outputFileName

	histo = inFile.Get( version+'AnalysisPlots'+Groom+'/'+name )

#	histos.values()[0].SetMaximum( 2* max( listMax ) ) 
#	histos.values()[0].GetXaxis().SetRangeUser( 0, xmax )
	binWidth = histo.GetBinWidth(1)

	legend=TLegend(0.60,0.75,0.90,0.90)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.03)

	#histo.SetFillColor(48)
	histo.SetFillStyle(1001)

	tdrStyle.SetPadRightMargin(0.05)
	can = TCanvas('c1', 'c1',  10, 10, 750, 500 )

	if log: 
		can.SetLogy()
		outName = outputFileName.replace('_AnalysisPlots','_Log_AnalysisPlots')
	else:
		outName = outputFileName 

	legend.AddEntry( histo, sample, 'f' )
	histo.GetYaxis().SetTitleOffset(0.90)
	histo.Draw('hist')
	histo.GetYaxis().SetTitle( 'Events / '+str(binWidth) )

	labelAxis( name, histo, '' )
	legend.Draw()
	if not (labX and labY): labels( '', sample, PU )
	else: labels( '', 'MC Truth', PU, labX, labY )
	can.SaveAs( 'Plots/'+outName )
	del can

def plotDiffSample( inFileSample1, inFileSample2, sample1, sample2, Groom, name, xmax, labX, labY, log, Diff , Norm=False):
	"""docstring for plot"""

	outputFileName = name+'_'+Groom+'_'+args.decay+'RPVSt'+mass+'_Diff'+Diff+'.'+ext 
	print 'Processing.......', outputFileName

	histos = {}
	histos[ 'Sample1' ] = inFileSample1.Get( version+'AnalysisPlots'+Groom+'/'+name )
	histos[ 'Sample2' ] = inFileSample2.Get( version+'AnalysisPlots'+Groom+'/'+name )

	hSample1 = histos[ 'Sample2' ].Clone()
	hSample2 = histos[ 'Sample1' ].Clone()
	hSample1.Divide( hSample2 )

	binWidth = histos['Sample1'].GetBinWidth(1)

	legend=TLegend(0.60,0.75,0.90,0.90)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.03)

	if not Norm:
		histos[ 'Sample1' ].SetLineWidth(2)
		histos[ 'Sample1' ].SetLineColor(48)
		histos[ 'Sample2' ].SetLineColor(38)
		histos[ 'Sample2' ].SetLineWidth(2)
		#histos[ 'Sample1' ].SetMaximum( 1.2* max( histos[ 'Sample1' ].GetMaximum(), histos[ 'Sample2' ].GetMaximum() ) ) 
		#histos.values()[0].GetXaxis().SetRangeUser( 0, xmax )

		can = TCanvas('c1', 'c1',  10, 10, 750, 750 )
		pad1 = TPad("pad1", "Fit",0,0.25,1.00,1.00,-1)
		pad2 = TPad("pad2", "Pull",0,0.00,1.00,0.25,-1);
		pad1.Draw()
		pad2.Draw()

		pad1.cd()
		if log: 
			pad1.SetLogy()
			outName = outputFileName.replace('_Diff','_Log_Diff')
		else:
			outName = outputFileName 

		legend.AddEntry( histos[ 'Sample1' ], sample1, 'l' )
		legend.AddEntry( histos[ 'Sample2' ], sample2, 'l' )
		histos['Sample1'].SetMinimum(10)
		histos['Sample1'].Draw('hist')
		histos['Sample1'].GetYaxis().SetTitleOffset(1.2)
		histos['Sample2'].Draw('hist same')
		histos['Sample1'].GetYaxis().SetTitle( 'Events / '+str(binWidth) )

		labelAxis( name, histos['Sample1'], Groom )
		legend.Draw()
		if not (labX and labY): labels( name, '13 TeV - Scaled to '+lumi+' fb^{-1}', '' )
		else: labels( name, '13 TeV - Scaled to '+lumi+' fb^{-1}', '', labX, labY )

		pad2.cd()
		hSample1.SetLineColor(48)
		#hSample1.SetFillStyle(1001)
		hSample1.GetYaxis().SetTitle("Ratio")
		hSample1.GetYaxis().SetLabelSize(0.12)
		hSample1.GetXaxis().SetLabelSize(0.12)
		hSample1.GetYaxis().SetTitleSize(0.12)
		hSample1.GetYaxis().SetTitleOffset(0.45)
		#hSample1.SetMaximum(1.0)
		hSample1.Sumw2()
		hSample1.Draw("histe")

		can.SaveAs( 'Plots/'+outName )
		del can
	else:
		histos[ 'Sample1' ].SetLineWidth(2)
		histos[ 'Sample1' ].SetLineColor(48)
		histos[ 'Sample2' ].SetLineColor(38)
		histos[ 'Sample2' ].SetLineWidth(2)

		can = TCanvas('c1', 'c1',  10, 10, 750, 500 )
		if log: 
			can.SetLogy()
			outName = outputFileName.replace('_Diff','_Log_Norm_Diff')
			histos[ 'Sample1' ].GetYaxis().SetTitleOffset(1.2)
		else:
			outName = outputFileName.replace('_Diff','_Norm_Diff')

		legend.AddEntry( histos[ 'Sample1' ], sample1 , 'l' )
		legend.AddEntry( histos[ 'Sample2' ], sample2 , 'l' )
		histos['Sample1'].GetYaxis().SetTitle( 'Normalized / '+str(binWidth) )

		histos['Sample1'].DrawNormalized()
		histos['Sample2'].DrawNormalized('same')

		legend.Draw()
		labelAxis( name, histos['Sample1'], Groom )
		if not (labX and labY): labels( name, '13 TeV - Scaled to '+lumi+' fb^{-1}', '' )
		else: labels( name, '13 TeV - Scaled to '+lumi+' fb^{-1}', '', labX, labY )

		can.SaveAs( 'Plots/'+outName )
		del can


def plotQuality( dataFile, bkgFiles, Groom, nameInRoot, name, xmin, xmax, rebinX, labX, labY, log, PU, version ):
	"""docstring for plot"""

	outputFileName = name+'_'+Groom+'_'+PU+'_QCD'+qcd+'_dataQuality'+version+'Plots.'+ext
	print 'Processing.......', outputFileName

	histos = {}
	histos[ 'Data' ] = dataFile.Get( nameInRoot+'_DATA' if 'qual' in process else nameInRoot )
	if rebinX > 1: histos[ 'Data' ].Rebin( rebinX )

	for samples in bkgFiles:
		histos[ samples ] = bkgFiles[ samples ][0].Get( nameInRoot+'_'+samples if 'qual' in process else nameInRoot )
		if bkgFiles[ samples ][1] != 1: histos[ samples ].Scale( bkgFiles[ samples ][1] ) 
		if rebinX > 1: histos[ samples ].Rebin( rebinX )
		if samples in 'QCD'+qcd+'All': hBkg = histos[ 'QCD'+qcd+'All' ].Clone()
		else: hBkg.Add( histos[ samples ].Clone() )

	hData = histos[ 'Data' ].Clone()
	hRatio = histos[ 'Data' ].Clone()
	hRatio.Divide( hBkg )
	#hData.Scale( 1/ hData.Integral() )
	#hBkg.Scale( 1/ hData.Integral() )
	
	'''
	for bin in range(0,  hSoSB.GetNbinsX()):
		hSoSB.SetBinContent(bin, 0.)
		hSoSB.SetBinError(bin, 0.)

	hSoSB2 = hSoSB.Clone()
	for ibin in range(0, hSoSB.GetNbinsX()):
	
		binContData = histos[ 'Data' ].GetBinContent(ibin)
		binErrData = histos[ 'Data' ].GetBinError(ibin)
		binContBkg = histos[ 'QCD' ].GetBinContent(ibin) + histos[ 'TTJets' ].GetBinContent(ibin) + histos[ 'WJets' ].GetBinContent(ibin) + histos[ 'ZJets' ].GetBinContent(ibin)    
		binErrBkg = histos[ 'QCD' ].GetBinError(ibin)
		try:
			value = binContData / TMath.Sqrt( binContData + binContBkg )
		except ZeroDivisionError: continue
		hSoSB.SetBinContent( ibin, value )
	'''

	binWidth = histos['Data'].GetBinWidth(1)

	legend=TLegend(0.70,0.75,0.90,0.87)
	#legend=TLegend(0.50,0.75,0.90,0.87)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.04)
	legend.AddEntry( hData, 'DATA' , 'ep' )
	legend.AddEntry( hBkg, 'MC Bkg', 'lp' )

	hBkg.SetLineColor(kRed-4)
	hBkg.SetLineWidth(2)
	hData.SetMarkerStyle(8)

	tdrStyle.SetPadRightMargin(0.05)
	tdrStyle.SetPadLeftMargin(0.15)
	can = TCanvas('c1', 'c1',  10, 10, 750, 750 )
	pad1 = TPad("pad1", "Fit",0,0.207,1.00,1.00,-1)
	pad2 = TPad("pad2", "Pull",0,0.00,1.00,0.30,-1);
	pad1.Draw()
	pad2.Draw()

	pad1.cd()
	hData.GetYaxis().SetTitle( 'Normalized / '+str(binWidth) )
	if log: pad1.SetLogy() 	
	hData.DrawNormalized("E")
	hBkg.DrawNormalized('hist same')
	hData.SetMaximum( 1.2* max( hData.GetMaximum(), hBkg.GetMaximum() )  )
	#hData.GetYaxis().SetTitleOffset(1.2)
	if xmax: hData.GetXaxis().SetRangeUser( xmin, xmax )
	#hData.GetYaxis().SetTitle( 'Events / '+str(binWidth) )

	CMS_lumi.relPosX = 0.13
	CMS_lumi.CMS_lumi(pad1, 4, 0)
	labelAxis( name, hData, Groom )
	legend.Draw()
	if not (labX and labY): setSelection( [ bkgLabel, 'jet p_{T} > 150 GeV', 'jet |#eta| < 2.4', 'numJets > 1', 'HT > 900 GeV' ], '', ''  )
	else: setSelection( [ bkgLabel, 'jet p_{T} > 150 GeV', 'jet |#eta| < 2.4', 'numJets > 1', 'HT > 900 GeV' ], labX, labY )

	pad2.cd()
	pad2.SetGrid()
	pad2.SetTopMargin(0)
	pad2.SetBottomMargin(0.3)
	'''
	hSoSB.SetFillColor(48)
	hSoSB.SetFillStyle(1001)
	hSoSB.GetYaxis().SetTitle("S / #sqrt{S+B}")
	hSoSB.GetYaxis().SetLabelSize(0.12)
	hSoSB.GetXaxis().SetLabelSize(0.12)
	hSoSB.GetYaxis().SetTitleSize(0.12)
	hSoSB.GetYaxis().SetTitleOffset(0.45)
	#hSoSB.SetMaximum(0.7)
	hSoSB.Sumw2()
	if xmax: hSoSB.GetXaxis().SetRangeUser( xmin, xmax )
	hSoSB.Draw("hist")
	'''
	labelAxis( name, hRatio, Groom )
	hRatio.SetMarkerStyle(8)
	hRatio.GetXaxis().SetTitleOffset(1.1)
	hRatio.GetXaxis().SetLabelSize(0.12)
	hRatio.GetXaxis().SetTitleSize(0.12)
	hRatio.GetYaxis().SetTitle("Data/Bkg")
	hRatio.GetYaxis().SetLabelSize(0.12)
	hRatio.GetYaxis().SetTitleSize(0.12)
	hRatio.GetYaxis().SetTitleOffset(0.55)
	#if( hRatio.GetMaximum() > 2 ): hRatio.SetMaximum( 2.0 )
	hRatio.SetMaximum( 1.5 )
	hRatio.SetMinimum( 0.5 )
	if xmax: hRatio.GetXaxis().SetRangeUser( xmin, xmax )
	hRatio.Draw('E')

	can.SaveAs( 'Plots/'+ outputFileName )
	del can

def plotSystematics( inFileSample, Groom, name, xmin, xmax, rebinX, labX, labY, log, version, proc):
	"""docstring for plot"""

	if 'JES' in proc: typeSys = 'JES'

	outputFileName = name+'_'+args.decay+'RPVSt'+mass+'_'+typeSys+version+'.'+ext 
	print 'Processing.......', outputFileName

	histos = {}
	histos[ 'Nominal' ] = inFileSample[ 'Signal' ][0].Get( version+'AnalysisPlots'+Groom+'/'+name )
	histos[ 'Nominal' ].Scale( inFileSample[ 'Signal' ][1] )
	histos[ 'Up' ] = inFileSample[ 'Signal' ][0].Get( version+'AnalysisPlots'+Groom+typeSys+'Up/'+name )
	histos[ 'Up' ].Scale( inFileSample[ 'Signal' ][1] )
	histos[ 'Down' ] = inFileSample[ 'Signal' ][0].Get( version+'AnalysisPlots'+Groom+typeSys+'Down/'+name )
	histos[ 'Down' ].Scale( inFileSample[ 'Signal' ][1] )

	if rebinX > 1: 
		for k in histos: histos[ k ].Rebin( rebinX )

	binWidth = histos['Nominal'].GetBinWidth(1)

	legend=TLegend(0.60,0.75,0.90,0.90)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.03)
	legend.AddEntry( histos[ 'Nominal' ], 'Nominal', 'l' )
	legend.AddEntry( histos[ 'Up' ], typeSys+'Up', 'l' )
	legend.AddEntry( histos[ 'Down' ], typeSys+'Down', 'l' )

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
	histos['Nominal'].Draw('histe')
	histos['Up'].Draw('histe same')
	histos['Down'].Draw('histe same')
	histos['Nominal'].GetYaxis().SetTitleOffset(0.9)
	histos['Nominal'].GetYaxis().SetTitle( 'Events / '+str(binWidth) )

	labelAxis( name, histos['Nominal'], Groom )
	legend.Draw()
	CMS_lumi.extraText = "Preliminary Simulation"
	CMS_lumi.relPosX = 0.12
	CMS_lumi.CMS_lumi(can, 4, 0)
	if not (labX and labY): labels( name, '', '' )
	else: labels( name, '', '', labX, labY )

	can.SaveAs( 'Plots/'+outputFileName )
	del can

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

	#tmpHisto.Reset()
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

def plotBkgEstimation( dataFile, bkgFiles, Groom, nameInRoot, xmin, xmax, rebinX, labX, labY, log, PU, version, Norm=False ):
	"""docstring for plotBkgEstimation"""

	SRHistos = {}
	CRHistos = {}
	for bkgSamples in bkgFiles:
		SRHistos[ bkgSamples ] = bkgFiles[ bkgSamples ][0].Get( nameInRoot+'_'+bkgSamples+'_A' )
		CRHistos[ bkgSamples ] = bkgFiles[ bkgSamples ][0].Get( nameInRoot+'_'+bkgSamples+'_ABCDProj' )
		if rebinX > 1: 
			SRHistos[ bkgSamples ].Rebin( rebinX )
			CRHistos[ bkgSamples ].Rebin( rebinX )
		if bkgFiles[ bkgSamples ][1] != 1: 
			scale = bkgFiles[ bkgSamples ][1] 
			SRHistos[ bkgSamples ].Scale( scale ) 
			CRHistos[ bkgSamples ].Scale( scale )

	
	hDataCR =  dataFile.Get( nameInRoot+'_DATA_ABCDProj' )
	hDataCR.Rebin( rebinX )
	'''
	BsideData = dataFile.Get( nameInRoot+'_DATA_B' )
	CsideData = dataFile.Get( nameInRoot+'_DATA_C' )
	DsideData = dataFile.Get( nameInRoot+'_DATA_D' )
	if rebinX > 1: 
		#hDataCR.Rebin( rebinX )
		BsideData.Rebin( rebinX )
		CsideData.Rebin( rebinX )
		DsideData.Rebin( rebinX )
	BsideContentData, BsideErrorData  = listOfCont( BsideData )
	CsideContentData, CsideErrorData  = listOfCont( CsideData )
	DsideContentData, DsideErrorData  = listOfCont( DsideData )
	hDataCR = BCDHisto( BsideData, BsideContentData, CsideContentData, DsideContentData ) 
	'''

	#hSR = allHistosFile.Get( nameInRoot+'_QCDHTAll_A' )
	hSR = SRHistos[ 'QCD'+qcd+'All' ].Clone()
	hCR = CRHistos[ 'QCD'+qcd+'All' ].Clone()
	#hSR.Rebin(10)
	#hSR = SRHistos[ 'QCDHT500to700' ].Clone()
	#hCR = CRHistos[ 'QCDHT500to700' ].Clone()
	for samples in SRHistos:
		if 'QCD' not in samples: 
			tmpSR = SRHistos[ samples ].Clone()
			tmpCR = CRHistos[ samples ].Clone()
			hSR.Add( tmpSR )
			hCR.Add( tmpCR )
	
	#hSR.Scale(1/hSR.Integral())
	#hCR.Scale(1/hCR.Integral())
	#hDataCR.Scale(1/2606)
	tmphSR = hSR.Clone()
	tmphSR.Reset()
	tmphSR.Divide( hCR, hSR, 1., 1., '' )
	
	tmphCR = hCR.Clone()
	tmphCR.Reset()
	tmphCR.Divide( hDataCR, hSR, 1., 1., '' )
	binWidth = hSR.GetBinWidth(1)

	if 'Pt' in qcd: bkgLabel='(w QCD pythia8)'
	else: bkgLabel='(w QCD madgraphMLM+pythia8)'
	legend=TLegend(0.55,0.75,0.90,0.87)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.04)
	legend.AddEntry( hSR, 'MC '+bkgLabel+' SR' , 'l' )
	legend.AddEntry( hCR, 'MC '+bkgLabel+' ABCD Proj', 'pl' )

	hSR.SetLineColor(kRed-4)
	hSR.SetLineWidth(2)
	hSR.GetYaxis().SetTitle('Events / '+str(binWidth))
	hSR.GetXaxis().SetRangeUser( 0, 350 )
	hSR.SetMaximum( 1.2* max( hSR.GetMaximum(), hCR.GetMaximum() ) )
	hCR.SetLineColor(kBlue-4)
	hCR.SetLineWidth(2)
	hCR.SetLineStyle(2)
	hDataCR.SetMarkerStyle(8)

	tdrStyle.SetPadRightMargin(0.05)
	tdrStyle.SetPadLeftMargin(0.15)
	can = TCanvas('c1', 'c1',  10, 10, 750, 750 )
	pad1 = TPad("pad1", "Fit",0,0.207,1.00,1.00,-1)
	pad2 = TPad("pad2", "Pull",0,0.00,1.00,0.30,-1);
	pad1.Draw()
	pad2.Draw()

	pad1.cd()
	pad1.SetGrid()
	#if log: pad1.SetLogy() 	
	hSR.Draw("histe")
	hCR.Draw('histe same')

	CMS_lumi.extraText = "Preliminary Simulation"
	CMS_lumi.relPosX = 0.13
	CMS_lumi.CMS_lumi(pad1, 4, 0)
	legend.Draw()
	#if not (labX and labY): labels( name, '', '' )
	#labels( name1, '', '' ) #, labX, labY )

	pad2.cd()
	pad2.SetGrid()
	pad2.SetTopMargin(0)
	pad2.SetBottomMargin(0.3)
	
	labelAxis( nameInRoot, tmphSR, Groom )
	tmphSR.GetXaxis().SetRangeUser( 0, 350 )
	tmphSR.SetMarkerStyle(8)
	tmphSR.GetXaxis().SetTitleOffset(1.1)
	tmphSR.GetXaxis().SetLabelSize(0.12)
	tmphSR.GetXaxis().SetTitleSize(0.12)
	tmphSR.GetYaxis().SetTitle("CR/SR")
	tmphSR.GetYaxis().SetLabelSize(0.12)
	tmphSR.GetYaxis().SetTitleSize(0.12)
	tmphSR.GetYaxis().SetTitleOffset(0.55)
	tmphSR.SetMaximum( 2. )
	tmphSR.SetMinimum( 0. )
	tmphSR.GetYaxis().SetNdivisions(505)
	tmphSR.Draw()
	#tmphCR.Draw()
	line.Draw("same")

	outputFileName = nameInRoot+'_Bkg_'+Groom+'_'+args.RANGE+'_QCD'+qcd+'_bkgShapeEstimation'+version+'Plots.'+ext
	print 'Processing.......', outputFileName
	can.SaveAs( 'Plots/'+ outputFileName )
	del can

	legend2=TLegend(0.55,0.75,0.90,0.87)
	legend2.SetFillStyle(0)
	legend2.SetTextSize(0.04)
	legend2.AddEntry( hSR, 'MC '+bkgLabel+' SR' , 'l' )
	legend2.AddEntry( hDataCR, 'DATA ABCD Proj', 'pl' )
	can = TCanvas('c1', 'c1',  10, 10, 750, 750 )
	pad1 = TPad("pad1", "Fit",0,0.207,1.00,1.00,-1)
	pad2 = TPad("pad2", "Pull",0,0.00,1.00,0.30,-1);
	pad1.Draw()
	pad2.Draw()

	pad1.cd()
	pad1.SetGrid()
	#if log: pad1.SetLogy() 	
	hSR.Draw("histe")
	hDataCR.Draw('PE same')

	CMS_lumi.extraText = "Preliminary"
	CMS_lumi.relPosX = 0.13
	CMS_lumi.CMS_lumi(pad1, 4, 0)
	legend2.Draw()
	#if not (labX and labY): labels( name, '', '' )
	#labels( name1, '', '' ) #, labX, labY )

	pad2.cd()
	pad2.SetGrid()
	pad2.SetTopMargin(0)
	pad2.SetBottomMargin(0.3)
	
	labelAxis( nameInRoot, tmphCR, Groom )
	tmphCR.GetXaxis().SetRangeUser( 0, 350 )
	tmphCR.SetMarkerStyle(8)
	tmphCR.GetXaxis().SetTitleOffset(1.1)
	tmphCR.GetXaxis().SetLabelSize(0.12)
	tmphCR.GetXaxis().SetTitleSize(0.12)
	tmphCR.GetYaxis().SetTitle("DATA/MC")
	tmphCR.GetYaxis().SetLabelSize(0.12)
	tmphCR.GetYaxis().SetTitleSize(0.12)
	tmphCR.GetYaxis().SetTitleOffset(0.55)
	tmphCR.SetMaximum( 2. )
	tmphCR.SetMinimum( 0. )
	tmphCR.GetYaxis().SetNdivisions(505)
	tmphCR.Draw()
	line.Draw("same")

	outputFileName = nameInRoot+'_DATA_Bkg_'+Groom+'_'+args.RANGE+'_QCD'+qcd+'_bkgShapeEstimation'+version+'Plots.'+ext
	print 'Processing.......', outputFileName
	can.SaveAs( 'Plots/'+ outputFileName )
	del can


def plot2DBkgEstimation( rootFile, sample, Groom, nameInRoot, titleXAxis, titleXAxis2, Xmin, Xmax, rebinx, Ymin, Ymax, rebiny, legX, legY, PU, version ):
	"""docstring for plot"""

	outputFileName = nameInRoot+'_'+sample+'_'+Groom+'_'+args.RANGE+'_bkgShapeEstimation'+version+'Plots.'+ext
	print 'Processing.......', outputFileName

	bkgHistos = OrderedDict()
	if 'QCDHTAll' in sample:
		for bkgSamples in [ 'QCDHT500to700', 'QCDHT700to1000', 'QCDHT1000to1500', 'QCDHT1500to2000', 'QCDHT2000toInf' ]:
			bkgHistos[ bkgSamples+'_A' ] = Rebin2D( rootFile.Get( nameInRoot+'_'+bkgSamples+'_A' ), rebinx, rebiny )
			bkgHistos[ bkgSamples+'_B' ] = Rebin2D( rootFile.Get( nameInRoot+'_'+bkgSamples+'_B' ), rebinx, rebiny )
			bkgHistos[ bkgSamples+'_C' ] = Rebin2D( rootFile.Get( nameInRoot+'_'+bkgSamples+'_C' ), rebinx, rebiny )
			bkgHistos[ bkgSamples+'_D' ] = Rebin2D( rootFile.Get( nameInRoot+'_'+bkgSamples+'_D' ), rebinx, rebiny )

		hBkg = bkgHistos[ 'QCDHT500to700_B' ].Clone()
		for samples in bkgHistos:
			if 'QCDHT500to700_B' not in samples: hBkg.Add( bkgHistos[ samples ].Clone() )
	else: 
		if not 'DATA' in sample: bkgHistos[ sample+'_A' ] = Rebin2D( rootFile.Get( nameInRoot+'_'+sample+'_A' ), rebinx, rebiny )
		bkgHistos[ sample+'_B' ] = Rebin2D( rootFile.Get( nameInRoot+'_'+sample+'_B' ), rebinx, rebiny )
		bkgHistos[ sample+'_C' ] = Rebin2D( rootFile.Get( nameInRoot+'_'+sample+'_C' ), rebinx, rebiny )
		bkgHistos[ sample+'_D' ] = Rebin2D( rootFile.Get( nameInRoot+'_'+sample+'_D' ), rebinx, rebiny )

		hBkg = bkgHistos[ sample+'_B' ].Clone()
		for samples in bkgHistos:
			if sample+'_B' not in samples: hBkg.Add( bkgHistos[ samples ].Clone() )

	if 'DATA' in sample: CMS_lumi.extraText = "Preliminary"
	else: CMS_lumi.extraText = "Preliminary Simulation"
	hBkg.GetXaxis().SetTitle( titleXAxis )
	hBkg.GetYaxis().SetTitleOffset( 0.9 )
	hBkg.GetYaxis().SetTitle( titleXAxis2 )
	corrFactor = hBkg.GetCorrelationFactor()
	textBox=TLatex()
	textBox.SetNDC()
	textBox.SetTextSize(0.05) 
	textBox.SetTextFont(62) ### 62 is bold, 42 is normal

	if (Xmax or Ymax):
		hBkg.GetXaxis().SetRangeUser( Xmin, Xmax )
		hBkg.GetYaxis().SetRangeUser( Ymin, Ymax )

	tdrStyle.SetPadRightMargin(0.12)
	can = TCanvas('c1', 'c1',  750, 500 )
	can.SetLogz()
	hBkg.Draw('colz')
	textBox.DrawLatex(0.6, 0.8, 'Corr. Factor = '+str(round(corrFactor,2)))

	CMS_lumi.relPosX = 0.13
	CMS_lumi.CMS_lumi(can, 4, 0)

	can.SaveAs( 'Plots/'+outputFileName )
	#can.SaveAs( 'Plots/'+outputFileName.replace(''+ext, 'gif') )
	del can

def tmpplotDiffSample( sample1, sample2, Groom, name, xmax, labX, labY, log, Diff , Norm=False):
	"""docstring for plot"""

	outputFileName = name+'_'+args.decay+'RPVSt'+mass+'_Diff'+Diff+'.'+ext 
	print 'Processing.......', outputFileName

	histos = {}
	#inFileSample1 = TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_pruned_RPVStopStopToJets_'+args.decay+'_M-'+str(mass)+'_v2.root')
	#histos[ 'Sample1' ] = inFileSample1.Get( 'massAve_deltaEtaDijet_RPVStopStopToJets_'+args.decay+'_M-'+str(mass) )
	inFileSample1 = TFile.Open('Rootfiles/v74X/RUNMiniBoostedAnalysis_pruned_TTJets_low_v03.root')
	histos[ 'Sample1' ] = inFileSample1.Get( 'massAve_deltaEtaDijet_TTJets' )
	histos[ 'Sample1' ].Rebin(10)
	inFileSample2 = TFile.Open('Rootfiles/v02/RUNMiniBoostedAnalysis_pruned_TTJets_low_v2.root')
	histos[ 'Sample2' ] = inFileSample2.Get( 'massAve_deltaEtaDijet_TTJets' )
	histos[ 'Sample2' ].Rebin(10)
	histos[ 'Sample2' ].Scale(0.4)

	hSample1 = histos[ 'Sample2' ].Clone()
	hSample2 = histos[ 'Sample1' ].Clone()
	hSample1.Divide( hSample2 )

	binWidth = histos['Sample1'].GetBinWidth(1)

	legend=TLegend(0.60,0.75,0.90,0.90)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.03)

	histos[ 'Sample1' ].SetLineWidth(2)
	histos[ 'Sample1' ].SetLineColor(48)
	histos[ 'Sample2' ].SetLineColor(38)
	histos[ 'Sample2' ].SetLineWidth(2)
	histos[ 'Sample1' ].SetMaximum( 1.2* max( histos[ 'Sample1' ].GetMaximum(), histos[ 'Sample2' ].GetMaximum() ) ) 
	histos.values()[0].GetXaxis().SetRangeUser( 0, xmax )

	can = TCanvas('c1', 'c1',  10, 10, 750, 500 )
	legend.AddEntry( histos[ 'Sample1' ], sample1, 'l' )
	legend.AddEntry( histos[ 'Sample2' ], sample2, 'l' )
	histos['Sample1'].SetMinimum(10)
	histos['Sample1'].Draw('histe')
	histos['Sample1'].GetYaxis().SetTitleOffset(0.9)
	histos['Sample2'].Draw('histe same')
	histos['Sample1'].GetYaxis().SetTitle( 'Events / '+str(binWidth) )

	CMS_lumi.extraText = "Preliminary Simulation"
	CMS_lumi.relPosX = 0.14
	CMS_lumi.CMS_lumi(can, 4, 0)
	labelAxis( name, histos['Sample1'], '' )
	legend.Draw()
	#if not (labX and labY): labels( name, '13 TeV - Scaled to '+lumi+' fb^{-1}', '' )
	#else: labels( name, '13 TeV - Scaled to '+lumi+' fb^{-1}', '', labX, labY )

	can.SaveAs( 'Plots/'+outputFileName )
	del can


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--proc', action='store', default='1D', help='Process to draw, example: 1D, 2D, MC.' )
	parser.add_argument('-d', '--decay', action='store', default='UDD312', dest='decay', help='Decay, example: UDD312, UDD323.' )
	parser.add_argument('-v', '--version', action='store', default='Boosted', help='Boosted or non version, example: Boosted' )
	parser.add_argument('-g', '--grom', action='store', default='pruned', dest='grooming', help='Grooming Algorithm, example: Pruned, Filtered.' )
	parser.add_argument('-m', '--mass', action='store', default='100', help='Mass of Stop, example: 100' )
	parser.add_argument('-C', '--cut', action='store', default='_cutMassAsym', help='cut, example: cutDEta' )
	parser.add_argument('-pu', '--PU', action='store', default='Asympt25ns', help='PU, example: PU40bx25.' )
	parser.add_argument('-s', '--single', action='store', default='all', help='single histogram, example: massAve_cutDijet.' )
	parser.add_argument('-q', '--QCD', action='store', default='Pt', help='Type of QCD binning, example: HT.' )
	parser.add_argument('-c', '--campaign', action='store', default='RunIISpring15MiniAODv2-74X', help='Campaign, example: PHYS14.' )
	parser.add_argument('-l', '--lumi', action='store', type=float, default=149.9, help='Luminosity, example: 1.' )
	parser.add_argument('-r', '--range', action='store', default='low', dest='RANGE', help='Trigger used, example PFHT800.' )
	parser.add_argument('-e', '--extension', action='store', default='png', help='Extension of plots.' )

	try:
		args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)

	process = args.proc
	PU = args.PU
	qcd = args.QCD
	camp = args.campaign
	lumi = args.lumi
	histo = args.single
	mass = args.mass
	cut = args.cut
	single = args.single
	version = args.version
	ext = args.extension
	
	bkgFiles = OrderedDict() 
	signalFiles = {}
	CMS_lumi.extraText = "Preliminary"
	lumi = 2606.
	CMS_lumi.lumi_13TeV = "2.60 fb^{-1}"
	
	if 'Pt' in qcd: 
		bkgLabel='(w QCD pythia8)'
		QCDSF = 1 #0.88
	else: 
		bkgLabel='(w QCD madgraphMLM+pythia8)'
		QCDSF = 1.05

	if process in [ 'mini', '2Dmini', 'qual', 'bkgEst', '2DbkgEst', 'CF', 'Norm' ]:
		dataFile = TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_DATA_'+args.RANGE+'_v03.root')
		signalFiles[ 'Signal' ] = [ TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_RPVStopStopToJets_'+args.decay+'_M-'+str(mass)+'_v03.root'), 1, args.decay+' RPV #tilde{t} '+str(mass)+' GeV', kRed-4]
		bkgFiles[ 'TTJets' ] = [ TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_TTJets_'+args.RANGE+'_v03.root'),	1, 't #bar{t} + Jets', kGreen ]
#		bkgFiles[ 'ZJetsToQQ' ] = [ TFile.Open('Rootfiles/RUNMiniResolvedAnalysis_ZJetsToQQ_HT600toInf_13TeV-madgraph_RunIISpring15MiniAODv03-74X_Asympt25ns_v09_v03.root'), 1., 'Z + Jets', kOrange ]
		bkgFiles[ 'WJetsToQQ' ] = [ TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_WJetsToQQ_'+args.RANGE+'_v03.root'), 1., 'W + Jets', kMagenta ]
		bkgFiles[ 'WWTo4Q' ] = [ TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_WWTo4Q_'+args.RANGE+'_v03.root'), 1 , 'WW (had)', kMagenta+2 ]
		bkgFiles[ 'ZZTo4Q' ] = [ TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_ZZTo4Q_'+args.RANGE+'_v03.root'), 1, 'ZZ (had)', kOrange+2 ]
		bkgFiles[ 'WZ' ] = [ TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_WZ_'+args.RANGE+'_v03.root'), 1, 'WZ', kCyan ]
		bkgFiles[ 'QCD'+qcd+'All' ] = [ TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_QCD'+qcd+'All_'+args.RANGE+'_v03.root'), QCDSF, 'QCD', kBlue-4 ]
		#bkgFiles[ 'QCDPtAll' ] = [ TFile.Open('Rootfiles/RUNMiniBoostedAnalysis_'+args.grooming+'_QCDPtAll_'+args.RANGE+'_v03.root'), QCDSF, 'QCD', kBlue-4 ]

	else:
		dataFile = TFile.Open('Rootfiles/RUNAnalysis_JetHT_Run2015D-16Dec2015-v1_v76x_v1p0_v03.root')
		signalFiles[ 'Signal' ] = [ TFile.Open('Rootfiles/RUNAnalysis_RPVStopStopToJets_'+args.decay+'_M-'+str(mass)+'_RunIIFall15MiniAODv2_v76x_v1p0_v03.root'), lumi, args.decay+' RPV #tilde{t} '+str(mass)+' GeV', kRed-4]
		#bkgFiles[ 'QCDHTAll' ] = [ TFile.Open('Rootfiles/RUNAnalysis_QCDHTAll_RunIIFall15MiniAODv2_v76x_v1p0_v03.root'), lumi*1.05, 'QCDHT', kBlue-4 ]
		bkgFiles[ 'QCD'+qcd+'All' ] = [ TFile.Open('Rootfiles/RUNAnalysis_QCD'+qcd+'All_RunIIFall15MiniAODv2_v76x_v1p0_v03.root'), lumi*QCDSF, 'QCD'+qcd+'', kBlue-4 ]
		bkgFiles[ 'TTJets' ] = [ TFile.Open('Rootfiles/RUNAnalysis_TTJets_RunIIFall15MiniAODv2_v76x_v1p0_v03.root'),	lumi, 't #bar{t} + Jets', kGreen ]
		bkgFiles[ 'WJets' ] = [ TFile.Open('Rootfiles/RUNAnalysis_WJetsToQQ_HT-600ToInf_RunIIFall15MiniAODv2_v76x_v1p0_v03.root'), lumi , 'W + Jets', kMagenta ]
		bkgFiles[ 'WWTo4Q' ] = [ TFile.Open('Rootfiles/RUNAnalysis_WWTo4Q_RunIIFall15MiniAODv2_v76x_v1p0_v03.root'), lumi , 'WW (had)', kMagenta+2 ]
		#bkgFiles[ 'ZJets' ] = [ TFile.Open('Rootfiles/RUNAnalysis_ZJetsToQQ_HT600toInf_13TeV-madgraph_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'), lumi, 'Z + Jets', kOrange ]
		bkgFiles[ 'ZZTo4Q' ] = [ TFile.Open('Rootfiles/RUNAnalysis_ZZTo4Q_RunIIFall15MiniAODv2_v76x_v1p0_v03.root'), lumi, 'ZZ (had)', kOrange+2 ]
		bkgFiles[ 'WZ' ] = [ TFile.Open('Rootfiles/RUNAnalysis_WZ_RunIIFall15MiniAODv2_v76x_v1p0_v03.root'), lumi, 'WZ', kCyan ]
			

	dijetlabX = 0.85
	dijetlabY = 0.55
	subjet112vs212labX = 0.7
	subjet112vs212labY = 0.88
	polAnglabX = 0.2
	polAnglabY = 0.88
	taulabX = 0.40
	taulabY = 0.80
	cosPhilabX = 0.15
	cosPhilabY = 0.45

	massMinX = 0
	massMaxX = 400
	polAngXmin = 0.7
	polAngXmax = 1.0
	HTMinX = 300
	HTMaxX = 1300
	ptMinX = 100
	ptMaxX = 800


	plotList = [ 
		[ '2D', 'Boosted', 'jetTrimmedMassHT', 'Leading Trimmed Jet Mass [GeV]', 'HT [GeV]', 0, massMaxX, 1, 100, HTMaxX, 1, jetMassHTlabX, jetMassHTlabY],
		[ '2D', 'Boosted', 'leadMassHT', 'Leading Jet Mass [GeV]', 'HT [GeV]', 0, massMaxX, 1, 100, HTMaxX, 1, jetMassHTlabX, jetMassHTlabY],

		[ '2D', 'Boosted', 'leadMassHT_cutTrigger', 'Leading Jet Mass [GeV]', 'HT [GeV]', 0, massMaxX, 1, 100, HTMaxX, 1, jetMassHTlabX, jetMassHTlabY],

		[ '1D', 'Boosted', 'jet1Pt', 100, 1500, 1, '', '', False],
		[ '1D', 'Boosted', 'jet1Eta', -3, 3, 1, '', '', False],
		[ '1D', 'Boosted', 'jet1Mass', 0, massMaxX, 1, '', '', False],
		[ '1D', 'Boosted', 'HT', 700, 2000, 5, '', '', False],
		[ '1D', 'Boosted', 'jet2Pt', 100, 1500, 1, '', '', False],
		[ '1D', 'Boosted', 'jet2Eta', -3, 3, 1, '', '', False],
		[ '1D', 'Boosted', 'jet2Mass', 0, massMaxX, 1, '', '', False],
		[ '1D', 'Boosted', 'massAve', 0, massMaxX, 1, '', '', False],

		[ '1D', 'Resolved', 'HT', 700, 5000, 2, '', '', True],
		[ '1D', 'Resolved', 'jet1Pt', 100, 1500, 2, '', '', True],
		[ '1D', 'Resolved', 'jet2Pt', 0, 1500, 2, '', '', True],
		[ '1D', 'Resolved', 'jet3Pt', 0, 500, 2, '', '', True],
		[ '1D', 'Resolved', 'jet4Pt', 0, 300, 2, '', '', True],
		[ '1D', 'Resolved', 'massAve', 0, 1000, 2, '', '', True],

		#[ 'qual', 'Boosted', 'subjetPtRatio', '', '', '', '', True],
		[ 'qual', 'Boosted', 'deltaEtaDijet', '', '', 1,  0.85, 0.45, True],
		#[ 'qual', 'Boosted', 'prunedMassAsym', '', '', 1, 0.45, 0.45, False],
		#[ 'qual', 'Boosted', 'jet1Tau21', '', '', 1, 0.45, 0.85, False],
		#[ 'qual', 'Boosted', 'jet2Tau21', '', '', 1, 0.45, 0.85, False],
		#[ 'qual', 'Boosted', 'jet1Tau31', '', '', 1, 0.45, 0.85, False],
		#[ 'qual', 'Boosted', 'jet2Tau31', '', '', 1, 0.45, 0.85, False],
		[ 'qual', 'Boosted', 'jet1Tau32', '', '', 1, 0.45, 0.85, False],
		[ 'qual', 'Boosted', 'jet1CosThetaStar', '', '', 1, 0.85, 0.45, False],
		[ 'qual', 'Boosted', 'jet2CosThetaStar', '', '', 1, 0.85, 0.45, False],
		[ 'qual', 'Boosted', 'jet1Pt', 100, 1500, 10, 0.85, 0.45, False],
		#[ 'qual', 'Boosted', 'jet1Eta', -3, 3, 1, 0.85, 0.45, False],
		[ 'qual', 'Boosted', 'jet2Pt', 100, 1500, 10, 0.85, 0.45, False],
		#[ 'qual', 'Boosted', 'jet2Eta', -3, 3, 1, 0.85, 0.45, False],
		[ 'qual', 'Boosted', 'numJets', '', '', 1, 0.85, 0.45, True],
		[ 'qual', 'Boosted', 'massAve', 0, 400, 10, 0.85, 0.70, True],
		[ 'qual', 'Boosted', 'HT', 700, 2000, 10, 0.85, 0.45, True],
		[ 'qual', 'Boosted', 'MET', 0, 100, 10, 0.85, 0.45, False],
		[ 'qual', 'Resolved', 'jet1Pt', 100, 1500, 1, 0.85, 0.45, True],
		[ 'qual', 'Resolved', 'jet2Pt', 0, 1500, 1, 0.85, 0.45, True],
		[ 'qual', 'Resolved', 'jet3Pt', 0, 500, 1, 0.85, 0.45, True],
		[ 'qual', 'Resolved', 'jet4Pt', 0, 300, 1, 0.85, 0.45, True],
		[ 'qual', 'Resolved', 'HT', 700, 2000, 1, 0.85, 0.45, True],
		[ 'qual', 'Resolved', 'jetNum', '', '', 1, 0.85, 0.45, True],
		[ 'qual', 'Resolved', 'massAve', 0, 1000, 2, '', '', True],
		[ 'jetIDQual', version, 'HT', 700, 2000, 1, 0.90, 0.70, True],
		[ 'jetIDQual', version, 'NPV', 0, 50, 1, 0.90, 0.70, False],
		[ 'jetIDQual', version, 'jetNum', '', '', 1, 0.90, 0.70, True],
		[ 'jetIDQual', 'Boosted', 'jet1NeutralHadronEnergy', '', '', 5, 0.90, 0.70, True],
		[ 'jetIDQual', 'Boosted', 'jet1NeutralEmEnergy', '', '', 5, 0.90, 0.70, True],
		[ 'jetIDQual', 'Boosted', 'jet1ChargedHadronEnergy', '', '', 5, 0.90, 0.70, True],
		[ 'jetIDQual', 'Boosted', 'jet1ChargedEmEnergy', '', '', 5, 0.90, 0.70, True],
		[ 'jetIDQual', 'Boosted', 'jet1ChargedMultiplicity', '', '', 1, 0.90, 0.70, True],
		[ 'jetIDQual', 'Boosted', 'jet1NumConst', '', '', 1, 0.90, 0.70, True],
		[ 'jetIDQual', version, 'jet1Pt', 400, 1500, 1, 0.90, 0.70, True],
		[ 'jetIDQual', version, 'jet1Eta', -3, 3, 5, 0.90, 0.70, False],
		[ 'jetIDQual', 'Boosted', 'jet1Mass', 0, 1000, 10, 0.90, 0.70, True],
		[ 'jetIDQual', 'Boosted', 'jet1PrunedMass', 0, 1000, 10, 0.90, 0.70, True],
		[ 'jetIDQual', 'Boosted', 'jet1TrimmedMass', 0, 1000, 10, 0.90, 0.70, True],
		[ 'jetIDQual', 'Boosted', 'jet1FilteredMass', 0, 1000, 10, 0.90, 0.70, True],
		[ 'jetIDQual', 'Boosted', 'jet1SoftDropMass', 0, 1000, 10, 0.90, 0.70, True],
		[ 'jetIDQual', 'Boosted', 'jet2NeutralHadronEnergy', '', '', 5, 0.90, 0.70, True],
		[ 'jetIDQual', 'Boosted', 'jet2NeutralEmEnergy', '', '', 5, 0.90, 0.70, True],
		[ 'jetIDQual', 'Boosted', 'jet2ChargedHadronEnergy', '', '', 5, 0.90, 0.70, True],
		[ 'jetIDQual', 'Boosted', 'jet2ChargedEmEnergy', '', '', 5, 0.90, 0.70, True],
		[ 'jetIDQual', 'Boosted', 'jet2ChargedMultiplicity', '', '', 1, 0.90, 0.70, True],
		[ 'jetIDQual', 'Boosted', 'jet2NumConst', '', '', 1, 0.90, 0.70, True],
		[ 'jetIDQual', version, 'jet2Pt', 400, 1500, 1, 0.90, 0.70, True],
		[ 'jetIDQual', version, 'jet2Eta', -3, 3, 5, 0.90, 0.70, False],
		[ 'jetIDQual', 'Boosted', 'jet2Mass', 0, 1000, 10, 0.90, 0.70, True],
		[ 'jetIDQual', 'Boosted', 'jet2PrunedMass', 0, 1000, 10, 0.90, 0.70, True],
		[ 'jetIDQual', 'Boosted', 'jet2TrimmedMass', 0, 1000, 10, 0.90, 0.70, True],
		[ 'jetIDQual', 'Boosted', 'jet2FilteredMass', 0, 1000, 10, 0.90, 0.70, True],
		[ 'jetIDQual', 'Boosted', 'jet2SoftDropMass', 0, 1000, 10, 0.90, 0.70, True],
		[ 'jetIDQual', version, 'MET', '', '', 1, 0.90, 0.70, False],
		[ 'jetIDQual', version, 'METHT', '', '', 1, 0.90, 0.70, True],
		#[ 'jetIDQual', version, 'NPV_NOPUWeight', '', '', 1, 0.90, 0.70, False],
		[ 'jetIDQual', version, 'neutralHadronEnergy', '', '', 5, 0.90, 0.70, True],
		[ 'jetIDQual', version, 'neutralEmEnergy', '', '', 5, 0.90, 0.70, True],
		[ 'jetIDQual', version, 'chargedHadronEnergy', '', '', 5, 0.90, 0.70, True],
		[ 'jetIDQual', version, 'chargedEmEnergy', '', '', 5, 0.90, 0.70, True],
		[ 'jetIDQual', version, 'chargedMultiplicity', '', '', 1, 0.90, 0.70, True],
		[ 'jetIDQual', version, 'numConst', '', '', 1, 0.90, 0.70, True],

		#[ 'Norm', 'Boosted', 'NPV', '', '', 1, '', '', False],
		#[ 'Norm', 'Boosted', 'jet1Subjet1Pt', '', '', '', '', True],
		#[ 'Norm', 'Boosted', 'jet1Subjet2Pt', '', '', '', True],
		#[ 'Norm', 'Boosted', 'jet2Subjet1Pt', '', '', '', True],
		#[ 'Norm', 'Boosted', 'jet2Subjet2Pt', '', '', '', True],
		#[ 'Norm', 'Boosted', 'jet1Subjet1Mass', '', '', '', True],
		#[ 'Norm', 'Boosted', 'jet1Subjet2Mass', '', '', '', True],
		#[ 'Norm', 'Boosted', 'jet2Subjet1Mass', '', '', '', True],
		#[ 'Norm', 'Boosted', 'jet2Subjet2Mass', '', '', '', True],
		#[ 'Norm', 'Boosted', 'jet1Tau1', '', '', 1, taulabX, taulabY, False],
		#[ 'Norm', 'Boosted', 'jet1Tau2', '', '', 1, taulabX, taulabY, False],
		#[ 'Norm', 'Boosted', 'jet1Tau3', '', '', 1, taulabX, taulabY, False],
		[ 'Norm', 'Boosted', 'jet1Tau21', '', '', 1, taulabX, taulabY, False],
		[ 'Norm', 'Boosted', 'jet2Tau21', '', '', 1, taulabX, taulabY, False],
		[ 'Norm', 'Boosted', 'jet2Tau31', '', '', 1, taulabX, taulabY, False],
		[ 'Norm', 'Boosted', 'jet1Tau31', '', '', 1, taulabX, taulabY, False],
		[ 'Norm', 'Boosted', 'prunedMassAsym', '', '', 1, 0.40, 0.80, False],
		[ 'Norm', 'Boosted', 'deltaEtaDijet', '', '', 1, '', '', False],
		[ 'Norm', 'Boosted', 'jet1Tau32', '', '', 1, taulabX, taulabY, False],
		[ 'Norm', 'Boosted', 'jet2Tau32', '', '', 1, taulabX, taulabY, False],
		[ 'Norm', 'Boosted', 'jet1SubjetPtRatio', '', '', 1,taulabX, taulabY,  True],
		[ 'Norm', 'Boosted', 'jet2SubjetPtRatio', '', '', 1, taulabX, taulabY,  True],
		#[ 'Norm', 'Boosted', 'subjetPtRatio', '', '', 1, '', '', True],
		[ 'Norm', 'Boosted', 'jet1CosThetaStar', '', '', 1, '', '', False],
		[ 'Norm', 'Boosted', 'jet2CosThetaStar', '', '', 1, '', '', False],
		#[ 'Norm', 'Boosted', 'jet1Subjet21MassRatio', '', '', 1, '', '', False],
		#[ 'Norm', 'Boosted', 'jet1Subjet112MassRatio', '', '', 1, '', '', False],
		#[ 'Norm', 'Boosted', 'jet1Subjet1JetMassRatio', '', '', 1, '', '', False],
		#[ 'Norm', 'Boosted', 'jet1Subjet212MassRatio', '', '', 1, '', '', False],
		#[ 'Norm', 'Boosted', 'jet1Subjet2JetMassRatio', '', '', 1, '', '', False],
		#[ 'Norm', 'Boosted', 'jet2Subjet112MassRatio', '', '', 1, '', '', False],
		#[ 'Norm', 'Boosted', 'jet2Subjet1JetMassRatio', '', '', 1, '', '', False],
		#[ 'Norm', 'Boosted', 'jet2Subjet212MassRatio', '', '', 1, '', '', False],
		#[ 'Norm', 'Boosted', 'jet2Subjet2JetMassRatio', '', '', 1, '', '', False],
		#[ 'Norm', 'Boosted', 'subjetPtRatio', '', '', 1, '', '', False],
		#[ 'Norm', 'Boosted', 'subjetMass21Ratio', '', '', 1, '', '', False],
		#[ 'Norm', 'Boosted', 'subjet112MassRatio', '', '', 1, '', '', False],
		#[ 'Norm', 'Boosted', 'subjet212MassRatio', '', '', 1, '', '', False],
		#[ 'Norm', 'Boosted', 'subjetPolAngle13412', polAngXmin, polAngXmax, 1, '', '', False],
		#[ 'Norm', 'Boosted', 'subjetPolAngle31234', polAngXmin, polAngXmax, 1, '', '', False],
		[ 'Norm', 'Resolved', 'massRes', '', '', 1, '', '', False],
		[ 'Norm', 'Resolved', 'deltaEta', '', '', 1, '', '', False],
		[ 'Norm', 'Resolved', 'minDeltaR', '', '', 1, '', '', False],
		[ 'Norm', 'Resolved', 'deltaR', '', '', 1, '', '', False],
		[ 'Norm', 'Resolved', 'jet4Pt', 0, 300, 1, '', '', False],
		[ 'Norm', 'Resolved', 'cosThetaStar1', '', '', 1, '', '', False],
		[ 'Norm', 'Resolved', 'cosThetaStar2', '', '', 1, '', '', False],


		[ 'simple', 'HT',  1000, '', '', False],
		[ 'simple', 'HT',  1000, '', '', True],
		[ 'simple', 'massAve_cutDijet',  massMaxX, '', '', False],
		[ 'simple', 'massAve_cutAsym',  massMaxX, '', '', False],
		[ 'simple', 'massAve_cutCosTheta',  massMaxX, '', '', False],
		[ 'simple', 'massAve_cutSubjetPtRatio',  massMaxX, '', '', False],
		#[ 'simple', 'massAve_cutSubjetPtRatio',  massMaxX, '', '', True ],
		[ 'simple', 'massAve_cutTau31',  massMaxX, '', '', False],
		[ 'simple', 'massAve_cutTau21',  massMaxX, '', '', False],
		
		[ 'sys', 'Boosted', 'massAve', 0, massMaxX, 1, 0.85, 0.45, False],
		[ 'sys', 'Boosted', 'jet1Pt', 400, 1500, 2, 0.85, 0.45, False],
		[ 'sys', 'Boosted', 'jet2Pt', 400, 1500, 2, 0.85, 0.45, False],
		[ 'sys', 'Boosted', 'HT', 700, 2000, 5, 0.85, 0.45, False],

		[ 'mini', version, 'massAve', 0, massMaxX, 10, '', '', False],
		[ '2Dmini', 'Boosted', 'massAsymVsdeltaEtaDijet', 'Mass Asymmetry', '| #eta_{j1} - #eta_{j2} |', 0, 1, 1, 0, 5, 1, jetMassHTlabX, jetMassHTlabY],
		[ '2Dmini', 'Boosted', 'massAsymVsjet1Tau21', 'Mass Asymmetry', 'Leading jet #tau_{21} |', 0, 1, 1, 0, 1, 1, jetMassHTlabX, jetMassHTlabY],
		[ '2Dmini', 'Boosted', 'massAsymVsjet2Tau21', 'Mass Asymmetry', '2nd Leading jet #tau_{21} |', 0, 1, 1, 0, 1, 1, jetMassHTlabX, jetMassHTlabY],
		[ '2Dmini', 'Boosted', 'massAsymVsjet1Tau31', 'Mass Asymmetry', 'Leading jet #tau_{31} |', 0, 1, 1, 0, 1, 1, jetMassHTlabX, jetMassHTlabY],
		[ '2Dmini', 'Boosted', 'massAsymVsjet2Tau31', 'Mass Asymmetry', '2nd Leading jet #tau_{31} |', 0, 1, 1, 0, 1, 1, jetMassHTlabX, jetMassHTlabY],
		[ '2Dmini', 'Boosted', 'deltaEtaDijetVsjet1Tau21', '| #eta_{j1} - #eta_{j2} |', 'Leading jet #tau_{21} |', 0, 5, 1, 0, 1, 1, jetMassHTlabX, jetMassHTlabY],
		[ '2Dmini', 'Boosted', 'deltaEtaDijetVsjet2Tau21', '| #eta_{j1} - #eta_{j2} |', '2nd Leading jet #tau_{21} |', 0, 5, 1, 0, 1, 1, jetMassHTlabX, jetMassHTlabY],
		[ '2Dmini', 'Boosted', 'deltaEtaDijetVsjet1Tau31', '| #eta_{j1} - #eta_{j2} |', 'Leading jet #tau_{31} |', 0, 5, 1, 0, 1, 1, jetMassHTlabX, jetMassHTlabY],
		[ '2Dmini', 'Boosted', 'deltaEtaDijetVsjet2Tau31', '| #eta_{j1} - #eta_{j2} |', '2nd Leading jet #tau_{31} |', 0, 5, 1, 0, 1, 1, jetMassHTlabX, jetMassHTlabY],
		[ 'bkgEst', version, 'massAve', 0, massMaxX, 10, '', '', False],
		[ '2DbkgEst', 'Boosted', 'prunedMassAsymVsdeltaEtaDijet', 'Mass Asymmetry', '| #eta_{j1} - #eta_{j2} |', 0, 1, 1, 0, 5, 1, jetMassHTlabX, jetMassHTlabY],

		]

	if 'all' in single: Plots = [ x[2:] for x in plotList if ( ( process in x[0] ) and ( x[1] in version ) )  ]
	else: Plots = [ y[2:] for y in plotList if ( ( process in y[0] ) and ( y[1] in version ) and ( y[2] in single ) )  ]

	if 'Resolved' in version: args.grooming =  '' 
	if 'all' in args.grooming: Groommers = [ '', 'Trimmed', 'Pruned', 'Filtered', "SoftDrop" ]
	else: Groommers = [ args.grooming ]

	if 'all' in cut: 
		if 'Boosted' in version: listCuts = [ '_jet1Tau21', '_jet2Tau21', '_prunedMassAsym', '_deltaEtaDijet', '_jet1Tau31', '_jet2Tau31' ]
		else: listCuts = [ '_cutMassRes', '_cutDelta', '_cutEtaBand', '_cutDeltaR', '_cutCosTheta', '_cutDEta', '_cutMassPairing' ]
	#elif 'NO' in cut: listCuts = [ '_cutNOMassAsym', '_cutTau21_NOMA', '_cutCosTheta_NOMA', '_cutDEta_NOMA' ]
	else: listCuts = [ cut ]

	if 'CF' in process:
		plotCutFlow( signalFiles, bkgFiles, args.grooming, 'cutflow', 8, True, PU, True )
	elif 'tmp' in process:
		tmpplotDiffSample( '74X', '76X', '', 'massAve_deltaEtaDijet_TTJets', 500, '', '', False, '74Xvs76X' )

	for i in Plots:
		for optGroom in Groommers:
			if process in '2D': 
				plot2D( signalFiles, 'RPVSt'+str(mass), optGroom, version+'AnalysisPlots'+Groom+'/'+[0], i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], PU, version )
				plot2D( bkgFiles, 'QCD', optGroom, version+'AnalysisPlots'+Groom+'/'+[0], i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], PU, version )
				#plot2D( inputFileTTJets, 'TTJets', optGroom, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], PU, version )
				#plot2D( inputFileWJetsToQQ, 'WJets', optGroom, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], PU, version )
				#plot2D( inputFileZJetsToQQ, 'ZJets', optGroom, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], PU, version )

			elif '1D' in process:
				for cut1 in listCuts:
					plotSignalBkg( signalFiles, bkgFiles, optGroom, version+'AnalysisPlots'+optGroom+'/'+i[0]+cut1, i[0]+cut1, i[1], i[2], i[3], i[4], i[5], i[6], PU, version )
			
			elif ( 'jetIDQual' in process ):
				for cut1 in listCuts:
					if 'Boosted' in version: plotQuality( dataFile, bkgFiles, optGroom, version+'AnalysisPlots/'+i[0]+cut1, i[0]+cut1, i[1], i[2], i[3], i[4], i[5], i[6], PU, version )
					else: plotQuality( dataFile, bkgFiles, '', version+'AnalysisPlots/'+i[0]+cut1, i[0]+cut1, i[1], i[2], i[3], i[4], i[5], i[6], PU, version )
			elif ( 'qual' in process ):
				for cut1 in listCuts:
					if 'Boosted' in version: plotQuality( dataFile, bkgFiles, optGroom, i[0]+cut1, i[0]+cut1, i[1], i[2], i[3], i[4], i[5], i[6], PU, version )
					else: plotQuality( dataFile, bkgFiles, '', i[0]+cut1, i[0]+cut1, i[1], i[2], i[3], i[4], i[5], i[6], PU, version )
			
			elif 'mini' in process:
				for cut1 in listCuts:
					if '2D' in process: plot2DSignalBkg( signalFiles, bkgFiles, optGroom, i[0], i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], PU, version )
					else: plotSignalBkg( signalFiles, bkgFiles, optGroom, i[0]+cut1, i[0]+cut1, i[1], i[2], i[3], i[4], i[5], i[6], PU, version )
			
			elif 'Norm' in process:
				for cut1 in listCuts:
					#plotSignalBkg( signalFiles, bkgFiles, optGroom, version+'AnalysisPlots'+optGroom+'/'+i[0]+cut1, i[0]+cut1, i[1], i[2], i[3], i[4], i[5], i[6], PU, version, True )
					plotSignalBkg( signalFiles, bkgFiles, optGroom, i[0]+cut1, i[0]+cut1, i[1], i[2], i[3], i[4], i[5], i[6], PU, version, True )


			elif 'simple' in process:
				plotSimple( inputFileTTJets, 'TTJets', optGroom, i[0], i[1], i[2], i[3], i[4], PU )
				plotSimple( inputFileWJetsToQQ, 'WJets', optGroom, i[0], i[1], i[2], i[3], i[4], PU )
				plotSimple( inputFileZJetsToQQ, 'ZJets', optGroom, i[0], i[1], i[2], i[3], i[4], PU )
			
			elif 'sys' in process:
				for cut in listCuts: plotSystematics( signalFiles, optGroom, i[0]+cut, i[1], i[2], i[3], i[4], i[5], i[6], version, process )
			
			elif 'bkgEst' in process:
				if '2D' in process: 
					for bkg in bkgFiles: plot2DBkgEstimation( bkgFiles[ bkg ][0], bkg, optGroom, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], PU, version )
					for bkg in signalFiles: plot2DBkgEstimation( signalFiles[ bkg ][0], bkg, optGroom, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], PU, version )
					#plot2DBkgEstimation( dataFile, 'DATA', optGroom, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], PU, version )
				else: 
					tmpListCuts = selection[ 'RPVStopStopToJets_'+args.decay+'_M-'+str(mass) ][-2:]
					nameVarABCD = i[0]+'_'+tmpListCuts[0][0]+'Vs'+tmpListCuts[1][0]
					plotBkgEstimation( dataFile, bkgFiles, optGroom, nameVarABCD, i[1], i[2], i[3], i[4], i[5], i[6], PU, version )
