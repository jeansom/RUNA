// -*- C++ -*-
//
// Package:    SimAnalyzer
// Class:      SimAnalyzer
// 
/**\class SimAnalyzer SimAnalyzer.cc UserCode/SimAnalyzer/src/SimAnalyzer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Alejandro Gomez
//         Created:  Mon May 20 14:38:03 CDT 2013
// $Id: SimAnalyzer.cc,v 1.2 2013/06/19 02:42:01 algomez Exp $
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
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"

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



template<class Jet>
class SimAnalyzer : public edm::EDAnalyzer {
	public:
		explicit SimAnalyzer(const edm::ParameterSet&);
		static void fillDescriptions(edm::ConfigurationDescriptions & descriptions);
		~SimAnalyzer();

		
	private:
		virtual void beginJob() ;
		virtual void analyze(const edm::Event&, const edm::EventSetup&);
		virtual void endJob() ;

	// ----------member data ---------------------------
	typedef std::vector<Jet> JetCollection;
      	edm::Service<TFileService> fs_;
      	map< string, TH1D* > histos1D_;
	map< string, TH2D* > histos2D_;

	double momPdgId_;
	double dau1PdgId_;
	double dau2PdgId_;
	double dauDeltaR_;
	double minPt_;
      	EDGetTokenT<reco::GenJetCollection> genJets_;
      	EDGetTokenT<vector<reco::GenParticle>> genParticles_;
      	EDGetTokenT<JetCollection> recoJets_;

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
template<class Jet>
SimAnalyzer<Jet>::SimAnalyzer(const edm::ParameterSet& iConfig) :
	genJets_(consumes<reco::GenJetCollection>(iConfig.getParameter<InputTag>("genJets"))),
	genParticles_(consumes<vector<reco::GenParticle>>(iConfig.getParameter<InputTag>("genParticles"))),
	recoJets_(consumes<JetCollection>(iConfig.getParameter<InputTag>("recoJets")))
{
	momPdgId_	= iConfig.getParameter<double>("momPdgId");
	dau1PdgId_	= iConfig.getParameter<double>("dau1PdgId");
	dau2PdgId_	= iConfig.getParameter<double>("dau2PdgId");
	dauDeltaR_	= iConfig.getParameter<double>("dauDeltaR");
	minPt_		= iConfig.getParameter<double>("minPt");
}


template<class Jet>
SimAnalyzer<Jet>::~SimAnalyzer()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to for each event  ------------
template<class Jet>
void SimAnalyzer<Jet>::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup){

	using namespace std;
	using namespace edm;
	using namespace reco;

	Handle<reco::GenJetCollection> genJets;
	iEvent.getByToken(genJets_, genJets);

	Handle<std::vector<reco::GenParticle>> particles;
	iEvent.getByToken(genParticles_, particles);

	Handle<JetCollection> recoJets;
	iEvent.getByToken(recoJets_, recoJets);

	// Reading genParticle info and saving mothers and daughters info
	TLorentzVector momPar1, momPar2;				
	vector<TLorentzVector> dauPar1, dauPar2;
	int dumm = 0;
	for(const reco::GenParticle &p : *particles ) {

		if( !p.mother() ) continue;

		// Saving mothers
		if ( p.status() == 22 ) {
			if ( p.pdgId() ==  momPdgId_ ) {
				momPar1.SetPtEtaPhiE( p.pt(), p.eta(), p.phi(), p.energy()  );
				histos1D_[ "mom_Pt" ]->Fill( momPar1.Pt() );
				histos1D_[ "mom_Mass" ]->Fill( momPar1.M() );
			}
		        if ( p.pdgId() == - momPdgId_ ) {
				momPar2.SetPtEtaPhiE( p.pt(), p.eta(), p.phi(), p.energy()  );
				histos1D_[ "mom_Pt" ]->Fill( momPar2.Pt() );
				histos1D_[ "mom_Mass" ]->Fill( momPar2.M() );
			} 
		}
		
		// Saving daughters
		TLorentzVector tmp;
		if ( p.status() == 23 ) {
			dumm++;
			if( abs( p.mother()->pdgId() ) == momPdgId_ ) {

				if ( ( p.pdgId() == dau1PdgId_ ) || ( p.pdgId() == dau2PdgId_ )  ) {
					tmp.SetPtEtaPhiE( p.pt(), p.eta(), p.phi(), p.energy() );
					dauPar2.push_back( tmp );
					//LogWarning("GenParticles") << p.pdgId() << " " << p.status() << " 3 or 1 ";
				} else if ( ( p.pdgId() == -dau1PdgId_ ) || ( p.pdgId() == -dau2PdgId_ )  ) {
					tmp.SetPtEtaPhiE( p.pt(), p.eta(), p.phi(), p.energy() );
					dauPar1.push_back( tmp );
					//LogWarning("GenParticles") << p.pdgId() << " " << p.status() << " -3 or -1 ";
				}
			}
		} 
	}
	histos1D_[ "numFinalParticles" ]->Fill( dumm );

	// Reconstruct mothers
	TLorentzVector tmpFromMom1, tmpFromMom2;
	vector<TLorentzVector> boostedDaughters, resolvedDaughters;
	if ( dauPar1.size() == 2 ) {
		tmpFromMom1 = ( dauPar1[0] + dauPar1[1] );
		histos1D_[ "momFromDau_Pt" ]->Fill( tmpFromMom1.Pt() );
		histos1D_[ "momFromDau_Mass" ]->Fill( tmpFromMom1.M() );
		double tmpDeltaR = dauPar1[0].DeltaR( dauPar1[0] );
		histos1D_[ "dauDeltaR" ]->Fill( tmpDeltaR );
		if ( tmpDeltaR < dauDeltaR_ ) {
			boostedDaughters.push_back( dauPar1[0] );
			boostedDaughters.push_back( dauPar1[1] );
		} else {
			resolvedDaughters.push_back( dauPar1[0] );
			resolvedDaughters.push_back( dauPar1[1] );
		}

		if ( ( tmpFromMom1.M() - momPar1.M() ) < 5 ){
			histos1D_[ "dau_Pt" ]->Fill( dauPar1[0].Pt() );
			histos1D_[ "dau_Pt" ]->Fill( dauPar1[1].Pt() );
			histos1D_[ "dau_Eta" ]->Fill( dauPar1[0].Eta() );
			histos1D_[ "dau_Eta" ]->Fill( dauPar1[1].Eta() );
		}
	} else LogWarning("GenParticles") << "This event have more than 2 quarks with 23 status. " << dauPar1.size();

	if ( dauPar2.size() == 2 ) {
		tmpFromMom2 = ( dauPar2[0] + dauPar2[1] );
		histos1D_[ "momFromDau_Pt" ]->Fill( tmpFromMom2.Pt() );
		histos1D_[ "momFromDau_Mass" ]->Fill( tmpFromMom2.M() );
		double tmpDeltaR = dauPar2[0].DeltaR( dauPar2[1] );
		histos1D_[ "dauDeltaR" ]->Fill( tmpDeltaR );
		if ( tmpDeltaR < dauDeltaR_ ) {
			boostedDaughters.push_back( dauPar2[0] );
			boostedDaughters.push_back( dauPar2[1] );
		} else {
			resolvedDaughters.push_back( dauPar2[0] );
			resolvedDaughters.push_back( dauPar2[1] );
		}

		if ( ( tmpFromMom2.M() - momPar2.M() ) < 5 ){
			histos1D_[ "dau_Pt" ]->Fill( dauPar2[0].Pt() );
			histos1D_[ "dau_Pt" ]->Fill( dauPar2[1].Pt() );
			histos1D_[ "dau_Eta" ]->Fill( dauPar2[0].Eta() );
			histos1D_[ "dau_Eta" ]->Fill( dauPar2[1].Eta() );
		}
	} else LogWarning("GenParticles") << "This event have more than 2 quarks with 23 status.";

	// genJets plots
	float rawGenHT = 0;
	int numRawGenJets = 0;
	float genHT = 0;
	int numGenJets = 0;
	vector<TLorentzVector> selGenJets;
    	for (const reco::GenJet &genJet : *genJets) {
		numRawGenJets += 1;
		rawGenHT += genJet.pt();
		histos1D_[ "genRawJetPt" ]->Fill( genJet.pt() );
		histos1D_[ "genRawJetEta" ]->Fill( genJet.eta() );
		histos1D_[ "genRawJetMass" ]->Fill( genJet.mass() );

		if( TMath::Abs( genJet.eta() ) > 2.5 ) continue;
		if( genJet.pt() < minPt_ ) continue;
		TLorentzVector tmpSelJet;
		tmpSelJet.SetPtEtaPhiE( genJet.pt(), genJet.eta(), genJet.phi(), genJet.energy() );
		selGenJets.push_back( tmpSelJet );
		
		numGenJets += 1;	
		if ( numGenJets==1) {
			histos1D_[ "genJet1Pt" ]->Fill( genJet.pt() );
			histos1D_[ "genJet1Eta" ]->Fill( genJet.eta() );
			histos1D_[ "genJet1Mass" ]->Fill( genJet.mass() );
		}
		genHT += genJet.pt();
		histos1D_[ "genJetPt" ]->Fill( genJet.pt() );
		histos1D_[ "genJetEta" ]->Fill( genJet.eta() );
		histos1D_[ "genJetMass" ]->Fill( genJet.mass() );

	}
	if( rawGenHT > 0 ) histos1D_[ "rawGenHT" ]->Fill( rawGenHT );
	if( genHT > 0 ) histos1D_[ "genHT" ]->Fill( genHT );
	histos1D_[ "rawNumGenJets" ]->Fill( numRawGenJets );
	histos1D_[ "numGenJets" ]->Fill( numGenJets );
	if( ( rawGenHT > 0 ) && ( genHT > 0 ) ) histos2D_[ "rawGenHTvsgenHT" ]->Fill( rawGenHT, genHT );

	// recoJets plots
	float rawRecoHT = 0;
	int numRawRecoJets = 0;
	float recoHT = 0;
	int numRecoJets = 0;
	vector<TLorentzVector> selRecoJets;
    	//for (const reco::PFJet &recoJet : *recoJets) {
    	for (const Jet &recoJet : *recoJets) {
		numRawRecoJets += 1;
		rawRecoHT += recoJet.pt();
		histos1D_[ "recoRawJetPt" ]->Fill( recoJet.pt() );
		histos1D_[ "recoRawJetEta" ]->Fill( recoJet.eta() );
		histos1D_[ "recoRawJetMass" ]->Fill( recoJet.mass() );

		if( TMath::Abs( recoJet.eta() ) > 2.5 ) continue;
		if( recoJet.pt() < minPt_ ) continue;
		TLorentzVector tmpSelRecoJet;
		tmpSelRecoJet.SetPtEtaPhiE( recoJet.pt(), recoJet.eta(), recoJet.phi(), recoJet.energy() );
		selRecoJets.push_back( tmpSelRecoJet );
		
		numRecoJets += 1;	
		if ( numRecoJets==1) {
			histos1D_[ "recoJet1Pt" ]->Fill( recoJet.pt() );
			histos1D_[ "recoJet1Eta" ]->Fill( recoJet.eta() );
			histos1D_[ "recoJet1Mass" ]->Fill( recoJet.mass() );
		}
		recoHT += recoJet.pt();
		histos1D_[ "recoJetPt" ]->Fill( recoJet.pt() );
		histos1D_[ "recoJetEta" ]->Fill( recoJet.eta() );
		histos1D_[ "recoJetMass" ]->Fill( recoJet.mass() );
	}
	if( rawRecoHT > 0 ) histos1D_[ "rawRecoHT" ]->Fill( rawRecoHT );
	if( recoHT > 0 ) histos1D_[ "recoHT" ]->Fill( recoHT );
	histos1D_[ "rawNumRecoJets" ]->Fill( numRawRecoJets );
	histos1D_[ "numRecoJets" ]->Fill( numRecoJets );
	if( ( rawRecoHT > 0 ) && ( recoHT > 0 ) ) histos2D_[ "rawRecoHTvsrecoHT" ]->Fill( rawRecoHT, recoHT );

	/// Matching GenJets
	double tmpMinGenDeltaR = 999;
	double tmp2MinGenDeltaR = 999;
	//double tmp3MinGenDeltaR = 999;
	//double tmp4MinGenDeltaR = 999;
	int numBoostedGenJets = 0;
	vector<TLorentzVector> boostedGenJets;
	if ( boostedDaughters.size() > 1 ){
		for( const TLorentzVector &selGenJet : selGenJets ){ 
			double tmpMatch = selGenJet.DeltaR( boostedDaughters[0] );
			if ( tmpMatch < tmpMinGenDeltaR ) {
				tmpMinGenDeltaR = tmpMatch;
				double tmp2Match = selGenJet.DeltaR( boostedDaughters[1] );
				if ( ( tmpMatch < dauDeltaR_ ) && ( tmp2Match < dauDeltaR_ ) ){
					boostedGenJets.push_back( selGenJet );
					numBoostedGenJets++;
				}
			} 

			if ( boostedDaughters.size() > 3 ){
				double tmp3Match = selGenJet.DeltaR( boostedDaughters[2] );
				if ( tmp3Match < tmp2MinGenDeltaR ) {
					tmp2MinGenDeltaR = tmp3Match;
					double tmp4Match = selGenJet.DeltaR( boostedDaughters[3] );
					if ( ( tmp3Match < dauDeltaR_ ) && ( tmp4Match < dauDeltaR_ ) ){
						boostedGenJets.push_back( selGenJet );
						numBoostedGenJets++;
					}
				} 
			}
		}
	}
	histos1D_[ "numBoostedGenJets" ]->Fill( numBoostedGenJets );
	if ( boostedGenJets.size() > 0 ) {
		histos1D_[ "boostedGenJetPt" ]->Fill( boostedGenJets[0].Pt() );
		histos1D_[ "boostedGenJetMass" ]->Fill( boostedGenJets[0].M() );
		if ( boostedGenJets.size() > 1 ) {
			histos1D_[ "boostedGenJetPt" ]->Fill( boostedGenJets[1].Pt() );
			histos1D_[ "boostedGenJetMass" ]->Fill( boostedGenJets[1].M() );
		}
	}

	double tmpMinGenResolvedDeltaR = 999;
	double tmp2MinGenResolvedDeltaR = 999;
	double tmp3MinGenResolvedDeltaR = 999;
	double tmp4MinGenResolvedDeltaR = 999;
	TLorentzVector tmpResolvedGenJets1, tmpResolvedGenJets2, tmpResolvedGenJets3, tmpResolvedGenJets4;
	vector<TLorentzVector> resolvedGenJets;
	if ( resolvedDaughters.size() > 1 ){
		for( const TLorentzVector &selGenJet : selGenJets ){ 
			double tmpMatch = selGenJet.DeltaR( resolvedDaughters[0] );
			if ( tmpMatch < tmpMinGenResolvedDeltaR ) {
				tmpMinGenResolvedDeltaR = tmpMatch;
				tmpResolvedGenJets1 = selGenJet;
			} 
			double tmp2Match = selGenJet.DeltaR( resolvedDaughters[1] );
			if ( tmp2Match < tmp2MinGenResolvedDeltaR ) {
				tmp2MinGenResolvedDeltaR = tmp2Match;
				tmpResolvedGenJets2 = selGenJet;
			} 

			if ( resolvedDaughters.size() > 3 ){
				double tmp3Match = selGenJet.DeltaR( resolvedDaughters[2] );
				if ( tmp3Match < tmp3MinGenResolvedDeltaR ) {
					tmp3MinGenResolvedDeltaR = tmp3Match;
					tmpResolvedGenJets3 = selGenJet;
				} 
				double tmp4Match = selGenJet.DeltaR( resolvedDaughters[3] );
				if ( tmp4Match < tmp4MinGenResolvedDeltaR ) {
					tmp4MinGenResolvedDeltaR = tmp4Match;
					tmpResolvedGenJets4 = selGenJet;
				} 
			}
		}
	}
	if ( ( tmpResolvedGenJets1.Pt() != tmpResolvedGenJets2.Pt() ) && ( tmpResolvedGenJets1.Pt() > 0 ) && ( tmpResolvedGenJets2.Pt() > 0 ) ) {
		TLorentzVector resolvedJets1 = tmpResolvedGenJets1 + tmpResolvedGenJets2;
		histos1D_[ "resolvedGenJetPt" ]->Fill( resolvedJets1.Pt() );
		histos1D_[ "resolvedGenJetMass" ]->Fill( resolvedJets1.M() );
	}
	if ( ( tmpResolvedGenJets3.Pt() != tmpResolvedGenJets4.Pt() ) && ( tmpResolvedGenJets3.Pt() > 0 ) && ( tmpResolvedGenJets4.Pt() > 0 ) ) {
		TLorentzVector resolvedJets2 = tmpResolvedGenJets3 + tmpResolvedGenJets4;
		histos1D_[ "resolvedGenJetPt" ]->Fill( resolvedJets2.Pt() );
		histos1D_[ "resolvedGenJetMass" ]->Fill( resolvedJets2.M() );
	}

	/// Matching RecoJets
	double tmpMinRecoDeltaR = 999;
	double tmp2MinRecoDeltaR = 999;
	int numBoostedRecoJets = 0;
	vector<TLorentzVector> boostedRecoJets;
	if ( boostedDaughters.size() > 1 ){
		for( const TLorentzVector &selRecoJet : selRecoJets ){ 
			double tmpMatch = selRecoJet.DeltaR( boostedDaughters[0] );
			if ( tmpMatch < tmpMinRecoDeltaR ) {
				tmpMinRecoDeltaR = tmpMatch;
				double tmp2Match = selRecoJet.DeltaR( boostedDaughters[1] );
				if ( ( tmpMatch < dauDeltaR_ ) && ( tmp2Match < dauDeltaR_ ) ){
					boostedRecoJets.push_back( selRecoJet );
					numBoostedRecoJets++;
				}
			} 
			if ( boostedDaughters.size() > 3 ){
				double tmp3Match = selRecoJet.DeltaR( boostedDaughters[2] );
				if ( tmp3Match < tmp2MinRecoDeltaR ) {
					tmp2MinRecoDeltaR = tmp3Match;
					double tmp4Match = selRecoJet.DeltaR( boostedDaughters[3] );
					if ( ( tmp3Match < dauDeltaR_ ) && ( tmp4Match < dauDeltaR_ ) ){
						boostedRecoJets.push_back( selRecoJet );
						numBoostedRecoJets++;
					}
				} 
			}
		}
	}
	histos1D_[ "numBoostedRecoJets" ]->Fill( numBoostedRecoJets );
	if ( boostedRecoJets.size() > 0 ) {
		histos1D_[ "boostedRecoJetPt" ]->Fill( boostedRecoJets[0].Pt() );
		histos1D_[ "boostedRecoJetMass" ]->Fill( boostedRecoJets[0].M() );
		if ( boostedRecoJets.size() > 1 ) {
			histos1D_[ "boostedRecoJetPt" ]->Fill( boostedRecoJets[1].Pt() );
			histos1D_[ "boostedRecoJetMass" ]->Fill( boostedRecoJets[1].M() );
		}
	}

	double tmpMinRecoResolvedDeltaR = 999;
	double tmp2MinRecoResolvedDeltaR = 999;
	double tmp3MinRecoResolvedDeltaR = 999;
	double tmp4MinRecoResolvedDeltaR = 999;
	TLorentzVector tmpResolvedRecoJets1, tmpResolvedRecoJets2, tmpResolvedRecoJets3, tmpResolvedRecoJets4;
	vector<TLorentzVector> resolvedRecoJets;
	if ( resolvedDaughters.size() > 1 ){
		for( const TLorentzVector &selRecoJet : selRecoJets ){ 
			double tmpMatch = selRecoJet.DeltaR( resolvedDaughters[0] );
			if ( tmpMatch < tmpMinRecoResolvedDeltaR ) {
				tmpMinRecoResolvedDeltaR = tmpMatch;
				tmpResolvedRecoJets1 = selRecoJet;
			} 
			double tmp2Match = selRecoJet.DeltaR( resolvedDaughters[1] );
			if ( tmp2Match < tmp2MinRecoResolvedDeltaR ) {
				tmp2MinRecoResolvedDeltaR = tmp2Match;
				tmpResolvedRecoJets2 = selRecoJet;
			} 

			if ( resolvedDaughters.size() > 3 ){
				double tmp3Match = selRecoJet.DeltaR( resolvedDaughters[2] );
				if ( tmp3Match < tmp3MinRecoResolvedDeltaR ) {
					tmp3MinRecoResolvedDeltaR = tmp3Match;
					tmpResolvedRecoJets3 = selRecoJet;
				} 
				double tmp4Match = selRecoJet.DeltaR( resolvedDaughters[3] );
				if ( tmp4Match < tmp4MinRecoResolvedDeltaR ) {
					tmp4MinRecoResolvedDeltaR = tmp4Match;
					tmpResolvedRecoJets4 = selRecoJet;
				} 
			}
		}
	}
	if ( ( tmpResolvedRecoJets1.Pt() != tmpResolvedRecoJets2.Pt() ) && ( tmpResolvedRecoJets1.Pt() > 0 ) && ( tmpResolvedRecoJets2.Pt() > 0 ) ) {
		TLorentzVector resolvedJets1 = tmpResolvedRecoJets1 + tmpResolvedRecoJets2;
		histos1D_[ "resolvedRecoJetPt" ]->Fill( resolvedJets1.Pt() );
		histos1D_[ "resolvedRecoJetMass" ]->Fill( resolvedJets1.M() );
	}
	if ( ( tmpResolvedRecoJets3.Pt() != tmpResolvedRecoJets4.Pt() ) && ( tmpResolvedRecoJets3.Pt() > 0 ) && ( tmpResolvedRecoJets4.Pt() > 0 ) ) {
		TLorentzVector resolvedJets2 = tmpResolvedRecoJets3 + tmpResolvedRecoJets4;
		histos1D_[ "resolvedRecoJetPt" ]->Fill( resolvedJets2.Pt() );
		histos1D_[ "resolvedRecoJetMass" ]->Fill( resolvedJets2.M() );
	}
}

// ------------ method called once each job just after ending the event loop  ------------
template<class Jet>
void SimAnalyzer<Jet>::beginJob() {

	histos1D_[ "mom_Pt" ] = fs_->make< TH1D >( "mom_Pt", "mom_Pt", 100, 0., 1000. );
	histos1D_[ "mom_Pt" ]->Sumw2();
	histos1D_[ "mom_Mass" ] = fs_->make< TH1D >( "mom_Mass", "mom_Mass", 100, 0., 1000. );
	histos1D_[ "mom_Mass" ]->Sumw2();
	histos1D_[ "numFinalParticles" ] = fs_->make< TH1D >( "numFinalParticles", "numFinalParticles", 10, 0., 10. );
	histos1D_[ "numFinalParticles" ]->Sumw2();
	histos1D_[ "momFromDau_Pt" ] = fs_->make< TH1D >( "momFromDau_Pt", "momFromDau_Pt", 100, 0., 1000. );
	histos1D_[ "momFromDau_Pt" ]->Sumw2();
	histos1D_[ "momFromDau_Mass" ] = fs_->make< TH1D >( "momFromDau_Mass", "momFromDau_Mass", 100, 0., 1000. );
	histos1D_[ "momFromDau_Mass" ]->Sumw2();
	histos1D_[ "dau_Pt" ] = fs_->make< TH1D >( "dau_Pt", "dau_Pt", 100, 0., 1000. );
	histos1D_[ "dau_Pt" ]->Sumw2();
	histos1D_[ "dau_Eta" ] = fs_->make< TH1D >( "dau_Eta", "dau_Eta", 40, -5., 5. );
	histos1D_[ "dau_Eta" ]->Sumw2();
	histos1D_[ "dauDeltaR" ] = fs_->make< TH1D >( "dauDeltaR", "dauDeltaR", 40, 0., 5. );
	histos1D_[ "dauDeltaR" ]->Sumw2();
	
	histos1D_[ "genRawJetPt" ] = fs_->make< TH1D >( "genRawJetPt", "genRawJetPt", 100, 0., 1000. );
	histos1D_[ "genRawJetPt" ]->Sumw2();
	histos1D_[ "genRawJetEta" ] = fs_->make< TH1D >( "genRawJetEta", "genRawJetEta", 24, -3., 3. );
	histos1D_[ "genRawJetEta" ]->Sumw2();
	histos1D_[ "genRawJetMass" ] = fs_->make< TH1D >( "genRawJetMass", "genRawJetMass", 50, 0., 500. );
	histos1D_[ "genRawJetMass" ]->Sumw2();
	histos1D_[ "rawGenHT" ] = fs_->make< TH1D >( "rawGenHT", "rawGenHT", 150, 0., 1500. );
	histos1D_[ "rawGenHT" ]->Sumw2();
	histos1D_[ "rawNumGenJets" ] = fs_->make< TH1D >( "rawNumGenJets", "rawNumGenJets", 15, 0., 15. );
	histos1D_[ "rawNumGenJets" ]->Sumw2();
	histos1D_[ "genJet1Pt" ] = fs_->make< TH1D >( "genJet1Pt", "genJet1Pt", 100, 0., 1000. );
	histos1D_[ "genJet1Pt" ]->Sumw2();
	histos1D_[ "genJet1Eta" ] = fs_->make< TH1D >( "genJet1Eta", "genJet1Eta", 24, -3., 3. );
	histos1D_[ "genJet1Eta" ]->Sumw2();
	histos1D_[ "genJet1Mass" ] = fs_->make< TH1D >( "genJet1Mass", "genJet1Mass", 50, 0., 500. );
	histos1D_[ "genJet1Mass" ]->Sumw2();
	histos1D_[ "genJetPt" ] = fs_->make< TH1D >( "genJetPt", "genJetPt", 100, 0., 1000. );
	histos1D_[ "genJetPt" ]->Sumw2();
	histos1D_[ "genJetEta" ] = fs_->make< TH1D >( "genJetEta", "genJetEta", 24, -3., 3. );
	histos1D_[ "genJetEta" ]->Sumw2();
	histos1D_[ "genJetMass" ] = fs_->make< TH1D >( "genJetMass", "genJetMass", 50, 0., 500. );
	histos1D_[ "genJetMass" ]->Sumw2();
	histos1D_[ "genHT" ] = fs_->make< TH1D >( "genHT", "genHT", 150, 0., 1500. );
	histos1D_[ "genHT" ]->Sumw2();
	histos1D_[ "numGenJets" ] = fs_->make< TH1D >( "numGenJets", "numGenJets", 15, 0., 15. );
	histos1D_[ "numGenJets" ]->Sumw2();

	histos2D_[ "rawGenHTvsgenHT" ] = fs_->make< TH2D >( "rawGenHTvsgenHT", "rawGenHTvsgenHT", 150, 0., 1500., 150, 0., 1500. );
	histos2D_[ "rawGenHTvsgenHT" ]->Sumw2();

	histos1D_[ "recoRawJetPt" ] = fs_->make< TH1D >( "recoRawJetPt", "recoRawJetPt", 100, 0., 1000. );
	histos1D_[ "recoRawJetPt" ]->Sumw2();
	histos1D_[ "recoRawJetEta" ] = fs_->make< TH1D >( "recoRawJetEta", "recoRawJetEta", 24, -3., 3. );
	histos1D_[ "recoRawJetEta" ]->Sumw2();
	histos1D_[ "recoRawJetMass" ] = fs_->make< TH1D >( "recoRawJetMass", "recoRawJetMass", 50, 0., 500. );
	histos1D_[ "recoRawJetMass" ]->Sumw2();
	histos1D_[ "rawRecoHT" ] = fs_->make< TH1D >( "rawRecoHT", "rawRecoHT", 150, 0., 1500. );
	histos1D_[ "rawRecoHT" ]->Sumw2();
	histos1D_[ "rawNumRecoJets" ] = fs_->make< TH1D >( "rawNumRecoJets", "rawNumRecoJets", 15, 0., 15. );
	histos1D_[ "rawNumRecoJets" ]->Sumw2();
	histos1D_[ "recoJet1Pt" ] = fs_->make< TH1D >( "recoJet1Pt", "recoJet1Pt", 100, 0., 1000. );
	histos1D_[ "recoJet1Pt" ]->Sumw2();
	histos1D_[ "recoJet1Eta" ] = fs_->make< TH1D >( "recoJet1Eta", "recoJet1Eta", 24, -3., 3. );
	histos1D_[ "recoJet1Eta" ]->Sumw2();
	histos1D_[ "recoJet1Mass" ] = fs_->make< TH1D >( "recoJet1Mass", "recoJet1Mass", 50, 0., 500. );
	histos1D_[ "recoJet1Mass" ]->Sumw2();
	histos1D_[ "recoJetPt" ] = fs_->make< TH1D >( "recoJetPt", "recoJetPt", 100, 0., 1000. );
	histos1D_[ "recoJetPt" ]->Sumw2();
	histos1D_[ "recoJetEta" ] = fs_->make< TH1D >( "recoJetEta", "recoJetEta", 24, -3., 3. );
	histos1D_[ "recoJetEta" ]->Sumw2();
	histos1D_[ "recoJetMass" ] = fs_->make< TH1D >( "recoJetMass", "recoJetMass", 50, 0., 500. );
	histos1D_[ "recoJetMass" ]->Sumw2();
	histos1D_[ "recoHT" ] = fs_->make< TH1D >( "recoHT", "recoHT", 150, 0., 1500. );
	histos1D_[ "recoHT" ]->Sumw2();
	histos1D_[ "numRecoJets" ] = fs_->make< TH1D >( "numRecoJets", "numRecoJets", 15, 0., 15. );
	histos1D_[ "numRecoJets" ]->Sumw2();

	histos2D_[ "rawRecoHTvsrecoHT" ] = fs_->make< TH2D >( "rawRecoHTvsrecoHT", "rawRecoHTvsrecoHT", 150, 0., 1500., 150, 0., 1500. );
	histos2D_[ "rawRecoHTvsrecoHT" ]->Sumw2();

	histos1D_[ "boostedGenJetMass" ] = fs_->make< TH1D >( "boostedGenJetMass", "boostedGenJetMass", 50, 0., 500. );
	histos1D_[ "boostedGenJetMass" ]->Sumw2();
	histos1D_[ "boostedGenJetPt" ] = fs_->make< TH1D >( "boostedGenJetPt", "boostedGenJetPt", 100, 0., 1000. );
	histos1D_[ "boostedGenJetPt" ]->Sumw2();
	histos1D_[ "numBoostedGenJets" ] = fs_->make< TH1D >( "numBoostedGenJets", "numBoostedGenJets", 15, 0., 15. );
	histos1D_[ "numBoostedGenJets" ]->Sumw2();

	histos1D_[ "boostedRecoJetMass" ] = fs_->make< TH1D >( "boostedRecoJetMass", "boostedRecoJetMass", 50, 0., 500. );
	histos1D_[ "boostedRecoJetMass" ]->Sumw2();
	histos1D_[ "boostedRecoJetPt" ] = fs_->make< TH1D >( "boostedRecoJetPt", "boostedRecoJetPt", 100, 0., 1000. );
	histos1D_[ "boostedRecoJetPt" ]->Sumw2();
	histos1D_[ "numBoostedRecoJets" ] = fs_->make< TH1D >( "numBoostedRecoJets", "numBoostedRecoJets", 15, 0., 15. );
	histos1D_[ "numBoostedRecoJets" ]->Sumw2();

	histos1D_[ "resolvedGenJetMass" ] = fs_->make< TH1D >( "resolvedGenJetMass", "resolvedGenJetMass", 50, 0., 500. );
	histos1D_[ "resolvedGenJetMass" ]->Sumw2();
	histos1D_[ "resolvedGenJetPt" ] = fs_->make< TH1D >( "resolvedGenJetPt", "resolvedGenJetPt", 100, 0., 1000. );
	histos1D_[ "resolvedGenJetPt" ]->Sumw2();

	histos1D_[ "resolvedRecoJetMass" ] = fs_->make< TH1D >( "resolvedRecoJetMass", "resolvedRecoJetMass", 50, 0., 500. );
	histos1D_[ "resolvedRecoJetMass" ]->Sumw2();
	histos1D_[ "resolvedRecoJetPt" ] = fs_->make< TH1D >( "resolvedRecoJetPt", "resolvedRecoJetPt", 100, 0., 1000. );
	histos1D_[ "resolvedRecoJetPt" ]->Sumw2();
}

template<class Jet>
void SimAnalyzer<Jet>::endJob() {
}


template<class Jet>
void SimAnalyzer<Jet>::fillDescriptions(edm::ConfigurationDescriptions & descriptions) {

	ParameterSetDescription desc;
	desc.add<InputTag>("genJets", 	InputTag("ak4GenJetsNoNu"));
	desc.add<InputTag>("genParticles", 	InputTag("genParticles"));
	desc.add<InputTag>("recoJets", 	InputTag("ak4PFJetsCHS"));
	desc.add<double>("momPdgId", 1000006);
	desc.add<double>("dau1PdgId", 1);
	desc.add<double>("dau2PdgId", 3);
	desc.add<double>("dauDeltaR", 0.4);
	desc.add<double>("minPt", 50.);
	descriptions.addDefault(desc);

}

//define this as a plug-in
typedef SimAnalyzer<reco::PFJet> SimAnalyzerAOD;
DEFINE_FWK_MODULE(SimAnalyzerAOD);

typedef SimAnalyzer<pat::Jet> SimAnalyzerMiniAOD;
DEFINE_FWK_MODULE(SimAnalyzerMiniAOD);
