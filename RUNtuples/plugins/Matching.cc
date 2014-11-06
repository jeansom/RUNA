// -*- C++ -*-
//
// Package:    RUNA/RUNtuples
// Class:      Matching
// 
/**\class Matching Matching.cc RUNA/RUNtuples/plugins/Matching.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  alejandro gomez
//         Created:  Fri, 31 Oct 2014 16:15:59 GMT
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"

#include "TH1D.h"
#include <TLorentzVector.h>
//
// class declaration
//

class Matching : public edm::EDAnalyzer {
   public:
      explicit Matching(const edm::ParameterSet&);
      ~Matching();

      //static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      //virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
      //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

      // ----------member data ---------------------------
      edm::EDGetTokenT<reco::PFJetCollection> jets_;
      edm::EDGetTokenT<reco::GenParticleCollection> genParticles_;

      std::map< std::string, TH1D* > histos1D_;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
Matching::Matching(const edm::ParameterSet& iConfig):
    jets_(consumes<reco::PFJetCollection>(iConfig.getParameter<edm::InputTag>("jets"))),
    genParticles_(consumes<reco::GenParticleCollection>(iConfig.getParameter<edm::InputTag>("genParticles")))
{
   //now do what ever initialization is needed

}


Matching::~Matching()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
Matching::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;

	edm::Handle<reco::PFJetCollection> jets;
	iEvent.getByToken(jets_, jets);
	
	edm::Handle<reco::GenParticleCollection> genParticles;
	iEvent.getByToken(genParticles_, genParticles);

	std::vector<TLorentzVector> stopADaughter, stopBDaughter, p4Jets;

	for( const reco::GenParticle &p : * genParticles){

		const reco::Candidate * mom = p.mother();
		bool finalParticle =  (p.status() == 21 || p.status() == 22 || p.status() == 23);
		if(!mom || !finalParticle ) continue;

		TLorentzVector tmp1, tmp2;
		if( mom->pdgId() == 1000002 ){
			//LogWarning("stopA") << mom->pdgId() << " " << p.pdgId();
			tmp1.SetPtEtaPhiE( p.pt(), p.eta(), p.phi(), p.energy() );
		       	stopADaughter.push_back( tmp1 );
		}
		if( mom->pdgId() == -1000002 ){
			//LogWarning("stopB") << mom->pdgId() << " " << p.pdgId();
			tmp2.SetPtEtaPhiE( p.pt(), p.eta(), p.phi(), p.energy() );
		       	stopBDaughter.push_back( tmp2 );
		}
	}

	for (const pat::Jet &ijet : *jets) {

		if( ijet.pt() < 100 || TMath::Abs( ijet.eta() ) > 3.0 ) continue;
		TLorentzVector tmpJet;
		tmpJet.SetPtEtaPhiE( ijet.pt(), ijet.eta(), ijet.phi(), ijet.energy() );
		p4Jets.push_back( tmpJet );
		//LogWarning("jet pt") << ijet.pt() << " " << ijet.eta();
	}

	Int_t indexStopA[2] = { -1, -1};
	Int_t indexStopB[2] = { -1, -1};
	for (unsigned int i = 0; i < stopADaughter.size(); i++) {
		double tmpDeltaR1 = 999;
		double tmpDeltaR2 = 999;
		for (unsigned int j = 0; j < p4Jets.size(); j++) {

			double deltaR1 = stopADaughter[i].DeltaR( p4Jets[j] );
			if( deltaR1 < tmpDeltaR1 ) {
				tmpDeltaR1 = deltaR1;
				if( tmpDeltaR1 < 0.7 ) indexStopA[i] = j;
				//LogWarning("deltaR1") << i << " " << j << " " << tmpDeltaR1;
			}

			double deltaR2 = stopBDaughter[i].DeltaR( p4Jets[j] );
			if( deltaR2 < tmpDeltaR2 ){
			       tmpDeltaR2 = deltaR2;
			       if( tmpDeltaR2 < 0.7 ) indexStopB[i] = j;
				//LogWarning("deltaR2") << i << " " << j << " " << tmpDeltaR2;
			}
		}
		histos1D_[ "deltaR" ]->Fill( tmpDeltaR1 );
		histos1D_[ "deltaR" ]->Fill( tmpDeltaR2 );
	}
	if( indexStopA[0] != -1 && indexStopA[0] == indexStopA[1] ) LogWarning("StopA") << indexStopA[0] << " " << indexStopA[1] ;
	if( indexStopB[0] != -1 && indexStopB[0] == indexStopB[1] ) LogWarning("StopB") << indexStopB[0] << " " << indexStopB[1];


}


// ------------ method called once each job just before starting event loop  ------------
void 
Matching::beginJob()
{
	edm::Service< TFileService > fileService;

	histos1D_[ "deltaR" ] = fileService->make< TH1D >( "deltaR", "deltaR", 50, 0., 5. );
	histos1D_[ "deltaR" ]->SetXTitle( "Delta R" );
}

// ------------ method called once each job just after ending the event loop  ------------
void 
Matching::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
/*
void 
Matching::beginRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a run  ------------
/*
void 
Matching::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when starting to processes a luminosity block  ------------
/*
void 
Matching::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a luminosity block  ------------
/*
void 
Matching::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
/*void
Matching::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}*/

//define this as a plug-in
DEFINE_FWK_MODULE(Matching);
