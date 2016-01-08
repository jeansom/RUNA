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
import argparse
try:
	from RUNA.RUNAnalysis.histoLabels import labels, labelAxis 
	from RUNA.RUNAnalysis.scaleFactors import scaleFactor as SF
	import RUNA.RUNAnalysis.CMS_lumi as CMS_lumi 
	import RUNA.RUNAnalysis.tdrstyle as tdrstyle
except ImportError:
	sys.path.append('../python')
	from histoLabels import labels, labelAxis 
	from scaleFactors import scaleFactor as SF
	import CMS_lumi as CMS_lumi 
	import tdrstyle as tdrstyle


gROOT.Reset()
gROOT.SetBatch()
gROOT.ForceStyle()
tdrstyle.setTDRStyle()

gStyle.SetOptStat(0)

def plotSignalBkg( signalFiles, bkgFiles, Grom, nameInRoot, name, xmin, xmax, rebinX, labX, labY, log, PU, version, Norm=False ):
	"""docstring for plot"""

	if 'mini' in process: outputFileName = name+'_'+Grom+'_RPVSt'+jj+mass+'_'+PU+'_PlusBkg_Mini'+version+'AnalysisPlots.'+ext 
	else: outputFileName = name+'_'+Grom+'_RPVSt'+jj+mass+'_'+PU+'_PlusBkg_'+version+'AnalysisPlots.'+ext 
	print 'Processing.......', outputFileName

	legend=TLegend(0.60,0.60,0.90,0.87)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.04)

	signalHistos = {}
	binWidth = 0
	maxList = []
	if len(signalFiles) > 0:
		for samples in signalFiles:
			signalHistos[ samples ] = signalFiles[ samples ][0].Get(nameInRoot)
			if rebinX > 1: signalHistos[ samples ].Rebin( rebinX )
			if signalFiles[ samples ][1] != 1: signalHistos[ samples ].Scale( signalFiles[ samples ][1] ) 
			legend.AddEntry( signalHistos[ samples ], signalFiles[ samples ][2], 'l' if Norm else 'f' )
			if Norm:
				signalHistos[ samples ].SetLineColor( signalFiles[ samples ][3] )
				signalHistos[ samples ].SetLineWidth( 3 )
				signalHistos[ samples ].Scale( 1 / signalHistos[ samples ].Integral() )
				maxList.append( signalHistos[ samples ].GetMaximum() )
			else:
				signalHistos[ samples ].SetFillStyle( 1001 )
				signalHistos[ samples ].SetFillColor( signalFiles[ samples ][3] )
			binWidth = signalHistos[ samples ].GetBinWidth( 1 )

	dummy = 0
	bkgHistos = {}
	if len(bkgFiles) > 0:
		for samples in bkgFiles:
			dummy += 1
			bkgHistos[ samples ] = bkgFiles[ samples ][0].Get(nameInRoot)
			if rebinX > 1: bkgHistos[ samples ].Rebin( rebinX )
			if bkgFiles[ samples ][1] != 1: bkgHistos[ samples ].Scale( bkgFiles[ samples ][1] ) 
			if (dummy == 1): hBkg = bkgHistos[ samples ].Clone()
			else: hBkg.Add( bkgHistos[ samples ].Clone() )
			legend.AddEntry( bkgHistos[ samples ], bkgFiles[ samples ][2], 'l' if Norm else 'f' )
			if Norm:
				bkgHistos[ samples ].SetLineColor( bkgFiles[ samples ][3] )
				bkgHistos[ samples ].SetLineWidth( 3 )
				bkgHistos[ samples ].Scale( 1 / bkgHistos[ samples ].Integral() )
				maxList.append( bkgHistos[ samples ].GetMaximum() )
			else:
				bkgHistos[ samples ].SetFillStyle( 1001 )
				bkgHistos[ samples ].SetFillColor( bkgFiles[ samples ][3] )
		

	'''
	for bin in range(0,  hSoSB.GetNbinsX()):
		hSoSB.SetBinContent(bin, 0.)
		hSoSB.SetBinError(bin, 0.)

	hSoSB2 = hSoSB.Clone()
	for ibin in range(0, hSoSB.GetNbinsX()):
	
		binContSignal = histos[ 'Signal' ].GetBinContent(ibin)
		binErrSignal = histos[ 'Signal' ].GetBinError(ibin)
		binContBkg = histos[ 'QCD' ].GetBinContent(ibin) + histos[ 'TTJets' ].GetBinContent(ibin) + histos[ 'WJets' ].GetBinContent(ibin) + histos[ 'ZJets' ].GetBinContent(ibin)    
		binErrBkg = histos[ 'QCD' ].GetBinError(ibin)
		try:
			value = binContSignal / TMath.Sqrt( binContSignal + binContBkg )
		except ZeroDivisionError: continue
		hSoSB.SetBinContent( ibin, value )
	'''
	CMS_lumi.extraText = "Preliminary Simulation"


	if not Norm:

		stackHisto = THStack('stackHisto', 'stack')
		for samples in bkgHistos: stackHisto.Add( bkgHistos[ samples ] )
		for samples in signalHistos: stackHisto.Add( signalHistos[ samples ] )

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
		if not (labX and labY): labels( name, PU, camp )
		else: labels( name, PU, camp, labX, labY )

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
		hSignal = signalHistos[ 'Signal' ].Clone()
		hSignalBkg = signalHistos[ 'Signal' ].Clone()
		hSignalBkg.Add( hBkg )
		hSignal.Divide( hSignalBkg )
		
		labelAxis( name, hSignal, Grom )
		hSignal.GetYaxis().SetTitleOffset(1.2)
		hSignal.GetXaxis().SetLabelSize(0.12)
		hSignal.GetXaxis().SetTitleSize(0.12)
		hSignal.GetYaxis().SetTitle("S / B")
		hSignal.GetYaxis().SetLabelSize(0.12)
		hSignal.GetYaxis().SetTitleSize(0.12)
		hSignal.GetYaxis().SetTitleOffset(0.45)
		hSignal.SetMaximum(0.7)
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
		labelAxis( name, signalHistos['Signal'], Grom )
		signalHistos['Signal'].Draw('hist')
		for sample in bkgHistos: bkgHistos[ samples ].Draw('hist same')
		signalHistos['Signal'].SetMaximum( 1.1 * max( maxList ) )

		CMS_lumi.lumi_13TeV = ''
		CMS_lumi.relPosX = 0.14
		CMS_lumi.CMS_lumi(can, 4, 0)
		legend.Draw()
		if not (labX and labY): labels( name, PU, camp )
		else: labels( name, PU, camp, labX, labY )

		can.SaveAs( 'Plots/'+outputFileName )
		del can


def plot2D( inFiles, sample, Grom, nameInRoot, name, titleXAxis, titleXAxis2, Xmin, Xmax, rebinx, Ymin, Ymax, rebiny, legX, legY, PU, version ):
	"""docstring for plot"""

	outputFileName = name+'_'+Grom+'_'+sample+'_'+camp+'_'+PU+'_'+version+'AnalysisPlots.'+ext 
	print 'Processing.......', outputFileName
	for samples in inFiles:
		h1 = inFiles[ samples ][0].Get( nameInRoot )
	#h1 = inFile.Get( 'AnalysisPlots'+Grom+'/'+name )
	#h1 = inFile.Get( 'TriggerEfficiency'+Grom+'/'+name )
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


def plotCutFlow( signalFiles, bkgFiles, Grom, name, xmax, log, PU, Norm=False ):
	"""docstring for plot"""

	outputFileName = name+'_'+Grom+'_RPVSt'+mass+'to'+jj+'_'+PU+'_Bkg_AnalysisPlots.'+ext 
	print 'Processing.......', outputFileName

	histos = {}
	if len(signalFiles) > 0:
		for samples in signalFiles:
			histos[ samples ] = signalFiles[ samples ][0].Get(version+'AnalysisPlots'+Grom+'/'+name)
			if signalFiles[ samples ][1] != 1: histos[ samples ].Scale( signalFiles[ samples ][1] ) 

	dummy = 0
	if len(bkgFiles) > 0:
		for samples in bkgFiles:
			dummy += 1
			histos[ samples ] = bkgFiles[ samples ][0].Get(version+'AnalysisPlots'+Grom+'/'+name)
			if bkgFiles[ samples ][1] != 1: histos[ samples ].Scale( bkgFiles[ samples ][1] ) 
			if (dummy == 1): hBkg = histos[ samples ].Clone()

	hSignal = histos[ 'Signal' ].Clone()
	hQCD = histos[ 'QCD' ].Clone()
	hTTJets = histos[ 'TTJets' ].Clone()
	hWJets = histos[ 'WJets' ].Clone()
	hWWTo4Q = histos[ 'WWTo4Q' ].Clone()
	hZJets = histos[ 'ZJets' ].Clone()
	hZZTo4Q = histos[ 'ZZTo4Q' ].Clone()
	hWZ = histos[ 'WZ' ].Clone()

	for bin in range(0,  hSignal.GetNbinsX()):
		hSignal.SetBinContent(bin, 0.)
		hSignal.SetBinError(bin, 0.)
		hQCD.SetBinContent(bin, 0.)
		hQCD.SetBinError(bin, 0.)
		hTTJets.SetBinContent(bin, 0.)
		hTTJets.SetBinError(bin, 0.)
		hWJets.SetBinContent(bin, 0.)
		hWJets.SetBinError(bin, 0.)
		hWWTo4Q.SetBinContent(bin, 0.)
		hWWTo4Q.SetBinError(bin, 0.)
		hZJets.SetBinContent(bin, 0.)
		hZJets.SetBinError(bin, 0.)
		hZZTo4Q.SetBinContent(bin, 0.)
		hZZTo4Q.SetBinError(bin, 0.)
		hWZ.SetBinContent(bin, 0.)
		hWZ.SetBinError(bin, 0.)
	
	totalEventsSignal = histos[ 'Signal' ].GetBinContent(1)
	totalEventsQCD = histos[ 'QCD' ].GetBinContent(1)
	totalEventsTTJets = histos[ 'TTJets' ].GetBinContent(1)
	totalEventsWJets = histos[ 'WJets' ].GetBinContent(1)
	totalEventsWWTo4Q = histos[ 'WWTo4Q' ].GetBinContent(1)
	totalEventsZJets = histos[ 'ZJets' ].GetBinContent(1)
	totalEventsZZTo4Q = histos[ 'ZZTo4Q' ].GetBinContent(1)
	totalEventsWZ = histos[ 'WZ' ].GetBinContent(1)
	#print totalEventsSignal, totalEventsQCD

	cutFlowSignalList = []
	cutFlowQCDList = []
	cutFlowTTJetsList = []
	cutFlowWJetsList = []
	cutFlowWWTo4QList = []
	cutFlowZJetsList = []
	cutFlowZZTo4QList = []
	cutFlowWZList = []

	for ibin in range(0, hQCD.GetNbinsX()+1):
	
		cutFlowSignalList.append( histos[ 'Signal' ].GetBinContent(ibin) )
		cutFlowQCDList.append( histos[ 'QCD' ].GetBinContent(ibin) )
		cutFlowTTJetsList.append( histos[ 'TTJets' ].GetBinContent(ibin) )
		cutFlowWJetsList.append( histos[ 'WJets' ].GetBinContent(ibin) )
		cutFlowWWTo4QList.append( histos[ 'WWTo4Q' ].GetBinContent(ibin) )
		cutFlowZJetsList.append( histos[ 'ZJets' ].GetBinContent(ibin) )
		cutFlowZZTo4QList.append( histos[ 'ZZTo4Q' ].GetBinContent(ibin) )
		cutFlowWZList.append( histos[ 'WZ' ].GetBinContent(ibin) )

		hSignal.SetBinContent( ibin , histos[ 'Signal' ].GetBinContent(ibin) / totalEventsSignal )
		hQCD.SetBinContent( ibin , histos[ 'QCD' ].GetBinContent(ibin) / totalEventsQCD )
		hTTJets.SetBinContent( ibin , histos[ 'TTJets' ].GetBinContent(ibin) / totalEventsTTJets )
		hWJets.SetBinContent( ibin , histos[ 'WJets' ].GetBinContent(ibin) / totalEventsWJets )
		hWWTo4Q.SetBinContent( ibin , histos[ 'WWTo4Q' ].GetBinContent(ibin) / totalEventsWWTo4Q )
		hZJets.SetBinContent( ibin , histos[ 'ZJets' ].GetBinContent(ibin) / totalEventsZJets )
		hZZTo4Q.SetBinContent( ibin , histos[ 'ZZTo4Q' ].GetBinContent(ibin) / totalEventsZZTo4Q )
		hWZ.SetBinContent( ibin , histos[ 'WZ' ].GetBinContent(ibin) / totalEventsWZ )
		
	hSB = hSignal.Clone()
	hBkg = hQCD.Clone()
	hBkg.Add( hTTJets )
	hBkg.Add( hWJets )
	hBkg.Add( hWWTo4Q )
	hBkg.Add( hZJets )
	hBkg.Add( hZZTo4Q )
	hBkg.Add( hWZ )
	hSB.Divide( hBkg )
	hSB.GetXaxis().SetBinLabel( ibin, '')
	print "Signal", cutFlowSignalList
	print "QCD", cutFlowQCDList
	print "TTJets", cutFlowTTJetsList
	print "WJets", cutFlowWJetsList
	print "WWTo4Q", cutFlowWWTo4QList
	print "ZJets", cutFlowZJetsList
	print "ZZTo4Q", cutFlowZZTo4QList
	print "WZ", cutFlowWZList
	print 'total', [ cutFlowQCDList[i] + cutFlowTTJetsList[i] +cutFlowWJetsList[i] + cutFlowWWTo4QList[i] + cutFlowZJetsList[i] + cutFlowZZTo4QList[i] + cutFlowWZList[i]  for i in range(len(cutFlowQCDList))]

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
	hWJets.SetLineWidth(2)
	hWJets.SetLineColor(kMagenta-4)
	hWWTo4Q.SetLineWidth(2)
	hWWTo4Q.SetLineColor(kMagenta-6)
	hZJets.SetLineWidth(2)
	hZJets.SetLineColor(kOrange-4)
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
	legend.AddEntry( hSignal, 'RPV #tilde{t}#rightarrow '+jj+' '+mass+' GeV' , 'l' )
	legend.AddEntry( hQCD, 'QCD', 'l' )
	legend.AddEntry( hTTJets, 't #bar{t} + Jets' , 'l' )
	legend.AddEntry( hWJets, 'W + Jets' , 'l' )
	legend.AddEntry( hWWTo4Q, 'WW (had)' , 'l' )
	legend.AddEntry( hZJets, 'Z + Jets' , 'l' )
	legend.AddEntry( hZZTo4Q, 'ZZ (had)' , 'l' )
	hSignal.GetYaxis().SetTitle( 'Percentage / '+str(binWidth) )
	hSignal.GetXaxis().SetRangeUser( 1, xmax )

	hSignal.SetMinimum(0.0001)
	hSignal.Draw()
	hQCD.Draw('same')
	hTTJets.Draw('same')
	hWJets.Draw('same')
	hWWTo4Q.Draw('same')
	hZJets.Draw('same')
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

def plotSimple( inFile, sample, Grom, name, xmax, labX, labY, log, PU, Norm=False ):
	"""docstring for plot"""

	outputFileName = name+'_'+sample+'_AnalysisPlots.'+ext 
	print 'Processing.......', outputFileName

	histo = inFile.Get( version+'AnalysisPlots'+Grom+'/'+name )

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

def plotDiffSample( inFileSample1, inFileSample2, sample1, sample2, Grom, name, xmax, labX, labY, log, Diff , Norm=False):
	"""docstring for plot"""

	outputFileName = name+'_'+Grom+'_RPVSt'+mass+'to'+jj+'_Diff'+Diff+'.'+ext 
	print 'Processing.......', outputFileName

	histos = {}
	histos[ 'Sample1' ] = inFileSample1.Get( version+'AnalysisPlots'+Grom+'/'+name )
	histos[ 'Sample2' ] = inFileSample2.Get( version+'AnalysisPlots'+Grom+'/'+name )

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

		labelAxis( name, histos['Sample1'], Grom )
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
		labelAxis( name, histos['Sample1'], Grom )
		if not (labX and labY): labels( name, '13 TeV - Scaled to '+lumi+' fb^{-1}', '' )
		else: labels( name, '13 TeV - Scaled to '+lumi+' fb^{-1}', '', labX, labY )

		can.SaveAs( 'Plots/'+outName )
		del can


def plotOptimization( inputFile, listHistos, tmpHisto ):
	"""docstring for plot"""

	outName = tmpHisto+'_Optimization.'+ext 
	print 'Processing.......', outName

	legend=TLegend(0.60,0.15,0.90,0.50)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.03)

	histos = {}
	dum = 1
	maxHisto = []
	for histo in listHistos:
		histos[ histo ] = inputFile.Get(histo)
		histos[ histo ].SetLineWidth(2)
		histos[ histo ].SetLineColor(dum)
		maxHisto.append( histos[ histo ].GetMaximum() )
		legend.AddEntry( histos[ histo ], histo, 'l' )
		dum += 1

	histos[ tmpHisto ].SetMaximum( 1.1* max( maxHisto ) ) 
	histos[ tmpHisto ].SetMinimum( 0 )

	can = TCanvas('c1', 'c1',  10, 10, 750, 500 )
	histos[ tmpHisto ].Draw()
	for iHisto in histos: 
		if iHisto != tmpHisto: histos[ iHisto ].Draw('hist same')

	histos[ tmpHisto ].GetYaxis().SetTitleOffset(0.8)
	histos[ tmpHisto ].GetYaxis().SetTitle( 'S/ Sqrt(S+B)' )
	histos[ tmpHisto ].GetXaxis().SetTitle( '' )
	legend.Draw()

	can.SaveAs( 'Plots/'+outName )
	del can

def plot2DOptimization( inFileSig, inFileBkg, Grom, name, titleXAxis, titleXAxis2, Xmin, Xmax, rebinx, Ymin, Ymax, rebiny, legX, legY, PU ):
	"""docstring for plot"""

	outputFileName = name+'_'+Grom+'_'+camp+'_'+PU+'_OptimizationPlots.'+ext 
	print 'Processing.......', utputFileName
	hSig = inFileSig.Get( name )
	hBkg = inFileBkg.Get( name )
	
	hD = hSig.Clone( "hD" )
	hsum = hSig.Clone( "hsum" )
	hsum.Add( hBkg )
	hD.Divide( hsum )

	hD.GetXaxis().SetTitle( titleXAxis )
	hD.GetYaxis().SetTitleOffset( 1.0 )
	hD.GetYaxis().SetTitle( titleXAxis2 )

	hD.GetXaxis().SetRangeUser( Xmin, Xmax )
	hD.GetYaxis().SetRangeUser( Ymin, Ymax )

	tdrStyle.SetPadRightMargin(0.12)
	can = TCanvas('c1', 'c1',  750, 500 )
	#can.SetLogz()
	#hD.SetMaximum(5000)
	hD.Draw('cont1')

	CMS_lumi.relPosX = 0.13
	CMS_lumi.CMS_lumi(can, 4, 0)
	if not (legX and legY): labels( name, PU, camp )
	else: labels( name, PU, camp, legX, legY )

	can.SaveAs( 'Plots/'+outputFileName )
	del can

def plotQuality( dataFile, bkgFiles, Grom, nameInRoot, name, xmin, xmax, rebinX, labX, labY, log, PU, version ):
	"""docstring for plot"""

	outputFileName = name+'_'+Grom+'_'+PU+'_dataQuality'+version+'Plots.'+ext
	print 'Processing.......', outputFileName

	histos = {}
	histos[ 'Data' ] = dataFile.Get(nameInRoot)
	if rebinX > 1: histos[ 'Data' ].Rebin( rebinX )

	dummy = 0
	for samples in bkgFiles:
		dummy += 1
		histos[ samples ] = bkgFiles[ samples ][0].Get(nameInRoot)
		if bkgFiles[ samples ][1] != 1: histos[ samples ].Scale( bkgFiles[ samples ][1] ) 
		if rebinX > 1: histos[ samples ].Rebin( rebinX )
		if (dummy == 1): hBkg = histos[ samples ].Clone()
		else: hBkg.Add( histos[ samples ].Clone() )

	hData = histos[ 'Data' ].Clone()
	hRatio = histos[ 'Data' ].Clone()
	hRatio.Divide( hBkg )
	
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

	legend=TLegend(0.60,0.75,0.90,0.87)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.04)
	legend.AddEntry( hData, 'Run2015D' , 'ep' )
	legend.AddEntry( hBkg, 'Background', 'l' )

	hBkg.SetLineColor(kRed-4)
	hData.SetMarkerStyle(8)

	tdrStyle.SetPadRightMargin(0.05)
	tdrStyle.SetPadLeftMargin(0.15)
	can = TCanvas('c1', 'c1',  10, 10, 750, 750 )
	pad1 = TPad("pad1", "Fit",0,0.207,1.00,1.00,-1)
	pad2 = TPad("pad2", "Pull",0,0.00,1.00,0.30,-1);
	pad1.Draw()
	pad2.Draw()

	pad1.cd()
	pad1.SetLogy() 	
	hData.Draw("E")
	hBkg.Draw('hist same')
	#hData.GetYaxis().SetTitleOffset(1.2)
	if xmax: hData.GetXaxis().SetRangeUser( xmin, xmax )
	hData.GetYaxis().SetTitle( 'Events / '+str(binWidth) )

	CMS_lumi.relPosX = 0.13
	CMS_lumi.CMS_lumi(pad1, 4, 0)
	#labelAxis( name, hData, Grom )
	legend.Draw()
	if not (labX and labY): labels( name, '', '' )
	else: labels( name, '', '', labX, labY )

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
	labelAxis( name, hRatio, Grom )
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
	hRatio.Draw()

	can.SaveAs( 'Plots/'+ outputFileName )
	del can

def plotSystematics( inFileSample, Grom, name, xmin, xmax, rebinX, labX, labY, log, version, proc):
	"""docstring for plot"""

	if 'JES' in proc: typeSys = 'JES'

	outputFileName = name+'_RPVSt'+mass+'to'+jj+'_'+typeSys+version+'.'+ext 
	print 'Processing.......', outputFileName

	histos = {}
	histos[ 'Nominal' ] = inFileSample[ 'Signal' ][0].Get( version+'AnalysisPlots'+Grom+'/'+name )
	histos[ 'Nominal' ].Scale( inFileSample[ 'Signal' ][1] )
	histos[ 'Up' ] = inFileSample[ 'Signal' ][0].Get( version+'AnalysisPlots'+Grom+typeSys+'Up/'+name )
	histos[ 'Up' ].Scale( inFileSample[ 'Signal' ][1] )
	histos[ 'Down' ] = inFileSample[ 'Signal' ][0].Get( version+'AnalysisPlots'+Grom+typeSys+'Down/'+name )
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

	labelAxis( name, histos['Nominal'], Grom )
	legend.Draw()
	CMS_lumi.extraText = "Preliminary Simulation"
	CMS_lumi.relPosX = 0.12
	CMS_lumi.CMS_lumi(can, 4, 0)
	if not (labX and labY): labels( name, '', '' )
	else: labels( name, '', '', labX, labY )

	can.SaveAs( 'Plots/'+outputFileName )
	del can

def tmpplotDiff( dataFile, name1, name2 ):
	"""docstring for plot"""

	outputFileName = name1.replace('BoostedAnalysisPlotsPruned/', '')+'_'+name2.replace('BoostedAnalysisPlotsPruned/', '')+'_'+PU+'_bkgShapeDiff'+version+'Plots.'+ext
	print 'Processing.......', outputFileName

	h1 = dataFile.Get( name1 )
	h1.Scale( 1/h1.Integral() )
	h2 = dataFile.Get( name2 )
	h2.Scale( 1/h2.Integral() )

	tmph1 = h1.Clone()
	tmph2 = h2.Clone()
	tmph1.Divide( tmph2 )

	binWidth = h1.GetBinWidth(1)

	legend=TLegend(0.60,0.75,0.90,0.87)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.04)
	legend.AddEntry( h1, 'Signal Region' , 'l' )
	legend.AddEntry( h2, 'Bkg Region', 'pl' )

	h1.SetLineColor(kRed-4)
	h1.GetXaxis().SetRangeUser( 0, 350 )

	tdrStyle.SetPadRightMargin(0.05)
	tdrStyle.SetPadLeftMargin(0.15)
	can = TCanvas('c1', 'c1',  10, 10, 750, 750 )
	pad1 = TPad("pad1", "Fit",0,0.207,1.00,1.00,-1)
	pad2 = TPad("pad2", "Pull",0,0.00,1.00,0.30,-1);
	pad1.Draw()
	pad2.Draw()

	pad1.cd()
	#if log: pad1.SetLogy() 	
	h1.Draw("hist")
	h2.Draw('same')

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
	
	labelAxis( name1, tmph1, 'Pruned' )
	tmph1.GetXaxis().SetRangeUser( 0, 350 )
	tmph1.SetMarkerStyle(8)
	tmph1.GetXaxis().SetTitleOffset(1.1)
	tmph1.GetXaxis().SetLabelSize(0.12)
	tmph1.GetXaxis().SetTitleSize(0.12)
	tmph1.GetYaxis().SetTitle("Ratio")
	tmph1.GetYaxis().SetLabelSize(0.12)
	tmph1.GetYaxis().SetTitleSize(0.12)
	tmph1.GetYaxis().SetTitleOffset(0.55)
	#if( tmph1.GetMaximum() > 2 ): tmph1.SetMaximum( 2.0 )
	tmph1.SetMaximum( 1.5 )
	tmph1.SetMinimum( 0.5 )
	tmph1.Draw()

	can.SaveAs( 'Plots/'+ outputFileName )
	del can



if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--proc', action='store', default='1D', help='Process to draw, example: 1D, 2D, MC.' )
	parser.add_argument('-d', '--decay', action='store', default='jj', help='Decay, example: jj, bj.' )
	parser.add_argument('-v', '--version', action='store', default='Boosted', help='Boosted or non version, example: Boosted' )
	parser.add_argument('-g', '--grom', action='store', default='Pruned', help='Grooming Algorithm, example: Pruned, Filtered.' )
	parser.add_argument('-m', '--mass', action='store', default='100', help='Mass of Stop, example: 100' )
	parser.add_argument('-C', '--cut', action='store', default='_cutMassAsym', help='cut, example: cutDEta' )
	parser.add_argument('-pu', '--PU', action='store', default='Asympt25ns', help='PU, example: PU40bx25.' )
	parser.add_argument('-s', '--single', action='store', default='all', help='single histogram, example: massAve_cutDijet.' )
	parser.add_argument('-q', '--QCD', action='store', default='Pt', help='Type of QCD binning, example: HT.' )
	parser.add_argument('-c', '--campaign', action='store', default='RunIISpring15MiniAODv2-74X', help='Campaign, example: PHYS14.' )
	parser.add_argument('-l', '--lumi', action='store', type=float, default=149.9, help='Luminosity, example: 1.' )
	#parser.add_argument('-t', '--trigger', action='store', default='all', help='Trigger used, example PFHT800.' )
	parser.add_argument('-e', '--extension', action='store', default='png', help='Extension of plots.' )

	try:
		args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)

	process = args.proc
	jj = args.decay
	PU = args.PU
	qcd = args.QCD
	camp = args.campaign
	lumi = args.lumi
	histo = args.single
	mass = args.mass
	cut = args.cut
	grom = args.grom
	single = args.single
	version = args.version
	#triggerUsed = args.trigger
	ext = args.extension
	
	bkgFiles = {}
	signalFiles = {}
	CMS_lumi.extraText = "Preliminary"
	lumi = 2431.937
	CMS_lumi.lumi_13TeV = "2.43 fb^{-1}"
	QCDSF = 0.92

	if ( 'mini' in process ) or ( '2dOpt' in process ):
		signalFiles[ 'Signal' ] = [ TFile.Open('Rootfiles/RUNMini'+version+'Analysis_RPVStopStopToJets_UDD312_M-'+str(mass)+'-madgraph_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'), 1, 'RPV #tilde{t}#rightarrow '+jj+' '+str(mass)+' GeV', kRed-4]
		bkgFiles[ 'QCD' ] = [ TFile.Open('Rootfiles/RUNMini'+version+'Analysis_QCDPtAll_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'), QCDSF, 'QCD', kBlue-4 ]
		bkgFiles[ 'TTJets' ] = [ TFile.Open('Rootfiles/RUNMini'+version+'Analysis_TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'),	1, 't #bar{t} + Jets', kGreen ]
		bkgFiles[ 'WJets' ] = [ TFile.Open('Rootfiles/RUNMini'+version+'Analysis_WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'), 1 , 'W + Jets', kMagenta ]
		bkgFiles[ 'WWTo4Q' ] = [ TFile.Open('Rootfiles/RUNMini'+version+'Analysis_WWTo4Q_13TeV-powheg_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'), 1 , 'WW (had)', kMagenta+2 ]
		bkgFiles[ 'ZJets' ] = [ TFile.Open('Rootfiles/RUNMini'+version+'Analysis_ZJetsToQQ_HT600toInf_13TeV-madgraph_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'), 1, 'Z + Jets', kOrange ]
		bkgFiles[ 'ZZTo4Q' ] = [ TFile.Open('Rootfiles/RUNMini'+version+'Analysis_ZZTo4Q_13TeV_amcatnloFXFX_madspin_pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'), 1, 'ZZ (had)', kOrange+2 ]
		#bkgFiles[ 'WZ' ] = [ TFile.Open('Rootfiles/RUNMini'+version+'Analysis_WZ_TuneCUETP8M1_13TeV-pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'), 1, 'WZ', kCyan ]
	else:
		#dataFile = TFile.Open('Rootfiles/RUNAnalysis_JetHTRun2015D-All_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v02.root')
		dataFile = TFile.Open('Rootfiles/RUNAnalysis_JetHTRun2015D-All_v09_v01.root')
		signalFiles[ 'Signal' ] = [ TFile.Open('Rootfiles/RUNAnalysis_RPVStopStopToJets_UDD312_M-'+str(mass)+'-madgraph_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'), lumi, 'RPV #tilde{t}#rightarrow '+jj+' '+str(mass)+' GeV', kRed-4]
		bkgFiles[ 'QCD' ] = [ TFile.Open('Rootfiles/RUNAnalysis_QCDPtAll_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'), QCDSF*lumi, 'QCD', kBlue-4 ]
		bkgFiles[ 'TTJets' ] = [ TFile.Open('Rootfiles/RUNAnalysis_TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'),	lumi, 't #bar{t} + Jets', kGreen ]
		bkgFiles[ 'WJets' ] = [ TFile.Open('Rootfiles/RUNAnalysis_WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'), lumi , 'W + Jets', kMagenta ]
		bkgFiles[ 'WWTo4Q' ] = [ TFile.Open('Rootfiles/RUNAnalysis_WWTo4Q_13TeV-powheg_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'), lumi , 'WW (had)', kMagenta+2 ]
		bkgFiles[ 'ZJets' ] = [ TFile.Open('Rootfiles/RUNAnalysis_ZJetsToQQ_HT600toInf_13TeV-madgraph_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'), lumi, 'Z + Jets', kOrange ]
		bkgFiles[ 'ZZTo4Q' ] = [ TFile.Open('Rootfiles/RUNAnalysis_ZZTo4Q_13TeV_amcatnloFXFX_madspin_pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'), lumi, 'ZZ (had)', kOrange+2 ]
		bkgFiles[ 'WZ' ] = [ TFile.Open('Rootfiles/RUNAnalysis_WZ_TuneCUETP8M1_13TeV-pythia8_RunIISpring15MiniAODv2-74X_Asympt25ns_v09_v03.root'), lumi, 'WZ', kCyan ]
			

	dijetlabX = 0.85
	dijetlabY = 0.55
	subjet112vs212labX = 0.7
	subjet112vs212labY = 0.88
	jetMassHTlabX = 0.85
	jetMassHTlabY = 0.20
	polAnglabX = 0.2
	polAnglabY = 0.88
	taulabX = '' #0.6
	taulabY = '' #0.40
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

		[ '2D', 'Boosted', 'jet1Subjet112vs212MassRatio_cutDijet', 'm_{1}/m_{12}', 'm_{2}/m_{12}', '', '', 1, '', '', 1, subjet112vs212labX, subjet112vs212labY  ],
		[ '2D', 'Boosted', 'jet1Subjet1JetvsSubjet2JetMassRatio_cutDijet', 'm_{1}/M_{12}', 'm_{2}/M_{12}', '', '', 1, '', '', 1, subjet112vs212labX, subjet112vs212labY  ],
		[ '2D', 'Boosted', 'jet2Subjet112vs212MassRatio_cutDijet', 'm_{3}/m_{34}', 'm_{4}/m_{34}', '', '', 1, '', '', 1, subjet112vs212labX, subjet112vs212labY  ],
		[ '2D', 'Boosted', 'jet2Subjet1JetvsSubjet2JetMassRatio_cutDijet', 'm_{3}/M_{34}', 'm_{4}/M_{34}', '', '', 1, '', '', 1, subjet112vs212labX, subjet112vs212labY  ],
		[ '2D', 'Boosted', 'subjet12Mass_cutDijet', 'm_{1}', 'm_{2}', '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],
		[ '2D', 'Boosted', 'dijetCorr_cutDijet', '#eta_{sjet1}', '#eta_{sjet2}', '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],
		[ '2D', 'Boosted', 'dijetCorrPhi_cutDijet', '#phi_{sjet1}', '#phi_{sjet2}', '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],
		[ '2D', 'Boosted', 'subjet112vs212MassRatio_cutDijet', 'm_{1}/m_{12}', 'm_{2}/m_{12}', '', '', 1, '', '', 1, subjet112vs212labX, subjet112vs212labY  ],
		[ '2D', 'Boosted', 'subjet1JetvsSubjet2JetMassRatio_cutDijet', 'm_{1}/M_{12}', 'm_{2}/M_{12}', '', '', 1, '', '', 1, subjet112vs212labX, subjet112vs212labY  ],
		[ '2D', 'Boosted', 'subjetPolAngle13412vs31234_cutDijet', 'cos #psi_{1(34)}^{[12]}', 'cos #psi_{3(12)}^{[34]}', polAngXmin, polAngXmax, 1, polAngXmin, polAngXmax, 1, cosPhilabX, cosPhilabY  ],
		[ '2D', 'Boosted', 'mu1234_cutDijet', '', '', '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],
		[ '2D', 'Boosted', 'mu3412_cutDijet', '', '', '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],
		[ '2D', 'Boosted', 'dalitz1234_cutDijet', 'X', 'Y', '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],
		[ '2D', 'Boosted', 'dalitz3412_cutDijet', 'X', 'Y', '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],
		[ '2D', 'Boosted', 'leadMassHT_cutDijet', 'Leading Jet Mass [GeV]', 'HT [GeV]', 0, massMaxX, 1, 100, HTMaxX, 1, jetMassHTlabX, jetMassHTlabY],

		#[ '2D', 'Boosted', 'subjet12Mass_cutAsym', 'm_{1}', 'm_{2}', '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],
		[ '2D', 'Boosted', 'dijetCorr_cutAsym', '#eta_{sjet1}', '#eta_{sjet2}', '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],
		[ '2D', 'Boosted', 'dijetCorrPhi_cutAsym', '#phi_{sjet1}', '#phi_{sjet2}', '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],
		#[ '2D', 'Boosted', 'subjet112vs212MassRatio_cutAsym', 'm_{1}/m_{12}', 'm_{2}/m_{12}', '', '', 1, '', '', 1, subjet112vs212labX, subjet112vs212labY  ],
		#[ '2D', 'Boosted', 'subjet1JetvsSubjet2JetMassRatio_cutAsym', 'm_{1}/M_{12}', 'm_{2}/M_{12}', '', '', 1, '', '', 1, subjet112vs212labX, subjet112vs212labY  ],
		#[ '2D', 'Boosted', 'subjetPolAngle13412vs31234_cutAsym', 'cos #psi_{1(34)}^{[12]}', 'cos #psi_{3(12)}^{[34]}', '', '', 1, '', '', 1, '', ''  ],
		#[ '2D', 'Boosted', 'mu1234_cutAsym', '', '', 1, '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],
		#[ '2D', 'Boosted', 'mu3412_cutAsym', '', '', 1, '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],
		#[ '2D', 'Boosted', 'dalitz1234_cutAsym', 'X', 'Y', '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],
		#[ '2D', 'Boosted', 'dalitz3412_cutAsym', 'X', 'Y', '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],

		#[ '2D', 'Boosted', 'subjet12Mass_cutCosTheta', 'm_{1}', 'm_{2}', '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],
		#[ '2D', 'Boosted', 'dijetCorr_cutCosTheta', '#eta_{sjet1}', '#eta_{sjet2}', '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],
		#[ '2D', 'Boosted', 'dijetCorrPhi_cutCosTheta', '#phi_{sjet1}', '#phi_{sjet2}', '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],
		#[ '2D', 'Boosted', 'subjet112vs212MassRatio_cutCosTheta', 'm_{1}/m_{12}', 'm_{2}/m_{12}', '', '', 1, '', '', 1, subjet112vs212labX, subjet112vs212labY  ],
		#[ '2D', 'Boosted', 'subjet1JetvsSubjet2JetMassRatio_cutCosTheta', 'm_{1}/M_{12}', 'm_{2}/M_{12}', '', '', 1, '', '', 1, subjet112vs212labX, subjet112vs212labY  ],
		#[ '2D', 'Boosted', 'subjetPolAngle13412vs31234_cutCosTheta', 'cos #psi_{1(34)}^{[12]}', 'cos #psi_{3(12)}^{[34]}', '', '', 1, '', '', 1, '', ''  ],
		#[ '2D', 'Boosted', 'mu1234_cutCosTheta', '', '', 1, '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],
		#[ '2D', 'Boosted', 'mu3412_cutCosTheta', '', '', 1, '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],
		#[ '2D', 'Boosted', 'dalitz1234_cutCosTheta', 'X', 'Y', '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],
		#[ '2D', 'Boosted', 'dalitz3412_cutCosTheta', 'X', 'Y', '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],
		[ '2D', 'Resolved', 'deltavsMassAve_cutBestPair', 'Average dijet mass [GeV]', 'Delta',  '', '', 1, '', '', 1, dijetlabX, dijetlabY ],
		[ '2D', 'Resolved', 'dijetsEta_cutBestPair', '#eta dijet1', '#eta dijet2',  '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],

		[ '2dmini', 'Boosted', 'massAsymVsmassAve_SR', 'Mass Asymmetry', 'Average Pruned Mass [GeV]',  '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],
		[ '2dmini', 'Boosted', 'massAsymVsHT_SR', 'Mass Asymmetry', 'HT [GeV]',  '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],
		[ '2dmini', 'Boosted', 'massAsymVsjet1Tau21_SR', 'Mass Asymmetry', 'Leading jet #tau_{21}',  '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],
		[ '2dmini', 'Boosted', 'massAsymVsjet2Tau21_SR', 'Mass Asymmetry', '2nd Leading jet #tau_{21}',  '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],
		[ '2dmini', 'Boosted', 'massAsymVsjet1Tau31_SR', 'Mass Asymmetry', 'Leading jet #tau_{31}',  '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],
		[ '2dmini', 'Boosted', 'massAsymVsjet2Tau31_SR', 'Mass Asymmetry', '2nd Leading jet #tau_{31}',  '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],
		[ '2dmini', 'Boosted', 'massAsymVsjet1Pt_SR', 'Mass Asymmetry', 'Leading jet p_{T} [GeV]',  '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],
		[ '2dmini', 'Boosted', 'massAsymVsjet2Pt_SR', 'Mass Asymmetry', '2nd Leading jet p_{T} [GeV]',  '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],
		[ '2dmini', 'Boosted', 'massAsymVsmassAve_CR', 'Mass Asymmetry', 'Average Pruned Mass [GeV]',  '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],
		[ '2dmini', 'Boosted', 'massAsymVsHT_CR', 'Mass Asymmetry', 'HT [GeV]',  '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],
		[ '2dmini', 'Boosted', 'massAsymVsjet1Tau21_CR', 'Mass Asymmetry', 'Leading jet #tau_{21}',  '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],
		[ '2dmini', 'Boosted', 'massAsymVsjet2Tau21_CR', 'Mass Asymmetry', '2nd Leading jet #tau_{21}',  '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],
		[ '2dmini', 'Boosted', 'massAsymVsjet1Tau31_CR', 'Mass Asymmetry', 'Leading jet #tau_{31}',  '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],
		[ '2dmini', 'Boosted', 'massAsymVsjet2Tau31_CR', 'Mass Asymmetry', '2nd Leading jet #tau_{31}',  '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],
		[ '2dmini', 'Boosted', 'massAsymVsjet1Pt_CR', 'Mass Asymmetry', 'Leading jet p_{T} [GeV]',  '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],
		[ '2dmini', 'Boosted', 'massAsymVsjet2Pt_CR', 'Mass Asymmetry', '2nd Leading jet p_{T} [GeV]',  '', '', 1, '', '', 1, dijetlabX, dijetlabY  ],

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

		[ 'qual', 'Boosted', 'jet1Pt', 100, 1500, 0.92, 0.8, False],
		[ 'qual', 'Boosted', 'jet1Eta', -3, 3, 0.92, 0.8, False],
		[ 'qual', 'Boosted', 'jet1Mass', 0, 1000, 0.92, 0.8, True],
		[ 'qual', 'Boosted', 'jet2Pt', 100, 1500, 0.92, 0.8, False],
		[ 'qual', 'Boosted', 'jet2Eta', -3, 3, 0.92, 0.8, False],
		[ 'qual', 'Boosted', 'jet2Mass', 0, 1000, 0.92, 0.8, True],
		[ 'qual', 'Boosted', 'jetNum', '', '', 0.92, 0.8, True],
		[ 'qual', 'Boosted', 'HT', 700, 2000, 0.92, 0.8, True],
		[ 'qual', 'Boosted', 'MET', 0, 100, 0.92, 0.8, False],
		[ 'qual', 'Boosted', 'massAve', 0, 400, 0.92, 0.8, False],
		#[ 'qual', 'Boosted', 'subjetPtRatio', '', '', '', '', True],
		[ 'qual', 'Boosted', 'deltaEtaDijet', '', '', '', '', True],
		[ 'qual', 'Boosted', 'massAsymmetry', '', '', 0.85, 0.45, False],
		[ 'qual', 'Boosted', 'jet1CosThetaStar', '', '', '', '', False],
		[ 'qual', 'Boosted', 'jet2CosThetaStar', '', '', '', '', False],
		[ 'qual', 'Boosted', 'jet1Tau21', '', '', 0.85, 0.45, False],
		[ 'qual', 'Boosted', 'jet2Tau21', '', '', 0.85, 0.45, False],
		[ 'qual', 'Boosted', 'jet1Tau31', '', '', 0.85, 0.45, False],
		[ 'qual', 'Boosted', 'jet2Tau31', '', '', 0.85, 0.45, False],
		[ 'qual', 'Resolved', 'jet1Pt', 100, 1500, 0.85, 0.45, True],
		[ 'qual', 'Resolved', 'jet2Pt', 0, 1500, 0.85, 0.45, True],
		[ 'qual', 'Resolved', 'jet3Pt', 0, 500, 0.85, 0.45, True],
		[ 'qual', 'Resolved', 'jet4Pt', 0, 300, 0.85, 0.45, True],
		[ 'qual', 'Resolved', 'HT', 700, 2000, 0.85, 0.45, True],
		[ 'qual', 'Resolved', 'jetNum', '', '', 0.85, 0.45, True],
		[ 'qual', 'Resolved', 'massAve', 0, 1000, 2, '', '', True],
		[ 'jetIDQual', version, 'neutralHadronEnergy', '', '', 0.85, 0.45, True],
		[ 'jetIDQual', version, 'neutralEmEnergy', '', '', 0.85, 0.45, True],
		[ 'jetIDQual', version, 'chargedHadronEnergy', '', '', 0.85, 0.45, True],
		[ 'jetIDQual', version, 'chargedEmEnergy', '', '', 0.85, 0.45, True],
		[ 'jetIDQual', version, 'chargedMultiplicity', '', '', 0.85, 0.45, True],
		[ 'jetIDQual', version, 'numConst', '', '', 0.85, 0.45, True],
		[ 'jetIDQual', version, 'jetPt', 100, 1500, 0.92, 0.8, False],
		[ 'jetIDQual', version, 'jetEta', -3, 3, 0.92, 0.8, False],
		[ 'jetIDQual', 'Boosted', 'jetMass', 0, 1000, 0.92, 0.8, True],
		[ 'jetIDQual', version, 'NPV', 0, 50, 0.85, 0.45, False],
		[ 'jetIDQual', version, 'NPV_NOPUWeight', '', '', 0.85, 0.45, False],
		[ 'jetIDQual', version, 'MET', '', '', 0.85, 0.45, False],

		[ 'Norm', 'Boosted', 'NPV', '', '', 1, '', '', False],
		#[ 'Norm', 'Boosted', 'jet1Subjet1Pt', '', '', '', '', True],
		#[ 'Norm', 'Boosted', 'jet1Subjet2Pt', '', '', '', True],
		#[ 'Norm', 'Boosted', 'jet2Subjet1Pt', '', '', '', True],
		#[ 'Norm', 'Boosted', 'jet2Subjet2Pt', '', '', '', True],
		#[ 'Norm', 'Boosted', 'jet1Subjet1Mass', '', '', '', True],
		#[ 'Norm', 'Boosted', 'jet1Subjet2Mass', '', '', '', True],
		#[ 'Norm', 'Boosted', 'jet2Subjet1Mass', '', '', '', True],
		#[ 'Norm', 'Boosted', 'jet2Subjet2Mass', '', '', '', True],
		[ 'Norm', 'Boosted', 'jet1Tau1', '', '', 1, taulabX, taulabY, False],
		[ 'Norm', 'Boosted', 'jet1Tau2', '', '', 1, taulabX, taulabY, False],
		[ 'Norm', 'Boosted', 'jet1Tau3', '', '', 1, taulabX, taulabY, False],
		[ 'Norm', 'Boosted', 'jet1Tau21', '', '', 1, taulabX, taulabY, False],
		[ 'Norm', 'Boosted', 'jet1Tau31', '', '', 1, taulabX, taulabY, False],
		[ 'Norm', 'Boosted', 'jet1Tau32', '', '', 1, taulabX, taulabY, False],
		[ 'Norm', 'Boosted', 'jet2Tau21', '', '', 1, taulabX, taulabY, False],
		[ 'Norm', 'Boosted', 'jet2Tau31', '', '', 1, taulabX, taulabY, False],
		[ 'Norm', 'Boosted', 'jet2Tau32', '', '', 1, taulabX, taulabY, False],
		[ 'Norm', 'Boosted', 'jet1SubjetPtRatio', '', '', 1, '', '', True],
		[ 'Norm', 'Boosted', 'jet2SubjetPtRatio', '', '', 1, '', '', True],
		[ 'Norm', 'Boosted', 'subjetPtRatio', '', '', 1, '', '', True],
		[ 'Norm', 'Boosted', 'massAsymmetry', '', '', 1, 0.55, 0.83, False],
		[ 'Norm', 'Boosted', 'jet1CosThetaStar', '', '', 1, '', '', False],
		[ 'Norm', 'Boosted', 'jet2CosThetaStar', '', '', 1, '', '', False],
		[ 'Norm', 'Boosted', 'deltaEtaDijet', '', '', 1, '', '', False],
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

		[ 'CF', version, 'cutflow', 10, True],
		[ 'CF', version, 'cutflowSimple', 10, True],

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

		#[ 'mini', version, 'massAve_NOMassAsymTau21CosTheta', 0, massMaxX, 1, '', '', False],
		[ 'mini', version, 'massAve_cutMassAsym', 0, massMaxX, 1, '', '', False],
		#[ 'mini', version, 'massAve_Tau21NOCosTheta', 0, massMaxX, 1, '', '', False],
		#[ 'mini', version, 'massAve_NOMassAsymTau21', 0, massMaxX, 1, '', '', False],
		[ '2dOpt', 'massAveVsHT', 'Average Pruned Mass [GeV]', 'HT [GeV]', 0, massMaxX, 1, 700, HTMaxX, 1, jetMassHTlabX, jetMassHTlabY],
		[ '2dOpt', 'massAsymVscosThetaStar', 'Mass asymmetry', 'cos #theta^{*}', 0, 1, 1, 0, 1, 1, jetMassHTlabX, jetMassHTlabY],

		]

	if 'all' in single: Plots = [ x[2:] for x in plotList if ( ( x[0] in process ) and ( x[1] in version ) )  ]
	else: Plots = [ y[2:] for y in plotList if ( ( y[0] in process ) and ( y[1] in version ) and ( y[2] in single ) )  ]

	if 'Resolved' in version: grom =  '' 
	if 'all' in grom: Grommers = [ '', 'Trimmed', 'Pruned', 'Filtered', "SoftDrop" ]
	else: Grommers = [ grom ]

	if 'all' in cut: 
		if 'Boosted' in version: selection = [ '_cutDijet', '_cutMassAsym', '_cutTau21', '_cutCosTheta', '_cutDEta' ]
		else: selection = [ '_cutMassRes', '_cutDelta', '_cutEtaBand', '_cutDeltaR', '_cutCosTheta', '_cutDEta', '_cutMassPairing' ]
	#elif 'NO' in cut: selection = [ '_cutNOMassAsym', '_cutTau21_NOMA', '_cutCosTheta_NOMA', '_cutDEta_NOMA' ]
	else: selection = [ cut ]

	if 'opt' in process:
		inputFile = TFile('Rootfiles/RUNOptimizationStudies_v0.root')
		plotOptimization( inputFile, [ 'massAsym', 'J1CosTheta', 'J2CosTheta', 'J1Tau21', 'J2Tau21', 'J1Tau31', 'J2Tau31', 'J1SubjetPtRatio', 'J2SubjetPtRatio' ], 'massAsym' )
		#plotOptimization( inputFile, [ 'massAsym', 'deltaEta', 'J1CosTheta', 'J2CosTheta', 'J1Tau21', 'J2Tau21', 'J1Tau31', 'J2Tau31', 'J1SubjetPtRatio', 'J2SubjetPtRatio' ] )
		plotOptimization( inputFile, [ 'MA_J1CosTheta', 'MA_J2CosTheta', 'MA_J1Tau21', 'MA_J2Tau21', 'MA_J1Tau31', 'MA_J2Tau31', 'MA_J1SubjetPtRatio', 'MA_J2SubjetPtRatio' ], 'MA_J1Tau21' )
		plotOptimization( inputFile, [ 'MAT21_J1CosTheta', 'MAT21_J2CosTheta', 'MAT21_J1Tau31', 'MAT21_J2Tau31', 'MAT21_J1SubjetPtRatio', 'MAT21_J2SubjetPtRatio' ], 'MAT21_J1CosTheta' )
		plotOptimization( inputFile, [ 'MAT21CTS_J1Tau31', 'MAT21CTS_J2Tau31', 'MAT21CTS_J1SubjetPtRatio', 'MAT21CTS_J2SubjetPtRatio' ], 'MAT21CTS_J1Tau31' )
	elif 'tmp' in process:
		tmpplotDiff( TFile.Open('Rootfiles/RUNAnalysis_QCDPtAll_RunIISpring15MiniAODv2-74X_Asympt25ns_v08_v03.root'), 'BoostedAnalysisPlotsPruned/massAve_cutCosTheta', 'BoostedAnalysisPlotsPruned/massAve_NOMassCutCosTheta'  )

	else:
		for i in Plots:
			for optGrom in Grommers:
				if '2D' in process: 
					plot2D( signalFiles, 'RPVStto'+jj, optGrom, version+'AnalysisPlots'+Grom+'/'+[0], i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], PU, version )
					plot2D( bkgFiles, 'QCD', optGrom, version+'AnalysisPlots'+Grom+'/'+[0], i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], PU, version )
					#plot2D( inputFileTTJets, 'TTJets', optGrom, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], PU, version )
					#plot2D( inputFileWJetsToQQ, 'WJets', optGrom, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], PU, version )
					#plot2D( inputFileZJetsToQQ, 'ZJets', optGrom, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], PU, version )
				elif '2dmini' in process: 
					plot2D( signalFiles, 'RPVStto'+jj, optGrom, i[0], i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], PU, version )
					plot2D( bkgFiles, 'QCD', optGrom, i[0], i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], PU, version )

				elif '1D' in process:
					for cut1 in selection:
						plotSignalBkg( signalFiles, bkgFiles, optGrom, version+'AnalysisPlots'+optGrom+'/'+i[0]+cut1, i[0]+cut1, i[1], i[2], i[3], i[4], i[5], i[6], PU, version )
				
				elif ( ( 'qual' in process ) or ( 'jetIDQual' in process ) ):
					for cut1 in selection:
						if 'Boosted' in version: plotQuality( dataFile, bkgFiles, optGrom, version+'AnalysisPlots'+optGrom+'/'+i[0]+cut1, i[0]+cut1, i[1], i[2], i[3], i[4], i[5], i[6], PU, version )
						else: plotQuality( dataFile, bkgFiles, '', version+'AnalysisPlots/'+i[0]+cut1, i[0]+cut1, i[1], i[2], i[3], i[4], i[5], i[6], PU, version )
				
				elif 'mini' in process:
					plotSignalBkg( signalFiles, bkgFiles, optGrom, i[0], i[0], i[1], i[2], i[3], i[4], i[5], i[6], PU, version )
				
				elif 'Norm' in process:
					for cut1 in selection:
						plotSignalBkg( signalFiles, bkgFiles, optGrom, version+'AnalysisPlots'+optGrom+'/'+i[0]+cut1, i[0]+cut1, i[1], i[2], i[3], i[4], i[5], i[6], PU, version, True )

				elif 'CF' in process:
					plotCutFlow( signalFiles, bkgFiles, optGrom, i[0], i[1], i[2], PU, True )

				elif 'simple' in process:
					plotSimple( inputFileTTJets, 'TTJets', optGrom, i[0], i[1], i[2], i[3], i[4], PU )
					plotSimple( inputFileWJetsToQQ, 'WJets', optGrom, i[0], i[1], i[2], i[3], i[4], PU )
					plotSimple( inputFileZJetsToQQ, 'ZJets', optGrom, i[0], i[1], i[2], i[3], i[4], PU )
				
				elif '2dOpt' in process: 
					plot2DOptimization( inputMiniFileSignal, inputMiniFileQCD, optGrom, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], PU )
				elif 'sys' in process:
					for cut in selection: plotSystematics( signalFiles, optGrom, i[0]+cut, i[1], i[2], i[3], i[4], i[5], i[6], version, process )
				
