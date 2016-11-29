// -*- C++ -*-
//
// Package:    RUNA/RUNTriggerEfficiency
// Class:      RUNBoostedMiniAODTriggerEfficiency
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
#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/HLTReco/interface/TriggerObject.h"
#include "DataFormats/HLTReco/interface/TriggerEvent.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"
#include "DataFormats/PatCandidates/interface/PackedTriggerPrescales.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

#include "RUNA/RUNAnalysis/interface/CommonVariablesStructure.h"

using namespace edm;
using namespace std;

//
// constants, enums and typedefs
//

//
// class declaration
//
class RUNBoostedMiniAODTriggerEfficiency : public EDAnalyzer {
	public:
		explicit RUNBoostedMiniAODTriggerEfficiency(const ParameterSet&);
		static void fillDescriptions(edm::ConfigurationDescriptions & descriptions);
		~RUNBoostedMiniAODTriggerEfficiency();

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

		double cutAK8jetPt;
		double cutAK8HT;
		double cutAK8jet1Pt;
		double cutAK8jet2Pt;
		double cutAK8jet1Mass;
		TString baseTrigger;
		vector<string> triggerPass;

		edm::EDGetTokenT<edm::TriggerResults> triggerBits_;
		edm::EDGetTokenT<pat::PackedTriggerPrescales> triggerPrescales_;
		edm::EDGetTokenT<trigger::TriggerEvent> triggerEvent_;
		edm::EDGetTokenT<pat::JetCollection> jetToken_;
};

//
// static data member definitions
//

//
// constructors and destructor
//
RUNBoostedMiniAODTriggerEfficiency::RUNBoostedMiniAODTriggerEfficiency(const ParameterSet& iConfig):
	triggerBits_(consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("bits"))),
	triggerPrescales_(consumes<pat::PackedTriggerPrescales>(iConfig.getParameter<edm::InputTag>("prescales"))),
	triggerEvent_(consumes<trigger::TriggerEvent>(iConfig.getParameter<edm::InputTag>("hltTrigger"))),
	jetToken_(consumes<pat::JetCollection>(iConfig.getParameter<edm::InputTag>("recoJets")))
{
	cutAK8jetPt = iConfig.getParameter<double>("cutAK8jetPt");
	cutAK8HT = iConfig.getParameter<double>("cutAK8HT");
	cutAK8jet1Pt = iConfig.getParameter<double>("cutAK8jet1Pt");
	cutAK8jet2Pt = iConfig.getParameter<double>("cutAK8jet2Pt");
	cutAK8jet1Mass = iConfig.getParameter<double>("cutAK8jet1Mass");
	baseTrigger = iConfig.getParameter<string>("baseTrigger");
	triggerPass = iConfig.getParameter<vector<string>>("triggerPass");
}


RUNBoostedMiniAODTriggerEfficiency::~RUNBoostedMiniAODTriggerEfficiency()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void RUNBoostedMiniAODTriggerEfficiency::analyze(const Event& iEvent, const EventSetup& iSetup) {

	edm::Handle<edm::TriggerResults> triggerBits;
	edm::Handle<pat::PackedTriggerPrescales> triggerPrescales;
	edm::Handle<trigger::TriggerEvent> trigEvent; 
	edm::Handle<pat::JetCollection> jets;

	iEvent.getByToken(triggerBits_, triggerBits);
	iEvent.getByToken(triggerPrescales_, triggerPrescales);
	iEvent.getByToken(triggerEvent_,trigEvent);
	iEvent.getByToken(jetToken_, jets);

	const edm::TriggerNames &names = iEvent.triggerNames(*triggerBits);
  	bool ORTriggers = checkORListOfTriggerBitsMiniAOD( names, triggerBits, triggerPrescales, triggerPass, false );
  	bool basedTriggerFired = checkTriggerBitsMiniAOD( names, triggerBits, triggerPrescales, baseTrigger, true );

	/// Applying kinematic, trigger and jet ID
	pat::JetCollection JETS;
	vector<TLorentzVector> puppiJETS;
	float HT = 0, puppiHT = 0;

	for (const pat::Jet &jet : *jets) {

		if ( TMath::Abs( jet.eta() ) > 2.4 ) continue;
		string typeOfJetID = "looseJetID";	// check trigger with looser jet id
		bool idL = jetID( jet.eta(), jet.energy(), jet.jecFactor(0), jet.neutralHadronEnergyFraction(), jet.neutralEmEnergyFraction(), jet.chargedHadronEnergyFraction(), jet.muonEnergy(), jet.chargedEmEnergyFraction(), jet.chargedMultiplicity(), jet.neutralMultiplicity(), typeOfJetID ); 

		if( ( jet.pt() > cutAK8jetPt ) && idL ) { 
			HT += jet.pt();
			JETS.push_back( jet );
		}
		
		///// Puppi jets
		if ( jet.userFloat("ak8PFJetsPuppiValueMap:pt") > cutAK8jetPt && idL ){
			puppiHT += jet.userFloat("ak8PFJetsPuppiValueMap:pt");

			TLorentzVector puppi_softdrop, puppi_softdrop_subjet;
			auto const & sdSubjetsPuppi = jet.subjets("SoftDropPuppi");
			for ( auto const & it : sdSubjetsPuppi ) {
				puppi_softdrop_subjet.SetPtEtaPhiM(it->pt(),it->eta(),it->phi(),it->mass());
				puppi_softdrop+=puppi_softdrop_subjet;
			}
			///// I am artificially storing softdrop mass as mass jet, just for simplicity
			TLorentzVector puppijet;
			puppijet.SetPtEtaPhiM( jet.userFloat("ak8PFJetsPuppiValueMap:pt"), jet.userFloat("ak8PFJetsPuppiValueMap:eta"), jet.userFloat("ak8PFJetsPuppiValueMap:phi"), puppi_softdrop.M() );
			puppiJETS.push_back( puppijet );

		}
	}


	if ( JETS.size() > 1 ) {

		// Mass average 
		float prunedMassAve = massAverage( JETS[0].userFloat("ak8PFJetsCHSPrunedMass"), JETS[1].userFloat("ak8PFJetsCHSPrunedMass") );
		//////////////////////////////////////////////////////////////////////////

		
		histos2D_[ "jet1PrunedMassHT_cutDijet_noTrigger" ]->Fill( JETS[0].userFloat("ak8PFJetsCHSPrunedMass"), HT );

		if ( basedTriggerFired || ORTriggers ) {
			if ( basedTriggerFired && ORTriggers ) {
				histos2D_[ "jet1PrunedMassHT_cutDijet_triggerOneAndTwo" ]->Fill( JETS[0].userFloat("ak8PFJetsCHSPrunedMass"), HT );
			} else if ( basedTriggerFired ) {
				histos2D_[ "jet1PrunedMassHT_cutDijet_triggerOne" ]->Fill( JETS[0].userFloat("ak8PFJetsCHSPrunedMass"), HT );
			} else if ( ORTriggers ) {
				histos2D_[ "jet1PrunedMassHT_cutDijet_triggerTwo" ]->Fill( JETS[0].userFloat("ak8PFJetsCHSPrunedMass"), HT );
			}
		} else {
			histos2D_[ "jet1PrunedMassHT_cutDijet_noTriggerOneOrTwo" ]->Fill( JETS[0].userFloat("ak8PFJetsCHSPrunedMass"), HT );
		}


		if ( basedTriggerFired ) {
			histos1D_[ "HTDenom_cutDijet" ]->Fill( HT  );
			histos1D_[ "prunedMassAveDenom_cutDijet" ]->Fill( prunedMassAve );
			histos1D_[ "jet1PrunedMassDenom_cutDijet" ]->Fill( JETS[0].userFloat("ak8PFJetsCHSPrunedMass")  );
			histos1D_[ "jet1PtDenom_cutDijet" ]->Fill( JETS[0].pt()   );
			histos1D_[ "jet2PrunedMassDenom_cutDijet" ]->Fill( JETS[1].userFloat("ak8PFJetsCHSPrunedMass")  );
			histos1D_[ "jet2PtDenom_cutDijet" ]->Fill( JETS[1].pt() );

			histos2D_[ "jet1PrunedMassHTDenom_cutDijet" ]->Fill( JETS[0].userFloat("ak8PFJetsCHSPrunedMass"), HT );
			histos2D_[ "jet1PrunedMassjet1PtDenom_cutDijet" ]->Fill( JETS[0].userFloat("ak8PFJetsCHSPrunedMass"), JETS[0].pt() );

			histos2D_[ "jet2PrunedMassHTDenom_cutDijet" ]->Fill( JETS[1].userFloat("ak8PFJetsCHSPrunedMass"), HT );
			histos2D_[ "jet2PrunedMassjet2PtDenom_cutDijet" ]->Fill( JETS[1].userFloat("ak8PFJetsCHSPrunedMass"), JETS[1].pt() );

			histos2D_[ "prunedMassAveHTDenom_cutDijet" ]->Fill( prunedMassAve, HT );
			histos2D_[ "prunedMassAvejet1PtDenom_cutDijet" ]->Fill( prunedMassAve, JETS[0].pt() );
			histos2D_[ "prunedMassAvejet2PtDenom_cutDijet" ]->Fill( prunedMassAve, JETS[1].pt() );

			if ( ORTriggers ){
				histos1D_[ "HTPassing_cutDijet" ]->Fill( HT  );
				histos1D_[ "prunedMassAvePassing_cutDijet" ]->Fill( prunedMassAve );
				histos1D_[ "jet1PrunedMassPassing_cutDijet" ]->Fill( JETS[0].userFloat("ak8PFJetsCHSPrunedMass")  );
				histos1D_[ "jet1PtPassing_cutDijet" ]->Fill( JETS[0].pt()   );
				histos1D_[ "jet2PrunedMassPassing_cutDijet" ]->Fill( JETS[1].userFloat("ak8PFJetsCHSPrunedMass")  );
				histos1D_[ "jet2PtPassing_cutDijet" ]->Fill( JETS[1].pt() );

				histos2D_[ "jet1PrunedMassHTPassing_cutDijet" ]->Fill( JETS[0].userFloat("ak8PFJetsCHSPrunedMass"), HT );
				histos2D_[ "jet1PrunedMassjet1PtPassing_cutDijet" ]->Fill( JETS[0].userFloat("ak8PFJetsCHSPrunedMass"), JETS[0].pt() );

				histos2D_[ "jet2PrunedMassHTPassing_cutDijet" ]->Fill( JETS[1].userFloat("ak8PFJetsCHSPrunedMass"), HT );
				histos2D_[ "jet2PrunedMassjet2PtPassing_cutDijet" ]->Fill( JETS[1].userFloat("ak8PFJetsCHSPrunedMass"), JETS[1].pt() );

				histos2D_[ "prunedMassAveHTPassing_cutDijet" ]->Fill( prunedMassAve, HT );
				histos2D_[ "prunedMassAvejet1PtPassing_cutDijet" ]->Fill( prunedMassAve, JETS[0].pt() );
				histos2D_[ "prunedMassAvejet2PtPassing_cutDijet" ]->Fill( prunedMassAve, JETS[1].pt() );
			}

			if ( HT > cutAK8HT ) {
				histos1D_[ "HTDenom_cutHT" ]->Fill( HT  );
				histos1D_[ "prunedMassAveDenom_cutHT" ]->Fill( prunedMassAve );
				histos1D_[ "jet1PrunedMassDenom_cutHT" ]->Fill( JETS[0].userFloat("ak8PFJetsCHSPrunedMass")  );
				histos1D_[ "jet1PtDenom_cutHT" ]->Fill( JETS[0].pt()   );
				histos1D_[ "jet2PrunedMassDenom_cutHT" ]->Fill( JETS[1].userFloat("ak8PFJetsCHSPrunedMass")  );
				histos1D_[ "jet2PtDenom_cutHT" ]->Fill( JETS[1].pt() );

				histos2D_[ "jet1PrunedMassHTDenom_cutHT" ]->Fill( JETS[0].userFloat("ak8PFJetsCHSPrunedMass"), HT );
				histos2D_[ "jet1PrunedMassjet1PtDenom_cutHT" ]->Fill( JETS[0].userFloat("ak8PFJetsCHSPrunedMass"), JETS[0].pt() );

				histos2D_[ "jet2PrunedMassHTDenom_cutHT" ]->Fill( JETS[1].userFloat("ak8PFJetsCHSPrunedMass"), HT );
				histos2D_[ "jet2PrunedMassjet2PtDenom_cutHT" ]->Fill( JETS[1].userFloat("ak8PFJetsCHSPrunedMass"), JETS[1].pt() );

				histos2D_[ "prunedMassAveHTDenom_cutHT" ]->Fill( prunedMassAve, HT );
				histos2D_[ "prunedMassAvejet1PtDenom_cutHT" ]->Fill( prunedMassAve, JETS[0].pt() );
				histos2D_[ "prunedMassAvejet2PtDenom_cutHT" ]->Fill( prunedMassAve, JETS[1].pt() );

				if ( ORTriggers ){
					histos1D_[ "HTPassing_cutHT" ]->Fill( HT  );
					histos1D_[ "prunedMassAvePassing_cutHT" ]->Fill( prunedMassAve );
					histos1D_[ "jet1PrunedMassPassing_cutHT" ]->Fill( JETS[0].userFloat("ak8PFJetsCHSPrunedMass")  );
					histos1D_[ "jet1PtPassing_cutHT" ]->Fill( JETS[0].pt()   );
					histos1D_[ "jet2PrunedMassPassing_cutHT" ]->Fill( JETS[1].userFloat("ak8PFJetsCHSPrunedMass")  );
					histos1D_[ "jet2PtPassing_cutHT" ]->Fill( JETS[1].pt() );

					histos2D_[ "jet1PrunedMassHTPassing_cutHT" ]->Fill( JETS[0].userFloat("ak8PFJetsCHSPrunedMass"), HT );
					histos2D_[ "jet1PrunedMassjet1PtPassing_cutHT" ]->Fill( JETS[0].userFloat("ak8PFJetsCHSPrunedMass"), JETS[0].pt() );

					histos2D_[ "jet2PrunedMassHTPassing_cutHT" ]->Fill( JETS[1].userFloat("ak8PFJetsCHSPrunedMass"), HT );
					histos2D_[ "jet2PrunedMassjet2PtPassing_cutHT" ]->Fill( JETS[1].userFloat("ak8PFJetsCHSPrunedMass"), JETS[1].pt() );

					histos2D_[ "prunedMassAveHTPassing_cutHT" ]->Fill( prunedMassAve, HT );
					histos2D_[ "prunedMassAvejet1PtPassing_cutHT" ]->Fill( prunedMassAve, JETS[0].pt() );
					histos2D_[ "prunedMassAvejet2PtPassing_cutHT" ]->Fill( prunedMassAve, JETS[1].pt() );
				}
			}


			if ( JETS[0].userFloat("ak8PFJetsCHSPrunedMass") > cutAK8jet1Mass ) {
				histos1D_[ "HTDenom_cutjet1PrunedMass" ]->Fill( HT  );
				histos1D_[ "prunedMassAveDenom_cutjet1PrunedMass" ]->Fill( prunedMassAve );
				histos1D_[ "jet1PrunedMassDenom_cutjet1PrunedMass" ]->Fill( JETS[0].userFloat("ak8PFJetsCHSPrunedMass")  );
				histos1D_[ "jet1PtDenom_cutjet1PrunedMass" ]->Fill( JETS[0].pt()   );
				histos1D_[ "jet2PrunedMassDenom_cutjet1PrunedMass" ]->Fill( JETS[1].userFloat("ak8PFJetsCHSPrunedMass")  );
				histos1D_[ "jet2PtDenom_cutjet1PrunedMass" ]->Fill( JETS[1].pt() );

				histos2D_[ "jet1PrunedMassHTDenom_cutjet1PrunedMass" ]->Fill( JETS[0].userFloat("ak8PFJetsCHSPrunedMass"), HT );
				histos2D_[ "jet1PrunedMassjet1PtDenom_cutjet1PrunedMass" ]->Fill( JETS[0].userFloat("ak8PFJetsCHSPrunedMass"), JETS[0].pt() );

				histos2D_[ "jet2PrunedMassHTDenom_cutjet1PrunedMass" ]->Fill( JETS[1].userFloat("ak8PFJetsCHSPrunedMass"), HT );
				histos2D_[ "jet2PrunedMassjet2PtDenom_cutjet1PrunedMass" ]->Fill( JETS[1].userFloat("ak8PFJetsCHSPrunedMass"), JETS[1].pt() );

				histos2D_[ "prunedMassAveHTDenom_cutjet1PrunedMass" ]->Fill( prunedMassAve, HT );
				histos2D_[ "prunedMassAvejet1PtDenom_cutjet1PrunedMass" ]->Fill( prunedMassAve, JETS[0].pt() );
				histos2D_[ "prunedMassAvejet2PtDenom_cutjet1PrunedMass" ]->Fill( prunedMassAve, JETS[1].pt() );

				if ( ORTriggers ){
					histos1D_[ "HTPassing_cutjet1PrunedMass" ]->Fill( HT  );
					histos1D_[ "prunedMassAvePassing_cutjet1PrunedMass" ]->Fill( prunedMassAve );
					histos1D_[ "jet1PrunedMassPassing_cutjet1PrunedMass" ]->Fill( JETS[0].userFloat("ak8PFJetsCHSPrunedMass")  );
					histos1D_[ "jet1PtPassing_cutjet1PrunedMass" ]->Fill( JETS[0].pt()   );
					histos1D_[ "jet2PrunedMassPassing_cutjet1PrunedMass" ]->Fill( JETS[1].userFloat("ak8PFJetsCHSPrunedMass")  );
					histos1D_[ "jet2PtPassing_cutjet1PrunedMass" ]->Fill( JETS[1].pt() );

					histos2D_[ "jet1PrunedMassHTPassing_cutjet1PrunedMass" ]->Fill( JETS[0].userFloat("ak8PFJetsCHSPrunedMass"), HT );
					histos2D_[ "jet1PrunedMassjet1PtPassing_cutjet1PrunedMass" ]->Fill( JETS[0].userFloat("ak8PFJetsCHSPrunedMass"), JETS[0].pt() );

					histos2D_[ "jet2PrunedMassHTPassing_cutjet1PrunedMass" ]->Fill( JETS[1].userFloat("ak8PFJetsCHSPrunedMass"), HT );
					histos2D_[ "jet2PrunedMassjet2PtPassing_cutjet1PrunedMass" ]->Fill( JETS[1].userFloat("ak8PFJetsCHSPrunedMass"), JETS[1].pt() );

					histos2D_[ "prunedMassAveHTPassing_cutjet1PrunedMass" ]->Fill( prunedMassAve, HT );
					histos2D_[ "prunedMassAvejet1PtPassing_cutjet1PrunedMass" ]->Fill( prunedMassAve, JETS[0].pt() );
					histos2D_[ "prunedMassAvejet2PtPassing_cutjet1PrunedMass" ]->Fill( prunedMassAve, JETS[1].pt() );
				}
			}


			if ( ( JETS[0].pt() > cutAK8jet1Pt ) && ( JETS[1].pt() > cutAK8jet2Pt ) ) {
				histos1D_[ "HTDenom_cut2jetsPt" ]->Fill( HT  );
				histos1D_[ "prunedMassAveDenom_cut2jetsPt" ]->Fill( prunedMassAve );
				histos1D_[ "jet1PrunedMassDenom_cut2jetsPt" ]->Fill( JETS[0].userFloat("ak8PFJetsCHSPrunedMass")  );
				histos1D_[ "jet1PtDenom_cut2jetsPt" ]->Fill( JETS[0].pt()   );
				histos1D_[ "jet2PrunedMassDenom_cut2jetsPt" ]->Fill( JETS[1].userFloat("ak8PFJetsCHSPrunedMass")  );
				histos1D_[ "jet2PtDenom_cut2jetsPt" ]->Fill( JETS[1].pt() );

				histos2D_[ "jet1PrunedMassHTDenom_cut2jetsPt" ]->Fill( JETS[0].userFloat("ak8PFJetsCHSPrunedMass"), HT );
				histos2D_[ "jet1PrunedMassjet1PtDenom_cut2jetsPt" ]->Fill( JETS[0].userFloat("ak8PFJetsCHSPrunedMass"), JETS[0].pt() );

				histos2D_[ "jet2PrunedMassHTDenom_cut2jetsPt" ]->Fill( JETS[1].userFloat("ak8PFJetsCHSPrunedMass"), HT );
				histos2D_[ "jet2PrunedMassjet2PtDenom_cut2jetsPt" ]->Fill( JETS[1].userFloat("ak8PFJetsCHSPrunedMass"), JETS[1].pt() );

				histos2D_[ "prunedMassAveHTDenom_cut2jetsPt" ]->Fill( prunedMassAve, HT );
				histos2D_[ "prunedMassAvejet1PtDenom_cut2jetsPt" ]->Fill( prunedMassAve, JETS[0].pt() );
				histos2D_[ "prunedMassAvejet2PtDenom_cut2jetsPt" ]->Fill( prunedMassAve, JETS[1].pt() );

				if ( ORTriggers ){
					histos1D_[ "HTPassing_cut2jetsPt" ]->Fill( HT  );
					histos1D_[ "prunedMassAvePassing_cut2jetsPt" ]->Fill( prunedMassAve );
					histos1D_[ "jet1PrunedMassPassing_cut2jetsPt" ]->Fill( JETS[0].userFloat("ak8PFJetsCHSPrunedMass")  );
					histos1D_[ "jet1PtPassing_cut2jetsPt" ]->Fill( JETS[0].pt()   );
					histos1D_[ "jet2PrunedMassPassing_cut2jetsPt" ]->Fill( JETS[1].userFloat("ak8PFJetsCHSPrunedMass")  );
					histos1D_[ "jet2PtPassing_cut2jetsPt" ]->Fill( JETS[1].pt() );

					histos2D_[ "jet1PrunedMassHTPassing_cut2jetsPt" ]->Fill( JETS[0].userFloat("ak8PFJetsCHSPrunedMass"), HT );
					histos2D_[ "jet1PrunedMassjet1PtPassing_cut2jetsPt" ]->Fill( JETS[0].userFloat("ak8PFJetsCHSPrunedMass"), JETS[0].pt() );

					histos2D_[ "jet2PrunedMassHTPassing_cut2jetsPt" ]->Fill( JETS[1].userFloat("ak8PFJetsCHSPrunedMass"), HT );
					histos2D_[ "jet2PrunedMassjet2PtPassing_cut2jetsPt" ]->Fill( JETS[1].userFloat("ak8PFJetsCHSPrunedMass"), JETS[1].pt() );

					histos2D_[ "prunedMassAveHTPassing_cut2jetsPt" ]->Fill( prunedMassAve, HT );
					histos2D_[ "prunedMassAvejet1PtPassing_cut2jetsPt" ]->Fill( prunedMassAve, JETS[0].pt() );
					histos2D_[ "prunedMassAvejet2PtPassing_cut2jetsPt" ]->Fill( prunedMassAve, JETS[1].pt() );
				}
			}
		}
	}
	JETS.clear();

	///// Puppi jets
	if ( puppiJETS.size() > 1 ) {

		// Mass average 
		float softDropMassAve = massAverage( puppiJETS[0].M(), puppiJETS[1].M() );
		//////////////////////////////////////////////////////////////////////////

		
		histos2D_[ "jet1SoftDropMassHT_cutDijet_noTrigger" ]->Fill( puppiJETS[0].M(), puppiHT );

		if ( basedTriggerFired || ORTriggers ) {
			if ( basedTriggerFired && ORTriggers ) {
				histos2D_[ "jet1SoftDropMassHT_cutDijet_triggerOneAndTwo" ]->Fill( puppiJETS[0].M(), puppiHT );
			} else if ( basedTriggerFired ) {
				histos2D_[ "jet1SoftDropMassHT_cutDijet_triggerOne" ]->Fill( puppiJETS[0].M(), puppiHT );
			} else if ( ORTriggers ) {
				histos2D_[ "jet1SoftDropMassHT_cutDijet_triggerTwo" ]->Fill( puppiJETS[0].M(), puppiHT );
			}
		} else {
			histos2D_[ "jet1SoftDropMassHT_cutDijet_noTriggerOneOrTwo" ]->Fill( puppiJETS[0].M(), puppiHT );
		}


		if ( basedTriggerFired ) {
			histos1D_[ "puppiHTDenom_cutDijet" ]->Fill( puppiHT  );
			histos1D_[ "softDropMassAveDenom_cutDijet" ]->Fill( softDropMassAve );
			histos1D_[ "jet1SoftDropMassDenom_cutDijet" ]->Fill( puppiJETS[0].M()  );
			histos1D_[ "puppiJet1PtDenom_cutDijet" ]->Fill( puppiJETS[0].Pt()   );
			histos1D_[ "jet2SoftDropMassDenom_cutDijet" ]->Fill( puppiJETS[1].M()  );
			histos1D_[ "puppiJet2PtDenom_cutDijet" ]->Fill( puppiJETS[1].Pt() );

			histos2D_[ "jet1SoftDropMassHTDenom_cutDijet" ]->Fill( puppiJETS[0].M(), puppiHT );
			histos2D_[ "jet1SoftDropMassjet1PtDenom_cutDijet" ]->Fill( puppiJETS[0].M(), puppiJETS[0].Pt() );

			histos2D_[ "jet2SoftDropMassHTDenom_cutDijet" ]->Fill( puppiJETS[1].M(), puppiHT );
			histos2D_[ "jet2SoftDropMassjet2PtDenom_cutDijet" ]->Fill( puppiJETS[1].M(), puppiJETS[1].Pt() );

			histos2D_[ "softDropMassAveHTDenom_cutDijet" ]->Fill( softDropMassAve, puppiHT );
			histos2D_[ "softDropMassAvejet1PtDenom_cutDijet" ]->Fill( softDropMassAve, puppiJETS[0].Pt() );
			histos2D_[ "softDropMassAvejet2PtDenom_cutDijet" ]->Fill( softDropMassAve, puppiJETS[1].Pt() );

			if ( ORTriggers ){
				histos1D_[ "puppiHTPassing_cutDijet" ]->Fill( puppiHT  );
				histos1D_[ "softDropMassAvePassing_cutDijet" ]->Fill( softDropMassAve );
				histos1D_[ "jet1SoftDropMassPassing_cutDijet" ]->Fill( puppiJETS[0].M()  );
				histos1D_[ "puppiJet1PtPassing_cutDijet" ]->Fill( puppiJETS[0].Pt()   );
				histos1D_[ "jet2SoftDropMassPassing_cutDijet" ]->Fill( puppiJETS[1].M()  );
				histos1D_[ "puppiJet2PtPassing_cutDijet" ]->Fill( puppiJETS[1].Pt() );

				histos2D_[ "jet1SoftDropMassHTPassing_cutDijet" ]->Fill( puppiJETS[0].M(), puppiHT );
				histos2D_[ "jet1SoftDropMassjet1PtPassing_cutDijet" ]->Fill( puppiJETS[0].M(), puppiJETS[0].Pt() );

				histos2D_[ "jet2SoftDropMassHTPassing_cutDijet" ]->Fill( puppiJETS[1].M(), puppiHT );
				histos2D_[ "jet2SoftDropMassjet2PtPassing_cutDijet" ]->Fill( puppiJETS[1].M(), puppiJETS[1].Pt() );

				histos2D_[ "softDropMassAveHTPassing_cutDijet" ]->Fill( softDropMassAve, puppiHT );
				histos2D_[ "softDropMassAvejet1PtPassing_cutDijet" ]->Fill( softDropMassAve, puppiJETS[0].Pt() );
				histos2D_[ "softDropMassAvejet2PtPassing_cutDijet" ]->Fill( softDropMassAve, puppiJETS[1].Pt() );
			}

			if ( puppiHT > cutAK8HT ) {
				histos1D_[ "puppiHTDenom_cutHT" ]->Fill( puppiHT  );
				histos1D_[ "softDropMassAveDenom_cutHT" ]->Fill( softDropMassAve );
				histos1D_[ "jet1SoftDropMassDenom_cutHT" ]->Fill( puppiJETS[0].M()  );
				histos1D_[ "puppiJet1PtDenom_cutHT" ]->Fill( puppiJETS[0].Pt()   );
				histos1D_[ "jet2SoftDropMassDenom_cutHT" ]->Fill( puppiJETS[1].M()  );
				histos1D_[ "puppiJet2PtDenom_cutHT" ]->Fill( puppiJETS[1].Pt() );

				histos2D_[ "jet1SoftDropMassHTDenom_cutHT" ]->Fill( puppiJETS[0].M(), puppiHT );
				histos2D_[ "jet1SoftDropMassjet1PtDenom_cutHT" ]->Fill( puppiJETS[0].M(), puppiJETS[0].Pt() );

				histos2D_[ "jet2SoftDropMassHTDenom_cutHT" ]->Fill( puppiJETS[1].M(), puppiHT );
				histos2D_[ "jet2SoftDropMassjet2PtDenom_cutHT" ]->Fill( puppiJETS[1].M(), puppiJETS[1].Pt() );

				histos2D_[ "softDropMassAveHTDenom_cutHT" ]->Fill( softDropMassAve, puppiHT );
				histos2D_[ "softDropMassAvejet1PtDenom_cutHT" ]->Fill( softDropMassAve, puppiJETS[0].Pt() );
				histos2D_[ "softDropMassAvejet2PtDenom_cutHT" ]->Fill( softDropMassAve, puppiJETS[1].Pt() );

				if ( ORTriggers ){
					histos1D_[ "puppiHTPassing_cutHT" ]->Fill( puppiHT  );
					histos1D_[ "softDropMassAvePassing_cutHT" ]->Fill( softDropMassAve );
					histos1D_[ "jet1SoftDropMassPassing_cutHT" ]->Fill( puppiJETS[0].M()  );
					histos1D_[ "puppiJet1PtPassing_cutHT" ]->Fill( puppiJETS[0].Pt()   );
					histos1D_[ "jet2SoftDropMassPassing_cutHT" ]->Fill( puppiJETS[1].M()  );
					histos1D_[ "puppiJet2PtPassing_cutHT" ]->Fill( puppiJETS[1].Pt() );

					histos2D_[ "jet1SoftDropMassHTPassing_cutHT" ]->Fill( puppiJETS[0].M(), puppiHT );
					histos2D_[ "jet1SoftDropMassjet1PtPassing_cutHT" ]->Fill( puppiJETS[0].M(), puppiJETS[0].Pt() );

					histos2D_[ "jet2SoftDropMassHTPassing_cutHT" ]->Fill( puppiJETS[1].M(), puppiHT );
					histos2D_[ "jet2SoftDropMassjet2PtPassing_cutHT" ]->Fill( puppiJETS[1].M(), puppiJETS[1].Pt() );

					histos2D_[ "softDropMassAveHTPassing_cutHT" ]->Fill( softDropMassAve, puppiHT );
					histos2D_[ "softDropMassAvejet1PtPassing_cutHT" ]->Fill( softDropMassAve, puppiJETS[0].Pt() );
					histos2D_[ "softDropMassAvejet2PtPassing_cutHT" ]->Fill( softDropMassAve, puppiJETS[1].Pt() );
				}
			}

			if ( puppiJETS[0].M() > cutAK8jet1Mass ) {
				histos1D_[ "puppiHTDenom_cutjet1SoftDropMass" ]->Fill( puppiHT  );
				histos1D_[ "softDropMassAveDenom_cutjet1SoftDropMass" ]->Fill( softDropMassAve );
				histos1D_[ "jet1SoftDropMassDenom_cutjet1SoftDropMass" ]->Fill( puppiJETS[0].M()  );
				histos1D_[ "puppiJet1PtDenom_cutjet1SoftDropMass" ]->Fill( puppiJETS[0].Pt()   );
				histos1D_[ "jet2SoftDropMassDenom_cutjet1SoftDropMass" ]->Fill( puppiJETS[1].M()  );
				histos1D_[ "puppiJet2PtDenom_cutjet1SoftDropMass" ]->Fill( puppiJETS[1].Pt() );

				histos2D_[ "jet1SoftDropMassHTDenom_cutjet1SoftDropMass" ]->Fill( puppiJETS[0].M(), puppiHT );
				histos2D_[ "jet1SoftDropMassjet1PtDenom_cutjet1SoftDropMass" ]->Fill( puppiJETS[0].M(), puppiJETS[0].Pt() );

				histos2D_[ "jet2SoftDropMassHTDenom_cutjet1SoftDropMass" ]->Fill( puppiJETS[1].M(), puppiHT );
				histos2D_[ "jet2SoftDropMassjet2PtDenom_cutjet1SoftDropMass" ]->Fill( puppiJETS[1].M(), puppiJETS[1].Pt() );

				histos2D_[ "softDropMassAveHTDenom_cutjet1SoftDropMass" ]->Fill( softDropMassAve, puppiHT );
				histos2D_[ "softDropMassAvejet1PtDenom_cutjet1SoftDropMass" ]->Fill( softDropMassAve, puppiJETS[0].Pt() );
				histos2D_[ "softDropMassAvejet2PtDenom_cutjet1SoftDropMass" ]->Fill( softDropMassAve, puppiJETS[1].Pt() );

				if ( ORTriggers ){
					histos1D_[ "puppiHTPassing_cutjet1SoftDropMass" ]->Fill( puppiHT  );
					histos1D_[ "softDropMassAvePassing_cutjet1SoftDropMass" ]->Fill( softDropMassAve );
					histos1D_[ "jet1SoftDropMassPassing_cutjet1SoftDropMass" ]->Fill( puppiJETS[0].M()  );
					histos1D_[ "puppiJet1PtPassing_cutjet1SoftDropMass" ]->Fill( puppiJETS[0].Pt()   );
					histos1D_[ "jet2SoftDropMassPassing_cutjet1SoftDropMass" ]->Fill( puppiJETS[1].M()  );
					histos1D_[ "puppiJet2PtPassing_cutjet1SoftDropMass" ]->Fill( puppiJETS[1].Pt() );

					histos2D_[ "jet1SoftDropMassHTPassing_cutjet1SoftDropMass" ]->Fill( puppiJETS[0].M(), puppiHT );
					histos2D_[ "jet1SoftDropMassjet1PtPassing_cutjet1SoftDropMass" ]->Fill( puppiJETS[0].M(), puppiJETS[0].Pt() );

					histos2D_[ "jet2SoftDropMassHTPassing_cutjet1SoftDropMass" ]->Fill( puppiJETS[1].M(), puppiHT );
					histos2D_[ "jet2SoftDropMassjet2PtPassing_cutjet1SoftDropMass" ]->Fill( puppiJETS[1].M(), puppiJETS[1].Pt() );

					histos2D_[ "softDropMassAveHTPassing_cutjet1SoftDropMass" ]->Fill( softDropMassAve, puppiHT );
					histos2D_[ "softDropMassAvejet1PtPassing_cutjet1SoftDropMass" ]->Fill( softDropMassAve, puppiJETS[0].Pt() );
					histos2D_[ "softDropMassAvejet2PtPassing_cutjet1SoftDropMass" ]->Fill( softDropMassAve, puppiJETS[1].Pt() );
				}
			}

			if ( ( puppiJETS[0].Pt() > cutAK8jet1Pt ) && ( puppiJETS[1].Pt() > cutAK8jet2Pt ) ) {
				histos1D_[ "puppiHTDenom_cut2jetsPt" ]->Fill( puppiHT  );
				histos1D_[ "softDropMassAveDenom_cut2jetsPt" ]->Fill( softDropMassAve );
				histos1D_[ "jet1SoftDropMassDenom_cut2jetsPt" ]->Fill( puppiJETS[0].M()  );
				histos1D_[ "puppiJet1PtDenom_cut2jetsPt" ]->Fill( puppiJETS[0].Pt()   );
				histos1D_[ "jet2SoftDropMassDenom_cut2jetsPt" ]->Fill( puppiJETS[1].M()  );
				histos1D_[ "puppiJet2PtDenom_cut2jetsPt" ]->Fill( puppiJETS[1].Pt() );

				histos2D_[ "jet1SoftDropMassHTDenom_cut2jetsPt" ]->Fill( puppiJETS[0].M(), puppiHT );
				histos2D_[ "jet1SoftDropMassjet1PtDenom_cut2jetsPt" ]->Fill( puppiJETS[0].M(), puppiJETS[0].Pt() );

				histos2D_[ "jet2SoftDropMassHTDenom_cut2jetsPt" ]->Fill( puppiJETS[1].M(), puppiHT );
				histos2D_[ "jet2SoftDropMassjet2PtDenom_cut2jetsPt" ]->Fill( puppiJETS[1].M(), puppiJETS[1].Pt() );

				histos2D_[ "softDropMassAveHTDenom_cut2jetsPt" ]->Fill( softDropMassAve, puppiHT );
				histos2D_[ "softDropMassAvejet1PtDenom_cut2jetsPt" ]->Fill( softDropMassAve, puppiJETS[0].Pt() );
				histos2D_[ "softDropMassAvejet2PtDenom_cut2jetsPt" ]->Fill( softDropMassAve, puppiJETS[1].Pt() );

				if ( ORTriggers ){
					histos1D_[ "puppiHTPassing_cut2jetsPt" ]->Fill( puppiHT  );
					histos1D_[ "softDropMassAvePassing_cut2jetsPt" ]->Fill( softDropMassAve );
					histos1D_[ "jet1SoftDropMassPassing_cut2jetsPt" ]->Fill( puppiJETS[0].M()  );
					histos1D_[ "puppiJet1PtPassing_cut2jetsPt" ]->Fill( puppiJETS[0].Pt()   );
					histos1D_[ "jet2SoftDropMassPassing_cut2jetsPt" ]->Fill( puppiJETS[1].M()  );
					histos1D_[ "puppiJet2PtPassing_cut2jetsPt" ]->Fill( puppiJETS[1].Pt() );

					histos2D_[ "jet1SoftDropMassHTPassing_cut2jetsPt" ]->Fill( puppiJETS[0].M(), puppiHT );
					histos2D_[ "jet1SoftDropMassjet1PtPassing_cut2jetsPt" ]->Fill( puppiJETS[0].M(), puppiJETS[0].Pt() );

					histos2D_[ "jet2SoftDropMassHTPassing_cut2jetsPt" ]->Fill( puppiJETS[1].M(), puppiHT );
					histos2D_[ "jet2SoftDropMassjet2PtPassing_cut2jetsPt" ]->Fill( puppiJETS[1].M(), puppiJETS[1].Pt() );

					histos2D_[ "softDropMassAveHTPassing_cut2jetsPt" ]->Fill( softDropMassAve, puppiHT );
					histos2D_[ "softDropMassAvejet1PtPassing_cut2jetsPt" ]->Fill( softDropMassAve, puppiJETS[0].Pt() );
					histos2D_[ "softDropMassAvejet2PtPassing_cut2jetsPt" ]->Fill( softDropMassAve, puppiJETS[1].Pt() );
				}
			}
		}
	}
	puppiJETS.clear();

}


// ------------ method called once each job just before starting event loop  ------------
void RUNBoostedMiniAODTriggerEfficiency::beginJob() {

	//////// test plots
	histos2D_[ "jet1PrunedMassHT_cutDijet_noTrigger" ] = fs_->make< TH2D >( "jet1PrunedMassHT_cutDijet_noTrigger", "jet1PrunedMassHT", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet1PrunedMassHT_cutDijet_triggerOne" ] = fs_->make< TH2D >( "jet1PrunedMassHT_cutDijet_triggerOne", "jet1PrunedMassHT", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet1PrunedMassHT_cutDijet_triggerTwo" ] = fs_->make< TH2D >( "jet1PrunedMassHT_cutDijet_triggerTwo", "jet1PrunedMassHT", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet1PrunedMassHT_cutDijet_triggerOneAndTwo" ] = fs_->make< TH2D >( "jet1PrunedMassHT_cutDijet_triggerOneAndTwo", "jet1PrunedMassHT", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet1PrunedMassHT_cutDijet_noTriggerOneOrTwo" ] = fs_->make< TH2D >( "jet1PrunedMassHT_cutDijet_noTriggerOneOrTwo", "jet1PrunedMassHT", 60, 0., 600., 500, 0., 5000.);


	histos2D_[ "jet1SoftDropMassHT_cutDijet_noTrigger" ] = fs_->make< TH2D >( "jet1SoftDropMassHT_cutDijet_noTrigger", "jet1SoftDropMassHT", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet1SoftDropMassHT_cutDijet_triggerOne" ] = fs_->make< TH2D >( "jet1SoftDropMassHT_cutDijet_triggerOne", "jet1SoftDropMassHT", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet1SoftDropMassHT_cutDijet_triggerTwo" ] = fs_->make< TH2D >( "jet1SoftDropMassHT_cutDijet_triggerTwo", "jet1SoftDropMassHT", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet1SoftDropMassHT_cutDijet_triggerOneAndTwo" ] = fs_->make< TH2D >( "jet1SoftDropMassHT_cutDijet_triggerOneAndTwo", "jet1SoftDropMassHT", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet1SoftDropMassHT_cutDijet_noTriggerOneOrTwo" ] = fs_->make< TH2D >( "jet1SoftDropMassHT_cutDijet_noTriggerOneOrTwo", "jet1SoftDropMassHT", 60, 0., 600., 500, 0., 5000.);
	///////////////////////////////////////////////////////////////////

	/////// Denom cutDijet	
	histos1D_[ "HTDenom_cutDijet" ] = fs_->make< TH1D >( "HTDenom_cutDijet", "HTDenom_cutDijet", 500, 0., 5000. );
	histos1D_[ "puppiHTDenom_cutDijet" ] = fs_->make< TH1D >( "puppiHTDenom_cutDijet", "puppiHTDenom_cutDijet", 500, 0., 5000. );
	histos1D_[ "prunedMassAveDenom_cutDijet" ] = fs_->make< TH1D >( "prunedMassAveDenom_cutDijet", "prunedMassAveDenom_cutDijet", 60, 0., 600. );
	histos1D_[ "softDropMassAveDenom_cutDijet" ] = fs_->make< TH1D >( "softDropMassAveDenom_cutDijet", "softDropMassAveDenom_cutDijet", 60, 0., 600. );
	histos1D_[ "jet1PrunedMassDenom_cutDijet" ] = fs_->make< TH1D >( "jet1PrunedMassDenom_cutDijet", "jet1PrunedMassDenom_cutDijet", 60, 0., 600. );
	histos1D_[ "jet1SoftDropMassDenom_cutDijet" ] = fs_->make< TH1D >( "jet1SoftDropMassDenom_cutDijet", "jet1SoftDropMassDenom_cutDijet", 60, 0., 600. );
	histos1D_[ "jet1PtDenom_cutDijet" ] = fs_->make< TH1D >( "jet1PtDenom_cutDijet", "jet1PtDenom_cutDijet", 150, 0., 1500. );
	histos1D_[ "puppiJet1PtDenom_cutDijet" ] = fs_->make< TH1D >( "puppiJet1PtDenom_cutDijet", "puppiJet1PtDenom_cutDijet", 150, 0., 1500. );
	histos1D_[ "jet2PrunedMassDenom_cutDijet" ] = fs_->make< TH1D >( "jet2PrunedMassDenom_cutDijet", "jet2PrunedMassDenom_cutDijet", 60, 0., 600. );
	histos1D_[ "jet2SoftDropMassDenom_cutDijet" ] = fs_->make< TH1D >( "jet2SoftDropMassDenom_cutDijet", "jet2SoftDropMassDenom_cutDijet", 60, 0., 600. );
	histos1D_[ "jet2PtDenom_cutDijet" ] = fs_->make< TH1D >( "jet2PtDenom_cutDijet", "jet2PtDenom_cutDijet", 150, 0., 1500. );
	histos1D_[ "puppiJet2PtDenom_cutDijet" ] = fs_->make< TH1D >( "puppiJet2PtDenom_cutDijet", "puppiJet2PtDenom_cutDijet", 150, 0., 1500. );

	histos2D_[ "jet1PrunedMassHTDenom_cutDijet" ] = fs_->make< TH2D >( "jet1PrunedMassHTDenom_cutDijet", "jet1PrunedMassHTDenom_cutDijet", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet1PrunedMassjet1PtDenom_cutDijet" ] = fs_->make< TH2D >( "jet1PrunedMassjet1PtDenom_cutDijet", "jet1PrunedMassjet1PtDenom_cutDijet", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jet1SoftDropMassHTDenom_cutDijet" ] = fs_->make< TH2D >( "jet1SoftDropMassHTDenom_cutDijet", "jet1SoftDropMassHTDenom_cutDijet", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet1SoftDropMassjet1PtDenom_cutDijet" ] = fs_->make< TH2D >( "jet1SoftDropMassjet1PtDenom_cutDijet", "jet1SoftDropMassjet1PtDenom_cutDijet", 60, 0., 600., 150, 0., 1500.);

	histos2D_[ "jet2PrunedMassHTDenom_cutDijet" ] = fs_->make< TH2D >( "jet2PrunedMassHTDenom_cutDijet", "jet2PrunedMassHTDenom_cutDijet", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet2PrunedMassjet2PtDenom_cutDijet" ] = fs_->make< TH2D >( "jet2PrunedMassjet2PtDenom_cutDijet", "jet2PrunedMassjet2PtDenom_cutDijet", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jet2SoftDropMassHTDenom_cutDijet" ] = fs_->make< TH2D >( "jet2SoftDropMassHTDenom_cutDijet", "jet2SoftDropMassHTDenom_cutDijet", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet2SoftDropMassjet2PtDenom_cutDijet" ] = fs_->make< TH2D >( "jet2SoftDropMassjet2PtDenom_cutDijet", "jet2SoftDropMassjet2PtDenom_cutDijet", 60, 0., 600., 150, 0., 1500.);

	histos2D_[ "prunedMassAveHTDenom_cutDijet" ] = fs_->make< TH2D >( "prunedMassAveHTDenom_cutDijet", "prunedMassAveHTDenom_cutDijet", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "prunedMassAvejet1PtDenom_cutDijet" ] = fs_->make< TH2D >( "prunedMassAvejet1PtDenom_cutDijet", "prunedMassAvejet1PtDenom_cutDijet", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "prunedMassAvejet2PtDenom_cutDijet" ] = fs_->make< TH2D >( "prunedMassAvejet2PtDenom_cutDijet", "prunedMassAvejet2PtDenom_cutDijet", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "softDropMassAveHTDenom_cutDijet" ] = fs_->make< TH2D >( "softDropMassAveHTDenom_cutDijet", "softDropMassAveHTDenom_cutDijet", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "softDropMassAvejet1PtDenom_cutDijet" ] = fs_->make< TH2D >( "softDropMassAvejet1PtDenom_cutDijet", "softDropMassAvejet1PtDenom_cutDijet", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "softDropMassAvejet2PtDenom_cutDijet" ] = fs_->make< TH2D >( "softDropMassAvejet2PtDenom_cutDijet", "softDropMassAvejet2PtDenom_cutDijet", 60, 0., 600., 150, 0., 1500.);
	///////////////////////////////////////////////////////////////////


	/////// Passing cutDijet	
	histos1D_[ "HTPassing_cutDijet" ] = fs_->make< TH1D >( "HTPassing_cutDijet", "HTPassing_cutDijet", 500, 0., 5000. );
	histos1D_[ "puppiHTPassing_cutDijet" ] = fs_->make< TH1D >( "puppiHTPassing_cutDijet", "puppiHTPassing_cutDijet", 500, 0., 5000. );
	histos1D_[ "prunedMassAvePassing_cutDijet" ] = fs_->make< TH1D >( "prunedMassAvePassing_cutDijet", "prunedMassAvePassing_cutDijet", 60, 0., 600. );
	histos1D_[ "softDropMassAvePassing_cutDijet" ] = fs_->make< TH1D >( "softDropMassAvePassing_cutDijet", "softDropMassAvePassing_cutDijet", 60, 0., 600. );
	histos1D_[ "jet1PrunedMassPassing_cutDijet" ] = fs_->make< TH1D >( "jet1PrunedMassPassing_cutDijet", "jet1PrunedMassPassing_cutDijet", 60, 0., 600. );
	histos1D_[ "jet1SoftDropMassPassing_cutDijet" ] = fs_->make< TH1D >( "jet1SoftDropMassPassing_cutDijet", "jet1SoftDropMassPassing_cutDijet", 60, 0., 600. );
	histos1D_[ "jet1PtPassing_cutDijet" ] = fs_->make< TH1D >( "jet1PtPassing_cutDijet", "jet1PtPassing_cutDijet", 150, 0., 1500. );
	histos1D_[ "puppiJet1PtPassing_cutDijet" ] = fs_->make< TH1D >( "puppiJet1PtPassing_cutDijet", "puppiJet1PtPassing_cutDijet", 150, 0., 1500. );
	histos1D_[ "jet2PrunedMassPassing_cutDijet" ] = fs_->make< TH1D >( "jet2PrunedMassPassing_cutDijet", "jet2PrunedMassPassing_cutDijet", 60, 0., 600. );
	histos1D_[ "jet2SoftDropMassPassing_cutDijet" ] = fs_->make< TH1D >( "jet2SoftDropMassPassing_cutDijet", "jet2SoftDropMassPassing_cutDijet", 60, 0., 600. );
	histos1D_[ "jet2PtPassing_cutDijet" ] = fs_->make< TH1D >( "jet2PtPassing_cutDijet", "jet2PtPassing_cutDijet", 150, 0., 1500. );
	histos1D_[ "puppiJet2PtPassing_cutDijet" ] = fs_->make< TH1D >( "puppiJet2PtPassing_cutDijet", "puppiJet2PtPassing_cutDijet", 150, 0., 1500. );

	histos2D_[ "jet1PrunedMassHTPassing_cutDijet" ] = fs_->make< TH2D >( "jet1PrunedMassHTPassing_cutDijet", "jet1PrunedMassHTPassing_cutDijet", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet1PrunedMassjet1PtPassing_cutDijet" ] = fs_->make< TH2D >( "jet1PrunedMassjet1PtPassing_cutDijet", "jet1PrunedMassjet1PtPassing_cutDijet", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jet1SoftDropMassHTPassing_cutDijet" ] = fs_->make< TH2D >( "jet1SoftDropMassHTPassing_cutDijet", "jet1SoftDropMassHTPassing_cutDijet", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet1SoftDropMassjet1PtPassing_cutDijet" ] = fs_->make< TH2D >( "jet1SoftDropMassjet1PtPassing_cutDijet", "jet1SoftDropMassjet1PtPassing_cutDijet", 60, 0., 600., 150, 0., 1500.);

	histos2D_[ "jet2PrunedMassHTPassing_cutDijet" ] = fs_->make< TH2D >( "jet2PrunedMassHTPassing_cutDijet", "jet2PrunedMassHTPassing_cutDijet", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet2PrunedMassjet2PtPassing_cutDijet" ] = fs_->make< TH2D >( "jet2PrunedMassjet2PtPassing_cutDijet", "jet2PrunedMassjet2PtPassing_cutDijet", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jet2SoftDropMassHTPassing_cutDijet" ] = fs_->make< TH2D >( "jet2SoftDropMassHTPassing_cutDijet", "jet2SoftDropMassHTPassing_cutDijet", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet2SoftDropMassjet2PtPassing_cutDijet" ] = fs_->make< TH2D >( "jet2SoftDropMassjet2PtPassing_cutDijet", "jet2SoftDropMassjet2PtPassing_cutDijet", 60, 0., 600., 150, 0., 1500.);

	histos2D_[ "prunedMassAveHTPassing_cutDijet" ] = fs_->make< TH2D >( "prunedMassAveHTPassing_cutDijet", "prunedMassAveHTPassing_cutDijet", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "prunedMassAvejet1PtPassing_cutDijet" ] = fs_->make< TH2D >( "prunedMassAvejet1PtPassing_cutDijet", "prunedMassAvejet1PtPassing_cutDijet", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "prunedMassAvejet2PtPassing_cutDijet" ] = fs_->make< TH2D >( "prunedMassAvejet2PtPassing_cutDijet", "prunedMassAvejet2PtPassing_cutDijet", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "softDropMassAveHTPassing_cutDijet" ] = fs_->make< TH2D >( "softDropMassAveHTPassing_cutDijet", "softDropMassAveHTPassing_cutDijet", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "softDropMassAvejet1PtPassing_cutDijet" ] = fs_->make< TH2D >( "softDropMassAvejet1PtPassing_cutDijet", "softDropMassAvejet1PtPassing_cutDijet", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "softDropMassAvejet2PtPassing_cutDijet" ] = fs_->make< TH2D >( "softDropMassAvejet2PtPassing_cutDijet", "softDropMassAvejet2PtPassing_cutDijet", 60, 0., 600., 150, 0., 1500.);
	///////////////////////////////////////////////////////////////////


	/////// Denom cutHT	
	histos1D_[ "HTDenom_cutHT" ] = fs_->make< TH1D >( "HTDenom_cutHT", "HTDenom_cutHT", 500, 0., 5000. );
	histos1D_[ "puppiHTDenom_cutHT" ] = fs_->make< TH1D >( "puppiHTDenom_cutHT", "puppiHTDenom_cutHT", 500, 0., 5000. );
	histos1D_[ "prunedMassAveDenom_cutHT" ] = fs_->make< TH1D >( "prunedMassAveDenom_cutHT", "prunedMassAveDenom_cutHT", 60, 0., 600. );
	histos1D_[ "softDropMassAveDenom_cutHT" ] = fs_->make< TH1D >( "softDropMassAveDenom_cutHT", "softDropMassAveDenom_cutHT", 60, 0., 600. );
	histos1D_[ "jet1PrunedMassDenom_cutHT" ] = fs_->make< TH1D >( "jet1PrunedMassDenom_cutHT", "jet1PrunedMassDenom_cutHT", 60, 0., 600. );
	histos1D_[ "jet1SoftDropMassDenom_cutHT" ] = fs_->make< TH1D >( "jet1SoftDropMassDenom_cutHT", "jet1SoftDropMassDenom_cutHT", 60, 0., 600. );
	histos1D_[ "jet1PtDenom_cutHT" ] = fs_->make< TH1D >( "jet1PtDenom_cutHT", "jet1PtDenom_cutHT", 150, 0., 1500. );
	histos1D_[ "puppiJet1PtDenom_cutHT" ] = fs_->make< TH1D >( "puppiJet1PtDenom_cutHT", "puppiJet1PtDenom_cutHT", 150, 0., 1500. );
	histos1D_[ "jet2PrunedMassDenom_cutHT" ] = fs_->make< TH1D >( "jet2PrunedMassDenom_cutHT", "jet2PrunedMassDenom_cutHT", 60, 0., 600. );
	histos1D_[ "jet2SoftDropMassDenom_cutHT" ] = fs_->make< TH1D >( "jet2SoftDropMassDenom_cutHT", "jet2SoftDropMassDenom_cutHT", 60, 0., 600. );
	histos1D_[ "jet2PtDenom_cutHT" ] = fs_->make< TH1D >( "jet2PtDenom_cutHT", "jet2PtDenom_cutHT", 150, 0., 1500. );
	histos1D_[ "puppiJet2PtDenom_cutHT" ] = fs_->make< TH1D >( "puppiJet2PtDenom_cutHT", "puppiJet2PtDenom_cutHT", 150, 0., 1500. );

	histos2D_[ "jet1PrunedMassHTDenom_cutHT" ] = fs_->make< TH2D >( "jet1PrunedMassHTDenom_cutHT", "jet1PrunedMassHTDenom_cutHT", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet1PrunedMassjet1PtDenom_cutHT" ] = fs_->make< TH2D >( "jet1PrunedMassjet1PtDenom_cutHT", "jet1PrunedMassjet1PtDenom_cutHT", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jet1SoftDropMassHTDenom_cutHT" ] = fs_->make< TH2D >( "jet1SoftDropMassHTDenom_cutHT", "jet1SoftDropMassHTDenom_cutHT", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet1SoftDropMassjet1PtDenom_cutHT" ] = fs_->make< TH2D >( "jet1SoftDropMassjet1PtDenom_cutHT", "jet1SoftDropMassjet1PtDenom_cutHT", 60, 0., 600., 150, 0., 1500.);

	histos2D_[ "jet2PrunedMassHTDenom_cutHT" ] = fs_->make< TH2D >( "jet2PrunedMassHTDenom_cutHT", "jet2PrunedMassHTDenom_cutHT", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet2PrunedMassjet2PtDenom_cutHT" ] = fs_->make< TH2D >( "jet2PrunedMassjet2PtDenom_cutHT", "jet2PrunedMassjet2PtDenom_cutHT", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jet2SoftDropMassHTDenom_cutHT" ] = fs_->make< TH2D >( "jet2SoftDropMassHTDenom_cutHT", "jet2SoftDropMassHTDenom_cutHT", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet2SoftDropMassjet2PtDenom_cutHT" ] = fs_->make< TH2D >( "jet2SoftDropMassjet2PtDenom_cutHT", "jet2SoftDropMassjet2PtDenom_cutHT", 60, 0., 600., 150, 0., 1500.);

	histos2D_[ "prunedMassAveHTDenom_cutHT" ] = fs_->make< TH2D >( "prunedMassAveHTDenom_cutHT", "prunedMassAveHTDenom_cutHT", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "prunedMassAvejet1PtDenom_cutHT" ] = fs_->make< TH2D >( "prunedMassAvejet1PtDenom_cutHT", "prunedMassAvejet1PtDenom_cutHT", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "prunedMassAvejet2PtDenom_cutHT" ] = fs_->make< TH2D >( "prunedMassAvejet2PtDenom_cutHT", "prunedMassAvejet2PtDenom_cutHT", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "softDropMassAveHTDenom_cutHT" ] = fs_->make< TH2D >( "softDropMassAveHTDenom_cutHT", "softDropMassAveHTDenom_cutHT", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "softDropMassAvejet1PtDenom_cutHT" ] = fs_->make< TH2D >( "softDropMassAvejet1PtDenom_cutHT", "softDropMassAvejet1PtDenom_cutHT", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "softDropMassAvejet2PtDenom_cutHT" ] = fs_->make< TH2D >( "softDropMassAvejet2PtDenom_cutHT", "softDropMassAvejet2PtDenom_cutHT", 60, 0., 600., 150, 0., 1500.);
	///////////////////////////////////////////////////////////////////


	/////// Passing cutHT	
	histos1D_[ "HTPassing_cutHT" ] = fs_->make< TH1D >( "HTPassing_cutHT", "HTPassing_cutHT", 500, 0., 5000. );
	histos1D_[ "puppiHTPassing_cutHT" ] = fs_->make< TH1D >( "puppiHTPassing_cutHT", "puppiHTPassing_cutHT", 500, 0., 5000. );
	histos1D_[ "prunedMassAvePassing_cutHT" ] = fs_->make< TH1D >( "prunedMassAvePassing_cutHT", "prunedMassAvePassing_cutHT", 60, 0., 600. );
	histos1D_[ "softDropMassAvePassing_cutHT" ] = fs_->make< TH1D >( "softDropMassAvePassing_cutHT", "softDropMassAvePassing_cutHT", 60, 0., 600. );
	histos1D_[ "jet1PrunedMassPassing_cutHT" ] = fs_->make< TH1D >( "jet1PrunedMassPassing_cutHT", "jet1PrunedMassPassing_cutHT", 60, 0., 600. );
	histos1D_[ "jet1SoftDropMassPassing_cutHT" ] = fs_->make< TH1D >( "jet1SoftDropMassPassing_cutHT", "jet1SoftDropMassPassing_cutHT", 60, 0., 600. );
	histos1D_[ "jet1PtPassing_cutHT" ] = fs_->make< TH1D >( "jet1PtPassing_cutHT", "jet1PtPassing_cutHT", 150, 0., 1500. );
	histos1D_[ "puppiJet1PtPassing_cutHT" ] = fs_->make< TH1D >( "puppiJet1PtPassing_cutHT", "puppiJet1PtPassing_cutHT", 150, 0., 1500. );
	histos1D_[ "jet2PrunedMassPassing_cutHT" ] = fs_->make< TH1D >( "jet2PrunedMassPassing_cutHT", "jet2PrunedMassPassing_cutHT", 60, 0., 600. );
	histos1D_[ "jet2SoftDropMassPassing_cutHT" ] = fs_->make< TH1D >( "jet2SoftDropMassPassing_cutHT", "jet2SoftDropMassPassing_cutHT", 60, 0., 600. );
	histos1D_[ "jet2PtPassing_cutHT" ] = fs_->make< TH1D >( "jet2PtPassing_cutHT", "jet2PtPassing_cutHT", 150, 0., 1500. );
	histos1D_[ "puppiJet2PtPassing_cutHT" ] = fs_->make< TH1D >( "puppiJet2PtPassing_cutHT", "puppiJet2PtPassing_cutHT", 150, 0., 1500. );

	histos2D_[ "jet1PrunedMassHTPassing_cutHT" ] = fs_->make< TH2D >( "jet1PrunedMassHTPassing_cutHT", "jet1PrunedMassHTPassing_cutHT", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet1PrunedMassjet1PtPassing_cutHT" ] = fs_->make< TH2D >( "jet1PrunedMassjet1PtPassing_cutHT", "jet1PrunedMassjet1PtPassing_cutHT", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jet1SoftDropMassHTPassing_cutHT" ] = fs_->make< TH2D >( "jet1SoftDropMassHTPassing_cutHT", "jet1SoftDropMassHTPassing_cutHT", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet1SoftDropMassjet1PtPassing_cutHT" ] = fs_->make< TH2D >( "jet1SoftDropMassjet1PtPassing_cutHT", "jet1SoftDropMassjet1PtPassing_cutHT", 60, 0., 600., 150, 0., 1500.);

	histos2D_[ "jet2PrunedMassHTPassing_cutHT" ] = fs_->make< TH2D >( "jet2PrunedMassHTPassing_cutHT", "jet2PrunedMassHTPassing_cutHT", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet2PrunedMassjet2PtPassing_cutHT" ] = fs_->make< TH2D >( "jet2PrunedMassjet2PtPassing_cutHT", "jet2PrunedMassjet2PtPassing_cutHT", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jet2SoftDropMassHTPassing_cutHT" ] = fs_->make< TH2D >( "jet2SoftDropMassHTPassing_cutHT", "jet2SoftDropMassHTPassing_cutHT", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet2SoftDropMassjet2PtPassing_cutHT" ] = fs_->make< TH2D >( "jet2SoftDropMassjet2PtPassing_cutHT", "jet2SoftDropMassjet2PtPassing_cutHT", 60, 0., 600., 150, 0., 1500.);

	histos2D_[ "prunedMassAveHTPassing_cutHT" ] = fs_->make< TH2D >( "prunedMassAveHTPassing_cutHT", "prunedMassAveHTPassing_cutHT", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "prunedMassAvejet1PtPassing_cutHT" ] = fs_->make< TH2D >( "prunedMassAvejet1PtPassing_cutHT", "prunedMassAvejet1PtPassing_cutHT", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "prunedMassAvejet2PtPassing_cutHT" ] = fs_->make< TH2D >( "prunedMassAvejet2PtPassing_cutHT", "prunedMassAvejet2PtPassing_cutHT", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "softDropMassAveHTPassing_cutHT" ] = fs_->make< TH2D >( "softDropMassAveHTPassing_cutHT", "softDropMassAveHTPassing_cutHT", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "softDropMassAvejet1PtPassing_cutHT" ] = fs_->make< TH2D >( "softDropMassAvejet1PtPassing_cutHT", "softDropMassAvejet1PtPassing_cutHT", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "softDropMassAvejet2PtPassing_cutHT" ] = fs_->make< TH2D >( "softDropMassAvejet2PtPassing_cutHT", "softDropMassAvejet2PtPassing_cutHT", 60, 0., 600., 150, 0., 1500.);
	///////////////////////////////////////////////////////////////////


	/////// Denom cutjet1PrunedMass	
	histos1D_[ "HTDenom_cutjet1PrunedMass" ] = fs_->make< TH1D >( "HTDenom_cutjet1PrunedMass", "HTDenom_cutjet1PrunedMass", 500, 0., 5000. );
	histos1D_[ "puppiHTDenom_cutjet1PrunedMass" ] = fs_->make< TH1D >( "puppiHTDenom_cutjet1PrunedMass", "puppiHTDenom_cutjet1PrunedMass", 500, 0., 5000. );
	histos1D_[ "prunedMassAveDenom_cutjet1PrunedMass" ] = fs_->make< TH1D >( "prunedMassAveDenom_cutjet1PrunedMass", "prunedMassAveDenom_cutjet1PrunedMass", 60, 0., 600. );
	histos1D_[ "softDropMassAveDenom_cutjet1PrunedMass" ] = fs_->make< TH1D >( "softDropMassAveDenom_cutjet1PrunedMass", "softDropMassAveDenom_cutjet1PrunedMass", 60, 0., 600. );
	histos1D_[ "jet1PrunedMassDenom_cutjet1PrunedMass" ] = fs_->make< TH1D >( "jet1PrunedMassDenom_cutjet1PrunedMass", "jet1PrunedMassDenom_cutjet1PrunedMass", 60, 0., 600. );
	histos1D_[ "jet1SoftDropMassDenom_cutjet1PrunedMass" ] = fs_->make< TH1D >( "jet1SoftDropMassDenom_cutjet1PrunedMass", "jet1SoftDropMassDenom_cutjet1PrunedMass", 60, 0., 600. );
	histos1D_[ "jet1PtDenom_cutjet1PrunedMass" ] = fs_->make< TH1D >( "jet1PtDenom_cutjet1PrunedMass", "jet1PtDenom_cutjet1PrunedMass", 150, 0., 1500. );
	histos1D_[ "puppiJet1PtDenom_cutjet1PrunedMass" ] = fs_->make< TH1D >( "puppiJet1PtDenom_cutjet1PrunedMass", "puppiJet1PtDenom_cutjet1PrunedMass", 150, 0., 1500. );
	histos1D_[ "jet2PrunedMassDenom_cutjet1PrunedMass" ] = fs_->make< TH1D >( "jet2PrunedMassDenom_cutjet1PrunedMass", "jet2PrunedMassDenom_cutjet1PrunedMass", 60, 0., 600. );
	histos1D_[ "jet2SoftDropMassDenom_cutjet1PrunedMass" ] = fs_->make< TH1D >( "jet2SoftDropMassDenom_cutjet1PrunedMass", "jet2SoftDropMassDenom_cutjet1PrunedMass", 60, 0., 600. );
	histos1D_[ "jet2PtDenom_cutjet1PrunedMass" ] = fs_->make< TH1D >( "jet2PtDenom_cutjet1PrunedMass", "jet2PtDenom_cutjet1PrunedMass", 150, 0., 1500. );
	histos1D_[ "puppiJet2PtDenom_cutjet1PrunedMass" ] = fs_->make< TH1D >( "puppiJet2PtDenom_cutjet1PrunedMass", "puppiJet2PtDenom_cutjet1PrunedMass", 150, 0., 1500. );

	histos2D_[ "jet1PrunedMassHTDenom_cutjet1PrunedMass" ] = fs_->make< TH2D >( "jet1PrunedMassHTDenom_cutjet1PrunedMass", "jet1PrunedMassHTDenom_cutjet1PrunedMass", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet1PrunedMassjet1PtDenom_cutjet1PrunedMass" ] = fs_->make< TH2D >( "jet1PrunedMassjet1PtDenom_cutjet1PrunedMass", "jet1PrunedMassjet1PtDenom_cutjet1PrunedMass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jet1SoftDropMassHTDenom_cutjet1PrunedMass" ] = fs_->make< TH2D >( "jet1SoftDropMassHTDenom_cutjet1PrunedMass", "jet1SoftDropMassHTDenom_cutjet1PrunedMass", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet1SoftDropMassjet1PtDenom_cutjet1PrunedMass" ] = fs_->make< TH2D >( "jet1SoftDropMassjet1PtDenom_cutjet1PrunedMass", "jet1SoftDropMassjet1PtDenom_cutjet1PrunedMass", 60, 0., 600., 150, 0., 1500.);

	histos2D_[ "jet2PrunedMassHTDenom_cutjet1PrunedMass" ] = fs_->make< TH2D >( "jet2PrunedMassHTDenom_cutjet1PrunedMass", "jet2PrunedMassHTDenom_cutjet1PrunedMass", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet2PrunedMassjet2PtDenom_cutjet1PrunedMass" ] = fs_->make< TH2D >( "jet2PrunedMassjet2PtDenom_cutjet1PrunedMass", "jet2PrunedMassjet2PtDenom_cutjet1PrunedMass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jet2SoftDropMassHTDenom_cutjet1PrunedMass" ] = fs_->make< TH2D >( "jet2SoftDropMassHTDenom_cutjet1PrunedMass", "jet2SoftDropMassHTDenom_cutjet1PrunedMass", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet2SoftDropMassjet2PtDenom_cutjet1PrunedMass" ] = fs_->make< TH2D >( "jet2SoftDropMassjet2PtDenom_cutjet1PrunedMass", "jet2SoftDropMassjet2PtDenom_cutjet1PrunedMass", 60, 0., 600., 150, 0., 1500.);

	histos2D_[ "prunedMassAveHTDenom_cutjet1PrunedMass" ] = fs_->make< TH2D >( "prunedMassAveHTDenom_cutjet1PrunedMass", "prunedMassAveHTDenom_cutjet1PrunedMass", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "prunedMassAvejet1PtDenom_cutjet1PrunedMass" ] = fs_->make< TH2D >( "prunedMassAvejet1PtDenom_cutjet1PrunedMass", "prunedMassAvejet1PtDenom_cutjet1PrunedMass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "prunedMassAvejet2PtDenom_cutjet1PrunedMass" ] = fs_->make< TH2D >( "prunedMassAvejet2PtDenom_cutjet1PrunedMass", "prunedMassAvejet2PtDenom_cutjet1PrunedMass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "softDropMassAveHTDenom_cutjet1PrunedMass" ] = fs_->make< TH2D >( "softDropMassAveHTDenom_cutjet1PrunedMass", "softDropMassAveHTDenom_cutjet1PrunedMass", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "softDropMassAvejet1PtDenom_cutjet1PrunedMass" ] = fs_->make< TH2D >( "softDropMassAvejet1PtDenom_cutjet1PrunedMass", "softDropMassAvejet1PtDenom_cutjet1PrunedMass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "softDropMassAvejet2PtDenom_cutjet1PrunedMass" ] = fs_->make< TH2D >( "softDropMassAvejet2PtDenom_cutjet1PrunedMass", "softDropMassAvejet2PtDenom_cutjet1PrunedMass", 60, 0., 600., 150, 0., 1500.);
	///////////////////////////////////////////////////////////////////


	/////// Passing cutjet1PrunedMass	
	histos1D_[ "HTPassing_cutjet1PrunedMass" ] = fs_->make< TH1D >( "HTPassing_cutjet1PrunedMass", "HTPassing_cutjet1PrunedMass", 500, 0., 5000. );
	histos1D_[ "puppiHTPassing_cutjet1PrunedMass" ] = fs_->make< TH1D >( "puppiHTPassing_cutjet1PrunedMass", "puppiHTPassing_cutjet1PrunedMass", 500, 0., 5000. );
	histos1D_[ "prunedMassAvePassing_cutjet1PrunedMass" ] = fs_->make< TH1D >( "prunedMassAvePassing_cutjet1PrunedMass", "prunedMassAvePassing_cutjet1PrunedMass", 60, 0., 600. );
	histos1D_[ "softDropMassAvePassing_cutjet1PrunedMass" ] = fs_->make< TH1D >( "softDropMassAvePassing_cutjet1PrunedMass", "softDropMassAvePassing_cutjet1PrunedMass", 60, 0., 600. );
	histos1D_[ "jet1PrunedMassPassing_cutjet1PrunedMass" ] = fs_->make< TH1D >( "jet1PrunedMassPassing_cutjet1PrunedMass", "jet1PrunedMassPassing_cutjet1PrunedMass", 60, 0., 600. );
	histos1D_[ "jet1SoftDropMassPassing_cutjet1PrunedMass" ] = fs_->make< TH1D >( "jet1SoftDropMassPassing_cutjet1PrunedMass", "jet1SoftDropMassPassing_cutjet1PrunedMass", 60, 0., 600. );
	histos1D_[ "jet1PtPassing_cutjet1PrunedMass" ] = fs_->make< TH1D >( "jet1PtPassing_cutjet1PrunedMass", "jet1PtPassing_cutjet1PrunedMass", 150, 0., 1500. );
	histos1D_[ "puppiJet1PtPassing_cutjet1PrunedMass" ] = fs_->make< TH1D >( "puppiJet1PtPassing_cutjet1PrunedMass", "puppiJet1PtPassing_cutjet1PrunedMass", 150, 0., 1500. );
	histos1D_[ "jet2PrunedMassPassing_cutjet1PrunedMass" ] = fs_->make< TH1D >( "jet2PrunedMassPassing_cutjet1PrunedMass", "jet2PrunedMassPassing_cutjet1PrunedMass", 60, 0., 600. );
	histos1D_[ "jet2SoftDropMassPassing_cutjet1PrunedMass" ] = fs_->make< TH1D >( "jet2SoftDropMassPassing_cutjet1PrunedMass", "jet2SoftDropMassPassing_cutjet1PrunedMass", 60, 0., 600. );
	histos1D_[ "jet2PtPassing_cutjet1PrunedMass" ] = fs_->make< TH1D >( "jet2PtPassing_cutjet1PrunedMass", "jet2PtPassing_cutjet1PrunedMass", 150, 0., 1500. );
	histos1D_[ "puppiJet2PtPassing_cutjet1PrunedMass" ] = fs_->make< TH1D >( "puppiJet2PtPassing_cutjet1PrunedMass", "puppiJet2PtPassing_cutjet1PrunedMass", 150, 0., 1500. );

	histos2D_[ "jet1PrunedMassHTPassing_cutjet1PrunedMass" ] = fs_->make< TH2D >( "jet1PrunedMassHTPassing_cutjet1PrunedMass", "jet1PrunedMassHTPassing_cutjet1PrunedMass", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet1PrunedMassjet1PtPassing_cutjet1PrunedMass" ] = fs_->make< TH2D >( "jet1PrunedMassjet1PtPassing_cutjet1PrunedMass", "jet1PrunedMassjet1PtPassing_cutjet1PrunedMass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jet1SoftDropMassHTPassing_cutjet1PrunedMass" ] = fs_->make< TH2D >( "jet1SoftDropMassHTPassing_cutjet1PrunedMass", "jet1SoftDropMassHTPassing_cutjet1PrunedMass", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet1SoftDropMassjet1PtPassing_cutjet1PrunedMass" ] = fs_->make< TH2D >( "jet1SoftDropMassjet1PtPassing_cutjet1PrunedMass", "jet1SoftDropMassjet1PtPassing_cutjet1PrunedMass", 60, 0., 600., 150, 0., 1500.);

	histos2D_[ "jet2PrunedMassHTPassing_cutjet1PrunedMass" ] = fs_->make< TH2D >( "jet2PrunedMassHTPassing_cutjet1PrunedMass", "jet2PrunedMassHTPassing_cutjet1PrunedMass", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet2PrunedMassjet2PtPassing_cutjet1PrunedMass" ] = fs_->make< TH2D >( "jet2PrunedMassjet2PtPassing_cutjet1PrunedMass", "jet2PrunedMassjet2PtPassing_cutjet1PrunedMass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jet2SoftDropMassHTPassing_cutjet1PrunedMass" ] = fs_->make< TH2D >( "jet2SoftDropMassHTPassing_cutjet1PrunedMass", "jet2SoftDropMassHTPassing_cutjet1PrunedMass", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet2SoftDropMassjet2PtPassing_cutjet1PrunedMass" ] = fs_->make< TH2D >( "jet2SoftDropMassjet2PtPassing_cutjet1PrunedMass", "jet2SoftDropMassjet2PtPassing_cutjet1PrunedMass", 60, 0., 600., 150, 0., 1500.);

	histos2D_[ "prunedMassAveHTPassing_cutjet1PrunedMass" ] = fs_->make< TH2D >( "prunedMassAveHTPassing_cutjet1PrunedMass", "prunedMassAveHTPassing_cutjet1PrunedMass", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "prunedMassAvejet1PtPassing_cutjet1PrunedMass" ] = fs_->make< TH2D >( "prunedMassAvejet1PtPassing_cutjet1PrunedMass", "prunedMassAvejet1PtPassing_cutjet1PrunedMass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "prunedMassAvejet2PtPassing_cutjet1PrunedMass" ] = fs_->make< TH2D >( "prunedMassAvejet2PtPassing_cutjet1PrunedMass", "prunedMassAvejet2PtPassing_cutjet1PrunedMass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "softDropMassAveHTPassing_cutjet1PrunedMass" ] = fs_->make< TH2D >( "softDropMassAveHTPassing_cutjet1PrunedMass", "softDropMassAveHTPassing_cutjet1PrunedMass", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "softDropMassAvejet1PtPassing_cutjet1PrunedMass" ] = fs_->make< TH2D >( "softDropMassAvejet1PtPassing_cutjet1PrunedMass", "softDropMassAvejet1PtPassing_cutjet1PrunedMass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "softDropMassAvejet2PtPassing_cutjet1PrunedMass" ] = fs_->make< TH2D >( "softDropMassAvejet2PtPassing_cutjet1PrunedMass", "softDropMassAvejet2PtPassing_cutjet1PrunedMass", 60, 0., 600., 150, 0., 1500.);
	///////////////////////////////////////////////////////////////////


	/////// Denom cutjet1SoftDropMass	
	histos1D_[ "HTDenom_cutjet1SoftDropMass" ] = fs_->make< TH1D >( "HTDenom_cutjet1SoftDropMass", "HTDenom_cutjet1SoftDropMass", 500, 0., 5000. );
	histos1D_[ "puppiHTDenom_cutjet1SoftDropMass" ] = fs_->make< TH1D >( "puppiHTDenom_cutjet1SoftDropMass", "puppiHTDenom_cutjet1SoftDropMass", 500, 0., 5000. );
	histos1D_[ "prunedMassAveDenom_cutjet1SoftDropMass" ] = fs_->make< TH1D >( "prunedMassAveDenom_cutjet1SoftDropMass", "prunedMassAveDenom_cutjet1SoftDropMass", 60, 0., 600. );
	histos1D_[ "softDropMassAveDenom_cutjet1SoftDropMass" ] = fs_->make< TH1D >( "softDropMassAveDenom_cutjet1SoftDropMass", "softDropMassAveDenom_cutjet1SoftDropMass", 60, 0., 600. );
	histos1D_[ "jet1PrunedMassDenom_cutjet1SoftDropMass" ] = fs_->make< TH1D >( "jet1PrunedMassDenom_cutjet1SoftDropMass", "jet1PrunedMassDenom_cutjet1SoftDropMass", 60, 0., 600. );
	histos1D_[ "jet1SoftDropMassDenom_cutjet1SoftDropMass" ] = fs_->make< TH1D >( "jet1SoftDropMassDenom_cutjet1SoftDropMass", "jet1SoftDropMassDenom_cutjet1SoftDropMass", 60, 0., 600. );
	histos1D_[ "jet1PtDenom_cutjet1SoftDropMass" ] = fs_->make< TH1D >( "jet1PtDenom_cutjet1SoftDropMass", "jet1PtDenom_cutjet1SoftDropMass", 150, 0., 1500. );
	histos1D_[ "puppiJet1PtDenom_cutjet1SoftDropMass" ] = fs_->make< TH1D >( "puppiJet1PtDenom_cutjet1SoftDropMass", "puppiJet1PtDenom_cutjet1SoftDropMass", 150, 0., 1500. );
	histos1D_[ "jet2PrunedMassDenom_cutjet1SoftDropMass" ] = fs_->make< TH1D >( "jet2PrunedMassDenom_cutjet1SoftDropMass", "jet2PrunedMassDenom_cutjet1SoftDropMass", 60, 0., 600. );
	histos1D_[ "jet2SoftDropMassDenom_cutjet1SoftDropMass" ] = fs_->make< TH1D >( "jet2SoftDropMassDenom_cutjet1SoftDropMass", "jet2SoftDropMassDenom_cutjet1SoftDropMass", 60, 0., 600. );
	histos1D_[ "jet2PtDenom_cutjet1SoftDropMass" ] = fs_->make< TH1D >( "jet2PtDenom_cutjet1SoftDropMass", "jet2PtDenom_cutjet1SoftDropMass", 150, 0., 1500. );
	histos1D_[ "puppiJet2PtDenom_cutjet1SoftDropMass" ] = fs_->make< TH1D >( "puppiJet2PtDenom_cutjet1SoftDropMass", "puppiJet2PtDenom_cutjet1SoftDropMass", 150, 0., 1500. );

	histos2D_[ "jet1PrunedMassHTDenom_cutjet1SoftDropMass" ] = fs_->make< TH2D >( "jet1PrunedMassHTDenom_cutjet1SoftDropMass", "jet1PrunedMassHTDenom_cutjet1SoftDropMass", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet1PrunedMassjet1PtDenom_cutjet1SoftDropMass" ] = fs_->make< TH2D >( "jet1PrunedMassjet1PtDenom_cutjet1SoftDropMass", "jet1PrunedMassjet1PtDenom_cutjet1SoftDropMass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jet1SoftDropMassHTDenom_cutjet1SoftDropMass" ] = fs_->make< TH2D >( "jet1SoftDropMassHTDenom_cutjet1SoftDropMass", "jet1SoftDropMassHTDenom_cutjet1SoftDropMass", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet1SoftDropMassjet1PtDenom_cutjet1SoftDropMass" ] = fs_->make< TH2D >( "jet1SoftDropMassjet1PtDenom_cutjet1SoftDropMass", "jet1SoftDropMassjet1PtDenom_cutjet1SoftDropMass", 60, 0., 600., 150, 0., 1500.);

	histos2D_[ "jet2PrunedMassHTDenom_cutjet1SoftDropMass" ] = fs_->make< TH2D >( "jet2PrunedMassHTDenom_cutjet1SoftDropMass", "jet2PrunedMassHTDenom_cutjet1SoftDropMass", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet2PrunedMassjet2PtDenom_cutjet1SoftDropMass" ] = fs_->make< TH2D >( "jet2PrunedMassjet2PtDenom_cutjet1SoftDropMass", "jet2PrunedMassjet2PtDenom_cutjet1SoftDropMass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jet2SoftDropMassHTDenom_cutjet1SoftDropMass" ] = fs_->make< TH2D >( "jet2SoftDropMassHTDenom_cutjet1SoftDropMass", "jet2SoftDropMassHTDenom_cutjet1SoftDropMass", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet2SoftDropMassjet2PtDenom_cutjet1SoftDropMass" ] = fs_->make< TH2D >( "jet2SoftDropMassjet2PtDenom_cutjet1SoftDropMass", "jet2SoftDropMassjet2PtDenom_cutjet1SoftDropMass", 60, 0., 600., 150, 0., 1500.);

	histos2D_[ "prunedMassAveHTDenom_cutjet1SoftDropMass" ] = fs_->make< TH2D >( "prunedMassAveHTDenom_cutjet1SoftDropMass", "prunedMassAveHTDenom_cutjet1SoftDropMass", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "prunedMassAvejet1PtDenom_cutjet1SoftDropMass" ] = fs_->make< TH2D >( "prunedMassAvejet1PtDenom_cutjet1SoftDropMass", "prunedMassAvejet1PtDenom_cutjet1SoftDropMass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "prunedMassAvejet2PtDenom_cutjet1SoftDropMass" ] = fs_->make< TH2D >( "prunedMassAvejet2PtDenom_cutjet1SoftDropMass", "prunedMassAvejet2PtDenom_cutjet1SoftDropMass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "softDropMassAveHTDenom_cutjet1SoftDropMass" ] = fs_->make< TH2D >( "softDropMassAveHTDenom_cutjet1SoftDropMass", "softDropMassAveHTDenom_cutjet1SoftDropMass", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "softDropMassAvejet1PtDenom_cutjet1SoftDropMass" ] = fs_->make< TH2D >( "softDropMassAvejet1PtDenom_cutjet1SoftDropMass", "softDropMassAvejet1PtDenom_cutjet1SoftDropMass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "softDropMassAvejet2PtDenom_cutjet1SoftDropMass" ] = fs_->make< TH2D >( "softDropMassAvejet2PtDenom_cutjet1SoftDropMass", "softDropMassAvejet2PtDenom_cutjet1SoftDropMass", 60, 0., 600., 150, 0., 1500.);
	///////////////////////////////////////////////////////////////////


	/////// Passing cutjet1SoftDropMass	
	histos1D_[ "HTPassing_cutjet1SoftDropMass" ] = fs_->make< TH1D >( "HTPassing_cutjet1SoftDropMass", "HTPassing_cutjet1SoftDropMass", 500, 0., 5000. );
	histos1D_[ "puppiHTPassing_cutjet1SoftDropMass" ] = fs_->make< TH1D >( "puppiHTPassing_cutjet1SoftDropMass", "puppiHTPassing_cutjet1SoftDropMass", 500, 0., 5000. );
	histos1D_[ "prunedMassAvePassing_cutjet1SoftDropMass" ] = fs_->make< TH1D >( "prunedMassAvePassing_cutjet1SoftDropMass", "prunedMassAvePassing_cutjet1SoftDropMass", 60, 0., 600. );
	histos1D_[ "softDropMassAvePassing_cutjet1SoftDropMass" ] = fs_->make< TH1D >( "softDropMassAvePassing_cutjet1SoftDropMass", "softDropMassAvePassing_cutjet1SoftDropMass", 60, 0., 600. );
	histos1D_[ "jet1PrunedMassPassing_cutjet1SoftDropMass" ] = fs_->make< TH1D >( "jet1PrunedMassPassing_cutjet1SoftDropMass", "jet1PrunedMassPassing_cutjet1SoftDropMass", 60, 0., 600. );
	histos1D_[ "jet1SoftDropMassPassing_cutjet1SoftDropMass" ] = fs_->make< TH1D >( "jet1SoftDropMassPassing_cutjet1SoftDropMass", "jet1SoftDropMassPassing_cutjet1SoftDropMass", 60, 0., 600. );
	histos1D_[ "jet1PtPassing_cutjet1SoftDropMass" ] = fs_->make< TH1D >( "jet1PtPassing_cutjet1SoftDropMass", "jet1PtPassing_cutjet1SoftDropMass", 150, 0., 1500. );
	histos1D_[ "puppiJet1PtPassing_cutjet1SoftDropMass" ] = fs_->make< TH1D >( "puppiJet1PtPassing_cutjet1SoftDropMass", "puppiJet1PtPassing_cutjet1SoftDropMass", 150, 0., 1500. );
	histos1D_[ "jet2PrunedMassPassing_cutjet1SoftDropMass" ] = fs_->make< TH1D >( "jet2PrunedMassPassing_cutjet1SoftDropMass", "jet2PrunedMassPassing_cutjet1SoftDropMass", 60, 0., 600. );
	histos1D_[ "jet2SoftDropMassPassing_cutjet1SoftDropMass" ] = fs_->make< TH1D >( "jet2SoftDropMassPassing_cutjet1SoftDropMass", "jet2SoftDropMassPassing_cutjet1SoftDropMass", 60, 0., 600. );
	histos1D_[ "jet2PtPassing_cutjet1SoftDropMass" ] = fs_->make< TH1D >( "jet2PtPassing_cutjet1SoftDropMass", "jet2PtPassing_cutjet1SoftDropMass", 150, 0., 1500. );
	histos1D_[ "puppiJet2PtPassing_cutjet1SoftDropMass" ] = fs_->make< TH1D >( "puppiJet2PtPassing_cutjet1SoftDropMass", "puppiJet2PtPassing_cutjet1SoftDropMass", 150, 0., 1500. );

	histos2D_[ "jet1PrunedMassHTPassing_cutjet1SoftDropMass" ] = fs_->make< TH2D >( "jet1PrunedMassHTPassing_cutjet1SoftDropMass", "jet1PrunedMassHTPassing_cutjet1SoftDropMass", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet1PrunedMassjet1PtPassing_cutjet1SoftDropMass" ] = fs_->make< TH2D >( "jet1PrunedMassjet1PtPassing_cutjet1SoftDropMass", "jet1PrunedMassjet1PtPassing_cutjet1SoftDropMass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jet1SoftDropMassHTPassing_cutjet1SoftDropMass" ] = fs_->make< TH2D >( "jet1SoftDropMassHTPassing_cutjet1SoftDropMass", "jet1SoftDropMassHTPassing_cutjet1SoftDropMass", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet1SoftDropMassjet1PtPassing_cutjet1SoftDropMass" ] = fs_->make< TH2D >( "jet1SoftDropMassjet1PtPassing_cutjet1SoftDropMass", "jet1SoftDropMassjet1PtPassing_cutjet1SoftDropMass", 60, 0., 600., 150, 0., 1500.);

	histos2D_[ "jet2PrunedMassHTPassing_cutjet1SoftDropMass" ] = fs_->make< TH2D >( "jet2PrunedMassHTPassing_cutjet1SoftDropMass", "jet2PrunedMassHTPassing_cutjet1SoftDropMass", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet2PrunedMassjet2PtPassing_cutjet1SoftDropMass" ] = fs_->make< TH2D >( "jet2PrunedMassjet2PtPassing_cutjet1SoftDropMass", "jet2PrunedMassjet2PtPassing_cutjet1SoftDropMass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jet2SoftDropMassHTPassing_cutjet1SoftDropMass" ] = fs_->make< TH2D >( "jet2SoftDropMassHTPassing_cutjet1SoftDropMass", "jet2SoftDropMassHTPassing_cutjet1SoftDropMass", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet2SoftDropMassjet2PtPassing_cutjet1SoftDropMass" ] = fs_->make< TH2D >( "jet2SoftDropMassjet2PtPassing_cutjet1SoftDropMass", "jet2SoftDropMassjet2PtPassing_cutjet1SoftDropMass", 60, 0., 600., 150, 0., 1500.);

	histos2D_[ "prunedMassAveHTPassing_cutjet1SoftDropMass" ] = fs_->make< TH2D >( "prunedMassAveHTPassing_cutjet1SoftDropMass", "prunedMassAveHTPassing_cutjet1SoftDropMass", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "prunedMassAvejet1PtPassing_cutjet1SoftDropMass" ] = fs_->make< TH2D >( "prunedMassAvejet1PtPassing_cutjet1SoftDropMass", "prunedMassAvejet1PtPassing_cutjet1SoftDropMass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "prunedMassAvejet2PtPassing_cutjet1SoftDropMass" ] = fs_->make< TH2D >( "prunedMassAvejet2PtPassing_cutjet1SoftDropMass", "prunedMassAvejet2PtPassing_cutjet1SoftDropMass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "softDropMassAveHTPassing_cutjet1SoftDropMass" ] = fs_->make< TH2D >( "softDropMassAveHTPassing_cutjet1SoftDropMass", "softDropMassAveHTPassing_cutjet1SoftDropMass", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "softDropMassAvejet1PtPassing_cutjet1SoftDropMass" ] = fs_->make< TH2D >( "softDropMassAvejet1PtPassing_cutjet1SoftDropMass", "softDropMassAvejet1PtPassing_cutjet1SoftDropMass", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "softDropMassAvejet2PtPassing_cutjet1SoftDropMass" ] = fs_->make< TH2D >( "softDropMassAvejet2PtPassing_cutjet1SoftDropMass", "softDropMassAvejet2PtPassing_cutjet1SoftDropMass", 60, 0., 600., 150, 0., 1500.);
	///////////////////////////////////////////////////////////////////



	/////// Denom cut2jetsPt	
	histos1D_[ "HTDenom_cut2jetsPt" ] = fs_->make< TH1D >( "HTDenom_cut2jetsPt", "HTDenom_cut2jetsPt", 500, 0., 5000. );
	histos1D_[ "puppiHTDenom_cut2jetsPt" ] = fs_->make< TH1D >( "puppiHTDenom_cut2jetsPt", "puppiHTDenom_cut2jetsPt", 500, 0., 5000. );
	histos1D_[ "prunedMassAveDenom_cut2jetsPt" ] = fs_->make< TH1D >( "prunedMassAveDenom_cut2jetsPt", "prunedMassAveDenom_cut2jetsPt", 60, 0., 600. );
	histos1D_[ "softDropMassAveDenom_cut2jetsPt" ] = fs_->make< TH1D >( "softDropMassAveDenom_cut2jetsPt", "softDropMassAveDenom_cut2jetsPt", 60, 0., 600. );
	histos1D_[ "jet1PrunedMassDenom_cut2jetsPt" ] = fs_->make< TH1D >( "jet1PrunedMassDenom_cut2jetsPt", "jet1PrunedMassDenom_cut2jetsPt", 60, 0., 600. );
	histos1D_[ "jet1SoftDropMassDenom_cut2jetsPt" ] = fs_->make< TH1D >( "jet1SoftDropMassDenom_cut2jetsPt", "jet1SoftDropMassDenom_cut2jetsPt", 60, 0., 600. );
	histos1D_[ "jet1PtDenom_cut2jetsPt" ] = fs_->make< TH1D >( "jet1PtDenom_cut2jetsPt", "jet1PtDenom_cut2jetsPt", 150, 0., 1500. );
	histos1D_[ "puppiJet1PtDenom_cut2jetsPt" ] = fs_->make< TH1D >( "puppiJet1PtDenom_cut2jetsPt", "puppiJet1PtDenom_cut2jetsPt", 150, 0., 1500. );
	histos1D_[ "jet2PrunedMassDenom_cut2jetsPt" ] = fs_->make< TH1D >( "jet2PrunedMassDenom_cut2jetsPt", "jet2PrunedMassDenom_cut2jetsPt", 60, 0., 600. );
	histos1D_[ "jet2SoftDropMassDenom_cut2jetsPt" ] = fs_->make< TH1D >( "jet2SoftDropMassDenom_cut2jetsPt", "jet2SoftDropMassDenom_cut2jetsPt", 60, 0., 600. );
	histos1D_[ "jet2PtDenom_cut2jetsPt" ] = fs_->make< TH1D >( "jet2PtDenom_cut2jetsPt", "jet2PtDenom_cut2jetsPt", 150, 0., 1500. );
	histos1D_[ "puppiJet2PtDenom_cut2jetsPt" ] = fs_->make< TH1D >( "puppiJet2PtDenom_cut2jetsPt", "puppiJet2PtDenom_cut2jetsPt", 150, 0., 1500. );

	histos2D_[ "jet1PrunedMassHTDenom_cut2jetsPt" ] = fs_->make< TH2D >( "jet1PrunedMassHTDenom_cut2jetsPt", "jet1PrunedMassHTDenom_cut2jetsPt", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet1PrunedMassjet1PtDenom_cut2jetsPt" ] = fs_->make< TH2D >( "jet1PrunedMassjet1PtDenom_cut2jetsPt", "jet1PrunedMassjet1PtDenom_cut2jetsPt", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jet1SoftDropMassHTDenom_cut2jetsPt" ] = fs_->make< TH2D >( "jet1SoftDropMassHTDenom_cut2jetsPt", "jet1SoftDropMassHTDenom_cut2jetsPt", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet1SoftDropMassjet1PtDenom_cut2jetsPt" ] = fs_->make< TH2D >( "jet1SoftDropMassjet1PtDenom_cut2jetsPt", "jet1SoftDropMassjet1PtDenom_cut2jetsPt", 60, 0., 600., 150, 0., 1500.);

	histos2D_[ "jet2PrunedMassHTDenom_cut2jetsPt" ] = fs_->make< TH2D >( "jet2PrunedMassHTDenom_cut2jetsPt", "jet2PrunedMassHTDenom_cut2jetsPt", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet2PrunedMassjet2PtDenom_cut2jetsPt" ] = fs_->make< TH2D >( "jet2PrunedMassjet2PtDenom_cut2jetsPt", "jet2PrunedMassjet2PtDenom_cut2jetsPt", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jet2SoftDropMassHTDenom_cut2jetsPt" ] = fs_->make< TH2D >( "jet2SoftDropMassHTDenom_cut2jetsPt", "jet2SoftDropMassHTDenom_cut2jetsPt", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet2SoftDropMassjet2PtDenom_cut2jetsPt" ] = fs_->make< TH2D >( "jet2SoftDropMassjet2PtDenom_cut2jetsPt", "jet2SoftDropMassjet2PtDenom_cut2jetsPt", 60, 0., 600., 150, 0., 1500.);

	histos2D_[ "prunedMassAveHTDenom_cut2jetsPt" ] = fs_->make< TH2D >( "prunedMassAveHTDenom_cut2jetsPt", "prunedMassAveHTDenom_cut2jetsPt", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "prunedMassAvejet1PtDenom_cut2jetsPt" ] = fs_->make< TH2D >( "prunedMassAvejet1PtDenom_cut2jetsPt", "prunedMassAvejet1PtDenom_cut2jetsPt", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "prunedMassAvejet2PtDenom_cut2jetsPt" ] = fs_->make< TH2D >( "prunedMassAvejet2PtDenom_cut2jetsPt", "prunedMassAvejet2PtDenom_cut2jetsPt", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "softDropMassAveHTDenom_cut2jetsPt" ] = fs_->make< TH2D >( "softDropMassAveHTDenom_cut2jetsPt", "softDropMassAveHTDenom_cut2jetsPt", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "softDropMassAvejet1PtDenom_cut2jetsPt" ] = fs_->make< TH2D >( "softDropMassAvejet1PtDenom_cut2jetsPt", "softDropMassAvejet1PtDenom_cut2jetsPt", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "softDropMassAvejet2PtDenom_cut2jetsPt" ] = fs_->make< TH2D >( "softDropMassAvejet2PtDenom_cut2jetsPt", "softDropMassAvejet2PtDenom_cut2jetsPt", 60, 0., 600., 150, 0., 1500.);
	///////////////////////////////////////////////////////////////////


	/////// Passing cut2jetsPt	
	histos1D_[ "HTPassing_cut2jetsPt" ] = fs_->make< TH1D >( "HTPassing_cut2jetsPt", "HTPassing_cut2jetsPt", 500, 0., 5000. );
	histos1D_[ "puppiHTPassing_cut2jetsPt" ] = fs_->make< TH1D >( "puppiHTPassing_cut2jetsPt", "puppiHTPassing_cut2jetsPt", 500, 0., 5000. );
	histos1D_[ "prunedMassAvePassing_cut2jetsPt" ] = fs_->make< TH1D >( "prunedMassAvePassing_cut2jetsPt", "prunedMassAvePassing_cut2jetsPt", 60, 0., 600. );
	histos1D_[ "softDropMassAvePassing_cut2jetsPt" ] = fs_->make< TH1D >( "softDropMassAvePassing_cut2jetsPt", "softDropMassAvePassing_cut2jetsPt", 60, 0., 600. );
	histos1D_[ "jet1PrunedMassPassing_cut2jetsPt" ] = fs_->make< TH1D >( "jet1PrunedMassPassing_cut2jetsPt", "jet1PrunedMassPassing_cut2jetsPt", 60, 0., 600. );
	histos1D_[ "jet1SoftDropMassPassing_cut2jetsPt" ] = fs_->make< TH1D >( "jet1SoftDropMassPassing_cut2jetsPt", "jet1SoftDropMassPassing_cut2jetsPt", 60, 0., 600. );
	histos1D_[ "jet1PtPassing_cut2jetsPt" ] = fs_->make< TH1D >( "jet1PtPassing_cut2jetsPt", "jet1PtPassing_cut2jetsPt", 150, 0., 1500. );
	histos1D_[ "puppiJet1PtPassing_cut2jetsPt" ] = fs_->make< TH1D >( "puppiJet1PtPassing_cut2jetsPt", "puppiJet1PtPassing_cut2jetsPt", 150, 0., 1500. );
	histos1D_[ "jet2PrunedMassPassing_cut2jetsPt" ] = fs_->make< TH1D >( "jet2PrunedMassPassing_cut2jetsPt", "jet2PrunedMassPassing_cut2jetsPt", 60, 0., 600. );
	histos1D_[ "jet2SoftDropMassPassing_cut2jetsPt" ] = fs_->make< TH1D >( "jet2SoftDropMassPassing_cut2jetsPt", "jet2SoftDropMassPassing_cut2jetsPt", 60, 0., 600. );
	histos1D_[ "jet2PtPassing_cut2jetsPt" ] = fs_->make< TH1D >( "jet2PtPassing_cut2jetsPt", "jet2PtPassing_cut2jetsPt", 150, 0., 1500. );
	histos1D_[ "puppiJet2PtPassing_cut2jetsPt" ] = fs_->make< TH1D >( "puppiJet2PtPassing_cut2jetsPt", "puppiJet2PtPassing_cut2jetsPt", 150, 0., 1500. );

	histos2D_[ "jet1PrunedMassHTPassing_cut2jetsPt" ] = fs_->make< TH2D >( "jet1PrunedMassHTPassing_cut2jetsPt", "jet1PrunedMassHTPassing_cut2jetsPt", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet1PrunedMassjet1PtPassing_cut2jetsPt" ] = fs_->make< TH2D >( "jet1PrunedMassjet1PtPassing_cut2jetsPt", "jet1PrunedMassjet1PtPassing_cut2jetsPt", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jet1SoftDropMassHTPassing_cut2jetsPt" ] = fs_->make< TH2D >( "jet1SoftDropMassHTPassing_cut2jetsPt", "jet1SoftDropMassHTPassing_cut2jetsPt", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet1SoftDropMassjet1PtPassing_cut2jetsPt" ] = fs_->make< TH2D >( "jet1SoftDropMassjet1PtPassing_cut2jetsPt", "jet1SoftDropMassjet1PtPassing_cut2jetsPt", 60, 0., 600., 150, 0., 1500.);

	histos2D_[ "jet2PrunedMassHTPassing_cut2jetsPt" ] = fs_->make< TH2D >( "jet2PrunedMassHTPassing_cut2jetsPt", "jet2PrunedMassHTPassing_cut2jetsPt", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet2PrunedMassjet2PtPassing_cut2jetsPt" ] = fs_->make< TH2D >( "jet2PrunedMassjet2PtPassing_cut2jetsPt", "jet2PrunedMassjet2PtPassing_cut2jetsPt", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "jet2SoftDropMassHTPassing_cut2jetsPt" ] = fs_->make< TH2D >( "jet2SoftDropMassHTPassing_cut2jetsPt", "jet2SoftDropMassHTPassing_cut2jetsPt", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "jet2SoftDropMassjet2PtPassing_cut2jetsPt" ] = fs_->make< TH2D >( "jet2SoftDropMassjet2PtPassing_cut2jetsPt", "jet2SoftDropMassjet2PtPassing_cut2jetsPt", 60, 0., 600., 150, 0., 1500.);

	histos2D_[ "prunedMassAveHTPassing_cut2jetsPt" ] = fs_->make< TH2D >( "prunedMassAveHTPassing_cut2jetsPt", "prunedMassAveHTPassing_cut2jetsPt", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "prunedMassAvejet1PtPassing_cut2jetsPt" ] = fs_->make< TH2D >( "prunedMassAvejet1PtPassing_cut2jetsPt", "prunedMassAvejet1PtPassing_cut2jetsPt", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "prunedMassAvejet2PtPassing_cut2jetsPt" ] = fs_->make< TH2D >( "prunedMassAvejet2PtPassing_cut2jetsPt", "prunedMassAvejet2PtPassing_cut2jetsPt", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "softDropMassAveHTPassing_cut2jetsPt" ] = fs_->make< TH2D >( "softDropMassAveHTPassing_cut2jetsPt", "softDropMassAveHTPassing_cut2jetsPt", 60, 0., 600., 500, 0., 5000.);
	histos2D_[ "softDropMassAvejet1PtPassing_cut2jetsPt" ] = fs_->make< TH2D >( "softDropMassAvejet1PtPassing_cut2jetsPt", "softDropMassAvejet1PtPassing_cut2jetsPt", 60, 0., 600., 150, 0., 1500.);
	histos2D_[ "softDropMassAvejet2PtPassing_cut2jetsPt" ] = fs_->make< TH2D >( "softDropMassAvejet2PtPassing_cut2jetsPt", "softDropMassAvejet2PtPassing_cut2jetsPt", 60, 0., 600., 150, 0., 1500.);
	///////////////////////////////////////////////////////////////////
	
	///// Sumw2 all the histos
	for( auto const& histo : histos1D_ ) histos1D_[ histo.first ]->Sumw2();
	for( auto const& histo : histos2D_ ) histos2D_[ histo.first ]->Sumw2();



}

// ------------ method called once each job just after ending the event loop  ------------
void RUNBoostedMiniAODTriggerEfficiency::endJob() {

}

void RUNBoostedMiniAODTriggerEfficiency::fillDescriptions(edm::ConfigurationDescriptions & descriptions) {

	edm::ParameterSetDescription desc;

	desc.add<double>("cutAK8jetPt", 150.);
	desc.add<double>("cutAK8HT", 900.);
	desc.add<double>("cutAK8jet1Pt", 500.);
	desc.add<double>("cutAK8jet2Pt", 450.);
	desc.add<double>("cutAK8jet1Mass", 60.);
	desc.add<string>("baseTrigger", "HLT_PFHT475");
	desc.add<InputTag>("bits", 	InputTag("TriggerResults", "", "HLT"));
	desc.add<InputTag>("prescales", 	InputTag("patTrigger"));
	desc.add<InputTag>("hltTrigger", 	InputTag("hltTriggerSummaryAOD","","HLT"));
	desc.add<InputTag>("recoJets", 	InputTag("slimmedJetsAK8"));
	vector<string> HLTPass;
	HLTPass.push_back("HLT_AK8PFHT700_TrimR0p1PT0p03Mass50");
	desc.add<vector<string>>("triggerPass",	HLTPass);

	descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(RUNBoostedMiniAODTriggerEfficiency);
