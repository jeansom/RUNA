#! /usr/bin/env python

#CONFIGURATION

from optparse import OptionParser
parser = OptionParser()

parser.add_option('--files', type='string', action='store',
                  dest='files',
                  help='Input files')

parser.add_option('--outname', type='string', action='store',
                  default='outplots.root',
                  dest='outname',
                  help='Name of output file')

parser.add_option('--verbose', action='store_true',
                  default=False,
                  dest='verbose',
                  help='Print debugging info')

parser.add_option('--maxevents', type='int', action='store',
                  default=1000,
                  dest='maxevents',
                  help='Number of events to run. -1 is all events')




(options, args) = parser.parse_args()
argv = []


#FWLITE STUFF

import ROOT
import sys, os
from DataFormats.FWLite import Events, Handle
ROOT.gROOT.Macro("~/rootlogon.C")
import copy
import random



#AK8 Jets label and Handles
### MiniAOD
#h_jetsAK8 = Handle("vector<pat::Jet>")
#l_jetsAK8 = ("slimmedJetsAK8" ) 
### AOD
#h_jetsAK8 = Handle("vector<reco::PFJet>")
#l_jetsAK8 = ("ak8PFJetsCHS" ) 
## RAW
h_jetsAK8 = Handle("vector<reco::GenJet>")
l_jetsAK8 = ("ak8GenJets" ) 
h_jetsAK4 = Handle("vector<reco::GenJet>")
l_jetsAK4 = ("ak4GenJets" ) 
#



#HISTOGRAMS

f = ROOT.TFile(options.outname, "RECREATE")
f.cd()


h_ptAK8 = ROOT.TH1F("h_ptAK8", "AK8 Jet p_{T};p_{T} (GeV)", 300, 0, 3000)
h_HTAK8 = ROOT.TH1F("h_HTAK8", "AK8 HT;HT (GeV)", 300, 0, 3000)
h_etaAK8 = ROOT.TH1F("h_etaAK8", "AK8 Jet #eta;#eta", 120, -6, 6)
h_phiAK8 = ROOT.TH1F("h_phiAK8", "AK8 Jet #phi;#phi (radians)",100,-3.14, 3.14)
h_mAK8 = ROOT.TH1F("h_mAK8", "AK8 Jet Mass;Mass (GeV)", 100, 0, 1000)
h_numJetsAK8 = ROOT.TH1F("h_numJetsAK8", "AK8 number of Jets; Number of Jets", 20, 0, 20)
h_HTAK8_cutPt = ROOT.TH1F("h_HTAK8_cutPt", "AK8_cutPt HT;HT (GeV)", 300, 0, 3000)
h_numJetsAK8_cutPt = ROOT.TH1F("h_numJetsAK8_cutPt", "AK8_cutPt number of Jets; Number of Jets", 20, 0, 20)
h_HTAK8_wocutPt = ROOT.TH2F("h_HTAK8_wocutPt", "AK8_wocutPt HT;HT (GeV)", 300, 0, 3000, 300, 0, 3000)

h_ptAK4 = ROOT.TH1F("h_ptAK4", "AK4 Jet p_{T};p_{T} (GeV)", 300, 0, 3000)
h_HTAK4 = ROOT.TH1F("h_HTAK4", "AK4 HT;HT (GeV)", 300, 0, 3000)
h_etaAK4 = ROOT.TH1F("h_etaAK4", "AK4 Jet #eta;#eta", 120, -6, 6)
h_phiAK4 = ROOT.TH1F("h_phiAK4", "AK4 Jet #phi;#phi (radians)",100,-3.14, 3.14)
h_mAK4 = ROOT.TH1F("h_mAK4", "AK4 Jet Mass;Mass (GeV)", 100, 0, 1000)
h_numJetsAK4 = ROOT.TH1F("h_numJetsAK4", "AK4 number of Jets; Number of Jets", 20, 0, 20)
h_HTAK4_cutPt = ROOT.TH1F("h_HTAK4_cutPt", "AK4_cutPt HT;HT (GeV)", 300, 0, 3000)
h_numJetsAK4_cutPt = ROOT.TH1F("h_numJetsAK4_cutPt", "AK4_cutPt number of Jets; Number of Jets", 20, 0, 20)
h_HTAK4_wocutPt = ROOT.TH2F("h_HTAK4_wocutPt", "AK4_wocutPt HT;HT (GeV)", 300, 0, 3000, 300, 0, 3000)


#EVENT LOOP

nevents = 0
filesModule = __import__( options.files  )#'RPVSt100tojj_13TeV_RunIISpring15DR74_MiniAOD_cfi')
filesraw = filesModule.readFiles  #[ options.files ]
#filesModule = __import__( 'RPVSt200tojj_13TeV_RunIISpring15DR74_RAW_cfi')
##filesraw = [ options.files ]
files = []
for ifile in filesraw :
    if len( ifile ) > 2 : 
        s = 'root://cmsxrootd.fnal.gov/' + ifile.rstrip()
#        #s = ifile.rstrip()
        files.append( s )
        print 'Added ' + s

#inputDir = '/cms/gomez/EOS/RPVSt100tojj_13TeV_pythia8/GENSIM_RunIISpring15DR74_v2/150713_202010/*/'
#files = os.popen('ls -1 '+inputDir+'*.root').read().splitlines()


# loop over files
for ifile in files :
    print 'Processing file ' + ifile
    events = Events (ifile)
    if options.maxevents > 0 and nevents > options.maxevents :
        break

    # loop over events in this file
    i = 0
    for event in events:
        if options.maxevents > 0 and nevents > options.maxevents :
            break
        i += 1
        nevents += 1

        if nevents % 1000 == 0 : 
            print '    ---> Event ' + str(nevents)
        if options.verbose :
            print '==============================================='
            print '    ---> Event ' + str(nevents)



        ############################################
        # Get the AK8 jets
        ############################################

        event.getByLabel ( l_jetsAK8, h_jetsAK8 )
        jetsAK8 = h_jetsAK8.product()
        event.getByLabel ( l_jetsAK4, h_jetsAK4 )
        jetsAK4 = h_jetsAK4.product()

 	AK8HT = 0	
 	AK8HT_cutPt = 0	
	numJetsAK8 = 0
	numJetsAK8_cutPt = 0
        for jetAK8 in jetsAK8: 
		numJetsAK8 += 1
		AK8HT+= jetAK8.pt()
		h_ptAK8.Fill( jetAK8.pt() )
		h_etaAK8.Fill( jetAK8.eta() )
		h_phiAK8.Fill( jetAK8.phi() )
		h_mAK8.Fill( jetAK8.mass() )
		if( ( jetAK8.pt()> 150 ) and ( abs( jetAK8.eta() ) < 2.5 ) ):
			AK8HT_cutPt += jetAK8.pt()
			numJetsAK8_cutPt += 1

	if( AK8HT > 0 ): h_HTAK8.Fill( AK8HT )
	if( AK8HT_cutPt > 0 ): 
		h_HTAK8_cutPt.Fill( AK8HT_cutPt )
		h_numJetsAK8_cutPt.Fill( numJetsAK8_cutPt )
	if ( ( AK8HT > 0 ) and ( AK8HT_cutPt > 0 ) ): h_HTAK8_wocutPt.Fill( AK8HT, AK8HT_cutPt )
	h_numJetsAK8.Fill( numJetsAK8 )

 	AK4HT = 0	
 	AK4HT_cutPt = 0	
	numJetsAK4 = 0
	numJetsAK4_cutPt = 0
        for jetAK4 in jetsAK4: 
		numJetsAK4+=1
		AK4HT+= jetAK4.pt()
		h_ptAK4.Fill( jetAK4.pt() )
		h_etaAK4.Fill( jetAK4.eta() )
		h_phiAK4.Fill( jetAK4.phi() )
		h_mAK4.Fill( jetAK4.mass() )
		if( ( jetAK4.pt()> 50 ) and ( abs( jetAK4.eta() ) < 2.5 ) ):
			AK4HT_cutPt += jetAK4.pt()
			numJetsAK4_cutPt += 1

	if( AK4HT > 0 ): h_HTAK4.Fill( AK4HT )
	if( AK4HT_cutPt > 0 ): 
		h_HTAK4_cutPt.Fill( AK4HT_cutPt )
		h_numJetsAK4_cutPt.Fill( numJetsAK4_cutPt )
	if ( ( AK4HT > 0 ) and ( AK4HT_cutPt > 0 ) ): h_HTAK4_wocutPt.Fill( AK4HT, AK4HT_cutPt )
	h_numJetsAK4.Fill( numJetsAK4 )

f.cd()
f.Write()
f.Close()


