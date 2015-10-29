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
      double cutMassRes;
      double cutDelta;
      double cutEtaBand;
      double cutJetPt;
      double cutHT;
      vector<string> triggerPass;

      vector<float> *jetsPt = new std::vector<float>();
      vector<float> *jetsEta = new std::vector<float>();
      vector<float> *jetsPhi = new std::vector<float>();
      vector<float> *jetsE = new std::vector<float>();
      ULong64_t event = 0;
      int numJets = 0, numPV = 0;
      unsigned int lumi = 0, run=0;
      float HT = 0, mass1 = -999, mass2 = -999, avgMass = -999, delta1 = -999, delta2 = -999, massRes = -999, eta1 = -999, eta2 = -999, deltaEta = -999, puWeight = -999;

      EDGetTokenT<vector<float>> jetPt_;
      EDGetTokenT<vector<float>> jetEta_;
      EDGetTokenT<vector<float>> jetPhi_;
      EDGetTokenT<vector<float>> jetE_;
      EDGetTokenT<vector<float>> jetMass_;
      EDGetTokenT<vector<float>> jetCSV_;
      EDGetTokenT<vector<float>> jetCSVV1_;
      EDGetTokenT<int> NPV_;
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
	jetMass_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetMass"))),
	jetCSV_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetCSV"))),
	jetCSVV1_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetCSVV1"))),
	NPV_(consumes<int>(iConfig.getParameter<InputTag>("NPV"))),
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
	bjSample 	= iConfig.getParameter<bool>("bjSample");
	mkTree 		= iConfig.getParameter<bool>("mkTree");
	cutMassRes      = iConfig.getParameter<double>     ("cutMassRes");
	cutDelta        = iConfig.getParameter<double>     ("cutDelta");
	cutEtaBand      = iConfig.getParameter<double>     ("cutEtaBand");
	cutJetPt	= iConfig.getParameter<double>     ("cutJetPt");
	cutHT 		= iConfig.getParameter<double>("cutHT");
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
	
	cutmap["Processed"] += 1;

	int numPV = *NPV;
	//vector< JETtype > JETS;
	vector< TLorentzVector > JETS;
	vector< float > tmpTriggerMass;
	int numJets = 0;
	double rawHT = 0;
	//bool bTagCSV = 0;
	HT = 0;

	for (size_t i = 0; i < jetPt->size(); i++) {

		if( TMath::Abs( (*jetEta)[i] ) > 2.4 ) continue;

		rawHT += (*jetPt)[i];
		histos1D_[ "rawJetPt" ]->Fill( (*jetPt)[i] , puWeight );

		bool idL = loosejetID( (*jetE)[i], (*jecFactor)[i], (*neutralHadronEnergy)[i], (*neutralEmEnergy)[i], (*chargedHadronEnergy)[i], (*chargedEmEnergy)[i], (*chargedHadronMultiplicity)[i], (*neutralHadronMultiplicity)[i], (*chargedMultiplicity)[i] ); 

		if( ( (*jetPt)[i] > 40. ) && idL ) { 

			HT += (*jetPt)[i];
			++numJets;

			TLorentzVector tmpJet;
			tmpJet.SetPtEtaPhiE( (*jetPt)[i], (*jetEta)[i], (*jetPhi)[i], (*jetE)[i] );

			//if ( (*jetCSV)[i] > 0.244 ) bTagCSV = 1; 	// CSVL
			//if ( (*jetCSV)[i] > 0.679 ) bTagCSV = 1; 	// CSVM
			//if ( (*jetCSVV1)[i] > 0.405 ) bTagCSV = 1; 	// CSVV1L
			//if ( (*jetCSVV1)[i] > 0.783 ) bTagCSV = 1; 	// CSVV1M

			/*JETtype tmpJET;
			tmpJET = tmpJet;
			tmpJET.mass = (*jetMass)[i];
			tmpJET.btagCSV = bTagCSV;
			JETS.push_back( tmpJET );
			*/
			JETS.push_back( tmpJet );
	   
			histos1D_[ "jetPt" ]->Fill( (*jetPt)[i] , puWeight );
			histos1D_[ "jetEta" ]->Fill( (*jetEta)[i] , puWeight );
			double jec = 1. / ( (*jecFactor)[i] * (*jetE)[i] );
			histos1D_[ "neutralHadronEnergy" ]->Fill( (*neutralHadronEnergy)[i] * jec, puWeight );
			histos1D_[ "neutralEmEnergy" ]->Fill( (*neutralEmEnergy)[i] * jec, puWeight );
			histos1D_[ "chargedHadronEnergy" ]->Fill( (*chargedHadronEnergy)[i] * jec, puWeight );
			histos1D_[ "chargedEmEnergy" ]->Fill( (*chargedEmEnergy)[i] * jec, puWeight );
			histos1D_[ "numConst" ]->Fill( (*chargedHadronMultiplicity)[i] + (*neutralHadronMultiplicity)[i], puWeight );
			histos1D_[ "chargedMultiplicity" ]->Fill( (*chargedMultiplicity)[i] * jec, puWeight );

		}
	}

	//sort(JETS.begin(), JETS.end(), [](const JETtype &p1, const JETtype &p2) { TLorentzVector tmpP1, tmpP2; tmpP1 = p1; tmpP2 = p2;  return tmpP1.M() > tmpP2.M(); }); 
	histos1D_[ "jetNum" ]->Fill( numJets, puWeight );
	histos1D_[ "NPV" ]->Fill( numPV, puWeight );
	histos1D_[ "NPV_NOPUWeight" ]->Fill( numPV );
	if ( HT > 0 ) histos1D_[ "HT" ]->Fill( HT , puWeight );
	if ( rawHT > 0 ) histos1D_[ "rawHT" ]->Fill( rawHT , puWeight );

	clearVariables();

	if ( ORTriggers ) {
		
		cutmap["Trigger"] += 1;
		histos1D_[ "HT_cutTrigger" ]->Fill( HT , puWeight );
		histos1D_[ "NPV_cutTrigger" ]->Fill( numPV, puWeight );
		histos1D_[ "jetNum_cutTrigger" ]->Fill( numJets, puWeight );
		for (int i = 0; i < numJets; i++) {
			histos1D_[ "jetPt_cutTrigger" ]->Fill( JETS[i].Pt(), puWeight );
			histos1D_[ "jetEta_cutTrigger" ]->Fill( JETS[i].Eta(), puWeight );
			jetsPt->push_back( JETS[i].Pt() );
			jetsEta->push_back( JETS[i].Eta() );
			jetsPhi->push_back( JETS[i].Phi() );
			jetsE->push_back( JETS[i].E() );
		}
		event		= *ievent;
		run		= *Run;
		lumi		= *Lumi;
		if( numJets > 3 ) { 
			
			cutmap["4Jets"] += 1;
			histos1D_[ "HT_cut4Jets" ]->Fill( HT, puWeight );
			histos1D_[ "jetNum_cut4Jets" ]->Fill( numJets, puWeight );
			histos1D_[ "jet1Pt_cut4Jets" ]->Fill( JETS[0].Pt(), puWeight );
			histos1D_[ "jet2Pt_cut4Jets" ]->Fill( JETS[1].Pt(), puWeight );
			histos1D_[ "jet3Pt_cut4Jets" ]->Fill( JETS[2].Pt(), puWeight );
			histos1D_[ "jet4Pt_cut4Jets" ]->Fill( JETS[3].Pt(), puWeight );

			if( ( numJets == 4 ) && ( JETS[3].Pt() > cutJetPt ) && ( HT > cutHT ) ){
				
				cutmap["4JetPt"] += 1;
				histos1D_[ "HT_cutHT" ]->Fill( HT, puWeight );
				histos1D_[ "jetNum_cutHT" ]->Fill( numJets, puWeight );
				histos1D_[ "jet1Pt_cutHT" ]->Fill( JETS[0].Pt(), puWeight );
				histos1D_[ "jet2Pt_cutHT" ]->Fill( JETS[1].Pt(), puWeight );
				histos1D_[ "jet3Pt_cutHT" ]->Fill( JETS[2].Pt(), puWeight );
				histos1D_[ "jet4Pt_cutHT" ]->Fill( JETS[3].Pt(), puWeight );

		
				vector<double> tmpDijetR;
				double dR12 = JETS[0].DeltaR( JETS[1] );
				double dR34 = JETS[2].DeltaR( JETS[3] );
				double dijetR1234 = abs( dR12 - 1 )  + abs( dR34 - 1 );
				tmpDijetR.push_back( dijetR1234 );

				double dR13 = JETS[0].DeltaR( JETS[2] );
				double dR24 = JETS[1].DeltaR( JETS[3] );
				double dijetR1324 = abs( dR13 - 1 )  + abs( dR24 - 1 );
				tmpDijetR.push_back( dijetR1324 );

				double dR14 = JETS[0].DeltaR( JETS[3] );
				double dR23 = JETS[1].DeltaR( JETS[2] );
				double dijetR1423 = abs( dR14 - 1 )  + abs( dR23 - 1 );
				tmpDijetR.push_back( dijetR1423 );

				//LogWarning("test") << min_element(tmpDijetR.begin(), tmpDijetR.end()) - tmpDijetR.begin()  << " " << dijetR1234 << " " << dijetR1324 << " " << dijetR1423 ;
				int minDeltaR = min_element(tmpDijetR.begin(), tmpDijetR.end()) - tmpDijetR.begin();
				TLorentzVector j1, j2, j3, j4;

				if( minDeltaR == 0 ){
					j1 = JETS[0];
					j2 = JETS[1];
					j3 = JETS[2];
					j4 = JETS[3];
				} else if ( minDeltaR == 1 ) {
					j1 = JETS[0];
					j2 = JETS[2];
					j3 = JETS[1];
					j4 = JETS[3];
				} else if ( minDeltaR == 2 ) {
					j1 = JETS[0];
					j2 = JETS[3];
					j3 = JETS[1];
					j4 = JETS[2];
				}


				mass1 = ( j1 + j2 ).M();
				mass2 = ( j3 + j4 ).M();
				avgMass = ( mass1 + mass2 ) / 2;
				delta1 = ( j1.Pt() + j2.Pt() ) - avgMass;
				delta2 = ( j3.Pt() + j4.Pt() ) - avgMass;
				massRes = TMath::Abs( mass1 - mass2 ) / avgMass;
				eta1 = ( j1 + j2 ).Eta();
				eta2 = ( j3 + j4 ).Eta();
				deltaEta = TMath::Abs( eta1 - eta2 );

				if ( mkTree ) {
					RUNAtree->Fill();
				} else {
					histos1D_[ "jet4Pt_cutBestPair" ]->Fill( j4.Pt(), puWeight );
					histos1D_[ "massAve_cutBestPair" ]->Fill( avgMass, puWeight );
					histos1D_[ "massRes_cutBestPair" ]->Fill( massRes, puWeight );
					histos1D_[ "deltaEta_cutBestPair" ]->Fill( deltaEta, puWeight );
					histos1D_[ "minDeltaR_cutBestPair" ]->Fill( minDeltaR , puWeight );
					histos1D_[ "HT_cutBestPair" ]->Fill( HT, puWeight );
					histos2D_[ "deltavsMassAve_cutBestPair" ]->Fill( avgMass, delta1 , puWeight );
					histos2D_[ "deltavsMassAve_cutBestPair" ]->Fill( avgMass, delta2 , puWeight );
					histos2D_[ "dijetsEta_cutBestPair" ]->Fill( eta1, eta2, puWeight );

					if ( ( delta1 > cutDelta ) && ( delta2  > cutDelta ) ) {
						cutmap["Delta"] += 1;
						histos1D_[ "HT_cutDelta" ]->Fill( HT, puWeight );
						histos1D_[ "jetNum_cutDelta" ]->Fill( numJets, puWeight );
						histos1D_[ "jet1Pt_cutDelta" ]->Fill( JETS[0].Pt(), puWeight );
						histos1D_[ "jet2Pt_cutDelta" ]->Fill( JETS[1].Pt(), puWeight );
						histos1D_[ "jet3Pt_cutDelta" ]->Fill( JETS[2].Pt(), puWeight );
						histos1D_[ "jet4Pt_cutDelta" ]->Fill( JETS[3].Pt(), puWeight );
						histos1D_[ "massAve_cutDelta" ]->Fill( avgMass, puWeight );
						histos1D_[ "massRes_cutDelta" ]->Fill( massRes, puWeight );
						histos1D_[ "deltaEta_cutDelta" ]->Fill( deltaEta, puWeight );
						histos1D_[ "minDeltaR_cutDelta" ]->Fill( minDeltaR , puWeight );
						histos2D_[ "deltavsMassAve_cutDelta" ]->Fill( avgMass, delta1 , puWeight );
						histos2D_[ "deltavsMassAve_cutDelta" ]->Fill( avgMass, delta2 , puWeight );
						histos2D_[ "dijetsEta_cutDelta" ]->Fill( eta1, eta2, puWeight );

						if ( massRes < cutMassRes ) { 
							cutmap["MassRes"] += 1;
							histos1D_[ "HT_cutMassRes" ]->Fill( HT, puWeight );
							histos1D_[ "jetNum_cutMassRes" ]->Fill( numJets, puWeight );
							histos1D_[ "jet1Pt_cutMassRes" ]->Fill( JETS[0].Pt(), puWeight );
							histos1D_[ "jet2Pt_cutMassRes" ]->Fill( JETS[1].Pt(), puWeight );
							histos1D_[ "jet3Pt_cutMassRes" ]->Fill( JETS[2].Pt(), puWeight );
							histos1D_[ "jet4Pt_cutMassRes" ]->Fill( JETS[3].Pt(), puWeight );
							histos1D_[ "massAve_cutMassRes" ]->Fill( avgMass, puWeight );
							histos1D_[ "massRes_cutMassRes" ]->Fill( massRes, puWeight );
							histos1D_[ "deltaEta_cutMassRes" ]->Fill( deltaEta, puWeight );
							histos1D_[ "minDeltaR_cutMassRes" ]->Fill( minDeltaR , puWeight );
							histos2D_[ "deltavsMassAve_cutMassRes" ]->Fill( avgMass, delta1 , puWeight );
							histos2D_[ "deltavsMassAve_cutMassRes" ]->Fill( avgMass, delta2 , puWeight );
							histos2D_[ "dijetsEta_cutMassRes" ]->Fill( eta1, eta2, puWeight );
						
							if ( TMath::Abs(eta1 - eta2) <  cutEtaBand ) {
								cutmap["EtaBand"] += 1;
								histos1D_[ "HT_cutEtaBand" ]->Fill( HT, puWeight );
								histos1D_[ "jetNum_cutEtaBand" ]->Fill( numJets, puWeight );
								histos1D_[ "jet1Pt_cutEtaBand" ]->Fill( JETS[0].Pt(), puWeight );
								histos1D_[ "jet2Pt_cutEtaBand" ]->Fill( JETS[1].Pt(), puWeight );
								histos1D_[ "jet3Pt_cutEtaBand" ]->Fill( JETS[2].Pt(), puWeight );
								histos1D_[ "jet4Pt_cutEtaBand" ]->Fill( JETS[3].Pt(), puWeight );
								histos1D_[ "massAve_cutEtaBand" ]->Fill( avgMass, puWeight );
								histos1D_[ "massRes_cutEtaBand" ]->Fill( massRes, puWeight );
								histos1D_[ "deltaEta_cutEtaBand" ]->Fill( deltaEta, puWeight );
								histos1D_[ "minEtaBandR_cutEtaBand" ]->Fill( minDeltaR , puWeight );
								histos2D_[ "deltavsMassAve_cutEtaBand" ]->Fill( avgMass, delta1 , puWeight );
								histos2D_[ "deltavsMassAve_cutEtaBand" ]->Fill( avgMass, delta2 , puWeight );
								histos2D_[ "dijetsEta_cutEtaBand" ]->Fill( eta1, eta2, puWeight );
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
	histos1D_[ "NPV_cutTrigger" ] = fs_->make< TH1D >( "NPV_cutTrigger", "NPV_cutTrigger", 80, 0., 80. );
	histos1D_[ "NPV_cutTrigger" ]->Sumw2();

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

	histos1D_[ "jet1Pt_cutHT" ] = fs_->make< TH1D >( "jet1Pt_cutHT", "jet1Pt_cutHT", 100, 0., 1000. );
	histos1D_[ "jet1Pt_cutHT" ]->Sumw2();
	histos1D_[ "jet2Pt_cutHT" ] = fs_->make< TH1D >( "jet2Pt_cutHT", "jet2Pt_cutHT", 100, 0., 1000. );
	histos1D_[ "jet2Pt_cutHT" ]->Sumw2();
	histos1D_[ "jet3Pt_cutHT" ] = fs_->make< TH1D >( "jet3Pt_cutHT", "jet3Pt_cutHT", 100, 0., 1000. );
	histos1D_[ "jet3Pt_cutHT" ]->Sumw2();
	histos1D_[ "jet4Pt_cutHT" ] = fs_->make< TH1D >( "jet4Pt_cutHT", "jet4Pt_cutHT", 100, 0., 1000. );
	histos1D_[ "jet4Pt_cutHT" ]->Sumw2();
	histos1D_[ "jetNum_cutHT" ] = fs_->make< TH1D >( "jetNum_cutHT", "jetNum_cutHT", 10, 0., 10. );
	histos1D_[ "jetNum_cutHT" ]->Sumw2();
	histos1D_[ "HT_cutHT" ] = fs_->make< TH1D >( "HT_cutHT", "HT_cutHT", 300, 0., 3000. );
	histos1D_[ "HT_cutHT" ]->Sumw2();


	if (mkTree) {
		RUNAtree = fs_->make< TTree >("RUNATree", "RUNATree"); 
		RUNAtree->Branch( "run", &run, "run/I" );
		RUNAtree->Branch( "lumi", &lumi, "lumi/I" );
		RUNAtree->Branch( "event", &event, "event/I" );
		RUNAtree->Branch( "numJets", &numJets, "numJets/I" );
		RUNAtree->Branch( "numPV", &numPV, "numPV/I" );
		RUNAtree->Branch( "puWeight", &puWeight, "puWeight/F" );
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
		RUNAtree->Branch( "jetsPt", "vector<float>", &jetsPt);
		RUNAtree->Branch( "jetsEta", "vector<float>", &jetsEta);
		RUNAtree->Branch( "jetsPhi", "vector<float>", &jetsPhi);
		RUNAtree->Branch( "jetsE", "vector<float>", &jetsE);
	} else {
		histos1D_[ "jet4Pt_cutBestPair" ] = fs_->make< TH1D >( "jet4Pt_cutBestPair", "jet4Pt_cutBestPair", 100, 0., 1000. );
		histos1D_[ "jet4Pt_cutBestPair" ]->Sumw2();
		histos1D_[ "massAve_cutBestPair" ] = fs_->make< TH1D >( "massAve_cutBestPair", "massAve_cutBestPair", 200, 0., 2000. );
		histos1D_[ "massAve_cutBestPair" ]->Sumw2();
		histos1D_[ "massRes_cutBestPair" ] = fs_->make< TH1D >( "massRes_cutBestPair", "massRes_cutBestPair", 50, 0., 2. );
		histos1D_[ "massRes_cutBestPair" ]->Sumw2();
		histos1D_[ "deltaEta_cutBestPair" ] = fs_->make< TH1D >( "deltaEta_cutBestPair", "deltaEta_cutBestPair", 50, 0., 10. );
		histos1D_[ "deltaEta_cutBestPair" ]->Sumw2();
		histos1D_[ "minDeltaR_cutBestPair" ] = fs_->make< TH1D >( "minDeltaR_cutBestPair", "minDeltaR_cutBestPair", 5, 0., 5. );
		histos1D_[ "minDeltaR_cutBestPair" ]->Sumw2();
		histos1D_[ "HT_cutBestPair" ] = fs_->make< TH1D >( "HT_cutBestPair", "HT_cutBestPair", 300, 0., 3000. );
		histos1D_[ "HT_cutBestPair" ]->Sumw2();
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
		histos1D_[ "minDeltaR_cutMassRes" ] = fs_->make< TH1D >( "minDeltaR_cutMassRes", "minDeltaR_cutMassRes", 5, 0., 5. );
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
		histos1D_[ "minDeltaR_cutDelta" ] = fs_->make< TH1D >( "minDeltaR_cutDelta", "minDeltaR_cutDelta", 5, 0., 5. );
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
		histos1D_[ "minEtaBandR_cutEtaBand" ] = fs_->make< TH1D >( "minEtaBandR_cutEtaBand", "minEtaBandR_cutEtaBand", 5, 0., 5. );
		histos1D_[ "minEtaBandR_cutEtaBand" ]->Sumw2();
		histos2D_[ "deltavsMassAve_cutEtaBand" ] = fs_->make< TH2D >( "deltavsMassAve_cutEtaBand", "deltavsMassAve_cutEtaBand", 200, 0., 2000.,  300, -500., 1000. );
		histos2D_[ "deltavsMassAve_cutEtaBand" ]->Sumw2();
		histos2D_[ "dijetsEta_cutEtaBand" ] = fs_->make< TH2D >( "dijetsEta_cutEtaBand", "dijetsEta_cutEtaBand", 48, -3., 3., 48, -3., 3. );
		histos2D_[ "dijetsEta_cutEtaBand" ]->Sumw2();
	}

	cutLabels.push_back("Processed");
	cutLabels.push_back("Trigger");
	cutLabels.push_back("4Jets");
	cutLabels.push_back("4JetPt");
	cutLabels.push_back("MassRes");
	cutLabels.push_back("Delta");
	cutLabels.push_back("EtaBand");
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
	desc.add<double>("cutJetPt", 1);
	desc.add<double>("cutHT", 1);
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
	desc.add<InputTag>("jetMass", 	InputTag("jetsAK4:jetAK4Mass"));
	desc.add<InputTag>("jetCSV", 	InputTag("jetsAK4:jetAK4CSV"));
	desc.add<InputTag>("jetCSVV1", 	InputTag("jetsAK4:jetAK4CSVV1"));
	desc.add<InputTag>("NPV", 	InputTag("eventUserData:npv"));
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
