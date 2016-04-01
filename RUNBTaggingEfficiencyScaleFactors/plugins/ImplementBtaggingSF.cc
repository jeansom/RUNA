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
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"

#include "CondFormats/BTauObjects/interface/BTagCalibration.h"
#include "CondFormats/BTauObjects/interface/BTagCalibrationReader.h"

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
      EDGetTokenT<pat::MuonCollection> muonToken_;
      EDGetTokenT<pat::ElectronCollection> electronToken_;
      EDGetTokenT<pat::TauCollection> tauToken_;
      EDGetTokenT<pat::PhotonCollection> photonToken_;
      EDGetTokenT<pat::JetCollection> jetToken_;
      EDGetTokenT<pat::JetCollection> puppijetToken_;
      EDGetTokenT<pat::METCollection> metToken_;
  
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
  muonToken_(consumes<pat::MuonCollection>(iConfig.getParameter<InputTag>("muons"))),
  electronToken_(consumes<pat::ElectronCollection>(iConfig.getParameter<InputTag>("electrons"))),
  tauToken_(consumes<pat::TauCollection>(iConfig.getParameter<InputTag>("taus"))),
  photonToken_(consumes<pat::PhotonCollection>(iConfig.getParameter<InputTag>("photons"))),
  jetToken_(consumes<pat::JetCollection>(iConfig.getParameter<InputTag>("jets"))),
  puppijetToken_(consumes<pat::JetCollection>(iConfig.getParameter<InputTag>("puppijets"))),
  metToken_(consumes<pat::METCollection>(iConfig.getParameter<InputTag>("mets"))),

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
  jecAK4PayloadNames_.push_back("JECs/Summer15_25nsV6_MC_L1FastJet_AK4PFchs.txt");
  jecAK4PayloadNames_.push_back("JECs/Summer15_25nsV6_MC_L2Relative_AK4PFchs.txt");
  jecAK4PayloadNames_.push_back("JECs/Summer15_25nsV6_MC_L3Absolute_AK4PFchs.txt");

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
    Handle<pat::MuonCollection> muons;
    Handle<pat::ElectronCollection> electrons;
    Handle<pat::PhotonCollection> photons;
    Handle<pat::TauCollection> taus;
    Handle<pat::JetCollection> jets;
    Handle<pat::JetCollection> puppijets;
    Handle<pat::METCollection> mets;
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

    if( isMiniAOD == 0){
      
      iEvent.getByToken(vtxToken_, vertices);
      if (vertices->empty()) return; // skip the event if no PV found
      iEvent.getByToken(muonToken_, muons);
      iEvent.getByToken(electronToken_, electrons);
      iEvent.getByToken(photonToken_, photons);
      iEvent.getByToken(tauToken_, taus);
      iEvent.getByToken(jetToken_, jets);
      iEvent.getByToken(puppijetToken_, puppijets);
      iEvent.getByToken(metToken_, mets);

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

    BTagCalibration calib_csv("csv","CSVv2.csv");
    BTagCalibrationReader reader(&calib_csv,           // calibration instance
				 BTagEntry::OP_MEDIUM,    //operating point
				 "mujets",                 //measurement type
				 "central");             //systematics type
    BTagCalibrationReader readerUp(&calib_csv,           // calibration instance
				 BTagEntry::OP_MEDIUM,    //operating point
				 "mujets",                 //measurement type
				 "up");             //systematics type
    BTagCalibrationReader readerDown(&calib_csv,           // calibration instance
				 BTagEntry::OP_MEDIUM,    //operating point
				 "mujets",                 //measurement type
				 "down");             //systematics type
    BTagCalibrationReader readerLight(&calib_csv,           // calibration instance
				 BTagEntry::OP_MEDIUM,    //operating point
				 "incl",                 //measurement type
				 "central");             //systematics type
    BTagCalibrationReader readerLightUp(&calib_csv,           // calibration instance
				 BTagEntry::OP_MEDIUM,    //operating point
				 "incl",                 //measurement type
				 "up");             //systematics type
    BTagCalibrationReader readerLightDown(&calib_csv,           // calibration instance
				 BTagEntry::OP_MEDIUM,    //operating point
				 "incl",                 //measurement type
				 "down");             //systematics type    

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
	    double ptmax = 670.;
	    double ptmin = 20.;
	    float ptTemp = pt;
	    if( pt > ptmax ) ptTemp = ptmax;
	    if( pt < ptmin ) ptTemp = ptmin;

	    if ( partonFlavor == 5 ) {

	      SF = reader.eval(BTagEntry::FLAV_B, 
			       eta,
			       ptTemp);
	      SFup = readerUp.eval(BTagEntry::FLAV_B,
				   eta,
				   ptTemp);
	      SFdown = readerDown.eval(BTagEntry::FLAV_B,
				       eta,
				       ptTemp);
	      SFerr = fabs( SFup-SF )>fabs( SFdown-SF)? fabs( SFup-SF):fabs( SFdown-SF);
	    }
	    else if ( partonFlavor == 4 ) {

	      SF = reader.eval(BTagEntry::FLAV_C,
			       eta,
			       ptTemp);
	      SFup = readerUp.eval(BTagEntry::FLAV_C,
				   eta,
				   ptTemp);
	      SFdown = readerDown.eval(BTagEntry::FLAV_C,
				       eta,
				       ptTemp);
	      SFerr = fabs( SFup-SF )>fabs( SFdown-SF)? fabs( SFup-SF):fabs( SFdown-SF);
	    }
	    else {
	      cout << "Light Flavor jet!" << endl;
	      SF = readerLight.eval(BTagEntry::FLAV_UDSG,
				    eta,
				    ptTemp);
	      SFup = readerLightUp.eval(BTagEntry::FLAV_UDSG,
					eta,
					ptTemp);
	      SFdown = readerLightDown.eval(BTagEntry::FLAV_UDSG,
					    eta,
					    ptTemp);
	      SFerr = fabs( SFup-SF )>fabs( SFdown-SF)? fabs( SFup-SF):fabs( SFdown-SF);	    
	    }
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
	if( (*jets)[i].bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags") > .8 && !(fabs((*jets)[i].eta()) > 2.4) && (*jets)[i].bDiscriminator("pfCombinedIncludsiveSecondaryVertexV2BJetTags") <= 1 ) {
	  h_bjet_wt_errorsquared->Fill((*jets)[i].pt(),errsquared);
	}
      }
      if( isMiniAOD == 1 ) {
	if( (*jetCSV)[i] > .8 && !(fabs((*jetEta)[i]) > 2.4 ) && (*jetCSV)[i] <= 1 ) {
	  h_bjet_wt_errorsquared->Fill((*jetPt)[i], errsquared);
	}
      }
    }

    for ( size_t i = 0; i < sizeJets; i++ ) {
      if( isMiniAOD == 0 ) {
	if(  (*jets)[i].bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags") > .8 && !(fabs((*jets)[i].eta()) > 2.4) && (*jets)[i].bDiscriminator("pfCombinedIncludsiveSecondaryVertexV2BJetTags") <= 1 ) {

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
	    JetCorrector->setJetA((*ak8jets)[i].jetArea());
	    
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
	if( (*jetCSV)[i] > .8 && !(fabs((*jetEta)[i]) > 2.4 ) && (*jetCSV)[i] <= 1 ) {
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


