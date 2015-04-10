#!/usr/bin/env python
'''
File: DrawHistogram.py
Author: Alejandro Gomez Espinosa
Email: gomez@physics.rutgers.edu
Description: My Draw histograms. Check for options at the end.
'''

#from ROOT import TFile, TH1F, THStack, TCanvas, TMath, gROOT, gPad
from ROOT import *
from setTDRStyle import *
import time, os, math, sys
#import tarfile
import argparse


gROOT.Reset()
gROOT.SetBatch()
setTDRStyle()
gROOT.ForceStyle()
gROOT.SetStyle('tdrStyle')


gStyle.SetOptStat(0)

def labels( name, sample, PU, X=0.6, Y=0.70 ):
	if 'cutHT' in name: setSelection( sample, '13 TeV - '+PU, 'jet p_{T} > 150 GeV', 'jet |#eta| < 2.4', 'HT > 700 TeV', '', '', X, Y)
	elif 'cutAsym' in name: setSelection( sample, '13 TeV - '+PU, 'HT > 700 TeV', 'A < 0.1', '', '', '', X, Y )
	elif 'cutCosTheta' in name: setSelection( sample, '13 TeV - '+PU, 'HT > 700 TeV', 'A < 0.1', '|cos(#theta*)| < 0.3', '', '', X, Y )
	elif 'cutSubjetPtRatio' in name: setSelection( sample, '13 TeV - '+PU, 'HT > 700 TeV', 'A < 0.1', '|cos(#theta*)| < 0.3', 'subjet pt ratio > 0.3', '', X, Y )
	elif 'cutTau31' in name: setSelection( sample, '13 TeV - '+PU, 'HT > 700 TeV', 'A < 0.1', '|cos(#theta*)| < 0.3', '#tau_{31} < 0.5', '', X, Y )
	elif '' in name: setSelection( sample, '', '', '', '', '', '', X, Y) 
	else: setSelection( ' ' )

def labelAxis(name, histo, Grom ):

	if 'massAve' in name: 
		if 'Trimmed' in Grom: histo.GetXaxis().SetTitle( 'Average Trimmed Mass [GeV]' )
		elif 'Pruned' in Grom: histo.GetXaxis().SetTitle( 'Average Pruned Mass [GeV]' )
		elif 'Filtered' in Grom: histo.GetXaxis().SetTitle( 'Average Filtered Mass [GeV]' )
		else: histo.GetXaxis().SetTitle( 'Average Mass [GeV]' )
	elif 'massAsymmetry' in name: histo.GetXaxis().SetTitle( 'Mass Asymmetry (A)' )
	elif 'cosThetaStar' in name: histo.GetXaxis().SetTitle( 'cos(#theta *)' )
	elif 'jetEta' in name: histo.GetXaxis().SetTitle( 'Jet #eta' )
	elif 'Tau1_' in name: histo.GetXaxis().SetTitle( '#tau_{1}' )
	elif 'Tau2_' in name: histo.GetXaxis().SetTitle( '#tau_{2}' )
	elif 'Tau3_' in name: histo.GetXaxis().SetTitle( '#tau_{3}' )
	elif 'Tau21_' in name: histo.GetXaxis().SetTitle( '#tau_{21} ' )
	elif 'Tau31_' in name: histo.GetXaxis().SetTitle( '#tau_{31} ' )
	elif 'Tau32_' in name: histo.GetXaxis().SetTitle( '#tau_{32} ' )
	elif 'PtRatio' in name: histo.GetXaxis().SetTitle( 'Subjet pt ratio (min[ p_{T}^{sj1}, p_{T}^{sj2}/ max[ p_{T}^{sj1}, p_{T}^{sj2})' )
	elif 'Mass21' in name: histo.GetXaxis().SetTitle( 'Subjet m_{2}/m_{1}' )
	elif '112Mass' in name: histo.GetXaxis().SetTitle( 'Subjet m_{1}/m_{12}' )
	elif '212Mass' in name: histo.GetXaxis().SetTitle( 'Subjet m_{2}/m_{12}' )
	elif 'PolAngle13412_' in name: histo.GetXaxis().SetTitle( 'cos \psi_{1(34)}^{[12]}' )
	elif 'PolAngle31234_' in name: histo.GetXaxis().SetTitle( 'cos \psi_{3(12)}^{[34]}' )
	elif 'HT' in name: histo.GetXaxis().SetTitle( 'HT [GeV]' )
	elif 'jetPt' in name: histo.GetXaxis().SetTitle( 'Jet p_{T} [GeV]' )
	elif 'NPV' in name: histo.GetXaxis().SetTitle( 'Number of Primary Vertex' )


def plot( inFileSignal, inFileQCD, Grom, name, xmax, labX, labY, log, PU, Norm=False ):
	"""docstring for plot"""

	outputFileName = name+'_'+Grom+'_RPVSt100to'+jj+'_'+PU+'_QCD_AnalysisPlots.pdf' 
	print 'Processing.......', outputFileName

	histos = {}
	histos[ 'Signal' ] = inFileSignal.Get( 'AnalysisPlots'+Grom+'/'+name )
	histos[ 'QCD' ] = inFileQCD.Get( 'AnalysisPlots'+Grom+'/'+name )

	hSignal = histos[ 'Signal' ].Clone()
	hSignalQCD = histos[ 'Signal' ].Clone()
	hSignalQCD.Add( histos[ 'QCD' ].Clone() )
	hSignal.Divide( hSignalQCD )

#	histos.values()[0].SetMaximum( 2* max( listMax ) ) 
#	histos.values()[0].GetXaxis().SetRange( 0, xmax )
	binWidth = histos['Signal'].GetBinWidth(1)

	legend=TLegend(0.60,0.75,0.90,0.90)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.03)

	if not Norm:
		#histos[ 'Signal' ].Scale(100)
		tmpHisto = histos[ 'Signal' ].Clone()
		tmpHisto.SetLineColor(49)
		tmpHisto.SetFillColor(0)
		tmpHisto.SetLineWidth(2)
		histos[ 'Signal' ].SetFillColor(48)
		histos[ 'Signal' ].SetFillStyle(1001)
		histos[ 'Signal' ].SetFillColor(48)
		histos[ 'QCD' ].SetFillColor(38)
		histos[ 'QCD' ].SetFillStyle(1001)
		histos[ 'Signal' ].Scale(0.25)
		histos[ 'QCD' ].Scale(0.25)
		tmpHisto.Scale(0.25)

		stackHisto = THStack('stackHisto', 'stack')
		stackHisto.Add( histos['QCD'] )
		stackHisto.Add( histos['Signal'] )

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

		legend.AddEntry( histos[ 'Signal' ], 'RPV #tilde{t}#rightarrow '+jj+' 100 GeV' , 'f' )
		legend.AddEntry( histos[ 'QCD' ], 'QCD' , 'f' )
		stackHisto.SetMinimum(10)
		stackHisto.Draw('hist')
		stackHisto.GetYaxis().SetTitleOffset(1.2)
		#histos['Signal'].Draw('hist same')
		tmpHisto.Draw("hist same")
		stackHisto.GetYaxis().SetTitle( 'Events / '+str(binWidth) )

		labelAxis( name, stackHisto, Grom )
		legend.Draw()
		if not (labX and labY): labels( name, 'Scaled to '+lumi+' fb^{-1}', PU )
		else: labels( name, 'Scaled to '+lumi+' fb^{-1}', PU, labX, labY )

		pad2.cd()
		hSignal.SetFillColor(48)
		hSignal.SetFillStyle(1001)
		hSignal.GetYaxis().SetTitle("S / S+B")
		hSignal.GetYaxis().SetLabelSize(0.12)
		hSignal.GetXaxis().SetLabelSize(0.12)
		hSignal.GetYaxis().SetTitleSize(0.12)
		hSignal.GetYaxis().SetTitleOffset(0.45)
		hSignal.SetMaximum(0.7)
		hSignal.Sumw2()
		hSignal.Draw("hist")

		can.SaveAs( 'Plots/'+outName )
		del can
	else:
		histos[ 'Signal' ].SetLineWidth(2)
		histos[ 'Signal' ].SetLineColor(48)
		histos[ 'QCD' ].SetLineColor(38)
		histos[ 'QCD' ].SetLineWidth(2)

		can = TCanvas('c1', 'c1',  10, 10, 750, 500 )
		if log: 
			can.SetLogy()
			outName = outputFileName.replace('_AnalysisPlots','_Log_AnalysisPlots')
			histos[ 'Signal' ].GetYaxis().SetTitleOffset(1.2)
		else:
			outName = outputFileName 

		legend.AddEntry( histos[ 'Signal' ], 'RPV #tilde{t}#rightarrow '+jj+' 100 GeV' , 'l' )
		legend.AddEntry( histos[ 'QCD' ], 'QCD' , 'l' )
		histos['Signal'].GetYaxis().SetTitle( 'Normalized / '+str(binWidth) )

		histos['Signal'].DrawNormalized()
		histos['QCD'].DrawNormalized('same')

		legend.Draw()
		labelAxis( name, histos['Signal'], Grom )
		if not (labX and labY): labels( name, 'Scaled to '+lumi+' fb^{-1}', PU )
		else: labels( name, 'Scaled to '+lumi+' fb^{-1}', PU, labX, labY )

		can.SaveAs( 'Plots/'+outName )
		del can


def plot2D( inFile, sample, Grom, name, titleXAxis, titleXAxis2, xmax, xmax2, legX, legY, PU ):
	"""docstring for plot"""

	outputFileName = name+'_'+Grom+'_'+sample+'_'+PU+'_AnalysisPlots.pdf' 
	print 'Processing.......', outputFileName
	h1 = inFile.Get( 'AnalysisPlots'+Grom+'/'+name )

	h1.GetXaxis().SetTitle( titleXAxis )
	h1.GetYaxis().SetTitle( titleXAxis2 )

	if not '' in (xmax or xmax2):
		h1.GetXaxis().SetRange( 0, xmax )
		h1.GetYaxis().SetRange( 0, xmax2 )

	can = TCanvas('c1', 'c1',  10, 10, 750, 500 )
	#can.SetLogz()
	h1.Draw('colz')

	if not (legX and legY): labels( name, sample, PU )
	else: labels( name, sample, PU, legX, legY )

	can.SaveAs( 'Plots/'+outputFileName )
	del can


def plotCutFlow( inFileSignal, inFileQCD, Grom, name, xmax, log, PU, Norm=False ):
	"""docstring for plot"""

	outputFileName = name+'_'+Grom+'_RPVSt100to'+jj+'_'+PU+'_QCD_AnalysisPlots.pdf' 
	print 'Processing.......', outputFileName

	histos = {}
	histos[ 'Signal' ] = inFileSignal.Get( 'AnalysisPlots'+Grom+'/'+name )
	histos[ 'QCD' ] = inFileQCD.Get( 'AnalysisPlots'+Grom+'/'+name )

	hSignal = histos[ 'Signal' ].Clone()
	hQCD = histos[ 'QCD' ].Clone()
	hSB = hSignal.Clone()
	hSB.Divide( hQCD )

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
		hSB.GetXaxis().SetBinLabel( ibin, '')
		
	print "Signal", cutFlowSignalList
	print "QCD", cutFlowQCDList

	#hSB = hSignal.Clone()
	#hSB.Divide( hQCD )

#	histos.values()[0].SetMaximum( 2* max( listMax ) ) 
#	histos.values()[0].GetXaxis().SetRange( 0, xmax )
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

	legend.AddEntry( hSignal, 'RPV #tilde{t}#rightarrow '+jj+' 100 GeV' , 'l' )
	legend.AddEntry( hQCD, 'QCD' , 'l' )
	hSignal.GetYaxis().SetTitle( 'Percentage / '+str(binWidth) )

	hSignal.SetMinimum(0.000001)
	hSignal.Draw()
	hQCD.Draw('same')

	legend.Draw()
	labels( name, '', '' )

	pad2.cd()
	hSB.GetYaxis().SetTitle("S / B")
	hSB.GetYaxis().SetLabelSize(0.12)
	hSB.GetXaxis().SetLabelSize(0.12)
	hSB.GetYaxis().SetTitleSize(0.12)
	hSB.GetYaxis().SetTitleOffset(0.45)
	#hSB.SetMaximum(0.7)
	hSB.Sumw2()
	hSB.Draw("hist")

	can.SaveAs( 'Plots/'+outName )
	del can

def plotSimple( inFile, sample, name, xmax, labX, labY, log, PU, Norm=False ):
	"""docstring for plot"""

	outputFileName = name+'_'+sample+'_MCAnalysisPlots.pdf' 
	print 'Processing.......', outputFileName

	histo = inFile.Get( 'AnalysisPlots/'+name )

#	histos.values()[0].SetMaximum( 2* max( listMax ) ) 
#	histos.values()[0].GetXaxis().SetRange( 0, xmax )
	binWidth = histo.GetBinWidth(1)

	legend=TLegend(0.60,0.75,0.90,0.90)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.03)

	#histos[ 'Signal' ].Scale(100)
	histo.SetFillColor(48)
	histo.SetFillStyle(1001)

	can = TCanvas('c1', 'c1',  10, 10, 750, 500 )

	if log: 
		can.SetLogy()
		outName = outputFileName.replace('_AnalysisPlots','_Log_AnalysisPlots')
	else:
		outName = outputFileName 

	legend.AddEntry( histo, 'RPV #tilde{t}#rightarrow '+jj+' 100 GeV' , 'f' )
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

	outputFileName = name+'_'+Grom+'_RPVSt100to'+jj+'_Diff'+Diff+'.pdf' 
	print 'Processing.......', outputFileName

	histos = {}
	histos[ 'Sample1' ] = inFileSample1.Get( 'AnalysisPlots'+Grom+'/'+name )
	histos[ 'Sample2' ] = inFileSample2.Get( 'AnalysisPlots'+Grom+'/'+name )

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
		#histos[ 'Sample1' ].Scale(0.25)
		#histos[ 'Sample1' ].SetMaximum( 1.2* max( histos[ 'Sample1' ].GetMaximum(), histos[ 'Sample2' ].GetMaximum() ) ) 
		#histos.values()[0].GetXaxis().SetRange( 0, xmax )

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
		if not (labX and labY): labels( name, 'Scaled to '+lumi+' fb^{-1}', '' )
		else: labels( name, 'Scaled to '+lumi+' fb^{-1}', '', labX, labY )

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
		if not (labX and labY): labels( name, 'Scaled to '+lumi+' fb^{-1}', '' )
		else: labels( name, 'Scaled to '+lumi+' fb^{-1}', '', labX, labY )

		can.SaveAs( 'Plots/'+outName )
		del can

def plotDiffPU( inFileSample, Grom, name, xmax, labX, labY, log, Diff , Norm=False):
	"""docstring for plot"""

	outputFileName = name+'_'+Grom+'_RPVSt100to'+jj+'_Diff'+Diff+'s.pdf' 
	print 'Processing.......', outputFileName

	histos = {}
	histos[ 'Sample1' ] = inFileSample.Get( 'AnalysisPlots'+Grom+'/'+name.replace('_','LowPU_' ) )
	histos[ 'Sample2' ] = inFileSample.Get( 'AnalysisPlots'+Grom+'/'+name.replace('_','MedPU_' ) )
	histos[ 'Sample3' ] = inFileSample.Get( 'AnalysisPlots'+Grom+'/'+name.replace('_','HighPU_' ) )

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
	#histos.values()[0].GetXaxis().SetRange( 0, xmax )

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
	if not (labX and labY): labels( name, 'Scaled to '+lumi+' fb^{-1}', '' )
	else: labels( name, 'Scaled to '+lumi+' fb^{-1}', '', labX, labY )

	can.SaveAs( 'Plots/'+outName )
	del can

	'''
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
		if not (labX and labY): labels( name, 'Scaled to '+lumi+' fb^{-1}', '' )
		else: labels( name, 'Scaled to '+lumi+' fb^{-1}', '', labX, labY )

		can.SaveAs( 'Plots/'+outName )
		del can
	'''

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--proc', action='store', default='1D', help='Process to draw, example: 1D, 2D, MC.' )
	parser.add_argument('-d', '--decay', action='store', default='jj', help='Decay, example: jj, bj.' )
	parser.add_argument('-pu', '--PU', action='store', default='PU20bx25', help='PU, example: PU40bx25.' )
	parser.add_argument('-l', '--lumi', action='store', default='1', help='Luminosity, example: 1.' )
	args = parser.parse_args()

	process = args.proc
	jj = args.decay
	PU = args.PU
	lumi = args.lumi
	
	inputFileSample = TFile.Open('RUNAnalysis_RPVSt100tojj_pythia8_13TeV_PU40bx50_PHYS14.root')
	inputFileSignal = TFile.Open('Rootfiles/RUNAnalysis_RPVSt100to'+jj+'_'+PU+'.root')
	inputFileMCSignal = TFile.Open('RUNMCAnalysis_RPVSt100tojj_pythia8_13TeV_PU20bx25.root')
	inputFileQCD = TFile.Open('Rootfiles/RUNAnalysis_QCDALL_'+PU+'.root')

	if '2D' in process:

		dijetlabX = 0.15
		dijetlabY = 0.88
		subjet112vs212labX = 0.7
		subjet112vs212labY = 0.88

		Plots_2D = [ 
			[ 'jet1Subjet112vs212MassRatio_cutHT', 'm_{1}/m_{12}', 'm_{2}/m_{12}', '', '', subjet112vs212labX, subjet112vs212labY  ],
			[ 'jet1Subjet1JetvsSubjet2JetMassRatio_cutHT', 'm_{1}/M_{12}', 'm_{2}/M_{12}', '', '', subjet112vs212labX, subjet112vs212labY  ],
			[ 'jet2Subjet112vs212MassRatio_cutHT', 'm_{3}/m_{34}', 'm_{4}/m_{34}', '', '', subjet112vs212labX, subjet112vs212labY  ],
			[ 'jet2Subjet1JetvsSubjet2JetMassRatio_cutHT', 'm_{3}/M_{34}', 'm_{4}/M_{34}', '', '', subjet112vs212labX, subjet112vs212labY  ],
			[ 'subjet12Mass_cutHT', 'm_{1}', 'm_{2}', '', '', dijetlabX, dijetlabY  ],
			[ 'dijetCorr_cutHT', '#eta_{sjet1}', '#eta_{sjet2}', '', '', dijetlabX, dijetlabY  ],
			[ 'dijetCorrPhi_cutHT', '#phi_{sjet1}', '#phi_{sjet2}', '', '', dijetlabX, dijetlabY  ],
			[ 'subjet112vs212MassRatio_cutHT', 'm_{1}/m_{12}', 'm_{2}/m_{12}', '', '', subjet112vs212labX, subjet112vs212labY  ],
			[ 'subjet1JetvsSubjet2JetMassRatio_cutHT', 'm_{1}/M_{12}', 'm_{2}/M_{12}', '', '', subjet112vs212labX, subjet112vs212labY  ],
			[ 'subjetPolAngle13412vs31234_cutHT', 'cos #psi_{1(34)}^{[12]}', 'cos #psi_{3(12)}^{[34]}', '', '', '', ''  ],
			[ 'tmpSubjetPolAngle13412vs31234_cutHT', 'cos #psi_{1(34)}^{[12]}', 'cos #psi_{3(12)}^{[34]}', '', '', '', ''  ],
			[ 'mu1234_cutHT', '', '', '', '', dijetlabX, dijetlabY  ],
			[ 'mu3412_cutHT', '', '', '', '', dijetlabX, dijetlabY  ],
			[ 'dalitz1234_cutHT', 'y', 'x', '', '', dijetlabX, dijetlabY  ],
			[ 'dalitz3412_cutHT', 'y', 'x', '', '', dijetlabX, dijetlabY  ],

			[ 'subjet12Mass_cutAsym', 'm_{1}', 'm_{2}', '', '', dijetlabX, dijetlabY  ],
			[ 'dijetCorr_cutAsym', '#eta_{sjet1}', '#eta_{sjet2}', '', '', dijetlabX, dijetlabY  ],
			[ 'dijetCorrPhi_cutAsym', '#phi_{sjet1}', '#phi_{sjet2}', '', '', dijetlabX, dijetlabY  ],
			[ 'subjet112vs212MassRatio_cutAsym', 'm_{1}/m_{12}', 'm_{2}/m_{12}', '', '', subjet112vs212labX, subjet112vs212labY  ],
			[ 'subjet1JetvsSubjet2JetMassRatio_cutAsym', 'm_{1}/M_{12}', 'm_{2}/M_{12}', '', '', subjet112vs212labX, subjet112vs212labY  ],
			[ 'subjetPolAngle13412vs31234_cutAsym', 'cos #psi_{1(34)}^{[12]}', 'cos #psi_{3(12)}^{[34]}', '', '', '', ''  ],
			[ 'tmpSubjetPolAngle13412vs31234_cutAsym', 'cos #psi_{1(34)}^{[12]}', 'cos #psi_{3(12)}^{[34]}', '', '', '', ''  ],
			#[ 'mu1234_cutAsym', '', '', '', '', dijetlabX, dijetlabY  ],
			#[ 'mu3412_cutAsym', '', '', '', '', dijetlabX, dijetlabY  ],
			[ 'dalitz1234_cutAsym', 'y', 'x', '', '', dijetlabX, dijetlabY  ],
			[ 'dalitz3412_cutAsym', 'y', 'x', '', '', dijetlabX, dijetlabY  ],

			[ 'subjet12Mass_cutCosTheta', 'm_{1}', 'm_{2}', '', '', dijetlabX, dijetlabY  ],
			[ 'dijetCorr_cutCosTheta', '#eta_{sjet1}', '#eta_{sjet2}', '', '', dijetlabX, dijetlabY  ],
			[ 'dijetCorrPhi_cutCosTheta', '#phi_{sjet1}', '#phi_{sjet2}', '', '', dijetlabX, dijetlabY  ],
			[ 'subjet112vs212MassRatio_cutCosTheta', 'm_{1}/m_{12}', 'm_{2}/m_{12}', '', '', subjet112vs212labX, subjet112vs212labY  ],
			[ 'subjet1JetvsSubjet2JetMassRatio_cutCosTheta', 'm_{1}/M_{12}', 'm_{2}/M_{12}', '', '', subjet112vs212labX, subjet112vs212labY  ],
			[ 'subjetPolAngle13412vs31234_cutCosTheta', 'cos #psi_{1(34)}^{[12]}', 'cos #psi_{3(12)}^{[34]}', '', '', '', ''  ],
			[ 'tmpSubjetPolAngle13412vs31234_cutCosTheta', 'cos #psi_{1(34)}^{[12]}', 'cos #psi_{3(12)}^{[34]}', '', '', '', ''  ],
			#[ 'mu1234_cutCosTheta', '', '', '', '', dijetlabX, dijetlabY  ],
			#[ 'mu3412_cutCosTheta', '', '', '', '', dijetlabX, dijetlabY  ],
			[ 'dalitz1234_cutCosTheta', 'y', 'x', '', '', dijetlabX, dijetlabY  ],
			[ 'dalitz3412_cutCosTheta', 'y', 'x', '', '', dijetlabX, dijetlabY  ],

			[ 'subjet12Mass_cutSubjetPtRatio', 'm_{1}', 'm_{2}', '', '', dijetlabX, dijetlabY  ],
			[ 'dijetCorr_cutSubjetPtRatio', '#eta_{sjet1}', '#eta_{sjet2}', '', '', dijetlabX, dijetlabY  ],
			[ 'dijetCorrPhi_cutSubjetPtRatio', '#phi_{sjet1}', '#phi_{sjet2}', '', '', dijetlabX, dijetlabY  ],
			[ 'subjet112vs212MassRatio_cutSubjetPtRatio', 'm_{1}/m_{12}', 'm_{2}/m_{12}', '', '', subjet112vs212labX, subjet112vs212labY  ],
			[ 'subjet1JetvsSubjet2JetMassRatio_cutSubjetPtRatio', 'm_{1}/M_{12}', 'm_{2}/M_{12}', '', '', subjet112vs212labX, subjet112vs212labY  ],
			[ 'subjetPolAngle13412vs31234_cutSubjetPtRatio', 'cos #psi_{1(34)}^{[12]}', 'cos #psi_{3(12)}^{[34]}', '', '', '', ''  ],
			[ 'tmpSubjetPolAngle13412vs31234_cutSubjetPtRatio', 'cos #psi_{1(34)}^{[12]}', 'cos #psi_{3(12)}^{[34]}', '', '', '', ''  ],
			#[ 'mu1234_cutSubjetPtRatio', '', '', '', '', dijetlabX, dijetlabY  ],
			#[ 'mu3412_cutSubjetPtRatio', '', '', '', '', dijetlabX, dijetlabY  ],
			[ 'dalitz1234_cutSubjetPtRatio', 'y', 'x', '', '', dijetlabX, dijetlabY  ],
			[ 'dalitz3412_cutSubjetPtRatio', 'y', 'x', '', '', dijetlabX, dijetlabY  ],

			[ 'subjet12Mass_cutTau31', 'm_{1}', 'm_{2}', '', '', dijetlabX, dijetlabY  ],
			[ 'dijetCorr_cutTau31', '#eta_{sjet1}', '#eta_{sjet2}', '', '', dijetlabX, dijetlabY  ],
			[ 'dijetCorrPhi_cutTau31', '#phi_{sjet1}', '#phi_{sjet2}', '', '', dijetlabX, dijetlabY  ],
			[ 'subjet112vs212MassRatio_cutTau31', 'm_{1}/m_{12}', 'm_{2}/m_{12}', '', '', subjet112vs212labX, subjet112vs212labY  ],
			[ 'subjet1JetvsSubjet2JetMassRatio_cutTau31', 'm_{1}/M_{12}', 'm_{2}/M_{12}', '', '', subjet112vs212labX, subjet112vs212labY  ],
			[ 'subjetPolAngle13412vs31234_cutTau31', 'cos #psi_{1(34)}^{[12]}', 'cos #psi_{3(12)}^{[34]}', '', '', '', ''  ],
			[ 'tmpSubjetPolAngle13412vs31234_cutTau31', 'cos #psi_{1(34)}^{[12]}', 'cos #psi_{3(12)}^{[34]}', '', '', '', ''  ],
			#[ 'mu1234_cutTau31', '', '', '', '', dijetlabX, dijetlabY  ],
			#[ 'mu3412_cutTau31', '', '', '', '', dijetlabX, dijetlabY  ],
			#[ 'dalitz1234_cutTau31', 'y', 'x', '', '', dijetlabX, dijetlabY  ],
			#[ 'dalitz3412_cutTau31', 'y', 'x', '', '', dijetlabX, dijetlabY  ],
			]

		for i in Plots_2D: 
			plot2D( inputFileSignal, 'RPVSt100to'+jj, '', i[0], i[1], i[2], i[3], i[4], i[5], i[6], PU )
			plot2D( inputFileSignal, 'RPVSt100to'+jj, 'Trimmed', i[0], i[1], i[2], i[3], i[4], i[5], i[6], PU )
			plot2D( inputFileSignal, 'RPVSt100to'+jj, 'Pruned', i[0], i[1], i[2], i[3], i[4], i[5], i[6], PU )
			plot2D( inputFileSignal, 'RPVSt100to'+jj, 'Filtered', i[0], i[1], i[2], i[3], i[4], i[5], i[6], PU )
			plot2D( inputFileQCD, 'QCD', '', i[0], i[1], i[2], i[3], i[4], i[5], i[6], PU )
			plot2D( inputFileQCD, 'QCD', 'Trimmed', i[0], i[1], i[2], i[3], i[4], i[5], i[6], PU )
			plot2D( inputFileQCD, 'QCD', 'Pruned', i[0], i[1], i[2], i[3], i[4], i[5], i[6], PU )
			plot2D( inputFileQCD, 'QCD', 'Filtered', i[0], i[1], i[2], i[3], i[4], i[5], i[6], PU )

	elif '1D' in process:

		Plots = [
			[ 'jetPt', '', '', '', True],
			[ 'jetPt', '', '', '', False],
			[ 'jetEta', '', '', '', True],
			[ 'jetEta', '', '', '', False],
			[ 'jetMass', '', '', '', True],
			[ 'jetMass', '', '', '', False],
			[ 'HT', '', '', '', True],
			[ 'HT', '', '', '', False],
			[ 'massAve_cutHT', '', '', '', True],
			[ 'massAve_cutHT', '', '', '', False],
			[ 'jet1Subjet1Pt_cutHT', '', '', '', True],
			[ 'jet1Subjet1Pt_cutHT', '', '', '', False],
			[ 'jet1Subjet2Pt_cutHT', '', '', '', True],
			[ 'jet1Subjet2Pt_cutHT', '', '', '', False],
			[ 'jet2Subjet1Pt_cutHT', '', '', '', True],
			[ 'jet2Subjet1Pt_cutHT', '', '', '', False],
			[ 'jet2Subjet2Pt_cutHT', '', '', '', True],
			[ 'jet2Subjet2Pt_cutHT', '', '', '', False],
			[ 'jet1Subjet1Mass_cutHT', '', '', '', True],
			[ 'jet1Subjet1Mass_cutHT', '', '', '', False],
			[ 'jet1Subjet2Mass_cutHT', '', '', '', True],
			[ 'jet1Subjet2Mass_cutHT', '', '', '', False],
			[ 'jet2Subjet1Mass_cutHT', '', '', '', True],
			[ 'jet2Subjet1Mass_cutHT', '', '', '', False],
			[ 'jet2Subjet2Mass_cutHT', '', '', '', True],
			[ 'jet2Subjet2Mass_cutHT', '', '', '', False],
			[ 'massAve_cutAsym', '', '', '', True],
			[ 'massAve_cutAsym', '', '', '', False],
			[ 'massAve_cutCosTheta', '', '', '', True],
			[ 'massAve_cutCosTheta', '', '', '', False],
			[ 'massAve_cutSubjetPtRatio', '', '', '', True],
			[ 'massAve_cutSubjetPtRatio', '', '', '', False],
			[ 'massAve_cutTau31', '', '', '', True],
			[ 'massAve_cutTau31', '', '', '', False],
			]

		for i in Plots: 
			plot( inputFileSignal, inputFileQCD, '', i[0], i[1], i[2], i[3], i[4], PU )
			plot( inputFileSignal, inputFileQCD, 'Trimmed', i[0], i[1], i[2], i[3], i[4], PU )
			plot( inputFileSignal, inputFileQCD, 'Pruned', i[0], i[1], i[2], i[3], i[4], PU )
			plot( inputFileSignal, inputFileQCD, 'Filtered', i[0], i[1], i[2], i[3], i[4], PU )
		

	elif 'Norm' in process:

		polAnglabX = 0.2
		polAnglabY = 0.88
		taulabX = 0.6
		taulabY = 0.40

		NormPlots = [
			[ 'jet1Tau1_cutHT', '', taulabX, taulabY, True],
			[ 'jet1Tau1_cutHT', '', taulabX, taulabY, False],
			[ 'jet1Tau2_cutHT', '', taulabX, taulabY, True],
			[ 'jet1Tau2_cutHT', '', taulabX, taulabY, False],
			[ 'jet1Tau3_cutHT', '', taulabX, taulabY, True],
			[ 'jet1Tau3_cutHT', '', taulabX, taulabY, False],
			[ 'jet1Tau21_cutHT', '', taulabX, taulabY, True],
			[ 'jet1Tau21_cutHT', '', taulabX, taulabY, False],
			[ 'jet1Tau31_cutHT', '', taulabX, taulabY, True],
			[ 'jet1Tau31_cutHT', '', taulabX, taulabY, False],
			[ 'jet1Tau32_cutHT', '', taulabX, taulabY, True],
			[ 'jet1Tau32_cutHT', '', taulabX, taulabY, False],
			[ 'jet1SubjetPtRatio_cutHT', '', '', '', True],
			[ 'jet1SubjetPtRatio_cutHT', '', '', '', False],
			[ 'jet2SubjetPtRatio_cutHT', '', '', '', True],
			[ 'jet2SubjetPtRatio_cutHT', '', '', '', False],
			[ 'subjetPtRatio_cutHT', '', '', '', True],
			[ 'subjetPtRatio_cutHT', '', '', '', False],
			[ 'massAsymmetry_cutHT', '', '', '', True],
			[ 'massAsymmetry_cutHT', '', '', '', False],
			[ 'cosThetaStar_cutHT', '', '', '', True],
			[ 'cosThetaStar_cutHT', '', '', '', False],
			#[ 'jet1Subjet21MassRatio_cutHT', '', '', '', True],
			#[ 'jet1Subjet21MassRatio_cutHT', '', '', '', False],
			[ 'jet1Subjet112MassRatio_cutHT', '', '', '', True],
			[ 'jet1Subjet112MassRatio_cutHT', '', '', '', False],
			[ 'jet1Subjet1JetMassRatio_cutHT', '', '', '', True],
			[ 'jet1Subjet1JetMassRatio_cutHT', '', '', '', False],
			[ 'jet1Subjet212MassRatio_cutHT', '', '', '', True],
			[ 'jet1Subjet212MassRatio_cutHT', '', '', '', False],
			[ 'jet1Subjet2JetMassRatio_cutHT', '', '', '', True],
			[ 'jet1Subjet2JetMassRatio_cutHT', '', '', '', False],
			[ 'jet2Subjet112MassRatio_cutHT', '', '', '', True],
			[ 'jet2Subjet112MassRatio_cutHT', '', '', '', False],
			[ 'jet2Subjet1JetMassRatio_cutHT', '', '', '', True],
			[ 'jet2Subjet1JetMassRatio_cutHT', '', '', '', False],
			[ 'jet2Subjet212MassRatio_cutHT', '', '', '', True],
			[ 'jet2Subjet212MassRatio_cutHT', '', '', '', False],
			[ 'jet2Subjet2JetMassRatio_cutHT', '', '', '', True],
			[ 'jet2Subjet2JetMassRatio_cutHT', '', '', '', False],
			[ 'subjetPtRatio_cutHT', '', '', '', True],
			[ 'subjetPtRatio_cutHT', '', '', '', False],
			[ 'subjetMass21Ratio_cutHT', '', '', '', True],
			[ 'subjetMass21Ratio_cutHT', '', '', '', False],
			[ 'subjet112MassRatio_cutHT', '', '', '', True],
			[ 'subjet112MassRatio_cutHT', '', '', '', False],
			[ 'subjet212MassRatio_cutHT', '', '', '', True],
			[ 'subjet212MassRatio_cutHT', '', '', '', False],
			[ 'subjetPolAngle13412_cutHT', '', '', '', True],
			[ 'subjetPolAngle13412_cutHT', '', '', '', False],
			[ 'subjetPolAngle31234_cutHT', '', '', '', True],
			[ 'subjetPolAngle31234_cutHT', '', '', '', False],
			[ 'tmpSubjetPolAngle13412_cutHT', '', '', '', True],
			[ 'tmpSubjetPolAngle13412_cutHT', '', '', '', False],
			[ 'tmpSubjetPolAngle31234_cutHT', '', '', '', True],
			[ 'tmpSubjetPolAngle31234_cutHT', '', '', '', False],
			[ 'cosThetaStar_cutAsym', '', '', '', True],
			[ 'cosThetaStar_cutAsym', '', '', '', False],
			[ 'jet1Tau21_cutAsym', '', taulabX, taulabY, True],
			[ 'jet1Tau21_cutAsym', '', taulabX, taulabY, False],
			[ 'jet1Tau31_cutAsym', '', taulabX, taulabY, True],
			[ 'jet1Tau31_cutAsym', '', taulabX, taulabY, False],
			[ 'jet1Tau32_cutAsym', '', taulabX, taulabY, True],
			[ 'jet1Tau32_cutAsym', '', taulabX, taulabY, False],
			[ 'subjetPtRatio_cutAsym', '', '', '', True],
			[ 'subjetPtRatio_cutAsym', '', '', '', False],
			[ 'subjetPtRatio_cutAsym', '', '', '', True],
			[ 'subjetPtRatio_cutAsym', '', '', '', False],
			[ 'subjetMass21Ratio_cutAsym', '', '', '', True],
			[ 'subjetMass21Ratio_cutAsym', '', '', '', False],
			[ 'subjet112MassRatio_cutAsym', '', '', '', True],
			[ 'subjet112MassRatio_cutAsym', '', '', '', False],
			[ 'subjet212MassRatio_cutAsym', '', '', '', True],
			[ 'subjet212MassRatio_cutAsym', '', '', '', False],
			[ 'subjetPolAngle13412_cutAsym', '', '', '', True],
			[ 'subjetPolAngle13412_cutAsym', '', '', '', False],
			[ 'subjetPolAngle31234_cutAsym', '', '', '', True],
			[ 'subjetPolAngle31234_cutAsym', '', '', '', False],
			[ 'tmpSubjetPolAngle13412_cutAsym', '', '', '', True],
			[ 'tmpSubjetPolAngle13412_cutAsym', '', '', '', False],
			[ 'tmpSubjetPolAngle31234_cutAsym', '', '', '', True],
			[ 'tmpSubjetPolAngle31234_cutAsym', '', '', '', False],
			[ 'jet1Tau21_cutCosTheta', '', taulabX, taulabY, True],
			[ 'jet1Tau21_cutCosTheta', '', taulabX, taulabY, False],
			[ 'jet1Tau31_cutCosTheta', '', taulabX, taulabY, True],
			[ 'jet1Tau31_cutCosTheta', '', taulabX, taulabY, False],
			[ 'jet1Tau32_cutCosTheta', '', taulabX, taulabY, True],
			[ 'jet1Tau32_cutCosTheta', '', taulabX, taulabY, False],
			[ 'subjetPtRatio_cutCosTheta', '', '', '', True],
			[ 'subjetPtRatio_cutCosTheta', '', '', '', False],
			[ 'subjetPtRatio_cutCosTheta', '', '', '', True],
			[ 'subjetPtRatio_cutCosTheta', '', '', '', False],
			[ 'subjetMass21Ratio_cutCosTheta', '', '', '', True],
			[ 'subjetMass21Ratio_cutCosTheta', '', '', '', False],
			[ 'subjet112MassRatio_cutCosTheta', '', '', '', True],
			[ 'subjet112MassRatio_cutCosTheta', '', '', '', False],
			[ 'subjet212MassRatio_cutCosTheta', '', '', '', True],
			[ 'subjet212MassRatio_cutCosTheta', '', '', '', False],
			[ 'subjetPolAngle13412_cutCosTheta', '', '', '', True],
			[ 'subjetPolAngle13412_cutCosTheta', '', '', '', False],
			[ 'subjetPolAngle31234_cutCosTheta', '', '', '', True],
			[ 'subjetPolAngle31234_cutCosTheta', '', '', '', False],
			[ 'tmpSubjetPolAngle13412_cutCosTheta', '', '', '', True],
			[ 'tmpSubjetPolAngle13412_cutCosTheta', '', '', '', False],
			[ 'tmpSubjetPolAngle31234_cutCosTheta', '', '', '', True],
			[ 'tmpSubjetPolAngle31234_cutCosTheta', '', '', '', False],
			[ 'jet1Tau21_cutSubjetPtRatio', '', taulabX, taulabY, True],
			[ 'jet1Tau21_cutSubjetPtRatio', '', taulabX, taulabY, False],
			[ 'jet1Tau31_cutSubjetPtRatio', '', taulabX, taulabY, True],
			[ 'jet1Tau31_cutSubjetPtRatio', '', taulabX, taulabY, False],
			[ 'jet1Tau32_cutSubjetPtRatio', '', taulabX, taulabY, True],
			[ 'jet1Tau32_cutSubjetPtRatio', '', taulabX, taulabY, False],
			[ 'subjetMass21Ratio_cutSubjetPtRatio', '', '', '', True],
			[ 'subjetMass21Ratio_cutSubjetPtRatio', '', '', '', False],
			[ 'subjet112MassRatio_cutSubjetPtRatio', '', '', '', True],
			[ 'subjet112MassRatio_cutSubjetPtRatio', '', '', '', False],
			[ 'subjet212MassRatio_cutSubjetPtRatio', '', '', '', True],
			[ 'subjet212MassRatio_cutSubjetPtRatio', '', '', '', False],
			[ 'subjetPolAngle13412_cutSubjetPtRatio', '', polAnglabX, polAnglabY, True],
			[ 'subjetPolAngle13412_cutSubjetPtRatio', '', polAnglabX, polAnglabY, False],
			[ 'subjetPolAngle31234_cutSubjetPtRatio', '', polAnglabX, polAnglabY, True],
			[ 'subjetPolAngle31234_cutSubjetPtRatio', '', polAnglabX, polAnglabY, False],
			[ 'tmpSubjetPolAngle13412_cutSubjetPtRatio', '', polAnglabX, polAnglabY, True],
			[ 'tmpSubjetPolAngle13412_cutSubjetPtRatio', '', polAnglabX, polAnglabY, False],
			[ 'tmpSubjetPolAngle31234_cutSubjetPtRatio', '', polAnglabX, polAnglabY, True],
			[ 'tmpSubjetPolAngle31234_cutSubjetPtRatio', '', polAnglabX, polAnglabY, False],
			[ 'subjetMass21Ratio_cutTau31', '', '', '', True],
			[ 'subjetMass21Ratio_cutTau31', '', '', '', False],
			[ 'subjet112MassRatio_cutTau31', '', '', '', True],
			[ 'subjet112MassRatio_cutTau31', '', '', '', False],
			[ 'subjet212MassRatio_cutTau31', '', '', '', True],
			[ 'subjet212MassRatio_cutTau31', '', '', '', False],
			[ 'subjetPolAngle13412_cutTau31', '', polAnglabX, polAnglabY, True],
			[ 'subjetPolAngle13412_cutTau31', '', polAnglabX, polAnglabY, False],
			[ 'subjetPolAngle31234_cutTau31', '', polAnglabX, polAnglabY, True],
			[ 'subjetPolAngle31234_cutTau31', '', polAnglabX, polAnglabY, False],
			[ 'tmpSubjetPolAngle13412_cutTau31', '', polAnglabX, polAnglabY, True],
			[ 'tmpSubjetPolAngle13412_cutTau31', '', polAnglabX, polAnglabY, False],
			[ 'tmpSubjetPolAngle31234_cutTau31', '', polAnglabX, polAnglabY, True],
			[ 'tmpSubjetPolAngle31234_cutTau31', '', polAnglabX, polAnglabY, False],
			]

		for i in NormPlots: 
			plot( inputFileSignal, inputFileQCD, '', i[0], i[1], i[2], i[3], i[4], PU, True )
			plot( inputFileSignal, inputFileQCD, 'Trimmed', i[0], i[1], i[2], i[3], i[4], PU, True )
			plot( inputFileSignal, inputFileQCD, 'Pruned', i[0], i[1], i[2], i[3], i[4], PU, True )
			plot( inputFileSignal, inputFileQCD, 'Filtered', i[0], i[1], i[2], i[3], i[4], PU, True )


	elif 'CF' in process:
		CFPlots = [
			[ 'cutflow', '', True],
			[ 'cutflowSimple', '', True],
			]
		for i in CFPlots: 
			plotCutFlow( inputFileSignal, inputFileQCD, '', i[0], i[1], i[2], PU, True )
			plotCutFlow( inputFileSignal, inputFileQCD, 'Trimmed', i[0], i[1], i[2], PU, True )
			plotCutFlow( inputFileSignal, inputFileQCD, 'Pruned', i[0], i[1], i[2], PU, True )
			plotCutFlow( inputFileSignal, inputFileQCD, 'Filtered', i[0], i[1], i[2], PU, True )

	elif 'MC' in process:
		MCPlots = [
			[ 'subjetPtRatio', '', '', '', True],
			[ 'subjetPtRatio', '', '', '', False],
			[ 'subjetMass21Ratio', '', '', '', True],
			[ 'subjetMass21Ratio', '', '', '', False],
			[ 'subjet112MassRatio', '', '', '', True],
			[ 'subjet112MassRatio', '', '', '', False],
			[ 'subjet212MassRatio', '', '', '', True],
			[ 'subjet212MassRatio', '', '', '', False],
			[ 'subjetPolAngle13412', '', '', '', True],
			[ 'subjetPolAngle13412', '', '', '', False],
			[ 'subjetPolAngle31234', '', '', '', True],
			[ 'subjetPolAngle31234', '', '', '', False],
			#[ '', '', True],
			#[ '', '', False],
			#[ '', '', True],
			#[ '', '', False],
			]
		for i in MCPlots: 
			plotSimple( inputFileMCSignal, 'RPVSt100tojj', i[0], i[1], i[2], i[3], i[4], PU, True )

		dijetlabX = 0.15
		dijetlabY = 0.88
		subjet112vs212labX = 0.7
		subjet112vs212labY = 0.88

		MCPlots_2D = [
			[ 'dijetCorr', '#eta_{sjet1}', '#eta_{sjet2}', '', '', dijetlabX, dijetlabY  ],
			[ 'dijetCorrPhi', '#phi_{sjet1}', '#phi_{sjet2}', '', '', dijetlabX, dijetlabY  ],
			[ 'subjet12Mass', 'm_{1}', 'm_{2}', '', '', dijetlabX, dijetlabY  ],
			[ 'subjet112vs212MassRatio', 'm_{1}/m_{12}', 'm_{2}/m_{12}', '', '', subjet112vs212labX, subjet112vs212labY  ],
			[ 'subjetPolAngle13412vs31234', 'cos #psi_{1(34)}^{[12]}', 'cos #psi_{3(12)}^{[34]}', '', '', '', ''  ],
			[ 'dalitz1234', '', '', '', '', dijetlabX, dijetlabY  ],
			[ 'dalitz3412', '', '', '', '', dijetlabX, dijetlabY  ],
			]
		for i in MCPlots_2D: 
			plot2D( inputFileMCSignal, 'RPVSt100to'+jj, '', i[0], i[1], i[2], i[3], i[4], i[5], i[6], PU )

	elif 'diffSample' in process:

		diffPlots = [
			[ 'jetPt', '', '', '', True],
			[ 'jetPt', '', '', '', False],
			[ 'jetEta', '', '', '', True],
			[ 'jetEta', '', '', '', False],
			[ 'jetMass', '', '', '', True],
			[ 'jetMass', '', '', '', False],
			[ 'HT', '', '', '', True],
			[ 'HT', '', '', '', False],
			[ 'massAve_cutHT', '', '', '', True],
			[ 'massAve_cutHT', '', '', '', False],
			[ 'massAve_cutAsym', '', '', '', True],
			[ 'massAve_cutAsym', '', '', '', False],
			[ 'massAve_cutCosTheta', '', '', '', True],
			[ 'massAve_cutCosTheta', '', '', '', False],
			[ 'massAve_cutSubjetPtRatio', '', '', '', True],
			[ 'massAve_cutSubjetPtRatio', '', '', '', False],
			[ 'massAve_cutTau31', '', '', '', True],
			[ 'massAve_cutTau31', '', '', '', False],
			[ 'subjetPtRatio_cutHT', '', '', '', True],
			[ 'subjetPtRatio_cutHT', '', '', '', False],
			[ 'massAsymmetry_cutHT', '', '', '', True],
			[ 'massAsymmetry_cutHT', '', '', '', False],
			[ 'cosThetaStar_cutHT', '', '', '', True],
			[ 'cosThetaStar_cutHT', '', '', '', False],
			]

		inputFileSample1 = TFile.Open('Rootfiles/RUNAnalysis_RPVSt100to'+jj+'_PU40bx50_CSA14.root')
		inputFileSample2 = TFile.Open('Rootfiles/RUNAnalysis_RPVSt100to'+jj+'_PU20bx25.root')
		inputFileSample3 = TFile.Open('Rootfiles/RUNAnalysis_RPVSt100to'+jj+'_PU40bx50.root')

		for i in diffPlots: 
			'''
			plotDiffSample( inputFileSample2, inputFileSample1, 'PU20bx25', 'PU40bx50', '', i[0], i[1], i[2], i[3], i[4], 'PU'  )
			plotDiffSample( inputFileSample2, inputFileSample1, 'PU20bx25', 'PU40bx50', 'Trimmed', i[0], i[1], i[2], i[3], i[4], 'PU' )
			plotDiffSample( inputFileSample2, inputFileSample1, 'PU20bx25', 'PU40bx50', 'Pruned', i[0], i[1], i[2], i[3], i[4], 'PU' )
			plotDiffSample( inputFileSample2, inputFileSample1, 'PU20bx25', 'PU40bx50', 'Filtered', i[0], i[1], i[2], i[3], i[4], 'PU' )
			plotDiffSample( inputFileSample2, inputFileSample1, 'PU20bx25', 'PU40bx50', '', i[0], i[1], i[2], i[3], i[4], 'PU', True  )
			plotDiffSample( inputFileSample2, inputFileSample1, 'PU20bx25', 'PU40bx50', 'Trimmed', i[0], i[1], i[2], i[3], i[4], 'PU', True )
			plotDiffSample( inputFileSample2, inputFileSample1, 'PU20bx25', 'PU40bx50', 'Pruned', i[0], i[1], i[2], i[3], i[4], 'PU', True )
			plotDiffSample( inputFileSample2, inputFileSample1, 'PU20bx25', 'PU40bx50', 'Filtered', i[0], i[1], i[2], i[3], i[4], 'PU', True )
			'''

			plotDiffSample( inputFileSample3, inputFileSample1, 'PHYS14', 'CSA14', '', i[0], i[1], i[2], i[3], i[4], 'SIM'  )
			plotDiffSample( inputFileSample3, inputFileSample1, 'PHYS14', 'CSA14', 'Trimmed', i[0], i[1], i[2], i[3], i[4], 'SIM' )
			plotDiffSample( inputFileSample3, inputFileSample1, 'PHYS14', 'CSA14', 'Pruned', i[0], i[1], i[2], i[3], i[4], 'SIM' )
			plotDiffSample( inputFileSample3, inputFileSample1, 'PHYS14', 'CSA14', 'Filtered', i[0], i[1], i[2], i[3], i[4], 'SIM' )
			plotDiffSample( inputFileSample3, inputFileSample1, 'PHYS14', 'CSA14', '', i[0], i[1], i[2], i[3], i[4], 'SIM', True  )
			plotDiffSample( inputFileSample3, inputFileSample1, 'PHYS14', 'CSA14', 'Trimmed', i[0], i[1], i[2], i[3], i[4], 'SIM', True )
			plotDiffSample( inputFileSample3, inputFileSample1, 'PHYS14', 'CSA14', 'Pruned', i[0], i[1], i[2], i[3], i[4], 'SIM', True )
			plotDiffSample( inputFileSample3, inputFileSample1, 'PHYS14', 'CSA14', 'Filtered', i[0], i[1], i[2], i[3], i[4], 'SIM', True )

	elif 'diffPU' in process:

		diffPUPlots = [
			[ 'massAve_cutHT', '', '', '', True],
			[ 'massAve_cutHT', '', '', '', False],
			[ 'massAve_cutAsym', '', '', '', True],
			[ 'massAve_cutAsym', '', '', '', False],
			[ 'massAve_cutCosTheta', '', '', '', True],
			[ 'massAve_cutCosTheta', '', '', '', False],
			[ 'massAve_cutSubjetPtRatio', '', '', '', True],
			[ 'massAve_cutSubjetPtRatio', '', '', '', False],
			]

		for i in diffPUPlots: 

			plotDiffPU( inputFileSample, '', i[0], i[1], i[2], i[3], i[4], 'PU'  )
			plotDiffPU( inputFileSample, 'Trimmed', i[0], i[1], i[2], i[3], i[4], 'PU' )
			plotDiffPU( inputFileSample, 'Pruned', i[0], i[1], i[2], i[3], i[4], 'PU' )
			plotDiffPU( inputFileSample, 'Filtered', i[0], i[1], i[2], i[3], i[4], 'PU' )

	elif 'NPV' in process:
		Plots = [
			[ 'NPV', '', '', '', False],
			#[ '', '', '', '', True],
			#[ '', '', '', '', False],
			]
		for i in Plots: 
			plotSimple( inputFileSample, 'RPVSt100tojj', i[0], i[1], i[2], i[3], i[4], PU, True )
