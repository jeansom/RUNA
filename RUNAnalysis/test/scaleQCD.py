#!/usr/bin/env python
'''
File: scaleQCD.py
Author: Alejandro Gomez Espinosa
Email: gomez@physics.rutgers.edu
Description: simple script to scale QCD Files
'''

from ROOT import TFile, TH1, TH2, TMath, gROOT, gPad, TTree
import sys, os
from scaleFactors import scaleFactor
#from ROOT import *

gROOT.Reset()
gROOT.SetBatch()


listDir = []

def scaleQCD( inFileName ):
	"""docstring for scaleQCD"""

	if os.path.exists(inFileName+'_Scaled.root'): 
		os.remove(inFileName+'_Scaled.root')
		outfile = TFile( inFileName+'_Scaled.root', "RECREATE")
	else: outfile = TFile( inFileName+'_Scaled.root', "RECREATE")
	
	infile = TFile( inFileName+'.root', "READ")

	scale = 1000* scaleFactor(inFileName)

	listDir = []
	for k in infile.GetListOfKeys(): 
		name = k.GetName()
		listDir.append( name )
	for j in listDir:
		outfile.mkdir(j)
		outfile.cd(j)
		dir = infile.GetDirectory(j)
		for q in dir.GetListOfKeys():
			name = q.GetName()
			h = infile.Get( j+'/'+name)
			try:
				hOut = h.Clone()
				hOut.Scale( scale )
				#if not isinstance(h,TH2): hOut.Scale( scale )
				hOut.Write()
			except AttributeError:
				pass
		outfile.cd('/')
	
	outfile.Write()
	outfile.Close()
	infile.Close()

if __name__ == '__main__':

	'''
	scaleQCD( 'RUNAnalysis_QCD_HT-500To1000_PHYS14_PU20bx25_v03_v06' )
	scaleQCD( 'RUNAnalysis_QCD_HT_1000ToInf_PHYS14_PU20bx25_v03_v06' )
	'''

	ptBins = [
			'170to300',
			'300to470',
			'470to600',
			'600to800',
			'800to1000',
			'1000to1400',
			'1400to1800'
			]

	for pt in ptBins:
		print pt
		#scaleQCD( 'RUNAnalysis_QCD_Pt-'+pt+'_CSA14_PU40bx50_v03_v06' )
		scaleQCD( 'RUNAnalysis_QCD_Pt-'+pt+'_PHYS14_PU20bx25_v03_v07' )
		scaleQCD( 'RUNAnalysis_QCD_Pt-'+pt+'_PHYS14_PU30BX50_v03_v07' )
	scaleQCD( 'RUNAnalysis_RPVSt100tojj_PHYS14_PU20bx25_v03_v07' )
	scaleQCD( 'RUNAnalysis_RPVSt100tojj_PHYS14_PU30BX50_v03_v07' )
	scaleQCD( 'RUNAnalysis_RPVSt350tojj_PHYS14_PU20bx25_v03_v07' )
