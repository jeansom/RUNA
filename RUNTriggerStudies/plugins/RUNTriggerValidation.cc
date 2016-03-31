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

using namespace edm;
using namespace std;

class RUNTriggerValidation : public edm::EDAnalyzer {

	public:
		explicit RUNTriggerValidation(const edm::ParameterSet&);
      		static void fillDescriptions(edm::ConfigurationDescriptions & descriptions);
		~RUNTriggerValidation() {}

	private:
		virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      		virtual void beginJob() override;

	edm::EDGetTokenT<edm::TriggerResults> triggerBits_;
	edm::EDGetTokenT<pat::TriggerObjectStandAloneCollection> triggerObjects_;
	edm::EDGetTokenT<pat::PackedTriggerPrescales> triggerPrescales_;
	edm::EDGetTokenT<trigger::TriggerEvent> triggerEvent_;
	edm::EDGetTokenT<pat::JetCollection> jetToken_;
	std::string hltPath_;
    	int triggerBit;

	edm::Service<TFileService> fs_;
	map< string, TH1D* > histos1D_;
	map< string, TH2D* > histos2D_;
};

RUNTriggerValidation::RUNTriggerValidation(const edm::ParameterSet& iConfig):
	triggerBits_(consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("bits"))),
	triggerObjects_(consumes<pat::TriggerObjectStandAloneCollection>(iConfig.getParameter<edm::InputTag>("objects"))),
	triggerPrescales_(consumes<pat::PackedTriggerPrescales>(iConfig.getParameter<edm::InputTag>("prescales"))),
	triggerEvent_(consumes<trigger::TriggerEvent>(iConfig.getParameter<edm::InputTag>("hltTrigger"))),
	jetToken_(consumes<pat::JetCollection>(iConfig.getParameter<edm::InputTag>("recoJets"))),
	hltPath_(iConfig.getParameter<std::string>("hltPath"))
{
}

void RUNTriggerValidation::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {

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
	triggerBit = -1;
  	bool pathFound = 0;
	std::string triggerName;
	for (unsigned int i = 0, n = triggerBits->size(); i < n; ++i) {
		if (TString(names.triggerName(i)).Contains(hltPath_) && (triggerBits->accept(i))) {
			triggerBit = i;
			pathFound=1;
			triggerName = names.triggerName(i);
			//std::cout << "\n === TRIGGER PATHS === " << std::endl;
			//std::cout << "Trigger " << names.triggerName(i) << ", prescale " << triggerPrescales->getPrescaleForIndex(i) << ": " << (triggerBits->accept(i) ? "PASS" : "fail (or not run)") << std::endl;
		}
	}

	if (pathFound) {
		//std::cout << "\n === TRIGGER OBJECTS === " << std::endl;
		double hltHT = 0;
		double hlttrimmedMass = 0;
		int numJets = 0;
		for (pat::TriggerObjectStandAlone obj : *triggerObjects) { // note: not "const &" since we want to call unpackPathNames
			obj.unpackPathNames(names);
			if ( TString(obj.collection()).Contains("hltAK8PFJetsTrimR0p1PT0p03") ) {
				//std::cout << "\tTrigger object Trimmed Mass:  pt " << obj.pt() << ", eta " << obj.eta() << ", phi " << obj.phi() << ", mass " << obj.mass() << std::endl;
				hlttrimmedMass = obj.mass();
				numJets++;
				histos1D_[ "hltTrimmedMass" ]->Fill( obj.mass() );
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
		if ( hltHT > 0 ) histos2D_[ "hltTrimmedMassvsHT" ]->Fill( hlttrimmedMass, hltHT );
		if ( numJets > 0 ) histos1D_[ "hltNumJetsTrimmedMass" ]->Fill( numJets );

		double HT = 0;
		int k = 0;
		for (const pat::Jet &jet : *jets) {
			HT += jet.pt();
			if ((++k)==1){
				histos1D_[ "jet1Mass" ]->Fill( jet.mass() );
				histos1D_[ "jet1TrimmedMass" ]->Fill( jet.userFloat( "ak8PFJetsCHSTrimmedMass" ) );
				histos1D_[ "jet1Pt" ]->Fill( jet.pt() );
			}
		}
		if ( HT > 0 ) histos1D_[ "HT" ]->Fill( HT );
	}
}

void RUNTriggerValidation::beginJob() {

	histos1D_[ "hltTrimmedMass" ] = fs_->make< TH1D >( "hltTrimmedMass", "hltTrimmedMass", 100, 0., 1000. );
	histos1D_[ "hltTrimmedMass" ]->Sumw2();
	histos1D_[ "hltNumJetsTrimmedMass" ] = fs_->make< TH1D >( "hltNumJetsTrimmedMass", "hltNumJetsTrimmedMass", 10, 0., 10. );
	histos1D_[ "hltNumJetsTrimmedMass" ]->Sumw2();
	histos1D_[ "hltHT" ] = fs_->make< TH1D >( "hltHT", "hltHT", 100, 0., 2000. );
	histos1D_[ "hltHT" ]->Sumw2();
	histos1D_[ "jet1Mass" ] = fs_->make< TH1D >( "jet1Mass", "jet1Mass", 100, 0., 1000. );
	histos1D_[ "jet1Mass" ]->Sumw2();
	histos1D_[ "jet1TrimmedMass" ] = fs_->make< TH1D >( "jet1TrimmedMass", "jet1TrimmedMass", 100, 0., 1000. );
	histos1D_[ "jet1TrimmedMass" ]->Sumw2();
	histos1D_[ "jet1Pt" ] = fs_->make< TH1D >( "jet1Pt", "jet1Pt", 100, 0., 1000. );
	histos1D_[ "jet1Pt" ]->Sumw2();
	histos1D_[ "HT" ] = fs_->make< TH1D >( "HT", "HT", 100, 0., 2000. );
	histos1D_[ "HT" ]->Sumw2();

	histos2D_[ "hltTrimmedMassvsHT" ] = fs_->make< TH2D >( "hltTrimmedMassvsHT", "hltTrimmedMassvsHT", 100, 0., 1000., 100, 0., 2000. );
	histos2D_[ "hltTrimmedMassvsHT" ]->Sumw2();
}

void RUNTriggerValidation::fillDescriptions(edm::ConfigurationDescriptions & descriptions) {

	edm::ParameterSetDescription desc;
	desc.add<InputTag>("bits", 	InputTag("TriggerResults", "", "HLT"));
	desc.add<InputTag>("prescales", 	InputTag("patTrigger"));
	desc.add<InputTag>("objects", 	InputTag("selectedPatTrigger"));
	desc.add<InputTag>("hltPath", 	InputTag("HLT_PFHT800"));
	desc.add<InputTag>("hltTrigger", 	InputTag("hltTriggerSummaryAOD","","HLT"));
	desc.add<InputTag>("recoJets", 	InputTag("slimmedJetsAK8"));
	descriptions.addDefault(desc);
}
      

//define this as a plug-in
DEFINE_FWK_MODULE(RUNTriggerValidation);
