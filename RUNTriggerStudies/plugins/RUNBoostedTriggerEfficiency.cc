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
      EDGetTokenT<vector<float>> jetPrunedMass_;
      EDGetTokenT<vector<float>> jetFilteredMass_;
      EDGetTokenT<vector<float>> jetSoftDropMass_;
      EDGetTokenT<vector<float>> jetTau1_;
      EDGetTokenT<vector<float>> jetTau2_;
      EDGetTokenT<vector<float>> jetTau3_;
      EDGetTokenT<vector<float>> jetNSubjets_;
      EDGetTokenT<vector<float>> jetSubjetIndex0_;
      EDGetTokenT<vector<float>> jetSubjetIndex1_;
      EDGetTokenT<vector<float>> jetSubjetIndex2_;
      EDGetTokenT<vector<float>> jetSubjetIndex3_;
      EDGetTokenT<vector<vector<int>>> jetKeys_;
      EDGetTokenT<vector<float>> jetCSVv2_;
      EDGetTokenT<vector<float>> jetCSVv2V1_;
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
	jetPrunedMass_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetPrunedMass"))),
	jetFilteredMass_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetFilteredMass"))),
	jetSoftDropMass_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetSoftDropMass"))),
	jetTau1_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetTau1"))),
	jetTau2_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetTau2"))),
	jetTau3_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetTau3"))),
	jetNSubjets_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetNSubjets"))),
	jetSubjetIndex0_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetSubjetIndex0"))),
	jetSubjetIndex1_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetSubjetIndex1"))),
	jetSubjetIndex2_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetSubjetIndex2"))),
	jetSubjetIndex3_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetSubjetIndex3"))),
	jetKeys_(consumes<vector<vector<int>>>(iConfig.getParameter<InputTag>("jetKeys"))),
	jetCSVv2_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetCSVv2"))),
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

	Handle<vector<float> > jetPrunedMass;
	iEvent.getByToken(jetPrunedMass_, jetPrunedMass);

	Handle<vector<float> > jetFilteredMass;
	iEvent.getByToken(jetFilteredMass_, jetFilteredMass);

	Handle<vector<float> > jetSoftDropMass;
	iEvent.getByToken(jetSoftDropMass_, jetSoftDropMass);

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

	Handle<vector<float> > jetCSVv2;
	iEvent.getByToken(jetCSVv2_, jetCSVv2);

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
	bool ORTriggers = checkORListOfTriggerBits( triggerName, triggerBit, triggerPass );

	/// Applying kinematic, trigger and jet ID
	vector< myJet > JETS;
	vector< float > tmpTriggerMass;
	vector< float > tmpMass;
	bool bTagCSVv2 = 0;
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

			//if ( (*jetCSVv2)[i] > 0.244 ) bTagCSVv2 = 1; 	// CSVv2L
			if ( (*jetCSVv2)[i] > 0.679 ) bTagCSVv2 = 1; 	// CSVv2M
			//if ( (*jetCSVv2V1)[i] > 0.405 ) bTagCSVv2 = 1; 	// CSVv2V1L
			//if ( (*jetCSVv2V1)[i] > 0.783 ) bTagCSVv2 = 1; 	// CSVv2V1M

			myJet tmpJET;
			tmpJET.p4 = tmpJet;
			tmpJET.subjet0 = tmpSubjet0;
			tmpJET.subjet1 = tmpSubjet1;
			tmpJET.mass = (*jetMass)[i];
			tmpJET.trimmedMass = (*jetTrimmedMass)[i] ;
			tmpJET.prunedMass = (*jetPrunedMass)[i] ;
			tmpJET.filteredMass = (*jetFilteredMass)[i] ;
			tmpJET.softDropMass = (*jetSoftDropMass)[i] ;
			tmpJET.tau1 = (*jetTau1)[i];
			tmpJET.tau2 = (*jetTau2)[i];
			tmpJET.tau3 = (*jetTau3)[i];
			tmpJET.btagCSVv2 = bTagCSVv2;
			JETS.push_back( tmpJET );
	   
		}
	}

	sort(tmpTriggerMass.begin(), tmpTriggerMass.end(), [](const float p1, const float p2) { return p1 > p2; }); 
	float trimmedMass = -999;
	if ( ( tmpTriggerMass.size()> 0 ) ) trimmedMass = tmpTriggerMass[0];
	tmpTriggerMass.clear();
	
	if (HT > 0 ) { 
		histos2D_[ "jetPrunedMassHT_noTrigger" ]->Fill( JETS[0].mass, HT );
		histos2D_[ "jetTrimmedMassHT_noTrigger" ]->Fill( trimmedMass, HT );
	}

	/// THIS IS MORE HISTORIC, DONT USE IT ANYMORE
	if ( basedTriggerFired || ORTriggers ) {
		if ( basedTriggerFired && ORTriggers ) {
			if(JETS.size() > 0) histos2D_[ "jetPrunedMassHT_triggerOneAndTwo" ]->Fill( JETS[0].mass, HT );
			histos2D_[ "jetTrimmedMassHT_triggerOneAndTwo" ]->Fill( trimmedMass, HT );
		} else if ( basedTriggerFired ) {
			if(JETS.size() > 0) histos2D_[ "jetPrunedMassHT_triggerOne" ]->Fill( JETS[0].mass, HT );
			histos2D_[ "jetTrimmedMassHT_triggerOne" ]->Fill( trimmedMass, HT );
		} else if ( ORTriggers ) {
			if(JETS.size() > 0) histos2D_[ "jetPrunedMassHT_triggerTwo" ]->Fill( JETS[0].mass, HT );
			histos2D_[ "jetTrimmedMassHT_triggerTwo" ]->Fill( trimmedMass, HT );
		}
	}
	////////////////////////////////////////////////////////////////////////


	//// test ak4 
	float ak4HT = 0;
	for (size_t i = 0; i < jetAk4Pt->size(); i++) ak4HT += (*jetAk4Pt)[i];
	///////////////////

	vector<TLorentzVector> jet1SubjetsTLV, jet2SubjetsTLV;
	if ( JETS.size() > 1 ) {

		// Mass average 
		//float massAve = massAverage( JETS[0].mass, JETS[1].mass );
		//float trimmedMassAve = massAverage( JETS[0].trimmedMass, JETS[1].trimmedMass );
		float prunedMassAve = massAverage( JETS[0].prunedMass, JETS[1].prunedMass );
		//float filteredMassAve = massAverage( JETS[0].filteredMass, JETS[1].filteredMass );
		//float softDropMassAve = massAverage( JETS[0].softDropMass, JETS[1].softDropMass );
		//////////////////////////////////////////////////////////////////////////


		
		histos2D_[ "jetPrunedMassHT_cutDijet_noTrigger" ]->Fill( JETS[0].prunedMass, HT );
		histos2D_[ "jetTrimmedMassHT_cutDijet_noTrigger" ]->Fill( trimmedMass, HT );
		if ( basedTriggerFired || ORTriggers ) {
			if ( basedTriggerFired && ORTriggers ) {
				histos2D_[ "jetPrunedMassHT_cutDijet_triggerOneAndTwo" ]->Fill( JETS[0].prunedMass, HT );
				histos2D_[ "jetTrimmedMassHT_cutDijet_triggerOneAndTwo" ]->Fill( trimmedMass, HT );
			} else if ( basedTriggerFired ) {
				histos2D_[ "jetPrunedMassHT_cutDijet_triggerOne" ]->Fill( JETS[0].prunedMass, HT );
				histos2D_[ "jetTrimmedMassHT_cutDijet_triggerOne" ]->Fill( trimmedMass, HT );
			} else if ( ORTriggers ) {
				histos2D_[ "jetPrunedMassHT_cutDijet_triggerTwo" ]->Fill( JETS[0].prunedMass, HT );
				histos2D_[ "jetTrimmedMassHT_cutDijet_triggerTwo" ]->Fill( trimmedMass, HT );
			}
		}

		if ( basedTriggerFired ) {
			histos1D_[ "ak4HTDenom_cutDijet" ]->Fill( ak4HT  );
			histos1D_[ "HTDenom_cutDijet" ]->Fill( HT  );
			histos1D_[ "trimmedMassDenom_cutDijet" ]->Fill( trimmedMass  );
			histos1D_[ "prunedMassAveDenom_cutDijet" ]->Fill( prunedMassAve  );
			histos1D_[ "jet1PrunedMassDenom_cutDijet" ]->Fill( JETS[0].prunedMass  );
			histos1D_[ "jet1SoftDropMassDenom_cutDijet" ]->Fill( JETS[0].softDropMass  );
			histos1D_[ "jet1PtDenom_cutDijet" ]->Fill( JETS[0].p4.Pt()   );
			histos1D_[ "jet2PtDenom_cutDijet" ]->Fill( JETS[1].p4.Pt()   );
			histos2D_[ "jet1PtHTDenom_cutDijet" ]->Fill( JETS[0].p4.Pt(), HT );
			histos2D_[ "jet2PtHTDenom_cutDijet" ]->Fill( JETS[1].p4.Pt(), HT );
			histos2D_[ "jet1PtPrunedMassDenom_cutDijet" ]->Fill( JETS[0].p4.Pt(), JETS[0].prunedMass );
			histos2D_[ "jet2PtPrunedMassDenom_cutDijet" ]->Fill( JETS[1].p4.Pt(), JETS[1].prunedMass );
			histos2D_[ "jet1PtSoftDropMassDenom_cutDijet" ]->Fill( JETS[0].p4.Pt(), JETS[0].softDropMass );
			histos2D_[ "jet2PtSoftDropMassDenom_cutDijet" ]->Fill( JETS[1].p4.Pt(), JETS[1].softDropMass );
			histos2D_[ "jetPrunedMassHTDenom_cutDijet" ]->Fill( JETS[0].prunedMass, HT );
			histos2D_[ "jetSoftDropMassHTDenom_cutDijet" ]->Fill( JETS[0].softDropMass, HT );
			histos2D_[ "jetTrimmedMassHTDenom_cutDijet" ]->Fill( trimmedMass, HT );
			histos2D_[ "prunedMassAveHTDenom_cutDijet" ]->Fill( prunedMassAve, HT );

			if ( ORTriggers ){
				histos1D_[ "ak4HTPassing_cutDijet" ]->Fill( ak4HT  );
				histos1D_[ "HTPassing_cutDijet" ]->Fill( HT  );
				histos1D_[ "trimmedMassPassing_cutDijet" ]->Fill( trimmedMass  );
				histos1D_[ "prunedMassAvePassing_cutDijet" ]->Fill( prunedMassAve  );
				histos1D_[ "jet1PrunedMassPassing_cutDijet" ]->Fill( JETS[0].prunedMass  );
				histos1D_[ "jet1SoftDropMassPassing_cutDijet" ]->Fill( JETS[0].softDropMass  );
				histos1D_[ "jet1PtPassing_cutDijet" ]->Fill( JETS[0].p4.Pt()   );
				histos1D_[ "jet2PtPassing_cutDijet" ]->Fill( JETS[1].p4.Pt()   );
				histos2D_[ "jet1PtHTPassing_cutDijet" ]->Fill( JETS[0].p4.Pt(), HT );
				histos2D_[ "jet2PtHTPassing_cutDijet" ]->Fill( JETS[1].p4.Pt(), HT );
				histos2D_[ "jet1PtPrunedMassPassing_cutDijet" ]->Fill( JETS[0].p4.Pt(), JETS[0].prunedMass );
				histos2D_[ "jet2PtPrunedMassPassing_cutDijet" ]->Fill( JETS[1].p4.Pt(), JETS[1].prunedMass );
				histos2D_[ "jet1PtSoftDropMassPassing_cutDijet" ]->Fill( JETS[0].p4.Pt(), JETS[0].softDropMass );
				histos2D_[ "jet2PtSoftDropMassPassing_cutDijet" ]->Fill( JETS[1].p4.Pt(), JETS[1].softDropMass );
				histos2D_[ "jetPrunedMassHTPassing_cutDijet" ]->Fill( JETS[0].prunedMass, HT );
				histos2D_[ "jetSoftDropMassHTPassing_cutDijet" ]->Fill( JETS[0].softDropMass, HT );
				histos2D_[ "jetTrimmedMassHTPassing_cutDijet" ]->Fill( trimmedMass, HT );
				histos2D_[ "prunedMassAveHTPassing_cutDijet" ]->Fill( prunedMassAve, HT );
			}

			if ( HT > 900 ) {
				histos1D_[ "ak4HTDenom_cutHT" ]->Fill( ak4HT  );
				histos1D_[ "HTDenom_cutHT" ]->Fill( HT  );
				histos1D_[ "trimmedMassDenom_cutHT" ]->Fill( trimmedMass  );
				histos1D_[ "prunedMassAveDenom_cutHT" ]->Fill( prunedMassAve  );
				histos1D_[ "jet1PrunedMassDenom_cutHT" ]->Fill( JETS[0].prunedMass  );
				histos1D_[ "jet1SoftDropMassDenom_cutHT" ]->Fill( JETS[0].softDropMass  );
				histos1D_[ "jet1PtDenom_cutHT" ]->Fill( JETS[0].p4.Pt()   );
				histos1D_[ "jet2PtDenom_cutHT" ]->Fill( JETS[1].p4.Pt()   );
				histos2D_[ "jet1PtHTDenom_cutHT" ]->Fill( JETS[0].p4.Pt(), HT );
				histos2D_[ "jet2PtHTDenom_cutHT" ]->Fill( JETS[1].p4.Pt(), HT );
				histos2D_[ "jet1PtPrunedMassDenom_cutHT" ]->Fill( JETS[0].p4.Pt(), JETS[0].prunedMass );
				histos2D_[ "jet2PtPrunedMassDenom_cutHT" ]->Fill( JETS[1].p4.Pt(), JETS[1].prunedMass );
				histos2D_[ "jet1PtSoftDropMassDenom_cutHT" ]->Fill( JETS[0].p4.Pt(), JETS[0].softDropMass );
				histos2D_[ "jet2PtSoftDropMassDenom_cutHT" ]->Fill( JETS[1].p4.Pt(), JETS[1].softDropMass );
				histos2D_[ "jetPrunedMassHTDenom_cutHT" ]->Fill( JETS[0].prunedMass, HT );
				histos2D_[ "jetSoftDropMassHTDenom_cutHT" ]->Fill( JETS[0].softDropMass, HT );
				histos2D_[ "jetTrimmedMassHTDenom_cutHT" ]->Fill( trimmedMass, HT );
				histos2D_[ "prunedMassAveHTDenom_cutHT" ]->Fill( prunedMassAve, HT );
				if ( ORTriggers ){
					histos1D_[ "ak4HTPassing_cutHT" ]->Fill( ak4HT  );
					histos1D_[ "HTPassing_cutHT" ]->Fill( HT  );
					histos1D_[ "trimmedMassPassing_cutHT" ]->Fill( trimmedMass  );
					histos1D_[ "prunedMassAvePassing_cutHT" ]->Fill( prunedMassAve  );
					histos1D_[ "jet1PrunedMassPassing_cutHT" ]->Fill( JETS[0].prunedMass  );
					histos1D_[ "jet1SoftDropMassPassing_cutHT" ]->Fill( JETS[0].softDropMass  );
					histos1D_[ "jet1PtPassing_cutHT" ]->Fill( JETS[0].p4.Pt()   );
					histos1D_[ "jet2PtPassing_cutHT" ]->Fill( JETS[1].p4.Pt()   );
					histos2D_[ "jet1PtHTPassing_cutHT" ]->Fill( JETS[0].p4.Pt(), HT );
					histos2D_[ "jet2PtHTPassing_cutHT" ]->Fill( JETS[1].p4.Pt(), HT );
					histos2D_[ "jet1PtPrunedMassPassing_cutHT" ]->Fill( JETS[0].p4.Pt(), JETS[0].prunedMass );
					histos2D_[ "jet2PtPrunedMassPassing_cutHT" ]->Fill( JETS[1].p4.Pt(), JETS[1].prunedMass );
					histos2D_[ "jet1PtSoftDropMassPassing_cutHT" ]->Fill( JETS[0].p4.Pt(), JETS[0].softDropMass );
					histos2D_[ "jet2PtSoftDropMassPassing_cutHT" ]->Fill( JETS[1].p4.Pt(), JETS[1].softDropMass );
					histos2D_[ "jetPrunedMassHTPassing_cutHT" ]->Fill( JETS[0].prunedMass, HT );
					histos2D_[ "jetSoftDropMassHTPassing_cutHT" ]->Fill( JETS[0].softDropMass, HT );
					histos2D_[ "jetTrimmedMassHTPassing_cutHT" ]->Fill( trimmedMass, HT );
					histos2D_[ "prunedMassAveHTPassing_cutHT" ]->Fill( prunedMassAve, HT );
				}
			}


			if ( ( JETS[0].p4.Pt() > cutjet1Ptvalue ) && ( JETS[1].p4.Pt() > cutjet2Ptvalue ) ) {
				histos1D_[ "ak4HTDenom_cutTriggerEff" ]->Fill( ak4HT  );
				histos1D_[ "HTDenom_cutTriggerEff" ]->Fill( HT  );
				histos1D_[ "trimmedMassDenom_cutTriggerEff" ]->Fill( trimmedMass  );
				histos1D_[ "prunedMassAveDenom_cutTriggerEff" ]->Fill( prunedMassAve  );
				histos1D_[ "jet1PrunedMassDenom_cutTriggerEff" ]->Fill( JETS[0].prunedMass  );
				histos1D_[ "jet1SoftDropMassDenom_cutTriggerEff" ]->Fill( JETS[0].softDropMass  );
				histos1D_[ "jet1PtDenom_cutTriggerEff" ]->Fill( JETS[0].p4.Pt()   );
				histos1D_[ "jet2PtDenom_cutTriggerEff" ]->Fill( JETS[1].p4.Pt()   );
				histos2D_[ "jet1PtHTDenom_cutTriggerEff" ]->Fill( JETS[0].p4.Pt(), HT );
				histos2D_[ "jet2PtHTDenom_cutTriggerEff" ]->Fill( JETS[1].p4.Pt(), HT );
				histos2D_[ "jet1PtPrunedMassDenom_cutTriggerEff" ]->Fill( JETS[0].p4.Pt(), JETS[0].prunedMass );
				histos2D_[ "jet2PtPrunedMassDenom_cutTriggerEff" ]->Fill( JETS[1].p4.Pt(), JETS[1].prunedMass );
				histos2D_[ "jet1PtSoftDropMassDenom_cutTriggerEff" ]->Fill( JETS[0].p4.Pt(), JETS[0].softDropMass );
				histos2D_[ "jet2PtSoftDropMassDenom_cutTriggerEff" ]->Fill( JETS[1].p4.Pt(), JETS[1].softDropMass );
				histos2D_[ "jetPrunedMassHTDenom_cutTriggerEff" ]->Fill( JETS[0].prunedMass, HT );
				histos2D_[ "jetSoftDropMassHTDenom_cutTriggerEff" ]->Fill( JETS[0].softDropMass, HT );
				histos2D_[ "jetTrimmedMassHTDenom_cutTriggerEff" ]->Fill( trimmedMass, HT );
				histos2D_[ "prunedMassAveHTDenom_cutTriggerEff" ]->Fill( prunedMassAve, HT );
				if ( ORTriggers ){
					histos1D_[ "ak4HTPassing_cutTriggerEff" ]->Fill( ak4HT  );
					histos1D_[ "HTPassing_cutTriggerEff" ]->Fill( HT  );
					histos1D_[ "trimmedMassPassing_cutTriggerEff" ]->Fill( trimmedMass  );
					histos1D_[ "prunedMassAvePassing_cutTriggerEff" ]->Fill( prunedMassAve  );
					histos1D_[ "jet1PrunedMassPassing_cutTriggerEff" ]->Fill( JETS[0].prunedMass  );
					histos1D_[ "jet1SoftDropMassPassing_cutTriggerEff" ]->Fill( JETS[0].softDropMass  );
					histos1D_[ "jet1PtPassing_cutTriggerEff" ]->Fill( JETS[0].p4.Pt()   );
					histos1D_[ "jet2PtPassing_cutTriggerEff" ]->Fill( JETS[1].p4.Pt()   );
					histos2D_[ "jet1PtHTPassing_cutTriggerEff" ]->Fill( JETS[0].p4.Pt(), HT );
					histos2D_[ "jet2PtHTPassing_cutTriggerEff" ]->Fill( JETS[1].p4.Pt(), HT );
					histos2D_[ "jet1PtPrunedMassPassing_cutTriggerEff" ]->Fill( JETS[0].p4.Pt(), JETS[0].prunedMass );
					histos2D_[ "jet2PtPrunedMassPassing_cutTriggerEff" ]->Fill( JETS[1].p4.Pt(), JETS[1].prunedMass );
					histos2D_[ "jet1PtSoftDropMassPassing_cutTriggerEff" ]->Fill( JETS[0].p4.Pt(), JETS[0].softDropMass );
					histos2D_[ "jet2PtSoftDropMassPassing_cutTriggerEff" ]->Fill( JETS[1].p4.Pt(), JETS[1].softDropMass );
					histos2D_[ "jetPrunedMassHTPassing_cutTriggerEff" ]->Fill( JETS[0].prunedMass, HT );
					histos2D_[ "jetSoftDropMassHTPassing_cutTriggerEff" ]->Fill( JETS[0].softDropMass, HT );
					histos2D_[ "jetTrimmedMassHTPassing_cutTriggerEff" ]->Fill( trimmedMass, HT );
					histos2D_[ "prunedMassAveHTPassing_cutTriggerEff" ]->Fill( prunedMassAve, HT );
				}
			}

		}
	}

	if ( JETS.size() > 1 ) {

		if ( basedTriggerFired ) {
			histos1D_[ "HTDenom_cutJet" ]->Fill( HT  );
			histos1D_[ "trimmedMassDenom_cutJet" ]->Fill( trimmedMass  );
			histos1D_[ "jet1PrunedMassDenom_cutJet" ]->Fill( JETS[0].prunedMass  );
			histos1D_[ "jet1SoftDropMassDenom_cutJet" ]->Fill( JETS[0].softDropMass  );
			histos1D_[ "jet1PtDenom_cutJet" ]->Fill( JETS[0].p4.Pt()   );
			histos2D_[ "jet1PtHTDenom_cutJet" ]->Fill( JETS[0].p4.Pt(), HT );
			histos2D_[ "jet1PtPrunedMassDenom_cutJet" ]->Fill( JETS[0].p4.Pt(), JETS[0].prunedMass );
			histos2D_[ "jet1PtSoftDropMassDenom_cutJet" ]->Fill( JETS[0].p4.Pt(), JETS[0].softDropMass );
			histos2D_[ "jetPrunedMassHTDenom_cutJet" ]->Fill( JETS[0].prunedMass, HT );
			histos2D_[ "jetSoftDropMassHTDenom_cutJet" ]->Fill( JETS[0].softDropMass, HT );
			histos2D_[ "jetTrimmedMassHTDenom_cutJet" ]->Fill( trimmedMass, HT );

			if ( ORTriggers ){
				histos1D_[ "HTPassing_cutJet" ]->Fill( HT  );
				histos1D_[ "trimmedMassPassing_cutJet" ]->Fill( trimmedMass  );
				histos1D_[ "jet1PrunedMassPassing_cutJet" ]->Fill( JETS[0].prunedMass  );
				histos1D_[ "jet1SoftDropMassPassing_cutJet" ]->Fill( JETS[0].softDropMass  );
				histos1D_[ "jet1PtPassing_cutJet" ]->Fill( JETS[0].p4.Pt()   );
				histos2D_[ "jet1PtHTPassing_cutJet" ]->Fill( JETS[0].p4.Pt(), HT );
				histos2D_[ "jet1PtPrunedMassPassing_cutJet" ]->Fill( JETS[0].p4.Pt(), JETS[0].prunedMass );
				histos2D_[ "jet1PtSoftDropMassPassing_cutJet" ]->Fill( JETS[0].p4.Pt(), JETS[0].softDropMass );
				histos2D_[ "jetPrunedMassHTPassing_cutJet" ]->Fill( JETS[0].prunedMass, HT );
				histos2D_[ "jetSoftDropMassHTPassing_cutJet" ]->Fill( JETS[0].softDropMass, HT );
				histos2D_[ "jetTrimmedMassHTPassing_cutJet" ]->Fill( trimmedMass, HT );
			}
		}

		if ( JETS[0].p4.Pt() > 400 ) {
			
			if ( basedTriggerFired ) {
				histos1D_[ "HTDenom_cutJetPt" ]->Fill( HT  );
				histos1D_[ "trimmedMassDenom_cutJetPt" ]->Fill( trimmedMass  );
				histos1D_[ "jet1PrunedMassDenom_cutJetPt" ]->Fill( JETS[0].prunedMass  );
				histos1D_[ "jet1SoftDropMassDenom_cutJetPt" ]->Fill( JETS[0].softDropMass  );
				histos1D_[ "jet1PtDenom_cutJetPt" ]->Fill( JETS[0].p4.Pt()   );
				histos2D_[ "jet1PtHTDenom_cutJetPt" ]->Fill( JETS[0].p4.Pt(), HT );
				histos2D_[ "jet1PtPrunedMassDenom_cutJetPt" ]->Fill( JETS[0].p4.Pt(), JETS[0].prunedMass );
				histos2D_[ "jet1PtSoftDropMassDenom_cutJetPt" ]->Fill( JETS[0].p4.Pt(), JETS[0].softDropMass );
				histos2D_[ "jetPrunedMassHTDenom_cutJetPt" ]->Fill( JETS[0].prunedMass, HT );
				histos2D_[ "jetSoftDropMassHTDenom_cutJetPt" ]->Fill( JETS[0].softDropMass, HT );
				histos2D_[ "jetTrimmedMassHTDenom_cutJetPt" ]->Fill( trimmedMass, HT );

				if ( ORTriggers ){
					histos1D_[ "HTPassing_cutJetPt" ]->Fill( HT  );
					histos1D_[ "trimmedMassPassing_cutJetPt" ]->Fill( trimmedMass  );
					histos1D_[ "jet1PrunedMassPassing_cutJetPt" ]->Fill( JETS[0].prunedMass  );
					histos1D_[ "jet1SoftDropMassPassing_cutJetPt" ]->Fill( JETS[0].softDropMass  );
					histos1D_[ "jet1PtPassing_cutJetPt" ]->Fill( JETS[0].p4.Pt()   );
					histos2D_[ "jet1PtHTPassing_cutJetPt" ]->Fill( JETS[0].p4.Pt(), HT );
					histos2D_[ "jet1PtPrunedMassPassing_cutJetPt" ]->Fill( JETS[0].p4.Pt(), JETS[0].prunedMass );
					histos2D_[ "jet1PtSoftDropMassPassing_cutJetPt" ]->Fill( JETS[0].p4.Pt(), JETS[0].softDropMass );
					histos2D_[ "jetPrunedMassHTPassing_cutJetPt" ]->Fill( JETS[0].prunedMass, HT );
					histos2D_[ "jetSoftDropMassHTPassing_cutJetPt" ]->Fill( JETS[0].softDropMass, HT );
					histos2D_[ "jetTrimmedMassHTPassing_cutJetPt" ]->Fill( trimmedMass, HT );
				}
			}
		}
	}
	JETS.clear();

}


// ------------ method called once each job just before starting event loop  ------------
void RUNBoostedTriggerEfficiency::beginJob() {

	histos2D_[ "jetPrunedMassHT_noTrigger" ] = fs_->make< TH2D >( "jetPrunedMassHT_noTrigger", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetPrunedMassHT_noTrigger" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetPrunedMassHT_noTrigger" ]->SetXTitle( "Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jetPrunedMassHT_noTrigger" ]->Sumw2();

	histos2D_[ "jetTrimmedMassHT_noTrigger" ] = fs_->make< TH2D >( "jetTrimmedMassHT_noTrigger", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetTrimmedMassHT_noTrigger" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetTrimmedMassHT_noTrigger" ]->SetXTitle( "Leading Jet Trimmed Mass [GeV]" );
	histos2D_[ "jetTrimmedMassHT_noTrigger" ]->Sumw2();

	histos2D_[ "jetPrunedMassHT_triggerOne" ] = fs_->make< TH2D >( "jetPrunedMassHT_triggerOne", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetPrunedMassHT_triggerOne" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetPrunedMassHT_triggerOne" ]->SetXTitle( "Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jetPrunedMassHT_triggerOne" ]->Sumw2();

	histos2D_[ "jetPrunedMassHT_triggerTwo" ] = fs_->make< TH2D >( "jetPrunedMassHT_triggerTwo", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetPrunedMassHT_triggerTwo" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetPrunedMassHT_triggerTwo" ]->SetXTitle( "Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jetPrunedMassHT_triggerTwo" ]->Sumw2();

	histos2D_[ "jetPrunedMassHT_triggerOneAndTwo" ] = fs_->make< TH2D >( "jetPrunedMassHT_triggerOneAndTwo", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetPrunedMassHT_triggerOneAndTwo" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetPrunedMassHT_triggerOneAndTwo" ]->SetXTitle( "Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jetPrunedMassHT_triggerOneAndTwo" ]->Sumw2();


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

	histos2D_[ "jetPrunedMassHT_cutDijet_noTrigger" ] = fs_->make< TH2D >( "jetPrunedMassHT_cutDijet_noTrigger", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetPrunedMassHT_cutDijet_noTrigger" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetPrunedMassHT_cutDijet_noTrigger" ]->SetXTitle( "Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jetPrunedMassHT_cutDijet_noTrigger" ]->Sumw2();

	histos2D_[ "jetPrunedMassHT_cutDijet_triggerOne" ] = fs_->make< TH2D >( "jetPrunedMassHT_cutDijet_triggerOne", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetPrunedMassHT_cutDijet_triggerOne" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetPrunedMassHT_cutDijet_triggerOne" ]->SetXTitle( "Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jetPrunedMassHT_cutDijet_triggerOne" ]->Sumw2();

	histos2D_[ "jetPrunedMassHT_cutDijet_triggerTwo" ] = fs_->make< TH2D >( "jetPrunedMassHT_cutDijet_triggerTwo", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetPrunedMassHT_cutDijet_triggerTwo" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetPrunedMassHT_cutDijet_triggerTwo" ]->SetXTitle( "Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jetPrunedMassHT_cutDijet_triggerTwo" ]->Sumw2();

	histos2D_[ "jetPrunedMassHT_cutDijet_triggerOneAndTwo" ] = fs_->make< TH2D >( "jetPrunedMassHT_cutDijet_triggerOneAndTwo", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetPrunedMassHT_cutDijet_triggerOneAndTwo" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetPrunedMassHT_cutDijet_triggerOneAndTwo" ]->SetXTitle( "Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jetPrunedMassHT_cutDijet_triggerOneAndTwo" ]->Sumw2();

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






	histos1D_[ "ak4HTDenom_cutDijet" ] = fs_->make< TH1D >( "ak4HTDenom_cutDijet", "ak4HTDenom_cutDijet", 150, 0., 1500. );
	histos1D_[ "ak4HTDenom_cutDijet" ]->Sumw2();
	histos1D_[ "ak4HTPassing_cutDijet" ] = fs_->make< TH1D >( "ak4HTPassing_cutDijet", "ak4HTPassing_cutDijet", 150, 0., 1500. );
	histos1D_[ "ak4HTPassing_cutDijet" ]->Sumw2();

	histos1D_[ "HTDenom_cutDijet" ] = fs_->make< TH1D >( "HTDenom_cutDijet", "HTDenom_cutDijet", 150, 0., 1500. );
	histos1D_[ "HTDenom_cutDijet" ]->Sumw2();
	histos1D_[ "HTPassing_cutDijet" ] = fs_->make< TH1D >( "HTPassing_cutDijet", "HTPassing_cutDijet", 150, 0., 1500. );
	histos1D_[ "HTPassing_cutDijet" ]->Sumw2();

	histos1D_[ "trimmedMassDenom_cutDijet" ] = fs_->make< TH1D >( "trimmedMassDenom_cutDijet", "trimmedMassDenom_cutDijet", 60, 0., 600. );
	histos1D_[ "trimmedMassDenom_cutDijet" ]->Sumw2();
	histos1D_[ "trimmedMassPassing_cutDijet" ] = fs_->make< TH1D >( "trimmedMassPassing_cutDijet", "trimmedMassPassing_cutDijet", 60, 0., 600. );
	histos1D_[ "trimmedMassPassing_cutDijet" ]->Sumw2();

	histos1D_[ "prunedMassAveDenom_cutDijet" ] = fs_->make< TH1D >( "prunedMassAveDenom_cutDijet", "prunedMassAveDenom_cutDijet", 60, 0., 600. );
	histos1D_[ "prunedMassAveDenom_cutDijet" ]->Sumw2();
	histos1D_[ "prunedMassAvePassing_cutDijet" ] = fs_->make< TH1D >( "prunedMassAvePassing_cutDijet", "prunedMassAvePassing_cutDijet", 60, 0., 600. );
	histos1D_[ "prunedMassAvePassing_cutDijet" ]->Sumw2();

	histos1D_[ "jet1PrunedMassDenom_cutDijet" ] = fs_->make< TH1D >( "jet1PrunedMassDenom_cutDijet", "jet1PrunedMassDenom_cutDijet", 60, 0., 600. );
	histos1D_[ "jet1PrunedMassDenom_cutDijet" ]->Sumw2();
	histos1D_[ "jet1PrunedMassPassing_cutDijet" ] = fs_->make< TH1D >( "jet1PrunedMassPassing_cutDijet", "jet1PrunedMassPassing_cutDijet", 60, 0., 600. );
	histos1D_[ "jet1PrunedMassPassing_cutDijet" ]->Sumw2();

	histos1D_[ "jet1SoftDropMassDenom_cutDijet" ] = fs_->make< TH1D >( "jet1SoftDropMassDenom_cutDijet", "jet1SoftDropMassDenom_cutDijet", 60, 0., 600. );
	histos1D_[ "jet1SoftDropMassDenom_cutDijet" ]->Sumw2();
	histos1D_[ "jet1SoftDropMassPassing_cutDijet" ] = fs_->make< TH1D >( "jet1SoftDropMassPassing_cutDijet", "jet1SoftDropMassPassing_cutDijet", 60, 0., 600. );
	histos1D_[ "jet1SoftDropMassPassing_cutDijet" ]->Sumw2();

	histos1D_[ "jet1PtDenom_cutDijet" ] = fs_->make< TH1D >( "jet1PtDenom_cutDijet", "jet1PtDenom_cutDijet", 150, 0., 1500. );
	histos1D_[ "jet1PtDenom_cutDijet" ]->Sumw2();
	histos1D_[ "jet1PtPassing_cutDijet" ] = fs_->make< TH1D >( "jet1PtPassing_cutDijet", "jet1PtPassing_cutDijet", 150, 0., 1500. );
	histos1D_[ "jet1PtPassing_cutDijet" ]->Sumw2();

	histos1D_[ "jet2PtDenom_cutDijet" ] = fs_->make< TH1D >( "jet2PtDenom_cutDijet", "jet2PtDenom_cutDijet", 150, 0., 1500. );
	histos1D_[ "jet2PtDenom_cutDijet" ]->Sumw2();
	histos1D_[ "jet2PtPassing_cutDijet" ] = fs_->make< TH1D >( "jet2PtPassing_cutDijet", "jet2PtPassing_cutDijet", 150, 0., 1500. );
	histos1D_[ "jet2PtPassing_cutDijet" ]->Sumw2();

	histos2D_[ "jet1PtHTDenom_cutDijet" ] = fs_->make< TH2D >( "jet1PtHTDenom_cutDijet", "HT vs Leading Jet Pt", 150, 0., 1500., 150, 0., 1500.);
	histos2D_[ "jet1PtHTDenom_cutDijet" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jet1PtHTDenom_cutDijet" ]->SetXTitle( "Leading Jet Pt [GeV]" );
	histos2D_[ "jet1PtHTDenom_cutDijet" ]->Sumw2();
	histos2D_[ "jet1PtHTPassing_cutDijet" ] = fs_->make< TH2D >( "jet1PtHTPassing_cutDijet", "HT vs Leading Jet Pt", 150, 0., 1500., 150, 0., 1500.);
	histos2D_[ "jet1PtHTPassing_cutDijet" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jet1PtHTPassing_cutDijet" ]->SetXTitle( "Leading Jet Pt [GeV]" );
	histos2D_[ "jet1PtHTPassing_cutDijet" ]->Sumw2();

	histos2D_[ "jet2PtHTDenom_cutDijet" ] = fs_->make< TH2D >( "jet2PtHTDenom_cutDijet", "HT vs Leading Jet Pt", 150, 0., 1500., 150, 0., 1500.);
	histos2D_[ "jet2PtHTDenom_cutDijet" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jet2PtHTDenom_cutDijet" ]->SetXTitle( "2nd Leading Jet Pt [GeV]" );
	histos2D_[ "jet2PtHTDenom_cutDijet" ]->Sumw2();
	histos2D_[ "jet2PtHTPassing_cutDijet" ] = fs_->make< TH2D >( "jet2PtHTPassing_cutDijet", "HT vs 2nd Leading Jet Pt", 150, 0., 1500., 150, 0., 1500.);
	histos2D_[ "jet2PtHTPassing_cutDijet" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jet2PtHTPassing_cutDijet" ]->SetXTitle( "2nd Leading Jet Pt [GeV]" );
	histos2D_[ "jet2PtHTPassing_cutDijet" ]->Sumw2();

	histos2D_[ "jet1PtPrunedMassDenom_cutDijet" ] = fs_->make< TH2D >( "jet1PtPrunedMassDenom_cutDijet", "Leading Jet Pruned Mass vs Leading Jet Pt", 150, 0., 1500., 60, 0., 600.);
	histos2D_[ "jet1PtPrunedMassDenom_cutDijet" ]->SetYTitle( "Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jet1PtPrunedMassDenom_cutDijet" ]->SetXTitle( "Leading Jet Pt [GeV]" );
	histos2D_[ "jet1PtPrunedMassDenom_cutDijet" ]->Sumw2();
	histos2D_[ "jet1PtPrunedMassPassing_cutDijet" ] = fs_->make< TH2D >( "jet1PtPrunedMassPassing_cutDijet", "Leading Jet Pruned Mass vs Leading Jet Pt", 150, 0., 1500., 60, 0., 600.);
	histos2D_[ "jet1PtPrunedMassPassing_cutDijet" ]->SetYTitle( "Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jet1PtPrunedMassPassing_cutDijet" ]->SetXTitle( "Leading Jet Pt [GeV]" );
	histos2D_[ "jet1PtPrunedMassPassing_cutDijet" ]->Sumw2();

	histos2D_[ "jet2PtPrunedMassDenom_cutDijet" ] = fs_->make< TH2D >( "jet2PtPrunedMassDenom_cutDijet", "Leading Jet Pruned Mass vs Leading Jet Pt", 150, 0., 1500., 60, 0., 600.);
	histos2D_[ "jet2PtPrunedMassDenom_cutDijet" ]->SetYTitle( "2nd Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jet2PtPrunedMassDenom_cutDijet" ]->SetXTitle( "2nd Leading Jet Pt [GeV]" );
	histos2D_[ "jet2PtPrunedMassDenom_cutDijet" ]->Sumw2();
	histos2D_[ "jet2PtPrunedMassPassing_cutDijet" ] = fs_->make< TH2D >( "jet2PtPrunedMassPassing_cutDijet", "Leading Jet Pruned Mass vs 2nd Leading Jet Pt", 150, 0., 1500., 60, 0., 600.);
	histos2D_[ "jet2PtPrunedMassPassing_cutDijet" ]->SetYTitle( "2nd Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jet2PtPrunedMassPassing_cutDijet" ]->SetXTitle( "2nd Leading Jet Pt [GeV]" );
	histos2D_[ "jet2PtPrunedMassPassing_cutDijet" ]->Sumw2();

	histos2D_[ "jet1PtSoftDropMassDenom_cutDijet" ] = fs_->make< TH2D >( "jet1PtSoftDropMassDenom_cutDijet", "Leading Jet SoftDrop Mass vs Leading Jet Pt", 150, 0., 1500., 60, 0., 600.);
	histos2D_[ "jet1PtSoftDropMassDenom_cutDijet" ]->SetYTitle( "Leading Jet SoftDrop Mass [GeV]" );
	histos2D_[ "jet1PtSoftDropMassDenom_cutDijet" ]->SetXTitle( "Leading Jet Pt [GeV]" );
	histos2D_[ "jet1PtSoftDropMassDenom_cutDijet" ]->Sumw2();
	histos2D_[ "jet1PtSoftDropMassPassing_cutDijet" ] = fs_->make< TH2D >( "jet1PtSoftDropMassPassing_cutDijet", "Leading Jet SoftDrop Mass vs Leading Jet Pt", 150, 0., 1500., 60, 0., 600.);
	histos2D_[ "jet1PtSoftDropMassPassing_cutDijet" ]->SetYTitle( "Leading Jet SoftDrop Mass [GeV]" );
	histos2D_[ "jet1PtSoftDropMassPassing_cutDijet" ]->SetXTitle( "Leading Jet Pt [GeV]" );
	histos2D_[ "jet1PtSoftDropMassPassing_cutDijet" ]->Sumw2();

	histos2D_[ "jet2PtSoftDropMassDenom_cutDijet" ] = fs_->make< TH2D >( "jet2PtSoftDropMassDenom_cutDijet", "Leading Jet SoftDrop Mass vs Leading Jet Pt", 150, 0., 1500., 60, 0., 600.);
	histos2D_[ "jet2PtSoftDropMassDenom_cutDijet" ]->SetYTitle( "2nd Leading Jet SoftDrop Mass [GeV]" );
	histos2D_[ "jet2PtSoftDropMassDenom_cutDijet" ]->SetXTitle( "2nd Leading Jet Pt [GeV]" );
	histos2D_[ "jet2PtSoftDropMassDenom_cutDijet" ]->Sumw2();
	histos2D_[ "jet2PtSoftDropMassPassing_cutDijet" ] = fs_->make< TH2D >( "jet2PtSoftDropMassPassing_cutDijet", "Leading Jet SoftDrop Mass vs 2nd Leading Jet Pt", 150, 0., 1500., 60, 0., 600.);
	histos2D_[ "jet2PtSoftDropMassPassing_cutDijet" ]->SetYTitle( "2nd Leading Jet SoftDrop Mass [GeV]" );
	histos2D_[ "jet2PtSoftDropMassPassing_cutDijet" ]->SetXTitle( "2nd Leading Jet Pt [GeV]" );
	histos2D_[ "jet2PtSoftDropMassPassing_cutDijet" ]->Sumw2();

	histos2D_[ "jetPrunedMassHTDenom_cutDijet" ] = fs_->make< TH2D >( "jetPrunedMassHTDenom_cutDijet", "HT vs 2nd Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetPrunedMassHTDenom_cutDijet" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetPrunedMassHTDenom_cutDijet" ]->SetXTitle( "2nd Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jetPrunedMassHTDenom_cutDijet" ]->Sumw2();
	histos2D_[ "jetPrunedMassHTPassing_cutDijet" ] = fs_->make< TH2D >( "jetPrunedMassHTPassing_cutDijet", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetPrunedMassHTPassing_cutDijet" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetPrunedMassHTPassing_cutDijet" ]->SetXTitle( "Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jetPrunedMassHTPassing_cutDijet" ]->Sumw2();

	histos2D_[ "jetSoftDropMassHTDenom_cutDijet" ] = fs_->make< TH2D >( "jetSoftDropMassHTDenom_cutDijet", "HT vs 2nd Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetSoftDropMassHTDenom_cutDijet" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetSoftDropMassHTDenom_cutDijet" ]->SetXTitle( "2nd Leading Jet SoftDrop Mass [GeV]" );
	histos2D_[ "jetSoftDropMassHTDenom_cutDijet" ]->Sumw2();
	histos2D_[ "jetSoftDropMassHTPassing_cutDijet" ] = fs_->make< TH2D >( "jetSoftDropMassHTPassing_cutDijet", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetSoftDropMassHTPassing_cutDijet" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetSoftDropMassHTPassing_cutDijet" ]->SetXTitle( "Leading Jet SoftDrop Mass [GeV]" );
	histos2D_[ "jetSoftDropMassHTPassing_cutDijet" ]->Sumw2();

	histos2D_[ "jetTrimmedMassHTDenom_cutDijet" ] = fs_->make< TH2D >( "jetTrimmedMassHTDenom_cutDijet", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetTrimmedMassHTDenom_cutDijet" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetTrimmedMassHTDenom_cutDijet" ]->SetXTitle( "Leading Jet Trimmed Mass [GeV]" );
	histos2D_[ "jetTrimmedMassHTDenom_cutDijet" ]->Sumw2();

	histos2D_[ "jetTrimmedMassHTPassing_cutDijet" ] = fs_->make< TH2D >( "jetTrimmedMassHTPassing_cutDijet", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetTrimmedMassHTPassing_cutDijet" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetTrimmedMassHTPassing_cutDijet" ]->SetXTitle( "Leading Jet Trimmed Mass [GeV]" );
	histos2D_[ "jetTrimmedMassHTPassing_cutDijet" ]->Sumw2();

	histos2D_[ "prunedMassAveHTDenom_cutDijet" ] = fs_->make< TH2D >( "prunedMassAveHTDenom_cutDijet", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "prunedMassAveHTDenom_cutDijet" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "prunedMassAveHTDenom_cutDijet" ]->SetXTitle( "Average Pruned Mass [GeV]" );
	histos2D_[ "prunedMassAveHTDenom_cutDijet" ]->Sumw2();
	histos2D_[ "prunedMassAveHTPassing_cutDijet" ] = fs_->make< TH2D >( "prunedMassAveHTPassing_cutDijet", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "prunedMassAveHTPassing_cutDijet" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "prunedMassAveHTPassing_cutDijet" ]->SetXTitle( "Average Pruned Mass [GeV]" );
	histos2D_[ "prunedMassAveHTPassing_cutDijet" ]->Sumw2();


	histos1D_[ "ak4HTDenom_cutHT" ] = fs_->make< TH1D >( "ak4HTDenom_cutHT", "ak4HTDenom_cutHT", 150, 0., 1500. );
	histos1D_[ "ak4HTDenom_cutHT" ]->Sumw2();
	histos1D_[ "ak4HTPassing_cutHT" ] = fs_->make< TH1D >( "ak4HTPassing_cutHT", "ak4HTPassing_cutHT", 150, 0., 1500. );
	histos1D_[ "ak4HTPassing_cutHT" ]->Sumw2();

	histos1D_[ "HTDenom_cutHT" ] = fs_->make< TH1D >( "HTDenom_cutHT", "HTDenom_cutHT", 150, 0., 1500. );
	histos1D_[ "HTDenom_cutHT" ]->Sumw2();
	histos1D_[ "HTPassing_cutHT" ] = fs_->make< TH1D >( "HTPassing_cutHT", "HTPassing_cutHT", 150, 0., 1500. );
	histos1D_[ "HTPassing_cutHT" ]->Sumw2();

	histos1D_[ "trimmedMassDenom_cutHT" ] = fs_->make< TH1D >( "trimmedMassDenom_cutHT", "trimmedMassDenom_cutHT", 60, 0., 600. );
	histos1D_[ "trimmedMassDenom_cutHT" ]->Sumw2();
	histos1D_[ "trimmedMassPassing_cutHT" ] = fs_->make< TH1D >( "trimmedMassPassing_cutHT", "trimmedMassPassing_cutHT", 60, 0., 600. );
	histos1D_[ "trimmedMassPassing_cutHT" ]->Sumw2();

	histos1D_[ "prunedMassAveDenom_cutHT" ] = fs_->make< TH1D >( "prunedMassAveDenom_cutHT", "prunedMassAveDenom_cutHT", 60, 0., 600. );
	histos1D_[ "prunedMassAveDenom_cutHT" ]->Sumw2();
	histos1D_[ "prunedMassAvePassing_cutHT" ] = fs_->make< TH1D >( "prunedMassAvePassing_cutHT", "prunedMassAvePassing_cutHT", 60, 0., 600. );
	histos1D_[ "prunedMassAvePassing_cutHT" ]->Sumw2();

	histos1D_[ "jet1PrunedMassDenom_cutHT" ] = fs_->make< TH1D >( "jet1PrunedMassDenom_cutHT", "jet1PrunedMassDenom_cutHT", 60, 0., 600. );
	histos1D_[ "jet1PrunedMassDenom_cutHT" ]->Sumw2();
	histos1D_[ "jet1PrunedMassPassing_cutHT" ] = fs_->make< TH1D >( "jet1PrunedMassPassing_cutHT", "jet1PrunedMassPassing_cutHT", 60, 0., 600. );
	histos1D_[ "jet1PrunedMassPassing_cutHT" ]->Sumw2();

	histos1D_[ "jet1SoftDropMassDenom_cutHT" ] = fs_->make< TH1D >( "jet1SoftDropMassDenom_cutHT", "jet1SoftDropMassDenom_cutHT", 60, 0., 600. );
	histos1D_[ "jet1SoftDropMassDenom_cutHT" ]->Sumw2();
	histos1D_[ "jet1SoftDropMassPassing_cutHT" ] = fs_->make< TH1D >( "jet1SoftDropMassPassing_cutHT", "jet1SoftDropMassPassing_cutHT", 60, 0., 600. );
	histos1D_[ "jet1SoftDropMassPassing_cutHT" ]->Sumw2();

	histos1D_[ "jet1PtDenom_cutHT" ] = fs_->make< TH1D >( "jet1PtDenom_cutHT", "jet1PtDenom_cutHT", 150, 0., 1500. );
	histos1D_[ "jet1PtDenom_cutHT" ]->Sumw2();
	histos1D_[ "jet1PtPassing_cutHT" ] = fs_->make< TH1D >( "jet1PtPassing_cutHT", "jet1PtPassing_cutHT", 150, 0., 1500. );
	histos1D_[ "jet1PtPassing_cutHT" ]->Sumw2();

	histos1D_[ "jet2PtDenom_cutHT" ] = fs_->make< TH1D >( "jet2PtDenom_cutHT", "jet2PtDenom_cutHT", 150, 0., 1500. );
	histos1D_[ "jet2PtDenom_cutHT" ]->Sumw2();
	histos1D_[ "jet2PtPassing_cutHT" ] = fs_->make< TH1D >( "jet2PtPassing_cutHT", "jet2PtPassing_cutHT", 150, 0., 1500. );
	histos1D_[ "jet2PtPassing_cutHT" ]->Sumw2();

	histos2D_[ "jet1PtHTDenom_cutHT" ] = fs_->make< TH2D >( "jet1PtHTDenom_cutHT", "HT vs Leading Jet Pt", 150, 0., 1500., 150, 0., 1500.);
	histos2D_[ "jet1PtHTDenom_cutHT" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jet1PtHTDenom_cutHT" ]->SetXTitle( "Leading Jet Pt [GeV]" );
	histos2D_[ "jet1PtHTDenom_cutHT" ]->Sumw2();
	histos2D_[ "jet1PtHTPassing_cutHT" ] = fs_->make< TH2D >( "jet1PtHTPassing_cutHT", "HT vs Leading Jet Pt", 150, 0., 1500., 150, 0., 1500.);
	histos2D_[ "jet1PtHTPassing_cutHT" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jet1PtHTPassing_cutHT" ]->SetXTitle( "Leading Jet Pt [GeV]" );
	histos2D_[ "jet1PtHTPassing_cutHT" ]->Sumw2();

	histos2D_[ "jet2PtHTDenom_cutHT" ] = fs_->make< TH2D >( "jet2PtHTDenom_cutHT", "HT vs Leading Jet Pt", 150, 0., 1500., 150, 0., 1500.);
	histos2D_[ "jet2PtHTDenom_cutHT" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jet2PtHTDenom_cutHT" ]->SetXTitle( "2nd Leading Jet Pt [GeV]" );
	histos2D_[ "jet2PtHTDenom_cutHT" ]->Sumw2();
	histos2D_[ "jet2PtHTPassing_cutHT" ] = fs_->make< TH2D >( "jet2PtHTPassing_cutHT", "HT vs 2nd Leading Jet Pt", 150, 0., 1500., 150, 0., 1500.);
	histos2D_[ "jet2PtHTPassing_cutHT" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jet2PtHTPassing_cutHT" ]->SetXTitle( "2nd Leading Jet Pt [GeV]" );
	histos2D_[ "jet2PtHTPassing_cutHT" ]->Sumw2();

	histos2D_[ "jet1PtPrunedMassDenom_cutHT" ] = fs_->make< TH2D >( "jet1PtPrunedMassDenom_cutHT", "Leading Jet Pruned Mass vs Leading Jet Pt", 150, 0., 1500., 60, 0., 600.);
	histos2D_[ "jet1PtPrunedMassDenom_cutHT" ]->SetYTitle( "Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jet1PtPrunedMassDenom_cutHT" ]->SetXTitle( "Leading Jet Pt [GeV]" );
	histos2D_[ "jet1PtPrunedMassDenom_cutHT" ]->Sumw2();
	histos2D_[ "jet1PtPrunedMassPassing_cutHT" ] = fs_->make< TH2D >( "jet1PtPrunedMassPassing_cutHT", "Leading Jet Pruned Mass vs Leading Jet Pt", 150, 0., 1500., 60, 0., 600.);
	histos2D_[ "jet1PtPrunedMassPassing_cutHT" ]->SetYTitle( "Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jet1PtPrunedMassPassing_cutHT" ]->SetXTitle( "Leading Jet Pt [GeV]" );
	histos2D_[ "jet1PtPrunedMassPassing_cutHT" ]->Sumw2();

	histos2D_[ "jet2PtPrunedMassDenom_cutHT" ] = fs_->make< TH2D >( "jet2PtPrunedMassDenom_cutHT", "Leading Jet Pruned Mass vs Leading Jet Pt", 150, 0., 1500., 60, 0., 600.);
	histos2D_[ "jet2PtPrunedMassDenom_cutHT" ]->SetYTitle( "2nd Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jet2PtPrunedMassDenom_cutHT" ]->SetXTitle( "2nd Leading Jet Pt [GeV]" );
	histos2D_[ "jet2PtPrunedMassDenom_cutHT" ]->Sumw2();
	histos2D_[ "jet2PtPrunedMassPassing_cutHT" ] = fs_->make< TH2D >( "jet2PtPrunedMassPassing_cutHT", "Leading Jet Pruned Mass vs 2nd Leading Jet Pt", 150, 0., 1500., 60, 0., 600.);
	histos2D_[ "jet2PtPrunedMassPassing_cutHT" ]->SetYTitle( "2nd Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jet2PtPrunedMassPassing_cutHT" ]->SetXTitle( "2nd Leading Jet Pt [GeV]" );
	histos2D_[ "jet2PtPrunedMassPassing_cutHT" ]->Sumw2();

	histos2D_[ "jet1PtSoftDropMassDenom_cutHT" ] = fs_->make< TH2D >( "jet1PtSoftDropMassDenom_cutHT", "Leading Jet SoftDrop Mass vs Leading Jet Pt", 150, 0., 1500., 60, 0., 600.);
	histos2D_[ "jet1PtSoftDropMassDenom_cutHT" ]->SetYTitle( "Leading Jet SoftDrop Mass [GeV]" );
	histos2D_[ "jet1PtSoftDropMassDenom_cutHT" ]->SetXTitle( "Leading Jet Pt [GeV]" );
	histos2D_[ "jet1PtSoftDropMassDenom_cutHT" ]->Sumw2();
	histos2D_[ "jet1PtSoftDropMassPassing_cutHT" ] = fs_->make< TH2D >( "jet1PtSoftDropMassPassing_cutHT", "Leading Jet SoftDrop Mass vs Leading Jet Pt", 150, 0., 1500., 60, 0., 600.);
	histos2D_[ "jet1PtSoftDropMassPassing_cutHT" ]->SetYTitle( "Leading Jet SoftDrop Mass [GeV]" );
	histos2D_[ "jet1PtSoftDropMassPassing_cutHT" ]->SetXTitle( "Leading Jet Pt [GeV]" );
	histos2D_[ "jet1PtSoftDropMassPassing_cutHT" ]->Sumw2();

	histos2D_[ "jet2PtSoftDropMassDenom_cutHT" ] = fs_->make< TH2D >( "jet2PtSoftDropMassDenom_cutHT", "Leading Jet SoftDrop Mass vs Leading Jet Pt", 150, 0., 1500., 60, 0., 600.);
	histos2D_[ "jet2PtSoftDropMassDenom_cutHT" ]->SetYTitle( "2nd Leading Jet SoftDrop Mass [GeV]" );
	histos2D_[ "jet2PtSoftDropMassDenom_cutHT" ]->SetXTitle( "2nd Leading Jet Pt [GeV]" );
	histos2D_[ "jet2PtSoftDropMassDenom_cutHT" ]->Sumw2();
	histos2D_[ "jet2PtSoftDropMassPassing_cutHT" ] = fs_->make< TH2D >( "jet2PtSoftDropMassPassing_cutHT", "Leading Jet SoftDrop Mass vs 2nd Leading Jet Pt", 150, 0., 1500., 60, 0., 600.);
	histos2D_[ "jet2PtSoftDropMassPassing_cutHT" ]->SetYTitle( "2nd Leading Jet SoftDrop Mass [GeV]" );
	histos2D_[ "jet2PtSoftDropMassPassing_cutHT" ]->SetXTitle( "2nd Leading Jet Pt [GeV]" );
	histos2D_[ "jet2PtSoftDropMassPassing_cutHT" ]->Sumw2();

	histos2D_[ "jetPrunedMassHTDenom_cutHT" ] = fs_->make< TH2D >( "jetPrunedMassHTDenom_cutHT", "HT vs 2nd Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetPrunedMassHTDenom_cutHT" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetPrunedMassHTDenom_cutHT" ]->SetXTitle( "2nd Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jetPrunedMassHTDenom_cutHT" ]->Sumw2();
	histos2D_[ "jetPrunedMassHTPassing_cutHT" ] = fs_->make< TH2D >( "jetPrunedMassHTPassing_cutHT", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetPrunedMassHTPassing_cutHT" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetPrunedMassHTPassing_cutHT" ]->SetXTitle( "Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jetPrunedMassHTPassing_cutHT" ]->Sumw2();

	histos2D_[ "jetSoftDropMassHTDenom_cutHT" ] = fs_->make< TH2D >( "jetSoftDropMassHTDenom_cutHT", "HT vs 2nd Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetSoftDropMassHTDenom_cutHT" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetSoftDropMassHTDenom_cutHT" ]->SetXTitle( "2nd Leading Jet SoftDrop Mass [GeV]" );
	histos2D_[ "jetSoftDropMassHTDenom_cutHT" ]->Sumw2();
	histos2D_[ "jetSoftDropMassHTPassing_cutHT" ] = fs_->make< TH2D >( "jetSoftDropMassHTPassing_cutHT", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetSoftDropMassHTPassing_cutHT" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetSoftDropMassHTPassing_cutHT" ]->SetXTitle( "Leading Jet SoftDrop Mass [GeV]" );
	histos2D_[ "jetSoftDropMassHTPassing_cutHT" ]->Sumw2();

	histos2D_[ "jetTrimmedMassHTDenom_cutHT" ] = fs_->make< TH2D >( "jetTrimmedMassHTDenom_cutHT", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetTrimmedMassHTDenom_cutHT" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetTrimmedMassHTDenom_cutHT" ]->SetXTitle( "Leading Jet Trimmed Mass [GeV]" );
	histos2D_[ "jetTrimmedMassHTDenom_cutHT" ]->Sumw2();

	histos2D_[ "jetTrimmedMassHTPassing_cutHT" ] = fs_->make< TH2D >( "jetTrimmedMassHTPassing_cutHT", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetTrimmedMassHTPassing_cutHT" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetTrimmedMassHTPassing_cutHT" ]->SetXTitle( "Leading Jet Trimmed Mass [GeV]" );
	histos2D_[ "jetTrimmedMassHTPassing_cutHT" ]->Sumw2();

	histos2D_[ "prunedMassAveHTDenom_cutHT" ] = fs_->make< TH2D >( "prunedMassAveHTDenom_cutHT", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "prunedMassAveHTDenom_cutHT" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "prunedMassAveHTDenom_cutHT" ]->SetXTitle( "Average Pruned Mass [GeV]" );
	histos2D_[ "prunedMassAveHTDenom_cutHT" ]->Sumw2();
	histos2D_[ "prunedMassAveHTPassing_cutHT" ] = fs_->make< TH2D >( "prunedMassAveHTPassing_cutHT", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "prunedMassAveHTPassing_cutHT" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "prunedMassAveHTPassing_cutHT" ]->SetXTitle( "Average Pruned Mass [GeV]" );
	histos2D_[ "prunedMassAveHTPassing_cutHT" ]->Sumw2();



	histos1D_[ "ak4HTDenom_cutTriggerEff" ] = fs_->make< TH1D >( "ak4HTDenom_cutTriggerEff", "ak4HTDenom_cutTriggerEff", 150, 0., 1500. );
	histos1D_[ "ak4HTDenom_cutTriggerEff" ]->Sumw2();
	histos1D_[ "ak4HTPassing_cutTriggerEff" ] = fs_->make< TH1D >( "ak4HTPassing_cutTriggerEff", "ak4HTPassing_cutTriggerEff", 150, 0., 1500. );
	histos1D_[ "ak4HTPassing_cutTriggerEff" ]->Sumw2();

	histos1D_[ "HTDenom_cutTriggerEff" ] = fs_->make< TH1D >( "HTDenom_cutTriggerEff", "HTDenom_cutTriggerEff", 150, 0., 1500. );
	histos1D_[ "HTDenom_cutTriggerEff" ]->Sumw2();
	histos1D_[ "HTPassing_cutTriggerEff" ] = fs_->make< TH1D >( "HTPassing_cutTriggerEff", "HTPassing_cutTriggerEff", 150, 0., 1500. );
	histos1D_[ "HTPassing_cutTriggerEff" ]->Sumw2();

	histos1D_[ "trimmedMassDenom_cutTriggerEff" ] = fs_->make< TH1D >( "trimmedMassDenom_cutTriggerEff", "trimmedMassDenom_cutTriggerEff", 60, 0., 600. );
	histos1D_[ "trimmedMassDenom_cutTriggerEff" ]->Sumw2();
	histos1D_[ "trimmedMassPassing_cutTriggerEff" ] = fs_->make< TH1D >( "trimmedMassPassing_cutTriggerEff", "trimmedMassPassing_cutTriggerEff", 60, 0., 600. );
	histos1D_[ "trimmedMassPassing_cutTriggerEff" ]->Sumw2();

	histos1D_[ "prunedMassAveDenom_cutTriggerEff" ] = fs_->make< TH1D >( "prunedMassAveDenom_cutTriggerEff", "prunedMassAveDenom_cutTriggerEff", 60, 0., 600. );
	histos1D_[ "prunedMassAveDenom_cutTriggerEff" ]->Sumw2();
	histos1D_[ "prunedMassAvePassing_cutTriggerEff" ] = fs_->make< TH1D >( "prunedMassAvePassing_cutTriggerEff", "prunedMassAvePassing_cutTriggerEff", 60, 0., 600. );
	histos1D_[ "prunedMassAvePassing_cutTriggerEff" ]->Sumw2();

	histos1D_[ "jet1PrunedMassDenom_cutTriggerEff" ] = fs_->make< TH1D >( "jet1PrunedMassDenom_cutTriggerEff", "jet1PrunedMassDenom_cutTriggerEff", 60, 0., 600. );
	histos1D_[ "jet1PrunedMassDenom_cutTriggerEff" ]->Sumw2();
	histos1D_[ "jet1PrunedMassPassing_cutTriggerEff" ] = fs_->make< TH1D >( "jet1PrunedMassPassing_cutTriggerEff", "jet1PrunedMassPassing_cutTriggerEff", 60, 0., 600. );
	histos1D_[ "jet1PrunedMassPassing_cutTriggerEff" ]->Sumw2();

	histos1D_[ "jet1SoftDropMassDenom_cutTriggerEff" ] = fs_->make< TH1D >( "jet1SoftDropMassDenom_cutTriggerEff", "jet1SoftDropMassDenom_cutTriggerEff", 60, 0., 600. );
	histos1D_[ "jet1SoftDropMassDenom_cutTriggerEff" ]->Sumw2();
	histos1D_[ "jet1SoftDropMassPassing_cutTriggerEff" ] = fs_->make< TH1D >( "jet1SoftDropMassPassing_cutTriggerEff", "jet1SoftDropMassPassing_cutTriggerEff", 60, 0., 600. );
	histos1D_[ "jet1SoftDropMassPassing_cutTriggerEff" ]->Sumw2();

	histos1D_[ "jet1PtDenom_cutTriggerEff" ] = fs_->make< TH1D >( "jet1PtDenom_cutTriggerEff", "jet1PtDenom_cutTriggerEff", 150, 0., 1500. );
	histos1D_[ "jet1PtDenom_cutTriggerEff" ]->Sumw2();
	histos1D_[ "jet1PtPassing_cutTriggerEff" ] = fs_->make< TH1D >( "jet1PtPassing_cutTriggerEff", "jet1PtPassing_cutTriggerEff", 150, 0., 1500. );
	histos1D_[ "jet1PtPassing_cutTriggerEff" ]->Sumw2();

	histos1D_[ "jet2PtDenom_cutTriggerEff" ] = fs_->make< TH1D >( "jet2PtDenom_cutTriggerEff", "jet2PtDenom_cutTriggerEff", 150, 0., 1500. );
	histos1D_[ "jet2PtDenom_cutTriggerEff" ]->Sumw2();
	histos1D_[ "jet2PtPassing_cutTriggerEff" ] = fs_->make< TH1D >( "jet2PtPassing_cutTriggerEff", "jet2PtPassing_cutTriggerEff", 150, 0., 1500. );
	histos1D_[ "jet2PtPassing_cutTriggerEff" ]->Sumw2();

	histos2D_[ "jet1PtHTDenom_cutTriggerEff" ] = fs_->make< TH2D >( "jet1PtHTDenom_cutTriggerEff", "HT vs Leading Jet Pt", 150, 0., 1500., 150, 0., 1500.);
	histos2D_[ "jet1PtHTDenom_cutTriggerEff" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jet1PtHTDenom_cutTriggerEff" ]->SetXTitle( "Leading Jet Pt [GeV]" );
	histos2D_[ "jet1PtHTDenom_cutTriggerEff" ]->Sumw2();
	histos2D_[ "jet1PtHTPassing_cutTriggerEff" ] = fs_->make< TH2D >( "jet1PtHTPassing_cutTriggerEff", "HT vs Leading Jet Pt", 150, 0., 1500., 150, 0., 1500.);
	histos2D_[ "jet1PtHTPassing_cutTriggerEff" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jet1PtHTPassing_cutTriggerEff" ]->SetXTitle( "Leading Jet Pt [GeV]" );
	histos2D_[ "jet1PtHTPassing_cutTriggerEff" ]->Sumw2();

	histos2D_[ "jet2PtHTDenom_cutTriggerEff" ] = fs_->make< TH2D >( "jet2PtHTDenom_cutTriggerEff", "HT vs Leading Jet Pt", 150, 0., 1500., 150, 0., 1500.);
	histos2D_[ "jet2PtHTDenom_cutTriggerEff" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jet2PtHTDenom_cutTriggerEff" ]->SetXTitle( "2nd Leading Jet Pt [GeV]" );
	histos2D_[ "jet2PtHTDenom_cutTriggerEff" ]->Sumw2();
	histos2D_[ "jet2PtHTPassing_cutTriggerEff" ] = fs_->make< TH2D >( "jet2PtHTPassing_cutTriggerEff", "HT vs 2nd Leading Jet Pt", 150, 0., 1500., 150, 0., 1500.);
	histos2D_[ "jet2PtHTPassing_cutTriggerEff" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jet2PtHTPassing_cutTriggerEff" ]->SetXTitle( "2nd Leading Jet Pt [GeV]" );
	histos2D_[ "jet2PtHTPassing_cutTriggerEff" ]->Sumw2();

	histos2D_[ "jet1PtPrunedMassDenom_cutTriggerEff" ] = fs_->make< TH2D >( "jet1PtPrunedMassDenom_cutTriggerEff", "Leading Jet Pruned Mass vs Leading Jet Pt", 150, 0., 1500., 60, 0., 600.);
	histos2D_[ "jet1PtPrunedMassDenom_cutTriggerEff" ]->SetYTitle( "Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jet1PtPrunedMassDenom_cutTriggerEff" ]->SetXTitle( "Leading Jet Pt [GeV]" );
	histos2D_[ "jet1PtPrunedMassDenom_cutTriggerEff" ]->Sumw2();
	histos2D_[ "jet1PtPrunedMassPassing_cutTriggerEff" ] = fs_->make< TH2D >( "jet1PtPrunedMassPassing_cutTriggerEff", "Leading Jet Pruned Mass vs Leading Jet Pt", 150, 0., 1500., 60, 0., 600.);
	histos2D_[ "jet1PtPrunedMassPassing_cutTriggerEff" ]->SetYTitle( "Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jet1PtPrunedMassPassing_cutTriggerEff" ]->SetXTitle( "Leading Jet Pt [GeV]" );
	histos2D_[ "jet1PtPrunedMassPassing_cutTriggerEff" ]->Sumw2();

	histos2D_[ "jet2PtPrunedMassDenom_cutTriggerEff" ] = fs_->make< TH2D >( "jet2PtPrunedMassDenom_cutTriggerEff", "Leading Jet Pruned Mass vs Leading Jet Pt", 150, 0., 1500., 60, 0., 600.);
	histos2D_[ "jet2PtPrunedMassDenom_cutTriggerEff" ]->SetYTitle( "2nd Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jet2PtPrunedMassDenom_cutTriggerEff" ]->SetXTitle( "2nd Leading Jet Pt [GeV]" );
	histos2D_[ "jet2PtPrunedMassDenom_cutTriggerEff" ]->Sumw2();
	histos2D_[ "jet2PtPrunedMassPassing_cutTriggerEff" ] = fs_->make< TH2D >( "jet2PtPrunedMassPassing_cutTriggerEff", "Leading Jet Pruned Mass vs 2nd Leading Jet Pt", 150, 0., 1500., 60, 0., 600.);
	histos2D_[ "jet2PtPrunedMassPassing_cutTriggerEff" ]->SetYTitle( "2nd Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jet2PtPrunedMassPassing_cutTriggerEff" ]->SetXTitle( "2nd Leading Jet Pt [GeV]" );
	histos2D_[ "jet2PtPrunedMassPassing_cutTriggerEff" ]->Sumw2();

	histos2D_[ "jet1PtSoftDropMassDenom_cutTriggerEff" ] = fs_->make< TH2D >( "jet1PtSoftDropMassDenom_cutTriggerEff", "Leading Jet SoftDrop Mass vs Leading Jet Pt", 150, 0., 1500., 60, 0., 600.);
	histos2D_[ "jet1PtSoftDropMassDenom_cutTriggerEff" ]->SetYTitle( "Leading Jet SoftDrop Mass [GeV]" );
	histos2D_[ "jet1PtSoftDropMassDenom_cutTriggerEff" ]->SetXTitle( "Leading Jet Pt [GeV]" );
	histos2D_[ "jet1PtSoftDropMassDenom_cutTriggerEff" ]->Sumw2();
	histos2D_[ "jet1PtSoftDropMassPassing_cutTriggerEff" ] = fs_->make< TH2D >( "jet1PtSoftDropMassPassing_cutTriggerEff", "Leading Jet SoftDrop Mass vs Leading Jet Pt", 150, 0., 1500., 60, 0., 600.);
	histos2D_[ "jet1PtSoftDropMassPassing_cutTriggerEff" ]->SetYTitle( "Leading Jet SoftDrop Mass [GeV]" );
	histos2D_[ "jet1PtSoftDropMassPassing_cutTriggerEff" ]->SetXTitle( "Leading Jet Pt [GeV]" );
	histos2D_[ "jet1PtSoftDropMassPassing_cutTriggerEff" ]->Sumw2();

	histos2D_[ "jet2PtSoftDropMassDenom_cutTriggerEff" ] = fs_->make< TH2D >( "jet2PtSoftDropMassDenom_cutTriggerEff", "Leading Jet SoftDrop Mass vs Leading Jet Pt", 150, 0., 1500., 60, 0., 600.);
	histos2D_[ "jet2PtSoftDropMassDenom_cutTriggerEff" ]->SetYTitle( "2nd Leading Jet SoftDrop Mass [GeV]" );
	histos2D_[ "jet2PtSoftDropMassDenom_cutTriggerEff" ]->SetXTitle( "2nd Leading Jet Pt [GeV]" );
	histos2D_[ "jet2PtSoftDropMassDenom_cutTriggerEff" ]->Sumw2();
	histos2D_[ "jet2PtSoftDropMassPassing_cutTriggerEff" ] = fs_->make< TH2D >( "jet2PtSoftDropMassPassing_cutTriggerEff", "Leading Jet SoftDrop Mass vs 2nd Leading Jet Pt", 150, 0., 1500., 60, 0., 600.);
	histos2D_[ "jet2PtSoftDropMassPassing_cutTriggerEff" ]->SetYTitle( "2nd Leading Jet SoftDrop Mass [GeV]" );
	histos2D_[ "jet2PtSoftDropMassPassing_cutTriggerEff" ]->SetXTitle( "2nd Leading Jet Pt [GeV]" );
	histos2D_[ "jet2PtSoftDropMassPassing_cutTriggerEff" ]->Sumw2();

	histos2D_[ "jetPrunedMassHTDenom_cutTriggerEff" ] = fs_->make< TH2D >( "jetPrunedMassHTDenom_cutTriggerEff", "HT vs 2nd Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetPrunedMassHTDenom_cutTriggerEff" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetPrunedMassHTDenom_cutTriggerEff" ]->SetXTitle( "2nd Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jetPrunedMassHTDenom_cutTriggerEff" ]->Sumw2();
	histos2D_[ "jetPrunedMassHTPassing_cutTriggerEff" ] = fs_->make< TH2D >( "jetPrunedMassHTPassing_cutTriggerEff", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetPrunedMassHTPassing_cutTriggerEff" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetPrunedMassHTPassing_cutTriggerEff" ]->SetXTitle( "Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jetPrunedMassHTPassing_cutTriggerEff" ]->Sumw2();

	histos2D_[ "jetSoftDropMassHTDenom_cutTriggerEff" ] = fs_->make< TH2D >( "jetSoftDropMassHTDenom_cutTriggerEff", "HT vs 2nd Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetSoftDropMassHTDenom_cutTriggerEff" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetSoftDropMassHTDenom_cutTriggerEff" ]->SetXTitle( "2nd Leading Jet SoftDrop Mass [GeV]" );
	histos2D_[ "jetSoftDropMassHTDenom_cutTriggerEff" ]->Sumw2();
	histos2D_[ "jetSoftDropMassHTPassing_cutTriggerEff" ] = fs_->make< TH2D >( "jetSoftDropMassHTPassing_cutTriggerEff", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetSoftDropMassHTPassing_cutTriggerEff" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetSoftDropMassHTPassing_cutTriggerEff" ]->SetXTitle( "Leading Jet SoftDrop Mass [GeV]" );
	histos2D_[ "jetSoftDropMassHTPassing_cutTriggerEff" ]->Sumw2();

	histos2D_[ "jetTrimmedMassHTDenom_cutTriggerEff" ] = fs_->make< TH2D >( "jetTrimmedMassHTDenom_cutTriggerEff", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetTrimmedMassHTDenom_cutTriggerEff" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetTrimmedMassHTDenom_cutTriggerEff" ]->SetXTitle( "Leading Jet Trimmed Mass [GeV]" );
	histos2D_[ "jetTrimmedMassHTDenom_cutTriggerEff" ]->Sumw2();

	histos2D_[ "jetTrimmedMassHTPassing_cutTriggerEff" ] = fs_->make< TH2D >( "jetTrimmedMassHTPassing_cutTriggerEff", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetTrimmedMassHTPassing_cutTriggerEff" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetTrimmedMassHTPassing_cutTriggerEff" ]->SetXTitle( "Leading Jet Trimmed Mass [GeV]" );
	histos2D_[ "jetTrimmedMassHTPassing_cutTriggerEff" ]->Sumw2();

	histos2D_[ "prunedMassAveHTDenom_cutTriggerEff" ] = fs_->make< TH2D >( "prunedMassAveHTDenom_cutTriggerEff", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "prunedMassAveHTDenom_cutTriggerEff" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "prunedMassAveHTDenom_cutTriggerEff" ]->SetXTitle( "Average Pruned Mass [GeV]" );
	histos2D_[ "prunedMassAveHTDenom_cutTriggerEff" ]->Sumw2();
	histos2D_[ "prunedMassAveHTPassing_cutTriggerEff" ] = fs_->make< TH2D >( "prunedMassAveHTPassing_cutTriggerEff", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "prunedMassAveHTPassing_cutTriggerEff" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "prunedMassAveHTPassing_cutTriggerEff" ]->SetXTitle( "Average Pruned Mass [GeV]" );
	histos2D_[ "prunedMassAveHTPassing_cutTriggerEff" ]->Sumw2();





	histos1D_[ "HTDenom_cutJet" ] = fs_->make< TH1D >( "HTDenom_cutJet", "HTDenom_cutJet", 150, 0., 1500. );
	histos1D_[ "HTDenom_cutJet" ]->Sumw2();
	histos1D_[ "HTPassing_cutJet" ] = fs_->make< TH1D >( "HTPassing_cutJet", "HTPassing_cutJet", 150, 0., 1500. );
	histos1D_[ "HTPassing_cutJet" ]->Sumw2();

	histos1D_[ "trimmedMassDenom_cutJet" ] = fs_->make< TH1D >( "trimmedMassDenom_cutJet", "trimmedMassDenom_cutJet", 60, 0., 600. );
	histos1D_[ "trimmedMassDenom_cutJet" ]->Sumw2();
	histos1D_[ "trimmedMassPassing_cutJet" ] = fs_->make< TH1D >( "trimmedMassPassing_cutJet", "trimmedMassPassing_cutJet", 60, 0., 600. );
	histos1D_[ "trimmedMassPassing_cutJet" ]->Sumw2();

	histos1D_[ "jet1PrunedMassDenom_cutJet" ] = fs_->make< TH1D >( "jet1PrunedMassDenom_cutJet", "jet1PrunedMassDenom_cutJet", 60, 0., 600. );
	histos1D_[ "jet1PrunedMassDenom_cutJet" ]->Sumw2();
	histos1D_[ "jet1PrunedMassPassing_cutJet" ] = fs_->make< TH1D >( "jet1PrunedMassPassing_cutJet", "jet1PrunedMassPassing_cutJet", 60, 0., 600. );
	histos1D_[ "jet1PrunedMassPassing_cutJet" ]->Sumw2();

	histos1D_[ "jet1SoftDropMassDenom_cutJet" ] = fs_->make< TH1D >( "jet1SoftDropMassDenom_cutJet", "jet1SoftDropMassDenom_cutJet", 60, 0., 600. );
	histos1D_[ "jet1SoftDropMassDenom_cutJet" ]->Sumw2();
	histos1D_[ "jet1SoftDropMassPassing_cutJet" ] = fs_->make< TH1D >( "jet1SoftDropMassPassing_cutJet", "jet1SoftDropMassPassing_cutJet", 60, 0., 600. );
	histos1D_[ "jet1SoftDropMassPassing_cutJet" ]->Sumw2();

	histos1D_[ "jet1PtDenom_cutJet" ] = fs_->make< TH1D >( "jet1PtDenom_cutJet", "jet1PtDenom_cutJet", 150, 0., 1500. );
	histos1D_[ "jet1PtDenom_cutJet" ]->Sumw2();
	histos1D_[ "jet1PtPassing_cutJet" ] = fs_->make< TH1D >( "jet1PtPassing_cutJet", "jet1PtPassing_cutJet", 150, 0., 1500. );
	histos1D_[ "jet1PtPassing_cutJet" ]->Sumw2();

	histos2D_[ "jet1PtHTDenom_cutJet" ] = fs_->make< TH2D >( "jet1PtHTDenom_cutJet", "HT vs Leading Jet Pt", 150, 0., 1500., 150, 0., 1500.);
	histos2D_[ "jet1PtHTDenom_cutJet" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jet1PtHTDenom_cutJet" ]->SetXTitle( "Leading Jet Pt [GeV]" );
	histos2D_[ "jet1PtHTDenom_cutJet" ]->Sumw2();
	histos2D_[ "jet1PtHTPassing_cutJet" ] = fs_->make< TH2D >( "jet1PtHTPassing_cutJet", "HT vs Leading Jet Pt", 150, 0., 1500., 150, 0., 1500.);
	histos2D_[ "jet1PtHTPassing_cutJet" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jet1PtHTPassing_cutJet" ]->SetXTitle( "Leading Jet Pt [GeV]" );
	histos2D_[ "jet1PtHTPassing_cutJet" ]->Sumw2();

	histos2D_[ "jet1PtPrunedMassDenom_cutJet" ] = fs_->make< TH2D >( "jet1PtPrunedMassDenom_cutJet", "Leading Jet Pruned Mass vs Leading Jet Pt", 150, 0., 1500., 60, 0., 600.);
	histos2D_[ "jet1PtPrunedMassDenom_cutJet" ]->SetYTitle( "Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jet1PtPrunedMassDenom_cutJet" ]->SetXTitle( "Leading Jet Pt [GeV]" );
	histos2D_[ "jet1PtPrunedMassDenom_cutJet" ]->Sumw2();
	histos2D_[ "jet1PtPrunedMassPassing_cutJet" ] = fs_->make< TH2D >( "jet1PtPrunedMassPassing_cutJet", "Leading Jet Pruned Mass vs Leading Jet Pt", 150, 0., 1500., 60, 0., 600.);
	histos2D_[ "jet1PtPrunedMassPassing_cutJet" ]->SetYTitle( "Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jet1PtPrunedMassPassing_cutJet" ]->SetXTitle( "Leading Jet Pt [GeV]" );
	histos2D_[ "jet1PtPrunedMassPassing_cutJet" ]->Sumw2();

	histos2D_[ "jet1PtSoftDropMassDenom_cutJet" ] = fs_->make< TH2D >( "jet1PtSoftDropMassDenom_cutJet", "Leading Jet SoftDrop Mass vs Leading Jet Pt", 150, 0., 1500., 60, 0., 600.);
	histos2D_[ "jet1PtSoftDropMassDenom_cutJet" ]->SetYTitle( "Leading Jet SoftDrop Mass [GeV]" );
	histos2D_[ "jet1PtSoftDropMassDenom_cutJet" ]->SetXTitle( "Leading Jet Pt [GeV]" );
	histos2D_[ "jet1PtSoftDropMassDenom_cutJet" ]->Sumw2();
	histos2D_[ "jet1PtSoftDropMassPassing_cutJet" ] = fs_->make< TH2D >( "jet1PtSoftDropMassPassing_cutJet", "Leading Jet SoftDrop Mass vs Leading Jet Pt", 150, 0., 1500., 60, 0., 600.);
	histos2D_[ "jet1PtSoftDropMassPassing_cutJet" ]->SetYTitle( "Leading Jet SoftDrop Mass [GeV]" );
	histos2D_[ "jet1PtSoftDropMassPassing_cutJet" ]->SetXTitle( "Leading Jet Pt [GeV]" );
	histos2D_[ "jet1PtSoftDropMassPassing_cutJet" ]->Sumw2();

	histos2D_[ "jetPrunedMassHTDenom_cutJet" ] = fs_->make< TH2D >( "jetPrunedMassHTDenom_cutJet", "HT vs 2nd Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetPrunedMassHTDenom_cutJet" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetPrunedMassHTDenom_cutJet" ]->SetXTitle( "2nd Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jetPrunedMassHTDenom_cutJet" ]->Sumw2();
	histos2D_[ "jetPrunedMassHTPassing_cutJet" ] = fs_->make< TH2D >( "jetPrunedMassHTPassing_cutJet", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetPrunedMassHTPassing_cutJet" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetPrunedMassHTPassing_cutJet" ]->SetXTitle( "Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jetPrunedMassHTPassing_cutJet" ]->Sumw2();

	histos2D_[ "jetSoftDropMassHTDenom_cutJet" ] = fs_->make< TH2D >( "jetSoftDropMassHTDenom_cutJet", "HT vs 2nd Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetSoftDropMassHTDenom_cutJet" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetSoftDropMassHTDenom_cutJet" ]->SetXTitle( "2nd Leading Jet SoftDrop Mass [GeV]" );
	histos2D_[ "jetSoftDropMassHTDenom_cutJet" ]->Sumw2();
	histos2D_[ "jetSoftDropMassHTPassing_cutJet" ] = fs_->make< TH2D >( "jetSoftDropMassHTPassing_cutJet", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetSoftDropMassHTPassing_cutJet" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetSoftDropMassHTPassing_cutJet" ]->SetXTitle( "Leading Jet SoftDrop Mass [GeV]" );
	histos2D_[ "jetSoftDropMassHTPassing_cutJet" ]->Sumw2();

	histos2D_[ "jetTrimmedMassHTDenom_cutJet" ] = fs_->make< TH2D >( "jetTrimmedMassHTDenom_cutJet", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetTrimmedMassHTDenom_cutJet" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetTrimmedMassHTDenom_cutJet" ]->SetXTitle( "Leading Jet Trimmed Mass [GeV]" );
	histos2D_[ "jetTrimmedMassHTDenom_cutJet" ]->Sumw2();

	histos2D_[ "jetTrimmedMassHTPassing_cutJet" ] = fs_->make< TH2D >( "jetTrimmedMassHTPassing_cutJet", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetTrimmedMassHTPassing_cutJet" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetTrimmedMassHTPassing_cutJet" ]->SetXTitle( "Leading Jet Trimmed Mass [GeV]" );
	histos2D_[ "jetTrimmedMassHTPassing_cutJet" ]->Sumw2();



	histos1D_[ "HTDenom_cutJetPt" ] = fs_->make< TH1D >( "HTDenom_cutJetPt", "HTDenom_cutJetPt", 150, 0., 1500. );
	histos1D_[ "HTDenom_cutJetPt" ]->Sumw2();
	histos1D_[ "HTPassing_cutJetPt" ] = fs_->make< TH1D >( "HTPassing_cutJetPt", "HTPassing_cutJetPt", 150, 0., 1500. );
	histos1D_[ "HTPassing_cutJetPt" ]->Sumw2();

	histos1D_[ "trimmedMassDenom_cutJetPt" ] = fs_->make< TH1D >( "trimmedMassDenom_cutJetPt", "trimmedMassDenom_cutJetPt", 60, 0., 600. );
	histos1D_[ "trimmedMassDenom_cutJetPt" ]->Sumw2();
	histos1D_[ "trimmedMassPassing_cutJetPt" ] = fs_->make< TH1D >( "trimmedMassPassing_cutJetPt", "trimmedMassPassing_cutJetPt", 60, 0., 600. );
	histos1D_[ "trimmedMassPassing_cutJetPt" ]->Sumw2();

	histos1D_[ "jet1PrunedMassDenom_cutJetPt" ] = fs_->make< TH1D >( "jet1PrunedMassDenom_cutJetPt", "jet1PrunedMassDenom_cutJetPt", 60, 0., 600. );
	histos1D_[ "jet1PrunedMassDenom_cutJetPt" ]->Sumw2();
	histos1D_[ "jet1PrunedMassPassing_cutJetPt" ] = fs_->make< TH1D >( "jet1PrunedMassPassing_cutJetPt", "jet1PrunedMassPassing_cutJetPt", 60, 0., 600. );
	histos1D_[ "jet1PrunedMassPassing_cutJetPt" ]->Sumw2();

	histos1D_[ "jet1SoftDropMassDenom_cutJetPt" ] = fs_->make< TH1D >( "jet1SoftDropMassDenom_cutJetPt", "jet1SoftDropMassDenom_cutJetPt", 60, 0., 600. );
	histos1D_[ "jet1SoftDropMassDenom_cutJetPt" ]->Sumw2();
	histos1D_[ "jet1SoftDropMassPassing_cutJetPt" ] = fs_->make< TH1D >( "jet1SoftDropMassPassing_cutJetPt", "jet1SoftDropMassPassing_cutJetPt", 60, 0., 600. );
	histos1D_[ "jet1SoftDropMassPassing_cutJetPt" ]->Sumw2();

	histos1D_[ "jet1PtDenom_cutJetPt" ] = fs_->make< TH1D >( "jet1PtDenom_cutJetPt", "jet1PtDenom_cutJetPt", 150, 0., 1500. );
	histos1D_[ "jet1PtDenom_cutJetPt" ]->Sumw2();
	histos1D_[ "jet1PtPassing_cutJetPt" ] = fs_->make< TH1D >( "jet1PtPassing_cutJetPt", "jet1PtPassing_cutJetPt", 150, 0., 1500. );
	histos1D_[ "jet1PtPassing_cutJetPt" ]->Sumw2();

	histos2D_[ "jet1PtHTDenom_cutJetPt" ] = fs_->make< TH2D >( "jet1PtHTDenom_cutJetPt", "HT vs Leading Jet Pt", 150, 0., 1500., 150, 0., 1500.);
	histos2D_[ "jet1PtHTDenom_cutJetPt" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jet1PtHTDenom_cutJetPt" ]->SetXTitle( "Leading Jet Pt [GeV]" );
	histos2D_[ "jet1PtHTDenom_cutJetPt" ]->Sumw2();
	histos2D_[ "jet1PtHTPassing_cutJetPt" ] = fs_->make< TH2D >( "jet1PtHTPassing_cutJetPt", "HT vs Leading Jet Pt", 150, 0., 1500., 150, 0., 1500.);
	histos2D_[ "jet1PtHTPassing_cutJetPt" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jet1PtHTPassing_cutJetPt" ]->SetXTitle( "Leading Jet Pt [GeV]" );
	histos2D_[ "jet1PtHTPassing_cutJetPt" ]->Sumw2();

	histos2D_[ "jet1PtPrunedMassDenom_cutJetPt" ] = fs_->make< TH2D >( "jet1PtPrunedMassDenom_cutJetPt", "Leading Jet Pruned Mass vs Leading Jet Pt", 150, 0., 1500., 60, 0., 600.);
	histos2D_[ "jet1PtPrunedMassDenom_cutJetPt" ]->SetYTitle( "Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jet1PtPrunedMassDenom_cutJetPt" ]->SetXTitle( "Leading Jet Pt [GeV]" );
	histos2D_[ "jet1PtPrunedMassDenom_cutJetPt" ]->Sumw2();
	histos2D_[ "jet1PtPrunedMassPassing_cutJetPt" ] = fs_->make< TH2D >( "jet1PtPrunedMassPassing_cutJetPt", "Leading Jet Pruned Mass vs Leading Jet Pt", 150, 0., 1500., 60, 0., 600.);
	histos2D_[ "jet1PtPrunedMassPassing_cutJetPt" ]->SetYTitle( "Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jet1PtPrunedMassPassing_cutJetPt" ]->SetXTitle( "Leading Jet Pt [GeV]" );
	histos2D_[ "jet1PtPrunedMassPassing_cutJetPt" ]->Sumw2();

	histos2D_[ "jet1PtSoftDropMassDenom_cutJetPt" ] = fs_->make< TH2D >( "jet1PtSoftDropMassDenom_cutJetPt", "Leading Jet SoftDrop Mass vs Leading Jet Pt", 150, 0., 1500., 60, 0., 600.);
	histos2D_[ "jet1PtSoftDropMassDenom_cutJetPt" ]->SetYTitle( "Leading Jet SoftDrop Mass [GeV]" );
	histos2D_[ "jet1PtSoftDropMassDenom_cutJetPt" ]->SetXTitle( "Leading Jet Pt [GeV]" );
	histos2D_[ "jet1PtSoftDropMassDenom_cutJetPt" ]->Sumw2();
	histos2D_[ "jet1PtSoftDropMassPassing_cutJetPt" ] = fs_->make< TH2D >( "jet1PtSoftDropMassPassing_cutJetPt", "Leading Jet SoftDrop Mass vs Leading Jet Pt", 150, 0., 1500., 60, 0., 600.);
	histos2D_[ "jet1PtSoftDropMassPassing_cutJetPt" ]->SetYTitle( "Leading Jet SoftDrop Mass [GeV]" );
	histos2D_[ "jet1PtSoftDropMassPassing_cutJetPt" ]->SetXTitle( "Leading Jet Pt [GeV]" );
	histos2D_[ "jet1PtSoftDropMassPassing_cutJetPt" ]->Sumw2();

	histos2D_[ "jetPrunedMassHTDenom_cutJetPt" ] = fs_->make< TH2D >( "jetPrunedMassHTDenom_cutJetPt", "HT vs 2nd Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetPrunedMassHTDenom_cutJetPt" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetPrunedMassHTDenom_cutJetPt" ]->SetXTitle( "2nd Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jetPrunedMassHTDenom_cutJetPt" ]->Sumw2();
	histos2D_[ "jetPrunedMassHTPassing_cutJetPt" ] = fs_->make< TH2D >( "jetPrunedMassHTPassing_cutJetPt", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetPrunedMassHTPassing_cutJetPt" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetPrunedMassHTPassing_cutJetPt" ]->SetXTitle( "Leading Jet Pruned Mass [GeV]" );
	histos2D_[ "jetPrunedMassHTPassing_cutJetPt" ]->Sumw2();

	histos2D_[ "jetSoftDropMassHTDenom_cutJetPt" ] = fs_->make< TH2D >( "jetSoftDropMassHTDenom_cutJetPt", "HT vs 2nd Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetSoftDropMassHTDenom_cutJetPt" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetSoftDropMassHTDenom_cutJetPt" ]->SetXTitle( "2nd Leading Jet SoftDrop Mass [GeV]" );
	histos2D_[ "jetSoftDropMassHTDenom_cutJetPt" ]->Sumw2();
	histos2D_[ "jetSoftDropMassHTPassing_cutJetPt" ] = fs_->make< TH2D >( "jetSoftDropMassHTPassing_cutJetPt", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetSoftDropMassHTPassing_cutJetPt" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetSoftDropMassHTPassing_cutJetPt" ]->SetXTitle( "Leading Jet SoftDrop Mass [GeV]" );
	histos2D_[ "jetSoftDropMassHTPassing_cutJetPt" ]->Sumw2();

	histos2D_[ "jetTrimmedMassHTDenom_cutJetPt" ] = fs_->make< TH2D >( "jetTrimmedMassHTDenom_cutJetPt", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetTrimmedMassHTDenom_cutJetPt" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetTrimmedMassHTDenom_cutJetPt" ]->SetXTitle( "Leading Jet Trimmed Mass [GeV]" );
	histos2D_[ "jetTrimmedMassHTDenom_cutJetPt" ]->Sumw2();

	histos2D_[ "jetTrimmedMassHTPassing_cutJetPt" ] = fs_->make< TH2D >( "jetTrimmedMassHTPassing_cutJetPt", "HT vs Leading Jet Mass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jetTrimmedMassHTPassing_cutJetPt" ]->SetYTitle( "HT [GeV]" );
	histos2D_[ "jetTrimmedMassHTPassing_cutJetPt" ]->SetXTitle( "Leading Jet Trimmed Mass [GeV]" );
	histos2D_[ "jetTrimmedMassHTPassing_cutJetPt" ]->Sumw2();
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
	desc.add<InputTag>("jetAk4Pt", 	InputTag("jetsAK4CHS:jetAK4CHSPt"));
	desc.add<InputTag>("jetPt", 	InputTag("jetsAK8CHS:jetAK8CHSPt"));
	desc.add<InputTag>("jetEta", 	InputTag("jetsAK8CHS:jetAK8CHSEta"));
	desc.add<InputTag>("jetPhi", 	InputTag("jetsAK8CHS:jetAK8CHSPhi"));
	desc.add<InputTag>("jetE", 	InputTag("jetsAK8CHS:jetAK8CHSE"));
	desc.add<InputTag>("jetMass", 	InputTag("jetsAK8CHS:jetAK8CHSMass"));
	desc.add<InputTag>("jetPrunedMass", 	InputTag("jetsAK8CHS:jetAK8CHSprunedMass"));
	desc.add<InputTag>("jetFilteredMass", 	InputTag("jetsAK8CHS:jetAK8CHSfilteredMass"));
	desc.add<InputTag>("jetSoftDropMass", 	InputTag("jetsAK8CHS:jetAK8CHSsoftDropMass"));
	desc.add<InputTag>("jetTrimmedMass", 	InputTag("jetsAK8CHS:jetAK8CHStrimmedMass"));
	desc.add<InputTag>("jetTau1", 	InputTag("jetsAK8CHS:jetAK8CHStau1"));
	desc.add<InputTag>("jetTau2", 	InputTag("jetsAK8CHS:jetAK8CHStau2"));
	desc.add<InputTag>("jetTau3", 	InputTag("jetsAK8CHS:jetAK8CHStau3"));
	desc.add<InputTag>("jetNSubjets", 	InputTag("jetsAK8CHS:jetAK8CHSnSubjets"));
	desc.add<InputTag>("jetSubjetIndex0", 	InputTag("jetsAK8CHS:jetAK8CHSvSubjetIndex0"));
	desc.add<InputTag>("jetSubjetIndex1", 	InputTag("jetsAK8CHS:jetAK8CHSvSubjetIndex1"));
	desc.add<InputTag>("jetSubjetIndex2", 	InputTag("jetsAK8CHS:jetAK8CHSvSubjetIndex2"));
	desc.add<InputTag>("jetSubjetIndex3", 	InputTag("jetsAK8CHS:jetAK8CHSvSubjetIndex3"));
	desc.add<InputTag>("jetKeys", 	InputTag("jetKeysAK8CHS"));
	desc.add<InputTag>("jetCSVv2", 	InputTag("jetsAK8CHS:jetAK8CHSCSVv2"));
	// JetID
	desc.add<InputTag>("jecFactor", 		InputTag("jetsAK8CHS:jetAK8CHSjecFactor0"));
	desc.add<InputTag>("neutralHadronEnergy", 	InputTag("jetsAK8CHS:jetAK8CHSneutralHadronEnergy"));
	desc.add<InputTag>("neutralEmEnergy", 		InputTag("jetsAK8CHS:jetAK8CHSneutralEmEnergy"));
	desc.add<InputTag>("chargedEmEnergy", 		InputTag("jetsAK8CHS:jetAK8CHSchargedEmEnergy"));
	desc.add<InputTag>("muonEnergy", 		InputTag("jetsAK8CHS:jetAK8CHSMuonEnergy"));
	desc.add<InputTag>("chargedHadronEnergy", 	InputTag("jetsAK8CHS:jetAK8CHSchargedHadronEnergy"));
	desc.add<InputTag>("chargedHadronMultiplicity",	InputTag("jetsAK8CHS:jetAK8CHSChargedHadronMultiplicity"));
	desc.add<InputTag>("neutralHadronMultiplicity",	InputTag("jetsAK8CHS:jetAK8CHSneutralHadronMultiplicity"));
	desc.add<InputTag>("chargedMultiplicity", 	InputTag("jetsAK8CHS:jetAK8CHSchargedMultiplicity"));
	// Trigger
	desc.add<InputTag>("triggerBit",		InputTag("TriggerUserData:triggerBitTree"));
	desc.add<InputTag>("triggerName",		InputTag("TriggerUserData:triggerNameTree"));
	// Subjets
	desc.add<InputTag>("subjetPt", 	InputTag("subjetsAK8CHS:subjetAK8CHSPt"));
	desc.add<InputTag>("subjetEta", 	InputTag("subjetsAK8CHS:subjetAK8CHSEta"));
	desc.add<InputTag>("subjetPhi", 	InputTag("subjetsAK8CHS:subjetAK8CHSPhi"));
	desc.add<InputTag>("subjetE", 	InputTag("subjetsAK8CHS:subjetAK8CHSE"));
	desc.add<InputTag>("subjetMass", 	InputTag("subjetsAK8CHS:subjetAK8CHSMass"));
	descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(RUNBoostedTriggerEfficiency);
