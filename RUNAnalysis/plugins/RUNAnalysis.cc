// -*- C++ -*-
//
// Package:    Ntuples/Ntuples
// Class:      RUNAnalysis
// 
/**\class RUNAnalysis RUNAnalysis.cc Ntuples/Ntuples/plugins/RUNAnalysis.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  alejandro gomez
//         Created:  Tue, 14 Oct 2014 23:13:13 GMT
//
//


// system include files
#include <memory>
#include <vector>
#include <TLorentzVector.h>
#include <TH2.h>
#include <TTree.h>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/LorentzVector.h"

#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"

#include "RUNA/RUNAnalysis/interface/CommonVariablesStructure.h"
#include "RUNA/RUNAnalysis/interface/PUReweighter.h"

using namespace edm;
using namespace std;

//
// constants, enums and typedefs
//

//
// class declaration
//
class RUNAnalysis : public EDAnalyzer {
   public:
      explicit RUNAnalysis(const ParameterSet&);
      static void fillDescriptions(edm::ConfigurationDescriptions & descriptions);
      ~RUNAnalysis();

   private:
      virtual void beginJob() override;
      virtual void analyze(const Event&, const EventSetup&) override;
      virtual void endJob() override;
      virtual void clearVariables();

      //virtual void beginRun(Run const&, EventSetup const&) override;
      //virtual void endRun(Run const&, EventSetup const&) override;
      //virtual void beginLuminosityBlock(LuminosityBlock const&, EventSetup const&) override;
      //virtual void endLuminosityBlock(LuminosityBlock const&, EventSetup const&) override;

      // ----------member data ---------------------------
      PUReweighter PUWeight_;
      Service<TFileService> fs_;
      TTree *RUNAtree;
      map< string, TH1D* > histos1D_;
      map< string, TH2D* > histos2D_;
      vector< string > cutLabels;
      map< string, double > cutmap;

      bool bjSample;
      bool mkTree;
      bool isData;
      string dataPUFile;
      double scale;
      double cutMassRes;
      double cutDelta;
      double cutEtaBand;
      double cutHT;
      double cutDeltaR;
      double cutCosThetaStar;
      vector<string> triggerPass;

      vector<float> *jetsPt = new std::vector<float>();
      vector<float> *jetsEta = new std::vector<float>();
      vector<float> *jetsPhi = new std::vector<float>();
      vector<float> *jetsE = new std::vector<float>();
      vector<float> *jetsQGL = new std::vector<float>();
      ULong64_t event = 0;
      int numJets = 0, numPV = 0;
      unsigned int lumi = 0, run=0;
      float HT = 0, mass1 = -999, mass2 = -999, avgMass = -999, MET = -999,
	    delta1 = -999, delta2 = -999, massRes = -999, eta1 = -999, eta2 = -999, deltaEta = -999, 
	    deltaR = -999, cosThetaStar1 = -999, cosThetaStar2 = -999,
	    puWeight = -999, lumiWeight = -999 ;

      EDGetTokenT<vector<float>> jetPt_;
      EDGetTokenT<vector<float>> jetEta_;
      EDGetTokenT<vector<float>> jetPhi_;
      EDGetTokenT<vector<float>> jetE_;
      EDGetTokenT<vector<float>> jetQGL_;
      EDGetTokenT<vector<float>> jetMass_;
      EDGetTokenT<vector<float>> jetCSV_;
      EDGetTokenT<vector<float>> jetCSVV1_;
      EDGetTokenT<int> NPV_;
      EDGetTokenT<vector<float>> metPt_;
      EDGetTokenT<int> trueNInt_;
      EDGetTokenT<vector<int>> bunchCross_;
      EDGetTokenT<vector<int>> puNumInt_;
      EDGetTokenT<unsigned int> lumi_;
      EDGetTokenT<unsigned int> run_;
      EDGetTokenT<ULong64_t> event_;

      // Trigger
      EDGetTokenT<vector<float>> triggerBit_;
      EDGetTokenT<vector<string>> triggerName_;
      
      //Jet ID
      EDGetTokenT<vector<float>> jecFactor_;
      EDGetTokenT<vector<float>> neutralHadronEnergy_;
      EDGetTokenT<vector<float>> neutralEmEnergy_;
      EDGetTokenT<vector<float>> chargedHadronEnergy_;
      EDGetTokenT<vector<float>> chargedEmEnergy_;
      EDGetTokenT<vector<float>> chargedHadronMultiplicity_;
      EDGetTokenT<vector<float>> neutralHadronMultiplicity_;
      EDGetTokenT<vector<float>> chargedMultiplicity_;
      EDGetTokenT<vector<float>> muonEnergy_; 


};

//
// static data member definitions
//

//
// constructors and destructor
//
RUNAnalysis::RUNAnalysis(const ParameterSet& iConfig):
//	getterOfProducts_(ProcessMatch(*), this) {
//	triggerBits_(consumes<TriggerResults>(iConfig.getParameter<InputTag>("bits"))),
	jetPt_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetPt"))),
	jetEta_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetEta"))),
	jetPhi_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetPhi"))),
	jetE_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetE"))),
	jetQGL_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetQGL"))),
	jetMass_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetMass"))),
	jetCSV_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetCSV"))),
	jetCSVV1_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetCSVV1"))),
	NPV_(consumes<int>(iConfig.getParameter<InputTag>("NPV"))),
	metPt_(consumes<vector<float>>(iConfig.getParameter<InputTag>("metPt"))),
	trueNInt_(consumes<int>(iConfig.getParameter<InputTag>("trueNInt"))),
	bunchCross_(consumes<vector<int>>(iConfig.getParameter<InputTag>("bunchCross"))),
	puNumInt_(consumes<vector<int>>(iConfig.getParameter<InputTag>("puNumInt"))),
	lumi_(consumes<unsigned int>(iConfig.getParameter<InputTag>("Lumi"))),
	run_(consumes<unsigned int>(iConfig.getParameter<InputTag>("Run"))),
	event_(consumes<ULong64_t>(iConfig.getParameter<InputTag>("Event"))),
	// Trigger
	triggerBit_(consumes<vector<float>>(iConfig.getParameter<InputTag>("triggerBit"))),
	triggerName_(consumes<vector<string>>(iConfig.getParameter<InputTag>("triggerName"))),
	//Jet ID,
	jecFactor_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jecFactor"))),
	neutralHadronEnergy_(consumes<vector<float>>(iConfig.getParameter<InputTag>("neutralHadronEnergy"))),
	neutralEmEnergy_(consumes<vector<float>>(iConfig.getParameter<InputTag>("neutralEmEnergy"))),
	chargedHadronEnergy_(consumes<vector<float>>(iConfig.getParameter<InputTag>("chargedHadronEnergy"))),
	chargedEmEnergy_(consumes<vector<float>>(iConfig.getParameter<InputTag>("chargedEmEnergy"))),
	chargedHadronMultiplicity_(consumes<vector<float>>(iConfig.getParameter<InputTag>("chargedHadronMultiplicity"))),
	neutralHadronMultiplicity_(consumes<vector<float>>(iConfig.getParameter<InputTag>("neutralHadronMultiplicity"))),
	chargedMultiplicity_(consumes<vector<float>>(iConfig.getParameter<InputTag>("chargedMultiplicity"))),
	muonEnergy_(consumes<vector<float>>(iConfig.getParameter<InputTag>("muonEnergy")))
{
	scale 		= iConfig.getParameter<double>("scale");
	bjSample 	= iConfig.getParameter<bool>("bjSample");
	mkTree 		= iConfig.getParameter<bool>("mkTree");
	cutMassRes      = iConfig.getParameter<double>     ("cutMassRes");
	cutDelta        = iConfig.getParameter<double>     ("cutDelta");
	cutEtaBand      = iConfig.getParameter<double>     ("cutEtaBand");
	cutHT 		= iConfig.getParameter<double>("cutHT");
	cutDeltaR 		= iConfig.getParameter<double>("cutDeltaR");
	cutCosThetaStar 		= iConfig.getParameter<double>("cutCosThetaStar");
	triggerPass 	= iConfig.getParameter<vector<string>>("triggerPass");
	isData 		= iConfig.getParameter<bool>("isData");
	dataPUFile 	= iConfig.getParameter<string>("dataPUFile");
}


RUNAnalysis::~RUNAnalysis()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void RUNAnalysis::analyze(const Event& iEvent, const EventSetup& iSetup) {


	/*vector<Handle< vector<float> > > handles;
	getterOfProducts_.fillHandles(event, handles);
	*/

	Handle<vector<float> > jetPt;
	iEvent.getByToken(jetPt_, jetPt);

	Handle<vector<float> > jetEta;
	iEvent.getByToken(jetEta_, jetEta);

	Handle<vector<float> > jetPhi;
	iEvent.getByToken(jetPhi_, jetPhi);

	Handle<vector<float> > jetE;
	iEvent.getByToken(jetE_, jetE);

	Handle<vector<float> > jetQGL;
	iEvent.getByToken(jetQGL_, jetQGL);

	Handle<vector<float> > jetMass;
	iEvent.getByToken(jetMass_, jetMass);

	Handle<vector<float> > jetCSV;
	iEvent.getByToken(jetCSV_, jetCSV);

	Handle<vector<float> > jetCSVV1;
	iEvent.getByToken(jetCSVV1_, jetCSVV1);

	Handle<int> NPV;
	iEvent.getByToken(NPV_, NPV);

	Handle<int> trueNInt;
	iEvent.getByToken(trueNInt_, trueNInt);

	Handle<vector<int>> bunchCross;
	iEvent.getByToken(bunchCross_, bunchCross);

	Handle<vector<int>> puNumInt;
	iEvent.getByToken(puNumInt_, puNumInt);

	Handle<unsigned int> Lumi;
	iEvent.getByToken(lumi_, Lumi);

	Handle<unsigned int> Run;
	iEvent.getByToken(run_, Run);

	Handle<ULong64_t> ievent;
	iEvent.getByToken(event_, ievent);

	Handle<vector<float> > metPt;
	iEvent.getByToken(metPt_, metPt);

	/// Trigger
	Handle<vector<float> > triggerBit;
	iEvent.getByToken(triggerBit_, triggerBit);

	Handle<vector<string> > triggerName;
	iEvent.getByToken(triggerName_, triggerName);

	/// Jet ID
	Handle<vector<float> > jecFactor;
	iEvent.getByToken(jecFactor_, jecFactor);

	Handle<vector<float> > neutralHadronEnergy;
	iEvent.getByToken(neutralHadronEnergy_, neutralHadronEnergy);

	Handle<vector<float> > neutralEmEnergy;
	iEvent.getByToken(neutralEmEnergy_, neutralEmEnergy);

	Handle<vector<float> > chargedHadronEnergy;
	iEvent.getByToken(chargedHadronEnergy_, chargedHadronEnergy);

	Handle<vector<float> > chargedEmEnergy;
	iEvent.getByToken(chargedEmEnergy_, chargedEmEnergy);

	Handle<vector<float> > chargedHadronMultiplicity;
	iEvent.getByToken(chargedHadronMultiplicity_, chargedHadronMultiplicity);

	Handle<vector<float> > neutralHadronMultiplicity;
	iEvent.getByToken(neutralHadronMultiplicity_, neutralHadronMultiplicity);

	Handle<vector<float> > chargedMultiplicity;
	iEvent.getByToken(chargedMultiplicity_, chargedMultiplicity);

	Handle<vector<float> > muonEnergy;
	iEvent.getByToken(muonEnergy_, muonEnergy);

	bool ORTriggers = checkORListOfTriggerBits( triggerName, triggerBit, triggerPass );
	// PU Reweight
	if ( isData ) puWeight = 1;
	else puWeight = PUWeight_.getPUWeight( *trueNInt, *bunchCross );
	histos1D_[ "PUWeight" ]->Fill( puWeight );
	lumiWeight = scale;
	double totalWeight = puWeight * lumiWeight;
	
	cutmap["Processed"] += totalWeight;

	int numPV = *NPV;
	vector< myJet > JETS;
	vector< float > tmpTriggerMass;
	int numberJets = 0;
	double rawHT = 0;
	//bool bTagCSV = 0;
	HT = 0;

	for (size_t i = 0; i < jetPt->size(); i++) {

		if( TMath::Abs( (*jetEta)[i] ) > 2.4 ) continue;

		rawHT += (*jetPt)[i];
		histos1D_[ "rawJetPt" ]->Fill( (*jetPt)[i] , puWeight );

		bool idL = jetID( (*jetEta)[i], (*jetE)[i], (*jecFactor)[i], (*neutralHadronEnergy)[i], (*neutralEmEnergy)[i], (*chargedHadronEnergy)[i], (*muonEnergy)[i], (*chargedEmEnergy)[i], (*chargedHadronMultiplicity)[i], (*neutralHadronMultiplicity)[i], (*chargedMultiplicity)[i] ); 

		if( ( (*jetPt)[i] > 40. ) && idL ) { 

			HT += (*jetPt)[i];
			++numberJets;

			TLorentzVector tmpJet;
			tmpJet.SetPtEtaPhiE( (*jetPt)[i], (*jetEta)[i], (*jetPhi)[i], (*jetE)[i] );

			//if ( (*jetCSV)[i] > 0.244 ) bTagCSV = 1; 	// CSVL
			//if ( (*jetCSV)[i] > 0.679 ) bTagCSV = 1; 	// CSVM
			//if ( (*jetCSVV1)[i] > 0.405 ) bTagCSV = 1; 	// CSVV1L
			//if ( (*jetCSVV1)[i] > 0.783 ) bTagCSV = 1; 	// CSVV1M
			//
			histos1D_[ "jetPt" ]->Fill( (*jetPt)[i] , puWeight );
			histos1D_[ "jetEta" ]->Fill( (*jetEta)[i] , puWeight );
			double jec = 1. / ( (*jecFactor)[i] * (*jetE)[i] );
			histos1D_[ "neutralHadronEnergy" ]->Fill( (*neutralHadronEnergy)[i] * jec, puWeight );
			histos1D_[ "neutralEmEnergy" ]->Fill( (*neutralEmEnergy)[i] * jec, puWeight );
			histos1D_[ "chargedHadronEnergy" ]->Fill( (*chargedHadronEnergy)[i] * jec, puWeight );
			histos1D_[ "chargedEmEnergy" ]->Fill( (*chargedEmEnergy)[i] * jec, puWeight );
			histos1D_[ "numConst" ]->Fill( (*chargedHadronMultiplicity)[i] + (*neutralHadronMultiplicity)[i], puWeight );
			histos1D_[ "chargedMultiplicity" ]->Fill( (*chargedMultiplicity)[i] * jec, puWeight );

			myJet tmpJET;
			tmpJET.p4 = tmpJet;
			tmpJET.btagCSV = (*jetCSV)[i];
			tmpJET.nhf = (*neutralHadronEnergy)[i] * jec;
			tmpJET.nEMf = (*neutralEmEnergy)[i] * jec;
			tmpJET.chf = (*chargedHadronEnergy)[i] * jec;
			tmpJET.cEMf = (*chargedEmEnergy)[i] * jec;
			tmpJET.numConst = (*chargedHadronMultiplicity)[i] + (*neutralHadronMultiplicity)[i];
			tmpJET.chm = (*chargedMultiplicity)[i] * jec;
			JETS.push_back( tmpJET );
		}
	}

	//sort(JETS.begin(), JETS.end(), [](const JETtype &p1, const JETtype &p2) { TLorentzVector tmpP1, tmpP2; tmpP1 = p1; tmpP2 = p2;  return tmpP1.M() > tmpP2.M(); }); 
	numJets = numberJets;
	histos1D_[ "jetNum" ]->Fill( numJets, totalWeight );
	histos1D_[ "NPV" ]->Fill( numPV, totalWeight );
	histos1D_[ "NPV_NOPUWeight" ]->Fill( numPV );
	if ( HT > 0 ) histos1D_[ "HT" ]->Fill( HT , totalWeight );
	if ( rawHT > 0 ) histos1D_[ "rawHT" ]->Fill( rawHT , totalWeight );
	MET = (*metPt)[0];

	clearVariables();

	if ( ORTriggers ) {
		
		cutmap["Trigger"] += totalWeight;
		histos1D_[ "HT_cutTrigger" ]->Fill( HT , totalWeight );
		histos1D_[ "jetNum_cutTrigger" ]->Fill( numJets, totalWeight );
		for (int i = 0; i < numJets; i++) {
			histos1D_[ "jetPt_cutTrigger" ]->Fill( JETS[i].p4.Pt(), totalWeight );
			histos1D_[ "jetEta_cutTrigger" ]->Fill( JETS[i].p4.Eta(), totalWeight );
		}
		event		= *ievent;
		run		= *Run;
		lumi		= *Lumi;

		if( numJets > 3 ) { 
			
			cutmap["4Jets"] += totalWeight;
			if ( !mkTree ) {
				histos1D_[ "HT_cut4Jets" ]->Fill( HT, totalWeight );
				histos1D_[ "jetNum_cut4Jets" ]->Fill( numJets, totalWeight );
				histos1D_[ "jet1Pt_cut4Jets" ]->Fill( JETS[0].p4.Pt(), totalWeight );
				histos1D_[ "jet2Pt_cut4Jets" ]->Fill( JETS[1].p4.Pt(), totalWeight );
				histos1D_[ "jet3Pt_cut4Jets" ]->Fill( JETS[2].p4.Pt(), totalWeight );
				histos1D_[ "jet4Pt_cut4Jets" ]->Fill( JETS[3].p4.Pt(), totalWeight );
				histos1D_[ "MET_cut4Jets" ]->Fill( MET, totalWeight );
			}

			if( ( numJets == 4 ) && ( HT > cutHT ) ){
				
				vector<double> tmpDijetR;
				double dR12 = JETS[0].p4.DeltaR( JETS[1].p4 );
				double dR34 = JETS[2].p4.DeltaR( JETS[3].p4 );
				bool maxdR1234 = (dR12 > dR34);
				double deltaR1234 = abs( dR12 - 0.8 )  + abs( dR34 - 0.8 );
				tmpDijetR.push_back( deltaR1234 );

				double dR13 = JETS[0].p4.DeltaR( JETS[2].p4 );
				double dR24 = JETS[1].p4.DeltaR( JETS[3].p4 );
				bool maxdR1324 = (dR13 > dR24);
				double deltaR1324 = abs( dR13 - 0.8 )  + abs( dR24 - 0.8 );
				tmpDijetR.push_back( deltaR1324 );

				double dR14 = JETS[0].p4.DeltaR( JETS[3].p4 );
				double dR23 = JETS[1].p4.DeltaR( JETS[2].p4 );
				bool maxdR1423 = (dR14 > dR23);
				double deltaR1423 = abs( dR14 - 0.8 )  + abs( dR23 - 0.8 );
				tmpDijetR.push_back( deltaR1423 );

				//LogWarning("test") << min_element(tmpDijetR.begin(), tmpDijetR.end()) - tmpDijetR.begin()  << " " << deltaR1234 << " " << deltaR1324 << " " << deltaR1423 ;
				int minDeltaR = min_element(tmpDijetR.begin(), tmpDijetR.end()) - tmpDijetR.begin();
				TLorentzVector j1, j2, j3, j4;
				double qgl1 = -9999, qgl2 = -9999, qgl3 = -9999, qgl4 = -9999;

				if( minDeltaR == 0 ){
					if ( maxdR1234 ){
						j1 = JETS[0].p4;
						j2 = JETS[1].p4;
						j3 = JETS[2].p4;
						j4 = JETS[3].p4;
						qgl1 = JETS[0].qgl;
						qgl2 = JETS[1].qgl;
						qgl3 = JETS[2].qgl;
						qgl4 = JETS[3].qgl;
					} else{
						j1 = JETS[2].p4;
						j2 = JETS[3].p4;
						j3 = JETS[0].p4;
						j4 = JETS[1].p4;
						qgl1 = JETS[2].qgl;
						qgl2 = JETS[3].qgl;
						qgl3 = JETS[0].qgl;
						qgl4 = JETS[1].qgl;
					}
				} else if ( minDeltaR == 1 ) {
					if ( maxdR1324 ){
						j1 = JETS[0].p4;
						j2 = JETS[2].p4;
						j3 = JETS[1].p4;
						j4 = JETS[3].p4;
						qgl1 = JETS[0].qgl;
						qgl2 = JETS[2].qgl;
						qgl3 = JETS[1].qgl;
						qgl4 = JETS[3].qgl;
					} else {
						j1 = JETS[1].p4;
						j2 = JETS[3].p4;
						j3 = JETS[0].p4;
						j4 = JETS[2].p4;
						qgl1 = JETS[1].qgl;
						qgl2 = JETS[3].qgl;
						qgl3 = JETS[0].qgl;
						qgl4 = JETS[2].qgl;
					}
				} else if ( minDeltaR == 2 ) {
					if ( maxdR1423 ){
						j1 = JETS[0].p4;
						j2 = JETS[3].p4;
						j3 = JETS[1].p4;
						j4 = JETS[2].p4;
						qgl1 = JETS[0].qgl;
						qgl2 = JETS[3].qgl;
						qgl3 = JETS[1].qgl;
						qgl4 = JETS[2].qgl;
					} else {
						j1 = JETS[1].p4;
						j2 = JETS[2].p4;
						j3 = JETS[0].p4;
						j4 = JETS[3].p4;
						qgl1 = JETS[1].qgl;
						qgl2 = JETS[2].qgl;
						qgl3 = JETS[0].qgl;
						qgl4 = JETS[3].qgl;
					}
				}

				jetsPt->push_back( j1.Pt() );
				jetsPt->push_back( j2.Pt() );
				jetsPt->push_back( j3.Pt() );
				jetsPt->push_back( j4.Pt() );
				jetsEta->push_back( j1.Eta() );
				jetsEta->push_back( j2.Eta() );
				jetsEta->push_back( j3.Eta() );
				jetsEta->push_back( j4.Eta() );
				jetsPhi->push_back( j1.Phi() );
				jetsPhi->push_back( j2.Phi() );
				jetsPhi->push_back( j3.Phi() );
				jetsPhi->push_back( j4.Phi() );
				jetsE->push_back( j1.E() );
				jetsE->push_back( j2.E() );
				jetsE->push_back( j3.E() );
				jetsE->push_back( j4.E() );
				jetsQGL->push_back( qgl1 );
				jetsQGL->push_back( qgl2 );
				jetsQGL->push_back( qgl3 );
				jetsQGL->push_back( qgl4 );

				mass1 = ( j1 + j2 ).M();
				mass2 = ( j3 + j4 ).M();
				avgMass = ( mass1 + mass2 ) / 2;
				delta1 = ( j1.Pt() + j2.Pt() ) - avgMass;
				delta2 = ( j3.Pt() + j4.Pt() ) - avgMass;
				massRes = TMath::Abs( mass1 - mass2 ) / avgMass;
				eta1 = ( j1 + j2 ).Eta();
				eta2 = ( j3 + j4 ).Eta();
				deltaEta = TMath::Abs( eta1 - eta2 );
				deltaR = abs( ( j1.DeltaR( j2 ) - 0.8 )  + abs( ( j3.DeltaR( j4 ) - 0.8 ) ) );
				cosThetaStar1 = cosThetaStar( j1, j2 );
				cosThetaStar2 = cosThetaStar( j3, j4 );

				if ( mkTree ) {
					RUNAtree->Fill();
				} else {

					cutmap["BestPair"] += totalWeight;
					histos1D_[ "HT_cutBestPair" ]->Fill( HT, totalWeight );
					histos1D_[ "MET_cutBestPair" ]->Fill( MET, totalWeight );
					histos1D_[ "jetNum_cutBestPair" ]->Fill( numJets, totalWeight );
					histos1D_[ "jet1Pt_cutBestPair" ]->Fill( JETS[0].p4.Pt(), totalWeight );
					histos1D_[ "jet2Pt_cutBestPair" ]->Fill( JETS[1].p4.Pt(), totalWeight );
					histos1D_[ "jet3Pt_cutBestPair" ]->Fill( JETS[2].p4.Pt(), totalWeight );
					histos1D_[ "jet4Pt_cutBestPair" ]->Fill( JETS[3].p4.Pt(), totalWeight );
					histos1D_[ "jet1QGL_cutBestPair" ]->Fill( qgl1, totalWeight );
					histos1D_[ "jet2QGL_cutBestPair" ]->Fill( qgl2, totalWeight );
					histos1D_[ "jet3QGL_cutBestPair" ]->Fill( qgl3, totalWeight );
					histos1D_[ "jet4QGL_cutBestPair" ]->Fill( qgl4, totalWeight );
					histos1D_[ "NPV_cutBestPair" ]->Fill( numPV, totalWeight );
					for (int i = 0; i < numJets; i++) {
						histos1D_[ "neutralHadronEnergy_cutBestPair" ]->Fill( JETS[i].nhf, totalWeight );
						histos1D_[ "neutralEmEnergy_cutBestPair" ]->Fill( JETS[i].nEMf, totalWeight );
						histos1D_[ "chargedHadronEnergy_cutBestPair" ]->Fill( JETS[i].chf, totalWeight );
						histos1D_[ "chargedEmEnergy_cutBestPair" ]->Fill( JETS[i].cEMf, totalWeight );
						histos1D_[ "numConst_cutBestPair" ]->Fill( JETS[i].numConst, totalWeight );
						histos1D_[ "chargedMultiplicity_cutBestPair" ]->Fill( JETS[i].chm, totalWeight );
					}

					histos1D_[ "massAve_cutBestPair" ]->Fill( avgMass, totalWeight );
					histos1D_[ "massRes_cutBestPair" ]->Fill( massRes, totalWeight );
					histos1D_[ "deltaEta_cutBestPair" ]->Fill( deltaEta, totalWeight );
					histos1D_[ "minDeltaR_cutBestPair" ]->Fill( minDeltaR , totalWeight );
					histos1D_[ "deltaR_cutBestPair" ]->Fill( deltaR , totalWeight );
					histos1D_[ "cosThetaStar1_cutBestPair" ]->Fill( cosThetaStar1 , totalWeight );
					histos1D_[ "cosThetaStar2_cutBestPair" ]->Fill( cosThetaStar2 , totalWeight );
					histos2D_[ "deltavsMassAve_cutBestPair" ]->Fill( avgMass, delta1 , totalWeight );
					histos2D_[ "deltavsMassAve_cutBestPair" ]->Fill( avgMass, delta2 , totalWeight );
					histos2D_[ "dijetsEta_cutBestPair" ]->Fill( eta1, eta2, totalWeight );

					if ( ( delta1 > cutDelta ) && ( delta2  > cutDelta ) ) {
						cutmap["Delta"] += totalWeight;
						histos1D_[ "HT_cutDelta" ]->Fill( HT, totalWeight );
						histos1D_[ "jetNum_cutDelta" ]->Fill( numJets, totalWeight );
						histos1D_[ "jet1Pt_cutDelta" ]->Fill( JETS[0].p4.Pt(), totalWeight );
						histos1D_[ "jet2Pt_cutDelta" ]->Fill( JETS[1].p4.Pt(), totalWeight );
						histos1D_[ "jet3Pt_cutDelta" ]->Fill( JETS[2].p4.Pt(), totalWeight );
						histos1D_[ "jet4Pt_cutDelta" ]->Fill( JETS[3].p4.Pt(), totalWeight );
						histos1D_[ "massAve_cutDelta" ]->Fill( avgMass, totalWeight );
						histos1D_[ "massRes_cutDelta" ]->Fill( massRes, totalWeight );
						histos1D_[ "deltaEta_cutDelta" ]->Fill( deltaEta, totalWeight );
						histos1D_[ "minDeltaR_cutDelta" ]->Fill( minDeltaR , totalWeight );
						histos2D_[ "deltavsMassAve_cutDelta" ]->Fill( avgMass, delta1 , totalWeight );
						histos2D_[ "deltavsMassAve_cutDelta" ]->Fill( avgMass, delta2 , totalWeight );
						histos2D_[ "dijetsEta_cutDelta" ]->Fill( eta1, eta2, totalWeight );

						if ( massRes < cutMassRes ) { 
							cutmap["MassRes"] += totalWeight;
							histos1D_[ "HT_cutMassRes" ]->Fill( HT, totalWeight );
							histos1D_[ "jetNum_cutMassRes" ]->Fill( numJets, totalWeight );
							histos1D_[ "jet1Pt_cutMassRes" ]->Fill( JETS[0].p4.Pt(), totalWeight );
							histos1D_[ "jet2Pt_cutMassRes" ]->Fill( JETS[1].p4.Pt(), totalWeight );
							histos1D_[ "jet3Pt_cutMassRes" ]->Fill( JETS[2].p4.Pt(), totalWeight );
							histos1D_[ "jet4Pt_cutMassRes" ]->Fill( JETS[3].p4.Pt(), totalWeight );
							histos1D_[ "massAve_cutMassRes" ]->Fill( avgMass, totalWeight );
							histos1D_[ "massRes_cutMassRes" ]->Fill( massRes, totalWeight );
							histos1D_[ "deltaEta_cutMassRes" ]->Fill( deltaEta, totalWeight );
							histos1D_[ "minDeltaR_cutMassRes" ]->Fill( minDeltaR , totalWeight );
							histos2D_[ "deltavsMassAve_cutMassRes" ]->Fill( avgMass, delta1 , totalWeight );
							histos2D_[ "deltavsMassAve_cutMassRes" ]->Fill( avgMass, delta2 , totalWeight );
							histos2D_[ "dijetsEta_cutMassRes" ]->Fill( eta1, eta2, totalWeight );
						
							if ( TMath::Abs(eta1 - eta2) <  cutEtaBand ) {
								cutmap["EtaBand"] += totalWeight;
								histos1D_[ "HT_cutEtaBand" ]->Fill( HT, totalWeight );
								histos1D_[ "jetNum_cutEtaBand" ]->Fill( numJets, totalWeight );
								histos1D_[ "jet1Pt_cutEtaBand" ]->Fill( JETS[0].p4.Pt(), totalWeight );
								histos1D_[ "jet2Pt_cutEtaBand" ]->Fill( JETS[1].p4.Pt(), totalWeight );
								histos1D_[ "jet3Pt_cutEtaBand" ]->Fill( JETS[2].p4.Pt(), totalWeight );
								histos1D_[ "jet4Pt_cutEtaBand" ]->Fill( JETS[3].p4.Pt(), totalWeight );
								histos1D_[ "massAve_cutEtaBand" ]->Fill( avgMass, totalWeight );
								histos1D_[ "massRes_cutEtaBand" ]->Fill( massRes, totalWeight );
								histos1D_[ "deltaEta_cutEtaBand" ]->Fill( deltaEta, totalWeight );
								histos1D_[ "minEtaBandR_cutEtaBand" ]->Fill( minDeltaR , totalWeight );
								histos2D_[ "deltavsMassAve_cutEtaBand" ]->Fill( avgMass, delta1 , totalWeight );
								histos2D_[ "deltavsMassAve_cutEtaBand" ]->Fill( avgMass, delta2 , totalWeight );
								histos2D_[ "dijetsEta_cutEtaBand" ]->Fill( eta1, eta2, totalWeight );
							}
						}
					}
					
					if ( deltaR < cutDeltaR )  {
						cutmap["DeltaR"] += totalWeight;
						histos1D_[ "HT_cutDeltaR" ]->Fill( HT, totalWeight );
						histos1D_[ "jetNum_cutDeltaR" ]->Fill( numJets, totalWeight );
						histos1D_[ "jet1Pt_cutDeltaR" ]->Fill( JETS[0].p4.Pt(), totalWeight );
						histos1D_[ "jet2Pt_cutDeltaR" ]->Fill( JETS[1].p4.Pt(), totalWeight );
						histos1D_[ "jet3Pt_cutDeltaR" ]->Fill( JETS[2].p4.Pt(), totalWeight );
						histos1D_[ "jet4Pt_cutDeltaR" ]->Fill( JETS[3].p4.Pt(), totalWeight );
						histos1D_[ "jet1QGL_cutDeltaR" ]->Fill( qgl1, totalWeight );
						histos1D_[ "jet2QGL_cutDeltaR" ]->Fill( qgl2, totalWeight );
						histos1D_[ "jet3QGL_cutDeltaR" ]->Fill( qgl3, totalWeight );
						histos1D_[ "jet4QGL_cutDeltaR" ]->Fill( qgl4, totalWeight );
						histos1D_[ "massAve_cutDeltaR" ]->Fill( avgMass, totalWeight );
						histos1D_[ "massRes_cutDeltaR" ]->Fill( massRes, totalWeight );
						histos1D_[ "deltaEta_cutDeltaR" ]->Fill( deltaEta, totalWeight );
						histos1D_[ "minDeltaR_cutDelta" ]->Fill( minDeltaR , totalWeight );
						histos2D_[ "dijetsEta_cutDeltaR" ]->Fill( eta1, eta2, totalWeight );
						histos1D_[ "deltaR_cutDeltaR" ]->Fill( deltaR , totalWeight );
						histos1D_[ "cosThetaStar1_cutDeltaR" ]->Fill( cosThetaStar1 , totalWeight );
						histos1D_[ "cosThetaStar2_cutDeltaR" ]->Fill( cosThetaStar2 , totalWeight );

						if ( TMath::Abs(eta1 - eta2) <  cutEtaBand ) {
							cutmap["DEta"] += totalWeight;
							histos1D_[ "HT_cutDEta" ]->Fill( HT, totalWeight );
							histos1D_[ "jetNum_cutDEta" ]->Fill( numJets, totalWeight );
							histos1D_[ "jet1Pt_cutDEta" ]->Fill( JETS[0].p4.Pt(), totalWeight );
							histos1D_[ "jet2Pt_cutDEta" ]->Fill( JETS[1].p4.Pt(), totalWeight );
							histos1D_[ "jet3Pt_cutDEta" ]->Fill( JETS[2].p4.Pt(), totalWeight );
							histos1D_[ "jet4Pt_cutDEta" ]->Fill( JETS[3].p4.Pt(), totalWeight );
							histos1D_[ "jet1QGL_cutDEta" ]->Fill( qgl1, totalWeight );
							histos1D_[ "jet2QGL_cutDEta" ]->Fill( qgl2, totalWeight );
							histos1D_[ "jet3QGL_cutDEta" ]->Fill( qgl3, totalWeight );
							histos1D_[ "jet4QGL_cutDEta" ]->Fill( qgl4, totalWeight );
							histos1D_[ "massAve_cutDEta" ]->Fill( avgMass, totalWeight );
							histos1D_[ "massRes_cutDEta" ]->Fill( massRes, totalWeight );
							histos1D_[ "deltaEta_cutDEta" ]->Fill( deltaEta, totalWeight );
							histos1D_[ "minDeltaR_cutDEta" ]->Fill( minDeltaR , totalWeight );
							histos2D_[ "dijetsEta_cutDEta" ]->Fill( eta1, eta2, totalWeight );
							histos1D_[ "deltaR_cutDEta" ]->Fill( deltaR , totalWeight );
							histos1D_[ "cosThetaStar1_cutDEta" ]->Fill( cosThetaStar1 , totalWeight );
							histos1D_[ "cosThetaStar2_cutDEta" ]->Fill( cosThetaStar2 , totalWeight );

							if ( massRes < cutMassRes ) { 
								cutmap["MassPairing"] += totalWeight;
								histos1D_[ "HT_cutMassPairing" ]->Fill( HT, totalWeight );
								histos1D_[ "jetNum_cutMassPairing" ]->Fill( numJets, totalWeight );
								histos1D_[ "jet1Pt_cutMassPairing" ]->Fill( JETS[0].p4.Pt(), totalWeight );
								histos1D_[ "jet2Pt_cutMassPairing" ]->Fill( JETS[1].p4.Pt(), totalWeight );
								histos1D_[ "jet3Pt_cutMassPairing" ]->Fill( JETS[2].p4.Pt(), totalWeight );
								histos1D_[ "jet4Pt_cutMassPairing" ]->Fill( JETS[3].p4.Pt(), totalWeight );
								histos1D_[ "jet1QGL_cutMassPairing" ]->Fill( qgl1, totalWeight );
								histos1D_[ "jet2QGL_cutMassPairing" ]->Fill( qgl2, totalWeight );
								histos1D_[ "jet3QGL_cutMassPairing" ]->Fill( qgl3, totalWeight );
								histos1D_[ "jet4QGL_cutMassPairing" ]->Fill( qgl4, totalWeight );
								histos1D_[ "massAve_cutMassPairing" ]->Fill( avgMass, totalWeight );
								histos1D_[ "massRes_cutMassPairing" ]->Fill( massRes, totalWeight );
								histos1D_[ "deltaEta_cutMassPairing" ]->Fill( deltaEta, totalWeight );
								histos1D_[ "minDeltaR_cutMassPairing" ]->Fill( minDeltaR , totalWeight );
								histos2D_[ "dijetsEta_cutMassPairing" ]->Fill( eta1, eta2, totalWeight );
								histos1D_[ "deltaR_cutMassPairing" ]->Fill( deltaR , totalWeight );
								histos1D_[ "cosThetaStar1_cutMassPairing" ]->Fill( cosThetaStar1 , totalWeight );
								histos1D_[ "cosThetaStar2_cutMassPairing" ]->Fill( cosThetaStar2 , totalWeight );

							}
								if ( ( cosThetaStar1 < cutCosThetaStar ) && ( cosThetaStar2 < cutCosThetaStar )){
									cutmap["CosTheta"] += totalWeight;
									histos1D_[ "HT_cutCosTheta" ]->Fill( HT, totalWeight );
									histos1D_[ "jetNum_cutCosTheta" ]->Fill( numJets, totalWeight );
									histos1D_[ "jet1Pt_cutCosTheta" ]->Fill( JETS[0].p4.Pt(), totalWeight );
									histos1D_[ "jet2Pt_cutCosTheta" ]->Fill( JETS[1].p4.Pt(), totalWeight );
									histos1D_[ "jet3Pt_cutCosTheta" ]->Fill( JETS[2].p4.Pt(), totalWeight );
									histos1D_[ "jet4Pt_cutCosTheta" ]->Fill( JETS[3].p4.Pt(), totalWeight );
									histos1D_[ "jet1QGL_cutCosTheta" ]->Fill( qgl1, totalWeight );
									histos1D_[ "jet2QGL_cutCosTheta" ]->Fill( qgl2, totalWeight );
									histos1D_[ "jet3QGL_cutCosTheta" ]->Fill( qgl3, totalWeight );
									histos1D_[ "jet4QGL_cutCosTheta" ]->Fill( qgl4, totalWeight );
									histos1D_[ "massAve_cutCosTheta" ]->Fill( avgMass, totalWeight );
									histos1D_[ "massRes_cutCosTheta" ]->Fill( massRes, totalWeight );
									histos1D_[ "deltaEta_cutCosTheta" ]->Fill( deltaEta, totalWeight );
									histos1D_[ "minDeltaR_cutCosTheta" ]->Fill( minDeltaR, totalWeight );
									histos2D_[ "dijetsEta_cutCosTheta" ]->Fill( eta1, eta2, totalWeight );
									histos1D_[ "deltaR_cutCosTheta" ]->Fill( deltaR , totalWeight );
									histos1D_[ "cosThetaStar1_cutCosTheta" ]->Fill( cosThetaStar1 , totalWeight );
									histos1D_[ "cosThetaStar2_cutCosTheta" ]->Fill( cosThetaStar2 , totalWeight );
									
									}
						}
					}
				}
			}
		}
	}
	JETS.clear();
}


// ------------ method called once each job just before starting event loop  ------------
void RUNAnalysis::beginJob() {

	// Calculate PUWeight
	if ( !isData ) PUWeight_.generateWeights( dataPUFile );

	histos1D_[ "rawJetPt" ] = fs_->make< TH1D >( "rawJetPt", "rawJetPt", 100, 0., 1000. );
	histos1D_[ "rawJetPt" ]->Sumw2();
	histos1D_[ "rawHT" ] = fs_->make< TH1D >( "rawHT", "rawHT", 300, 0., 3000. );
	histos1D_[ "rawHT" ]->Sumw2();

	histos1D_[ "jetPt" ] = fs_->make< TH1D >( "jetPt", "jetPt", 100, 0., 1000. );
	histos1D_[ "jetPt" ]->Sumw2();
	histos1D_[ "jetEta" ] = fs_->make< TH1D >( "jetEta", "jetEta", 100, -5., 5. );
	histos1D_[ "jetEta" ]->Sumw2();
	histos1D_[ "jetNum" ] = fs_->make< TH1D >( "jetNum", "jetNum", 10, 0., 10. );
	histos1D_[ "jetNum" ]->Sumw2();
	histos1D_[ "HT" ] = fs_->make< TH1D >( "HT", "HT", 300, 0., 3000. );
	histos1D_[ "HT" ]->Sumw2();
	histos1D_[ "NPV" ] = fs_->make< TH1D >( "NPV", "NPV", 80, 0., 80. );
	histos1D_[ "NPV" ]->Sumw2();
	histos1D_[ "NPV_NOPUWeight" ] = fs_->make< TH1D >( "NPV_NOPUWeight", "NPV_NOPUWeight", 80, 0., 80. );
	histos1D_[ "NPV_NOPUWeight" ]->Sumw2();
	histos1D_[ "PUWeight" ] = fs_->make< TH1D >( "PUWeight", "PUWeight", 50, 0., 5. );
	histos1D_[ "PUWeight" ]->Sumw2();
	histos1D_[ "neutralHadronEnergy" ] = fs_->make< TH1D >( "neutralHadronEnergy", "neutralHadronEnergy", 50, 0., 1. );
	histos1D_[ "neutralHadronEnergy" ]->Sumw2();
	histos1D_[ "neutralEmEnergy" ] = fs_->make< TH1D >( "neutralEmEnergy", "neutralEmEnergy", 50, 0., 1. );
	histos1D_[ "neutralEmEnergy" ]->Sumw2();
	histos1D_[ "chargedHadronEnergy" ] = fs_->make< TH1D >( "chargedHadronEnergy", "chargedHadronEnergy", 50, 0., 1. );
	histos1D_[ "chargedHadronEnergy" ]->Sumw2();
	histos1D_[ "chargedEmEnergy" ] = fs_->make< TH1D >( "chargedEmEnergy", "chargedEmEnergy", 50, 0., 1. );
	histos1D_[ "chargedEmEnergy" ]->Sumw2();
	histos1D_[ "chargedMultiplicity" ] = fs_->make< TH1D >( "chargedMultiplicity", "chargedMultiplicity", 50, 0., 1. );
	histos1D_[ "chargedMultiplicity" ]->Sumw2();
	histos1D_[ "numConst" ] = fs_->make< TH1D >( "numConst", "numConst", 100, 0., 100. );
	histos1D_[ "numConst" ]->Sumw2();


	histos1D_[ "jetPt_cutTrigger" ] = fs_->make< TH1D >( "jetPt_cutTrigger", "jetPt_cutTrigger", 100, 0., 1000. );
	histos1D_[ "jetPt_cutTrigger" ]->Sumw2();
	histos1D_[ "jetEta_cutTrigger" ] = fs_->make< TH1D >( "jetEta_cutTrigger", "jetEta_cutTrigger", 100, -5., 5. );
	histos1D_[ "jetEta_cutTrigger" ]->Sumw2();
	histos1D_[ "jetNum_cutTrigger" ] = fs_->make< TH1D >( "jetNum_cutTrigger", "jetNum_cutTrigger", 10, 0., 10. );
	histos1D_[ "jetNum_cutTrigger" ]->Sumw2();
	histos1D_[ "HT_cutTrigger" ] = fs_->make< TH1D >( "HT_cutTrigger", "HT_cutTrigger", 300, 0., 3000. );
	histos1D_[ "HT_cutTrigger" ]->Sumw2();


	if (mkTree) {
		RUNAtree = fs_->make< TTree >("RUNATree", "RUNATree"); 
		RUNAtree->Branch( "run", &run, "run/I" );
		RUNAtree->Branch( "lumi", &lumi, "lumi/I" );
		RUNAtree->Branch( "event", &event, "event/I" );
		RUNAtree->Branch( "numJets", &numJets, "numJets/I" );
		RUNAtree->Branch( "numPV", &numPV, "numPV/I" );
		RUNAtree->Branch( "puWeight", &puWeight, "puWeight/F" );
		RUNAtree->Branch( "lumiWeight", &lumiWeight, "lumiWeight/F" );
		RUNAtree->Branch( "HT", &HT, "HT/F" );
		RUNAtree->Branch( "mass1", &mass1, "mass1/F" );
		RUNAtree->Branch( "mass2", &mass2, "mass2/F" );
		RUNAtree->Branch( "avgMass", &avgMass, "avgMass/F" );
		RUNAtree->Branch( "delta1", &delta1, "delta1/F" );
		RUNAtree->Branch( "delta2", &delta2, "delta2/F" );
		RUNAtree->Branch( "massRes", &massRes, "massRes/F" );
		RUNAtree->Branch( "eta1", &eta1, "eta1/F" );
		RUNAtree->Branch( "eta2", &eta2, "eta2/F" );
		RUNAtree->Branch( "deltaEta", &deltaEta, "deltaEta/F" );
		RUNAtree->Branch( "deltaR", &deltaR, "deltaR/F" );
		RUNAtree->Branch( "cosThetaStar1", &cosThetaStar1, "cosThetaStar1/F" );
		RUNAtree->Branch( "cosThetaStar2", &cosThetaStar2, "cosThetaStar2/F" );
		RUNAtree->Branch( "jetsPt", "vector<float>", &jetsPt);
		RUNAtree->Branch( "jetsEta", "vector<float>", &jetsEta);
		RUNAtree->Branch( "jetsPhi", "vector<float>", &jetsPhi);
		RUNAtree->Branch( "jetsE", "vector<float>", &jetsE);
		RUNAtree->Branch( "jetsQGL", "vector<float>", &jetsQGL);
	} else {

		histos1D_[ "jet1Pt_cut4Jets" ] = fs_->make< TH1D >( "jet1Pt_cut4Jets", "jet1Pt_cut4Jets", 100, 0., 1000. );
		histos1D_[ "jet1Pt_cut4Jets" ]->Sumw2();
		histos1D_[ "jet2Pt_cut4Jets" ] = fs_->make< TH1D >( "jet2Pt_cut4Jets", "jet2Pt_cut4Jets", 100, 0., 1000. );
		histos1D_[ "jet2Pt_cut4Jets" ]->Sumw2();
		histos1D_[ "jet3Pt_cut4Jets" ] = fs_->make< TH1D >( "jet3Pt_cut4Jets", "jet3Pt_cut4Jets", 100, 0., 1000. );
		histos1D_[ "jet3Pt_cut4Jets" ]->Sumw2();
		histos1D_[ "jet4Pt_cut4Jets" ] = fs_->make< TH1D >( "jet4Pt_cut4Jets", "jet4Pt_cut4Jets", 100, 0., 1000. );
		histos1D_[ "jet4Pt_cut4Jets" ]->Sumw2();
		histos1D_[ "jetNum_cut4Jets" ] = fs_->make< TH1D >( "jetNum_cut4Jets", "jetNum_cut4Jets", 10, 0., 10. );
		histos1D_[ "jetNum_cut4Jets" ]->Sumw2();
		histos1D_[ "HT_cut4Jets" ] = fs_->make< TH1D >( "HT_cut4Jets", "HT_cut4Jets", 300, 0., 3000. );
		histos1D_[ "HT_cut4Jets" ]->Sumw2();
		histos1D_[ "MET_cut4Jets" ] = fs_->make< TH1D >( "MET_cut4Jets", "MET_cut4Jets", 20, 0., 200. );
		histos1D_[ "MET_cut4Jets" ]->Sumw2();

		histos1D_[ "jet1Pt_cutBestPair" ] = fs_->make< TH1D >( "jet1Pt_cutBestPair", "jet1Pt_cutBestPair", 100, 0., 1000. );
		histos1D_[ "jet1Pt_cutBestPair" ]->Sumw2();
		histos1D_[ "jet2Pt_cutBestPair" ] = fs_->make< TH1D >( "jet2Pt_cutBestPair", "jet2Pt_cutBestPair", 100, 0., 1000. );
		histos1D_[ "jet2Pt_cutBestPair" ]->Sumw2();
		histos1D_[ "jet3Pt_cutBestPair" ] = fs_->make< TH1D >( "jet3Pt_cutBestPair", "jet3Pt_cutBestPair", 100, 0., 1000. );
		histos1D_[ "jet3Pt_cutBestPair" ]->Sumw2();
		histos1D_[ "jet4Pt_cutBestPair" ] = fs_->make< TH1D >( "jet4Pt_cutBestPair", "jet4Pt_cutBestPair", 100, 0., 1000. );
		histos1D_[ "jet4Pt_cutBestPair" ]->Sumw2();
		histos1D_[ "jetNum_cutBestPair" ] = fs_->make< TH1D >( "jetNum_cutBestPair", "jetNum_cutBestPair", 10, 0., 10. );
		histos1D_[ "jetNum_cutBestPair" ]->Sumw2();
		histos1D_[ "HT_cutBestPair" ] = fs_->make< TH1D >( "HT_cutBestPair", "HT_cutBestPair", 300, 0., 3000. );
		histos1D_[ "HT_cutBestPair" ]->Sumw2();
		histos1D_[ "MET_cutBestPair" ] = fs_->make< TH1D >( "MET_cutBestPair", "MET_cutBestPair", 20, 0., 200. );
		histos1D_[ "MET_cutBestPair" ]->Sumw2();
		histos1D_[ "NPV_cutBestPair" ] = fs_->make< TH1D >( "NPV_cutBestPair", "NPV_cutBestPair", 80, 0., 80. );
		histos1D_[ "NPV_cutBestPair" ]->Sumw2();
		histos1D_[ "neutralHadronEnergy_cutBestPair" ] = fs_->make< TH1D >( "neutralHadronEnergy_cutBestPair", "neutralHadronEnergy", 50, 0., 1. );
		histos1D_[ "neutralHadronEnergy_cutBestPair" ]->Sumw2();
		histos1D_[ "neutralEmEnergy_cutBestPair" ] = fs_->make< TH1D >( "neutralEmEnergy_cutBestPair", "neutralEmEnergy", 50, 0., 1. );
		histos1D_[ "neutralEmEnergy_cutBestPair" ]->Sumw2();
		histos1D_[ "chargedHadronEnergy_cutBestPair" ] = fs_->make< TH1D >( "chargedHadronEnergy_cutBestPair", "chargedHadronEnergy", 50, 0., 1. );
		histos1D_[ "chargedHadronEnergy_cutBestPair" ]->Sumw2();
		histos1D_[ "chargedEmEnergy_cutBestPair" ] = fs_->make< TH1D >( "chargedEmEnergy_cutBestPair", "chargedEmEnergy", 50, 0., 1. );
		histos1D_[ "chargedEmEnergy_cutBestPair" ]->Sumw2();
		histos1D_[ "chargedMultiplicity_cutBestPair" ] = fs_->make< TH1D >( "chargedMultiplicity_cutBestPair", "chargedMultiplicity", 50, 0., 1. );
		histos1D_[ "chargedMultiplicity_cutBestPair" ]->Sumw2();
		histos1D_[ "numConst_cutBestPair" ] = fs_->make< TH1D >( "numConst_cutBestPair", "numConst", 100, 0., 100. );
		histos1D_[ "numConst_cutBestPair" ]->Sumw2();
		histos1D_[ "jet1QGL_cutBestPair" ] = fs_->make< TH1D >( "jet1QGL_cutBestPair", "jet1QGL_cutBestPair", 10, 0., 1. );
		histos1D_[ "jet1QGL_cutBestPair" ]->Sumw2();
		histos1D_[ "jet2QGL_cutBestPair" ] = fs_->make< TH1D >( "jet2QGL_cutBestPair", "jet2QGL_cutBestPair", 10, 0., 1. );
		histos1D_[ "jet2QGL_cutBestPair" ]->Sumw2();
		histos1D_[ "jet3QGL_cutBestPair" ] = fs_->make< TH1D >( "jet3QGL_cutBestPair", "jet3QGL_cutBestPair", 10, 0., 1. );
		histos1D_[ "jet3QGL_cutBestPair" ]->Sumw2();
		histos1D_[ "jet4QGL_cutBestPair" ] = fs_->make< TH1D >( "jet4QGL_cutBestPair", "jet4QGL_cutBestPair", 10, 0., 1. );
		histos1D_[ "jet4QGL_cutBestPair" ]->Sumw2();
		histos1D_[ "massAve_cutBestPair" ] = fs_->make< TH1D >( "massAve_cutBestPair", "massAve_cutBestPair", 200, 0., 2000. );
		histos1D_[ "massAve_cutBestPair" ]->Sumw2();
		histos1D_[ "massRes_cutBestPair" ] = fs_->make< TH1D >( "massRes_cutBestPair", "massRes_cutBestPair", 50, 0., 2. );
		histos1D_[ "massRes_cutBestPair" ]->Sumw2();
		histos1D_[ "deltaEta_cutBestPair" ] = fs_->make< TH1D >( "deltaEta_cutBestPair", "deltaEta_cutBestPair", 50, 0., 10. );
		histos1D_[ "deltaEta_cutBestPair" ]->Sumw2();
		histos1D_[ "minDeltaR_cutBestPair" ] = fs_->make< TH1D >( "minDeltaR_cutBestPair", "minDeltaR_cutBestPair", 50, 0., 5. );
		histos1D_[ "minDeltaR_cutBestPair" ]->Sumw2();
		histos1D_[ "deltaR_cutBestPair" ] = fs_->make< TH1D >( "deltaR_cutBestPair", "deltaR_cutBestPair", 50, 0., 5. );
		histos1D_[ "deltaR_cutBestPair" ]->Sumw2();
		histos1D_[ "cosThetaStar1_cutBestPair" ] = fs_->make< TH1D >( "cosThetaStar1_cutBestPair", "cosThetaStar1_cutBestPair", 10, 0., 1. );
		histos1D_[ "cosThetaStar1_cutBestPair" ]->Sumw2();
		histos1D_[ "cosThetaStar2_cutBestPair" ] = fs_->make< TH1D >( "cosThetaStar2_cutBestPair", "cosThetaStar2_cutBestPair", 10, 0., 1. );
		histos1D_[ "cosThetaStar2_cutBestPair" ]->Sumw2();
		histos2D_[ "deltavsMassAve_cutBestPair" ] = fs_->make< TH2D >( "deltavsMassAve_cutBestPair", "deltavsMassAve_cutBestPair", 200, 0., 2000.,  300, -500., 1000. );
		histos2D_[ "deltavsMassAve_cutBestPair" ]->Sumw2();
		histos2D_[ "dijetsEta_cutBestPair" ] = fs_->make< TH2D >( "dijetsEta_cutBestPair", "dijetsEta_cutBestPair", 48, -3., 3., 48, -3., 3. );
		histos2D_[ "dijetsEta_cutBestPair" ]->Sumw2();

		histos1D_[ "jet1Pt_cutMassRes" ] = fs_->make< TH1D >( "jet1Pt_cutMassRes", "jet1Pt_cutMassRes", 100, 0., 1000. );
		histos1D_[ "jet1Pt_cutMassRes" ]->Sumw2();
		histos1D_[ "jet2Pt_cutMassRes" ] = fs_->make< TH1D >( "jet2Pt_cutMassRes", "jet2Pt_cutMassRes", 100, 0., 1000. );
		histos1D_[ "jet2Pt_cutMassRes" ]->Sumw2();
		histos1D_[ "jet3Pt_cutMassRes" ] = fs_->make< TH1D >( "jet3Pt_cutMassRes", "jet3Pt_cutMassRes", 100, 0., 1000. );
		histos1D_[ "jet3Pt_cutMassRes" ]->Sumw2();
		histos1D_[ "jet4Pt_cutMassRes" ] = fs_->make< TH1D >( "jet4Pt_cutMassRes", "jet4Pt_cutMassRes", 100, 0., 1000. );
		histos1D_[ "jet4Pt_cutMassRes" ]->Sumw2();
		histos1D_[ "jetNum_cutMassRes" ] = fs_->make< TH1D >( "jetNum_cutMassRes", "jetNum_cutMassRes", 10, 0., 10. );
		histos1D_[ "jetNum_cutMassRes" ]->Sumw2();
		histos1D_[ "HT_cutMassRes" ] = fs_->make< TH1D >( "HT_cutMassRes", "HT_cutMassRes", 300, 0., 3000. );
		histos1D_[ "HT_cutMassRes" ]->Sumw2();
		histos1D_[ "massAve_cutMassRes" ] = fs_->make< TH1D >( "massAve_cutMassRes", "massAve_cutMassRes", 200, 0., 2000. );
		histos1D_[ "massAve_cutMassRes" ]->Sumw2();
		histos1D_[ "massRes_cutMassRes" ] = fs_->make< TH1D >( "massRes_cutMassRes", "massRes_cutMassRes", 50, 0., 2. );
		histos1D_[ "massRes_cutMassRes" ]->Sumw2();
		histos1D_[ "deltaEta_cutMassRes" ] = fs_->make< TH1D >( "deltaEta_cutMassRes", "deltaEta_cutMassRes", 50, 0., 10. );
		histos1D_[ "deltaEta_cutMassRes" ]->Sumw2();
		histos1D_[ "minDeltaR_cutMassRes" ] = fs_->make< TH1D >( "minDeltaR_cutMassRes", "minDeltaR_cutMassRes", 50, 0., 5. );
		histos1D_[ "minDeltaR_cutMassRes" ]->Sumw2();
		histos2D_[ "deltavsMassAve_cutMassRes" ] = fs_->make< TH2D >( "deltavsMassAve_cutMassRes", "deltavsMassAve_cutMassRes", 200, 0., 2000.,  300, -500., 1000. );
		histos2D_[ "deltavsMassAve_cutMassRes" ]->Sumw2();
		histos2D_[ "dijetsEta_cutMassRes" ] = fs_->make< TH2D >( "dijetsEta_cutMassRes", "dijetsEta_cutMassRes", 48, -3., 3., 48, -3., 3. );
		histos2D_[ "dijetsEta_cutMassRes" ]->Sumw2();

		histos1D_[ "jet1Pt_cutDelta" ] = fs_->make< TH1D >( "jet1Pt_cutDelta", "jet1Pt_cutDelta", 100, 0., 1000. );
		histos1D_[ "jet1Pt_cutDelta" ]->Sumw2();
		histos1D_[ "jet2Pt_cutDelta" ] = fs_->make< TH1D >( "jet2Pt_cutDelta", "jet2Pt_cutDelta", 100, 0., 1000. );
		histos1D_[ "jet2Pt_cutDelta" ]->Sumw2();
		histos1D_[ "jet3Pt_cutDelta" ] = fs_->make< TH1D >( "jet3Pt_cutDelta", "jet3Pt_cutDelta", 100, 0., 1000. );
		histos1D_[ "jet3Pt_cutDelta" ]->Sumw2();
		histos1D_[ "jet4Pt_cutDelta" ] = fs_->make< TH1D >( "jet4Pt_cutDelta", "jet4Pt_cutDelta", 100, 0., 1000. );
		histos1D_[ "jet4Pt_cutDelta" ]->Sumw2();
		histos1D_[ "jetNum_cutDelta" ] = fs_->make< TH1D >( "jetNum_cutDelta", "jetNum_cutDelta", 10, 0., 10. );
		histos1D_[ "jetNum_cutDelta" ]->Sumw2();
		histos1D_[ "HT_cutDelta" ] = fs_->make< TH1D >( "HT_cutDelta", "HT_cutDelta", 300, 0., 3000. );
		histos1D_[ "HT_cutDelta" ]->Sumw2();
		histos1D_[ "massAve_cutDelta" ] = fs_->make< TH1D >( "massAve_cutDelta", "massAve_cutDelta", 200, 0., 2000. );
		histos1D_[ "massAve_cutDelta" ]->Sumw2();
		histos1D_[ "massRes_cutDelta" ] = fs_->make< TH1D >( "massRes_cutDelta", "massRes_cutDelta", 50, 0., 2. );
		histos1D_[ "massRes_cutDelta" ]->Sumw2();
		histos1D_[ "deltaEta_cutDelta" ] = fs_->make< TH1D >( "deltaEta_cutDelta", "deltaEta_cutDelta", 50, 0., 10. );
		histos1D_[ "deltaEta_cutDelta" ]->Sumw2();
		histos1D_[ "minDeltaR_cutDelta" ] = fs_->make< TH1D >( "minDeltaR_cutDelta", "minDeltaR_cutDelta", 50, 0., 5. );
		histos1D_[ "minDeltaR_cutDelta" ]->Sumw2();
		histos2D_[ "deltavsMassAve_cutDelta" ] = fs_->make< TH2D >( "deltavsMassAve_cutDelta", "deltavsMassAve_cutDelta", 200, 0., 2000.,  300, -500., 1000. );
		histos2D_[ "deltavsMassAve_cutDelta" ]->Sumw2();
		histos2D_[ "dijetsEta_cutDelta" ] = fs_->make< TH2D >( "dijetsEta_cutDelta", "dijetsEta_cutDelta", 48, -3., 3., 48, -3., 3. );
		histos2D_[ "dijetsEta_cutDelta" ]->Sumw2();

		histos1D_[ "jet1Pt_cutEtaBand" ] = fs_->make< TH1D >( "jet1Pt_cutEtaBand", "jet1Pt_cutEtaBand", 100, 0., 1000. );
		histos1D_[ "jet1Pt_cutEtaBand" ]->Sumw2();
		histos1D_[ "jet2Pt_cutEtaBand" ] = fs_->make< TH1D >( "jet2Pt_cutEtaBand", "jet2Pt_cutEtaBand", 100, 0., 1000. );
		histos1D_[ "jet2Pt_cutEtaBand" ]->Sumw2();
		histos1D_[ "jet3Pt_cutEtaBand" ] = fs_->make< TH1D >( "jet3Pt_cutEtaBand", "jet3Pt_cutEtaBand", 100, 0., 1000. );
		histos1D_[ "jet3Pt_cutEtaBand" ]->Sumw2();
		histos1D_[ "jet4Pt_cutEtaBand" ] = fs_->make< TH1D >( "jet4Pt_cutEtaBand", "jet4Pt_cutEtaBand", 100, 0., 1000. );
		histos1D_[ "jet4Pt_cutEtaBand" ]->Sumw2();
		histos1D_[ "jetNum_cutEtaBand" ] = fs_->make< TH1D >( "jetNum_cutEtaBand", "jetNum_cutEtaBand", 10, 0., 10. );
		histos1D_[ "jetNum_cutEtaBand" ]->Sumw2();
		histos1D_[ "HT_cutEtaBand" ] = fs_->make< TH1D >( "HT_cutEtaBand", "HT_cutEtaBand", 300, 0., 3000. );
		histos1D_[ "HT_cutEtaBand" ]->Sumw2();
		histos1D_[ "massAve_cutEtaBand" ] = fs_->make< TH1D >( "massAve_cutEtaBand", "massAve_cutEtaBand", 200, 0., 2000. );
		histos1D_[ "massAve_cutEtaBand" ]->Sumw2();
		histos1D_[ "massRes_cutEtaBand" ] = fs_->make< TH1D >( "massRes_cutEtaBand", "massRes_cutEtaBand", 50, 0., 2. );
		histos1D_[ "massRes_cutEtaBand" ]->Sumw2();
		histos1D_[ "deltaEta_cutEtaBand" ] = fs_->make< TH1D >( "deltaEta_cutEtaBand", "deltaEta_cutEtaBand", 50, 0., 10. );
		histos1D_[ "deltaEta_cutEtaBand" ]->Sumw2();
		histos1D_[ "minEtaBandR_cutEtaBand" ] = fs_->make< TH1D >( "minEtaBandR_cutEtaBand", "minEtaBandR_cutEtaBand", 50, 0., 5. );
		histos1D_[ "minEtaBandR_cutEtaBand" ]->Sumw2();
		histos2D_[ "deltavsMassAve_cutEtaBand" ] = fs_->make< TH2D >( "deltavsMassAve_cutEtaBand", "deltavsMassAve_cutEtaBand", 200, 0., 2000.,  300, -500., 1000. );
		histos2D_[ "deltavsMassAve_cutEtaBand" ]->Sumw2();
		histos2D_[ "dijetsEta_cutEtaBand" ] = fs_->make< TH2D >( "dijetsEta_cutEtaBand", "dijetsEta_cutEtaBand", 48, -3., 3., 48, -3., 3. );
		histos2D_[ "dijetsEta_cutEtaBand" ]->Sumw2();
		
		
		histos1D_[ "jet1Pt_cutDeltaR" ] = fs_->make< TH1D >( "jet1Pt_cutDeltaR", "jet1Pt_cutDeltaR", 100, 0., 1000. );
		histos1D_[ "jet1Pt_cutDeltaR" ]->Sumw2();
		histos1D_[ "jet2Pt_cutDeltaR" ] = fs_->make< TH1D >( "jet2Pt_cutDeltaR", "jet2Pt_cutDeltaR", 100, 0., 1000. );
		histos1D_[ "jet2Pt_cutDeltaR" ]->Sumw2();
		histos1D_[ "jet3Pt_cutDeltaR" ] = fs_->make< TH1D >( "jet3Pt_cutDeltaR", "jet3Pt_cutDeltaR", 100, 0., 1000. );
		histos1D_[ "jet3Pt_cutDeltaR" ]->Sumw2();
		histos1D_[ "jet4Pt_cutDeltaR" ] = fs_->make< TH1D >( "jet4Pt_cutDeltaR", "jet4Pt_cutDeltaR", 100, 0., 1000. );
		histos1D_[ "jet4Pt_cutDeltaR" ]->Sumw2();
		histos1D_[ "jetNum_cutDeltaR" ] = fs_->make< TH1D >( "jetNum_cutDeltaR", "jetNum_cutDeltaR", 10, 0., 10. );
		histos1D_[ "jetNum_cutDeltaR" ]->Sumw2();
		histos1D_[ "HT_cutDeltaR" ] = fs_->make< TH1D >( "HT_cutDeltaR", "HT_cutDeltaR", 300, 0., 3000. );
		histos1D_[ "HT_cutDeltaR" ]->Sumw2();
		histos1D_[ "jet1QGL_cutDeltaR" ] = fs_->make< TH1D >( "jet1QGL_cutDeltaR", "jet1QGL_cutDeltaR", 10, 0., 1. );
		histos1D_[ "jet1QGL_cutDeltaR" ]->Sumw2();
		histos1D_[ "jet2QGL_cutDeltaR" ] = fs_->make< TH1D >( "jet2QGL_cutDeltaR", "jet2QGL_cutDeltaR", 10, 0., 1. );
		histos1D_[ "jet2QGL_cutDeltaR" ]->Sumw2();
		histos1D_[ "jet3QGL_cutDeltaR" ] = fs_->make< TH1D >( "jet3QGL_cutDeltaR", "jet3QGL_cutDeltaR", 10, 0., 1. );
		histos1D_[ "jet3QGL_cutDeltaR" ]->Sumw2();
		histos1D_[ "jet4QGL_cutDeltaR" ] = fs_->make< TH1D >( "jet4QGL_cutDeltaR", "jet4QGL_cutDeltaR", 10, 0., 1. );
		histos1D_[ "jet4QGL_cutDeltaR" ]->Sumw2();
		histos1D_[ "massAve_cutDeltaR" ] = fs_->make< TH1D >( "massAve_cutDeltaR", "massAve_cutDeltaR", 200, 0., 2000. );
		histos1D_[ "massAve_cutDeltaR" ]->Sumw2();
		histos1D_[ "massRes_cutDeltaR" ] = fs_->make< TH1D >( "massRes_cutDeltaR", "massRes_cutDeltaR", 50, 0., 2. );
		histos1D_[ "massRes_cutDeltaR" ]->Sumw2();
		histos1D_[ "deltaEta_cutDeltaR" ] = fs_->make< TH1D >( "deltaEta_cutDeltaR", "deltaEta_cutDeltaR", 50, 0., 10. );
		histos1D_[ "deltaEta_cutDeltaR" ]->Sumw2();
		histos1D_[ "minDeltaR_cutDeltaR" ] = fs_->make< TH1D >( "minDeltaR_cutDeltaR", "minDeltaR_cutDeltaR", 50, 0., 5. );
		histos1D_[ "minDeltaR_cutDeltaR" ]->Sumw2();
		histos2D_[ "dijetsEta_cutDeltaR" ] = fs_->make< TH2D >( "dijetsEta_cutDeltaR", "dijetsEta_cutDeltaR", 48, -3., 3., 48, -3., 3. );
		histos2D_[ "dijetsEta_cutDeltaR" ]->Sumw2();
		histos1D_[ "deltaR_cutDeltaR" ] = fs_->make< TH1D >( "deltaR_cutDeltaR", "deltaR_cutDeltaR", 50, 0., 5. );
		histos1D_[ "deltaR_cutDeltaR" ]->Sumw2();
		histos1D_[ "cosThetaStar1_cutDeltaR" ] = fs_->make< TH1D >( "cosThetaStar1_cutDeltaR", "cosThetaStar1_cutDeltaR", 10, 0., 1. );
		histos1D_[ "cosThetaStar1_cutDeltaR" ]->Sumw2();
		histos1D_[ "cosThetaStar2_cutDeltaR" ] = fs_->make< TH1D >( "cosThetaStar2_cutDeltaR", "cosThetaStar2_cutDeltaR", 10, 0., 1. );
		histos1D_[ "cosThetaStar2_cutDeltaR" ]->Sumw2();

		histos1D_[ "jet1Pt_cutDEta" ] = fs_->make< TH1D >( "jet1Pt_cutDEta", "jet1Pt_cutDEta", 100, 0., 1000. );
		histos1D_[ "jet1Pt_cutDEta" ]->Sumw2();
		histos1D_[ "jet2Pt_cutDEta" ] = fs_->make< TH1D >( "jet2Pt_cutDEta", "jet2Pt_cutDEta", 100, 0., 1000. );
		histos1D_[ "jet2Pt_cutDEta" ]->Sumw2();
		histos1D_[ "jet3Pt_cutDEta" ] = fs_->make< TH1D >( "jet3Pt_cutDEta", "jet3Pt_cutDEta", 100, 0., 1000. );
		histos1D_[ "jet3Pt_cutDEta" ]->Sumw2();
		histos1D_[ "jet4Pt_cutDEta" ] = fs_->make< TH1D >( "jet4Pt_cutDEta", "jet4Pt_cutDEta", 100, 0., 1000. );
		histos1D_[ "jet4Pt_cutDEta" ]->Sumw2();
		histos1D_[ "jetNum_cutDEta" ] = fs_->make< TH1D >( "jetNum_cutDEta", "jetNum_cutDEta", 10, 0., 10. );
		histos1D_[ "jetNum_cutDEta" ]->Sumw2();
		histos1D_[ "HT_cutDEta" ] = fs_->make< TH1D >( "HT_cutDEta", "HT_cutDEta", 300, 0., 3000. );
		histos1D_[ "HT_cutDEta" ]->Sumw2();
		histos1D_[ "jet1QGL_cutDEta" ] = fs_->make< TH1D >( "jet1QGL_cutDEta", "jet1QGL_cutDEta", 10, 0., 1. );
		histos1D_[ "jet1QGL_cutDEta" ]->Sumw2();
		histos1D_[ "jet2QGL_cutDEta" ] = fs_->make< TH1D >( "jet2QGL_cutDEta", "jet2QGL_cutDEta", 10, 0., 1. );
		histos1D_[ "jet2QGL_cutDEta" ]->Sumw2();
		histos1D_[ "jet3QGL_cutDEta" ] = fs_->make< TH1D >( "jet3QGL_cutDEta", "jet3QGL_cutDEta", 10, 0., 1. );
		histos1D_[ "jet3QGL_cutDEta" ]->Sumw2();
		histos1D_[ "jet4QGL_cutDEta" ] = fs_->make< TH1D >( "jet4QGL_cutDEta", "jet4QGL_cutDEta", 10, 0., 1. );
		histos1D_[ "jet4QGL_cutDEta" ]->Sumw2();
		histos1D_[ "massAve_cutDEta" ] = fs_->make< TH1D >( "massAve_cutDEta", "massAve_cutDEta", 200, 0., 2000. );
		histos1D_[ "massAve_cutDEta" ]->Sumw2();
		histos1D_[ "massRes_cutDEta" ] = fs_->make< TH1D >( "massRes_cutDEta", "massRes_cutDEta", 50, 0., 2. );
		histos1D_[ "massRes_cutDEta" ]->Sumw2();
		histos1D_[ "deltaEta_cutDEta" ] = fs_->make< TH1D >( "deltaEta_cutDEta", "deltaEta_cutDEta", 50, 0., 10. );
		histos1D_[ "deltaEta_cutDEta" ]->Sumw2();
		histos1D_[ "minDeltaR_cutDEta" ] = fs_->make< TH1D >( "minDeltaR_cutDEta", "minDeltaR_cutDEta", 50, 0., 5. );
		histos1D_[ "minDeltaR_cutDEta" ]->Sumw2();
		histos2D_[ "dijetsEta_cutDEta" ] = fs_->make< TH2D >( "dijetsEta_cutDEta", "dijetsEta_cutDEta", 48, -3., 3., 48, -3., 3. );
		histos2D_[ "dijetsEta_cutDEta" ]->Sumw2();
		histos1D_[ "deltaR_cutDEta" ] = fs_->make< TH1D >( "deltaR_cutDEta", "deltaR_cutDEta", 50, 0., 5. );
		histos1D_[ "deltaR_cutDEta" ]->Sumw2();
		histos1D_[ "cosThetaStar1_cutDEta" ] = fs_->make< TH1D >( "cosThetaStar1_cutDEta", "cosThetaStar1_cutDEta", 10, 0., 1. );
		histos1D_[ "cosThetaStar1_cutDEta" ]->Sumw2();
		histos1D_[ "cosThetaStar2_cutDEta" ] = fs_->make< TH1D >( "cosThetaStar2_cutDEta", "cosThetaStar2_cutDEta", 10, 0., 1. );
		histos1D_[ "cosThetaStar2_cutDEta" ]->Sumw2();

		histos1D_[ "jet1Pt_cutMassPairing" ] = fs_->make< TH1D >( "jet1Pt_cutMassPairing", "jet1Pt_cutMassPairing", 100, 0., 1000. );
		histos1D_[ "jet1Pt_cutMassPairing" ]->Sumw2();
		histos1D_[ "jet2Pt_cutMassPairing" ] = fs_->make< TH1D >( "jet2Pt_cutMassPairing", "jet2Pt_cutMassPairing", 100, 0., 1000. );
		histos1D_[ "jet2Pt_cutMassPairing" ]->Sumw2();
		histos1D_[ "jet3Pt_cutMassPairing" ] = fs_->make< TH1D >( "jet3Pt_cutMassPairing", "jet3Pt_cutMassPairing", 100, 0., 1000. );
		histos1D_[ "jet3Pt_cutMassPairing" ]->Sumw2();
		histos1D_[ "jet4Pt_cutMassPairing" ] = fs_->make< TH1D >( "jet4Pt_cutMassPairing", "jet4Pt_cutMassPairing", 100, 0., 1000. );
		histos1D_[ "jet4Pt_cutMassPairing" ]->Sumw2();
		histos1D_[ "jetNum_cutMassPairing" ] = fs_->make< TH1D >( "jetNum_cutMassPairing", "jetNum_cutMassPairing", 10, 0., 10. );
		histos1D_[ "jetNum_cutMassPairing" ]->Sumw2();
		histos1D_[ "HT_cutMassPairing" ] = fs_->make< TH1D >( "HT_cutMassPairing", "HT_cutMassPairing", 300, 0., 3000. );
		histos1D_[ "HT_cutMassPairing" ]->Sumw2();
		histos1D_[ "jet1QGL_cutMassPairing" ] = fs_->make< TH1D >( "jet1QGL_cutMassPairing", "jet1QGL_cutMassPairing", 10, 0., 1. );
		histos1D_[ "jet1QGL_cutMassPairing" ]->Sumw2();
		histos1D_[ "jet2QGL_cutMassPairing" ] = fs_->make< TH1D >( "jet2QGL_cutMassPairing", "jet2QGL_cutMassPairing", 10, 0., 1. );
		histos1D_[ "jet2QGL_cutMassPairing" ]->Sumw2();
		histos1D_[ "jet3QGL_cutMassPairing" ] = fs_->make< TH1D >( "jet3QGL_cutMassPairing", "jet3QGL_cutMassPairing", 10, 0., 1. );
		histos1D_[ "jet3QGL_cutMassPairing" ]->Sumw2();
		histos1D_[ "jet4QGL_cutMassPairing" ] = fs_->make< TH1D >( "jet4QGL_cutMassPairing", "jet4QGL_cutMassPairing", 10, 0., 1. );
		histos1D_[ "jet4QGL_cutMassPairing" ]->Sumw2();
		histos1D_[ "massAve_cutMassPairing" ] = fs_->make< TH1D >( "massAve_cutMassPairing", "massAve_cutMassPairing", 200, 0., 2000. );
		histos1D_[ "massAve_cutMassPairing" ]->Sumw2();
		histos1D_[ "massRes_cutMassPairing" ] = fs_->make< TH1D >( "massRes_cutMassPairing", "massRes_cutMassPairing", 50, 0., 2. );
		histos1D_[ "massRes_cutMassPairing" ]->Sumw2();
		histos1D_[ "deltaEta_cutMassPairing" ] = fs_->make< TH1D >( "deltaEta_cutMassPairing", "deltaEta_cutMassPairing", 50, 0., 10. );
		histos1D_[ "deltaEta_cutMassPairing" ]->Sumw2();
		histos1D_[ "minDeltaR_cutMassPairing" ] = fs_->make< TH1D >( "minDeltaR_cutMassPairing", "minDeltaR_cutMassPairing", 50, 0., 5. );
		histos1D_[ "minDeltaR_cutMassPairing" ]->Sumw2();
		histos2D_[ "dijetsEta_cutMassPairing" ] = fs_->make< TH2D >( "dijetsEta_cutMassPairing", "dijetsEta_cutMassPairing", 48, -3., 3., 48, -3., 3. );
		histos2D_[ "dijetsEta_cutMassPairing" ]->Sumw2();
		histos1D_[ "deltaR_cutMassPairing" ] = fs_->make< TH1D >( "deltaR_cutMassPairing", "deltaR_cutMassPairing", 50, 0., 5. );
		histos1D_[ "deltaR_cutMassPairing" ]->Sumw2();
		histos1D_[ "cosThetaStar1_cutMassPairing" ] = fs_->make< TH1D >( "cosThetaStar1_cutMassPairing", "cosThetaStar1_cutMassPairing", 10, 0., 1. );
		histos1D_[ "cosThetaStar1_cutMassPairing" ]->Sumw2();
		histos1D_[ "cosThetaStar2_cutMassPairing" ] = fs_->make< TH1D >( "cosThetaStar2_cutMassPairing", "cosThetaStar2_cutMassPairing", 10, 0., 1. );
		histos1D_[ "cosThetaStar2_cutMassPairing" ]->Sumw2();


		histos1D_[ "jet1Pt_cutCosTheta" ] = fs_->make< TH1D >( "jet1Pt_cutCosTheta", "jet1Pt_cutCosTheta", 100, 0., 1000. );
		histos1D_[ "jet1Pt_cutCosTheta" ]->Sumw2();
		histos1D_[ "jet2Pt_cutCosTheta" ] = fs_->make< TH1D >( "jet2Pt_cutCosTheta", "jet2Pt_cutCosTheta", 100, 0., 1000. );
		histos1D_[ "jet2Pt_cutCosTheta" ]->Sumw2();
		histos1D_[ "jet3Pt_cutCosTheta" ] = fs_->make< TH1D >( "jet3Pt_cutCosTheta", "jet3Pt_cutCosTheta", 100, 0., 1000. );
		histos1D_[ "jet3Pt_cutCosTheta" ]->Sumw2();
		histos1D_[ "jet4Pt_cutCosTheta" ] = fs_->make< TH1D >( "jet4Pt_cutCosTheta", "jet4Pt_cutCosTheta", 100, 0., 1000. );
		histos1D_[ "jet4Pt_cutCosTheta" ]->Sumw2();
		histos1D_[ "jetNum_cutCosTheta" ] = fs_->make< TH1D >( "jetNum_cutCosTheta", "jetNum_cutCosTheta", 10, 0., 10. );
		histos1D_[ "jetNum_cutCosTheta" ]->Sumw2();
		histos1D_[ "HT_cutCosTheta" ] = fs_->make< TH1D >( "HT_cutCosTheta", "HT_cutCosTheta", 300, 0., 3000. );
		histos1D_[ "HT_cutCosTheta" ]->Sumw2();
		histos1D_[ "jet1QGL_cutCosTheta" ] = fs_->make< TH1D >( "jet1QGL_cutCosTheta", "jet1QGL_cutCosTheta", 10, 0., 1. );
		histos1D_[ "jet1QGL_cutCosTheta" ]->Sumw2();
		histos1D_[ "jet2QGL_cutCosTheta" ] = fs_->make< TH1D >( "jet2QGL_cutCosTheta", "jet2QGL_cutCosTheta", 10, 0., 1. );
		histos1D_[ "jet2QGL_cutCosTheta" ]->Sumw2();
		histos1D_[ "jet3QGL_cutCosTheta" ] = fs_->make< TH1D >( "jet3QGL_cutCosTheta", "jet3QGL_cutCosTheta", 10, 0., 1. );
		histos1D_[ "jet3QGL_cutCosTheta" ]->Sumw2();
		histos1D_[ "jet4QGL_cutCosTheta" ] = fs_->make< TH1D >( "jet4QGL_cutCosTheta", "jet4QGL_cutCosTheta", 10, 0., 1. );
		histos1D_[ "jet4QGL_cutCosTheta" ]->Sumw2();
		histos1D_[ "massAve_cutCosTheta" ] = fs_->make< TH1D >( "massAve_cutCosTheta", "massAve_cutCosTheta", 200, 0., 2000. );
		histos1D_[ "massAve_cutCosTheta" ]->Sumw2();
		histos1D_[ "massRes_cutCosTheta" ] = fs_->make< TH1D >( "massRes_cutCosTheta", "massRes_cutCosTheta", 50, 0., 2. );
		histos1D_[ "massRes_cutCosTheta" ]->Sumw2();
		histos1D_[ "deltaEta_cutCosTheta" ] = fs_->make< TH1D >( "deltaEta_cutCosTheta", "deltaEta_cutCosTheta", 50, 0., 10. );
		histos1D_[ "deltaEta_cutCosTheta" ]->Sumw2();
		histos1D_[ "minDeltaR_cutCosTheta" ] = fs_->make< TH1D >( "minDeltaR_cutCosTheta", "minDeltaR_cutCosTheta", 50, 0., 5. );
		histos1D_[ "minDeltaR_cutCosTheta" ]->Sumw2();
		histos2D_[ "dijetsEta_cutCosTheta" ] = fs_->make< TH2D >( "dijetsEta_cutCosTheta", "dijetsEta_cutCosTheta", 48, -3., 3., 48, -3., 3. );
		histos2D_[ "dijetsEta_cutCosTheta" ]->Sumw2();
		histos1D_[ "deltaR_cutCosTheta" ] = fs_->make< TH1D >( "deltaR_cutCosTheta", "deltaR_cutCosTheta", 50, 0., 5. );
		histos1D_[ "deltaR_cutCosTheta" ]->Sumw2();
		histos1D_[ "cosThetaStar1_cutCosTheta" ] = fs_->make< TH1D >( "cosThetaStar1_cutCosTheta", "cosThetaStar1_cutCosTheta", 10, 0., 1. );
		histos1D_[ "cosThetaStar1_cutCosTheta" ]->Sumw2();
		histos1D_[ "cosThetaStar2_cutCosTheta" ] = fs_->make< TH1D >( "cosThetaStar2_cutCosTheta", "cosThetaStar2_cutCosTheta", 10, 0., 1. );
		histos1D_[ "cosThetaStar2_cutCosTheta" ]->Sumw2();
	}

	cutLabels.push_back("Processed");
	cutLabels.push_back("Trigger");
	cutLabels.push_back("4Jets");
	cutLabels.push_back("BestPair");
	cutLabels.push_back("MassRes");
	cutLabels.push_back("Delta");
	cutLabels.push_back("EtaBand");
	cutLabels.push_back("DeltaR");
	cutLabels.push_back("CosTheta");
	cutLabels.push_back("DEta");
	cutLabels.push_back("MassPairing");
	histos1D_[ "hcutflow" ] = fs_->make< TH1D >("cutflow","cut flow", cutLabels.size(), 0.5, cutLabels.size() +0.5 );
	histos1D_[ "hcutflow" ]->Sumw2();
	for( const string &ivec : cutLabels ) cutmap[ ivec ] = 0;
}

// ------------ method called once each job just after ending the event loop  ------------
void RUNAnalysis::endJob() {

	int ibin = 1;
	for( const string &ivec : cutLabels ) {
		histos1D_["hcutflow"]->SetBinContent( ibin, cutmap[ ivec ] );
		histos1D_["hcutflow"]->GetXaxis()->SetBinLabel( ibin, ivec.c_str() );
		ibin++;
	}

}

void RUNAnalysis::clearVariables() {

	jetsPt->clear();
	jetsEta->clear();
	jetsPhi->clear();
	jetsE->clear();

}

void RUNAnalysis::fillDescriptions(edm::ConfigurationDescriptions & descriptions) {

	edm::ParameterSetDescription desc;

	desc.add<double>("cutMassRes", 1);
	desc.add<double>("cutDelta", 1);
	desc.add<double>("cutEtaBand", 1);
	desc.add<double>("cutHT", 1);
	desc.add<double>("cutCosThetaStar", 1);
	desc.add<double>("cutDeltaR", 1);
	desc.add<double>("scale", 1);
	desc.add<bool>("bjSample", false);
	desc.add<bool>("mkTree", false);
	desc.add<bool>("isData", false);
	desc.add<string>("dataPUFile", "../data/PileupData2015D_JSON_10-23-2015.root");
	vector<string> HLTPass;
	HLTPass.push_back("HLT_PFHT800");
	desc.add<vector<string>>("triggerPass",	HLTPass);

	desc.add<InputTag>("Lumi", 	InputTag("eventInfo:evtInfoLumiBlock"));
	desc.add<InputTag>("Run", 	InputTag("eventInfo:evtInfoRunNumber"));
	desc.add<InputTag>("Event", 	InputTag("eventInfo:evtInfoEventNumber"));
	desc.add<InputTag>("bunchCross", 	InputTag("eventUserData:puBX"));
	desc.add<InputTag>("puNumInt", 	InputTag("eventUserData:puNInt"));
	desc.add<InputTag>("trueNInt", 	InputTag("eventUserData:puNtrueInt"));
	desc.add<InputTag>("jetPt", 	InputTag("jetsAK4:jetAK4Pt"));
	desc.add<InputTag>("jetEta", 	InputTag("jetsAK4:jetAK4Eta"));
	desc.add<InputTag>("jetPhi", 	InputTag("jetsAK4:jetAK4Phi"));
	desc.add<InputTag>("jetE", 	InputTag("jetsAK4:jetAK4E"));
	desc.add<InputTag>("jetQGL", 	InputTag("jetsAK4:jetAK4QGL"));
	desc.add<InputTag>("jetMass", 	InputTag("jetsAK4:jetAK4Mass"));
	desc.add<InputTag>("jetCSV", 	InputTag("jetsAK4:jetAK4CSV"));
	desc.add<InputTag>("jetCSVV1", 	InputTag("jetsAK4:jetAK4CSVV1"));
	desc.add<InputTag>("NPV", 	InputTag("eventUserData:npv"));
	desc.add<InputTag>("metPt", 	InputTag("met:metPt"));
	// JetID
	desc.add<InputTag>("jecFactor", 		InputTag("jetsAK4:jetAK4jecFactor0"));
	desc.add<InputTag>("neutralHadronEnergy", 	InputTag("jetsAK4:jetAK4neutralHadronEnergy"));
	desc.add<InputTag>("neutralEmEnergy", 		InputTag("jetsAK4:jetAK4neutralEmEnergy"));
	desc.add<InputTag>("chargedEmEnergy", 		InputTag("jetsAK4:jetAK4chargedEmEnergy"));
	desc.add<InputTag>("muonEnergy", 		InputTag("jetsAK4:jetAK4MuonEnergy"));
	desc.add<InputTag>("chargedHadronEnergy", 	InputTag("jetsAK4:jetAK4chargedHadronEnergy"));
	desc.add<InputTag>("chargedHadronMultiplicity",	InputTag("jetsAK4:jetAK4ChargedHadronMultiplicity"));
	desc.add<InputTag>("neutralHadronMultiplicity",	InputTag("jetsAK4:jetAK4neutralHadronMultiplicity"));
	desc.add<InputTag>("chargedMultiplicity", 	InputTag("jetsAK4:jetAK4chargedMultiplicity"));
	// Trigger
	desc.add<InputTag>("triggerBit",		InputTag("TriggerUserData:triggerBitTree"));
	desc.add<InputTag>("triggerName",		InputTag("TriggerUserData:triggerNameTree"));
	descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(RUNAnalysis);
