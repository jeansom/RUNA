#!/usr/bin/env python
'''
File: DrawHistogram.py
Author: Alejandro Gomez Espinosa
Email: gomez@physics.rutgers.edu
Description: My Draw histograms. Check for options at the end.
'''

#from ROOT import TFile, TH1F, THStack, TCanvas, TMath, gROOT, gPad
from ROOT import *
from tdrstyle import setSelection
import time, os, math, sys
import CMS_lumi, tdrstyle
import argparse


gROOT.Reset()
gROOT.SetBatch()
#setTDRStyle()
#gROOT.SetStyle('tdrStyle')
#set the tdr style
gROOT.ForceStyle()
tdrstyle.setTDRStyle()
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"


gStyle.SetOptStat(0)

def labels( name, PU, camp, X=0.90, Y=0.70, align='right', listSet=[] ):
	if 'cutDijet' in name: setSelection( [ camp+' - '+PU, triggerUsed, 'jet p_{T} > '+cutjPt+' GeV', 'jet |#eta| < 2.4', 'numJets > 1' ] , X, Y, align)
	elif ( 'cutAsym' in name ) or ('cutMassAsym' in name): setSelection( [ camp+' - '+PU, triggerUsed, 'numJets > 1', 'A < 0.1' ], X, Y, align )
	elif 'cutCosTheta' in name: setSelection( [ camp+' - '+PU, triggerUsed,  'numJets > 1','A < 0.1', '|cos(#theta*)| < 0.3'], X, Y, align )
	elif 'cutSubjetPtRatio' in name: setSelection( [ camp+' - '+PU, triggerUsed,  'numJets > 1','A < 0.1', '|cos(#theta*)| < 0.3', 'subjet pt ratio > 0.3'],  X, Y, align )
	elif 'Standard' in name: setSelection( [ camp+' - '+PU, triggerUsed, 'numJets > 1', 'A < 0.1', '|cos(#theta*)| < 0.3', 'subjet pt ratio > 0.3'],  X, Y, align )
	elif 'PFHT800' in name: setSelection( [ camp+' - '+PU, 'PFHT800', 'numJets > 1', 'A < 0.1', '|cos(#theta*)| < 0.3', 'subjet pt ratio > 0.3'],  X, Y, align )
	elif 'Brock' in name: setSelection( [ camp+' - '+PU, 'HT > 1600 TeV', 'numJets > 1', 'A < 0.1', '|cos(#theta*)| < 0.3', 'subjet pt ratio > 0.3'],  X, Y, align )
	elif 'cutTau31' in name: setSelection( [ camp+' - '+PU, triggerUsed, 'numJets > 1', 'A < 0.1', '|cos(#theta*)| < 0.3', '#tau_{31} < 0.5'],  X, Y, align )
	elif 'trigger' in name: setSelection(  [ camp+' - '+PU, triggerUsed, 'Loose selection'], X, Y, align )
	#elif 'trigger' in name: setSelection( [ 'RPV Stop 100 GeV', 'AK8PFHT650TrimMass50' ], X, Y, align) 
	elif '' in name: setSelection( [ camp, PU ], X, Y, align) 
	else: setSelection( listSel, X, Y, align )

def labelAxis(name, histo, Grom ):

	if 'massAve' in name: 
		if 'Trimmed' in Grom: histo.GetXaxis().SetTitle( 'Average Trimmed Mass [GeV]' )
		elif 'Pruned' in Grom: histo.GetXaxis().SetTitle( 'Average Pruned Mass [GeV]' )
		elif 'Filtered' in Grom: histo.GetXaxis().SetTitle( 'Average Filtered Mass [GeV]' )
		else: histo.GetXaxis().SetTitle( 'Average Mass [GeV]' )
	elif 'trimmedMass' in name: histo.GetXaxis().SetTitle( 'Leading Trimmed Jet Mass [GeV]' )
	elif 'massAsymmetry' in name: histo.GetXaxis().SetTitle( 'Mass Asymmetry (A)' )
	elif 'cosThetaStar' in name: histo.GetXaxis().SetTitle( 'cos(#theta *)' )
	elif 'jetEta' in name: histo.GetXaxis().SetTitle( 'Jet #eta' )
	elif 'Tau1_' in name: histo.GetXaxis().SetTitle( '#tau_{1}' )
	elif 'Tau2_' in name: histo.GetXaxis().SetTitle( '#tau_{2}' )
	elif 'Tau3_' in name: histo.GetXaxis().SetTitle( '#tau_{3}' )
	elif 'Tau21_' in name: histo.GetXaxis().SetTitle( '#tau_{21} ' )
	elif 'Tau31_' in name: histo.GetXaxis().SetTitle( '#tau_{31} ' )
	elif 'Tau32_' in name: histo.GetXaxis().SetTitle( '#tau_{32} ' )
	elif 'PtRatio_' in name: histo.GetXaxis().SetTitle( 'Subjet Pt_{2}/Pt_{1}' )
	elif 'Mass21' in name: histo.GetXaxis().SetTitle( 'Subjet m_{2}/m_{1}' )
	elif '112Mass' in name: histo.GetXaxis().SetTitle( 'Subjet m_{1}/m_{12}' )
	elif '212Mass' in name: histo.GetXaxis().SetTitle( 'Subjet m_{2}/m_{12}' )
	elif 'PolAngle13412_' in name: histo.GetXaxis().SetTitle( 'cos #psi_{1(34)}^{[12]}' )
	elif 'PolAngle31234_' in name: histo.GetXaxis().SetTitle( 'cos #psi_{3(12)}^{[34]}' )
	elif 'HT' in name: histo.GetXaxis().SetTitle( 'HT [GeV]' )
	elif 'jetPt' in name: histo.GetXaxis().SetTitle( 'Jet p_{T} [GeV]' )
	elif 'jetMass' in name: histo.GetXaxis().SetTitle( 'Jet Mass [GeV]' )
	elif 'jet1Pt' in name: histo.GetXaxis().SetTitle( 'Leading Jet p_{T} [GeV]' )
	elif 'jet1Mass' in name: histo.GetXaxis().SetTitle( 'Leading Jet Mass [GeV]' )
	elif 'NPV' in name: histo.GetXaxis().SetTitle( 'Number of Primary Vertex' )
	else: histo.GetXaxis().SetTitle( 'NO LABEL' )


def plot( inFileSignal, inFileQCD, kfactor, Grom, nameInRoot, name, xmin, xmax, labX, labY, log, PU, Norm=False ):
	"""docstring for plot"""

	outputFileName = name+'_'+Grom+'_RPVSt'+mass+'to'+jj+'_'+PU+'_QCD'+qcd+'_AnalysisPlots.pdf' 
	print 'Processing.......', outputFileName

	histos = {}
	histos[ 'Signal' ] = inFileSignal.Get( nameInRoot )
	histos[ 'QCD' ] = inFileQCD.Get( nameInRoot )
	histos[ 'QCD' ].Scale( kfactor )

	hSignal = histos[ 'Signal' ].Clone()
	hSignalQCD = histos[ 'Signal' ].Clone()
	hSignalQCD.Add( histos[ 'QCD' ].Clone() )
	hSignal.Divide( hSignalQCD )
	hSoSB = histos[ 'Signal' ].Clone()

	for bin in range(0,  hSoSB.GetNbinsX()):
		hSoSB.SetBinContent(bin, 0.)
		hSoSB.SetBinError(bin, 0.)

	for ibin in range(0, hSoSB.GetNbinsX()):
	
		binContSignal = histos[ 'Signal' ].GetBinContent(ibin)
		binErrSignal = histos[ 'Signal' ].GetBinError(ibin)
		binContBkg = histos[ 'QCD' ].GetBinContent(ibin)
		binErrBkg = histos[ 'QCD' ].GetBinError(ibin)
		try:
			value = binContSignal / TMath.Sqrt( binContSignal + binContBkg )
		except ZeroDivisionError: continue
		hSoSB.SetBinContent( ibin, value )

	binWidth = histos['Signal'].GetBinWidth(1)

	legend=TLegend(0.55,0.75,0.90,0.90)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.04)

	if not Norm:
		tmpHisto = histos[ 'Signal' ].Clone()
		tmpHisto.SetLineColor(kRed-4)
		tmpHisto.SetFillColor(0)
		tmpHisto.SetLineWidth(3)
		histos[ 'Signal' ].SetFillColor(kRed-4)
		histos[ 'Signal' ].SetFillStyle(1001)
		histos[ 'QCD' ].SetFillColor(kBlue-4)
		histos[ 'QCD' ].SetFillStyle(1001)

		stackHisto = THStack('stackHisto', 'stack')
		stackHisto.Add( histos['QCD'] )
		stackHisto.Add( histos['Signal'] )

  		tdrStyle.SetPadRightMargin(0.05)
  		tdrStyle.SetPadLeftMargin(0.15)
		can = TCanvas('c1', 'c1',  10, 10, 750, 750 )
		pad1 = TPad("pad1", "Fit",0,0.25,1.00,1.00,-1)
		pad2 = TPad("pad2", "Pull",0,0.00,1.00,0.25,-1);
		pad1.Draw()
		pad2.Draw()

		pad1.cd()
		if log: 
			pad1.SetLogy()
			outName = outputFileName.replace('_AnalysisPlots','_Log_AnalysisPlots')
		else:
			outName = outputFileName 

		legend.AddEntry( histos[ 'Signal' ], 'RPV #tilde{t}#rightarrow '+jj+' '+mass+' GeV' , 'f' )
		legend.AddEntry( histos[ 'QCD' ], 'QCD binned in '+qcd , 'f' )
		#stackHisto.SetMinimum(10)
		stackHisto.Draw('hist')
		stackHisto.GetYaxis().SetTitleOffset(1.2)
		if xmax: stackHisto.GetXaxis().SetRangeUser( xmin, xmax )
		#histos['Signal'].Draw('hist same')
		tmpHisto.Draw("hist same")
		stackHisto.GetYaxis().SetTitle( 'Events / '+str(binWidth) )

		CMS_lumi.CMS_lumi(pad1, 4, 0)
		CMS_lumi.relPosX = 0.14
		labelAxis( name, stackHisto, Grom )
		legend.Draw()
		if not (labX and labY): labels( name, PU, camp )
		else: labels( name, PU, camp, labX, labY )

		pad2.cd()
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
		hSignal.SetFillColor(kRed+1)
		hSignal.SetFillStyle(1001)
		hSignal.GetYaxis().SetTitle("S / B")
		hSignal.GetYaxis().SetLabelSize(0.12)
		hSignal.GetXaxis().SetLabelSize(0.12)
		hSignal.GetYaxis().SetTitleSize(0.12)
		hSignal.GetYaxis().SetTitleOffset(0.45)
		hSignal.SetMaximum(0.3)
		hSignal.Sumw2()
		if xmax: hSignal.GetXaxis().SetRangeUser( xmin, xmax )
		hSignal.Draw("hist")

		can.SaveAs( 'Plots/'+outName )
		del can
	else:
		histos[ 'Signal' ].SetLineWidth(3)
		histos[ 'Signal' ].SetLineColor(kRed-4)
		histos[ 'QCD' ].SetLineColor(kBlue-4)
		histos[ 'QCD' ].SetLineWidth(3)
		if xmax: histos['Signal'].GetXaxis().SetRangeUser( xmin, xmax )
		histos['Signal'].Scale( 1/ histos['Signal'].Integral() )
		histos['QCD'].Scale( 1/ histos['QCD'].Integral() )

  		tdrStyle.SetPadRightMargin(0.05)
		can = TCanvas('c1', 'c1', 750, 500 )
		if log: 
			can.SetLogy()
			outName = outputFileName.replace('_AnalysisPlots','_Log_AnalysisPlots')
			histos['Signal'].GetYaxis().SetTitleOffset(1.2)
		else:
			outName = outputFileName 

		legend.AddEntry( histos[ 'Signal' ], 'RPV #tilde{t}#rightarrow '+jj+' '+mass+' GeV' , 'l' )
		legend.AddEntry( histos[ 'QCD' ], 'QCD binned in '+qcd , 'l' )

		histos['Signal'].GetYaxis().SetTitleOffset(1.0)
		histos['Signal'].GetYaxis().SetTitle( 'Normalized / '+str(binWidth) )
		labelAxis( name, histos['Signal'], Grom )
		histos['Signal'].Draw('hist')
		histos['QCD'].Draw('hist same')
		hmax = 1.1* max( [ histos['Signal'].GetMaximum(), histos['QCD'].GetMaximum() ] )
		histos['Signal'].SetMaximum(hmax)

		CMS_lumi.CMS_lumi(can, 4, 0)
		CMS_lumi.relPosX = 0.14
		legend.Draw()
		if not (labX and labY): labels( name, PU, camp )
		else: labels( name, PU, camp, labX, labY )

		can.SaveAs( 'Plots/'+outName )
		del can


def plot2D( inFile, sample, Grom, name, titleXAxis, titleXAxis2, xmin, xmax, ymin, ymax, legX, legY, PU ):
	"""docstring for plot"""

	outputFileName = name+'_'+Grom+'_'+sample+'_'+camp+'_'+PU+'_AnalysisPlots.pdf' 
	print 'Processing.......', outputFileName
	#h1 = inFile.Get( boosted+'AnalysisPlots'+Grom+'/'+name )
	h1 = inFile.Get( 'AnalysisPlots'+Grom+'/'+name )
	#h1 = inFile.Get( 'TriggerEfficiency'+Grom+'/'+name )

	h1.GetXaxis().SetTitle( titleXAxis )
	h1.GetYaxis().SetTitleOffset( 0.9 )
	h1.GetYaxis().SetTitle( titleXAxis2 )

	if (xmax or ymax):
		h1.GetXaxis().SetRangeUser( xmin, xmax )
		h1.GetYaxis().SetRangeUser( ymin, ymax )

	tdrStyle.SetPadRightMargin(0.12)
	can = TCanvas('c1', 'c1',  750, 500 )
	#can.SetLogz()
	h1.Draw('colz')

	CMS_lumi.CMS_lumi(can, 4, 0)
	if not (legX and legY): labels( name, sample, PU, camp )
	else: labels( name, PU, camp, legX, legY )

	can.SaveAs( 'Plots/'+outputFileName )
	del can


def plotCutFlow( inFileSignal, inFileQCD, Grom, name, xmax, log, PU, Norm=False ):
	"""docstring for plot"""

	outputFileName = name+'_'+Grom+'_RPVSt'+mass+'to'+jj+'_'+PU+'_QCD_AnalysisPlots.pdf' 
	print 'Processing.......', outputFileName

	histos = {}
	histos[ 'Signal' ] = inFileSignal.Get( boosted+'AnalysisPlots'+Grom+'/'+name )
	histos[ 'QCD' ] = inFileQCD.Get( boosted+'AnalysisPlots'+Grom+'/'+name )

	hSignal = histos[ 'Signal' ].Clone()
	hQCD = histos[ 'QCD' ].Clone()

	for bin in range(0,  hSignal.GetNbinsX()):
		hSignal.SetBinContent(bin, 0.)
		hSignal.SetBinError(bin, 0.)
		hQCD.SetBinContent(bin, 0.)
		hQCD.SetBinError(bin, 0.)
	
	totalEventsSignal = histos[ 'Signal' ].GetBinContent(1)
	totalEventsQCD = histos[ 'QCD' ].GetBinContent(1)
	#print totalEventsSignal, totalEventsQCD

	cutFlowSignalList = []
	cutFlowQCDList = []

	for ibin in range(0, hQCD.GetNbinsX()+1):
	
		cutFlowSignalList.append( histos[ 'Signal' ].GetBinContent(ibin) )
		cutFlowQCDList.append( histos[ 'QCD' ].GetBinContent(ibin) )

		hSignal.SetBinContent( ibin , histos[ 'Signal' ].GetBinContent(ibin) / totalEventsSignal )
		hQCD.SetBinContent( ibin , histos[ 'QCD' ].GetBinContent(ibin) / totalEventsQCD )
		
	hSB = hSignal.Clone()
	hSB.Divide( hQCD )
	hSB.GetXaxis().SetBinLabel( ibin, '')
	print "Signal", cutFlowSignalList
	print "QCD", cutFlowQCDList

	#hSB = hSignal.Clone()
	#hSB.Divide( hQCD )

	binWidth = histos['Signal'].GetBinWidth(1)

	legend=TLegend(0.60,0.75,0.90,0.90)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.03)

	hSignal.SetLineWidth(2)
	hSignal.SetLineColor(48)
	hQCD.SetLineColor(38)
	hQCD.SetLineWidth(2)

	can = TCanvas('c1', 'c1',  10, 10, 750, 750 )
	pad1 = TPad("pad1", "Fit",0,0.25,1.00,1.00,-1)
	pad2 = TPad("pad2", "Pull",0,0.00,1.00,0.25,-1);
	pad1.Draw()
	pad2.Draw()

	pad1.cd()
	if log: 
		pad1.SetLogy()
		outName = outputFileName.replace('_AnalysisPlots','_Log_AnalysisPlots')
		hSignal.GetYaxis().SetTitleOffset(1.2)
	else:
		outName = outputFileName 

	pad1.SetGridx()
	legend.AddEntry( hSignal, 'RPV #tilde{t}#rightarrow '+jj+' '+mass+' GeV' , 'l' )
	legend.AddEntry( hQCD, 'QCD' , 'l' )
	hSignal.GetYaxis().SetTitle( 'Percentage / '+str(binWidth) )
	hSignal.GetXaxis().SetRangeUser( 1, xmax )

	hSignal.SetMinimum(0.0001)
	hSignal.Draw()
	hQCD.Draw('same')

	legend.Draw()
	labels( name, '', '', '' )

	pad2.cd()
	hSB.GetYaxis().SetTitle("S / B")
	hSB.GetYaxis().SetLabelSize(0.12)
	hSB.GetXaxis().SetLabelSize(0.12)
	hSB.GetYaxis().SetTitleSize(0.12)
	hSB.GetYaxis().SetTitleOffset(0.45)
	#hSB.SetMaximum(0.7)
	hSB.GetXaxis().SetRangeUser( 1, xmax )
	hSB.Sumw2()
	hSB.Draw("hist")

	can.SaveAs( 'Plots/'+outName )
	del can

def plotSimple( inFile, sample, name, xmax, labX, labY, log, PU, Norm=False ):
	"""docstring for plot"""

	outputFileName = name+'_'+sample+'_MCAnalysisPlots.pdf' 
	print 'Processing.......', outputFileName

	histo = inFile.Get( boosted+'AnalysisPlots/'+name )

#	histos.values()[0].SetMaximum( 2* max( listMax ) ) 
#	histos.values()[0].GetXaxis().SetRangeUser( 0, xmax )
	binWidth = histo.GetBinWidth(1)

	legend=TLegend(0.60,0.75,0.90,0.90)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.03)

	histo.SetFillColor(48)
	histo.SetFillStyle(1001)

	can = TCanvas('c1', 'c1',  10, 10, 750, 500 )

	if log: 
		can.SetLogy()
		outName = outputFileName.replace('_AnalysisPlots','_Log_AnalysisPlots')
	else:
		outName = outputFileName 

	legend.AddEntry( histo, 'RPV #tilde{t}#rightarrow '+jj+' '+mass+' GeV' , 'f' )
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

	outputFileName = name+'_'+Grom+'_RPVSt'+mass+'to'+jj+'_Diff'+Diff+'.pdf' 
	print 'Processing.......', outputFileName

	histos = {}
	histos[ 'Sample1' ] = inFileSample1.Get( boosted+'AnalysisPlots'+Grom+'/'+name )
	histos[ 'Sample2' ] = inFileSample2.Get( boosted+'AnalysisPlots'+Grom+'/'+name )

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

def plotDiffPU( inFileSample, Grom, name, xmax, labX, labY, log, Diff , Norm=False):
	"""docstring for plot"""

	#outputFileName = name+'_'+Grom+'_RPVSt100to'+jj+'_Diff'+Diff+'s.pdf' 
	outputFileName = name+'_'+Grom+'_QCDPtALL_Diff'+Diff+'s.pdf' 
	print 'Processing.......', outputFileName

	histos = {}
	histos[ 'Sample1' ] = inFileSample.Get( boosted+'AnalysisPlots'+Grom+'/'+name.replace('_','LowPU_' ) )
	histos[ 'Sample2' ] = inFileSample.Get( boosted+'AnalysisPlots'+Grom+'/'+name.replace('_','MedPU_' ) )
	histos[ 'Sample3' ] = inFileSample.Get( boosted+'AnalysisPlots'+Grom+'/'+name.replace('_','HighPU_' ) )

	binWidth = histos['Sample1'].GetBinWidth(1)

	legend=TLegend(0.60,0.75,0.90,0.90)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.03)

	histos[ 'Sample1' ].SetLineWidth(2)
	histos[ 'Sample1' ].SetLineColor(48)
	histos[ 'Sample2' ].SetLineColor(38)
	histos[ 'Sample2' ].SetLineWidth(2)
	histos[ 'Sample3' ].SetLineColor(30)
	histos[ 'Sample3' ].SetLineWidth(2)
	histos[ 'Sample1' ].SetMaximum( 1.2* max( histos[ 'Sample1' ].GetMaximum(), histos[ 'Sample2' ].GetMaximum() ) ) 
	#histos.values()[0].GetXaxis().SetRangeUser( 0, xmax )

	can = TCanvas('c1', 'c1',  10, 10, 750, 500 )
	if log: 
		outName = outputFileName.replace('_Diff','_Log_Diff')
	else:
		outName = outputFileName 

	legend.AddEntry( histos[ 'Sample1' ], 'Low PU', 'l' )
	legend.AddEntry( histos[ 'Sample2' ], 'Med PU', 'l' )
	legend.AddEntry( histos[ 'Sample3' ], 'High PU', 'l' )
	#histos['Sample1'].SetMinimum(10)
	histos['Sample1'].Draw('hist')
	histos['Sample1'].GetYaxis().SetTitleOffset(1.2)
	histos['Sample2'].Draw('hist same')
	histos['Sample3'].Draw('hist same')
	histos['Sample1'].GetYaxis().SetTitle( 'Events / '+str(binWidth) )

	labelAxis( name, histos['Sample1'], Grom )
	legend.Draw()
	if not (labX and labY): labels( name, '13 TeV - Scaled to '+lumi+' fb^{-1}', '', '' )
	else: labels( name, '13 TeV - Scaled to '+lumi+' fb^{-1}', '', labX, labY )

	can.SaveAs( 'Plots/'+outName )
	del can

def plotOptimization( inFileSignal, inFileBkg, Grom, name, Range, xmax, labX, labY, log, Norm=False):
	"""docstring for plot"""

	outputFileName = name+'_'+Grom+'_Optimization.pdf' 
	print 'Processing.......', outputFileName

	histosSignal = {}
	histosBkg = {}
	for x in Range:
		histosSignal[ x ] = inFileSignal.Get( name+x )
		histosBkg[ x ] = inFileBkg.Get( name+x )
		print histosSignal[x].Integral()

	'''
	binWidth = histos['Sample1'].GetBinWidth(1)

	legend=TLegend(0.60,0.75,0.90,0.90)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.03)

	histos[ 'Sample1' ].SetLineWidth(2)
	histos[ 'Sample1' ].SetLineColor(48)
	histos[ 'Sample2' ].SetLineColor(38)
	histos[ 'Sample2' ].SetLineWidth(2)
	histos[ 'Sample3' ].SetLineColor(30)
	histos[ 'Sample3' ].SetLineWidth(2)
	histos[ 'Sample1' ].SetMaximum( 1.2* max( histos[ 'Sample1' ].GetMaximum(), histos[ 'Sample2' ].GetMaximum() ) ) 
	#histos.values()[0].GetXaxis().SetRangeUser( 0, xmax )

	can = TCanvas('c1', 'c1',  10, 10, 750, 500 )
	if log: 
		outName = outputFileName.replace('_Diff','_Log_Diff')
	else:
		outName = outputFileName 

	legend.AddEntry( histos[ 'Sample1' ], 'Low PU', 'l' )
	legend.AddEntry( histos[ 'Sample2' ], 'Med PU', 'l' )
	legend.AddEntry( histos[ 'Sample3' ], 'High PU', 'l' )
	#histos['Sample1'].SetMinimum(10)
	histos['Sample1'].Draw('hist')
	histos['Sample1'].GetYaxis().SetTitleOffset(1.2)
	histos['Sample2'].Draw('hist same')
	histos['Sample3'].Draw('hist same')
	histos['Sample1'].GetYaxis().SetTitle( 'Events / '+str(binWidth) )

	labelAxis( name, histos['Sample1'], Grom )
	legend.Draw()
	if not (labX and labY): labels( name, '13 TeV - Scaled to '+lumi+' fb^{-1}', '', '' )
	else: labels( name, '13 TeV - Scaled to '+lumi+' fb^{-1}', '', labX, labY )

	can.SaveAs( 'Plots/'+outName )
	del can
	'''

def plotTriggerEfficiency( inFileSample, sample, triggerDenom, triggerPass, name, cut, xmin, xmax, rebin, labX, labY, log ):
	"""docstring for plot"""

	outputFileName = name+'_'+cut+'_'+triggerDenom+"_"+triggerPass+'_'+sample+'_TriggerEfficiency.pdf' 
	print 'Processing.......', outputFileName

	DenomOnly = inFileSample.Get( 'TriggerEfficiency'+triggerDenom+triggerPass.replace('AK8PFHT700TrimMass50','')+'/'+name+'Denom_'+cut )
	DenomOnly.Rebin(rebin)
	Denom = DenomOnly.Clone()
	PassingOnly = inFileSample.Get( 'TriggerEfficiency'+triggerDenom+triggerPass.replace('AK8PFHT700TrimMass50','')+'/'+name+'Passing_'+cut )
	PassingOnly.Rebin(rebin)
	Passing = PassingOnly.Clone()
	Efficiency = TGraphAsymmErrors( Passing, Denom, 'B'  )

	binWidth = DenomOnly.GetBinWidth(1)

	legend=TLegend(0.50,0.75,0.90,0.90)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.04)

	DenomOnly.SetLineWidth(2)
	DenomOnly.SetLineColor(kRed-4)
	PassingOnly.SetLineWidth(2)
	PassingOnly.SetLineColor(kBlue-4)

	can = TCanvas('c1', 'c1',  10, 10, 750, 750 )
	pad1 = TPad("pad1", "Histo",0,0.46,1.00,1.00,-1)
	pad2 = TPad("pad2", "Efficiency",0,0.00,1.00,0.49,-1);
	pad2.Draw()
	pad1.Draw()

	pad1.cd()
	if log: pad1.SetLogy()

	legend.AddEntry( DenomOnly, triggerDenom+' (basedline trigger)', 'l' )
	legend.AddEntry( PassingOnly, triggerPass, 'l' )
	#DenomOnly.SetMinimum(10)
	DenomOnly.GetXaxis().SetRangeUser( xmin, xmax )
	DenomOnly.Draw('histe')
	DenomOnly.GetYaxis().SetTitleSize(0.06)
	DenomOnly.GetYaxis().SetTitleOffset(0.8)
	DenomOnly.GetYaxis().SetLabelSize(0.06)
	DenomOnly.GetXaxis().SetTitleOffset(0.8)
	DenomOnly.GetXaxis().SetTitleSize(0.06)
	DenomOnly.GetXaxis().SetLabelSize(0.05)
	PassingOnly.Draw('histe same')
	DenomOnly.GetYaxis().SetTitle( 'Events / '+str(binWidth) )

	CMS_lumi.CMS_lumi(pad1, 4, 0)
	labelAxis( name, DenomOnly, 'Pruned')
	legend.Draw()
	if 'JetHT' in sample:
		if not (labX and labY): labels( 'trigger','', PU, camp, '', '')
		else: labels( 'trigger', '',  PU, camp, labX, labY ) #, sel1='AK8PFHT700TrimMass50' )
	else:
		if not (labX and labY): labels( 'trigger', 'RPV Stop 100 GeV', PU, camp, '', ''  )
		else: labels( 'trigger', 'RPV Stop 100 GeV', PU, camp, labX, labY )

	pad2.cd()
	Efficiency.SetLineWidth(2)
	Efficiency.SetLineColor(kBlue-4)
	#Efficiency.SetFillStyle(1001)
	Efficiency.GetYaxis().SetTitle("Efficiency")
	Efficiency.GetYaxis().SetLabelSize(0.06)
	Efficiency.GetXaxis().SetLabelSize(0.06)
	Efficiency.GetYaxis().SetTitleSize(0.06)
	Efficiency.GetYaxis().SetTitleOffset(0.8)
	Efficiency.SetMinimum(-0.1)
	Efficiency.GetXaxis().SetLimits( xmin, xmax )
	Efficiency.Draw()

	can.SaveAs( 'Plots/'+outputFileName )
	del can

	can1 = TCanvas('c1', 'c1',  10, 10, 750, 500 )
	Efficiency.SetMinimum(0)
	Efficiency.GetYaxis().SetLabelSize(0.05)
	Efficiency.GetXaxis().SetLabelSize(0.05)
	Efficiency.GetYaxis().SetTitleSize(0.06)
	Efficiency.GetYaxis().SetTitleOffset(0.8)
	Efficiency.GetXaxis().SetTitleOffset(0.8)
	Efficiency.Draw()
	can1.Update()

	rightmax = 1.2*PassingOnly.GetMaximum()
	rightmin = PassingOnly.GetMinimum()
	scale = gPad.GetUymax()/rightmax
	PassingOnly.SetLineColor(kBlue-5)
	PassingOnly.Scale( scale )
	PassingOnly.Draw( 'hist same' )
	#axis = TGaxis( gPad.GetUxmax(), gPad.GetUymin(), gPad.GetUxmax(), gPad.GetUymax(),-3,rightmax,710,"+L")
	axis = TGaxis( gPad.GetUxmax(), gPad.GetUymin(), gPad.GetUxmax(), gPad.GetUymax(),rightmin,rightmax,10,"+L")
	axis.SetTitle('Events / '+str(binWidth) )
	axis.SetTitleColor(kBlue-5)
	axis.SetTitleSize(0.06)
	axis.SetLabelSize(0.05)
	axis.SetTitleFont(42)
	axis.SetLabelFont(42)
	axis.SetLineColor(kBlue-5)
	axis.SetLabelColor(kBlue-5)
	axis.SetTitleOffset(0.7)
	axis.Draw()
	labelAxis( name, Efficiency, 'Pruned')
	CMS_lumi.relPosX = 0.11
	CMS_lumi.cmsTextSize = 0.7
	CMS_lumi.extraOverCmsTextSize = 0.6
	CMS_lumi.CMS_lumi(can1, 4, 0)

	can1.SaveAs( 'Plots/'+outputFileName.replace('.pdf','Merged.pdf') )
	del can1


def plot2DTriggerEfficiency( inFileSample, sample, triggerDenom, triggerPass, name, cut, Xmin, Xmax, rebinx, Ymin, Ymax, rebiny, labX, labY ):
	"""docstring for plot"""

	outputFileName = name+'_'+cut+'_'+triggerDenom+"_"+triggerPass+'_'+sample+'_TriggerEfficiency.pdf' 
	print 'Processing.......', outputFileName

	#Denom = inFileSample.Get( 'TriggerEfficiency'+triggerDenom+triggerPass.replace('AK8PFHT700TrimMass50','')+'/'+name+'Denom_'+cut )
	Denom = inFileSample.Get( 'TriggerEfficiency'+triggerPass.replace('AK8PFHT700TrimMass50','')+'/'+name+'Denom_'+cut )
	#Passing = inFileSample.Get( 'TriggerEfficiency'+triggerDenom+triggerPass.replace('AK8PFHT700TrimMass50','')+'/'+name+'Passing_'+cut )
	Passing = inFileSample.Get( 'TriggerEfficiency'+triggerPass.replace('AK8PFHT700TrimMass50','')+'/'+name+'Passing_'+cut )
	tmpDenom = Denom.Clone()
	tmpPassing = Passing.Clone()
	
	### Rebinning
	nbinsx = Denom.GetXaxis().GetNbins()
	nbinsy = Denom.GetYaxis().GetNbins()
	xmin  = Denom.GetXaxis().GetXmin()
	xmax  = Denom.GetXaxis().GetXmax()
	ymin  = Denom.GetYaxis().GetXmin()
	ymax  = Denom.GetYaxis().GetXmax()
	nx = nbinsx/rebinx
	ny = nbinsy/rebiny
	Denom.SetBins( nx, xmin, xmax, ny, ymin, ymax )
	Passing.SetBins( nx, xmin, xmax, ny, ymin, ymax )

	for biny in range( 1, nbinsy):
		for binx in range(1, nbinsx):
			ibin1 = Denom.GetBin(binx,biny)
			Denom.SetBinContent( ibin1, 0 )
			ibin2 = Denom.GetBin(binx,biny)
			Passing.SetBinContent( ibin2, 0 )
		
	for biny in range( 1, nbinsy):
		by = tmpDenom.GetYaxis().GetBinCenter( biny )
		iy = Denom.GetYaxis().FindBin(by)
		by2 = tmpPassing.GetYaxis().GetBinCenter( biny )
		iy2 = Passing.GetYaxis().FindBin(by2)
		for binx in range(1, nbinsx):
			bx = tmpDenom.GetXaxis().GetBinCenter(binx)
			ix  = Denom.GetXaxis().FindBin(bx)
			bin = tmpDenom.GetBin(binx,biny)
			ibin= Denom.GetBin(ix,iy)
			cu  = tmpDenom.GetBinContent(bin)
			Denom.AddBinContent(ibin,cu)

			bx2 = tmpPassing.GetXaxis().GetBinCenter(binx)
			ix2  = Passing.GetXaxis().FindBin(bx2)
			bin2 = tmpPassing.GetBin(binx,biny)
			ibin2 = Passing.GetBin(ix2,iy2)
			cu2  = tmpPassing.GetBinContent(bin2)
			Passing.AddBinContent(ibin2,cu2)

	Efficiency = Denom.Clone() #TH2D( '', '', nx, xmin, xmax, ny, ymin, ymax )
	Efficiency.Reset()
	Efficiency.Divide( Passing, Denom, 1, 1, 'B' )

	legend=TLegend(0.55,0.75,0.90,0.90)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.04)

	can = TCanvas('c1', 'c1',  10, 10, 750, 500 )
	gStyle.SetPaintTextFormat("4.2f")
	Efficiency.Draw('colz')
	Efficiency.Draw('same text')
	Efficiency.GetYaxis().SetTitleOffset(0.9)
	Efficiency.GetXaxis().SetRange( int(Xmin/(10.*rebinx)), int(Xmax/(10.*rebinx)) )
	Efficiency.GetXaxis().SetTitle( 'Leading Trimmed Jet Mass [GeV]' )
	Efficiency.GetYaxis().SetRange( int(Ymin/(10.*rebiny)), int(Ymax/(10.*rebiny)) )

	CMS_lumi.CMS_lumi(can, 4, 0)
	legend.Draw()
	if 'JetHT' in sample:
		if not (labX and labY): labels( 'trigger',PU, camp, )
		else: labels( 'trigger', PU, camp, labX, labY ) #, sel1= [ 'AK8PFHT700TrimMass50' ] )
	else:
		if not (labX and labY): labels( 'trigger', PU, camp  )
		else: labels( 'trigger', PU, camp, labX, labY)

	can.SaveAs( 'Plots/'+outputFileName )
	del can

def tmpplotTriggerEfficiency( inFileSample, sample, triggerDenom, triggerPass, name, cut, xmin, xmax, rebin, labX, labY, log ):
	"""docstring for plot"""

	outputFileName = name+'_'+cut+'_'+triggerDenom+'_DiffTriggers_'+sample+'_TriggerEfficiency.pdf' 
	print 'Processing.......', outputFileName

	DenomOnly = inFileSample.Get( 'TriggerEfficiency'+triggerDenom+'/'+name+'Denom_'+cut )
	DenomOnly.Rebin(rebin)
	Denom = DenomOnly.Clone()
	PassingOnly1 = inFileSample.Get( 'TriggerEfficiency'+triggerDenom+'/'+name+'Passing_'+cut )
	PassingOnly1.Rebin(rebin)
	Passing1 = PassingOnly1.Clone()
	PassingOnly2 = inFileSample.Get( 'TriggerEfficiency'+triggerDenom+'AKPFHT650/'+name+'Passing_'+cut )
	PassingOnly2.Rebin(rebin)
	Passing2 = PassingOnly2.Clone()
	PassingOnly3 = inFileSample.Get( 'TriggerEfficiency'+triggerDenom+'AKPFHT600/'+name+'Passing_'+cut )
	PassingOnly3.Rebin(rebin)
	Passing3 = PassingOnly3.Clone()
	PassingOnly4 = inFileSample.Get( 'TriggerEfficiency'+triggerDenom+'AKPFHT550/'+name+'Passing_'+cut )
	PassingOnly4.Rebin(rebin)
	Passing4 = PassingOnly4.Clone()
	PassingOnly5 = inFileSample.Get( 'TriggerEfficiency'+triggerDenom+'AKPFHT500/'+name+'Passing_'+cut )
	PassingOnly5.Rebin(rebin)
	Passing5 = PassingOnly5.Clone()
	
	Efficiency1 = TGraphAsymmErrors( Passing1, Denom, 'B'  )
	Efficiency2 = TGraphAsymmErrors( Passing2, Denom, 'B'  )
	Efficiency3 = TGraphAsymmErrors( Passing3, Denom, 'B'  )
	Efficiency4 = TGraphAsymmErrors( Passing4, Denom, 'B'  )
	Efficiency5 = TGraphAsymmErrors( Passing5, Denom, 'B'  )

	binWidth = DenomOnly.GetBinWidth(1)

	legend=TLegend(0.55,0.65,0.90,0.90)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.04)

	DenomOnly.SetLineWidth(2)
	DenomOnly.SetLineColor(kCyan-4)
	PassingOnly1.SetLineWidth(2)
	PassingOnly1.SetLineColor(kBlue-4)
	Efficiency1.SetLineWidth(2)
	Efficiency1.SetLineColor(kBlue-4)
	PassingOnly2.SetLineWidth(2)
	PassingOnly2.SetLineColor(kGreen-4)
	Efficiency2.SetLineWidth(2)
	Efficiency2.SetLineColor(kGreen-4)
	PassingOnly3.SetLineWidth(2)
	PassingOnly3.SetLineColor(kRed-4)
	Efficiency3.SetLineWidth(2)
	Efficiency3.SetLineColor(kRed-4)
	PassingOnly4.SetLineWidth(2)
	PassingOnly4.SetLineColor(kViolet-4)
	Efficiency4.SetLineWidth(2)
	Efficiency4.SetLineColor(kViolet-4)
	PassingOnly5.SetLineWidth(2)
	PassingOnly5.SetLineColor(kAzure-4)
	Efficiency5.SetLineWidth(2)
	Efficiency5.SetLineColor(kAzure-4)

	can = TCanvas('c1', 'c1',  10, 10, 750, 750 )
	pad1 = TPad("pad1", "Histo",0,0.50,1.00,1.00,-1)
	pad2 = TPad("pad2", "Efficiency",0,0.00,1.00,0.50,-1);
	pad1.Draw()
	pad2.Draw()

	pad1.cd()
	if log: pad1.SetLogy()
	legend.AddEntry( DenomOnly, triggerDenom+' (basedline trigger)', 'l' )
	legend.AddEntry( PassingOnly1, 'AK8PFHT700TrimMass50', 'l' )
	legend.AddEntry( PassingOnly2, 'AK8PFHT650TrimMass50', 'l' )
	'''
	legend.AddEntry( PassingOnly3, 'AK8PFHT600TrimMass50', 'l' )
	legend.AddEntry( PassingOnly4, 'AK8PFHT550TrimMass50', 'l' )
	legend.AddEntry( PassingOnly5, 'AK8PFHT500TrimMass50', 'l' )
	'''
	#DenomOnly.SetMinimum(10)
	DenomOnly.GetXaxis().SetRangeUser( xmin, xmax )
	DenomOnly.Draw('histe')
	DenomOnly.GetYaxis().SetTitleSize(0.06)
	DenomOnly.GetYaxis().SetTitleOffset(0.8)
	DenomOnly.GetYaxis().SetLabelSize(0.06)
	DenomOnly.GetXaxis().SetTitleOffset(0.9)
	DenomOnly.GetXaxis().SetTitleSize(0.06)
	DenomOnly.GetXaxis().SetLabelSize(0.06)
	PassingOnly1.Draw('histe same')
	PassingOnly2.Draw('histe same')
	'''
	PassingOnly3.Draw('histe same')
	PassingOnly4.Draw('histe same')
	PassingOnly5.Draw('histe same')
	'''
	DenomOnly.GetYaxis().SetTitle( 'Events / '+str(binWidth) )

	CMS_lumi.CMS_lumi(pad1, 4, 0)
	labelAxis( name, DenomOnly, 'Pruned')
	legend.Draw()
	if 'JetHT' in sample:
		if not (labX and labY): labels( 'trigger', 'Data - '+lumi+' pb^{-1}', PU, camp )
		else: labels( 'trigger', 'Data - '+lumi+' pb^{-1}',  PU, camp, labX, labY )
	else:
		if not (labX and labY): labels( 'trigger', 'RPV Stop 100 GeV', PU, camp )
		else: labels( 'trigger', 'RPV Stop 100 GeV', PU, camp, labX, labY  )

	pad2.cd()
	#Efficiency1.SetFillStyle(1001)
	Efficiency1.GetYaxis().SetTitle("Efficiency")
	Efficiency1.GetYaxis().SetLabelSize(0.06)
	Efficiency1.GetXaxis().SetLabelSize(0.06)
	Efficiency1.GetYaxis().SetTitleSize(0.06)
	Efficiency1.GetYaxis().SetTitleOffset(0.8)
	Efficiency1.SetMinimum(-0.1)
	Efficiency1.GetXaxis().SetLimits( xmin, xmax )
	Efficiency1.Draw()
	Efficiency2.Draw('same')
	'''
	Efficiency3.Draw('same')
	Efficiency4.Draw('same')
	Efficiency5.Draw('same')
	'''

	can.SaveAs( 'Plots/'+outputFileName )
	del can



if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--proc', action='store', default='1D', help='Process to draw, example: 1D, 2D, MC.' )
	parser.add_argument('-d', '--decay', action='store', default='jj', help='Decay, example: jj, bj.' )
	parser.add_argument('-b', '--boosted', action='store', default='Boosted', help='Boosted or non boosted, example: Boosted' )
	parser.add_argument('-g', '--grom', action='store', default='Pruned', help='Grooming Algorithm, example: Pruned, Filtered.' )
	parser.add_argument('-m', '--mass', action='store', default='100', help='Mass of Stop, example: 100' )
	parser.add_argument('-cHT', '--cutDijet', action='store', default='700', help='HT cut, example: 700' )
	parser.add_argument('-cjPt', '--cutjetPt', action='store', default='150', help='jet Pt cut, example: 150' )
	parser.add_argument('-cjM', '--cutjetMass', action='store', default='50', help='jet trimmed mass cut, example: 50' )
	parser.add_argument('-pu', '--PU', action='store', default='Asympt25ns', help='PU, example: PU40bx25.' )
	parser.add_argument('-s', '--single', action='store', default='all', help='single histogram, example: massAve_cutDijet.' )
	parser.add_argument('-q', '--QCD', action='store', default='Pt', help='Type of QCD binning, example: HT.' )
	parser.add_argument('-c', '--campaign', action='store', default='RunIISpring15DR74', help='Campaign, example: PHYS14.' )
	parser.add_argument('-l', '--lumi', action='store', default='1', help='Luminosity, example: 1.' )
	parser.add_argument('-t', '--trigger', action='store', default='AK8PFHT700TrimMass50', help='Trigger used, example PFHT800.' )

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
	cutDijet = args.cutDijet
	cutjPt = args.cutjetPt
	cutjM = args.cutjetMass
	grom = args.grom
	single = args.single
	boosted = args.boosted
	triggerUsed = args.trigger
	
	if 'DATA' in process: 
		CMS_lumi.lumi_13TeV = "40.5 pb^{-1}"
		CMS_lumi.extraText = "Preliminary"
	else:
		CMS_lumi.lumi_13TeV = lumi+" fb^{-1}"
		CMS_lumi.extraText = "Preliminary Simulation"

	#inputFileSample = TFile.Open('RUNAnalysis_RPVSt100tojj_pythia8_13TeV_PU40bx50_PHYS14.root')
	#inputFileMCSignal = TFile.Open('RUNMCAnalysis_RPVSt100tojj_pythia8_13TeV_PU20bx25.root')
	if 'trig' in process:
		if 'DATA' in process: 
			if 'MET' in process:
				inputTrigger = TFile.Open('Rootfiles/RUNTriggerEfficiency_MET_Asympt50ns_v01p2_ts_v05.root')
				SAMPLE = 'MET'
				BASEDTrigger = 'PFMET170'
			else:
				inputTrigger = TFile.Open('Rootfiles/RUNTriggerEfficiency_JetHT_Asympt50ns_v01p2_ts_v05.root')
				SAMPLE = 'JetHT'
				BASEDTrigger = 'PFHT475'
		else: 
			inputTrigger = TFile.Open('Rootfiles/RUNTriggerEfficiency_RPVSt100tojj_RunIISpring15DR74_Asympt25ns_TS_v02_v05.root')
			SAMPLE = 'RPVStop100tojj'
			BASEDTrigger = 'PFHT475'
	elif 'mini' in process:
		inputMiniFileSignal = TFile.Open('Rootfiles/RUNMiniAnalysis_RPVSt'+mass+'to'+jj+'_'+camp+'_'+PU+'_v03_v09.root')
		inputMiniFileQCD = TFile.Open('Rootfiles/RUNMiniAnalysis_QCD'+qcd+'All_'+camp+'_'+PU+'_v03_v09.root')
	else:
		#inputFileSignal = TFile.Open('Rootfiles/RUNAnalysis_RPVSt'+mass+'to'+jj+'_'+camp+'_'+PU+'_v02_v03.root')
		inputFileSignal = TFile.Open('Rootfiles/RUNTriggerEfficiency_RPVSt100tojj_RunIISpring15DR74_Asympt25ns_TS_v02_v05.root')
		#inputFileQCD = TFile.Open('Rootfiles/RUNAnalysis_QCD'+qcd+'All_'+camp+'_'+PU+'_v01_v03.root')

	dijetlabX = 0.15
	dijetlabY = 0.88
	triggerlabX = 0.60
	triggerlabY = 0.5 #0.75  #0.50
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
	massMaxX = 3*(int(mass))
	polAngXmin = 0.7
	polAngXmax = 1.0
	HTMinX = 300
	HTMaxX = 1300
	ptMinX = 100
	ptMaxX = 800


	plotList = [ 
		[ '2D', 'jetTrimmedMassHT', 'Leading Trimmed Jet Mass [GeV]', 'HT [GeV]', 0, massMaxX, 100, HTMaxX, jetMassHTlabX, jetMassHTlabY],
		[ '2D', 'jet1Subjet112vs212MassRatio_cutDijet', 'm_{1}/m_{12}', 'm_{2}/m_{12}', '', '', '', '', subjet112vs212labX, subjet112vs212labY  ],
		[ '2D', 'jet1Subjet1JetvsSubjet2JetMassRatio_cutDijet', 'm_{1}/M_{12}', 'm_{2}/M_{12}', '', '', '', '', subjet112vs212labX, subjet112vs212labY  ],
		[ '2D', 'jet2Subjet112vs212MassRatio_cutDijet', 'm_{3}/m_{34}', 'm_{4}/m_{34}', '', '', '', '', subjet112vs212labX, subjet112vs212labY  ],
		[ '2D', 'jet2Subjet1JetvsSubjet2JetMassRatio_cutDijet', 'm_{3}/M_{34}', 'm_{4}/M_{34}', '', '', '', '', subjet112vs212labX, subjet112vs212labY  ],
		[ '2D', 'subjet12Mass_cutDijet', 'm_{1}', 'm_{2}', '', '', '', '', dijetlabX, dijetlabY  ],
		[ '2D', 'dijetCorr_cutDijet', '#eta_{sjet1}', '#eta_{sjet2}', '', '', '', '', dijetlabX, dijetlabY  ],
		[ '2D', 'dijetCorrPhi_cutDijet', '#phi_{sjet1}', '#phi_{sjet2}', '', '', '', '', dijetlabX, dijetlabY  ],
		[ '2D', 'subjet112vs212MassRatio_cutDijet', 'm_{1}/m_{12}', 'm_{2}/m_{12}', '', '', '', '', subjet112vs212labX, subjet112vs212labY  ],
		[ '2D', 'subjet1JetvsSubjet2JetMassRatio_cutDijet', 'm_{1}/M_{12}', 'm_{2}/M_{12}', '', '', '', '', subjet112vs212labX, subjet112vs212labY  ],
		[ '2D', 'subjetPolAngle13412vs31234_cutDijet', 'cos #psi_{1(34)}^{[12]}', 'cos #psi_{3(12)}^{[34]}', polAngXmin, polAngXmax, polAngXmin, polAngXmax, cosPhilabX, cosPhilabY  ],
		[ '2D', 'mu1234_cutDijet', '', '', '', '', '', '', dijetlabX, dijetlabY  ],
		[ '2D', 'mu3412_cutDijet', '', '', '', '', '', '', dijetlabX, dijetlabY  ],
		[ '2D', 'dalitz1234_cutDijet', 'X', 'Y', '', '', '', '', dijetlabX, dijetlabY  ],
		[ '2D', 'dalitz3412_cutDijet', 'X', 'Y', '', '', '', '', dijetlabX, dijetlabY  ],

		#[ '2D', 'subjet12Mass_cutAsym', 'm_{1}', 'm_{2}', '', '', '', '', dijetlabX, dijetlabY  ],
		[ '2D', 'dijetCorr_cutAsym', '#eta_{sjet1}', '#eta_{sjet2}', '', '', '', '', dijetlabX, dijetlabY  ],
		[ '2D', 'dijetCorrPhi_cutAsym', '#phi_{sjet1}', '#phi_{sjet2}', '', '', '', '', dijetlabX, dijetlabY  ],
		#[ '2D', 'subjet112vs212MassRatio_cutAsym', 'm_{1}/m_{12}', 'm_{2}/m_{12}', '', '', '', '', subjet112vs212labX, subjet112vs212labY  ],
		#[ '2D', 'subjet1JetvsSubjet2JetMassRatio_cutAsym', 'm_{1}/M_{12}', 'm_{2}/M_{12}', '', '', '', '', subjet112vs212labX, subjet112vs212labY  ],
		#[ '2D', 'subjetPolAngle13412vs31234_cutAsym', 'cos #psi_{1(34)}^{[12]}', 'cos #psi_{3(12)}^{[34]}', '', '', '', '', '', ''  ],
		#[ '2D', 'mu1234_cutAsym', '', '', '', '', '', '', dijetlabX, dijetlabY  ],
		#[ '2D', 'mu3412_cutAsym', '', '', '', '', '', '', dijetlabX, dijetlabY  ],
		#[ '2D', 'dalitz1234_cutAsym', 'X', 'Y', '', '', '', '', dijetlabX, dijetlabY  ],
		#[ '2D', 'dalitz3412_cutAsym', 'X', 'Y', '', '', '', '', dijetlabX, dijetlabY  ],

		#[ '2D', 'subjet12Mass_cutCosTheta', 'm_{1}', 'm_{2}', '', '', '', '', dijetlabX, dijetlabY  ],
		#[ '2D', 'dijetCorr_cutCosTheta', '#eta_{sjet1}', '#eta_{sjet2}', '', '', '', '', dijetlabX, dijetlabY  ],
		#[ '2D', 'dijetCorrPhi_cutCosTheta', '#phi_{sjet1}', '#phi_{sjet2}', '', '', '', '', dijetlabX, dijetlabY  ],
		#[ '2D', 'subjet112vs212MassRatio_cutCosTheta', 'm_{1}/m_{12}', 'm_{2}/m_{12}', '', '', '', '', subjet112vs212labX, subjet112vs212labY  ],
		#[ '2D', 'subjet1JetvsSubjet2JetMassRatio_cutCosTheta', 'm_{1}/M_{12}', 'm_{2}/M_{12}', '', '', '', '', subjet112vs212labX, subjet112vs212labY  ],
		#[ '2D', 'subjetPolAngle13412vs31234_cutCosTheta', 'cos #psi_{1(34)}^{[12]}', 'cos #psi_{3(12)}^{[34]}', '', '', '', '', '', ''  ],
		#[ '2D', 'mu1234_cutCosTheta', '', '', '', '', '', '', dijetlabX, dijetlabY  ],
		#[ '2D', 'mu3412_cutCosTheta', '', '', '', '', '', '', dijetlabX, dijetlabY  ],
		#[ '2D', 'dalitz1234_cutCosTheta', 'X', 'Y', '', '', '', '', dijetlabX, dijetlabY  ],
		#[ '2D', 'dalitz3412_cutCosTheta', 'X', 'Y', '', '', '', '', dijetlabX, dijetlabY  ],

		[ '2D', 'subjet12Mass_cutSubjetPtRatio', 'm_{1}', 'm_{2}', '', '', '', '', dijetlabX, dijetlabY  ],
		[ '2D', 'dijetCorr_cutSubjetPtRatio', '#eta_{sjet1}', '#eta_{sjet2}', '', '', '', '', dijetlabX, dijetlabY  ],
		[ '2D', 'dijetCorrPhi_cutSubjetPtRatio', '#phi_{sjet1}', '#phi_{sjet2}', '', '', '', '', dijetlabX, dijetlabY  ],
		[ '2D', 'subjet112vs212MassRatio_cutSubjetPtRatio', 'm_{1}/m_{12}', 'm_{2}/m_{12}', '', '', '', '', subjet112vs212labX, subjet112vs212labY  ],
		[ '2D', 'subjet1JetvsSubjet2JetMassRatio_cutSubjetPtRatio', 'm_{1}/M_{12}', 'm_{2}/M_{12}', '', '', '', '', subjet112vs212labX, subjet112vs212labY  ],
		[ '2D', 'subjetPolAngle13412vs31234_cutSubjetPtRatio', 'cos #psi_{1(34)}^{[12]}', 'cos #psi_{3(12)}^{[34]}', polAngXmin, polAngXmax, polAngXmin, polAngXmax, cosPhilabX, cosPhilabY  ],
		[ '2D', 'subjetPolAngle13412vsSubjetPtRatio_cutSubjePtRatio', 'cos #psi_{1(34)}^{[12]}', 'Subjet Pt Ratio', polAngXmin, polAngXmax, polAngXmin, polAngXmax, cosPhilabX, cosPhilabY  ],
		[ '2D', 'mu1234_cutSubjetPtRatio', '', '', '', '', '', '', dijetlabX, dijetlabY  ],
		[ '2D', 'mu3412_cutSubjetPtRatio', '', '', '', '', '', '', dijetlabX, dijetlabY  ],
		[ '2D', 'dalitz1234_cutSubjetPtRatio', 'X', 'Y', '', '', '', '', dijetlabX, dijetlabY  ],
		[ '2D', 'dalitz3412_cutSubjetPtRatio', 'X', 'Y', '', '', '', '', dijetlabX, dijetlabY  ],

		#[ '2D', 'subjet12Mass_cutTau31', 'm_{1}', 'm_{2}', '', '', '', '', dijetlabX, dijetlabY  ],
		#[ '2D', 'dijetCorr_cutTau31', '#eta_{sjet1}', '#eta_{sjet2}', '', '', '', '', dijetlabX, dijetlabY  ],
		#[ '2D', 'dijetCorrPhi_cutTau31', '#phi_{sjet1}', '#phi_{sjet2}', '', '', '', '', dijetlabX, dijetlabY  ],
		#[ '2D', 'subjet112vs212MassRatio_cutTau31', 'm_{1}/m_{12}', 'm_{2}/m_{12}', '', '', '', '', subjet112vs212labX, subjet112vs212labY  ],
		#[ '2D', 'subjet1JetvsSubjet2JetMassRatio_cutTau31', 'm_{1}/M_{12}', 'm_{2}/M_{12}', '', '', '', '', subjet112vs212labX, subjet112vs212labY  ],
		#[ '2D', 'subjetPolAngle13412vs31234_cutTau31', 'cos #psi_{1(34)}^{[12]}', 'cos #psi_{3(12)}^{[34]}', '', '', '', '', '', ''  ],
		#[ '2D', 'mu1234_cutTau31', '', '', '', '', '', '', dijetlabX, dijetlabY  ],
		#[ '2D', 'mu3412_cutTau31', '', '', '', '', '', '', dijetlabX, dijetlabY  ],
		#[ '2D', 'dalitz1234_cutTau31', 'y', 'x', '', '', '', '', dijetlabX, dijetlabY  ],
		#[ '2D', 'dalitz3412_cutTau31', 'y', 'x', '', '', '', '', dijetlabX, dijetlabY  ],

		[ '1D', 'jetPt', 10, 1000, '', '', True],
		[ '1D', 'jetEta', '', '', '', '', True],
		[ '1D', 'jetMass', 0, massMaxX, '', '', True],
		[ '1D', 'HT', 0, 1000, '', '', False],
		[ '1D', 'HT', 0, 1000, '', '', True],
		[ '1D', 'massAve_cutDijet', 0, massMaxX, '', '', False],
		#[ '1D', 'jet1Subjet1Pt_cutDijet', '', '', '', '', True],
		#[ '1D', 'jet1Subjet2Pt_cutDijet', '', '', '', True],
		#[ '1D', 'jet2Subjet1Pt_cutDijet', '', '', '', True],
		#[ '1D', 'jet2Subjet2Pt_cutDijet', '', '', '', True],
		#[ '1D', 'jet1Subjet1Mass_cutDijet', '', '', '', True],
		#[ '1D', 'jet1Subjet2Mass_cutDijet', '', '', '', True],
		#[ '1D', 'jet2Subjet1Mass_cutDijet', '', '', '', True],
		#[ '1D', 'jet2Subjet2Mass_cutDijet', '', '', '', True],
		[ '1D', 'massAve_cutAsym', 0, massMaxX, '', '', False],
		[ '1D', 'massAve_cutCosTheta', 0, massMaxX, '', '', False],
		[ '1D', 'massAve_cutSubjetPtRatio', 0, massMaxX, '', '', False],
		#[ '1D', 'massAve_cutSubjetPtRatio', 0, massMaxX, '', '', True ],
		[ '1D', 'massAve_cutTau31', 0, massMaxX, '', '', False],

		[ 'Norm', 'NPV', '', '', '', '', False],
		[ 'Norm', 'jet1Tau1_cutDijet', '', '', taulabX, taulabY, False],
		[ 'Norm', 'jet1Tau2_cutDijet', '', '', taulabX, taulabY, False],
		[ 'Norm', 'jet1Tau3_cutDijet', '', '', taulabX, taulabY, False],
		[ 'Norm', 'jet1Tau21_cutDijet', '', '', taulabX, taulabY, False],
		[ 'Norm', 'jet1Tau31_cutDijet', '', '', taulabX, taulabY, False],
		[ 'Norm', 'jet1Tau32_cutDijet', '', '', taulabX, taulabY, False],
		[ 'Norm', 'jet1SubjetPtRatio_cutDijet', '', '', '', '', True],
		[ 'Norm', 'jet2SubjetPtRatio_cutDijet', '', '', '', '', True],
		[ 'Norm', 'subjetPtRatio_cutDijet', '', '', '', '', True],
		[ 'Norm', 'massAsymmetry_cutDijet', '', '', '', '', False],
		[ 'Norm', 'cosThetaStar_cutDijet', '', '', '', '', False],
		#[ 'Norm', 'jet1Subjet21MassRatio_cutDijet', '', '', '', '', False],
		[ 'Norm', 'jet1Subjet112MassRatio_cutDijet', '', '', '', '', False],
		[ 'Norm', 'jet1Subjet1JetMassRatio_cutDijet', '', '', '', '', False],
		[ 'Norm', 'jet1Subjet212MassRatio_cutDijet', '', '', '', '', False],
		[ 'Norm', 'jet1Subjet2JetMassRatio_cutDijet', '', '', '', '', False],
		[ 'Norm', 'jet2Subjet112MassRatio_cutDijet', '', '', '', '', False],
		[ 'Norm', 'jet2Subjet1JetMassRatio_cutDijet', '', '', '', '', False],
		[ 'Norm', 'jet2Subjet212MassRatio_cutDijet', '', '', '', '', False],
		[ 'Norm', 'jet2Subjet2JetMassRatio_cutDijet', '', '', '', '', False],
		[ 'Norm', 'subjetPtRatio_cutDijet', '', '', '', '', False],
		[ 'Norm', 'subjetMass21Ratio_cutDijet', '', '', '', '', False],
		[ 'Norm', 'subjet112MassRatio_cutDijet', '', '', '', '', False],
		[ 'Norm', 'subjet212MassRatio_cutDijet', '', '', '', '', False],
		[ 'Norm', 'subjetPolAngle13412_cutDijet', polAngXmin, polAngXmax, '', '', False],
		[ 'Norm', 'subjetPolAngle31234_cutDijet', polAngXmin, polAngXmax, '', '', False],
		[ 'Norm', 'cosThetaStar_cutAsym', '', '', '', '', False],
		#[ 'Norm', 'jet1Tau21_cutAsym', '', '', taulabX, taulabY, False],
		#[ 'Norm', 'jet1Tau31_cutAsym', '', '', taulabX, taulabY, False],
		#[ 'Norm', 'jet1Tau32_cutAsym', '', '', taulabX, taulabY, False],
		#[ 'Norm', 'subjetPtRatio_cutAsym', '', '', '', '', False],
		#[ 'Norm', 'subjetMass21Ratio_cutAsym', '', '', '', '', True],
		#[ 'Norm', 'subjet112MassRatio_cutAsym', '', '', '', '', True],
		#[ 'Norm', 'subjet212MassRatio_cutAsym', '', '', '', '', True],
		#[ 'Norm', 'subjetPolAngle13412_cutAsym', '', '', '', '', True],
		#[ 'Norm', 'subjetPolAngle31234_cutAsym', '', '', '', '', False],
		[ 'Norm', 'jet1Tau21_cutCosTheta', '', '', taulabX, taulabY, False],
		[ 'Norm', 'jet1Tau31_cutCosTheta', '', '', taulabX, taulabY, False],
		[ 'Norm', 'jet1Tau32_cutCosTheta', '', '', taulabX, taulabY, False],
		[ 'Norm', 'subjetPtRatio_cutCosTheta', '', '', '', '', False],
		#[ 'Norm', 'subjetMass21Ratio_cutCosTheta', '', '', '', '', True],
		#[ 'Norm', 'subjet112MassRatio_cutCosTheta', '', '', '', '', True],
		#[ 'Norm', 'subjet212MassRatio_cutCosTheta', '', '', '', '', True],
		[ 'Norm', 'subjetPolAngle13412_cutCosTheta', polAngXmin, polAngXmax, polAnglabX, polAnglabY, True],
		[ 'Norm', 'subjetPolAngle31234_cutCosTheta', polAngXmin, polAngXmax, polAnglabX, polAnglabY, True],
		#[ 'Norm', 'jet1Tau21_cutSubjetPtRatio', '', '', taulabX, taulabY, True],
		#[ 'Norm', 'jet1Tau31_cutSubjetPtRatio', '', '', taulabX, taulabY, True],
		#[ 'Norm', 'jet1Tau32_cutSubjetPtRatio', '', '', taulabX, taulabY, True],
		[ 'Norm', 'subjetMass21Ratio_cutSubjetPtRatio', '', '', '', '', True],
		[ 'Norm', 'subjet112MassRatio_cutSubjetPtRatio', '', '', '', '', True],
		[ 'Norm', 'subjet212MassRatio_cutSubjetPtRatio', '', '', '', '', True],
		[ 'Norm', 'subjetPolAngle13412_cutSubjetPtRatio', polAngXmin, polAngXmax, polAnglabX, polAnglabY, True],
		[ 'Norm', 'subjetPolAngle31234_cutSubjetPtRatio', polAngXmin, polAngXmax, polAnglabX, polAnglabY, True],
		[ 'Norm', 'subjetMass21Ratio_cutTau31', '', '', '', '', True],
		[ 'Norm', 'subjet112MassRatio_cutTau31', '', '', '', '', True],
		[ 'Norm', 'subjet212MassRatio_cutTau31', '', '', '', '', True],
		[ 'Norm', 'subjetPolAngle13412_cutTau31', polAngXmin, polAngXmax, polAnglabX, polAnglabY, True],
		[ 'Norm', 'subjetPolAngle31234_cutTau31', polAngXmin, polAngXmax, polAnglabX, polAnglabY, True],

		[ 'CF', 'cutflow', 6, True],
		[ 'CF', 'cutflowSimple', 6, True],

		[ 'mini', 'massAve_Standard', 0, massMaxX, '', '', False],
		[ 'mini', 'massAve_EffPFHT800', 0, massMaxX, '', '', False],
		[ 'mini', 'massAve_Brock', 0, massMaxX, '', '', False],

		[ 'opt', 'massAve_massAsym', ["%02d" % x for x in range(10)], 0, massMaxX, '', '', False],

		[ 'trigger', 'massAve', 'cutDijet', 0, massMaxX, 2, triggerlabX, triggerlabY, True],
		[ 'trigger', 'massAve', 'cutMassAsym', 0, massMaxX, 2, triggerlabX, triggerlabY, False],
		[ 'trigger', 'massAve', 'cutCosTheta', 0, massMaxX, 2, triggerlabX, triggerlabY, False],
		[ 'trigger', 'massAve', 'cutSubjetPtRatio', 0, massMaxX, 2, triggerlabX, triggerlabY, False],
		[ 'trigger', 'HT', 'cutDijet', HTMinX, HTMaxX, 5, triggerlabX, triggerlabY, True],
		[ 'trigger', 'HT', 'cutMassAsym', HTMinX, HTMaxX, 5, triggerlabX, triggerlabY, True],
		[ 'trigger', 'HT', 'cutCosTheta', HTMinX, HTMaxX, 5, triggerlabX, triggerlabY, True],
		[ 'trigger', 'HT', 'cutSubjetPtRatio', HTMinX, HTMaxX, 5, triggerlabX, triggerlabY, True],
		[ 'trigger', 'jet1Mass', 'cutDijet', 0, massMaxX, 2, triggerlabX, triggerlabY, True],
		[ 'trigger', 'jet1Mass', 'cutMassAsym', 0, massMaxX, 2, triggerlabX, triggerlabY, True],
		[ 'trigger', 'jet1Mass', 'cutCosTheta', 0, massMaxX, 2, triggerlabX, triggerlabY, True],
		[ 'trigger', 'jet1Mass', 'cutSubjetPtRatio', 0, massMaxX, 2, triggerlabX, triggerlabY, True],
		[ 'trigger', 'jet1Pt', 'cutDijet', ptMinX, ptMaxX, 2, triggerlabX, triggerlabY, True],
		[ 'trigger', 'jet1Pt', 'cutMassAsym', ptMinX, ptMaxX, 2, triggerlabX, triggerlabY, True],
		[ 'trigger', 'jet1Pt', 'cutCosTheta', ptMinX, ptMaxX, 2, triggerlabX, triggerlabY, True],
		[ 'trigger', 'jet1Pt', 'cutSubjetPtRatio', ptMinX, ptMaxX, 2, triggerlabX, triggerlabY, True],
		[ 'trigger', 'trimmedMass', 'cutDijet', massMinX, massMaxX, 2, triggerlabX, triggerlabY, True],
		[ 'trigger', 'trimmedMass', 'cutMassAsym', massMinX, massMaxX, 2, triggerlabX, triggerlabY, True],
		[ 'trigger', 'trimmedMass', 'cutCosTheta', massMinX, massMaxX, 2, triggerlabX, triggerlabY, True],
		[ 'trigger', 'trimmedMass', 'cutSubjetPtRatio', massMinX, massMaxX, 2, triggerlabX, triggerlabY, True],
		[ 'trigger', 'ak4HT', 'cutDijet', HTMinX, HTMaxX, 5, triggerlabX, triggerlabY, True],
		[ 'trigger', 'ak4HT', 'cutMassAsym', HTMinX, HTMaxX, 5, triggerlabX, triggerlabY, True],
		[ 'trigger', 'ak4HT', 'cutCosTheta', HTMinX, HTMaxX, 5, triggerlabX, triggerlabY, True],
		[ 'trigger', 'ak4HT', 'cutSubjetPtRatio', HTMinX, HTMaxX, 5, triggerlabX, triggerlabY, True],

		[ '2D', 'jetMassHTDenom_noTrigger', 'Leading Trimmed Jet Mass [GeV]', 'HT [GeV]', 20, 200, 100, HTMaxX, 0.85, 0.2],
		[ '2D', 'jetMassHTDenom_triggerOne', 'Leading Trimmed Jet Mass [GeV]', 'HT [GeV]', 20, 200, 100, HTMaxX, 0.85, 0.2],
		[ '2D', 'jetMassHTDenom_triggerTwo', 'Leading Trimmed Jet Mass [GeV]', 'HT [GeV]', 20, 200, 100, HTMaxX, 0.85, 0.2],
		[ '2D', 'jetMassHTDenom_triggerOneAndTwo', 'Leading Trimmed Jet Mass [GeV]', 'HT [GeV]', 20, 200, 100, HTMaxX, 0.85, 0.2],
		[ '2dtrig', 'jetMassHT', 'cutDijet', 20, 200, 2, HTMinX, HTMaxX, 5, jetMassHTlabX, jetMassHTlabY+0.05],
		[ '2dtrig', 'jetMassHT', 'cutMassAsym', 20, 200, 2, HTMinX, HTMaxX, 5, jetMassHTlabX, jetMassHTlabY+0.05],
		[ '2dtrig', 'jetMassHT', 'cutCosTheta', 20, 200, 2, HTMinX, HTMaxX, 5, jetMassHTlabX, jetMassHTlabY+0.05],
		[ '2dtrig', 'jetMassHT', 'cutSubjetPtRatio', 20, 200, 2, HTMinX, HTMaxX, 5, jetMassHTlabX, jetMassHTlabY+0.05],
		]

	if 'all' in single: Plots = [ x[1:] for x in plotList if x[0] in process ]
	else: Plots = [ y[1:] for y in plotList if ( ( y[0] in process ) and ( y[1] in single ) )  ]

	if 'all' in grom: Groomers = [ '', 'Trimmed', 'Pruned', 'Filtered' ]
	else: Grommers = [ grom ]

	if 'all' in triggerUsed: Triggers = [ 'PFHT800', 'AK8PFHT700TrimMass50' ]
	#else: Triggers = [ triggerUsed.replace('TrimMass50','').replace('AK8','AK') ]
	else: Triggers = [ triggerUsed ]

	for i in Plots:
		for optGrom in Grommers:
			if '2D' in process: 
				plot2D( inputFileSignal, 'RPVSt100to'+jj, optGrom, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], PU )
				#plot2D( inputFileQCD, 'QCD'+qcd, optGrom, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], PU )

			elif '1D' in process:
				plot( inputFileSignal, inputFileQCD, 1.5, optGrom, boosted+'AnalysisPlots'+optGrom+'/'+i[0], i[0], i[1], i[2], i[3], i[4], i[5], PU )
			
			elif 'mini' in process:
				plot( inputMiniFileSignal, inputMiniFileQCD, 1.5, optGrom, i[0], i[0], i[1], i[2], i[3], i[4], i[5], PU )
			
			elif 'Norm' in process:
				plot( inputFileSignal, inputFileQCD, 1.5, optGrom, boosted+'AnalysisPlots'+optGrom+'/'+i[0], i[0], i[1], i[2], i[3], i[4], i[5], PU, True )

			elif 'CF' in process:
				plotCutFlow( inputFileSignal, inputFileQCD, optGrom, i[0], i[1], i[2], PU, True )

			elif 'opt' in process:
				plotOptimization( inputMiniFileSignal, inputMiniFileQCD, optGrom, i[0], i[1], i[2], i[3], i[4], True )
			elif 'trigger' in process:
				for trig in Triggers:
					tmpplotTriggerEfficiency( inputTrigger, SAMPLE, 'PFHT475', trig, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7] )
					#plotTriggerEfficiency( inputTrigger, SAMPLE, 'PFHT475', trig, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7] )
					#plotTriggerEfficiency( inputTrigger, SAMPLE, 'PFMET170', trig, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7] )
					#plotTriggerEfficiency( inputTrigger, SAMPLE, 'IsoMu17', trig, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7] )
			elif '2dtrig' in process:
				for trig in Triggers:
					plot2DTriggerEfficiency( inputTrigger, SAMPLE, BASEDTrigger, trig, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9] )
					#plot2DTriggerEfficiency( inputTrigger, SAMPLE, 'IsoMu17', trig, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9] )



