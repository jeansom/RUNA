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

#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"

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

class ConvertBtaggingSF : public EDAnalyzer {
   public:
      explicit ConvertBtaggingSF(const ParameterSet&);
      ~ConvertBtaggingSF();

   private:
      virtual void analyze(const Event&, const EventSetup&) override;
      // ----------member data ---------------------------

      Service<TFileService> fs_;
         //map< string, TH1D* > histos1D_;
         //map< string, TH2D* > histos2D_;
     
      //AK4 SFb to AK8 SFb conversion plots
      TH1D * h_delta_r = fs_->make<TH1D>("h_delta_r","",50,0.,10.);
      TH1D * h_delta_r_min = fs_->make<TH1D>("h_delta_r_min","",50,0.,1.);
      TH1D * h_delta_r_2nd_min = fs_->make<TH1D>("h_delta_r_2nd_min","",50,0.,1.);
      TH1D * h_delta_r_1st2nd_min = fs_->make<TH1D>("h_delta_r_1st2nd_min","",50,0.,1.);
      TH1D * h_num_matches_foreach_AK8 = fs_->make<TH1D>("h_num_matches_foreach_AK8","",50,0.,4.);
      TH2D * h_delta_r_1st_v_2nd_min = fs_->make<TH2D>("h_delta_r_1st_v_2nd_min","",50,0.,1.,50,0.,2.);
      TH1D * h_eta_all_true_bjet_AK8 = fs_->make<TH1D>("h_eta_all_true_bjet_AK8","h_eta_all_true_bjet_AK8",50,-3.,3.);
      TH1D * h_eta_all_true_bjet_AK4 = fs_->make<TH1D>("h_eta_all_true_bjet_AK4","h_eta_all_true_bjet_AK4",50,-3.,3.);  
      TH1D * h_eta_true_bjet_with_match_AK8 = fs_->make<TH1D>("h_eta_true_bjet_with_match_AK8","h_eta_true_bjet_with_match_AK8",50,-3.,3.);
      TH1D * h_eta_true_bjet_with_match_AK4 = fs_->make<TH1D>("h_eta_true_bjet_with_match_AK4","h_eta_true_bjet_with_match_AK4",50,-3.,3.);
  
      TH2D * h_matched_AK4pt_vs_AK8pt = fs_->make<TH2D>("h_matched_AK4pt_vs_AK8pt", "h_matched_AK4pt_vs_AK8pt", 50, 0., 1000., 50, 0., 1000.);
      TH2D * h_matched_AK4pt_vs_AK8pt_AK4csv_cut = fs_->make<TH2D>("h_matched_AK4pt_vs_AK8pt_AK4csv_cut", "h_matched_AK4pt_vs_AK8pt_AK4csv_cut", 50, 0., 1000., 50, 0., 1000.);
      TH2D * h_matched_AK4pt_vs_AK8pt_AK8csv_cut = fs_->make<TH2D>("h_matched_AK4pt_vs_AK8pt_AK8csv_cut", "h_matched_AK4pt_vs_AK8pt_AK8csv_cut", 50, 0., 1000., 50, 0., 1000.);  
      TH2D * h_matched_AK4pt_vs_AK8pt_AK8AK4csv_cut = fs_->make<TH2D>("h_matched_AK4pt_vs_AK8pt_AK8AK4csv_cut", "h_matched_AK4pt_vs_AK8pt_AK8AK4csv_cut", 50, 0., 1000., 50, 0., 1000.);

      TH1D * h_event_count = fs_->make<TH1D>("h_event_count", "h_event_count", 50, 0., 1.);
      TH1D * h_n_AK8_jets = fs_->make<TH1D>("h_n_AK8_jets", "h_n_AK8_jets", 50, 0., 25.);
      TH1D * h_n_AK8_bjets = fs_->make<TH1D>("h_n_AK8_bjets", "h_n_AK8_bjets", 50, 0., 25.);
      TH1D * h_n_AK4_jets = fs_->make<TH1D>("h_n_AK4_jets", "h_n_AK4_jets", 50, 0., 25.);
      TH1D * h_n_AK4_bjets = fs_->make<TH1D>("h_n_AK4_bjets", "h_n_AK4_bjets", 50, 0., 25.);

      TH1D * h_pt_true_bjet_with_match_AK8 = fs_->make<TH1D>("h_pt_bjet_with_match_AK8","",50,0.,2000.);
      TH1D * h_pt_all_true_bjet_AK8 = fs_->make<TH1D>("h_pt_all_true_bjet_AK8","",50,0.,2000.);
      TH1D * h_pt_true_bjet_with_match_AK4 = fs_->make<TH1D>("h_pt_bjet_with_match_AK4","",50,0.,2000.);
      TH1D * h_pt_all_true_bjet_AK4 = fs_->make<TH1D>("h_pt_all_true_bjet_AK4","",50,0.,2000.);
      TH1D * h_csv_all_true_bjet_AK8 = fs_->make<TH1D>("h_csv_all_true_bjet_AK8","h_csv_all_true_bjet_AK8",50,0.,10.);
      TH1D * h_csv_all_true_bjet_AK4 = fs_->make<TH1D>("h_csv_all_true_bjet_AK4","h_csv_all_true_bjet_AK4",50,0.,10.);
      TH1D * h_num_AK8 = fs_->make<TH1D>("h_num_AK8","",50,0.,1000.);
      TH1D * h_num_AK4 = fs_->make<TH1D>("h_num_AK4","",50,0.,1000.);
      TH1D * h_num_AK4_bin_with_AK8pt = fs_->make<TH1D>("h_num_AK4_bin_with_AK8pt","h_num_AK4_bin_with_AK8pt",50,0.,1000.);
      TH1D * h_num_AK8_bin_with_AK4pt = fs_->make<TH1D>("h_num_AK8_bin_with_AK4pt","h_num_AK8_bin_with_AK4pt",50,0.,1000.);
      TH1D * h_denom_AK8 = fs_->make<TH1D>("h_denom_AK8","",50,0.,1000.);
      TH1D * h_denom_AK4 = fs_->make<TH1D>("h_denom_AK4","",50,0.,1000.);
      TH1D * h_denom_AK4_bin_with_AK8pt = fs_->make<TH1D>("h_denom_AK4_bin_with_AK8pt","h_denom_AK4_bin_with_AK8pt",50,0.,1000.);
      TH1D * h_denom_AK8_bin_with_AK4pt = fs_->make<TH1D>("h_denom_AK8_bin_with_AK4pt","h_denom_AK8_bin_with_AK4pt",50,0.,1000.);
      TH1D * h_csv_AK8_match = fs_->make<TH1D>("h_csv_AK8","",50,0.,2.);
      TH1D * h_csv_AK4_match = fs_->make<TH1D>("h_csv_AK4","",50,0.,2.);
      TH1D * h_npv_matched_jet_events = fs_->make<TH1D>("h_npv_matched_jet_events","h_npv_matched_jet_events",50,0.,50.);
      TH1D * h_npv_all_events = fs_->make<TH1D>("h_npv_all_events","h_npv_all_events",50,0.,50.);
      TH1D * h_area_AK8 = fs_->make<TH1D>("h_area_AK8","h_area_AK8",50,0.,5.);
      TH1D * h_area_AK4 = fs_->make<TH1D>("h_area_AK4","h_area_AK4",50,0.,5.);
      TH1D * h_matchedjetAK8_pt_pass_csv8ANDcsv4_cut = fs_->make<TH1D>("h_matchedjetAK8_pt_pass_csv8ANDcsv4_cut","h_matchedjetAK8_pt_pass_csv8ANDcsv4_cut", 50, 0., 1000.);
      TH1D * h_matchedjetAK8_pt_pass_ONLYcsv8_cut = fs_->make<TH1D>("h_matchedjetAK8_pt_pass_csv8_cut","h_matchedjetAK8_pt_pass_csv8_cut", 50, 0., 1000.);
      TH1D * h_matchedjetAK8_pt_pass_ONLYcsv4_cut = fs_->make<TH1D>("h_matchedjetAK8_pt_pass_csv4_cut","h_matchedjetAK8_pt_pass_csv4_cut", 50, 0., 1000.);
      TH1D * h_matchedjetAK4_pt_pass_csv8ANDcsv4_cut = fs_->make<TH1D>("h_matchedjetAK4_pt_pass_csv8ANDcsv4_cut","h_matchedjetAK4_pt_pass_csv8ANDcsv4_cut", 50, 0., 1000.);
      TH1D * h_matchedjetAK4_pt_pass_ONLYcsv8_cut = fs_->make<TH1D>("h_matchedjetAK4_pt_pass_csv8_cut","h_matchedjetAK4_pt_pass_csv8_cut", 50, 0., 1000.);
      TH1D * h_matchedjetAK4_pt_pass_ONLYcsv4_cut = fs_->make<TH1D>("h_matchedjetAK4_pt_pass_csv4_cut","h_matchedjetAK4_pt_pass_csv4_cut", 50, 0., 1000.);


      //MiniAOD Tokens 
      EDGetTokenT<reco::VertexCollection> vtxToken_;
      EDGetTokenT<pat::MuonCollection> muonToken_;
      EDGetTokenT<pat::ElectronCollection> electronToken_;
      EDGetTokenT<pat::TauCollection> tauToken_;
      EDGetTokenT<pat::PhotonCollection> photonToken_;
      EDGetTokenT<pat::JetCollection> jetToken_;
      EDGetTokenT<pat::JetCollection> ak8jetToken_;
      EDGetTokenT<pat::JetCollection> puppijetToken_;
      EDGetTokenT<pat::METCollection> metToken_;
  

      //Ntuple Tokens
      vector<float> *jetsPt = new std::vector<float>();
      vector<float> *jetsEta = new std::vector<float>();
      vector<float> *jetsPhi = new std::vector<float>();
      vector<float> *jetsE = new std::vector<float>();
      vector<float> *electronPt = new std::vector<float>();
      vector<float> *muonPt = new std::vector<float>();
  
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
      EDGetTokenT<vector<float>> elPt_;
      EDGetTokenT<vector<float>> muPt_;
      vector<float> *jetsAK8Pt = new std::vector<float>();
      vector<float> *jetsAK8Eta = new std::vector<float>();
      vector<float> *jetsAK8Phi = new std::vector<float>();
      vector<float> *jetsAK8E = new std::vector<float>();
    
      EDGetTokenT<vector<float>> jetAK8Pt_;
      EDGetTokenT<vector<float>> jetAK8Eta_;
      EDGetTokenT<vector<float>> jetAK8Phi_;
      EDGetTokenT<vector<float>> jetAK8E_;
      EDGetTokenT<vector<float>> jetAK8CSV_;
      EDGetTokenT<vector<float>> jetAK8CSVV1_;
      EDGetTokenT<vector<float>> jetAK8PartonFlavour_;
      EDGetTokenT<vector<float>> jetAK8Mass_;
      EDGetTokenT<vector<float>> jetAK8Area_;
      EDGetTokenT<double> rhoToken_;
    
      //Jet Corrector  
      vector<JetCorrectorParameters> jetPar;
      FactorizedJetCorrector * JetCorrector;
    

      //MiniAOD or Ntuple
      int isMiniAOD;
};

ConvertBtaggingSF::ConvertBtaggingSF(const ParameterSet& iConfig):
  //MiniAOD Tokens
  vtxToken_(consumes<reco::VertexCollection>(iConfig.getParameter<InputTag>("vertices"))),
  muonToken_(consumes<pat::MuonCollection>(iConfig.getParameter<InputTag>("muons"))),
  electronToken_(consumes<pat::ElectronCollection>(iConfig.getParameter<InputTag>("electrons"))),
  tauToken_(consumes<pat::TauCollection>(iConfig.getParameter<InputTag>("taus"))),
  photonToken_(consumes<pat::PhotonCollection>(iConfig.getParameter<InputTag>("photons"))),
  jetToken_(consumes<pat::JetCollection>(iConfig.getParameter<InputTag>("jets"))),
  ak8jetToken_(consumes<pat::JetCollection>(iConfig.getParameter<InputTag>("ak8jets"))),
  puppijetToken_(consumes<pat::JetCollection>(iConfig.getParameter<InputTag>("puppijets"))),
  metToken_(consumes<pat::METCollection>(iConfig.getParameter<InputTag>("mets"))),

  //Ntuple Tokens
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
  elPt_(consumes<vector<float>>(iConfig.getParameter<InputTag>("electronPt"))),
  muPt_(consumes<vector<float>>(iConfig.getParameter<InputTag>("muonPt"))),
  jetAK8Pt_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetAK8Pt"))),
  jetAK8Eta_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetAK8Eta"))),
  jetAK8Phi_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetAK8Phi"))),
  jetAK8E_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetAK8E"))),
  jetAK8CSV_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetAK8CSV"))),
  jetAK8CSVV1_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetAK8CSVV1"))),
  jetAK8PartonFlavour_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetAK8PartonFlavour"))),
  jetAK8Mass_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetAK8Mass"))),
  jetAK8Area_(consumes<vector<float>>(iConfig.getParameter<InputTag>("jetAK8Area"))),
  rhoToken_(consumes<double>(iConfig.getParameter<InputTag>("rho")))
{

  //MiniAOD or Ntuple
  isMiniAOD = iConfig.getParameter<int>("isMiniAOD");


  //Jet Correction Files
  vector<string> jecAK8PayloadNames_;
  jecAK8PayloadNames_.push_back("JECs/Summer15_25nsV6_MC_L1FastJet_AK8PFchs.txt");
  jecAK8PayloadNames_.push_back("JECs/Summer15_25nsV6_MC_L2Relative_AK8PFchs.txt");
  jecAK8PayloadNames_.push_back("JECs/Summer15_25nsV6_MC_L3Absolute_AK8PFchs.txt");

  for ( vector<string>::const_iterator payloadBegin = jecAK8PayloadNames_.begin(), payloadEnd = jecAK8PayloadNames_.end(), ipayload = payloadBegin; ipayload != payloadEnd; ++ipayload ) {
    JetCorrectorParameters pars(*ipayload);
    jetPar.push_back(pars);
  }
  JetCorrector = new FactorizedJetCorrector(jetPar);
}

ConvertBtaggingSF::~ConvertBtaggingSF()
{
}

void
ConvertBtaggingSF::analyze(const Event& iEvent, const EventSetup& iSetup)
{

    //miniaod
    Handle<reco::VertexCollection> vertices;    
    Handle<pat::MuonCollection> muons;
    Handle<pat::ElectronCollection> electrons;
    Handle<pat::PhotonCollection> photons;
    Handle<pat::TauCollection> taus;
    Handle<pat::JetCollection> jets;
    Handle<pat::JetCollection> ak8jets;
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
    Handle<vector<float> > electronPt;
    Handle<vector<float> > muonPt;
    Handle<vector<float> > jetAK8Pt;
    Handle<vector<float> > jetAK8Eta;
    Handle<vector<float> > jetAK8Phi;
    Handle<vector<float> > jetAK8E;
    Handle<vector<float> > jetAK8CSV;
    Handle<vector<float> > jetAK8CSVV1;
    Handle<vector<float> > jetAK8PartonFlavour;
    Handle<vector<float> > jetAK8Mass;
    Handle<vector<float> > jetAK8Area;
    Handle<int> npv;

    size_t sizeAK4 = 0;
    size_t sizeAK8 = 0;

    //Getting MiniAOD     
    if( isMiniAOD == 0){
      
      iEvent.getByToken(vtxToken_, vertices);
      if (vertices->empty()) return; // skip the event if no PV found
      iEvent.getByToken(muonToken_, muons);
      iEvent.getByToken(electronToken_, electrons);
      iEvent.getByToken(photonToken_, photons);
      iEvent.getByToken(tauToken_, taus);
      iEvent.getByToken(jetToken_, jets);
      iEvent.getByToken(ak8jetToken_, ak8jets);
      iEvent.getByToken(puppijetToken_, puppijets);
      iEvent.getByToken(metToken_, mets);

      iEvent.getByToken( rhoToken_, rho );

      //Number of AK4 and AK8 jets
      sizeAK8 = ak8jets->size();
      sizeAK4 = jets->size();
      
    }

    //Getting Ntuple
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
      iEvent.getByToken(elPt_, electronPt);
      iEvent.getByToken(muPt_, muonPt);
      iEvent.getByToken(jetAK8Pt_, jetAK8Pt);
      iEvent.getByToken(jetAK8Eta_, jetAK8Eta);
      iEvent.getByToken(jetAK8Phi_, jetAK8Phi);
      iEvent.getByToken(jetAK8E_, jetAK8E);
      iEvent.getByToken(jetAK8CSV_, jetAK8CSV);
      iEvent.getByToken(jetAK8CSVV1_, jetAK8CSVV1);
      iEvent.getByToken(jetAK8PartonFlavour_, jetAK8PartonFlavour);
      iEvent.getByToken(jetAK8Mass_, jetAK8Mass);
      iEvent.getByToken(jetAK8Area_, jetArea);
  
      //Number of AK8 and AK4 jets
      sizeAK8 = jetAK8Pt->size();
      sizeAK4 = jetPt->size();
      }

    int ak8index = 0;
    
    //Fill plots with number of primary vertices
    if( isMiniAOD == 0 ) h_npv_all_events->Fill(vertices->size());
    if( isMiniAOD == 1 ) h_npv_all_events->Fill(*npv);

    //Fill plots with number of AK8 and AK4 jets in each event
    h_n_AK8_jets->Fill(sizeAK8);
    h_n_AK4_jets->Fill(sizeAK4);

    float nAK8bjets = 0;
    float nAK4bjets = 0;

    //Loop through AK4 jets to fill basic plots
    for( size_t j = 0; j < sizeAK4; j++ )
      {
	//Fill plots with parton Flavour
	int partonFlavour = -1;
	if( isMiniAOD == 0 ) partonFlavour = abs((*jets)[j].partonFlavour());
	
	if( isMiniAOD == 1 ) partonFlavour = abs((*jetPartonFlavour)[j]);
	
	//Fill bjet plots
	if( partonFlavour == 5 ) {
	  nAK4bjets++;
	  TLorentzVector AK4;
	  if( isMiniAOD == 0 ) AK4.SetPtEtaPhiM((*jets)[j].pt(), (*jets)[j].eta(), (*jets)[j].phi(), (*jets)[j].mass());
	  
	  if( isMiniAOD == 1 ) AK4.SetPtEtaPhiM((*jetPt)[j], (*jetEta)[j], (*jetPhi)[j], (*jetMass)[j]);
	  
	  float csvAK4 = -10;
	  if( isMiniAOD == 0 ) csvAK4 = (*jets)[i].bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags");
	  if( isMiniAOD == 1 ) csvAK4 = (*jetCSV)[i];

	  h_csv_all_true_bjet_AK4->Fill(csvAK4);
	  h_eta_all_true_bjet_AK4->Fill(AK4.Eta());
	  h_pt_all_true_bjet_AK4->Fill(AK4.Pt());
	}
      }

    
    for( size_t i = 0; i < sizeAK8; i++) {
	int partonFlavour = -1;
	if( isMiniAOD == 0 ) partonFlavour = abs((*ak8jets)[i].partonFlavour());
	
	if( isMiniAOD == 1 ) partonFlavour = abs((*jetAK8PartonFlavour)[i]);
	
	if( partonFlavour == 5 ) {
	  nAK8bjets++;

	  TLorentzVector AK8;
	  if(isMiniAOD == 0) AK8.SetPtEtaPhiM((*ak8jets)[i].pt(), (*ak8jets)[i].eta(), (*ak8jets)[i].phi(), (*ak8jets)[i].mass());
	  if(isMiniAOD == 1) AK8.SetPtEtaPhiM((*jetAK8Pt)[i],(*jetAK8Eta)[i],(*jetAK8Phi)[i],(*jetAK8Mass)[i]);

	  float csvAK8 = -10;
	  if( isMiniAOD == 0 ) csvAK8 = (*ak8jets)[i].bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags");
	  if( isMiniAOD == 1 ) csvAK8 = (*jetAK8CSV)[i];

	  h_eta_all_true_bjet_AK8->Fill(AK8.Eta());
	  h_csv_all_true_bjet_AK8->Fill(csvAK8);
	  h_pt_all_true_bjet_AK8->Fill(AK8.Pt());

	}
    }

    //Fill number of AK8, AK4 MC-true bjets and number of events
    h_n_AK8_bjets->Fill(nAK8bjets);
    h_n_AK4_bjets->Fill(nAK4bjets);
    h_event_count->Fill(0);
      
    //Begin Scale Factors Conversion
    //Loop through AK8 jets
    for( size_t i = 0; i < sizeAK8; i++)
      {
	int partonFlavour = -1;

	if( isMiniAOD == 0 ) partonFlavour = abs((*ak8jets)[i].partonFlavour());
	if( isMiniAOD == 1 ) partonFlavour = abs((*jetAK8PartonFlavour)[i]);

	//Select only MC-true bjets
	if( partonFlavour == 5 ) {
	  TLorentzVector AK8Raw;
	  if(isMiniAOD == 0) AK8Raw.SetPtEtaPhiM((*ak8jets)[i].pt(), (*ak8jets)[i].eta(), (*ak8jets)[i].phi(), (*ak8jets)[i].mass());
	  if(isMiniAOD == 1) AK8Raw.SetPtEtaPhiM((*jetAK8Pt)[i],(*jetAK8Eta)[i],(*jetAK8Phi)[i],(*jetAK8Mass)[i]);

	  float csvAK8 = -10;
	  if( isMiniAOD == 0 ) csvAK8 = (*ak8jets)[i].bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags");
	  if( isMiniAOD == 1 ) csvAK8 = (*jetAK8CSV)[i];

	  //Add Jet Corrections to AK8 jets
	  double JEC = 1;
	  if( isMiniAOD == 0 ) {
	    JetCorrector->setJetPt(AK8Raw.Pt());
	    JetCorrector->setJetEta( AK8Raw.Eta() );
	    JetCorrector->setJetPhi( AK8Raw.Phi() );
	    JetCorrector->setJetE( AK8Raw.E() );
	    JetCorrector->setRho( *rho );
	    JetCorrector->setNPV( vertices->size() );
	    JetCorrector->setJetA((*ak8jets)[i].jetArea());
	    
	    JEC = JetCorrector->getCorrection();
	  }
	  
	  TLorentzVector AK8 = AK8Raw*JEC;

	  //Intilize AK4 variables
	  float deltaRMin = 1000;
	  float deltaR2ndMin = 2000;
	  
	  int ak4index = 0;
	  
	  int numMatches = 0;
	  
	  float ptAK4 = 0;
	  float csvAK4 = 0;
	  float etaAK4 = 0;

	  //Loop through AK4 jets within AK8 loop to find jet "matches"
	  for( size_t j = 0; j < sizeAK4; j++ )
	  {

	    int partonFlavour = -1;
	    if( isMiniAOD == 0 ) partonFlavour = abs((*jets)[j].partonFlavour());

	    if( isMiniAOD == 1 ) partonFlavour = abs((*jetPartonFlavour)[j]);

	    //Select only MC-true AK4 bjets
	    if( partonFlavour == 5 ) {
		TLorentzVector AK4;
		if( isMiniAOD == 0 ) AK4.SetPtEtaPhiM((*jets)[j].pt(), (*jets)[j].eta(), (*jets)[j].phi(), (*jets)[j].mass());

		if( isMiniAOD == 1 ) AK4.SetPtEtaPhiM((*jetPt)[j], (*jetEta)[j], (*jetPhi)[j], (*jetMass)[j]);
	      
		//Find minimum and second minimum delta R
		if( AK8.DeltaR(AK4) < deltaRMin ) {
		  deltaR2ndMin = deltaRMin;
		  ptAK4 = AK4.Pt();
		  etaAK4 = AK4.Eta();
		  deltaRMin = AK8.DeltaR(AK4);	
		  if( isMiniAOD == 0 ) csvAK4 = (*jets)[j].bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags");
		  if( isMiniAOD == 1 ) csvAK4 = (*jetCSV)[j];
		}
		else if( AK8.DeltaR(AK4) < deltaR2ndMin) {
		  deltaR2ndMin = AK8.DeltaR(AK4);
		}
		
		//Find number of jet matches for each AK8 jet
		if( AK8.DeltaR(AK4) < .3 ) numMatches++;
	
		//Fill Delta R plot
		h_delta_r->Fill(AK8.DeltaR(AK4));
		ak4index++;
	      }
	  
	    }

	  //Fill matching plots
	  if( true ) {
	    h_delta_r_min->Fill(deltaRMin);
	    h_delta_r_2nd_min->Fill(deltaR2ndMin);
	    h_delta_r_1st2nd_min->Fill(deltaRMin);
	    h_delta_r_1st2nd_min->Fill(deltaR2ndMin);
	    h_delta_r_1st_v_2nd_min->Fill(deltaRMin,deltaR2ndMin);
	    
	    h_num_matches_foreach_AK8->Fill(numMatches);
	  
	    //Fill matched jet plots for conversion
	    if( numMatches == 1 ) {
	      if( isMiniAOD == 0 )h_npv_matched_jet_events->Fill(vertices->size());
	      if( isMiniAOD == 1 )h_npv_matched_jet_events->Fill(*npv);	    
	      h_pt_true_bjet_with_match_AK8->Fill(AK8.Pt());
	      h_pt_true_bjet_with_match_AK4->Fill(ptAK4);
	      h_csv_AK8_match->Fill(csvAK8);
	      h_csv_AK4_match->Fill(csvAK4);
	      h_denom_AK4->Fill(ptAK4);
	      h_denom_AK8->Fill(AK8.Pt());
	      h_denom_AK4_bin_with_AK8pt->Fill(AK8.Pt());
	      h_denom_AK8_bin_with_AK4pt->Fill(ptAK4);
	      h_eta_true_bjet_with_match_AK8->Fill(AK8.Eta());
	      h_eta_true_bjet_with_match_AK4->Fill(etaAK4);
	      h_matched_AK4pt_vs_AK8pt->Fill( ptAK4, AK8.Pt());

	      //Fill plots to calculate errors
	      if( csvAK4 > .8 && csvAK8 > .8 ) {
		h_matchedjetAK8_pt_pass_csv8ANDcsv4_cut->Fill(AK8.Pt());
		h_matchedjetAK4_pt_pass_csv8ANDcsv4_cut->Fill(ptAK4);
	      h_matched_AK4pt_vs_AK8pt_AK8AK4csv_cut->Fill( ptAK4, AK8.Pt());
	      }
	      else if( csvAK4 > .8 && !(csvAK8 > .8) ) {
		h_matchedjetAK8_pt_pass_ONLYcsv4_cut->Fill(AK8.Pt());
		h_matchedjetAK4_pt_pass_ONLYcsv4_cut->Fill(ptAK4);
		h_matched_AK4pt_vs_AK8pt_AK4csv_cut->Fill( ptAK4, AK8.Pt());	     
	      }
	      else if( !(csvAK4 > .8) && csvAK8 > .8 ) {
		h_matchedjetAK8_pt_pass_ONLYcsv8_cut->Fill(AK8.Pt());
		h_matchedjetAK4_pt_pass_ONLYcsv8_cut->Fill(ptAK4);
		h_matched_AK4pt_vs_AK8pt_AK8csv_cut->Fill( ptAK4, AK8.Pt());
	      }
	      
	      if( csvAK4 > .8 ) h_num_AK4->Fill(ptAK4);
	      if( csvAK4 > .8 ) h_num_AK4_bin_with_AK8pt->Fill(AK8.Pt());
	      if( csvAK8 > .8 ) h_num_AK8->Fill(AK8.Pt());
	      if( csvAK8 > .8 ) h_num_AK8_bin_with_AK4pt->Fill(ptAK4);
	    }
	    ak8index++;      
	  }
	  
	}
      }

}


//define this as a plug-in
DEFINE_FWK_MODULE(ConvertBtaggingSF);


