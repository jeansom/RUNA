// -*- C++ -*-
//
// Package:    RUNA/RUNTriggerEfficiency
// Class:      RUNResolvedMiniAODTriggerEfficiency
// Original Author:  Alejandro Gomez Espinosa
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
class RUNResolvedMiniAODTriggerEfficiency : public EDAnalyzer {
	public:
		explicit RUNResolvedMiniAODTriggerEfficiency(const ParameterSet&);
		static void fillDescriptions(edm::ConfigurationDescriptions & descriptions);
		~RUNResolvedMiniAODTriggerEfficiency();

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

		TString baseTrigger;
		double cutAK4jetPt;
		double cutAK4jet4Pt;
		double cutAK4HT;
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
RUNResolvedMiniAODTriggerEfficiency::RUNResolvedMiniAODTriggerEfficiency(const ParameterSet& iConfig):
	triggerBits_(consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("bits"))),
	triggerPrescales_(consumes<pat::PackedTriggerPrescales>(iConfig.getParameter<edm::InputTag>("prescales"))),
	triggerEvent_(consumes<trigger::TriggerEvent>(iConfig.getParameter<edm::InputTag>("hltTrigger"))),
	jetToken_(consumes<pat::JetCollection>(iConfig.getParameter<edm::InputTag>("recoJets")))
{
	baseTrigger = iConfig.getParameter<string>("baseTrigger");
	cutAK4jetPt = iConfig.getParameter<double>("cutAK4jetPt");
	cutAK4jet4Pt = iConfig.getParameter<double>("cutAK4jet4Pt");
	cutAK4HT = iConfig.getParameter<double>("cutAK4HT");
	triggerPass = iConfig.getParameter<vector<string>>("triggerPass");
}


RUNResolvedMiniAODTriggerEfficiency::~RUNResolvedMiniAODTriggerEfficiency()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void RUNResolvedMiniAODTriggerEfficiency::analyze(const Event& iEvent, const EventSetup& iSetup) {

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
	float HT = 0;

	for (const pat::Jet &jet : *jets) {
		
		if ( TMath::Abs( jet.eta() ) > 2.4 ) continue;
		string typeOfJetID = "looseJetID";	// check trigger with looser jet id
		bool idL = jetID( jet.eta(), jet.energy(), jet.jecFactor(0), jet.neutralHadronEnergyFraction(), jet.neutralEmEnergyFraction(), jet.chargedHadronEnergyFraction(), jet.muonEnergy(), jet.chargedEmEnergyFraction(), jet.chargedMultiplicity(), jet.neutralMultiplicity(), typeOfJetID ); 

		if( ( jet.pt() > cutAK4jetPt ) && idL ) { 
			HT += jet.pt();
			JETS.push_back( jet );
		}
	}


	if ( JETS.size() > 3 ) {

		if ( basedTriggerFired ) {
			histos1D_[ "jet1PtDenom_cut4Jet" ]->Fill( JETS[0].pt() );
			histos1D_[ "jet2PtDenom_cut4Jet" ]->Fill( JETS[1].pt() );
			histos1D_[ "jet3PtDenom_cut4Jet" ]->Fill( JETS[2].pt() );
			histos1D_[ "jet4PtDenom_cut4Jet" ]->Fill( JETS[3].pt() );
			histos1D_[ "HTDenom_cut4Jet" ]->Fill( HT  );
			histos2D_[ "jet4PtHTDenom_cut4Jet" ]->Fill( JETS[3].pt(), HT );

			if ( ORTriggers ){
				histos1D_[ "jet1PtPassing_cut4Jet" ]->Fill( JETS[0].pt() );
				histos1D_[ "jet2PtPassing_cut4Jet" ]->Fill( JETS[1].pt() );
				histos1D_[ "jet3PtPassing_cut4Jet" ]->Fill( JETS[2].pt() );
				histos1D_[ "jet4PtPassing_cut4Jet" ]->Fill( JETS[3].pt() );
				histos1D_[ "HTPassing_cut4Jet" ]->Fill( HT  );
				histos2D_[ "jet4PtHTPassing_cut4Jet" ]->Fill( JETS[3].pt(), HT );
			}

			if ( JETS[3].pt() > cutAK4jet4Pt ) {
				histos1D_[ "jet1PtDenom_cutJet4Pt" ]->Fill( JETS[0].pt() );
				histos1D_[ "jet2PtDenom_cutJet4Pt" ]->Fill( JETS[1].pt() );
				histos1D_[ "jet3PtDenom_cutJet4Pt" ]->Fill( JETS[2].pt() );
				histos1D_[ "jet4PtDenom_cutJet4Pt" ]->Fill( JETS[3].pt() );
				histos1D_[ "HTDenom_cutJet4Pt" ]->Fill( HT  );
				histos2D_[ "jet4PtHTDenom_cutJet4Pt" ]->Fill( JETS[3].pt(), HT );

				if ( ORTriggers ){
					histos1D_[ "jet1PtPassing_cutJet4Pt" ]->Fill( JETS[0].pt() );
					histos1D_[ "jet2PtPassing_cutJet4Pt" ]->Fill( JETS[1].pt() );
					histos1D_[ "jet3PtPassing_cutJet4Pt" ]->Fill( JETS[2].pt() );
					histos1D_[ "jet4PtPassing_cutJet4Pt" ]->Fill( JETS[3].pt() );
					histos1D_[ "HTPassing_cutJet4Pt" ]->Fill( HT  );
					histos2D_[ "jet4PtHTPassing_cutJet4Pt" ]->Fill( JETS[3].pt(), HT );
				}
			}

			if ( HT > cutAK4HT ) {
				histos1D_[ "jet1PtDenom_cutHT" ]->Fill( JETS[0].pt() );
				histos1D_[ "jet2PtDenom_cutHT" ]->Fill( JETS[1].pt() );
				histos1D_[ "jet3PtDenom_cutHT" ]->Fill( JETS[2].pt() );
				histos1D_[ "jet4PtDenom_cutHT" ]->Fill( JETS[3].pt() );
				histos1D_[ "HTDenom_cutHT" ]->Fill( HT  );
				histos2D_[ "jet4PtHTDenom_cutHT" ]->Fill( JETS[3].pt(), HT );

				if ( ORTriggers ){
					histos1D_[ "jet1PtPassing_cutHT" ]->Fill( JETS[0].pt() );
					histos1D_[ "jet2PtPassing_cutHT" ]->Fill( JETS[1].pt() );
					histos1D_[ "jet3PtPassing_cutHT" ]->Fill( JETS[2].pt() );
					histos1D_[ "jet4PtPassing_cutHT" ]->Fill( JETS[3].pt() );
					histos1D_[ "HTPassing_cutHT" ]->Fill( HT  );
					histos2D_[ "jet4PtHTPassing_cutHT" ]->Fill( JETS[3].pt(), HT );
				}
			}
		}
	}
	JETS.clear();

}


// ------------ method called once each job just before starting event loop  ------------
void RUNResolvedMiniAODTriggerEfficiency::beginJob() {

	histos1D_[ "HTDenom_cut4Jet" ] = fs_->make< TH1D >( "HTDenom_cut4Jet", "HTDenom_cut4Jet", 500, 0., 5000. );
	histos1D_[ "HTDenom_cut4Jet" ]->Sumw2();
	histos1D_[ "HTPassing_cut4Jet" ] = fs_->make< TH1D >( "HTPassing_cut4Jet", "HTPassing_cut4Jet", 500, 0., 5000. );
	histos1D_[ "HTPassing_cut4Jet" ]->Sumw2();

	histos1D_[ "jet1PtDenom_cut4Jet" ] = fs_->make< TH1D >( "jet1PtDenom_cut4Jet", "jet1PtDenom_cut4Jet", 150, 0., 1500. );
	histos1D_[ "jet1PtDenom_cut4Jet" ]->Sumw2();
	histos1D_[ "jet1PtPassing_cut4Jet" ] = fs_->make< TH1D >( "jet1PtPassing_cut4Jet", "jet1PtPassing_cut4Jet", 150, 0., 1500. );
	histos1D_[ "jet1PtPassing_cut4Jet" ]->Sumw2();

	histos1D_[ "jet2PtDenom_cut4Jet" ] = fs_->make< TH1D >( "jet2PtDenom_cut4Jet", "jet2PtDenom_cut4Jet", 150, 0., 1500. );
	histos1D_[ "jet2PtDenom_cut4Jet" ]->Sumw2();
	histos1D_[ "jet2PtPassing_cut4Jet" ] = fs_->make< TH1D >( "jet2PtPassing_cut4Jet", "jet2PtPassing_cut4Jet", 150, 0., 1500. );
	histos1D_[ "jet2PtPassing_cut4Jet" ]->Sumw2();

	histos1D_[ "jet3PtDenom_cut4Jet" ] = fs_->make< TH1D >( "jet3PtDenom_cut4Jet", "jet3PtDenom_cut4Jet", 150, 0., 1500. );
	histos1D_[ "jet3PtDenom_cut4Jet" ]->Sumw2();
	histos1D_[ "jet3PtPassing_cut4Jet" ] = fs_->make< TH1D >( "jet3PtPassing_cut4Jet", "jet3PtPassing_cut4Jet", 150, 0., 1500. );
	histos1D_[ "jet3PtPassing_cut4Jet" ]->Sumw2();

	histos1D_[ "jet4PtDenom_cut4Jet" ] = fs_->make< TH1D >( "jet4PtDenom_cut4Jet", "jet4PtDenom_cut4Jet", 150, 0., 1500. );
	histos1D_[ "jet4PtDenom_cut4Jet" ]->Sumw2();
	histos1D_[ "jet4PtPassing_cut4Jet" ] = fs_->make< TH1D >( "jet4PtPassing_cut4Jet", "jet4PtPassing_cut4Jet", 150, 0., 1500. );
	histos1D_[ "jet4PtPassing_cut4Jet" ]->Sumw2();

	histos2D_[ "jet4PtHTDenom_cut4Jet" ] = fs_->make< TH2D >( "jet4PtHTDenom_cut4Jet", "HT vs 4th Leading Jet Pt", 150, 0., 1500., 500, 0., 5000.);
	histos2D_[ "jet4PtHTDenom_cut4Jet" ]->Sumw2();

	histos2D_[ "jet4PtHTPassing_cut4Jet" ] = fs_->make< TH2D >( "jet4PtHTPassing_cut4Jet", "HT vs 4th Leading Jet Pt", 150, 0., 1500., 500, 0., 5000.);
	histos2D_[ "jet4PtHTPassing_cut4Jet" ]->Sumw2();

	histos1D_[ "HTDenom_cutJet4Pt" ] = fs_->make< TH1D >( "HTDenom_cutJet4Pt", "HTDenom_cutJet4Pt", 500, 0., 5000. );
	histos1D_[ "HTDenom_cutJet4Pt" ]->Sumw2();
	histos1D_[ "HTPassing_cutJet4Pt" ] = fs_->make< TH1D >( "HTPassing_cutJet4Pt", "HTPassing_cutJet4Pt", 500, 0., 5000. );
	histos1D_[ "HTPassing_cutJet4Pt" ]->Sumw2();

	histos1D_[ "jet1PtDenom_cutJet4Pt" ] = fs_->make< TH1D >( "jet1PtDenom_cutJet4Pt", "jet1PtDenom_cutJet4Pt", 150, 0., 1500. );
	histos1D_[ "jet1PtDenom_cutJet4Pt" ]->Sumw2();
	histos1D_[ "jet1PtPassing_cutJet4Pt" ] = fs_->make< TH1D >( "jet1PtPassing_cutJet4Pt", "jet1PtPassing_cutJet4Pt", 150, 0., 1500. );
	histos1D_[ "jet1PtPassing_cutJet4Pt" ]->Sumw2();

	histos1D_[ "jet2PtDenom_cutJet4Pt" ] = fs_->make< TH1D >( "jet2PtDenom_cutJet4Pt", "jet2PtDenom_cutJet4Pt", 150, 0., 1500. );
	histos1D_[ "jet2PtDenom_cutJet4Pt" ]->Sumw2();
	histos1D_[ "jet2PtPassing_cutJet4Pt" ] = fs_->make< TH1D >( "jet2PtPassing_cutJet4Pt", "jet2PtPassing_cutJet4Pt", 150, 0., 1500. );
	histos1D_[ "jet2PtPassing_cutJet4Pt" ]->Sumw2();

	histos1D_[ "jet3PtDenom_cutJet4Pt" ] = fs_->make< TH1D >( "jet3PtDenom_cutJet4Pt", "jet3PtDenom_cutJet4Pt", 150, 0., 1500. );
	histos1D_[ "jet3PtDenom_cutJet4Pt" ]->Sumw2();
	histos1D_[ "jet3PtPassing_cutJet4Pt" ] = fs_->make< TH1D >( "jet3PtPassing_cutJet4Pt", "jet3PtPassing_cutJet4Pt", 150, 0., 1500. );
	histos1D_[ "jet3PtPassing_cutJet4Pt" ]->Sumw2();

	histos1D_[ "jet4PtDenom_cutJet4Pt" ] = fs_->make< TH1D >( "jet4PtDenom_cutJet4Pt", "jet4PtDenom_cutJet4Pt", 150, 0., 1500. );
	histos1D_[ "jet4PtDenom_cutJet4Pt" ]->Sumw2();
	histos1D_[ "jet4PtPassing_cutJet4Pt" ] = fs_->make< TH1D >( "jet4PtPassing_cutJet4Pt", "jet4PtPassing_cutJet4Pt", 150, 0., 1500. );
	histos1D_[ "jet4PtPassing_cutJet4Pt" ]->Sumw2();

	histos2D_[ "jet4PtHTDenom_cutJet4Pt" ] = fs_->make< TH2D >( "jet4PtHTDenom_cutJet4Pt", "HT vs 4th Leading Jet Pt", 150, 0., 1500., 500, 0., 5000.);
	histos2D_[ "jet4PtHTDenom_cutJet4Pt" ]->Sumw2();

	histos2D_[ "jet4PtHTPassing_cutJet4Pt" ] = fs_->make< TH2D >( "jet4PtHTPassing_cutJet4Pt", "HT vs 4th Leading Jet Pt", 150, 0., 1500., 500, 0., 5000.);
	histos2D_[ "jet4PtHTPassing_cutJet4Pt" ]->Sumw2();


	histos1D_[ "HTDenom_cutHT" ] = fs_->make< TH1D >( "HTDenom_cutHT", "HTDenom_cutHT", 500, 0., 5000. );
	histos1D_[ "HTDenom_cutHT" ]->Sumw2();
	histos1D_[ "HTPassing_cutHT" ] = fs_->make< TH1D >( "HTPassing_cutHT", "HTPassing_cutHT", 500, 0., 5000. );
	histos1D_[ "HTPassing_cutHT" ]->Sumw2();

	histos1D_[ "jet1PtDenom_cutHT" ] = fs_->make< TH1D >( "jet1PtDenom_cutHT", "jet1PtDenom_cutHT", 150, 0., 1500. );
	histos1D_[ "jet1PtDenom_cutHT" ]->Sumw2();
	histos1D_[ "jet1PtPassing_cutHT" ] = fs_->make< TH1D >( "jet1PtPassing_cutHT", "jet1PtPassing_cutHT", 150, 0., 1500. );
	histos1D_[ "jet1PtPassing_cutHT" ]->Sumw2();

	histos1D_[ "jet2PtDenom_cutHT" ] = fs_->make< TH1D >( "jet2PtDenom_cutHT", "jet2PtDenom_cutHT", 150, 0., 1500. );
	histos1D_[ "jet2PtDenom_cutHT" ]->Sumw2();
	histos1D_[ "jet2PtPassing_cutHT" ] = fs_->make< TH1D >( "jet2PtPassing_cutHT", "jet2PtPassing_cutHT", 150, 0., 1500. );
	histos1D_[ "jet2PtPassing_cutHT" ]->Sumw2();

	histos1D_[ "jet3PtDenom_cutHT" ] = fs_->make< TH1D >( "jet3PtDenom_cutHT", "jet3PtDenom_cutHT", 150, 0., 1500. );
	histos1D_[ "jet3PtDenom_cutHT" ]->Sumw2();
	histos1D_[ "jet3PtPassing_cutHT" ] = fs_->make< TH1D >( "jet3PtPassing_cutHT", "jet3PtPassing_cutHT", 150, 0., 1500. );
	histos1D_[ "jet3PtPassing_cutHT" ]->Sumw2();

	histos1D_[ "jet4PtDenom_cutHT" ] = fs_->make< TH1D >( "jet4PtDenom_cutHT", "jet4PtDenom_cutHT", 150, 0., 1500. );
	histos1D_[ "jet4PtDenom_cutHT" ]->Sumw2();
	histos1D_[ "jet4PtPassing_cutHT" ] = fs_->make< TH1D >( "jet4PtPassing_cutHT", "jet4PtPassing_cutHT", 150, 0., 1500. );
	histos1D_[ "jet4PtPassing_cutHT" ]->Sumw2();

	histos2D_[ "jet4PtHTDenom_cutHT" ] = fs_->make< TH2D >( "jet4PtHTDenom_cutHT", "jet4PtHTDenom_cutHT", 150, 0., 1500., 500, 0., 5000.);
	histos2D_[ "jet4PtHTDenom_cutHT" ]->Sumw2();

	histos2D_[ "jet4PtHTPassing_cutHT" ] = fs_->make< TH2D >( "jet4PtHTPassing_cutHT", "jet4PtHTPassing_cutHT", 150, 0., 1500., 500, 0., 5000.);
	histos2D_[ "jet4PtHTPassing_cutHT" ]->Sumw2();


}

// ------------ method called once each job just after ending the event loop  ------------
void RUNResolvedMiniAODTriggerEfficiency::endJob() {

}

void RUNResolvedMiniAODTriggerEfficiency::fillDescriptions(edm::ConfigurationDescriptions & descriptions) {

	edm::ParameterSetDescription desc;

	desc.add<double>("cutAK4jetPt", 50);
	desc.add<double>("cutAK4jet4Pt", 80);
	desc.add<double>("cutAK4HT", 800);
	desc.add<string>("baseTrigger", "HLT_PFHT475");
	desc.add<InputTag>("bits", 	InputTag("TriggerResults", "", "HLT"));
	desc.add<InputTag>("prescales", 	InputTag("patTrigger"));
	desc.add<InputTag>("hltTrigger", 	InputTag("hltTriggerSummaryAOD","","HLT"));
	desc.add<InputTag>("recoJets", 	InputTag("slimmedJets"));
	vector<string> HLTPass;
	HLTPass.push_back("HLT_PFHT800");
	desc.add<vector<string>>("triggerPass",	HLTPass);

	descriptions.addDefault(desc);
}
      

//define this as a plug-in
DEFINE_FWK_MODULE(RUNResolvedMiniAODTriggerEfficiency);
