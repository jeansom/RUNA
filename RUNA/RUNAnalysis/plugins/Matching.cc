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

#include "DataFormats/Math/interface/deltaR.h"

#include "TH1D.h"
#include <TLorentzVector.h>
//
// class declaration
//

class Matching : public edm::EDAnalyzer {
   public:
      explicit Matching(const edm::ParameterSet&);
      bool isAncestor(const reco::Candidate * ancestor, const reco::Candidate * particle);
//      bool checkDeltaR(reco::CandidateCollection p1, reco::CandidateCollection jets, double minDeltaR);
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
      int particle1, particle2, particle3;

      std::map< std::string, TH1D* > histos1D_;
      //std::map< std::size_t , reco::Candidate > decayStory_;
};

//
// constants, enums and typedefs
//
typedef struct {
	bool pass;
	std::vector<double> deltaRVector;
	int indexJet;
} matched;

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
    particle1 = iConfig.getParameter<int>("particle1");
    particle2 = iConfig.getParameter<int>("particle2");
    particle3 = iConfig.getParameter<int>("particle3");

}


Matching::~Matching()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//
//Check recursively if any ancestor of particle is the given one

bool Matching::isAncestor(const reco::Candidate* ancestor, const reco::Candidate * particle)
{
	//particle is already the ancestor
	//edm::LogWarning("testing") << ancestor->pdgId() << " " << ancestor->pt() << " " << particle->pdgId() << " " << particle->pt();
        if( ( ancestor->pdgId() == particle->pdgId() ) && ( ancestor->mass() == particle->mass() ) ) {  
		//edm::LogWarning("is ancestor") << ancestor->pdgId() << " " << ancestor->status() << " " << particle->mother()->pdgId() << " " << particle->pdgId();
		if ( ( ancestor->pt() == particle->pt() ) && ( particle->status() == 22 ) ) return true;
	}

	//otherwise loop on mothers, if any and return true if the ancestor is found
	if( particle->mother() != nullptr ) {
		if( isAncestor( ancestor,particle->mother()) ) return true;
	}
	//if we did not return yet, then particle and ancestor are not relatives
	return false;
}

matched checkDeltaR(reco::CandidateCollection partons, reco::CandidateCollection jets, double minDeltaR){

	std::vector<int> index;
	std::vector<double> deltaRVec;
	for( size_t i=0; i<partons.size(); i++ ){
		double deltaR = 99999;
		int ind = -1;
		const reco::Candidate & p1 = (partons)[i];
		//edm::LogWarning("genParticle ")  << p1.pdgId();

		for( unsigned int j=0; j<jets.size(); j++ ) {
			const reco::Candidate & p2 = (jets)[j];
			double tmpdeltaR = reco::deltaR2( p1.rapidity(), p1.phi(), p2.rapidity(), p2.phi() );
			//edm::LogWarning("calc deltaR") << tmpdeltaR << " " << j;
			if( tmpdeltaR < deltaR ) {
				deltaR = tmpdeltaR;
				ind = j;
			}
		}
		//edm::LogWarning("deltaR") << deltaR << " " << ind ;
		if( deltaR < minDeltaR) {
			index.push_back(ind);
			deltaRVec.push_back( deltaR );
		}
	}
//	for ( unsigned int i = 0; i < index.size(); i++) edm::LogWarning("index") << index[i] << " " << deltaRVec[i];
	
	bool passed;
	int finalindex = -9999;
	if( ( partons.size() == index.size() )  && std::equal(index.begin() + 1, index.end(), index.begin()) ){
		passed = true;
		finalindex = index[0];
	} else passed = false;

	matched results;
	results.pass = passed;
	results.deltaRVector = deltaRVec;
	results.indexJet = finalindex;

	return results;
}

// ------------ method called for each event  ------------
void
Matching::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;

	edm::Handle<reco::PFJetCollection> jets;
	iEvent.getByToken(jets_, jets);
	
	edm::Handle<reco::GenParticleCollection> genParticles;
	iEvent.getByToken(genParticles_, genParticles);


	reco::CandidateCollection p1Collection, p2Collection, p3Collection, finalParticlesCollection;

	for( size_t i = 0; i < genParticles->size(); i++ ) {

		const reco::Candidate &p = ( *genParticles )[i];

		if( ( TMath::Abs( p.pdgId() ) == particle1 ) && p.status() == 22 ) p1Collection.push_back( p );
		if( ( TMath::Abs( p.pdgId() ) == particle2 ) && p.status() == 22 ) p2Collection.push_back( p );
		if( ( TMath::Abs( p.pdgId() ) == particle3 ) && p.status() == 22 ) p3Collection.push_back( p );

		bool parton = ( ( TMath::Abs( p.pdgId() ) < 6 ) || ( p.pdgId() == 21 )  );
		if( p.status() == 23 && parton ) finalParticlesCollection.push_back( p );

	}

	std::vector< reco::CandidateCollection  > daughtersParticle1, daughtersParticle2, daughtersParticle3;
	if( finalParticlesCollection.size() > 0 ){

		reco::CandidateCollection tmp1, tmp2, tmp3, tmp4, tmp5, tmp6;
		if( p1Collection.size() == 2 ){

			const reco::Candidate * jp1 = &(p1Collection)[0];
			const reco::Candidate * jp2 = &(p1Collection)[1];

			for( reco::Candidate & fp : finalParticlesCollection ) {

				const reco::Candidate * finalMother = fp.mother();
				if( isAncestor( jp1, finalMother ) ) tmp1.push_back( fp );   //LogWarning("Particle found 1") << jp1->pdgId() << " " << fp.pdgId();
				if( isAncestor( jp2, finalMother ) ) tmp2.push_back( fp );  //LogWarning("Particle found 2") << jp2->pdgId() << " " << fp.pdgId();
			}

		}
		daughtersParticle1.push_back( tmp1 );
		daughtersParticle1.push_back( tmp2 );

		if( p2Collection.size() == 2 ){

			const reco::Candidate * ip1 = &(p2Collection)[0];
			const reco::Candidate * ip2 = &(p2Collection)[1];

			for( reco::Candidate & fp : finalParticlesCollection ) {

				//edm::LogWarning("finalParticle") << fp.pdgId(); 
				const reco::Candidate * finalMother = fp.mother();
				if( isAncestor( ip1, finalMother ) ) tmp3.push_back( fp );    //LogWarning("Particle found 1") << ip1->pdgId() << " " << fp.pdgId();
				if( isAncestor( ip2, finalMother ) ) tmp4.push_back( fp );  //LogWarning("Particle found 2") << jp2->pdgId() << " " << fp.pdgId();
			}

		}
		daughtersParticle2.push_back( tmp3 );
		daughtersParticle2.push_back( tmp4 );

		if( p3Collection.size() == 2 ){

			const reco::Candidate * kp1 = &(p3Collection)[0];
			const reco::Candidate * kp2 = &(p3Collection)[1];

			for( reco::Candidate & fp : finalParticlesCollection ) {

				const reco::Candidate * finalMother = fp.mother();
				if( isAncestor( kp1, finalMother ) ) tmp5.push_back( fp );   //LogWarning("Particle found 1") << jp1->pdgId() << " " << fp.pdgId();
				if( isAncestor( kp2, finalMother ) ) tmp6.push_back( fp );  //LogWarning("Particle found 2") << jp2->pdgId() << " " << fp.pdgId();
			}

		}
		daughtersParticle3.push_back( tmp5 );
		daughtersParticle3.push_back( tmp6 );
	} else LogWarning("No particles with status 23") << "No final particles";

	/*LogWarning("number of daughters 1") << daughtersParticle1.size() << " " << daughtersParticle1[0].size();
	LogWarning("number of daughters 2") << daughtersParticle2.size() << " " << daughtersParticle2[0].size();
	LogWarning("number of daughters 3") << daughtersParticle3.size() << " " << daughtersParticle3[0].size();
	*/

	reco::CandidateCollection selectedJets;
	for (const pat::Jet &ijet : *jets) {

		if( ijet.pt() < 100 || TMath::Abs( ijet.eta() ) > 2.5 ) continue;
		selectedJets.push_back( ijet );
		//LogWarning("jet pt") << ijet.pt() << " " << ijet.eta();
	}

	if( ( daughtersParticle1[0].size() > 1 ) && ( selectedJets.size() > 0 ) ){

		double deltaRdaughtersParticle1 = reco::deltaR2(  daughtersParticle1[0][0].rapidity(),  daughtersParticle1[0][0].phi(),  daughtersParticle1[0][1].rapidity(),  daughtersParticle1[0][1].phi() );
		histos1D_[ "p1DaughtersDeltaR" ]->Fill( deltaRdaughtersParticle1 );

	       matched infoPar11;
	       infoPar11 = checkDeltaR( daughtersParticle1[0], selectedJets, 0.6 );
	       bool passPar11 = infoPar11.pass;
	       std::vector<double> deltaR11 = infoPar11.deltaRVector;
	       int index11 = infoPar11.indexJet;

	       if (passPar11 && ( index11 > 0 ) ){ 
		       LogWarning( "Matching found" ) << "Particle " << particle1 << " has all its daughters in a single jet";
		       for( unsigned int q=0; q< deltaR11.size(); q++ ) histos1D_[ "p1DeltaR" ]->Fill( deltaR11[q] );
		       histos1D_[ "p1JetMass" ]->Fill( selectedJets[ index11 ].mass() );
	       }
	}

	if( ( daughtersParticle1[1].size() > 1 ) && ( selectedJets.size() > 0 ) ){

		double deltaRdaughtersParticle2 = reco::deltaR2(  daughtersParticle1[1][0].rapidity(),  daughtersParticle1[1][0].phi(),  daughtersParticle1[1][1].rapidity(),  daughtersParticle1[1][1].phi() );
		histos1D_[ "p2DaughtersDeltaR" ]->Fill( deltaRdaughtersParticle2 );

	       matched infoPar12;
	       infoPar12 = checkDeltaR( daughtersParticle1[1], selectedJets, 0.6 );
	       bool passPar12 = infoPar12.pass;
	       std::vector<double> deltaR12 = infoPar12.deltaRVector;
	       int index12 = infoPar12.indexJet;

	       if (passPar12 && ( index12 > 0 ) ){ 
		       LogWarning( "Matching found" ) << "Particle " << particle1 << " has all its daughters in a single jet";
		       for( unsigned int q=0; q< deltaR12.size(); q++ ) histos1D_[ "p1DeltaR" ]->Fill( deltaR12[q] );
		       histos1D_[ "p1JetMass" ]->Fill( selectedJets[ index12 ].mass() );
	       }
	}

	if( ( daughtersParticle2[0].size() > 1 ) && ( selectedJets.size() > 0 ) ){

	       matched infoPar21;
	       infoPar21 = checkDeltaR( daughtersParticle2[0], selectedJets, 0.6 );
	       bool passPar21 = infoPar21.pass;
	       std::vector<double> deltaR21 = infoPar21.deltaRVector;
	       int index21 = infoPar21.indexJet;

	       if (passPar21 && ( index21 > 0 ) ){ 
		       LogWarning( "Matching found" ) << "Particle " << particle2 << " has all its daughters in a single jet";
		       for( unsigned int q=0; q< deltaR21.size(); q++ ) histos1D_[ "p2DeltaR" ]->Fill( deltaR21[q] );
		       histos1D_[ "p2JetMass" ]->Fill( selectedJets[ index21 ].mass() );
	       }
	}

	if( ( daughtersParticle2[1].size() > 1 ) && ( selectedJets.size() > 0 ) ){

	       matched infoPar22;
	       infoPar22 = checkDeltaR( daughtersParticle2[1], selectedJets, 0.6 );
	       bool passPar22 = infoPar22.pass;
	       std::vector<double> deltaR22 = infoPar22.deltaRVector;
	       int index22 = infoPar22.indexJet;

	       if (passPar22 && ( index22 > 0 ) ){ 
		       LogWarning( "Matching found" ) << "Particle " << particle2 << " has all its daughters in a single jet";
		       for( unsigned int q=0; q< deltaR22.size(); q++ ) histos1D_[ "p2DeltaR" ]->Fill( deltaR22[q] );
		       histos1D_[ "p2JetMass" ]->Fill( selectedJets[ index22 ].mass() );
	       }

	}

	if( ( daughtersParticle3[0].size() > 1 ) && ( selectedJets.size() > 0 ) ){

	       matched infoPar31;
	       infoPar31 = checkDeltaR( daughtersParticle3[0], selectedJets, 0.6 );
	       bool passPar31 = infoPar31.pass;
	       std::vector<double> deltaR31 = infoPar31.deltaRVector;
	       int index31 = infoPar31.indexJet;

	       if (passPar31 && ( index31 > 0 ) ){ 
		       LogWarning( "Matching found" ) << "Particle " << particle3 << " has all its daughters in a single jet";
		       for( unsigned int q=0; q< deltaR31.size(); q++ ) histos1D_[ "p3DeltaR" ]->Fill( deltaR31[q] );
		       histos1D_[ "p3JetMass" ]->Fill( selectedJets[ index31 ].mass() );
	       }
	}

	if( ( daughtersParticle3[1].size() > 1 ) && ( selectedJets.size() > 0 ) ){

	       matched infoPar32;
	       infoPar32 = checkDeltaR( daughtersParticle3[1], selectedJets, 0.6 );
	       bool passPar32 = infoPar32.pass;
	       std::vector<double> deltaR32 = infoPar32.deltaRVector;
	       int index32 = infoPar32.indexJet;

	       if (passPar32 && ( index32 > 0 ) ){ 
		       LogWarning( "Matching found" ) << "Particle " << particle3 << " has all its daughters in a single jet";
		       for( unsigned int q=0; q< deltaR32.size(); q++ ) histos1D_[ "p3DeltaR" ]->Fill( deltaR32[q] );
		       histos1D_[ "p3JetMass" ]->Fill( selectedJets[ index32 ].mass() );
	       }

	}

}


// ------------ method called once each job just before starting event loop  ------------
void 
Matching::beginJob()
{
	edm::Service< TFileService > fileService;

	histos1D_[ "p1DaughtersDeltaR" ] = fileService->make< TH1D >( "p1DaughtersDeltaR", "p1DaughtersDeltaR", 150, 0., 1.5 );
	histos1D_[ "p1DaughtersDeltaR" ]->SetXTitle( "#Delta R( parton, parton)" );
	histos1D_[ "p2DaughtersDeltaR" ] = fileService->make< TH1D >( "p2DaughtersDeltaR", "p2DaughtersDeltaR", 150, 0., 1.5 );
	histos1D_[ "p2DaughtersDeltaR" ]->SetXTitle( "#Delta R( parton, parton)" );
	histos1D_[ "p1DeltaR" ] = fileService->make< TH1D >( "p1DeltaR", "p1DeltaR", 50, 0., 5. );
	histos1D_[ "p1DeltaR" ]->SetXTitle( "min #Delta R( jet, parton)" );
	histos1D_[ "p1JetMass" ] = fileService->make< TH1D >( "p1JetMass", "p1JetMass", 120, 0., 1200. );
	histos1D_[ "p1JetMass" ]->SetXTitle( "Mass Jet matched [GeV]" );

	histos1D_[ "p2DeltaR" ] = fileService->make< TH1D >( "p2DeltaR", "p2DeltaR", 50, 0., 5. );
	histos1D_[ "p2DeltaR" ]->SetXTitle( "min #Delta R( jet, parton)" );
	histos1D_[ "p2JetMass" ] = fileService->make< TH1D >( "p2JetMass", "p2JetMass", 120, 0., 1200. );
	histos1D_[ "p2JetMass" ]->SetXTitle( "Mass Jet matched [GeV]" );

	histos1D_[ "p3DeltaR" ] = fileService->make< TH1D >( "p3DeltaR", "p3DeltaR", 50, 0., 5. );
	histos1D_[ "p3DeltaR" ]->SetXTitle( "min #Delta R( jet, parton)" );
	histos1D_[ "p3JetMass" ] = fileService->make< TH1D >( "p3JetMass", "p3JetMass", 120, 0., 1200. );
	histos1D_[ "p3JetMass" ]->SetXTitle( "Mass Jet matched [GeV]" );
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
