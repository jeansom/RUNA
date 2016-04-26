// system include files
#include <memory>
#include <vector>
#include <TLorentzVector.h>
#include <TVector3.h>
#include <TH1.h>
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

#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"

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
		double subjet0BtagCSVv2;
		double subjet0BtagCMVAv2;
		TLorentzVector subjet1;
		double subjet1BtagCSVv2;
		double subjet1BtagCMVAv2;
		double mass;
		double trimmedMass;
		double prunedMass;
		double filteredMass;
		double softDropMass;
		double qgl;
		double tau1;
		double tau2;
		double tau3;
		double btagCSVv2;
		double btagCMVAv2;
		double btagDoubleB;
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

inline bool checkTriggerBitsMiniAOD( TriggerNames triggerNames, Handle<TriggerResults> triggerBits, TString HLTtrigger  ){

  	bool triggerFired = 0;
	for (unsigned int i = 0, n = triggerBits->size(); i < n; ++i) {
		if (TString(triggerNames.triggerName(i)).Contains(HLTtrigger) && (triggerBits->accept(i))) {
		       	triggerFired=1;
			//LogWarning("test") << "Trigger " << triggerNames.triggerName(i) << ": " << (triggerBits->accept(i) ? "PASS" : "fail (or not run)") ;
		}
	}

	return triggerFired;
}	

inline bool checkORListOfTriggerBitsMiniAOD( TriggerNames triggerNames, Handle<TriggerResults> triggerBits, vector<string>  triggerPass  ){

	vector<bool> triggersFired;
	for (size_t t = 0; t < triggerPass.size(); t++) {
		bool triggerFired = checkTriggerBitsMiniAOD( triggerNames, triggerBits, triggerPass[t] );
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

// all this section is based on https://github.com/jkarancs/B2GTTrees/blob/master/plugins/B2GEdmExtraVarProducer.cc#L215-L281
inline void getWeights( Handle<LHEEventProduct> lheEvtInfo, int lha_pdf_id_, vector<float> & scaleWeights, vector<float> & pdfWeights, vector<float> & alphaWeights ){

	/* Renormalization/Factorization scale weights
	 * These are the first 9 weights for all generators
	 * mu_R and mu_F are varied independently (by a factor of 1, 2, 0.5) - check LHE header
	 * [0] is the default weight (no variation) - it has worse precision even
	 * --> I skip saving it (one can just use 1)
	 * --> Also do not save unphysical combinations as recommended
	 * (mu_R = 0.5, mu_F = 2 and mu_R = 2, mu_F = 0.5)
	 * Save only: 1,2,3,4,6,8
	 */
	double lheOrigWeight = lheEvtInfo->originalXWGTUP();
	vector <gen::WeightsInfo> weightsTemp = lheEvtInfo->weights();
	if ( weightsTemp.size()>=9) for (size_t i=0; i<9; ++i) if (i!=0&&i!=5&&i!=7) scaleWeights.push_back( weightsTemp[i].wgt/lheOrigWeight);

	/* PDF weights
	 * Usually a set of 100 weights (excluding default)
	 * Only default PDF variation is saved, but if needed
	 * likely others are available depending on the generator
	 * index of first weight varies, beware!
	 * Sometimes first weight is default=1 weight (has to skip!)
	 * Additional info: MC2Hessian conversion will soon be provided
	 */
	size_t first = 9;
	// Madgraph nf5 - have to skip 1 weight which is default
	if (lha_pdf_id_ == 263000) first = 10;
	// Madgraph nf4 uses NNPDF30_lo_as_0130_nf_4 (ID=263400)
	// Which is the second 101 pdf set, again has to skip first weight
	if (lha_pdf_id_ == 263400) first = 111;
	if (weightsTemp.size()>=first+100) for (size_t i=first; i<first+100; ++i) pdfWeights.push_back(weightsTemp[i].wgt/lheOrigWeight);

	/* Alpha_s weights (only for NLO!)
	 * A set of two weights for 
	 * alpha_s = 0.118 - 0.002 and
	 * alpha_s = 0.118 + 0.002
	 * is given --> scale result uncertainty by 0.75
	 */
	if ( weightsTemp.size()>=111 &&
	    ( (lha_pdf_id_ == 260000) || // Powheg 5nf
	     (lha_pdf_id_ == 260400) || // Powheg 4nf 
	     (lha_pdf_id_ == 292000) || // aMC@NLO 5nf
	     (lha_pdf_id_ == 292200)    // aMC@NLO 5nf
	     ) ) {
		alphaWeights.push_back(weightsTemp[109].wgt/lheOrigWeight);
		alphaWeights.push_back(weightsTemp[110].wgt/lheOrigWeight);
	}
}
