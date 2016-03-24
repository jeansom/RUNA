// -*- C++ -*-
//
// Package:    RUNA/RUNtuples
// Class:      GenInfo
// 
/**\class GenInfo GenInfo.cc RUNA/RUNtuples/plugins/GenInfo.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  alejandro gomez
//         Created:  Tue, 21 Oct 2014 16:25:53 GMT
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

//
// class declaration
//

class GenInfo : public edm::EDProducer {
   public:
      explicit GenInfo(const edm::ParameterSet&);
      ~GenInfo();

   private:
      virtual void produce(edm::Event&, const edm::EventSetup&) override;
      
      // ----------member data ---------------------------
      edm::EDGetTokenT<reco::GenParticleCollection> src_;
      typedef std::vector<float> floatCollection;
      typedef std::vector<int> intCollection;
      
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
GenInfo::GenInfo(const edm::ParameterSet& iConfig):
	src_(consumes<reco::GenParticleCollection>(iConfig.getParameter<edm::InputTag>("src")))
{
	produces< floatCollection >( "genpt" ).setBranchAlias( "genPt" );
	produces< floatCollection >( "geneta" ).setBranchAlias( "genEta" );
	produces< floatCollection >( "genphi" ).setBranchAlias( "genPhi" );
	produces< floatCollection >( "genmass" ).setBranchAlias( "genMass" );
	produces< intCollection >( "gencharge" ).setBranchAlias( "genCharge" );
	produces< intCollection >( "gendummyindex" ).setBranchAlias( "genDummyIndex" );
	produces< intCollection >( "genstatus" ).setBranchAlias( "genStatus" );
	produces< intCollection >( "genmother" ).setBranchAlias( "genMother" );
	produces< intCollection >( "gennummother" ).setBranchAlias( "genNumMother" );
	produces< intCollection >( "gennumdaughter" ).setBranchAlias( "genNumDaughter" );
  
}


GenInfo::~GenInfo()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
GenInfo::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
	using namespace edm;
	using namespace reco; 
	using namespace std;

	// create the vectors. Use auto_ptr, as these pointers will automatically
	// delete when they go out of scope, a very efficient way to reduce memory leaks.
	auto_ptr<floatCollection> genPt( new floatCollection() );
	auto_ptr<floatCollection> genEta( new floatCollection() );
	auto_ptr<floatCollection> genPhi( new floatCollection() );
	auto_ptr<floatCollection> genMass( new floatCollection() );
	auto_ptr<intCollection> genCharge( new intCollection() );
	auto_ptr<intCollection> genDummyIndex( new intCollection() );
	auto_ptr<intCollection> genMother( new intCollection() );
	auto_ptr<intCollection> genStatus( new intCollection() );
	auto_ptr<intCollection> genNumMother( new intCollection() );
	auto_ptr<intCollection> genNumDaughter( new intCollection() );

	Handle<reco::GenParticleCollection> particles;
	iEvent.getByToken( src_ , particles );

	// and already reserve some space for the new data, to control the size
	// of your executible's memory use.
	const int particleSize = particles->size();
	genPt->reserve( particleSize );
	genEta->reserve( particleSize );
	genPhi->reserve( particleSize );
	genCharge->reserve( particleSize );
	genStatus->reserve( particleSize );
	genNumMother->reserve( particleSize );
	genNumDaughter->reserve( particleSize );
	genDummyIndex->reserve( particleSize );

	int index = 0;
	for ( const reco::GenParticle &p : *particles){
		index++;

		genPt->push_back( p.pt() );
		genPt->push_back( p.mass() );
		genEta->push_back( p.eta() );
		genPhi->push_back( p.phi() );
		genCharge->push_back( p.charge() );
		genNumMother->push_back( p.numberOfMothers() );
		genNumDaughter->push_back( p.numberOfDaughters() );
		genDummyIndex->push_back( index );

		const Candidate * mom = p.mother();
		if( mom ) genMother->push_back( mom->pdgId() );
		else genMother->push_back( 0 );

		genStatus->push_back( p.status() );
	}

	// and save the vectors
	iEvent.put( genPt, "genpt" );
	iEvent.put( genEta, "geneta" );
	iEvent.put( genPhi, "genphi" );
	iEvent.put( genMass, "genmass" );
	iEvent.put( genCharge, "gencharge" );
	iEvent.put( genDummyIndex, "gendummyindex" );
	iEvent.put( genStatus, "genstatus" );
	iEvent.put( genMother, "genmother" );
	iEvent.put( genNumMother, "gennummother" );
	iEvent.put( genNumDaughter, "gennumdaughter" );
 
}


//define this as a plug-in
DEFINE_FWK_MODULE(GenInfo);
