// system include files
#include <memory>
#include <TH1D.h>
#include <TH2D.h>
#include <TH1F.h>
#include <TFile.h>
#include <TLorentzVector.h>
#include <vector>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"

#include "CondFormats/BTauObjects/interface/BTagCalibration.h"
#include "CondTools/BTau/interface/BTagCalibrationReader.h"
#include "CondFormats/BTauObjects/src/BTagCalibration.cc"
#include "CondTools/BTau/src/BTagCalibrationReader.cc"

#include "CondFormats/JetMETObjects/interface/FactorizedJetCorrector.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
using namespace edm;
using namespace std;

//
// class declaration
//

class ImplementBtaggingSF : public EDAnalyzer {
   public:
      explicit ImplementBtaggingSF(const ParameterSet&);
      ~ImplementBtaggingSF();

   private:
      virtual void analyze(const Event&, const EventSetup&) override;
      // ----------member data ---------------------------

      Service<TFileService> fs_;
         //map< string, TH1D* > histos1D_;
         //map< string, TH2D* > histos2D_;
     
      TFile * f_EffMap = new TFile("EfficiencyMaps.root");  //Name of the Efficiency Map file
  
  // SFb plots
      TH1D * h_bjet_pt = fs_->make<TH1D>("h_bjet_pt","",50,0.,1000.);
      TH1D * h_bjet_pt_wt = fs_->make<TH1D>("h_bjet_pt_wt","",50,0.,1000.);
      TH1D * h_weights = fs_->make<TH1D>("h_weights","",50,-2,2);
      TH1D * h_bjet_wt_errorsquared = fs_->make<TH1D>("h_bjet_wt_errorsquared","",50,0.,1000.);
      TH1D * h_bjet_pt_wt_plus_err = fs_->make<TH1D>("h_bjet_pt_wt_plus_err","",50,0.,1000.);
      TH1D * h_bjet_pt_wt_minus_err = fs_->make<TH1D>("h_bjet_pt_wt_minus_err","",50,0.,1000.);

  EDGetTokenT<reco::VertexCollection> vtxToken_;
  EDGetTokenT<pat::JetCollection> jetToken_;
  
  vector<float> *jetsPt = new std::vector<float>();
  vector<float> *jetsEta = new std::vector<float>();
  vector<float> *jetsPhi = new std::vector<float>();
  vector<float> *jetsE = new std::vector<float>();
  
  EDGetTokenT<int> npv_;
  EDGetTokenT<vector<float>> jetPt_;
  EDGetTokenT<vector<float>> jetEta_;
  EDGetTokenT<vector<float>> jetPhi_;
  EDGetTokenT<vector<float>> jetE_;
  EDGetTokenT<vector<float>> jetCSV_;
  EDGetTokenT<vector<float>> jetCSVV1_;
  EDGetTokenT<vector<float>> jetPartonFlavour_;  
  EDGetTokenT<vector<float>> jetMass_;
  EDGetTokenT<vector<float>> jetArea_;

  EDGetTokenT<double> rhoToken_;

  //Jet Corrector  
  vector<JetCorrectorParameters> jetPar;
  FactorizedJetCorrector * JetCorrector;

  int isMiniAOD;

      TH2D * h2_EffMapB = (TH2D*)f_EffMap->Get("efficiency_b"); //Name of the b efficiency map
      TH2D * h2_EffMapC = (TH2D*)f_EffMap->Get("efficiency_c"); //Name of the c efficiency map
      TH2D * h2_EffMapUDSG = (TH2D*)f_EffMap->Get("efficiency_udsg"); //Name of the udsg efficiency map
};

ImplementBtaggingSF::ImplementBtaggingSF(const ParameterSet& iConfig):
  vtxToken_(consumes<reco::VertexCollection>(iConfig.getParameter<InputTag>("vertices"))),
  jetToken_(consumes<pat::JetCollection>(iConfig.getParameter<InputTag>("jets"))),

  npv_(consumes<int>(iConfig.getParameter<InputTag>("npv"))),
  jetPt_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetPt"))),
  jetEta_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetEta"))),
  jetPhi_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetPhi"))),
  jetE_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetE"))),
  jetCSV_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetCSV"))),
  jetCSVV1_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetCSVV1"))),
  jetPartonFlavour_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetPartonFlavour"))),
  jetMass_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetMass"))),
  jetArea_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetArea"))),
  rhoToken_(consumes<double>(iConfig.getParameter<InputTag>("rho")))
{
  isMiniAOD = iConfig.getParameter<int>("isMiniAOD");

  //Jet Correction Files
  vector<string> jecPayloadNames_;
  jecPayloadNames_.push_back("JECs/Spring16_25nsV6_MC_L1FastJet_AK4PFchs.txt");
  jecPayloadNames_.push_back("JECs/Spring16_25nsV6_MC_L2Relative_AK4PFchs.txt");
  jecPayloadNames_.push_back("JECs/Spring16_25nsV6_MC_L3Absolute_AK4PFchs.txt");

  for ( vector<string>::const_iterator payloadBegin = jecPayloadNames_.begin(), payloadEnd = jecPayloadNames_.end(), ipayload = payloadBegin; ipayload != payloadEnd; ++ipayload ) {
    JetCorrectorParameters pars(*ipayload);
    jetPar.push_back(pars);
  }
  JetCorrector = new FactorizedJetCorrector(jetPar);

}

ImplementBtaggingSF::~ImplementBtaggingSF()
{
}

void
ImplementBtaggingSF::analyze(const Event& iEvent, const EventSetup& iSetup)
{


    //miniaod
    Handle<reco::VertexCollection> vertices;
    Handle<pat::JetCollection> jets;
    Handle<double> rho;
    //ntuple
    Handle<vector<float> > jetPt;
    Handle<vector<float> > jetEta;
    Handle<vector<float> > jetPhi;
    Handle<vector<float> > jetE;
    Handle<vector<float> > jetCSV;
    Handle<vector<float> > jetCSVV1;
    Handle<vector<float> > jetPartonFlavour;
    Handle<vector<float> > jetMass;
    Handle<vector<float> > jetArea;
    Handle<int> npv;

    size_t sizeJets = 0;

    BTagCalibration calib("csv","CSVv2.csv");

    BTagCalibrationReader reader(BTagEntry::OP_MEDIUM,    // operating point
				 "central",
				 { "up", "down" });         //sys types
    
    reader.load(calib,                   // calibration instance
		BTagEntry::FLAV_B,       // btag flavour
		"comb");                  // measurement type
    reader.load(calib,
		BTagEntry::FLAV_C,
		"incl");
    reader.load(calib,
		BTagEntry::FLAV_UDSG,
		"incl");

    if( isMiniAOD == 0){
      
      iEvent.getByToken(vtxToken_, vertices);
      if (vertices->empty()) return; // skip the event if no PV found
      iEvent.getByToken(jetToken_, jets);

      iEvent.getByToken( rhoToken_, rho );

      
      sizeJets = jets->size();
      
    }
    if( isMiniAOD == 1 ){ 
      iEvent.getByToken(npv_, npv);
      if(*npv == 0) return; // skip the event if no PV found
      iEvent.getByToken(jetPt_, jetPt);
      iEvent.getByToken(jetEta_, jetEta);
      iEvent.getByToken(jetPhi_, jetPhi);
      iEvent.getByToken(jetE_, jetE);
      iEvent.getByToken(jetCSV_, jetCSV);
      iEvent.getByToken(jetCSVV1_, jetCSVV1);
      iEvent.getByToken(jetPartonFlavour_, jetPartonFlavour);
      iEvent.getByToken(jetMass_, jetMass);
      iEvent.getByToken(jetArea_, jetArea);

      sizeJets = jetPt->size();
    }


    //Begin scale factor implementation

    float wtbtag = 1.;
    float wtbtagError = 1.;
    
    float mcTag = 1.;
    float mcNoTag = 1.;
    float dataTag = 1.;
    float dataNoTag = 1.;

    float err1 = 0; 
    float err2 = 0; 
    float err3 = 0; 
    float err4 = 0; 


    for ( size_t i = 0; i < sizeJets; i++ ) {

      TLorentzVector RawJet;
      
      if(isMiniAOD == 0) RawJet.SetPtEtaPhiM((*jets)[i].pt(), (*jets)[i].eta(), (*jets)[i].phi(), (*jets)[i].mass());
      if(isMiniAOD == 1) RawJet.SetPtEtaPhiM((*jetPt)[i],(*jetEta)[i],(*jetPhi)[i],(*jetMass)[i]);

      //Add JECs to jets
      double JEC = 1;
      if( isMiniAOD == 0 ) {
	JetCorrector->setJetPt( RawJet.Pt());
	JetCorrector->setJetEta( RawJet.Eta() );
	JetCorrector->setJetPhi( RawJet.Phi() );
	JetCorrector->setJetE( RawJet.E() );
	JetCorrector->setRho( *rho );
	JetCorrector->setNPV( vertices->size() );
	JetCorrector->setJetA((*jets)[i].jetArea());
	
	JEC = JetCorrector->getCorrection();
      }
      
      TLorentzVector Jet = RawJet*JEC;


      float csv = -1000;
      int partonFlavor = -10;
      float eta = Jet.Eta();
      float pt = Jet.Pt();
      if( isMiniAOD == 0 ) {
	csv = (*jets)[i].bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags");
	partonFlavor = abs((*jets)[i].partonFlavour());
      }
      if( isMiniAOD == 1 ) {
	csv = (*jetCSV)[i];
	partonFlavor = abs((*jetPartonFlavour)[i]);
      }
      
      if( eta>2.4) continue;
      if( partonFlavor==0) continue; //for jets with flavor 0, we ignore.
      if( csv >= 1 || csv < 0 ) continue;

	    float eff = 1;
	    if( partonFlavor==5 ) {
	      ///the pt/eta dependent efficiency for b-tag for "b jet"
	      eff = h2_EffMapB->GetBinContent( h2_EffMapB->GetXaxis()->FindBin(pt), h2_EffMapB->GetYaxis()->FindBin(fabs(eta)) );
	    }else if( partonFlavor==4){
	      ///the pt/eta dependent efficiency for b-tag for "c jet"
	      eff = h2_EffMapC->GetBinContent( h2_EffMapC->GetXaxis()->FindBin(pt), h2_EffMapC->GetYaxis()->FindBin(fabs(eta)) );
	    }else{
	      ///the pt/eta dependent efficiency for b-tag for "light jet"
	      eff = h2_EffMapUDSG->GetBinContent( h2_EffMapUDSG->GetXaxis()->FindBin(pt), h2_EffMapUDSG->GetYaxis()->FindBin(fabs(eta)) );
	    }
	    bool istag = csv > .8 && eta<2.4 ;//csv value
	    float SF = 0;
	    float SFup = 0;
	    float SFdown = 0;
	    float SFerr = 0;

	    if ( partonFlavor == 5 ) {

	      SF = reader.eval_auto_bounds( "central", BTagEntry::FLAV_B, eta, pt );
	      SFup = reader.eval_auto_bounds( "up", BTagEntry::FLAV_B, eta, pt );
	      SFdown = reader.eval_auto_bounds( "down", BTagEntry::FLAV_B, eta, pt );

	    }
	    else if ( partonFlavor == 4 ) {

	      SF = reader.eval_auto_bounds( "central", BTagEntry::FLAV_C, eta, pt);
	      SFup = reader.eval_auto_bounds( "up", BTagEntry::FLAV_C, eta, pt);
	      SFdown = reader.eval_auto_bounds( "down", BTagEntry::FLAV_C, eta, pt);

	    }
	    else {

	      cout << "Light Flavor jet!" << endl;

	      SF = reader.eval_auto_bounds( "central", BTagEntry::FLAV_UDSG, eta, pt );
	      SFup = reader.eval_auto_bounds( "up", BTagEntry::FLAV_UDSG, eta, pt);
	      SFdown = reader.eval_auto_bounds( "down", BTagEntry::FLAV_UDSG, eta, pt );

	    }

	    SFerr = fabs( SFup-SF )>fabs( SFdown-SF)? fabs( SFup-SF):fabs( SFdown-SF);

	    if( SF == 0 || SFerr == 0 ) continue;

	    if(istag){
	      mcTag *= eff;
	      dataTag *= eff*SF;

	      if(partonFlavor==5 || partonFlavor == 4) err1 += SFerr/SF; //correlated for b/c
	      else err3 += SFerr/SF; //correlated for light
	      
	    }else{
	      mcNoTag *= (1-eff);
	      dataNoTag *= (1-eff*SF);

	      if(partonFlavor==5 || partonFlavor==4) err2 += (-eff*SFerr)/(1-eff*SF); // correlated for b/c
	      else err4 += (-eff*SFerr)/(1-eff*SF); //correlated for light
	      
	    }

    }
    wtbtag = (dataNoTag * dataTag) / (mcNoTag * mcTag);
    wtbtagError = sqrt( pow(err1+err2,2) + pow( err3 + err4, 2)) * wtbtag; //un-correlated for b/c and light
    float errsquared = pow(wtbtag,2) + pow(wtbtagError,2); 
    h_weights->Fill(wtbtag);
    
    for( size_t i = 0; i < sizeJets; i++ ) {
      if( isMiniAOD == 0 ) {
	float csv = (*jets)[i].bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags");
	if( csv > .8 && !(fabs((*jets)[i].eta()) > 2.4) && csv <= 1 ) {
	  h_bjet_wt_errorsquared->Fill((*jets)[i].pt(),errsquared);
	}
      }
      if( isMiniAOD == 1 ) {
	float csv = (*jetCSV)[i];
	if( csv > .8 && !(fabs((*jetEta)[i]) > 2.4 ) && csv <= 1 ) {
	  h_bjet_wt_errorsquared->Fill((*jetPt)[i], errsquared);
	}
      }
    }

    for ( size_t i = 0; i < sizeJets; i++ ) {
      if( isMiniAOD == 0 ) {
	float csv = (*jets)[i].bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags");
	if(  csv > .8 && !(fabs((*jets)[i].eta()) > 2.4) && csv <= 1 ) {

	  TLorentzVector RawJet;
	  if(isMiniAOD == 0) RawJet.SetPtEtaPhiM((*jets)[i].pt(), (*jets)[i].eta(), (*jets)[i].phi(), (*jets)[i].mass());
	  if(isMiniAOD == 1) RawJet.SetPtEtaPhiM((*jetPt)[i],(*jetEta)[i],(*jetPhi)[i],(*jetMass)[i]);


	  double JEC = 1;
	  if( isMiniAOD == 0 ) {
	    JetCorrector->setJetPt(RawJet.Pt());
	    JetCorrector->setJetEta( RawJet.Eta() );
	    JetCorrector->setJetPhi( RawJet.Phi() );
	    JetCorrector->setJetE( RawJet.E() );
	    JetCorrector->setRho( *rho );
	    JetCorrector->setNPV( vertices->size() );
	    JetCorrector->setJetA((*jets)[i].jetArea());
	    
	    JEC = JetCorrector->getCorrection();
	  }
	  
	  TLorentzVector Jet = RawJet*JEC;


	  h_bjet_pt->Fill(Jet.Pt());
	  h_bjet_pt_wt->Fill(Jet.Pt(),wtbtag);
	  h_bjet_pt_wt_plus_err->Fill(Jet.Pt(),wtbtag+wtbtagError);
	  h_bjet_pt_wt_minus_err->Fill(Jet.Pt(),wtbtag-wtbtagError);
	}
      }
      if( isMiniAOD == 1 ) {
	float csv = (*jetCSV)[i];
	if( csv > .8 && !(fabs((*jetEta)[i]) > 2.4 ) && csv <= 1 ) {
	  h_bjet_pt->Fill((*jetPt)[i]);
	  h_bjet_pt_wt->Fill((*jetPt)[i],wtbtag);
	  h_bjet_pt_wt_plus_err->Fill((*jetPt)[i],wtbtag+wtbtagError);
	  h_bjet_pt_wt_minus_err->Fill((*jetPt)[i],wtbtag-wtbtagError);
	}
      }
    }

}


//define this as a plug-in
DEFINE_FWK_MODULE(ImplementBtaggingSF);


