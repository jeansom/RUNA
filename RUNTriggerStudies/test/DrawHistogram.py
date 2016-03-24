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
from RUNA.RUNAnalysis.histoLabels import labels, labelAxis 
import RUNA.RUNAnalysis.CMS_lumi as CMS_lumi 
import RUNA.RUNAnalysis.tdrstyle as tdrstyle


gROOT.Reset()
gROOT.SetBatch()
#setTDRStyle()
#gROOT.SetStyle('tdrStyle')
#set the tdr style
gROOT.ForceStyle()
tdrstyle.setTDRStyle()
#CMS_lumi.writeExtraText = 1
#CMS_lumi.extraText = ""

gStyle.SetOptStat(0)


def plotTriggerEfficiency( inFileSample, sample, triggerDenom, triggerPass, name, cut, xmin, xmax, rebin, labX, labY, log, version, PU ):
	"""docstring for plot"""

	outputFileName = name+'_'+cut+'_'+triggerDenom+"_"+triggerPass+'_'+sample+'_'+version+'_TriggerEfficiency.'+ext
	print 'Processing.......', outputFileName

	DenomOnly = inFileSample.Get( version+'TriggerEfficiency'+triggerPass.replace(tmpTrig,'')+'/'+name+'Denom_'+cut )
	DenomOnly.Rebin(rebin)
	Denom = DenomOnly.Clone()
	PassingOnly = inFileSample.Get( version+'TriggerEfficiency'+triggerPass.replace(tmpTrig,'')+'/'+name+'Passing_'+cut )
	PassingOnly.Rebin(rebin)
	Passing = PassingOnly.Clone()
	Efficiency = TGraphAsymmErrors( Passing, Denom, 'cp'  )

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
	pad2 = TPad("pad2", "Efficiency",0,0.00,1.00,0.531,-1);
	pad1.Draw()
	pad2.Draw()

	pad1.cd()
	if log: pad1.SetLogy()

	legend.AddEntry( DenomOnly, triggerDenom+' (baseline trigger)', 'l' )
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
	legend.Draw()

	pad2.cd()
	pad2.SetTopMargin(0)
	pad2.SetBottomMargin(0.3)
	Efficiency.SetMarkerStyle(8)
	Efficiency.SetLineWidth(2)
	Efficiency.SetLineColor(kBlue-4)
	#Efficiency.SetFillStyle(1001)
	Efficiency.GetYaxis().SetTitle("Efficiency")
	Efficiency.GetYaxis().SetLabelSize(0.06)
	Efficiency.GetXaxis().SetLabelSize(0.06)
	Efficiency.GetYaxis().SetTitleSize(0.06)
	Efficiency.GetYaxis().SetTitleOffset(0.8)
	Efficiency.SetMinimum(-0.1)
	Efficiency.SetMaximum(1.1)
	Efficiency.GetXaxis().SetLimits( xmin, xmax )
	labelAxis( name, Efficiency, 'Pruned')
	Efficiency.Draw()
	if not (labX and labY): labels( '', '', '')
	else: labels( '', '', '', labX, labY, 'left' ) #, sel1='AK8PFHT700TrimMass50' )

	can.SaveAs( 'Plots/'+outputFileName.replace('.','Extended.') )
	del can

	can1 = TCanvas('c1', 'c1',  10, 10, 750, 500 )
	Efficiency.SetMarkerStyle(8)
	Efficiency.SetMinimum(-0.15)
	Efficiency.SetMaximum(1.15)
	Efficiency.GetYaxis().SetLabelSize(0.05)
	Efficiency.GetXaxis().SetLabelSize(0.05)
	Efficiency.GetYaxis().SetTitleSize(0.06)
	Efficiency.GetYaxis().SetTitleOffset(0.8)
	Efficiency.GetXaxis().SetTitleOffset(0.8)
	Efficiency.Draw()
	can1.Update()
	
	'''
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
	'''
	labelAxis( name, Efficiency, 'Pruned')
	CMS_lumi.relPosX = 0.11
	CMS_lumi.cmsTextSize = 0.7
	CMS_lumi.extraOverCmsTextSize = 0.6
	CMS_lumi.CMS_lumi(can1, 4, 0)
	#if not (labX and labY): labels( name, '', PU, camp,  )
	#else: labels( name, '', PU, camp, labX, labY-0.05 ) #, sel1= [ 'AK8PFHT700TrimMass50' ] )

	can1.SaveAs( 'Plots/'+outputFileName )
	del can1


def plot2DTriggerEfficiency( inFileSample, sample, triggerDenom, triggerPass, name, cut, xlabel, ylabel, Xmin, Xmax, rebinx, Ymin, Ymax, rebiny, labX, labY, version, PU ):
	"""docstring for plot"""

	outputFileName = name+'_'+cut+'_'+triggerDenom+"_"+triggerPass+'_'+sample+'_'+version+'_TriggerEfficiency.'+ext
	print 'Processing.......', outputFileName

	Denom = inFileSample.Get( version+'TriggerEfficiency'+triggerPass.replace(tmpTrig,'')+'/'+name+'Denom_'+cut )
	Passing = inFileSample.Get( version+'TriggerEfficiency'+triggerPass.replace(tmpTrig,'')+'/'+name+'Passing_'+cut )
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


	can = TCanvas('c1', 'c1',  10, 10, 1000, 750 )
	gStyle.SetPaintTextFormat("4.2f")
	Efficiency.Draw('colz')
	Efficiency.Draw('same text')
	Efficiency.GetYaxis().SetTitleOffset(1.0)
	Efficiency.SetMarkerSize(2)
	Efficiency.GetXaxis().SetRange( int(Xmin/(10.*rebinx)), int(Xmax/(10.*rebinx)) )
	Efficiency.GetXaxis().SetTitle( xlabel )
	Efficiency.GetYaxis().SetTitle( ylabel )
	Efficiency.GetYaxis().SetRange( int(Ymin/(10.*rebiny)), int(Ymax/(10.*rebiny)) )

	CMS_lumi.relPosX = 0.13
	CMS_lumi.CMS_lumi(can, 4, 0)
	#if not (labX and labY): labels( name, '', '', ''  )
	#else: labels( name, '', '', '', labX, labY ) #, sel1= [ 'AK8PFHT700TrimMass50' ] )

	can.SaveAs( 'Plots/'+outputFileName )
	del can




if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--proc', action='store', default='1D', help='Process to draw, example: 1D, 2D, MC.' )
	parser.add_argument('-d', '--decay', action='store', default='jj', help='Decay, example: jj, bj.' )
	parser.add_argument('-v', '--version', action='store', default='Boosted', help='Boosted or non version, example: Boosted' )
	parser.add_argument('-g', '--grom', action='store', default='Pruned', help='Grooming Algorithm, example: Pruned, Filtered.' )
	parser.add_argument('-m', '--mass', action='store', default='100', help='Mass of Stop, example: 100' )
	parser.add_argument('-C', '--cut', action='store', default='_cutDEta', help='cut, example: cutDEta' )
	parser.add_argument('-pu', '--PU', action='store', default='Asympt25ns', help='PU, example: PU40bx25.' )
	parser.add_argument('-s', '--single', action='store', default='all', help='single histogram, example: massAve_cutDijet.' )
	parser.add_argument('-c', '--campaign', action='store', default='RunIISpring15DR74', help='Campaign, example: PHYS14.' )
	parser.add_argument('-l', '--lumi', action='store', default='15.5', help='Luminosity, example: 1.' )
	parser.add_argument('-t', '--trigger', action='store', default='AK8PFHT700TrimMass50', help='Trigger used, example PFHT800.' )
	parser.add_argument('-e', '--extension', action='store', default='png', help='Extension of plots.' )

	try:
		args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)

	process = args.proc
	jj = args.decay
	PU = args.PU
	camp = args.campaign
	lumi = args.lumi
	histo = args.single
	mass = args.mass
	cut = args.cut
	grom = args.grom
	single = args.single
	version = args.version
	triggerUsed = args.trigger
	ext = args.extension
	
	bkgFiles = {}
	signalFiles = {}
	CMS_lumi.extraText = "Preliminary"
	if 'Boosted' in version: tmpTrig = 'AK8PFHT700TrimMass50'
	else: tmpTrig = 'PFHT800'

	CMS_lumi.lumi_13TeV = "2.6 fb^{-1}"
	if 'MET' in process:
		inputTrigger = TFile.Open('Rootfiles/RUNTriggerEfficiency_MET_Run2015C-PromptReco-v1.root')
		SAMPLE = 'MET'
		BASEDTrigger = 'PFMET170'
	else:
		inputTrigger = TFile.Open('Rootfiles/RUNTriggerStudies_JetHT_Run2015D-16Dec2015-v1_v76x_v1p0_v02.root')
		SAMPLE = 'JetHT_Run2015D'
		BASEDTrigger = 'PFHT475'

	triggerlabX = 0.15
	triggerlabY = 1.0
	jetMassHTlabX = 0.87
	jetMassHTlabY = 0.20

	massMinX = 0
	massMaxX = 3*(int(mass))
	HTMinX = 300
	HTMaxX = 1500
	ptMinX = 100
	ptMaxX = 800


	plotList = [ 

		[ '1D', 'HT', HTMinX, HTMaxX, 5, triggerlabX, triggerlabY, True],
		[ '1D', 'prunedMassAve', 0, massMaxX, 2, triggerlabX, triggerlabY, True],
		[ '1D', 'trimmedMass', massMinX, massMaxX, 2, triggerlabX, triggerlabY, True],
		#[ '1D', 'ak4HT', HTMinX, HTMaxX, 5, triggerlabX, triggerlabY, True],
		[ '1D', 'jet1Pt', ptMinX, ptMaxX, 2, triggerlabX, triggerlabY, True],
		[ '1D', 'jet2Pt', ptMinX, ptMaxX, 2, triggerlabX, triggerlabY, True],
		[ '1D', 'jet1PrunedMass', 0, massMaxX, 1, triggerlabX, triggerlabY, True],
		[ '1D', 'jet1SoftDropMass', 0, massMaxX, 1, triggerlabX, triggerlabY, True],
		#[ '1D', 'jet3Pt', 0, 200, 1, triggerlabX, triggerlabY, True],
		#[ '1D', 'jet4Pt', 0, 200, 1, triggerlabX, triggerlabY, True],

		#[ '2D', 'jetMassHTDenom_noTrigger', 'Leading Trimmed Jet Mass [GeV]', 'H_{T} [GeV]', 0, 200, 2, 100, HTMaxX, 5, 0.85, 0.2],
		#[ '2D', 'jetTrimmedMassHTDenom_noTrigger', 'Leading Trimmed Jet Mass [GeV]', 'H_{T} [GeV]', 0, 200, 2, 100, HTMaxX, 5, 0.85, 0.2],
		#[ '2D', 'jetMassHTDenom_triggerOne', 'Leading Trimmed Jet Mass [GeV]', 'H_{T} [GeV]', 0, 200, 2, 100, HTMaxX, 5, 0.85, 0.2],
		#[ '2D', 'jetMassHTDenom_triggerTwo', 'Leading Trimmed Jet Mass [GeV]', 'H_{T} [GeV]', 0, 200, 2, 100, HTMaxX, 5, 0.85, 0.2],
		#[ '2D', 'jetMassHTDenom_triggerOneAndTwo', 'Leading Trimmed Jet Mass [GeV]', 'H_{T} [GeV]', 0, 200, 2, 100, HTMaxX, 5, 0.85, 0.25],
		[ '2D', 'jetTrimmedMassHT', 'Leading Jet Trimmed Mass [GeV]', 'HT [GeV]', 20, 200, 2, HTMinX, 1200, 10, jetMassHTlabX, jetMassHTlabY],
		[ '2D', 'jetPrunedMassHT', 'Leading Jet Pruned Mass [GeV]', 'HT [GeV]', 20, 200, 2, HTMinX, 1200, 10, jetMassHTlabX, jetMassHTlabY],
		[ '2D', 'jetSoftDropMassHT', 'Leading Jet SoftDrop Mass [GeV]', 'HT [GeV]', 20, 200, 2, HTMinX, 1200, 10, jetMassHTlabX, jetMassHTlabY],
		[ '2D', 'jet1PtHT', 'Leading Jet Pt [GeV]', 'HT [GeV]', 150, 700, 5, HTMinX, 1200, 10, jetMassHTlabX, jetMassHTlabY],
		[ '2D', 'jet1PtPrunedMass', 'Leading Jet Pt [GeV]', 'Leading Jet Pruned Mass [GeV]', 150, 700, 5, 20, 200, 2, jetMassHTlabX, jetMassHTlabY],
		[ '2D', 'jet1PtSoftDropMass', 'Leading Jet Pt [GeV]', 'Leading Jet SoftDrop Mass [GeV]', 150, 700, 5, 20, 200, 2, jetMassHTlabX, jetMassHTlabY],
		[ '2D', 'jet2PtHT', '2nd Leading Jet Pt [GeV]', 'HT [GeV]', 150, 700, 5, HTMinX, 1200, 10, jetMassHTlabX, jetMassHTlabY],
		[ '2D', 'jet2PtPrunedMass', '2nd Leading Jet Pt [GeV]', '2nd Leading Jet Pruned Mass [GeV]', 150, 700, 5, 20, 200, 2, jetMassHTlabX, jetMassHTlabY],
		[ '2D', 'jet2PtSoftDropMass', '2nd Leading Jet Pt [GeV]', '2nd Leading Jet SoftDrop Mass [GeV]', 150, 700, 5, 20, 200, 2, jetMassHTlabX, jetMassHTlabY],
		[ '2D', 'prunedMassAveHT', 'Leading Jet Pruned Mass [GeV]', 'HT [GeV]', 20, 200, 2, HTMinX, 1200, 10, jetMassHTlabX, jetMassHTlabY],
		#[ '2D', 'jetMassHT', 20, 200, 2, HTMinX, 1200, 10, jetMassHTlabX, jetMassHTlabY],
		#[ '2D', 'jet4PtHT', 20, 200, 2, HTMinX, 1200, 10, jetMassHTlabX, jetMassHTlabY],
		]

	if 'all' in single: Plots = [ x[1:] for x in plotList if x[0] in process ]
	else: Plots = [ y[1:] for y in plotList if ( ( y[0] in process ) and ( y[1] in single ) )  ]

	if 'all' in grom: Groomers = [ '', 'Trimmed', 'Pruned', 'Filtered' ]
	else: Grommers = [ grom ]


	for i in Plots:
		if '1D' in process:
			plotTriggerEfficiency( inputTrigger, SAMPLE, BASEDTrigger, triggerUsed, i[0], cut, i[1], i[2], i[3], i[4], i[5], i[6], version, PU )
		elif '2D' in process:
			plot2DTriggerEfficiency( inputTrigger, SAMPLE, BASEDTrigger, triggerUsed, i[0], cut, i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], version, PU )



