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


def plotTriggerEfficiency( inFileSample, sample, triggerDenom, triggerPass, name, cut, xmin, xmax, rebin, labX, labY, log ):
	"""docstring for plot"""

	outputFileName = name+'_'+cut+'_'+triggerDenom+"_"+triggerPass+'_'+sample+'_TriggerEfficiency.pdf' 
	print 'Processing.......', outputFileName

	#DenomOnly = inFileSample.Get( 'TriggerEfficiency'+triggerDenom+triggerPass.replace('AK8PFHT700TrimMass50','')+'/'+name+'Denom_'+cut )
	DenomOnly = inFileSample.Get( 'TriggerEfficiency'+triggerPass.replace('AK8PFHT700TrimMass50','')+'/'+name+'Denom_'+cut )
	DenomOnly.Rebin(rebin)
	Denom = DenomOnly.Clone()
	#PassingOnly = inFileSample.Get( 'TriggerEfficiency'+triggerDenom+triggerPass.replace('AK8PFHT700TrimMass50','')+'/'+name+'Passing_'+cut )
	PassingOnly = inFileSample.Get( 'TriggerEfficiency'+triggerPass.replace('AK8PFHT700TrimMass50','')+'/'+name+'Passing_'+cut )
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
		if not (labX and labY): labels( 'trigger', PU, camp)
		else: labels( 'trigger', PU, camp, labX, labY ) #, sel1='AK8PFHT700TrimMass50' )
	else:
		if not (labX and labY): labels( 'trigger', PU, camp,   )
		else: labels( 'trigger', PU, camp, labX, labY )

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
	Efficiency.SetMaximum(1.15)
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
	if 'JetHT' in sample:
		if not (labX and labY): labels( 'triggerDATA', '', PU, camp,  )
		else: labels( 'triggerDATA', '', PU, camp, labX, labY-0.05 ) #, sel1= [ 'AK8PFHT700TrimMass50' ] )
	else:
		if not (labX and labY): labels( 'triggerSignal', '', PU, camp  )
		else: labels( 'triggerSignal', '', PU, camp, labX, labY)

	can1.SaveAs( 'Plots/'+outputFileName.replace('.pdf','Merged.pdf') )
	#can1.SaveAs( 'Plots/'+outputFileName.replace('.pdf','Merged.gif') )
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


	can = TCanvas('c1', 'c1',  10, 10, 750, 500 )
	gStyle.SetPaintTextFormat("4.2f")
	Efficiency.Draw('colz')
	Efficiency.Draw('same text')
	Efficiency.GetYaxis().SetTitleOffset(1.0)
	Efficiency.SetMarkerSize(2)
	Efficiency.GetXaxis().SetRange( int(Xmin/(10.*rebinx)), int(Xmax/(10.*rebinx)) )
	#Efficiency.GetXaxis().SetTitle( 'Leading Trimmed Jet Mass [GeV]' )
	Efficiency.GetYaxis().SetTitle( 'H_{T} [GeV]' )
	Efficiency.GetYaxis().SetRange( int(Ymin/(10.*rebiny)), int(Ymax/(10.*rebiny)) )

	CMS_lumi.relPosX = 0.13
	CMS_lumi.CMS_lumi(can, 4, 0)
	#if 'JetHT' in sample:
	if 'Dijet' in cut: sel = 'jet Pt > 150 GeV, jet |#eta| < 2.4, numJets > 1'
	else: sel =''
	if not (labX and labY): labels( 'triggerDATA', sel, PU, camp,  )
	else: labels( 'triggerDATA', sel, PU, camp, labX, labY ) #, sel1= [ 'AK8PFHT700TrimMass50' ] )
	#else:
	#	if not (labX and labY): labels( 'triggerSignal', PU, camp  )
	#	else: labels( 'triggerSignal', PU, camp, labX, labY)

	can.SaveAs( 'Plots/'+outputFileName )
	#can.SaveAs( 'Plots/'+outputFileName.replace('pdf', 'gif')  )
	del can




if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--proc', action='store', default='trigger', help='Process to draw, example: 1D, 2D, MC.' )
	parser.add_argument('-d', '--decay', action='store', default='jj', help='Decay, example: jj, bj.' )
	parser.add_argument('-b', '--boosted', action='store', default='Boosted', help='Boosted or non boosted, example: Boosted' )
	parser.add_argument('-g', '--grom', action='store', default='Pruned', help='Grooming Algorithm, example: Pruned, Filtered.' )
	parser.add_argument('-m', '--mass', action='store', default='100', help='Mass of Stop, example: 100' )
	parser.add_argument('-C', '--cut', action='store', default='_cutDEta', help='cut, example: cutDEta' )
	parser.add_argument('-pu', '--PU', action='store', default='Asympt25ns', help='PU, example: PU40bx25.' )
	parser.add_argument('-s', '--single', action='store', default='all', help='single histogram, example: massAve_cutDijet.' )
	parser.add_argument('-q', '--QCD', action='store', default='Pt', help='Type of QCD binning, example: HT.' )
	parser.add_argument('-c', '--campaign', action='store', default='RunIISpring15DR74', help='Campaign, example: PHYS14.' )
	parser.add_argument('-l', '--lumi', action='store', default='15.5', help='Luminosity, example: 1.' )
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
	cut = args.cut
	grom = args.grom
	single = args.single
	boosted = args.boosted
	triggerUsed = args.trigger
	
	bkgFiles = {}
	signalFiles = {}
	#if 'DATA' in process: 
	CMS_lumi.extraText = "Preliminary"
	#else:
	#	CMS_lumi.lumi_13TeV = lumi+" fb^{-1}"
	#	CMS_lumi.extraText = "Preliminary Simulation"

	#if 'DATA' in process: 
	if '50ns' in PU:
		CMS_lumi.lumi_13TeV = "71.52 pb^{-1}"
		if 'MET' in process:
			inputTrigger = TFile.Open('Rootfiles/RUNTriggerEfficiency_MET_Asympt50ns_v01p2_ts_v10.root')
			SAMPLE = 'MET'
			BASEDTrigger = 'PFMET170'
		else:
			inputTrigger = TFile.Open('Rootfiles/RUNTriggerEfficiency_JetHT_Run2015C-PromptReco-v1.root')
			SAMPLE = 'JetHT'
			BASEDTrigger = 'PFHT475'
	else:
		#CMS_lumi.lumi_13TeV = "166.37 pb^{-1}"
		CMS_lumi.lumi_13TeV = "15.4 pb^{-1}"
		if 'MET' in process:
			inputTrigger = TFile.Open('Rootfiles/RUNTriggerEfficiency_MET_Run2015C-PromptReco-v1.root')
			SAMPLE = 'MET'
			BASEDTrigger = 'PFMET170'
		else:
			inputTrigger = TFile.Open('Rootfiles/RUNTriggerEfficiency_JetHT_Run2015C-PromptReco-v1.root')
			SAMPLE = 'JetHT'
			BASEDTrigger = 'PFHT475'

	dijetlabX = 0.15
	dijetlabY = 0.88
	triggerlabX = 0.88
	triggerlabY = 0.90  #0.50
	subjet112vs212labX = 0.7
	subjet112vs212labY = 0.88
	jetMassHTlabX = 0.87
	jetMassHTlabY = 0.20

	massMinX = 0
	massMaxX = 3*(int(mass))
	polAngXmin = 0.7
	polAngXmax = 1.0
	HTMinX = 300
	HTMaxX = 1500
	ptMinX = 100
	ptMaxX = 800


	plotList = [ 

		[ 'trigger', 'jetTrimmedMass', 'cutHT', 0, massMaxX, 1, triggerlabX, triggerlabY, True],
		[ 'trigger', 'jet1Mass', 'cutHT', 0, massMaxX, 1, triggerlabX, triggerlabY, True],
		[ 'trigger', 'jetLeadMass', 'cutHT', 0, massMaxX, 1, triggerlabX, triggerlabY, True],
		[ 'trigger', 'jetLeadMass', 'cutDijet', 0, massMaxX, 1, triggerlabX, triggerlabY, True],
		[ 'trigger', 'massAve', 'cutDijet', 0, massMaxX, 2, triggerlabX, triggerlabY, True],
		[ 'trigger', 'massAve', 'cutMassAsym', 0, massMaxX, 2, triggerlabX, triggerlabY, False],
		[ 'trigger', 'HT', 'cutDijet', HTMinX, HTMaxX, 5, triggerlabX, triggerlabY, True],
		[ 'trigger', 'HT', 'cutMassAsym', HTMinX, HTMaxX, 5, triggerlabX, triggerlabY, True],
		[ 'trigger', 'HT', 'cutJetMass', HTMinX, HTMaxX, 5, triggerlabX, triggerlabY, True],
		[ 'trigger', 'jet1Mass', 'cutDijet', 0, massMaxX, 2, triggerlabX, triggerlabY, True],
		[ 'trigger', 'jet1Mass', 'cutMassAsym', 0, massMaxX, 2, triggerlabX, triggerlabY, True],
		[ 'trigger', 'jet1Pt', 'cutDijet', ptMinX, ptMaxX, 2, triggerlabX, triggerlabY, True],
		[ 'trigger', 'jet1Pt', 'cutMassAsym', ptMinX, ptMaxX, 2, triggerlabX, triggerlabY, True],
		[ 'trigger', 'trimmedMass', 'cutDijet', massMinX, massMaxX, 2, triggerlabX, triggerlabY, True],
		[ 'trigger', 'trimmedMass', 'cutMassAsym', massMinX, massMaxX, 2, triggerlabX, triggerlabY, True],
		[ 'trigger', 'ak4HT', 'cutDijet', HTMinX, HTMaxX, 5, triggerlabX, triggerlabY, True],
		[ 'trigger', 'ak4HT', 'cutMassAsym', HTMinX, HTMaxX, 5, triggerlabX, triggerlabY, True],

		#[ '2D', 'jetMassHTDenom_noTrigger', 'Leading Trimmed Jet Mass [GeV]', 'H_{T} [GeV]', 0, 200, 2, 100, HTMaxX, 5, 0.85, 0.2],
		#[ '2D', 'jetTrimmedMassHTDenom_noTrigger', 'Leading Trimmed Jet Mass [GeV]', 'H_{T} [GeV]', 0, 200, 2, 100, HTMaxX, 5, 0.85, 0.2],
		#[ '2D', 'jetMassHTDenom_triggerOne', 'Leading Trimmed Jet Mass [GeV]', 'H_{T} [GeV]', 0, 200, 2, 100, HTMaxX, 5, 0.85, 0.2],
		#[ '2D', 'jetMassHTDenom_triggerTwo', 'Leading Trimmed Jet Mass [GeV]', 'H_{T} [GeV]', 0, 200, 2, 100, HTMaxX, 5, 0.85, 0.2],
		#[ '2D', 'jetMassHTDenom_triggerOneAndTwo', 'Leading Trimmed Jet Mass [GeV]', 'H_{T} [GeV]', 0, 200, 2, 100, HTMaxX, 5, 0.85, 0.25],
		[ '2dtrig', 'jetMassHT', 'cutDijet', 20, 200, 2, HTMinX, 1200, 10, jetMassHTlabX, jetMassHTlabY],
		[ '2dtrig', 'jetMassHT', 'cutMassAsym', 20, 200, 2, HTMinX, 1200, 10, jetMassHTlabX, jetMassHTlabY],
		[ '2dtrig', 'jetTrimmedMassHT', 'cutDijet', 20, 200, 2, HTMinX, 1200, 10, jetMassHTlabX, jetMassHTlabY],
		[ '2dtrig', 'jetTrimmedMassHT', 'cutMassAsym', 20, 200, 2, HTMinX, 1200, 10, jetMassHTlabX, jetMassHTlabY],
		[ '2dtrig', 'massAveHT', 'cutDijet', 20, 200, 2, HTMinX, 1200, 10, jetMassHTlabX, jetMassHTlabY],
		[ '2dtrig', 'massAveHT', 'cutMassAsym', 20, 200, 2, HTMinX, 1200, 10, jetMassHTlabX, jetMassHTlabY],
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
			if 'trigger' in process:
				for trig in Triggers:
					#tmpplotTriggerEfficiency( inputTrigger, SAMPLE, 'PFHT475', trig, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7] )
					plotTriggerEfficiency( inputTrigger, SAMPLE, 'PFHT475', trig, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7] )
					#plotTriggerEfficiency( inputTrigger, SAMPLE, 'PFMET170', trig, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7] )
					#plotTriggerEfficiency( inputTrigger, SAMPLE, 'IsoMu17', trig, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7] )
			elif '2dtrig' in process:
				for trig in Triggers:
					plot2DTriggerEfficiency( inputTrigger, SAMPLE, BASEDTrigger, trig, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9] )



