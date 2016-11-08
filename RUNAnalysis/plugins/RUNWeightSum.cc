// -*- C++ -*-
//
// Package:    Ntuples/Ntuples
// Class:      RUNWeightSum
// 
/**\class RUNWeightSum RUNWeightSum.cc Ntuples/Ntuples/plugins/RUNWeightSum.cc

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
#include <TH1D.h>
#include <TH2D.h>
#include <TTree.h>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/LHERunInfoProduct.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/LorentzVector.h"

#include "RUNA/RUNAnalysis/interface/CommonVariablesStructure.h"
#include "RUNA/RUNAnalysis/interface/PUReweighter.h"

using namespace edm;
using namespace std;

//
// constants, enums and typedefs
//

//
// class declaration
//
class RUNWeightSum : public EDAnalyzer {
   public:
      explicit RUNWeightSum(const ParameterSet&);
      static void fillDescriptions(edm::ConfigurationDescriptions & descriptions);
      ~RUNWeightSum();

   private:
      virtual void beginJob() override;
      virtual void analyze(const Event&, const EventSetup&) override;
      virtual void endJob() override;
      //virtual void beginRun(const Run&, const EventSetup&) override;

      //virtual void endRun(Run const&, EventSetup const&) override;
      //virtual void beginLuminosityBlock(LuminosityBlock const&, EventSetup const&) override;
      //virtual void endLuminosityBlock(LuminosityBlock const&, EventSetup const&) override;

      // ----------member data ---------------------------
      int lhaPdfId ;
      
      Service<TFileService> fs_;
      TTree *RUNAtree;
      map< string, TH1D* > histos1D_;
      map< string, TH2D* > histos2D_;

      bool bjSample;
      bool isData;
      double scale;
      string dataPUFile;
      string jecVersion;
      TString systematics;

      double sumWeights = 0;

      EDGetTokenT<GenEventInfoProduct> generator_;
      EDGetTokenT<LHEEventProduct> extLHEProducer_;

};

//
// static data member definitions
//

//
// constructors and destructor
//
RUNWeightSum::RUNWeightSum(const ParameterSet& iConfig):
	generator_(consumes<GenEventInfoProduct>(iConfig.getParameter<InputTag>("generator")))
{
	consumes<LHERunInfoProduct,edm::InRun> (edm::InputTag("externalLHEProducer"));
}


RUNWeightSum::~RUNWeightSum()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void RUNWeightSum::analyze(const Event& iEvent, const EventSetup& iSetup) {

	// all this section is based on https://github.com/jkarancs/B2GTTrees/blob/master/plugins/B2GEdmExtraVarProducer.cc#L215-L281
	/////////// GEN weight
	Handle<GenEventInfoProduct> genEvtInfo; 
	iEvent.getByToken( generator_, genEvtInfo );
	double genWeight = genEvtInfo->weight();	
	sumWeights += genWeight;
	//vector<double> evtWeights = genEvtInfo->weights();
	//LogWarning("Event") << genWeight << " " << sumWeights;

}


// ------------ method called once each job just before starting event loop  ------------
void RUNWeightSum::beginJob() {

}

// ------------ method called once each job just after ending the event loop  ------------
void RUNWeightSum::endJob() {

	LogWarning("Total") << sumWeights;

}

void RUNWeightSum::fillDescriptions(edm::ConfigurationDescriptions & descriptions) {

	edm::ParameterSetDescription desc;

	desc.add<InputTag>("generator", 	InputTag("generator"));
	desc.add<InputTag>("extLHEProducer", 	InputTag("externalLHEProducer"));
}
      

//define this as a plug-in
DEFINE_FWK_MODULE(RUNWeightSum);
