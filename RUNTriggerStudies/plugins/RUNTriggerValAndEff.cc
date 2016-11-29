// system include files
#include <memory>
#include <cmath>
#include <TH1.h>
#include <TH2.h>
#include <TLorentzVector.h>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Math/interface/deltaR.h"
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/HLTReco/interface/TriggerObject.h"
#include "DataFormats/HLTReco/interface/TriggerEvent.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"
#include "DataFormats/PatCandidates/interface/PackedTriggerPrescales.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/JetReco/interface/Jet.h"

#include "RUNA/RUNAnalysis/interface/CommonVariablesStructure.h"

using namespace edm;
using namespace std;

class RUNTriggerValAndEff : public edm::EDAnalyzer {

	public:
		explicit RUNTriggerValAndEff(const edm::ParameterSet&);
      		static void fillDescriptions(edm::ConfigurationDescriptions & descriptions);
		~RUNTriggerValAndEff() {}

	private:
		virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      		virtual void beginJob() override;

	edm::EDGetTokenT<edm::TriggerResults> triggerBits_;
	edm::EDGetTokenT<pat::TriggerObjectStandAloneCollection> triggerObjects_;
	edm::EDGetTokenT<pat::PackedTriggerPrescales> triggerPrescales_;
	edm::EDGetTokenT<trigger::TriggerEvent> triggerEvent_;
	edm::EDGetTokenT<pat::JetCollection> jetToken_;
	std::string baseTrigger_;
      	vector<string> triggerPass_;

	edm::Service<TFileService> fs_;
	map< string, TH1D* > histos1D_;
	map< string, TH2D* > histos2D_;
};

RUNTriggerValAndEff::RUNTriggerValAndEff(const edm::ParameterSet& iConfig):
	triggerBits_(consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("bits"))),
	triggerObjects_(consumes<pat::TriggerObjectStandAloneCollection>(iConfig.getParameter<edm::InputTag>("objects"))),
	triggerPrescales_(consumes<pat::PackedTriggerPrescales>(iConfig.getParameter<edm::InputTag>("prescales"))),
	triggerEvent_(consumes<trigger::TriggerEvent>(iConfig.getParameter<edm::InputTag>("hltTrigger"))),
	jetToken_(consumes<pat::JetCollection>(iConfig.getParameter<edm::InputTag>("recoJets")))
{
	baseTrigger_ = iConfig.getParameter<std::string>("baseTrigger");
	triggerPass_ = iConfig.getParameter<vector<string>>("triggerPass");
}

void RUNTriggerValAndEff::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {

	edm::Handle<edm::TriggerResults> triggerBits;
	edm::Handle<pat::TriggerObjectStandAloneCollection> triggerObjects;
	edm::Handle<pat::PackedTriggerPrescales> triggerPrescales;
	edm::Handle<trigger::TriggerEvent> trigEvent; 
	edm::Handle<pat::JetCollection> jets;

	iEvent.getByToken(triggerBits_, triggerBits);
	iEvent.getByToken(triggerObjects_, triggerObjects);
	iEvent.getByToken(triggerPrescales_, triggerPrescales);
	iEvent.getByToken(triggerEvent_,trigEvent);
	iEvent.getByToken(jetToken_, jets);

	const edm::TriggerNames &names = iEvent.triggerNames(*triggerBits);
  	bool ORTriggers = checkORListOfTriggerBitsMiniAOD( names, triggerBits, triggerPrescales, triggerPass_, false );
  	bool baseTrigger = checkTriggerBitsMiniAOD( names, triggerBits, triggerPrescales, baseTrigger_, true );

	if ( baseTrigger || ORTriggers ) {

		if (ORTriggers) {
			//std::cout << "\n === TRIGGER OBJECTS === " << std::endl;
			double hltHT = 0;
			double hltprunedMass = 0;
			int numJets = 0;
			for (pat::TriggerObjectStandAlone obj : *triggerObjects) { // note: not "const &" since we want to call unpackPathNames
				obj.unpackPathNames(names);
				if ( TString(obj.collection()).Contains("hltAK8PFJetsTrimR0p1PT0p03") ) {
					//std::cout << "\tTrigger object Trimmed Mass:  pt " << obj.pt() << ", eta " << obj.eta() << ", phi " << obj.phi() << ", mass " << obj.mass() << std::endl;
					hltprunedMass = obj.mass();
					numJets++;
					histos1D_[ "hltPrunedMass" ]->Fill( obj.mass() );
				}
				if ( TString(obj.collection()).Contains("hltAK8PFHT") ) {
					for (unsigned h = 0; h < obj.filterIds().size(); ++h) {
						if (obj.filterIds()[h] == 89 ) {
							hltHT = obj.pt();
							histos1D_[ "hltHT" ]->Fill( obj.pt() );
							//std::cout << "\tTrigger object HT:  pt " << obj.pt() << ", eta " << obj.eta() << ", phi " << obj.phi() << ", mass " << obj.mass() << std::endl;
						}
					}
				}
			}
			if ( hltHT > 0 ) histos2D_[ "hltPrunedMassvsHT" ]->Fill( hltprunedMass, hltHT );
			if ( numJets > 0 ) histos1D_[ "hltNumJetsPrunedMass" ]->Fill( numJets );
		}

		double HT = 0;
		int k = 0;
		for (const pat::Jet &jet : *jets) {
			HT += jet.pt();
			if ( jet.pt() < 150 ) continue;
			if ( TMath::Abs( jet.eta() ) > 2.4 ) continue;

			if ((++k)==1){
				histos1D_[ "jet1Mass" ]->Fill( jet.mass() );
				histos1D_[ "jet1PrunedMass" ]->Fill( jet.userFloat( "ak8PFJetsCHSPrunedMass" ) );
				histos1D_[ "jet1Pt" ]->Fill( jet.pt() );
			}

			if ( baseTrigger ) {
				histos1D_[ "prunedMassDenom_cutDijet" ]->Fill( jet.userFloat( "ak8PFJetsCHSPrunedMass" ) );

				if ( ORTriggers ){
					histos1D_[ "prunedMassPassing_cutDijet" ]->Fill( jet.userFloat( "ak8PFJetsCHSPrunedMass" ) );
				}
			}
		}
		if ( HT > 0 ) histos1D_[ "HT" ]->Fill( HT );
	}
}

void RUNTriggerValAndEff::beginJob() {

	histos1D_[ "hltPrunedMass" ] = fs_->make< TH1D >( "hltPrunedMass", "hltPrunedMass", 100, 0., 1000. );
	histos1D_[ "hltPrunedMass" ]->Sumw2();
	histos1D_[ "hltNumJetsPrunedMass" ] = fs_->make< TH1D >( "hltNumJetsPrunedMass", "hltNumJetsPrunedMass", 10, 0., 10. );
	histos1D_[ "hltNumJetsPrunedMass" ]->Sumw2();
	histos1D_[ "hltHT" ] = fs_->make< TH1D >( "hltHT", "hltHT", 100, 0., 2000. );
	histos1D_[ "hltHT" ]->Sumw2();
	histos1D_[ "jet1Mass" ] = fs_->make< TH1D >( "jet1Mass", "jet1Mass", 100, 0., 1000. );
	histos1D_[ "jet1Mass" ]->Sumw2();
	histos1D_[ "jet1PrunedMass" ] = fs_->make< TH1D >( "jet1PrunedMass", "jet1PrunedMass", 100, 0., 1000. );
	histos1D_[ "jet1PrunedMass" ]->Sumw2();
	histos1D_[ "jet1Pt" ] = fs_->make< TH1D >( "jet1Pt", "jet1Pt", 100, 0., 1000. );
	histos1D_[ "jet1Pt" ]->Sumw2();
	histos1D_[ "HT" ] = fs_->make< TH1D >( "HT", "HT", 100, 0., 2000. );
	histos1D_[ "HT" ]->Sumw2();

	histos2D_[ "hltPrunedMassvsHT" ] = fs_->make< TH2D >( "hltPrunedMassvsHT", "hltPrunedMassvsHT", 100, 0., 1000., 100, 0., 2000. );
	histos2D_[ "hltPrunedMassvsHT" ]->Sumw2();

	histos1D_[ "prunedMassDenom_cutDijet" ] = fs_->make< TH1D >( "prunedMassDenom_cutDijet", "prunedMassDenom_cutDijet", 100, 0., 1000. );
	histos1D_[ "prunedMassDenom_cutDijet" ]->Sumw2();
	histos1D_[ "prunedMassPassing_cutDijet" ] = fs_->make< TH1D >( "prunedMassPassing_cutDijet", "prunedMassPassing_cutDijet", 100, 0., 1000. );
	histos1D_[ "prunedMassPassing_cutDijet" ]->Sumw2();
}

void RUNTriggerValAndEff::fillDescriptions(edm::ConfigurationDescriptions & descriptions) {

	edm::ParameterSetDescription desc;
	desc.add<InputTag>("bits", 	InputTag("TriggerResults", "", "HLT"));
	desc.add<InputTag>("prescales", 	InputTag("patTrigger"));
	desc.add<InputTag>("objects", 	InputTag("selectedPatTrigger"));
	desc.add<string>("baseTrigger", 	"HLT_PFHT800");
	desc.add<InputTag>("hltTrigger", 	InputTag("hltTriggerSummaryAOD","","HLT"));
	desc.add<InputTag>("recoJets", 	InputTag("slimmedJetsAK8"));
	vector<string> HLTPass;
	HLTPass.push_back("HLT_AK8PFHT650_TrimR0p1PT0p03Mass50");
	desc.add<vector<string>>("triggerPass",	HLTPass);
	descriptions.addDefault(desc);
}
      
//define this as a plug-in
DEFINE_FWK_MODULE(RUNTriggerValAndEff);
