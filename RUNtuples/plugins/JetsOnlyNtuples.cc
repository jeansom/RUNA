// -*- C++ -*-
//
// Package:    JetsOnlyNtuples/JetsOnlyNtuples
// Class:      JetsOnlyNtuples
// 
/**\class JetsOnlyNtuples JetsOnlyNtuples.cc JetsOnlyNtuples/JetsOnlyNtuples/plugins/JetsOnlyNtuples.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  alejandro gomez
//         Created:  Fri, 03 Oct 2014 18:17:41 GMT
//
//


// system include files
#include <memory>
#include <vector>
#include <iostream>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
//#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"

#include "TTree.h"
//
// class declaration
//

class JetsOnlyNtuples : public edm::EDProducer {
   public:
      explicit JetsOnlyNtuples(const edm::ParameterSet&);
      ~JetsOnlyNtuples();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      void initialize();
      virtual void beginJob() override;
      virtual void produce(edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      //virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
      //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

      // ----------member data ---------------------------
      edm::EDGetTokenT<reco::VertexCollection> vtxToken_;
      edm::EDGetTokenT<pat::JetCollection> jetToken_;
      edm::EDGetTokenT<pat::JetCollection> fatjetToken_;

      typedef std::vector<float> jetFloatCollection;
      typedef std::vector<int> jetIntCollection;
      typedef std::vector<bool> jetBoolCollection;

      edm::Service<TFileService> fs_;
      TTree *outTree_; 
      std::vector<float> *pt_;
      //jetFloatCollection *pt_;
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
JetsOnlyNtuples::JetsOnlyNtuples(const edm::ParameterSet& iConfig):
	vtxToken_(consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("vertices"))),
	jetToken_(consumes<pat::JetCollection>(iConfig.getParameter<edm::InputTag>("jets"))),
	fatjetToken_(consumes<pat::JetCollection>(iConfig.getParameter<edm::InputTag>("fatjets")))
{
	produces< jetFloatCollection >( "jetsPt" ).setBranchAlias( "jPt" );
//	produces< jetFloatCollection >( "jPt" ).setBranchAlias( "jPt" );
//	produces< jetFloatCollection >( "jPt" ).setBranchAlias( "jPt" );
}


JetsOnlyNtuples::~JetsOnlyNtuples()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void JetsOnlyNtuples::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {

	using namespace edm;
	using namespace reco; 
	using namespace std;

	initialize();
	// create the vectors. Use auto_ptr, as these pointers will automatically
	// delete when they go out of scope, a very efficient way to reduce memory leaks.
	auto_ptr<jetFloatCollection> jPt( new jetFloatCollection() );

	
	edm::Handle<reco::VertexCollection> vertices;
	iEvent.getByToken(vtxToken_, vertices);
	if (vertices->empty()) return; // skip the event if no PV found
	//const reco::Vertex &PV = vertices->front();

	edm::Handle<pat::JetCollection> jets;
	iEvent.getByToken(jetToken_, jets);

	// and already reserve some space for the new data, to control the size
	// of your executible's memory use.
	const int jetSize = jets->size();
	jPt->reserve( jetSize );

	//int ijet = 0;
	for (const pat::Jet &j : *jets) {

		double chf 	= j.chargedHadronEnergyFraction();
		double nhf 	= j.neutralHadronEnergyFraction() + j.HFHadronEnergyFraction();
		double phf 	= j.photonEnergy()/(j.jecFactor(0) * j.energy());
		double elf 	= j.electronEnergy()/(j.jecFactor(0) * j.energy());
		int chm    	= j.chargedHadronMultiplicity();
		int npr    	= j.chargedMultiplicity() + j.neutralMultiplicity(); 
		double muf 	= j.muonEnergy()/(j.jecFactor(0) * j.energy());
		float eta  	= fabs(j.eta());
		float pt   	= j.pt();
		//double area 	= j.jetArea();
		bool idL   	= (npr>1 && phf<0.99 && nhf<0.99);
		bool idT   	= (idL && ((eta<=2.4 && nhf<0.9 && phf<0.9 && elf<0.99 && muf<0.99 && chf>0 && chm>0) || eta>2.4));

		if (idT && pt > 40.0 && eta < 2.4 ) {
			jPt->push_back( pt );
			pt_->push_back( pt );
		//	ht += pt;
			/*chf_           ->push_back(chf);
			nhf_           ->push_back(nhf);
			phf_           ->push_back(phf);
			elf_           ->push_back(elf);
			muf_           ->push_back(muf);
			area_          ->push_back(area);
			jec_           ->push_back(1./ijet->jecFactor(0));
			pt_            ->push_back(pt);
			phi_           ->push_back(ijet->phi());
			eta_           ->push_back(ijet->eta());
			mass_          ->push_back(ijet->mass());
			energy_        ->push_back(ijet->energy());
			tau1_          ->push_back(ijet->userFloat("tau1"));
			tau2_          ->push_back(ijet->userFloat("tau2"));
			tau3_          ->push_back(ijet->userFloat("tau3"));*/
		//	nJets_++;
		}

        /*if (j.pt() < 20) continue;
        printf("jet  with pt %5.1f (raw pt %5.1f), eta %+4.2f, btag CSV %.3f, CISV %.3f, pileup mva disc %+.2f\n",
            j.pt(), j.pt()*j.jecFactor("Uncorrected"), j.eta(), std::max(0.f,j.bDiscriminator("combinedSecondaryVertexBJetTags")), std::max(0.f,j.bDiscriminator("combinedInclusiveSecondaryVertexBJetTags")), j.userFloat("pileupJetId:fullDiscriminant"));
        if ((++ijet) == 1) { // for the first jet, let's print the leading constituents
            std::vector<reco::CandidatePtr> daus(j.daughterPtrVector());
            std::sort(daus.begin(), daus.end(), [](const reco::CandidatePtr &p1, const reco::CandidatePtr &p2) { return p1->pt() > p2->pt(); }); // the joys of C++11
            for (unsigned int i2 = 0, n = daus.size(); i2 < n && i2 <= 3; ++i2) {
                const pat::PackedCandidate &cand = dynamic_cast<const pat::PackedCandidate &>(*daus[i2]);
                printf("         constituent %3d: pt %6.2f, dz(pv) %+.3f, pdgId %+3d\n", i2,cand.pt(),cand.dz(PV.position()),cand.pdgId());
            }
        }*/
    	}


    /*edm::Handle<pat::JetCollection> fatjets;
    iEvent.getByToken(fatjetToken_, fatjets);
    for (const pat::Jet &j : *fatjets) {
        printf("AK8j with pt %5.1f (raw pt %5.1f), eta %+4.2f, mass %5.1f ungroomed, %5.1f pruned, %5.1f Modpruned, %5.1f trimmed, %5.1f filtered. CMS TopTagger %.1f, Tau1 %5.1f\n",
            j.pt(), j.pt()*j.jecFactor("Uncorrected"), j.eta(), j.mass(), j.userFloat("ak8PFJetsCHSPrunedLinks"), j.userFloat("ak8PFJetsCHSPrunedModLinks"), j.userFloat("ak8PFJetsCHSTrimmedLinks"), j.userFloat("ak8PFJetsCHSFilteredLinks"), j.userFloat("cmsTopTagPFJetsCHSLinksAK8"), j.userFloat("NjettinessAK8:tau1"));
    }*/
 

	// and save the vectors
	iEvent.put( jPt, "jetsPt" );
	outTree_->Fill();     
}


// ------------ method called once each job just before starting event loop  ------------
void 
JetsOnlyNtuples::beginJob()
{
	outTree_ = fs_->make<TTree>("events","events");
	pt_             = new std::vector<float>;
	outTree_->Branch("jetPt"                ,"vector<float>"     ,&pt_);
}

// ------------ method called once each job just after ending the event loop  ------------
void 
JetsOnlyNtuples::endJob() 
{
	delete pt_;
}

void JetsOnlyNtuples::initialize(){
	pt_ ->clear();
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
JetsOnlyNtuples::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(JetsOnlyNtuples);
