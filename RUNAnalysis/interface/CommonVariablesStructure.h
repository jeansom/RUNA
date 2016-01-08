// system include files
#include <memory>
#include <vector>
#include <TLorentzVector.h>
#include <TVector3.h>
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

// Jet Corrections
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "CondFormats/JetMETObjects/interface/FactorizedJetCorrector.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"

using namespace edm;
using namespace std;



typedef struct Jet_struc {
	TLorentzVector p4;
	TLorentzVector subjet0;
	TLorentzVector subjet1;
	double mass;
	double tau1;
	double tau2;
	double tau3;
	double btagCSV;
	double nhf;
	double nEMf;
	double chf;
	double cEMf;
	int numConst;
	double chm;
} JETtype;

class myJet {
	public:
		TLorentzVector p4;
		TLorentzVector subjet0;
		TLorentzVector subjet1;
		double mass;
		double qgl;
		double tau1;
		double tau2;
		double tau3;
		double btagCSV;
		double nhf;
		double nEMf;
		double chf;
		double cEMf;
		int numConst;
		double chm;
};

inline float massAverage( float m1, float m2 ){ return ( (m1 + m2)/2 ); }

inline float massAsymmetry( float m1, float m2 ){ return abs( ( m1 - m2 )/( m1 + m2 ) ); }

inline float deltaValue( float p1, float p2 ){ return abs( p1 - p2 ); }

inline float calculateCosThetaStar( TLorentzVector jet1, TLorentzVector jet2 ){

	TLorentzVector tmpCM = jet1 + jet2;
	jet1.Boost( -tmpCM.BoostVector() );
	jet2.Boost( -tmpCM.BoostVector() );
	float valueCosThetaStar = TMath::Abs( ( jet1.Px() * tmpCM.Px() +  jet1.Py() * tmpCM.Py() + jet1.Pz() * tmpCM.Pz() ) / (jet1.E() * tmpCM.E() ) ) ;

	return valueCosThetaStar;
}

inline float cosThetaStar( TLorentzVector jet1, TLorentzVector jet2 ){

	TLorentzVector tmpCM = jet1 + jet2;
	TLorentzVector tmpJ1, tmpJ2;
	tmpJ1.SetPtEtaPhiE( jet1.Pt(), jet1.Eta(), jet1.Phi(), jet1.E() );
	tmpJ2.SetPtEtaPhiE( jet2.Pt(), jet2.Eta(), jet2.Phi(), jet2.E() );
	tmpJ1.Boost( -tmpCM.BoostVector() );
	tmpJ2.Boost( -tmpCM.BoostVector() );
	TVector3 tmpV1( tmpJ1.X(), tmpJ1.Y(), tmpJ1.Z() );
	TVector3 tmpV2( tmpJ2.X(), tmpJ2.Y(), tmpJ2.Z() );
	float valueCosThetaStar = TMath::Abs( tmpV1.CosTheta() ) ;

	return valueCosThetaStar;
}

inline bool jetID( double jetEta, double jetE, double jecFactor, double neutralHadronEnergy, double neutralEmEnergy, double chargedHadronEnergy, double muonEnergy, double chargedEmEnergy, int chargedHadronMultiplicity, int neutralHadronMultiplicity, double chargedMultiplicity ){ 

	double jec = 1. / ( jecFactor * jetE );
	double nhf = neutralHadronEnergy * jec;
	double nEMf = neutralEmEnergy * jec;
	double chf = chargedHadronEnergy * jec;
	double muf = muonEnergy * jec;
	double cEMf = chargedEmEnergy * jec;
	int numConst = chargedHadronMultiplicity + neutralHadronMultiplicity ; 
	double chm = chargedMultiplicity * jec;

	//bool idL = ( (nhf<0.99) && (nEMf<0.99) && (muf<0.8) && (cEMf<0.9) );  /// 8TeV recommendation
	//bool id = (nhf<0.99 && nEMf<0.99 && numConst>1) && ((abs(jetEta)<=2.4 && chf>0 && chm>0 && cEMf<0.99) || abs(jetEta)>2.4) && abs(jetEta)<=3.0; // looseJetID 
	//bool id = (nhf<0.90 && nEMf<0.90 && numConst>1) && ((abs(jetEta)<=2.4 && chf>0 && chm>0 && cEMf<0.99) || abs(jetEta)>2.4) && abs(jetEta)<=3.0; // tightJetID 
	bool id = ( nhf<0.90 && nEMf<0.90 && numConst>1 && muf<0.8) && ((abs(jetEta)<=2.4 && chf>0 && chm>0 && cEMf<0.90) || abs(jetEta)>2.4) && abs(jetEta)<=3.0; //tightLepVetoJetID

	return id;
}

inline bool checkTriggerBits( Handle<vector<string>> triggerNames, Handle<vector<float>> triggerBits, TString HLTtrigger  ){

	float triggerFired = 0;
	for (size_t t = 0; t < triggerNames->size(); t++) {
		if ( TString( (*triggerNames)[t] ).Contains( HLTtrigger ) ) {
			triggerFired = (*triggerBits)[t];
			//LogWarning("triggerbit") << (*triggerNames)[t] << " " <<  (*triggerBits)[t];
		}
	}
	if ( HLTtrigger.Contains( "NOTRIGGER" ) ) triggerFired = 1;

	return triggerFired;
}	

inline bool checkORListOfTriggerBits( Handle<vector<string>> triggerNames, Handle<vector<float>> triggerBits, vector<string>  triggerPass  ){

	vector<bool> triggersFired;
	for (size_t t = 0; t < triggerPass.size(); t++) {
		bool triggerFired = checkTriggerBits( triggerNames, triggerBits, triggerPass[t] );
		triggersFired.push_back( triggerFired );
		//if ( triggerFired ) LogWarning("test") << triggerPass[t] << " " << triggerFired;
	}
	
	bool ORTriggers = !none_of(triggersFired.begin(), triggersFired.end(), [](bool v) { return v; }); 
	//if( ORTriggers ) LogWarning("OR") << std::none_of(triggersFired.begin(), triggersFired.end(), [](bool v) { return v; }); 
	
	return ORTriggers;
}

inline double corrections( TLorentzVector rawJet, double jetArea, double Rho, int NPV, FactorizedJetCorrector* jetCorrector ){

	jetCorrector->setJetPt ( rawJet.Pt() );
	jetCorrector->setJetEta( rawJet.Eta() );
	jetCorrector->setJetPhi( rawJet.Phi() );
	jetCorrector->setJetE  ( rawJet.E() );
	jetCorrector->setJetA  ( jetArea );
	jetCorrector->setRho   ( Rho );
	jetCorrector->setNPV   ( NPV );
	double jecFactor= jetCorrector->getCorrection();

	return jecFactor;
}

inline double uncertainty( TLorentzVector rawJet, JetCorrectionUncertainty* jetUnc, bool getUnc ){

	jetUnc->setJetPt ( rawJet.Pt()  );
	jetUnc->setJetEta( rawJet.Eta() );
	double jetUncFactor = jetUnc->getUncertainty( getUnc );
	return jetUncFactor;
}

inline double getJER( double jetEta, int JERType ){

	double scaleNom = 1.0;
	double scaleUnc = 1.0;
	double eta = fabs(jetEta);
	if(eta>=0.0 && eta<0.8) { scaleNom = 1.061; scaleUnc = 0.023; }
	if(eta>=0.8 && eta<1.3) { scaleNom = 1.088; scaleUnc = 0.029; }
	if(eta>=1.3 && eta<1.9) { scaleNom = 1.106; scaleUnc = 0.030; }
	if(eta>=1.9 && eta<2.5) { scaleNom = 1.126; scaleUnc = 0.094; }
	if(eta>=2.5 && eta<3.0) { scaleNom = 1.343; scaleUnc = 0.123; }
	if(eta>=3.0 && eta<3.2) { scaleNom = 1.303; scaleUnc = 0.111; }
	if(eta>=3.2 && eta<5.0) { scaleNom = 1.320; scaleUnc = 0.286; }

	if ( JERType == 0 ) return scaleNom;
	else if ( JERType == 1 ) return (scaleNom + scaleUnc);
	else if ( JERType == -1 ) return (scaleNom - scaleUnc);
	else return 1.;
}

