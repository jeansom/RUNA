// -*- C++ -*-
//
// Package:    GenAnalyzer
// Class:      GenAnalyzer
// 
/**\class GenAnalyzer GenAnalyzer.cc UserCode/GenAnalyzer/src/GenAnalyzer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Alejandro Gomez
//         Created:  Mon May 20 14:38:03 CDT 2013
// $Id: GenAnalyzer.cc,v 1.2 2013/06/19 02:42:01 algomez Exp $
//
//


// system include files
#include <memory>
#include <vector>
#include <TH2.h>
#include <TH1D.h>
#include <TH2D.h>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/JetReco/interface/GenJet.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Math/interface/LorentzVector.h"
#include "TLorentzVector.h"
//
// class declaration
//

using namespace edm;
using namespace std;


class GenAnalyzer : public edm::EDAnalyzer {
	public:
		explicit GenAnalyzer(const edm::ParameterSet&);
		~GenAnalyzer();

		
	private:
		virtual void beginJob() ;
		virtual void analyze(const edm::Event&, const edm::EventSetup&);
		virtual void endJob() ;

	// ----------member data ---------------------------
      	edm::Service<TFileService> fs_;
      	map< string, TH1D* > histos1D_;
	map< string, TH2D* > histos2D_;

      	EDGetTokenT<reco::GenJetCollection> genAK4Jets_;
      	EDGetTokenT<reco::GenJetCollection> genAK8Jets_;

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
GenAnalyzer::GenAnalyzer(const edm::ParameterSet& iConfig) :
	genAK4Jets_(consumes<reco::GenJetCollection>(iConfig.getParameter<InputTag>("genAK4Jets"))),
	genAK8Jets_(consumes<reco::GenJetCollection>(iConfig.getParameter<InputTag>("genAK8Jets")))
{

}


GenAnalyzer::~GenAnalyzer()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to for each event  ------------
void GenAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup){

	using namespace std;
	using namespace edm;
	using namespace reco;

	Handle<reco::GenJetCollection> genAK4Jets;
	iEvent.getByToken(genAK4Jets_, genAK4Jets);

	Handle<reco::GenJetCollection> genAK8Jets;
	iEvent.getByToken(genAK8Jets_, genAK8Jets);

	float rawAK4HT = 0;
	int numRawAK4Jets = 0;
	float AK4HT = 0;
	int numAK4Jets = 0;
    	for (const reco::GenJet &genAK4Jet : *genAK4Jets) {
		numRawAK4Jets += 1;
		rawAK4HT += genAK4Jet.pt();
		histos1D_[ "genRawAK4JetPt" ]->Fill( genAK4Jet.pt() );
		histos1D_[ "genRawAK4JetEta" ]->Fill( genAK4Jet.eta() );
		histos1D_[ "genRawAK4JetMass" ]->Fill( genAK4Jet.mass() );

		if( TMath::Abs( genAK4Jet.eta() ) > 2.5 ) continue;
		if( genAK4Jet.pt() < 50 ) continue;
		
		numAK4Jets += 1;	
		if ( numAK4Jets==1) {
			histos1D_[ "genAK4Jet1Pt" ]->Fill( genAK4Jet.pt() );
			histos1D_[ "genAK4Jet1Eta" ]->Fill( genAK4Jet.eta() );
			histos1D_[ "genAK4Jet1Mass" ]->Fill( genAK4Jet.mass() );
		}
		AK4HT += genAK4Jet.pt();
		histos1D_[ "genAK4JetPt" ]->Fill( genAK4Jet.pt() );
		histos1D_[ "genAK4JetEta" ]->Fill( genAK4Jet.eta() );
		histos1D_[ "genAK4JetMass" ]->Fill( genAK4Jet.mass() );
	}
	if( rawAK4HT > 0 ) histos1D_[ "rawAK4HT" ]->Fill( rawAK4HT );
	if( AK4HT > 0 ) histos1D_[ "AK4HT" ]->Fill( AK4HT );
	histos1D_[ "rawNumAK4Jets" ]->Fill( numRawAK4Jets );
	histos1D_[ "NumAK4Jets" ]->Fill( numAK4Jets );

	float rawAK8HT = 0;
	int numRawAK8Jets = 0;
	float AK8HT = 0;
	int numAK8Jets = 0;
    	for (const reco::GenJet &genAK8Jet : *genAK8Jets) {
		numRawAK8Jets += 1;
		rawAK8HT += genAK8Jet.pt();
		histos1D_[ "genRawAK8JetPt" ]->Fill( genAK8Jet.pt() );
		histos1D_[ "genRawAK8JetEta" ]->Fill( genAK8Jet.eta() );
		histos1D_[ "genRawAK8JetMass" ]->Fill( genAK8Jet.mass() );

		if( TMath::Abs( genAK8Jet.eta() ) > 2.5 ) continue;
		if( genAK8Jet.pt() < 150 ) continue;
		
		numAK8Jets += 1;	
		if ( numAK8Jets==1) {
			histos1D_[ "genAK8Jet1Pt" ]->Fill( genAK8Jet.pt() );
			histos1D_[ "genAK8Jet1Eta" ]->Fill( genAK8Jet.eta() );
			histos1D_[ "genAK8Jet1Mass" ]->Fill( genAK8Jet.mass() );
		}
		AK8HT += genAK8Jet.pt();
		histos1D_[ "genAK8JetPt" ]->Fill( genAK8Jet.pt() );
		histos1D_[ "genAK8JetEta" ]->Fill( genAK8Jet.eta() );
		histos1D_[ "genAK8JetMass" ]->Fill( genAK8Jet.mass() );
	}
	if( rawAK8HT > 0 ) histos1D_[ "rawAK8HT" ]->Fill( rawAK8HT );
	if( AK8HT > 0 ) histos1D_[ "AK8HT" ]->Fill( AK8HT );
	histos1D_[ "rawNumAK8Jets" ]->Fill( numRawAK8Jets );
	histos1D_[ "NumAK8Jets" ]->Fill( numAK8Jets );


	if( ( rawAK4HT > 0 ) && ( AK4HT > 0 ) ) histos2D_[ "rawAK4HTvsAK4HT" ]->Fill( rawAK4HT, AK4HT );
	if( ( rawAK8HT > 0 ) && ( AK8HT > 0 ) ) histos2D_[ "rawAK8HTvsAK8HT" ]->Fill( rawAK8HT, AK8HT );

}

// ------------ method called once each job just after ending the event loop  ------------
void GenAnalyzer::beginJob() {
	
	histos1D_[ "genRawAK4JetPt" ] = fs_->make< TH1D >( "genRawAK4JetPt", "genRawAK4JetPt", 100, 0., 1000. );
	histos1D_[ "genRawAK4JetPt" ]->Sumw2();
	histos1D_[ "genRawAK4JetEta" ] = fs_->make< TH1D >( "genRawAK4JetEta", "genRawAK4JetEta", 24, -3., 3. );
	histos1D_[ "genRawAK4JetEta" ]->Sumw2();
	histos1D_[ "genRawAK4JetMass" ] = fs_->make< TH1D >( "genRawAK4JetMass", "genRawAK4JetMass", 50, 0., 500. );
	histos1D_[ "genRawAK4JetMass" ]->Sumw2();
	histos1D_[ "rawAK4HT" ] = fs_->make< TH1D >( "rawAK4HT", "rawAK4HT", 150, 0., 1500. );
	histos1D_[ "rawAK4HT" ]->Sumw2();
	histos1D_[ "rawNumAK4Jets" ] = fs_->make< TH1D >( "rawNumAK4Jets", "rawNumAK4Jets", 15, 0., 15. );
	histos1D_[ "rawNumAK4Jets" ]->Sumw2();
	histos1D_[ "genAK4Jet1Pt" ] = fs_->make< TH1D >( "genAK4Jet1Pt", "genAK4Jet1Pt", 100, 0., 1000. );
	histos1D_[ "genAK4Jet1Pt" ]->Sumw2();
	histos1D_[ "genAK4Jet1Eta" ] = fs_->make< TH1D >( "genAK4Jet1Eta", "genAK4Jet1Eta", 24, -3., 3. );
	histos1D_[ "genAK4Jet1Eta" ]->Sumw2();
	histos1D_[ "genAK4Jet1Mass" ] = fs_->make< TH1D >( "genAK4Jet1Mass", "genAK4Jet1Mass", 50, 0., 500. );
	histos1D_[ "genAK4Jet1Mass" ]->Sumw2();
	histos1D_[ "genAK4JetPt" ] = fs_->make< TH1D >( "genAK4JetPt", "genAK4JetPt", 100, 0., 1000. );
	histos1D_[ "genAK4JetPt" ]->Sumw2();
	histos1D_[ "genAK4JetEta" ] = fs_->make< TH1D >( "genAK4JetEta", "genAK4JetEta", 24, -3., 3. );
	histos1D_[ "genAK4JetEta" ]->Sumw2();
	histos1D_[ "genAK4JetMass" ] = fs_->make< TH1D >( "genAK4JetMass", "genAK4JetMass", 50, 0., 500. );
	histos1D_[ "genAK4JetMass" ]->Sumw2();
	histos1D_[ "AK4HT" ] = fs_->make< TH1D >( "AK4HT", "AK4HT", 150, 0., 1500. );
	histos1D_[ "AK4HT" ]->Sumw2();
	histos1D_[ "NumAK4Jets" ] = fs_->make< TH1D >( "NumAK4Jets", "NumAK4Jets", 15, 0., 15. );
	histos1D_[ "NumAK4Jets" ]->Sumw2();

	histos1D_[ "genRawAK8JetPt" ] = fs_->make< TH1D >( "genRawAK8JetPt", "genRawAK8JetPt", 100, 0., 1000. );
	histos1D_[ "genRawAK8JetPt" ]->Sumw2();
	histos1D_[ "genRawAK8JetEta" ] = fs_->make< TH1D >( "genRawAK8JetEta", "genRawAK8JetEta", 24, -3., 3. );
	histos1D_[ "genRawAK8JetEta" ]->Sumw2();
	histos1D_[ "genRawAK8JetMass" ] = fs_->make< TH1D >( "genRawAK8JetMass", "genRawAK8JetMass", 50, 0., 500. );
	histos1D_[ "genRawAK8JetMass" ]->Sumw2();
	histos1D_[ "rawAK8HT" ] = fs_->make< TH1D >( "rawAK8HT", "rawAK8HT", 150, 0., 1500. );
	histos1D_[ "rawAK8HT" ]->Sumw2();
	histos1D_[ "rawNumAK8Jets" ] = fs_->make< TH1D >( "rawNumAK8Jets", "rawNumAK8Jets", 15, 0., 15. );
	histos1D_[ "rawNumAK8Jets" ]->Sumw2();
	histos1D_[ "genAK8Jet1Pt" ] = fs_->make< TH1D >( "genAK8Jet1Pt", "genAK8Jet1Pt", 100, 0., 1000. );
	histos1D_[ "genAK8Jet1Pt" ]->Sumw2();
	histos1D_[ "genAK8Jet1Eta" ] = fs_->make< TH1D >( "genAK8Jet1Eta", "genAK8Jet1Eta", 24, -3., 3. );
	histos1D_[ "genAK8Jet1Eta" ]->Sumw2();
	histos1D_[ "genAK8Jet1Mass" ] = fs_->make< TH1D >( "genAK8Jet1Mass", "genAK8Jet1Mass", 50, 0., 500. );
	histos1D_[ "genAK8Jet1Mass" ]->Sumw2();
	histos1D_[ "genAK8JetPt" ] = fs_->make< TH1D >( "genAK8JetPt", "genAK8JetPt", 100, 0., 1000. );
	histos1D_[ "genAK8JetPt" ]->Sumw2();
	histos1D_[ "genAK8JetEta" ] = fs_->make< TH1D >( "genAK8JetEta", "genAK8JetEta", 24, -3., 3. );
	histos1D_[ "genAK8JetEta" ]->Sumw2();
	histos1D_[ "genAK8JetMass" ] = fs_->make< TH1D >( "genAK8JetMass", "genAK8JetMass", 50, 0., 500. );
	histos1D_[ "genAK8JetMass" ]->Sumw2();
	histos1D_[ "AK8HT" ] = fs_->make< TH1D >( "AK8HT", "AK8HT", 150, 0., 1500. );
	histos1D_[ "AK8HT" ]->Sumw2();
	histos1D_[ "NumAK8Jets" ] = fs_->make< TH1D >( "NumAK8Jets", "NumAK8Jets", 15, 0., 15. );
	histos1D_[ "NumAK8Jets" ]->Sumw2();

	histos2D_[ "rawAK4HTvsAK4HT" ] = fs_->make< TH2D >( "rawAK4HTvsAK4HT", "rawAK4HTvsAK4HT", 150, 0., 1500., 150, 0., 1500. );
	histos2D_[ "rawAK4HTvsAK4HT" ]->Sumw2();
	histos2D_[ "rawAK8HTvsAK8HT" ] = fs_->make< TH2D >( "rawAK8HTvsAK8HT", "rawAK8HTvsAK8HT", 150, 0., 1500., 150, 0., 1500. );
	histos2D_[ "rawAK8HTvsAK8HT" ]->Sumw2();
}
void 
GenAnalyzer::endJob() {

}

//define this as a plug-in
DEFINE_FWK_MODULE(GenAnalyzer);
