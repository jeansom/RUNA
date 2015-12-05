// -*- C++ -*-
//
// Package:    RUNA/Ntuples
// Class:      RUNBoostedTriggerEfficiency
// 
/**\class RUNBoostedTriggerEfficiency RUNBoostedTriggerEfficiency.cc Ntuples/Ntuples/plugins/RUNBoostedTriggerEfficiency.cc

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

#include "RUNA/RUNAnalysis/interface/CommonVariablesStructure.h"

using namespace edm;
using namespace std;

//
// constants, enums and typedefs
//

//
// class declaration
//
class RUNBoostedTriggerEfficiency : public EDAnalyzer {
   public:
      explicit RUNBoostedTriggerEfficiency(const ParameterSet&);
      static void fillDescriptions(edm::ConfigurationDescriptions & descriptions);
      ~RUNBoostedTriggerEfficiency();

   private:
      virtual void beginJob() override;
      virtual void analyze(const Event&, const EventSetup&) override;
      virtual void endJob() override;

      //virtual void beginRun(Run const&, EventSetup const&) override;
      //virtual void endRun(Run const&, EventSetup const&) override;
      //virtual void beginLuminosityBlock(LuminosityBlock const&, EventSetup const&) override;
      //virtual void endLuminosityBlock(LuminosityBlock const&, EventSetup const&) override;

      // ----------member data ---------------------------
      Service<TFileService> fs_;
      TTree *RUNAtree;
      map< string, TH1D* > histos1D_;
      map< string, TH2D* > histos2D_;
      vector< string > cutLabels;

      bool bjSample;
      TString baseTrigger;
      //double cutTrimmedMassvalue;
      double cutHTvalue;
      double cutjet1Ptvalue;
      double cutjet2Ptvalue;
      double cutAsymvalue;
      double cutTau31value;
      double cutTau21value;
      vector<string> triggerPass;

      ULong64_t event = 0;
      int numJets = 0, numPV = 0;
      unsigned int lumi = 0, run=0;

      EDGetTokenT<vector<float>> jetAk4Pt_;
      EDGetTokenT<vector<float>> jetPt_;
      EDGetTokenT<vector<float>> jetEta_;
      EDGetTokenT<vector<float>> jetPhi_;
      EDGetTokenT<vector<float>> jetE_;
      EDGetTokenT<vector<float>> jetMass_;
      EDGetTokenT<vector<float>> jetTrimmedMass_;
      EDGetTokenT<vector<float>> jetTau1_;
      EDGetTokenT<vector<float>> jetTau2_;
      EDGetTokenT<vector<float>> jetTau3_;
      EDGetTokenT<vector<float>> jetNSubjets_;
      EDGetTokenT<vector<float>> jetSubjetIndex0_;
      EDGetTokenT<vector<float>> jetSubjetIndex1_;
      EDGetTokenT<vector<float>> jetSubjetIndex2_;
      EDGetTokenT<vector<float>> jetSubjetIndex3_;
      EDGetTokenT<vector<vector<int>>> jetKeys_;
      EDGetTokenT<vector<float>> jetCSV_;
      EDGetTokenT<vector<float>> jetCSVV1_;
      EDGetTokenT<int> NPV_;
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

      // Subjets
      EDGetTokenT<vector<float>> subjetPt_;
      EDGetTokenT<vector<float>> subjetEta_;
      EDGetTokenT<vector<float>> subjetPhi_;
      EDGetTokenT<vector<float>> subjetE_;
      EDGetTokenT<vector<float>> subjetMass_;

};

//
// static data member definitions
//

//
// constructors and destructor
//
RUNBoostedTriggerEfficiency::RUNBoostedTriggerEfficiency(const ParameterSet& iConfig):
	jetAk4Pt_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetAk4Pt"))),
	jetPt_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetPt"))),
	jetEta_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetEta"))),
	jetPhi_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetPhi"))),
	jetE_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetE"))),
	jetMass_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetMass"))),
	jetTrimmedMass_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetTrimmedMass"))),
	jetTau1_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetTau1"))),
	jetTau2_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetTau2"))),
	jetTau3_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetTau3"))),
	jetNSubjets_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetNSubjets"))),
	jetSubjetIndex0_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetSubjetIndex0"))),
	jetSubjetIndex1_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetSubjetIndex1"))),
	jetSubjetIndex2_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetSubjetIndex2"))),
	jetSubjetIndex3_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetSubjetIndex3"))),
	jetKeys_(consumes<vector<vector<int>>>(iConfig.getParameter<InputTag>("jetKeys"))),
	jetCSV_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetCSV"))),
	jetCSVV1_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetCSVV1"))),
	NPV_(consumes<int>(iConfig.getParameter<InputTag>("NPV"))),
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
	muonEnergy_(consumes<vector<float>>(iConfig.getParameter<InputTag>("muonEnergy"))),
	// Subjets
	subjetPt_(consumes<vector<float>>(iConfig.getParameter<InputTag>("subjetPt"))),
	subjetEta_(consumes<vector<float>>(iConfig.getParameter<InputTag>("subjetEta"))),
	subjetPhi_(consumes<vector<float>>(iConfig.getParameter<InputTag>("subjetPhi"))),
	subjetE_(consumes<vector<float>>(iConfig.getParameter<InputTag>("subjetE"))),
	subjetMass_(consumes<vector<float>>(iConfig.getParameter<InputTag>("subjetMass")))
{
	bjSample = iConfig.getParameter<bool>("bjSample");
	baseTrigger = iConfig.getParameter<string>("baseTrigger");
	cutjet1Ptvalue = iConfig.getParameter<double>("cutjet1Ptvalue");
	cutjet2Ptvalue = iConfig.getParameter<double>("cutjet2Ptvalue");
	cutAsymvalue = iConfig.getParameter<double>("cutAsymvalue");
	cutTau31value = iConfig.getParameter<double>("cutTau31value");
	cutTau21value = iConfig.getParameter<double>("cutTau21value");
	triggerPass = iConfig.getParameter<vector<string>>("triggerPass");
}


RUNBoostedTriggerEfficiency::~RUNBoostedTriggerEfficiency()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void RUNBoostedTriggerEfficiency::analyze(const Event& iEvent, const EventSetup& iSetup) {


	Handle<vector<float> > jetAk4Pt;
	iEvent.getByToken(jetAk4Pt_, jetAk4Pt);

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

	Handle<vector<float> > jetTrimmedMass;
	iEvent.getByToken(jetTrimmedMass_, jetTrimmedMass);

	Handle<vector<float> > jetTau1;
	iEvent.getByToken(jetTau1_, jetTau1);

	Handle<vector<float> > jetTau2;
	iEvent.getByToken(jetTau2_, jetTau2);

	Handle<vector<float> > jetTau3;
	iEvent.getByToken(jetTau3_, jetTau3);

	Handle<vector<float> > jetNSubjets;
	iEvent.getByToken(jetNSubjets_, jetNSubjets);

	Handle<vector<float> > jetSubjetIndex0;
	iEvent.getByToken(jetSubjetIndex0_, jetSubjetIndex0);

	Handle<vector<float> > jetSubjetIndex1;
	iEvent.getByToken(jetSubjetIndex1_, jetSubjetIndex1);

	Handle<vector<float> > jetSubjetIndex2;
	iEvent.getByToken(jetSubjetIndex2_, jetSubjetIndex2);

	Handle<vector<float> > jetSubjetIndex3;
	iEvent.getByToken(jetSubjetIndex3_, jetSubjetIndex3);

	Handle<vector<vector<int> > > jetKeys;
	iEvent.getByToken(jetKeys_, jetKeys);

	Handle<vector<float> > jetCSV;
	iEvent.getByToken(jetCSV_, jetCSV);

	Handle<vector<float> > jetCSVV1;
	iEvent.getByToken(jetCSVV1_, jetCSVV1);

	Handle<int> NPV;
	iEvent.getByToken(NPV_, NPV);

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

	/// Subjets
	Handle<vector<float> > subjetPt;
	iEvent.getByToken(subjetPt_, subjetPt);

	Handle<vector<float> > subjetEta;
	iEvent.getByToken(subjetEta_, subjetEta);

	Handle<vector<float> > subjetPhi;
	iEvent.getByToken(subjetPhi_, subjetPhi);

	Handle<vector<float> > subjetE;
	iEvent.getByToken(subjetE_, subjetE);

	Handle<vector<float> > subjetMass;
	iEvent.getByToken(subjetMass_, subjetMass);

	bool basedTriggerFired = checkTriggerBits( triggerName, triggerBit, baseTrigger  );
	
	vector<bool> triggersFired;
	for (size_t t = 0; t < triggerPass.size(); t++) {
		bool triggerFired = checkTriggerBits( triggerName, triggerBit, triggerPass[t] );
		triggersFired.push_back( triggerFired );
		//if ( triggerFired ) LogWarning("test") << triggerPass[t] << " " << triggerFired;
	}
	
	bool ORTriggers = !none_of(triggersFired.begin(), triggersFired.end(), [](bool v) { return v; }); 
	//if( ORTriggers ) LogWarning("OR") << std::none_of(triggersFired.begin(), triggersFired.end(), [](bool v) { return v; }); 

	/// Applying kinematic, trigger and jet ID
	vector< JETtype > JETS;
	vector< float > tmpTriggerMass;
	vector< float > tmpMass;
	bool bTagCSV = 0;
	float HT = 0;

	for (size_t i = 0; i < jetPt->size(); i++) {

		//if( TMath::Abs( (*jetEta)[i] ) > 2.4 ) continue;

		bool idL = jetID( (*jetEta)[i], (*jetE)[i], (*jecFactor)[i], (*neutralHadronEnergy)[i], (*neutralEmEnergy)[i], (*chargedHadronEnergy)[i], (*muonEnergy)[i], (*chargedEmEnergy)[i], (*chargedHadronMultiplicity)[i], (*neutralHadronMultiplicity)[i], (*chargedMultiplicity)[i] ); 

		if( (*jetPt)[i] > 150  && idL ) { 
			//LogWarning("jetInfo") << i << " " << (*jetPt)[i] << " " << (*jetEta)[i] << " " << (*jetPhi)[i] << " " << (*jetMass)[i];

			HT += (*jetPt)[i];
			++numJets;
			tmpTriggerMass.push_back( (*jetTrimmedMass)[i] );
			tmpMass.push_back( (*jetMass)[i] );


			TLorentzVector tmpJet;
			tmpJet.SetPtEtaPhiE( (*jetPt)[i], (*jetEta)[i], (*jetPhi)[i], (*jetE)[i] );

			/// Vector of zeros
			TLorentzVector tmpSubjet0, tmpSubjet1, tmpZeros;
			tmpZeros.SetPtEtaPhiE( 0, 0, 0, 0 );

			for (size_t j = 0; j < subjetPt->size(); j++) {
				if( j == (*jetSubjetIndex0)[i] ) {
					//LogWarning("subjets0") << j << " " << (*jetSubjetIndex0)[i] << " " <<  subjetPt->size() << " " << (*subjetPt)[j];
					tmpSubjet0.SetPtEtaPhiE( (*subjetPt)[j], (*subjetEta)[j], (*subjetPhi)[j], (*subjetE)[j] );
				} //else tmpSubjet0 = tmpZeros ; 
					
				if( j == (*jetSubjetIndex1)[i] ) {
					tmpSubjet1.SetPtEtaPhiE( (*subjetPt)[j], (*subjetEta)[j], (*subjetPhi)[j], (*subjetE)[j] );
				} //else tmpSubjet1 = tmpZeros ; 
			}

			//if ( (*jetCSV)[i] > 0.244 ) bTagCSV = 1; 	// CSVL
			if ( (*jetCSV)[i] > 0.679 ) bTagCSV = 1; 	// CSVM
			//if ( (*jetCSVV1)[i] > 0.405 ) bTagCSV = 1; 	// CSVV1L
			//if ( (*jetCSVV1)[i] > 0.783 ) bTagCSV = 1; 	// CSVV1M

			JETtype tmpJET;
			tmpJET.p4 = tmpJet;
			tmpJET.subjet0 = tmpSubjet0;
			tmpJET.subjet1 = tmpSubjet1;
			tmpJET.mass = (*jetMass)[i];
			tmpJET.tau1 = (*jetTau1)[i];
			tmpJET.tau2 = (*jetTau2)[i];
			tmpJET.tau3 = (*jetTau3)[i];
			tmpJET.btagCSV = bTagCSV;
			JETS.push_back( tmpJET );
	   
		}
	}

	sort(tmpTriggerMass.begin(), tmpTriggerMass.end(), [](const float p1, const float p2) { return p1 > p2; }); 
	float trimmedMass = -999;
	if ( ( tmpTriggerMass.size()> 0 ) ) trimmedMass = tmpTriggerMass[0];
	tmpTriggerMass.clear();
	
	sort(tmpMass.begin(), tmpMass.end(), [](const float p1, const float p2) { return p1 > p2; }); 
	float leadMass = -999;
	if ( ( tmpMass.size()> 0 ) ) leadMass = tmpMass[0];
	tmpMass.clear();

	if (HT > 0 ) { 
		histos2D_[ "jetMassHT_noTrigger" ]->Fill( JETS[0].mass, HT );
		histos2D_[ "jetTrimmedMassHT_noTrigger" ]->Fill( trimmedMass, HT );
	}
	if ( basedTriggerFired || triggersFired[0] ) {
		if ( basedTriggerFired && triggersFired[0] ) {
			if(JETS.size() > 0) histos2D_[ "jetMassHT_triggerOneAndTwo" ]->Fill( JETS[0].mass, HT );
			histos2D_[ "jetTrimmedMassHT_triggerOneAndTwo" ]->Fill( trimmedMass, HT );
		} else if ( basedTriggerFired ) {
			if(JETS.size() > 0) histos2D_[ "jetMassHT_triggerOne" ]->Fill( JETS[0].mass, HT );
			histos2D_[ "jetTrimmedMassHT_triggerOne" ]->Fill( trimmedMass, HT );
		} else if ( triggersFired[0] ) {
			if(JETS.size() > 0) histos2D_[ "jetMassHT_triggerTwo" ]->Fill( JETS[0].mass, HT );
			histos2D_[ "jetTrimmedMassHT_triggerTwo" ]->Fill( trimmedMass, HT );
		}
	}


	//// test ak4 
	float ak4HT = 0;
	for (size_t i = 0; i < jetAk4Pt->size(); i++) ak4HT += (*jetAk4Pt)[i];
	///////////////////

	bool cutMassAsym = 0;

	vector<TLorentzVector> jet1SubjetsTLV, jet2SubjetsTLV;

	if ( JETS.size() > 1 ) {

		// Mass average and asymmetry
		float jet1Mass = JETS[0].mass;
		float jet2Mass = JETS[1].mass;
		float jetPrunedMass = 0;
		if (jet1Mass > jet2Mass) jetPrunedMass = jet1Mass;
		else jetPrunedMass = jet2Mass;
		float massAve = ( jet1Mass + jet2Mass ) / 2.0;
		float massAsym = abs( jet1Mass - jet2Mass ) / ( jet1Mass + jet2Mass );
		//////////////////////////////////////////////////////////////////////////


		if( massAsym < cutAsymvalue ) cutMassAsym = 1;
		
		histos2D_[ "jetMassHT_cutDijet_noTrigger" ]->Fill( jetPrunedMass, HT );
		histos2D_[ "jetTrimmedMassHT_cutDijet_noTrigger" ]->Fill( trimmedMass, HT );
		if ( basedTriggerFired || triggersFired[0] ) {
			if ( basedTriggerFired && triggersFired[0] ) {
				histos2D_[ "jetMassHT_cutDijet_triggerOneAndTwo" ]->Fill( jetPrunedMass, HT );
				histos2D_[ "jetTrimmedMassHT_cutDijet_triggerOneAndTwo" ]->Fill( trimmedMass, HT );
			} else if ( basedTriggerFired ) {
				histos2D_[ "jetMassHT_cutDijet_triggerOne" ]->Fill( jetPrunedMass, HT );
				histos2D_[ "jetTrimmedMassHT_cutDijet_triggerOne" ]->Fill( trimmedMass, HT );
			} else if ( triggersFired[0] ) {
				histos2D_[ "jetMassHT_cutDijet_triggerTwo" ]->Fill( jetPrunedMass, HT );
				histos2D_[ "jetTrimmedMassHT_cutDijet_triggerTwo" ]->Fill( trimmedMass, HT );
			}
		}

		if ( basedTriggerFired ) {
			histos1D_[ "massAveDenom_cutDijet" ]->Fill( massAve  );
			histos1D_[ "trimmedMassDenom_cutDijet" ]->Fill( trimmedMass  );
			histos1D_[ "jet1MassDenom_cutDijet" ]->Fill( jetPrunedMass  );
			histos1D_[ "jetLeadMassDenom_cutDijet" ]->Fill( leadMass  );
			histos1D_[ "jet1PtDenom_cutDijet" ]->Fill( JETS[0].p4.Pt()   );
			histos1D_[ "jet2PtDenom_cutDijet" ]->Fill( JETS[1].p4.Pt()   );
			histos1D_[ "HTDenom_cutDijet" ]->Fill( HT  );
			histos1D_[ "ak4HTDenom_cutDijet" ]->Fill( ak4HT  );
			histos2D_[ "jet1PtHTDenom_cutDijet" ]->Fill( JETS[0].p4.Pt(), HT );
			histos2D_[ "jet2PtHTDenom_cutDijet" ]->Fill( JETS[1].p4.Pt(), HT );
			histos2D_[ "jetMassHTDenom_cutDijet" ]->Fill( jetPrunedMass, HT );
			histos2D_[ "jetTrimmedMassHTDenom_cutDijet" ]->Fill( trimmedMass, HT );
			histos2D_[ "massAveHTDenom_cutDijet" ]->Fill( massAve, HT );

			if ( ORTriggers ){
				histos1D_[ "massAvePassing_cutDijet" ]->Fill( massAve  );
				histos1D_[ "trimmedMassPassing_cutDijet" ]->Fill( trimmedMass  );
				histos1D_[ "jetLeadMassPassing_cutDijet" ]->Fill( leadMass  );
				histos1D_[ "jet1MassPassing_cutDijet" ]->Fill( jetPrunedMass  );
				histos1D_[ "jet1PtPassing_cutDijet" ]->Fill( JETS[0].p4.Pt()   );
				histos1D_[ "jet2PtPassing_cutDijet" ]->Fill( JETS[1].p4.Pt()   );
				histos1D_[ "HTPassing_cutDijet" ]->Fill( HT  );
				histos1D_[ "ak4HTPassing_cutDijet" ]->Fill( ak4HT  );
				histos2D_[ "jet1PtHTPassing_cutDijet" ]->Fill( JETS[0].p4.Pt(), HT );
				histos2D_[ "jet2PtHTPassing_cutDijet" ]->Fill( JETS[1].p4.Pt(), HT );
				histos2D_[ "jetMassHTPassing_cutDijet" ]->Fill( jetPrunedMass, HT );
				histos2D_[ "jetTrimmedMassHTPassing_cutDijet" ]->Fill( trimmedMass, HT );
				histos2D_[ "massAveHTPassing_cutDijet" ]->Fill( massAve, HT );
			}

			if ( HT > 900 ) {
				histos1D_[ "jetTrimmedMassDenom_cutHT" ]->Fill( trimmedMass  );
				histos1D_[ "jet1MassDenom_cutHT" ]->Fill( jetPrunedMass  );
				histos1D_[ "jetLeadMassDenom_cutHT" ]->Fill( leadMass  );
				histos1D_[ "HTDenom_cutHT" ]->Fill( HT  );
				if ( ORTriggers ){
					histos1D_[ "jetTrimmedMassPassing_cutHT" ]->Fill( trimmedMass  );
					histos1D_[ "jet1MassPassing_cutHT" ]->Fill( jetPrunedMass  );
					histos1D_[ "jetLeadMassPassing_cutHT" ]->Fill( leadMass  );
					histos1D_[ "HTPassing_cutHT" ]->Fill( HT  );
				}
			}

			if ( jetPrunedMass > 60 ) {
				histos1D_[ "jetTrimmedMassDenom_cutJetMass" ]->Fill( trimmedMass  );
				histos1D_[ "jet1MassDenom_cutJetMass" ]->Fill( jetPrunedMass  );
				histos1D_[ "HTDenom_cutJetMass" ]->Fill( HT  );
				if ( ORTriggers ){
					histos1D_[ "jetTrimmedMassPassing_cutJetMass" ]->Fill( trimmedMass  );
					histos1D_[ "jet1MassPassing_cutJetMass" ]->Fill( jetPrunedMass  );
					histos1D_[ "HTPassing_cutJetMass" ]->Fill( HT  );
				}
			}

			if ( ( JETS[0].p4.Pt() > cutjet1Ptvalue ) && ( JETS[1].p4.Pt() > cutjet2Ptvalue ) ) {
				histos1D_[ "massAveDenom_cutJetsPt" ]->Fill( massAve  );
				histos1D_[ "trimmedMassDenom_cutJetsPt" ]->Fill( trimmedMass  );
				histos1D_[ "jet1MassDenom_cutJetsPt" ]->Fill( jetPrunedMass  );
				histos1D_[ "jet1PtDenom_cutJetsPt" ]->Fill( JETS[0].p4.Pt()   );
				histos1D_[ "jet2PtDenom_cutJetsPt" ]->Fill( JETS[1].p4.Pt()   );
				histos1D_[ "HTDenom_cutJetsPt" ]->Fill( HT  );
				histos1D_[ "ak4HTDenom_cutJetsPt" ]->Fill( ak4HT  );
				histos2D_[ "jetMassHTDenom_cutJetsPt" ]->Fill( jetPrunedMass, HT );
				histos2D_[ "jetTrimmedMassHTDenom_cutJetsPt" ]->Fill( trimmedMass, HT );
				histos2D_[ "massAveHTDenom_cutJetsPt" ]->Fill( massAve, HT );
				if ( ORTriggers ){
					histos1D_[ "massAvePassing_cutJetsPt" ]->Fill( massAve  );
					histos1D_[ "trimmedMassPassing_cutJetsPt" ]->Fill( trimmedMass  );
					histos1D_[ "jet1MassPassing_cutJetsPt" ]->Fill( jetPrunedMass  );
					histos1D_[ "jet1PtPassing_cutJetsPt" ]->Fill( JETS[0].p4.Pt()   );
					histos1D_[ "jet2PtPassing_cutJetsPt" ]->Fill( JETS[1].p4.Pt()   );
					histos1D_[ "HTPassing_cutJetsPt" ]->Fill( HT  );
					histos1D_[ "ak4HTPassing_cutJetsPt" ]->Fill( ak4HT  );
					histos2D_[ "jetMassHTPassing_cutJetsPt" ]->Fill( jetPrunedMass, HT );
					histos2D_[ "jetTrimmedMassHTPassing_cutJetsPt" ]->Fill( trimmedMass, HT );
					histos2D_[ "massAveHTPassing_cutJetsPt" ]->Fill( massAve, HT );
				}
			}

			if ( ( cutMassAsym ) && ( HT > 900 ) && ( jetPrunedMass > 60 ) ) {
				histos1D_[ "massAveDenom_cutMassAsym" ]->Fill( massAve  );
				histos1D_[ "trimmedMassDenom_cutMassAsym" ]->Fill( trimmedMass  );
				histos1D_[ "jet1MassDenom_cutMassAsym" ]->Fill( jetPrunedMass  );
				histos1D_[ "jet1PtDenom_cutMassAsym" ]->Fill( JETS[0].p4.Pt()   );
				histos1D_[ "jet2PtDenom_cutMassAsym" ]->Fill( JETS[1].p4.Pt()   );
				histos1D_[ "HTDenom_cutMassAsym" ]->Fill( HT  );
				histos1D_[ "ak4HTDenom_cutMassAsym" ]->Fill( ak4HT  );
				histos2D_[ "jetMassHTDenom_cutMassAsym" ]->Fill( jetPrunedMass, HT );
				histos2D_[ "jetTrimmedMassHTDenom_cutMassAsym" ]->Fill( trimmedMass, HT );
				histos2D_[ "massAveHTDenom_cutMassAsym" ]->Fill( massAve, HT );

				if ( ORTriggers ){
					histos1D_[ "massAvePassing_cutMassAsym" ]->Fill( massAve  );
					histos1D_[ "trimmedMassPassing_cutMassAsym" ]->Fill( trimmedMass  );
					histos1D_[ "jet1MassPassing_cutMassAsym" ]->Fill( jetPrunedMass  );
					histos1D_[ "jet1PtPassing_cutMassAsym" ]->Fill( JETS[0].p4.Pt()   );
					histos1D_[ "jet2PtPassing_cutMassAsym" ]->Fill( JETS[1].p4.Pt()   );
					histos1D_[ "HTPassing_cutMassAsym" ]->Fill( HT  );
					histos1D_[ "ak4HTPassing_cutMassAsym" ]->Fill( ak4HT  );
					histos2D_[ "jetMassHTPassing_cutMassAsym" ]->Fill( jetPrunedMass, HT );
					histos2D_[ "jetTrimmedMassHTPassing_cutMassAsym" ]->Fill( trimmedMass, HT );
					histos2D_[ "massAveHTPassing_cutMassAsym" ]->Fill( massAve, HT );
				}
			}
		}
	}
	JETS.clear();

}


// ------------ method called once each job just before starting event loop  ------------
void RUNBoostedTriggerEfficiency::beginJob() {

	histos1D_[ "ak4HTDenom_cutDijet" ] = fs_->make< TH1D >( "ak4HTDenom_cutDijet", "ak4HTDenom_cutDijet", 150, 0., 1500. );
	histos1D_[ "ak4HTDenom_cutDijet" ]->Sumw2();
	histos1D_[ "ak4HTPassing_cutDijet" ] = fs_->make< TH1D >( "ak4HTPassing_cutDijet", "ak4HTPassing_cutDijet", 150, 0., 1500. );
	histos1D_[ "ak4HTPassing_cutDijet" ]->Sumw2();

	histos1D_[ "ak4HTDenom_cutMassAsym" ] = fs_->make< TH1D >( "ak4HTDenom_cutMassAsym", "ak4HTDenom_cutMassAsym", 150, 0., 1500. );
	histos1D_[ "ak4HTDenom_cutMassAsym" ]->Sumw2();
	histos1D_[ "ak4HTPassing_cutMassAsym" ] = fs_->make< TH1D >( "ak4HTPassing_cutMassAsym", "ak4HTPassing_cutMassAsym", 150, 0., 1500. );
	histos1D_[ "ak4HTPassing_cutMassAsym" ]->Sumw2();

	histos1D_[ "ak4HTDenom_cutJetsPt" ] = fs_->make< TH1D >( "ak4HTDenom_cutJetsPt", "ak4HTDenom_cutJetsPt", 150, 0., 1500. );
	histos1D_[ "ak4HTDenom_cutJetsPt" ]->Sumw2();
	histos1D_[ "ak4HTPassing_cutJetsPt" ] = fs_->make< TH1D >( "ak4HTPassing_cutJetsPt", "ak4HTPassing_cutJetsPt", 150, 0., 1500. );
	histos1D_[ "ak4HTPassing_cutJetsPt" ]->Sumw2();


	histos1D_[ "HTDenom_cutDijet" ] = fs_->make< TH1D >( "HTDenom_cutDijet", "HTDenom_cutDijet", 150, 0., 1500. );
	histos1D_[ "HTDenom_cutDijet" ]->Sumw2();
	histos1D_[ "HTPassing_cutDijet" ] = fs_->make< TH1D >( "HTPassing_cutDijet", "HTPassing_cutDijet", 150, 0., 1500. );
	histos1D_[ "HTPassing_cutDijet" ]->Sumw2();

	histos1D_[ "HTDenom_cutMassAsym" ] = fs_->make< TH1D >( "HTDenom_cutMassAsym", "HTDenom_cutMassAsym", 150, 0., 1500. );
	histos1D_[ "HTDenom_cutMassAsym" ]->Sumw2();
	histos1D_[ "HTPassing_cutMassAsym" ] = fs_->make< TH1D >( "HTPassing_cutMassAsym", "HTPassing_cutMassAsym", 150, 0., 1500. );
	histos1D_[ "HTPassing_cutMassAsym" ]->Sumw2();

	histos1D_[ "HTDenom_cutJetsPt" ] = fs_->make< TH1D >( "HTDenom_cutJetsPt", "HTDenom_cutJetsPt", 150, 0., 1500. );
	histos1D_[ "HTDenom_cutJetsPt" ]->Sumw2();
	histos1D_[ "HTPassing_cutJetsPt" ] = fs_->make< TH1D >( "HTPassing_cutJetsPt", "HTPassing_cutJetsPt", 150, 0., 1500. );
	histos1D_[ "HTPassing_cutJetsPt" ]->Sumw2();


	histos1D_[ "trimmedMassDenom_cutDijet" ] = fs_->make< TH1D >( "trimmedMassDenom_cutDijet", "trimmedMassDenom_cutDijet", 60, 0., 600. );
	histos1D_[ "trimmedMassDenom_cutDijet" ]->Sumw2();
	histos1D_[ "trimmedMassPassing_cutDijet" ] = fs_->make< TH1D >( "trimmedMassPassing_cutDijet", "trimmedMassPassing_cutDijet", 60, 0., 600. );
	histos1D_[ "trimmedMassPassing_cutDijet" ]->Sumw2();

	histos1D_[ "trimmedMassDenom_cutMassAsym" ] = fs_->make< TH1D >( "trimmedMassDenom_cutMassAsym", "trimmedMassDenom_cutMassAsym", 60, 0., 600. );
	histos1D_[ "trimmedMassDenom_cutMassAsym" ]->Sumw2();
	histos1D_[ "trimmedMassPassing_cutMassAsym" ] = fs_->make< TH1D >( "trimmedMassPassing_cutMassAsym", "trimmedMassPassing_cutMassAsym", 60, 0., 600. );
	histos1D_[ "trimmedMassPassing_cutMassAsym" ]->Sumw2();

	histos1D_[ "trimmedMassDenom_cutJetsPt" ] = fs_->make< TH1D >( "trimmedMassDenom_cutJetsPt", "trimmedMassDenom_cutJetsPt", 60, 0., 600. );
	histos1D_[ "trimmedMassDenom_cutJetsPt" ]->Sumw2();
	histos1D_[ "trimmedMassPassing_cutJetsPt" ] = fs_->make< TH1D >( "trimmedMassPassing_cutJetsPt", "trimmedMassPassing_cutJetsPt", 60, 0., 600. );
	histos1D_[ "trimmedMassPassing_cutJetsPt" ]->Sumw2();


	histos1D_[ "massAveDenom_cutDijet" ] = fs_->make< TH1D >( "massAveDenom_cutDijet", "massAveDenom_cutDijet", 60, 0., 600. );
	histos1D_[ "massAveDenom_cutDijet" ]->Sumw2();
	histos1D_[ "massAvePassing_cutDijet" ] = fs_->make< TH1D >( "massAvePassing_cutDijet", "massAvePassing_cutDijet", 60, 0., 600. );
	histos1D_[ "massAvePassing_cutDijet" ]->Sumw2();

	histos1D_[ "massAveDenom_cutMassAsym" ] = fs_->make< TH1D >( "massAveDenom_cutMassAsym", "massAveDenom_cutMassAsym", 60, 0., 600. );
	histos1D_[ "massAveDenom_cutMassAsym" ]->Sumw2();
	histos1D_[ "massAvePassing_cutMassAsym" ] = fs_->make< TH1D >( "massAvePassing_cutMassAsym", "massAvePassing_cutMassAsym", 60, 0., 600. );
	histos1D_[ "massAvePassing_cutMassAsym" ]->Sumw2();

	histos1D_[ "massAveDenom_cutJetsPt" ] = fs_->make< TH1D >( "massAveDenom_cutJetsPt", "massAveDenom_cutJetsPt", 60, 0., 600. );
	histos1D_[ "massAveDenom_cutJetsPt" ]->Sumw2();
	histos1D_[ "massAvePassing_cutJetsPt" ] = fs_->make< TH1D >( "massAvePassing_cutJetsPt", "massAvePassing_cutJetsPt", 60, 0., 600. );
	histos1D_[ "massAvePassing_cutJetsPt" ]->Sumw2();



	histos1D_[ "jet1PtDenom_cutDijet" ] = fs_->make< TH1D >( "jet1PtDenom_cutDijet", "jet1PtDenom_cutDijet", 100, 0., 1000. );
	histos1D_[ "jet1PtDenom_cutDijet" ]->Sumw2();
	histos1D_[ "jet1PtPassing_cutDijet" ] = fs_->make< TH1D >( "jet1PtPassing_cutDijet", "jet1PtPassing_cutDijet", 100, 0., 1000. );
	histos1D_[ "jet1PtPassing_cutDijet" ]->Sumw2();

	histos1D_[ "jet2PtDenom_cutDijet" ] = fs_->make< TH1D >( "jet2PtDenom_cutDijet", "jet2PtDenom_cutDijet", 100, 0., 1000. );
	histos1D_[ "jet2PtDenom_cutDijet" ]->Sumw2();
	histos1D_[ "jet2PtPassing_cutDijet" ] = fs_->make< TH1D >( "jet2PtPassing_cutDijet", "jet2PtPassing_cutDijet", 100, 0., 1000. );
	histos1D_[ "jet2PtPassing_cutDijet" ]->Sumw2();

	histos1D_[ "jet1PtDenom_cutMassAsym" ] = fs_->make< TH1D >( "jet1PtDenom_cutMassAsym", "jet1PtDenom_cutMassAsym", 100, 0., 1000. );
	histos1D_[ "jet1PtDenom_cutMassAsym" ]->Sumw2();
	histos1D_[ "jet1PtPassing_cutMassAsym" ] = fs_->make< TH1D >( "jet1PtPassing_cutMassAsym", "jet1PtPassing_cutMassAsym", 100, 0., 1000. );
	histos1D_[ "jet1PtPassing_cutMassAsym" ]->Sumw2();

	histos1D_[ "jet2PtDenom_cutMassAsym" ] = fs_->make< TH1D >( "jet2PtDenom_cutMassAsym", "jet2PtDenom_cutMassAsym", 100, 0., 1000. );
	histos1D_[ "jet2PtDenom_cutMassAsym" ]->Sumw2();
	histos1D_[ "jet2PtPassing_cutMassAsym" ] = fs_->make< TH1D >( "jet2PtPassing_cutMassAsym", "jet2PtPassing_cutMassAsym", 100, 0., 1000. );
	histos1D_[ "jet2PtPassing_cutMassAsym" ]->Sumw2();

	histos1D_[ "jet1PtDenom_cutJetsPt" ] = fs_->make< TH1D >( "jet1PtDenom_cutJetsPt", "jet1PtDenom_cutJetsPt", 100, 0., 1000. );
	histos1D_[ "jet1PtDenom_cutJetsPt" ]->Sumw2();
	histos1D_[ "jet1PtPassing_cutJetsPt" ] = fs_->make< TH1D >( "jet1PtPassing_cutJetsPt", "jet1PtPassing_cutJetsPt", 100, 0., 1000. );
	histos1D_[ "jet1PtPassing_cutJetsPt" ]->Sumw2();

	histos1D_[ "jet2PtDenom_cutJetsPt" ] = fs_->make< TH1D >( "jet2PtDenom_cutJetsPt", "jet2PtDenom_cutJetsPt", 100, 0., 1000. );
	histos1D_[ "jet2PtDenom_cutJetsPt" ]->Sumw2();
	histos1D_[ "jet2PtPassing_cutJetsPt" ] = fs_->make< TH1D >( "jet2PtPassing_cutJetsPt", "jet2PtPassing_cutJetsPt", 100, 0., 1000. );
	histos1D_[ "jet2PtPassing_cutJetsPt" ]->Sumw2();



	histos1D_[ "jet1MassDenom_cutDijet" ] = fs_->make< TH1D >( "jet1MassDenom_cutDijet", "jet1MassDenom_cutDijet", 60, 0., 600. );
	histos1D_[ "jet1MassDenom_cutDijet" ]->Sumw2();
	histos1D_[ "jet1MassPassing_cutDijet" ] = fs_->make< TH1D >( "jet1MassPassing_cutDijet", "jet1MassPassing_cutDijet", 60, 0., 600. );
	histos1D_[ "jet1MassPassing_cutDijet" ]->Sumw2();

	histos1D_[ "jet1MassDenom_cutHT" ] = fs_->make< TH1D >( "jet1MassDenom_cutHT", "jet1MassDenom_cutHT", 60, 0., 600. );
	histos1D_[ "jet1MassDenom_cutHT" ]->Sumw2();
	histos1D_[ "jet1MassPassing_cutHT" ] = fs_->make< TH1D >( "jet1MassPassing_cutHT", "jet1MassPassing_cutHT", 60, 0., 600. );
	histos1D_[ "jet1MassPassing_cutHT" ]->Sumw2();

	histos1D_[ "jetLeadMassDenom_cutDijet" ] = fs_->make< TH1D >( "jetLeadMassDenom_cutDijet", "jetLeadMassDenom_cutDijet", 60, 0., 600. );
	histos1D_[ "jetLeadMassDenom_cutDijet" ]->Sumw2();
	histos1D_[ "jetLeadMassPassing_cutDijet" ] = fs_->make< TH1D >( "jetLeadMassPassing_cutDijet", "jetLeadMassPassing_cutDijet", 60, 0., 600. );
	histos1D_[ "jetLeadMassPassing_cutDijet" ]->Sumw2();

	histos1D_[ "jetLeadMassDenom_cutHT" ] = fs_->make< TH1D >( "jetLeadMassDenom_cutHT", "jetLeadMassDenom_cutHT", 60, 0., 600. );
	histos1D_[ "jetLeadMassDenom_cutHT" ]->Sumw2();
	histos1D_[ "jetLeadMassPassing_cutHT" ] = fs_->make< TH1D >( "jetLeadMassPassing_cutHT", "jetLeadMassPassing_cutHT", 60, 0., 600. );
	histos1D_[ "jetLeadMassPassing_cutHT" ]->Sumw2();

	histos1D_[ "jetTrimmedMassDenom_cutHT" ] = fs_->make< TH1D >( "jetTrimmedMassDenom_cutHT", "jetTrimmedMassDenom_cutHT", 60, 0., 600. );
	histos1D_[ "jetTrimmedMassDenom_cutHT" ]->Sumw2();
	histos1D_[ "jetTrimmedMassPassing_cutHT" ] = fs_->make< TH1D >( "jetTrimmedMassPassing_cutHT", "jetTrimmedMassPassing_cutHT", 60, 0., 600. );
	histos1D_[ "jetTrimmedMassPassing_cutHT" ]->Sumw2();

	histos1D_[ "HTDenom_cutHT" ] = fs_->make< TH1D >( "HTDenom_cutHT", "HTDenom_cutHT", 150, 0., 1500. );
	histos1D_[ "HTDenom_cutHT" ]->Sumw2();
	histos1D_[ "HTPassing_cutHT" ] = fs_->make< TH1D >( "HTPassing_cutHT", "HTPassing_cutHT", 150, 0., 1500. );
	histos1D_[ "HTPassing_cutHT" ]->Sumw2();

	histos1D_[ "jet1MassDenom_cutJetMass" ] = fs_->make< TH1D >( "jet1MassDenom_cutJetMass", "jet1MassDenom_cutJetMass", 60, 0., 600. );
	histos1D_[ "jet1MassDenom_cutJetMass" ]->Sumw2();
	histos1D_[ "jet1MassPassing_cutJetMass" ] = fs_->make< TH1D >( "jet1MassPassing_cutJetMass", "jet1MassPassing_cutJetMass", 60, 0., 600. );
	histos1D_[ "jet1MassPassing_cutJetMass" ]->Sumw2();

	histos1D_[ "jetTrimmedMassDenom_cutJetMass" ] = fs_->make< TH1D >( "jetTrimmedMassDenom_cutJetMass", "jetTrimmedMassDenom_cutJetMass", 60, 0., 600. );
	histos1D_[ "jetTrimmedMassDenom_cutJetMass" ]->Sumw2();
	histos1D_[ "jetTrimmedMassPassing_cutJetMass" ] = fs_->make< TH1D >( "jetTrimmedMassPassing_cutJetMass", "jetTrimmedMassPassing_cutJetMass", 60, 0., 600. );
	histos1D_[ "jetTrimmedMassPassing_cutJetMass" ]->Sumw2();

	histos1D_[ "HTDenom_cutJetMass" ] = fs_->make< TH1D >( "HTDenom_cutJetMass", "HTDenom_cutJetMass", 150, 0., 1500. );
	histos1D_[ "HTDenom_cutJetMass" ]->Sumw2();
	histos1D_[ "HTPassing_cutJetMass" ] = fs_->make< TH1D >( "HTPassing_cutJetMass", "HTPassing_cutJetMass", 150, 0., 1500. );
	histos1D_[ "HTPassing_cutJetMass" ]->Sumw2();

	histos1D_[ "jet1MassDenom_cutMassAsym" ] = fs_->make< TH1D >( "jet1MassDenom_cutMassAsym", "jet1MassDenom_cutMassAsym", 60, 0., 600. );
	histos1D_[ "jet1MassDenom_cutMassAsym" ]->Sumw2();
	histos1D_[ "jet1MassPassing_cutMassAsym" ] = fs_->make< TH1D >( "jet1MassPassing_cutMassAsym", "jet1MassPassing_cutMassAsym", 60, 0., 600. );
	histos1D_[ "jet1MassPassing_cutMassAsym" ]->Sumw2();

	histos1D_[ "jet1MassDenom_cutHT" ] = fs_->make< TH1D >( "jet1MassDenom_cutHT", "jet1MassDenom_cutHT", 60, 0., 600. );
	histos1D_[ "jet1MassDenom_cutHT" ]->Sumw2();
	histos1D_[ "jet1MassPassing_cutHT" ] = fs_->make< TH1D >( "jet1MassPassing_cutHT", "jet1MassPassing_cutHT", 60, 0., 600. );
	histos1D_[ "jet1MassPassing_cutHT" ]->Sumw2();

	histos1D_[ "jet1MassDenom_cutJetsPt" ] = fs_->make< TH1D >( "jet1MassDenom_cutJetsPt", "jet1MassDenom_cutJetsPt", 60, 0., 600. );
	histos1D_[ "jet1MassDenom_cutJetsPt" ]->Sumw2();
	histos1D_[ "jet1MassPassing_cutJetsPt" ] = fs_->make< TH1D >( "jet1MassPassing_cutJetsPt", "jet1MassPassing_cutJetsPt", 60, 0., 600. );
	histos1D_[ "jet1MassPassing_cutJetsPt" ]->Sumw2();


	histos2D_[ "jetMassHT_noTrigger" ] = fs_->make< TH2D >( "jetMassHT_noTrigger", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetMassHT_noTrigger" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetMassHT_noTrigger" ]->SetXTitle( "Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jetMassHT_noTrigger" ]->Sumw2();

	histos2D_[ "jetMassHT_triggerOne" ] = fs_->make< TH2D >( "jetMassHT_triggerOne", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetMassHT_triggerOne" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetMassHT_triggerOne" ]->SetXTitle( "Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jetMassHT_triggerOne" ]->Sumw2();

	histos2D_[ "jetMassHT_triggerTwo" ] = fs_->make< TH2D >( "jetMassHT_triggerTwo", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetMassHT_triggerTwo" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetMassHT_triggerTwo" ]->SetXTitle( "Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jetMassHT_triggerTwo" ]->Sumw2();

	histos2D_[ "jetMassHT_triggerOneAndTwo" ] = fs_->make< TH2D >( "jetMassHT_triggerOneAndTwo", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetMassHT_triggerOneAndTwo" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetMassHT_triggerOneAndTwo" ]->SetXTitle( "Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jetMassHT_triggerOneAndTwo" ]->Sumw2();

	histos2D_[ "jetTrimmedMassHT_noTrigger" ] = fs_->make< TH2D >( "jetTrimmedMassHT_noTrigger", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetTrimmedMassHT_noTrigger" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetTrimmedMassHT_noTrigger" ]->SetXTitle( "Leading Jet Trimmed Mass [GeV]" );
	histos2D_[ "jetTrimmedMassHT_noTrigger" ]->Sumw2();

	histos2D_[ "jetTrimmedMassHT_triggerOne" ] = fs_->make< TH2D >( "jetTrimmedMassHT_triggerOne", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetTrimmedMassHT_triggerOne" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetTrimmedMassHT_triggerOne" ]->SetXTitle( "Leading Jet Trimmed Mass [GeV]" );
	histos2D_[ "jetTrimmedMassHT_triggerOne" ]->Sumw2();

	histos2D_[ "jetTrimmedMassHT_triggerTwo" ] = fs_->make< TH2D >( "jetTrimmedMassHT_triggerTwo", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetTrimmedMassHT_triggerTwo" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetTrimmedMassHT_triggerTwo" ]->SetXTitle( "Leading Jet Trimmed Mass [GeV]" );
	histos2D_[ "jetTrimmedMassHT_triggerTwo" ]->Sumw2();

	histos2D_[ "jetTrimmedMassHT_triggerOneAndTwo" ] = fs_->make< TH2D >( "jetTrimmedMassHT_triggerOneAndTwo", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetTrimmedMassHT_triggerOneAndTwo" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetTrimmedMassHT_triggerOneAndTwo" ]->SetXTitle( "Leading Jet Trimmed Mass [GeV]" );
	histos2D_[ "jetTrimmedMassHT_triggerOneAndTwo" ]->Sumw2();

	histos2D_[ "jetMassHT_cutDijet_noTrigger" ] = fs_->make< TH2D >( "jetMassHT_cutDijet_noTrigger", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetMassHT_cutDijet_noTrigger" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetMassHT_cutDijet_noTrigger" ]->SetXTitle( "Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jetMassHT_cutDijet_noTrigger" ]->Sumw2();

	histos2D_[ "jetMassHT_cutDijet_triggerOne" ] = fs_->make< TH2D >( "jetMassHT_cutDijet_triggerOne", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetMassHT_cutDijet_triggerOne" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetMassHT_cutDijet_triggerOne" ]->SetXTitle( "Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jetMassHT_cutDijet_triggerOne" ]->Sumw2();

	histos2D_[ "jetMassHT_cutDijet_triggerTwo" ] = fs_->make< TH2D >( "jetMassHT_cutDijet_triggerTwo", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetMassHT_cutDijet_triggerTwo" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetMassHT_cutDijet_triggerTwo" ]->SetXTitle( "Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jetMassHT_cutDijet_triggerTwo" ]->Sumw2();

	histos2D_[ "jetMassHT_cutDijet_triggerOneAndTwo" ] = fs_->make< TH2D >( "jetMassHT_cutDijet_triggerOneAndTwo", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetMassHT_cutDijet_triggerOneAndTwo" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetMassHT_cutDijet_triggerOneAndTwo" ]->SetXTitle( "Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jetMassHT_cutDijet_triggerOneAndTwo" ]->Sumw2();

	histos2D_[ "jetTrimmedMassHT_cutDijet_noTrigger" ] = fs_->make< TH2D >( "jetTrimmedMassHT_cutDijet_noTrigger", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetTrimmedMassHT_cutDijet_noTrigger" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetTrimmedMassHT_cutDijet_noTrigger" ]->SetXTitle( "Leading Jet Trimmed Mass [GeV]" );
	histos2D_[ "jetTrimmedMassHT_cutDijet_noTrigger" ]->Sumw2();

	histos2D_[ "jetTrimmedMassHT_cutDijet_triggerOne" ] = fs_->make< TH2D >( "jetTrimmedMassHT_cutDijet_triggerOne", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetTrimmedMassHT_cutDijet_triggerOne" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetTrimmedMassHT_cutDijet_triggerOne" ]->SetXTitle( "Leading Jet Trimmed Mass [GeV]" );
	histos2D_[ "jetTrimmedMassHT_cutDijet_triggerOne" ]->Sumw2();

	histos2D_[ "jetTrimmedMassHT_cutDijet_triggerTwo" ] = fs_->make< TH2D >( "jetTrimmedMassHT_cutDijet_triggerTwo", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetTrimmedMassHT_cutDijet_triggerTwo" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetTrimmedMassHT_cutDijet_triggerTwo" ]->SetXTitle( "Leading Jet Trimmed Mass [GeV]" );
	histos2D_[ "jetTrimmedMassHT_cutDijet_triggerTwo" ]->Sumw2();

	histos2D_[ "jetTrimmedMassHT_cutDijet_triggerOneAndTwo" ] = fs_->make< TH2D >( "jetTrimmedMassHT_cutDijet_triggerOneAndTwo", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetTrimmedMassHT_cutDijet_triggerOneAndTwo" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetTrimmedMassHT_cutDijet_triggerOneAndTwo" ]->SetXTitle( "Leading Jet Trimmed Mass [GeV]" );
	histos2D_[ "jetTrimmedMassHT_cutDijet_triggerOneAndTwo" ]->Sumw2();

	histos2D_[ "jet1PtHTDenom_cutDijet" ] = fs_->make< TH2D >( "jet1PtHTDenom_cutDijet", "HT vs Leading Jet Pt", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jet1PtHTDenom_cutDijet" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jet1PtHTDenom_cutDijet" ]->SetXTitle( "Leading Jet Pruned Pt [GeV]" );
	histos2D_[ "jet1PtHTDenom_cutDijet" ]->Sumw2();

	histos2D_[ "jet1PtHTPassing_cutDijet" ] = fs_->make< TH2D >( "jet1PtHTPassing_cutDijet", "HT vs Leading Jet Pt", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jet1PtHTPassing_cutDijet" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jet1PtHTPassing_cutDijet" ]->SetXTitle( "Leading Jet Pruned Pt [GeV]" );
	histos2D_[ "jet1PtHTPassing_cutDijet" ]->Sumw2();

	histos2D_[ "jet2PtHTDenom_cutDijet" ] = fs_->make< TH2D >( "jet2PtHTDenom_cutDijet", "HT vs Leading Jet Pt", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jet2PtHTDenom_cutDijet" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jet2PtHTDenom_cutDijet" ]->SetXTitle( "Leading Jet Pruned Pt [GeV]" );
	histos2D_[ "jet2PtHTDenom_cutDijet" ]->Sumw2();

	histos2D_[ "jet2PtHTPassing_cutDijet" ] = fs_->make< TH2D >( "jet2PtHTPassing_cutDijet", "HT vs 2nd Leading Jet Pt", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jet2PtHTPassing_cutDijet" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jet2PtHTPassing_cutDijet" ]->SetXTitle( "2nd Leading Jet Pruned Pt [GeV]" );
	histos2D_[ "jet2PtHTPassing_cutDijet" ]->Sumw2();

	histos2D_[ "jetMassHTDenom_cutDijet" ] = fs_->make< TH2D >( "jetMassHTDenom_cutDijet", "HT vs 2nd Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetMassHTDenom_cutDijet" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetMassHTDenom_cutDijet" ]->SetXTitle( "2nd Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jetMassHTDenom_cutDijet" ]->Sumw2();

	histos2D_[ "jetMassHTPassing_cutDijet" ] = fs_->make< TH2D >( "jetMassHTPassing_cutDijet", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetMassHTPassing_cutDijet" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetMassHTPassing_cutDijet" ]->SetXTitle( "Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jetMassHTPassing_cutDijet" ]->Sumw2();

	histos2D_[ "jetMassHTDenom_cutMassAsym" ] = fs_->make< TH2D >( "jetMassHTDenom_cutMassAsym", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetMassHTDenom_cutMassAsym" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetMassHTDenom_cutMassAsym" ]->SetXTitle( "Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jetMassHTDenom_cutMassAsym" ]->Sumw2();

	histos2D_[ "jetMassHTPassing_cutMassAsym" ] = fs_->make< TH2D >( "jetMassHTPassing_cutMassAsym", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetMassHTPassing_cutMassAsym" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetMassHTPassing_cutMassAsym" ]->SetXTitle( "Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jetMassHTPassing_cutMassAsym" ]->Sumw2();

	histos2D_[ "jetMassHTDenom_cutJetsPt" ] = fs_->make< TH2D >( "jetMassHTDenom_cutJetsPt", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetMassHTDenom_cutJetsPt" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetMassHTDenom_cutJetsPt" ]->SetXTitle( "Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jetMassHTDenom_cutJetsPt" ]->Sumw2();

	histos2D_[ "jetMassHTPassing_cutJetsPt" ] = fs_->make< TH2D >( "jetMassHTPassing_cutJetsPt", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetMassHTPassing_cutJetsPt" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetMassHTPassing_cutJetsPt" ]->SetXTitle( "Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jetMassHTPassing_cutJetsPt" ]->Sumw2();


	histos2D_[ "jetTrimmedMassHTDenom_cutDijet" ] = fs_->make< TH2D >( "jetTrimmedMassHTDenom_cutDijet", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetTrimmedMassHTDenom_cutDijet" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetTrimmedMassHTDenom_cutDijet" ]->SetXTitle( "Leading Jet Trimmed Mass [GeV]" );
	histos2D_[ "jetTrimmedMassHTDenom_cutDijet" ]->Sumw2();

	histos2D_[ "jetTrimmedMassHTPassing_cutDijet" ] = fs_->make< TH2D >( "jetTrimmedMassHTPassing_cutDijet", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetTrimmedMassHTPassing_cutDijet" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetTrimmedMassHTPassing_cutDijet" ]->SetXTitle( "Leading Jet Trimmed Mass [GeV]" );
	histos2D_[ "jetTrimmedMassHTPassing_cutDijet" ]->Sumw2();

	histos2D_[ "jetTrimmedMassHTDenom_cutMassAsym" ] = fs_->make< TH2D >( "jetTrimmedMassHTDenom_cutMassAsym", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetTrimmedMassHTDenom_cutMassAsym" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetTrimmedMassHTDenom_cutMassAsym" ]->SetXTitle( "Leading Jet Trimmed Mass [GeV]" );
	histos2D_[ "jetTrimmedMassHTDenom_cutMassAsym" ]->Sumw2();

	histos2D_[ "jetTrimmedMassHTPassing_cutMassAsym" ] = fs_->make< TH2D >( "jetTrimmedMassHTPassing_cutMassAsym", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetTrimmedMassHTPassing_cutMassAsym" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetTrimmedMassHTPassing_cutMassAsym" ]->SetXTitle( "Leading Jet Trimmed Mass [GeV]" );
	histos2D_[ "jetTrimmedMassHTPassing_cutMassAsym" ]->Sumw2();

	histos2D_[ "jetTrimmedMassHTDenom_cutJetsPt" ] = fs_->make< TH2D >( "jetTrimmedMassHTDenom_cutJetsPt", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetTrimmedMassHTDenom_cutJetsPt" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetTrimmedMassHTDenom_cutJetsPt" ]->SetXTitle( "Leading Jet Trimmed Mass [GeV]" );
	histos2D_[ "jetTrimmedMassHTDenom_cutJetsPt" ]->Sumw2();

	histos2D_[ "jetTrimmedMassHTPassing_cutJetsPt" ] = fs_->make< TH2D >( "jetTrimmedMassHTPassing_cutJetsPt", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetTrimmedMassHTPassing_cutJetsPt" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetTrimmedMassHTPassing_cutJetsPt" ]->SetXTitle( "Leading Jet Trimmed Mass [GeV]" );
	histos2D_[ "jetTrimmedMassHTPassing_cutJetsPt" ]->Sumw2();

	histos2D_[ "massAveHTDenom_noTrigger" ] = fs_->make< TH2D >( "massAveHTDenom_noTrigger", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "massAveHTDenom_noTrigger" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "massAveHTDenom_noTrigger" ]->SetXTitle( "Average Pruned Mass [GeV]" );
	histos2D_[ "massAveHTDenom_noTrigger" ]->Sumw2();

	histos2D_[ "massAveHTDenom_triggerOne" ] = fs_->make< TH2D >( "massAveHTDenom_triggerOne", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "massAveHTDenom_triggerOne" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "massAveHTDenom_triggerOne" ]->SetXTitle( "Average Pruned Mass [GeV]" );
	histos2D_[ "massAveHTDenom_triggerOne" ]->Sumw2();

	histos2D_[ "massAveHTDenom_triggerTwo" ] = fs_->make< TH2D >( "massAveHTDenom_triggerTwo", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "massAveHTDenom_triggerTwo" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "massAveHTDenom_triggerTwo" ]->SetXTitle( "Average Pruned Mass [GeV]" );
	histos2D_[ "massAveHTDenom_triggerTwo" ]->Sumw2();

	histos2D_[ "massAveHTDenom_triggerOneAndTwo" ] = fs_->make< TH2D >( "massAveHTDenom_triggerOneAndTwo", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "massAveHTDenom_triggerOneAndTwo" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "massAveHTDenom_triggerOneAndTwo" ]->SetXTitle( "Average Pruned Mass [GeV]" );
	histos2D_[ "massAveHTDenom_triggerOneAndTwo" ]->Sumw2();

	histos2D_[ "massAveHTDenom_cutDijet" ] = fs_->make< TH2D >( "massAveHTDenom_cutDijet", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "massAveHTDenom_cutDijet" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "massAveHTDenom_cutDijet" ]->SetXTitle( "Average Pruned Mass [GeV]" );
	histos2D_[ "massAveHTDenom_cutDijet" ]->Sumw2();

	histos2D_[ "massAveHTPassing_cutDijet" ] = fs_->make< TH2D >( "massAveHTPassing_cutDijet", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "massAveHTPassing_cutDijet" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "massAveHTPassing_cutDijet" ]->SetXTitle( "Average Pruned Mass [GeV]" );
	histos2D_[ "massAveHTPassing_cutDijet" ]->Sumw2();

	histos2D_[ "massAveHTDenom_cutMassAsym" ] = fs_->make< TH2D >( "massAveHTDenom_cutMassAsym", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "massAveHTDenom_cutMassAsym" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "massAveHTDenom_cutMassAsym" ]->SetXTitle( "Average Pruned Mass [GeV]" );
	histos2D_[ "massAveHTDenom_cutMassAsym" ]->Sumw2();

	histos2D_[ "massAveHTPassing_cutMassAsym" ] = fs_->make< TH2D >( "massAveHTPassing_cutMassAsym", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "massAveHTPassing_cutMassAsym" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "massAveHTPassing_cutMassAsym" ]->SetXTitle( "Average Pruned Mass [GeV]" );
	histos2D_[ "massAveHTPassing_cutMassAsym" ]->Sumw2();

	histos2D_[ "massAveHTDenom_cutJetsPt" ] = fs_->make< TH2D >( "massAveHTDenom_cutJetsPt", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "massAveHTDenom_cutJetsPt" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "massAveHTDenom_cutJetsPt" ]->SetXTitle( "Average Pruned Mass [GeV]" );
	histos2D_[ "massAveHTDenom_cutJetsPt" ]->Sumw2();

	histos2D_[ "massAveHTPassing_cutJetsPt" ] = fs_->make< TH2D >( "massAveHTPassing_cutJetsPt", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "massAveHTPassing_cutJetsPt" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "massAveHTPassing_cutJetsPt" ]->SetXTitle( "Average Pruned Mass [GeV]" );
	histos2D_[ "massAveHTPassing_cutJetsPt" ]->Sumw2();

}

// ------------ method called once each job just after ending the event loop  ------------
void RUNBoostedTriggerEfficiency::endJob() {

}

void RUNBoostedTriggerEfficiency::fillDescriptions(edm::ConfigurationDescriptions & descriptions) {

	edm::ParameterSetDescription desc;

	desc.add<double>("cutjet1Ptvalue", 1);
	desc.add<double>("cutjet2Ptvalue", 1);
	desc.add<double>("cutHTvalue", 1);
	desc.add<double>("cutAsymvalue", 1);
	desc.add<double>("cutCosThetavalue", 1);
	//desc.add<double>("cutSubjetPtRatiovalue", 1);
	desc.add<double>("cutTau31value", 1);
	desc.add<double>("cutTau21value", 1);
	//desc.add<double>("cutDEtavalue", 1);
	//desc.add<double>("cutBtagvalue", 1);
	desc.add<bool>("bjSample", false);
	desc.add<string>("baseTrigger", "HLT_PFHT475");
	vector<string> HLTPass;
	HLTPass.push_back("HLT_AK8PFHT700_TrimR0p1PT0p03Mass50");
	desc.add<vector<string>>("triggerPass",	HLTPass);

	desc.add<InputTag>("Lumi", 	InputTag("eventInfo:evtInfoLumiBlock"));
	desc.add<InputTag>("Run", 	InputTag("eventInfo:evtInfoRunNumber"));
	desc.add<InputTag>("Event", 	InputTag("eventInfo:evtInfoEventNumber"));
	desc.add<InputTag>("NPV", 	InputTag("eventUserData:npv"));
	desc.add<InputTag>("jetAk4Pt", 	InputTag("jetsAK4:jetAK4Pt"));
	desc.add<InputTag>("jetPt", 	InputTag("jetsAK8:jetAK8Pt"));
	desc.add<InputTag>("jetEta", 	InputTag("jetsAK8:jetAK8Eta"));
	desc.add<InputTag>("jetPhi", 	InputTag("jetsAK8:jetAK8Phi"));
	desc.add<InputTag>("jetE", 	InputTag("jetsAK8:jetAK8E"));
	desc.add<InputTag>("jetMass", 	InputTag("jetsAK8:jetAK8prunedMass"));
	desc.add<InputTag>("jetTrimmedMass", 	InputTag("jetsAK8:jetAK8trimmedMass"));
	desc.add<InputTag>("jetTau1", 	InputTag("jetsAK8:jetAK8tau1"));
	desc.add<InputTag>("jetTau2", 	InputTag("jetsAK8:jetAK8tau2"));
	desc.add<InputTag>("jetTau3", 	InputTag("jetsAK8:jetAK8tau3"));
	desc.add<InputTag>("jetNSubjets", 	InputTag("jetsAK8:jetAK8nSubjets"));
	desc.add<InputTag>("jetSubjetIndex0", 	InputTag("jetsAK8:jetAK8vSubjetIndex0"));
	desc.add<InputTag>("jetSubjetIndex1", 	InputTag("jetsAK8:jetAK8vSubjetIndex1"));
	desc.add<InputTag>("jetSubjetIndex2", 	InputTag("jetsAK8:jetAK8vSubjetIndex2"));
	desc.add<InputTag>("jetSubjetIndex3", 	InputTag("jetsAK8:jetAK8vSubjetIndex3"));
	desc.add<InputTag>("jetKeys", 	InputTag("jetKeysAK8"));
	desc.add<InputTag>("jetCSV", 	InputTag("jetsAK8:jetAK8CSV"));
	desc.add<InputTag>("jetCSVV1", 	InputTag("jetsAK8:jetAK8CSVV1"));
	// JetID
	desc.add<InputTag>("jecFactor", 		InputTag("jetsAK8:jetAK8jecFactor0"));
	desc.add<InputTag>("neutralHadronEnergy", 	InputTag("jetsAK8:jetAK8neutralHadronEnergy"));
	desc.add<InputTag>("neutralEmEnergy", 		InputTag("jetsAK8:jetAK8neutralEmEnergy"));
	desc.add<InputTag>("chargedEmEnergy", 		InputTag("jetsAK8:jetAK8chargedEmEnergy"));
	desc.add<InputTag>("muonEnergy", 		InputTag("jetsAK8:jetAK8MuonEnergy"));
	desc.add<InputTag>("chargedHadronEnergy", 	InputTag("jetsAK8:jetAK8chargedHadronEnergy"));
	desc.add<InputTag>("chargedHadronMultiplicity",	InputTag("jetsAK8:jetAK8ChargedHadronMultiplicity"));
	desc.add<InputTag>("neutralHadronMultiplicity",	InputTag("jetsAK8:jetAK8neutralHadronMultiplicity"));
	desc.add<InputTag>("chargedMultiplicity", 	InputTag("jetsAK8:jetAK8chargedMultiplicity"));
	// Trigger
	desc.add<InputTag>("triggerBit",		InputTag("TriggerUserData:triggerBitTree"));
	desc.add<InputTag>("triggerName",		InputTag("TriggerUserData:triggerNameTree"));
	// Subjets
	desc.add<InputTag>("subjetPt", 	InputTag("subjetsAK8:subjetAK8Pt"));
	desc.add<InputTag>("subjetEta", 	InputTag("subjetsAK8:subjetAK8Eta"));
	desc.add<InputTag>("subjetPhi", 	InputTag("subjetsAK8:subjetAK8Phi"));
	desc.add<InputTag>("subjetE", 	InputTag("subjetsAK8:subjetAK8E"));
	desc.add<InputTag>("subjetMass", 	InputTag("subjetsAK8:subjetAK8Mass"));
	descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(RUNBoostedTriggerEfficiency);
