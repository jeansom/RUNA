// -*- C++ -*-
//
// Package:    RUNA/RUNAnalysis
// Class:      RUNMCAnalysis
// 
/**\class RUNMCAnalysis RUNMCAnalysis.cc RUNA/RUNAnalysis/plugins/RUNMCAnalysis.cc

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

#include "FWCore/Framework/interface/GetterOfProducts.h"
#include "FWCore/Framework/interface/ProcessMatch.h"

using namespace edm;
using namespace std;

//
// constants, enums and typedefs
//
typedef struct Jet_struc {
	TLorentzVector p4;
	TLorentzVector subjet0;
	TLorentzVector subjet1;
	double mass;
	double tau1;
	double tau2;
	double tau3;
	bool btagCSV;
} JETtype;
//
// class declaration
//
class RUNMCAnalysis : public EDAnalyzer {
   public:
      explicit RUNMCAnalysis(const ParameterSet&);
      ~RUNMCAnalysis();

   private:
      virtual void beginJob() override;
      virtual void analyze(const Event&, const EventSetup&) override;
      virtual void endJob() override;

      //virtual void beginRun(Run const&, EventSetup const&) override;
      //virtual void endRun(Run const&, EventSetup const&) override;
      //virtual void beginLuminosityBlock(LuminosityBlock const&, EventSetup const&) override;
      //virtual void endLuminosityBlock(LuminosityBlock const&, EventSetup const&) override;

      // ----------member data ---------------------------
      //GetterOfProducts< vector<float> > getterOfProducts_;
      //EDGetTokenT<TriggerResults> triggerBits_;
      Service<TFileService> fs_;
      //TTree *RUNAtree;
      map< string, TH1D* > histos1D_;
      map< string, TH2D* > histos2D_;
      vector< string > cutLabels;
      map< string, double > cutmap;

      float scale = 1;

      EDGetTokenT<vector<float>> genPt_;
      EDGetTokenT<vector<float>> genEta_;
      EDGetTokenT<vector<float>> genPhi_;
      EDGetTokenT<vector<float>> genE_;
      EDGetTokenT<vector<float>> genMass_;
      EDGetTokenT<vector<float>> genMomID_;
      EDGetTokenT<vector<float>> genID_;
      EDGetTokenT<vector<float>> genStatus_;
      EDGetTokenT<vector<float>> genCharge_;

};

//
// static data member definitions
//

//
// constructors and destructor
//
RUNMCAnalysis::RUNMCAnalysis(const ParameterSet& iConfig):
//	getterOfProducts_(ProcessMatch(*), this) {
//	triggerBits_(consumes<TriggerResults>(iConfig.getParameter<InputTag>("bits"))),
	genPt_(consumes<vector<float>>(iConfig.getParameter<InputTag>("genPt"))),
	genEta_(consumes<vector<float>>(iConfig.getParameter<InputTag>("genEta"))),
	genPhi_(consumes<vector<float>>(iConfig.getParameter<InputTag>("genPhi"))),
	genE_(consumes<vector<float>>(iConfig.getParameter<InputTag>("genE"))),
	genMass_(consumes<vector<float>>(iConfig.getParameter<InputTag>("genMass"))),
	genMomID_(consumes<vector<float>>(iConfig.getParameter<InputTag>("genMomID"))),
	genID_(consumes<vector<float>>(iConfig.getParameter<InputTag>("genID"))),
	genStatus_(consumes<vector<float>>(iConfig.getParameter<InputTag>("genStatus"))),
	genCharge_(consumes<vector<float>>(iConfig.getParameter<InputTag>("genCharge")))
{
}


RUNMCAnalysis::~RUNMCAnalysis()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void RUNMCAnalysis::analyze(const Event& iEvent, const EventSetup& iSetup) {


	/*vector<Handle< vector<float> > > handles;
	getterOfProducts_.fillHandles(event, handles);
	*/

	Handle<vector<float> > genPt;
	iEvent.getByToken(genPt_, genPt);

	Handle<vector<float> > genEta;
	iEvent.getByToken(genEta_, genEta);

	Handle<vector<float> > genPhi;
	iEvent.getByToken(genPhi_, genPhi);

	Handle<vector<float> > genE;
	iEvent.getByToken(genE_, genE);

	Handle<vector<float> > genMass;
	iEvent.getByToken(genMass_, genMass);

	Handle<vector<float> > genMomID;
	iEvent.getByToken(genMomID_, genMomID);

	Handle<vector<float> > genID;
	iEvent.getByToken(genID_, genID);

	Handle<vector<float> > genStatus;
	iEvent.getByToken(genStatus_, genStatus);

	Handle<vector<float> > genCharge;
	iEvent.getByToken(genCharge_, genCharge);


	vector<TLorentzVector> stopParticles, antiStopParticles;
	TLorentzVector stop, antiStop;
	for (size_t i = 0; i < genPt->size(); i++) {

		if ( (*genStatus)[i] == 22 ){
			if ( (*genID)[i] < 0 ) antiStop.SetPtEtaPhiE( (*genPt)[i], (*genEta)[i], (*genPhi)[i], (*genE)[i] );
			else stop.SetPtEtaPhiE( (*genPt)[i], (*genEta)[i], (*genPhi)[i], (*genE)[i] );
		}

		TLorentzVector tmpStopParticle, tmpAntiStopParticle;
		if ( (*genStatus)[i] == 23 ){
			if ( (*genMomID)[i] < 0 ) {
				tmpAntiStopParticle.SetPtEtaPhiE( (*genPt)[i], (*genEta)[i], (*genPhi)[i], (*genE)[i] );
				antiStopParticles.push_back( tmpAntiStopParticle );
			       	//LogWarning("antiStop") << (*genID)[i] << " " << (*genMomID)[i] << " " << (*genStatus)[i] << " " << (*genCharge)[i] << " " << (*genPt)[i];
			} else { 
				tmpStopParticle.SetPtEtaPhiE( (*genPt)[i], (*genEta)[i], (*genPhi)[i], (*genE)[i] );
				stopParticles.push_back( tmpStopParticle );
				//LogWarning("Stop") << (*genID)[i] << " " << (*genMomID)[i] << " " << (*genStatus)[i] << " " << (*genCharge)[i];
			}
		}
	}

	//LogWarning("antiStops") << antiStopParticles.size() << " " << antiStopParticles[0].Pt() ;
	cutmap["Processed"] += 1;
	sort(stopParticles.begin(), stopParticles.end(), [](const TLorentzVector &p1, const TLorentzVector &p2) { return p1.Pt() > p2.Pt(); }); 
	sort(antiStopParticles.begin(), antiStopParticles.end(), [](const TLorentzVector &p1, const TLorentzVector &p2) { return p1.Pt() > p2.Pt(); }); 

	if( ( stopParticles.size() == 2 ) && ( antiStopParticles.size() == 2 ) ){

		//LogWarning("test") << stopParticles[0].Pt() << " " << stopParticles[1].Pt();
		//bool stopKin = ( ( stop.Pt() > 150 ) && ( TMath::Abs( stop.Eta() ) < 2.4 ) );
		//bool antiStopKin = ( ( antiStop.Pt() > 150 ) && ( TMath::Abs( antiStop.Eta() ) < 2.4 ) );
 
		//if ( stopKin && antiStopKin ) {
		double deltaRStop = stopParticles[0].DeltaR( stopParticles[1] );
		double deltaRAntiStop = antiStopParticles[0].DeltaR( antiStopParticles[1] );
		
		/*if( deltaRStop < 0.6 ) {
			double tmpStopMass = ( stopParticles[0] + stopParticles[1] ).M();
			LogWarning("Stop") << deltaRStop << " " <<  stopParticles[0].Pt() << " " << stopParticles[1].Pt() << " " << stop.Pt() << " " << stop.Eta() << " " << tmpStopMass;
		}*/

		if ( ( deltaRStop < 0.7 ) && ( deltaRAntiStop < 0.7 ) ){
			//LogWarning( "Boosted case" ) << deltaRStop << " " << deltaRAntiStop;
			
			TLorentzVector tmpJet1, tmpJet2, tmpCM;
			tmpJet1 = stop;
			tmpJet2 = antiStop;

			tmpCM = tmpJet1 + tmpJet2;
			tmpJet1.Boost( -tmpCM.BoostVector() );
			tmpJet2.Boost( -tmpCM.BoostVector() );
			double cosThetaStar = TMath::Abs( ( tmpJet1.Px() * tmpCM.Px() +  tmpJet1.Py() * tmpCM.Py() + tmpJet1.Pz() * tmpCM.Pz() ) / (tmpJet1.E() * tmpCM.E() ) ) ;

			histos1D_[ "cosThetaStar" ]->Fill( cosThetaStar );
			histos2D_[ "dijetCorr" ]->Fill( stop.Eta(), antiStop.Eta() );
			histos2D_[ "dijetCorrPhi" ]->Fill( stop.Phi(), antiStop.Phi() );

			double stopSubjetPtRatio = min( stopParticles[0].Pt(), stopParticles[1].Pt() ) / max( stopParticles[0].Pt(), stopParticles[1].Pt() );
			double antiStopSubjetPtRatio = min( antiStopParticles[0].Pt(), antiStopParticles[1].Pt() ) / max( antiStopParticles[0].Pt(), antiStopParticles[1].Pt() );
			histos1D_[ "subjetPtRatio" ]->Fill( stopSubjetPtRatio );
			histos1D_[ "subjetPtRatio" ]->Fill( antiStopSubjetPtRatio );

			histos1D_[ "subjetMass21Ratio" ]->Fill( stopParticles[0].M()/stopParticles[1].M() );
			histos1D_[ "subjetMass21Ratio" ]->Fill( antiStopParticles[0].M()/antiStopParticles[1].M() );

			histos1D_[ "subjet112MassRatio" ]->Fill( stopParticles[0].M()/ stop.M() );
			histos1D_[ "subjet112MassRatio" ]->Fill( antiStopParticles[0].M()/ antiStop.M() );

			histos1D_[ "subjet212MassRatio" ]->Fill( stopParticles[1].M()/ stop.M() );
			histos1D_[ "subjet212MassRatio" ]->Fill( antiStopParticles[1].M()/ antiStop.M() );

			histos2D_[ "subjet112vs212MassRatio" ]->Fill( stopParticles[0].M()/ stop.M(), stopParticles[1].M()/ stop.M() );
			histos2D_[ "subjet112vs212MassRatio" ]->Fill( antiStopParticles[0].M()/ antiStop.M(), antiStopParticles[1].M()/ antiStop.M() );

			double m1 = stopParticles[0].M();
			double m2 = stopParticles[1].M();
			double m3 = antiStopParticles[0].M();
			double m4 = antiStopParticles[1].M();
			double m12 = ( stopParticles[0] + stopParticles[1] ).M() ;
			double m34 = ( antiStopParticles[0] + antiStopParticles[1] ).M() ;
			double m134 = ( stopParticles[0] + antiStopParticles[0] + antiStopParticles[1] ).M() ;
			double m123 = ( stopParticles[0] + stopParticles[1] + antiStopParticles[0] ).M() ;
			double m124 = ( stopParticles[0] + stopParticles[1] + antiStopParticles[1] ).M() ;
			double m234 = ( stopParticles[1] + antiStopParticles[0] + antiStopParticles[1] ).M() ;
			double m1234 = ( stopParticles[0] + stopParticles[1] + antiStopParticles[0] + antiStopParticles[1] ).M() ;
			
			double tmpX1 = pow(m1234,2) * ( ( 2 * ( pow(m12,2) + pow(m1,2) ) ) - pow(m2,2) ) ;
			double tmpX2 = pow(m12,2) * ( pow(m134,2) - pow(m34,2) - pow(m1,2) );
			double tmpX3 = pow(m1234,4) - ( pow(m12,2) * pow(m34,2) ) ; 
			double tmpX4 = ( 2 * ( pow(m12,2) + pow(m1,2) ) ) - pow(m2,2);
			double tmpX5 = pow(m12,2) * pow(m1,2);
			double tmpx1 = tmpX1 - (tmpX2/2);
			double tmpx2 = tmpX3 * ( pow(tmpX4,2) - tmpX5 );
			double cosPhi13412 = TMath::Abs( tmpx1 / sqrt( tmpx2 ) );
			histos1D_[ "subjetPolAngle13412" ]->Fill( cosPhi13412 );

			double tmpY1 = pow(m1234,2) * ( ( 2 * ( pow(m34,2) + pow(m3,2) ) ) - pow(m4,2) ) ;
			double tmpY2 = pow(m34,2) * ( pow(m123,2) - pow(m12,2) - pow(m3,2) );
			double tmpY3 = pow(m1234,4) - ( pow(m12,2) * pow(m34,2) ) ; 
			double tmpY4 = ( 2 * ( pow(m34,2) + pow(m3,2) ) ) - pow(m4,2);
			double tmpY5 = pow(m34,2) * pow(m3,2);
			double tmpy1 = tmpY1 - (tmpY2/2);
			double tmpy2 = tmpY3 * ( pow(tmpY4,2) - tmpY5 );
			double cosPhi31234 = TMath::Abs( tmpy1 / sqrt( tmpy2 ) );
			histos1D_[ "subjetPolAngle31234" ]->Fill( cosPhi31234 );
			histos2D_[ "subjetPolAngle13412vs31234" ]->Fill( cosPhi13412, cosPhi31234 );

			vector<double> dalitz1, Dalitz1, dalitz2, Dalitz2;
			double tmptilde = pow( m1, 2 ) + pow( m2, 2) + pow( m34, 2 ) + pow( m1234, 2);
			double mtilde12 = pow( m12, 2 ) / tmptilde;
			double mtilde134 = pow( m134, 2 ) / tmptilde;
			double mtilde234 = pow( m234, 2 ) / tmptilde;
			//double tmpMtilde = pow( mtilde12, 2 ) + pow( mtilde134, 2 ) + pow( mtilde234, 2 );
			//LogWarning("test") << tmpMtilde;
			dalitz1.push_back( pow( mtilde12, 2 ) );
			dalitz1.push_back( pow( mtilde134, 2 ) );
			dalitz1.push_back( pow( mtilde234, 2 ) );
			sort( dalitz1.begin(), dalitz1.end(), [](const double &p1, const double &p2) { return p1 > p2; }); 
			histos1D_[ "mu1" ]->Fill( dalitz1[0] );
			histos1D_[ "mu2" ]->Fill( dalitz1[1] );
			histos1D_[ "mu3" ]->Fill( dalitz1[2] );
			histos2D_[ "mu1234" ]->Fill( dalitz1[0], dalitz1[2] );
			histos2D_[ "mu1234" ]->Fill( dalitz1[1], dalitz1[2] );
			histos2D_[ "mu1234" ]->Fill( dalitz1[0], dalitz1[1] );

			/// (a,b) = (mu1, mu2)
			double dalitzY1 = dalitz1[0];
			double dalitzX1 = ( dalitzY1 / sqrt(3) ) + ( ( 2 / sqrt(3) ) * dalitz1[1] );
			histos2D_[ "dalitz1234" ]->Fill( dalitzY1, dalitzX1 );

			/// (a,b) = (mu1, mu3)
			double dalitzY2 = dalitz1[0];
			double dalitzX2 = ( dalitzY2 / sqrt(3) ) + ( ( 2 / sqrt(3) ) * dalitz1[2] );
			histos2D_[ "dalitz1234" ]->Fill( dalitzY2, dalitzX2 );

			/// (a,b) = (mu2, mu3)
			double dalitzY3 = dalitz1[1];
			double dalitzX3 = ( dalitzY3 / sqrt(3) ) + ( ( 2 / sqrt(3) ) * dalitz1[2] );
			histos2D_[ "dalitz1234" ]->Fill( dalitzY3, dalitzX3 );

			double mtilde34 = pow( m34, 2 ) / tmptilde;
			double mtilde123 = pow( m123, 2 ) / tmptilde;
			double mtilde124 = pow( m124, 2 ) / tmptilde;
			dalitz2.push_back( pow( mtilde34, 2 ) );
			dalitz2.push_back( pow( mtilde123, 2 ) );
			dalitz2.push_back( pow( mtilde124, 2 ) );
			sort( dalitz2.begin(), dalitz2.end(), [](const double &p1, const double &p2) { return p1 > p2; }); 
			histos1D_[ "mu4" ]->Fill( dalitz2[0] );
			histos1D_[ "mu5" ]->Fill( dalitz2[1] );
			histos1D_[ "mu6" ]->Fill( dalitz2[2] );
			histos2D_[ "mu3412" ]->Fill( dalitz2[0], dalitz2[2] );
			histos2D_[ "mu3412" ]->Fill( dalitz2[1], dalitz2[2] );
			histos2D_[ "mu3412" ]->Fill( dalitz2[0], dalitz2[1] );

			/// (a,b) = (mu1, mu2)
			double dalitzY4 = dalitz2[0];
			double dalitzX4 = ( dalitzY4 / sqrt(3) ) + ( ( 2 / sqrt(3) ) * dalitz2[1] );
			histos2D_[ "dalitz3412" ]->Fill( dalitzY4, dalitzX4 );

			/// (a,b) = (mu1, mu3)
			double dalitzY5 = dalitz2[0];
			double dalitzX5 = ( dalitzY5 / sqrt(3) ) + ( ( 2 / sqrt(3) ) * dalitz2[2] );
			histos2D_[ "dalitz3412" ]->Fill( dalitzY5, dalitzX5 );

			/// (a,b) = (mu2, mu3)
			double dalitzY6 = dalitz2[1];
			double dalitzX6 = ( dalitzY6 / sqrt(3) ) + ( ( 2 / sqrt(3) ) * dalitz2[2] );
			histos2D_[ "dalitz3412" ]->Fill( dalitzY6, dalitzX6 );
		}
	}
}


// ------------ method called once each job just before starting event loop  ------------
void RUNMCAnalysis::beginJob() {

	//RUNAtree = fs_->make< TTree >("RUNATree", "RUNATree"); 
	//RUNAtree->Branch( "massAveForFit", &massAveForFit,"massAveForFit/F");

	histos1D_[ "rawJetPt" ] = fs_->make< TH1D >( "rawJetPt", "rawJetPt", 100, 0., 1000. );
	histos1D_[ "rawJetPt" ]->Sumw2();
	histos1D_[ "rawHT" ] = fs_->make< TH1D >( "rawHT", "rawHT", 150, 0., 1500. );
	histos1D_[ "rawHT" ]->Sumw2();

	histos1D_[ "jetPt" ] = fs_->make< TH1D >( "jetPt", "jetPt", 100, 0., 1000. );
	histos1D_[ "jetPt" ]->Sumw2();
	histos1D_[ "jetEta" ] = fs_->make< TH1D >( "jetEta", "jetEta", 100, -5., 5. );
	histos1D_[ "jetEta" ]->Sumw2();
	histos1D_[ "jetNum" ] = fs_->make< TH1D >( "jetNum", "jetNum", 10, 0., 10. );
	histos1D_[ "jetNum" ]->Sumw2();
	histos1D_[ "jetMass" ] = fs_->make< TH1D >( "jetMass", "jetMass", 30, 0., 300. );
	histos1D_[ "jetMass" ]->Sumw2();

	histos1D_[ "cosThetaStar" ] = fs_->make< TH1D >( "cosThetaStar", "cosThetaStar", 20, 0., 1. );
	histos1D_[ "cosThetaStar" ]->Sumw2();
	histos2D_[ "dijetCorr" ] = fs_->make< TH2D >( "dijetCorr", "dijetCorr", 20, -5., 5., 20, -5., 5. );
	histos2D_[ "dijetCorr" ]->Sumw2();
	histos2D_[ "dijetCorrPhi" ] = fs_->make< TH2D >( "dijetCorrPhi", "dijetCorrPhi", 20, -5., 5., 20, -5., 5. );
	histos2D_[ "dijetCorrPhi" ]->Sumw2();
	histos1D_[ "subjetPtRatio" ] = fs_->make< TH1D >( "subjetPtRatio", "subjetPtRatio", 20, 0., 1. );
	histos1D_[ "subjetPtRatio" ]->Sumw2();
	histos1D_[ "subjetMass21Ratio" ] = fs_->make< TH1D >( "subjetMass21Ratio", "subjetMass21Ratio", 100, 0., 5. );
	histos1D_[ "subjetMass21Ratio" ]->Sumw2();
	histos1D_[ "subjet112MassRatio" ] = fs_->make< TH1D >( "subjet112MassRatio", "subjet112MassRatio", 20, 0., 1. );
	histos1D_[ "subjet112MassRatio" ]->Sumw2();
	histos1D_[ "subjet212MassRatio" ] = fs_->make< TH1D >( "subjet212MassRatio", "subjet212MassRatio", 20, 0., 1. );
	histos1D_[ "subjet212MassRatio" ]->Sumw2();
	histos2D_[ "subjet12Mass" ] = fs_->make< TH2D >( "subjet12Mass", "subjet12Mass", 20, 0., 100., 20, 0., 100. );
	histos2D_[ "subjet12Mass" ]->Sumw2();
	histos2D_[ "subjet112vs212MassRatio" ] = fs_->make< TH2D >( "subjet112vs212MassRatio", "subjet112vs212MassRatio", 20, 0., 1., 20, 0., 1. );
	histos2D_[ "subjet112vs212MassRatio" ]->Sumw2();
	histos1D_[ "subjetPolAngle13412" ] = fs_->make< TH1D >( "subjetPolAngle13412", "subjetPolAngle13412", 20, 0., 1. );
	histos1D_[ "subjetPolAngle13412" ]->Sumw2();
	histos1D_[ "subjetPolAngle31234" ] = fs_->make< TH1D >( "subjetPolAngle31234", "subjetPolAngle31234", 20, 0., 1. );
	histos1D_[ "subjetPolAngle31234" ]->Sumw2();
	histos2D_[ "subjetPolAngle13412vs31234" ] = fs_->make< TH2D >( "subjetPolAngle13412vs31234", "subjetPolAngle13412vs31234", 20, 0., 1., 20, 0., 1. );
	histos2D_[ "subjetPolAngle13412vs31234" ]->Sumw2();

	histos1D_[ "mu1" ] = fs_->make< TH1D >( "mu1", "mu1", 40, 0., 1 );
	histos1D_[ "mu1" ]->Sumw2();
	histos1D_[ "mu2" ] = fs_->make< TH1D >( "mu2", "mu2", 40, 0., 1 );
	histos1D_[ "mu2" ]->Sumw2();
	histos1D_[ "mu3" ] = fs_->make< TH1D >( "mu3", "mu3", 40, 0., 1 );
	histos1D_[ "mu3" ]->Sumw2();
	histos2D_[ "mu1234" ] = fs_->make< TH2D >( "mu1234", "mu1234", 40, 0., 1, 40, 0., 1 );
	histos2D_[ "mu1234" ]->Sumw2();
	histos2D_[ "dalitz1234" ] = fs_->make< TH2D >( "dalitz1234", "dalitz1234", 40, 0., 1, 40, 0., 1 );
	histos2D_[ "dalitz1234" ]->Sumw2();
	histos1D_[ "mu4" ] = fs_->make< TH1D >( "mu4", "mu4", 40, 0., 1 );
	histos1D_[ "mu4" ]->Sumw2();
	histos1D_[ "mu5" ] = fs_->make< TH1D >( "mu5", "mu5", 40, 0., 1 );
	histos1D_[ "mu5" ]->Sumw2();
	histos1D_[ "mu6" ] = fs_->make< TH1D >( "mu6", "mu6", 40, 0., 1 );
	histos1D_[ "mu6" ]->Sumw2();
	histos2D_[ "mu3412" ] = fs_->make< TH2D >( "mu3412", "mu3412", 40, 0., 1, 40, 0., 1 );
	histos2D_[ "mu3412" ]->Sumw2();
	histos2D_[ "dalitz3412" ] = fs_->make< TH2D >( "dalitz3412", "dalitz3412", 40, 0., 1, 40, 0., 1 );
	histos2D_[ "dalitz3412" ]->Sumw2();

	cutLabels.push_back("Processed");
	histos1D_[ "hcutflow" ] = fs_->make< TH1D >("cutflow","cut flow", cutLabels.size(), 0.5, cutLabels.size() +0.5 );
	histos1D_[ "hcutflow" ]->Sumw2();
	histos1D_[ "hcutflowSimple" ] = fs_->make< TH1D >("cutflowSimple","simple cut flow", cutLabels.size(), 0.5, cutLabels.size() +0.5 );
	histos1D_[ "hcutflowSimple" ]->Sumw2();
	for( const string &ivec : cutLabels ) cutmap[ ivec ] = 0;
}

// ------------ method called once each job just after ending the event loop  ------------
void RUNMCAnalysis::endJob() {

	int ibin = 1;
	for( const string &ivec : cutLabels ) {
		histos1D_["hcutflow"]->SetBinContent( ibin, cutmap[ ivec ] * scale );
		histos1D_["hcutflow"]->GetXaxis()->SetBinLabel( ibin, ivec.c_str() );
		histos1D_["hcutflowSimple"]->SetBinContent( ibin, cutmap[ ivec ] );
		histos1D_["hcutflowSimple"]->GetXaxis()->SetBinLabel( ibin, ivec.c_str() );
		ibin++;
	}

}


//define this as a plug-in
DEFINE_FWK_MODULE(RUNMCAnalysis);
