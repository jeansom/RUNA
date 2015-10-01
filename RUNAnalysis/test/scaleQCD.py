#!/usr/bin/env python
'''
File: scaleQCD.py
Author: Alejandro Gomez Espinosa
Email: gomez@physics.rutgers.edu
Description: simple script to scale QCD Files
'''

from ROOT import TFile, TH1, TH2, TMath, gROOT, gPad, TTree
import sys, os
from RUNA.RUNAnalysis.scaleFactors import scaleFactor
#from ROOT import *

gROOT.Reset()
gROOT.SetBatch()


listDir = []

def scaleQCD( inFileName, lumi ):
	"""docstring for scaleQCD"""

	if os.path.exists(inFileName+'_Scaled.root'): 
		os.remove(inFileName+'_Scaled.root')
		outfile = TFile( inFileName+'_Scaled.root', "RECREATE")
	else: outfile = TFile( inFileName+'_Scaled.root', "RECREATE")
	
	infile = TFile( inFileName+'.root', "READ")

	scale = lumi * scaleFactor(inFileName)

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
				#hOut.Scale( scale )
				if not isinstance(h,TTree): hOut.Scale( scale )
				hOut.Write()
			except AttributeError:
				pass
		outfile.cd('/')
	
	outfile.Write()
	outfile.Close()
	infile.Close()

if __name__ == '__main__':


	ptBins = [
			'170to300',
			'300to470',
			'470to600',
			'600to800',
			'800to1000',
			'1000to1400',
			'1400to1800',
			'1800to2400',
			'2400to3200',
			'3200toInf'
			]

	for pt in ptBins:
		print pt
		scaleQCD( 'RUNAnalysis_QCD_Pt_'+pt+'_RunIISpring15DR74_Asympt50ns_v06_v00p2' )
