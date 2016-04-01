// -*- C++ -*-
//
// Package:    BTaggingEffAnalyzer
// Class:      BTaggingEffAnalyzer
// 
/**\class BTaggingEffAnalyzer BTaggingEffAnalyzer.cc Analysis/EDSHyFT/plugins/BTaggingEffAnalyzer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Dinko Ferencek
//         Created:  Thu Oct  4 20:25:54 CDT 2012
// $Id: BTaggingEffAnalyzer.cc,v 1.1.2.1 2012/10/05 06:11:47 ferencek Exp $
//
//


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
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "CondFormats/JetMETObjects/interface/FactorizedJetCorrector.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"

using namespace edm;
using namespace std;

//
// class declaration
//

class BTaggingEffAnalyzer : public EDAnalyzer {
   public:
      explicit BTaggingEffAnalyzer(const ParameterSet&);
      ~BTaggingEffAnalyzer();

      static void fillDescriptions(ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() ;
      virtual void analyze(const Event&, const EventSetup&);
      virtual void endJob() ;

      virtual void beginRun(Run const&, EventSetup const&);
      virtual void endRun(Run const&, EventSetup const&);
      virtual void beginLuminosityBlock(LuminosityBlock const&, EventSetup const&);
      virtual void endLuminosityBlock(LuminosityBlock const&, EventSetup const&);

      // ----------member data ---------------------------
  EDGetTokenT<pat::JetCollection> jetToken_;
  EDGetTokenT<vector<float>> jetPt_;
  EDGetTokenT<vector<float>> jetEta_;
  EDGetTokenT<vector<float>> jetPhi_;
  EDGetTokenT<vector<float>> jetPartonFlavor_;
  EDGetTokenT<vector<float>> jetCSV_;
  EDGetTokenT<vector<float>> jetArea_;

  EDGetTokenT<double> rhoToken_;

      std::string   discriminatorTag;
      double  discriminatorValue;
      int     ptNBins;
      double  ptMin;
      double  ptMax;
      int     etaNBins;
      double  etaMin;
      double  etaMax;

      //Jet Corrector  
      vector<JetCorrectorParameters> jetPar;
      FactorizedJetCorrector * JetCorrector;

 
      int     isMiniAOD;
      vector<float> *jetPt = new std::vector<float>();
      vector<float> *jetEta = new std::vector<float>();
      vector<float> *jetCSV = new std::vector<float>();
      vector<float> *jetPhi = new std::vector<float>();
    
      int     Njets = 0;
      Service<TFileService>  fs;
      TH2D * h2_BTaggingEff_Denom_b;
      TH2D * h2_BTaggingEff_Denom_c;
      TH2D * h2_BTaggingEff_Denom_udsg;
      TH2D * h2_BTaggingEff_Num_b;
      TH2D * h2_BTaggingEff_Num_c;
      TH2D * h2_BTaggingEff_Num_udsg;
};

//
// constants, enums and typedefs
//
typedef std::vector<pat::Jet> PatJetCollection;

//
// static data member definitions
//

//
// constructors and destructor
//
BTaggingEffAnalyzer::BTaggingEffAnalyzer(const ParameterSet& iConfig) :

  jetToken_(consumes<pat::JetCollection>(iConfig.getParameter<InputTag>("JetsTag"))),
  jetPt_(consumes<vector<float>>(iConfig.getParameter<InputTag>("JetPtTag"))),
  jetEta_(consumes<vector<float>>(iConfig.getParameter<InputTag>("JetEtaTag"))),
  jetPhi_(consumes<vector<float>>(iConfig.getParameter<InputTag>("JetPhiTag"))),
  jetPartonFlavor_(consumes<vector<float>>(iConfig.getParameter<InputTag>("JetPartonFlavorTag"))),
  jetCSV_(consumes<vector<float>>(iConfig.getParameter<InputTag>("JetCSVTag")))
 {
     //now do what ever initialization is needed
  
   isMiniAOD = iConfig.getParameter<int>("isMiniAOD");
   discriminatorTag = iConfig.getParameter<std::string>("DiscriminatorTag");
   discriminatorValue = iConfig.getParameter<double>("DiscriminatorValue");
   ptNBins = iConfig.getParameter<int>("PtNBins");
   ptMin = iConfig.getParameter<double>("PtMin");
   ptMax = iConfig.getParameter<double>("PtMax");
   etaNBins = iConfig.getParameter<int>("EtaNBins");
   etaMin = iConfig.getParameter<double>("EtaMin");
   etaMax = iConfig.getParameter<double>("EtaMax");
     
   h2_BTaggingEff_Denom_b    = fs->make<TH2D>("h2_BTaggingEff_Denom_b", ";p_{T} [GeV];#eta", ptNBins, ptMin, ptMax, etaNBins, etaMin, etaMax);
   h2_BTaggingEff_Denom_c    = fs->make<TH2D>("h2_BTaggingEff_Denom_c", ";p_{T} [GeV];#eta", ptNBins, ptMin, ptMax, etaNBins, etaMin, etaMax);
   h2_BTaggingEff_Denom_udsg = fs->make<TH2D>("h2_BTaggingEff_Denom_udsg", ";p_{T} [GeV];#eta", ptNBins, ptMin, ptMax, etaNBins, etaMin, etaMax);
   h2_BTaggingEff_Num_b    = fs->make<TH2D>("h2_BTaggingEff_Num_b", ";p_{T} [GeV];#eta", ptNBins, ptMin, ptMax, etaNBins, etaMin, etaMax);
   h2_BTaggingEff_Num_c    = fs->make<TH2D>("h2_BTaggingEff_Num_c", ";p_{T} [GeV];#eta", ptNBins, ptMin, ptMax, etaNBins, etaMin, etaMax);
   h2_BTaggingEff_Num_udsg = fs->make<TH2D>("h2_BTaggingEff_Num_udsg", ";p_{T} [GeV];#eta", ptNBins, ptMin, ptMax, etaNBins, etaMin, etaMax);

   //Jet Correction Files
   vector<string> jecPayloadNames_;
   jecPayloadNames_.push_back("JECs/Summer15_25nsV6_MC_L1FastJet_AK4PFchs.txt");
   jecPayloadNames_.push_back("JECs/Summer15_25nsV6_MC_L2Relative_AK4PFchs.txt");
   jecPayloadNames_.push_back("JECs/Summer15_25nsV6_MC_L3Absolute_AK4PFchs.txt");
   
   for ( vector<string>::const_iterator payloadBegin = jecPayloadNames_.begin(), payloadEnd = jecPayloadNames_.end(), ipayload = payloadBegin; ipayload != payloadEnd; ++ipayload ) {
     JetCorrectorParameters pars(*ipayload);
     jetPar.push_back(pars);
   }
   JetCorrector = new FactorizedJetCorrector(jetPar);

}


BTaggingEffAnalyzer::~BTaggingEffAnalyzer()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
BTaggingEffAnalyzer::analyze(const Event& iEvent, const EventSetup& iSetup)
{
  Handle<pat::JetCollection> jets;
  Handle<vector<float> > jetPt;
  Handle<vector<float> > jetEta;
  Handle<vector<float> > jetPhi;
  Handle<vector<float> > jetPartonFlavor;
  Handle<vector<float> > jetCSV;
  Handle<double> rho;  
  if( isMiniAOD == 0 ) {
    iEvent.getByToken(jetToken_, jets);
    Njets = jets->size();
    iEvent.getByToken( rhoToken_, rho );
  }
  if( isMiniAOD == 1 ) {
    iEvent.getByToken(jetPt_, jetPt);
    iEvent.getByToken(jetEta_, jetEta);
    iEvent.getByToken(jetPhi_, jetPhi);
    iEvent.getByToken(jetPartonFlavor_, jetPartonFlavor);
    iEvent.getByToken(jetCSV_, jetCSV);
    Njets = jetPt->size();
  }

  // loop over jets
  for( int i = 0; i < Njets; i++)
  {
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
    
    int partonFlavor = -10;
    float pt = Jet.Pt();
    float eta = Jet.Eta();
    float csv = -1000;


    if( isMiniAOD == 0 ){
      partonFlavor = (*jets)[i].partonFlavour();
      csv = (*jets)[i].bDiscriminator(discriminatorTag.c_str());
    }
    if( isMiniAOD == 1) {
      partonFlavor = (*jetPartonFlavor)[i];
      csv = (*jetCSV)[i];
    }

    cout << "Jet: " << i << ", pt: " << pt << ", eta: " << eta << ", csv: " << csv << endl;

    if( abs(partonFlavor)==5 )
    {
      h2_BTaggingEff_Denom_b->Fill(pt, eta);
      if( csv >= discriminatorValue ) h2_BTaggingEff_Num_b->Fill(pt, eta);
    }
    else if( abs(partonFlavor)==4 )
    {
      h2_BTaggingEff_Denom_c->Fill(pt, eta);
      if( csv >= discriminatorValue ) h2_BTaggingEff_Num_c->Fill(pt, eta);
    }
    else
    {
      h2_BTaggingEff_Denom_udsg->Fill(pt, eta);
      if( csv >= discriminatorValue ) h2_BTaggingEff_Num_udsg->Fill(pt, eta);
    }
  }
}


// ------------ method called once each job just before starting event loop  ------------
void 
BTaggingEffAnalyzer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
BTaggingEffAnalyzer::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
void 
BTaggingEffAnalyzer::beginRun(Run const&, EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
BTaggingEffAnalyzer::endRun(Run const&, EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
BTaggingEffAnalyzer::beginLuminosityBlock(LuminosityBlock const&, EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
BTaggingEffAnalyzer::endLuminosityBlock(LuminosityBlock const&, EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
BTaggingEffAnalyzer::fillDescriptions(ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(BTaggingEffAnalyzer);
