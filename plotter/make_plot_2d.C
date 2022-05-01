
//double x_cut[11] = {1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.,2.1,2.2};
//double y_cut[11] = {3.,2.9,2.8,2.7,2.6,2.5,2.4,2.3,2.2,2.1,2.};
double deltaEta_cut[30] = {0.2,0.4,0.6,0.8,1.,1.2,1.4,1.6,1.8,2.,2.2,2.4,2.6,2.8,3.,3.2,3.4,3.6,3.8,4.,4.2,4.4,4.6,4.8,5.,5.2,5.4,5.6,5.8,6.};
double deltaPhi_cut[30] = {3.,2.9,2.8,2.7,2.6,2.5,2.4,2.3,2.2,2.1,2.,1.9,1.8,1.7,1.6,1.5,1.4,1.3,1.2,1.1,1.,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1};
double deltaR_cut[30] = {0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.,2.1,2.2,2.3,2.4,2.4,2.5,2.6,2.7,2.9,3.};

//const char * x_label[11] = {"1.2","1.3","1.4","1.5","1.6","1.7","1.8","1.9","2.","2.1","2.2"};
//const char * y_label[11] = {"3.","2.9","2.8","2.7","2.6","2.5","2.4","2.3","2.2","2.1","2."};

const char * deltaEta_label[30] = {"0.2","0.4","0.6","0.8","1.","1.2","1.4","1.6","1.8","2.","2.2","2.4","2.6","2.8","3.","3.2","3.4","3.6","3.8","4.","4.2","4.4","4.6","4.8","5.","5.2","5.4","5.6","5.8","6."};
const char * deltaPhi_label[30] = {"3.","2.9","2.8","2.7","2.6","2.5","2.4","2.3","2.2","2.1","2.","1.9","1.8","1.7","1.6","1.5","1.4","1.3","1.2","1.1","1.","0.9","0.8","0.7","0.6","0.5","0.4","0.3","0.2","0.1"};
const char * deltaR_label[30] = {"0.1","0.2","0.3","0.4","0.5","0.6","0.7","0.8","0.9","1.","1.1","1.2","1.3","1.4","1.5","1.6","1.7","1.8","1.9","2.","2.1","2.2","2.3","2.4","2.4","2.5","2.6","2.7","2.9","3."};

void make_plot_2d(){
	gStyle->SetOptStat(0);
	gStyle->SetPaintTextFormat("5.2f");

	TFile *_file0 = TFile::Open("../preselected_Run2018.root");
	TTree * tree = (TTree*)_file0->Get("Events");

	TFile *_file1 = TFile::Open("outputs/preselected_ggH_HToUps1SG_M125_NNPDF31_TuneCP5_13TeV-powheg-pythia8_2018.root");
	TFile *_file2 = TFile::Open("outputs/preselected_ggH_HToUps2SG_M125_NNPDF31_TuneCP5_13TeV-powheg-pythia8_2018.root");
	TFile *_file3 = TFile::Open("outputs/preselected_ggH_HToUps3SG_M125_NNPDF31_TuneCP5_13TeV-powheg-pythia8_2018.root");
	TFile *_file4 = TFile::Open("outputs/preselected_ZToUpsilon1SGamma_TuneCP5_13TeV-amcatnloFXFX-pythia8_2018.root");
	TFile *_file5 = TFile::Open("outputs/preselected_ZToUpsilon2SGamma_TuneCP5_13TeV-amcatnloFXFX-pythia8_2018.root");
	TFile *_file6 = TFile::Open("outputs/preselected_ZToUpsilon3SGamma_TuneCP5_13TeV-amcatnloFXFX-pythia8_2018.root");

	TTree * treeZ3 = (TTree*)_file6->Get("Events");
	TTree * treeZ2 = (TTree*)_file5->Get("Events");
	TTree * treeZ1 = (TTree*)_file4->Get("Events");
	TTree * treeH3 = (TTree*)_file3->Get("Events");
	TTree * treeH2 = (TTree*)_file2->Get("Events");
	TTree * treeH1 = (TTree*)_file1->Get("Events");

	TH2F *h2_eta_phi_H = new TH2F("h2_eta_phi_H",";|#Delta#eta|<;|#Delta#phi|>;significance",30,0.15,6.05,30,0.05,3.05);
	TH2F *h2_eta_phi_Z = new TH2F("h2_eta_phi_Z",";|#Delta#eta|<;|#Delta#phi|>;significance",30,0.15,6.05,30,0.05,3.05);
	TH2F *h2_eta_R_H = new TH2F("h2_eta_R_H",";|#Delta#eta|<;#Delta R>;significance",30,0.15,6.05,30,0.05,3.05);
	TH2F *h2_eta_R_Z = new TH2F("h2_eta_R_Z",";|#Delta#eta|<;#Delta R>;significance",30,0.15,6.05,30,0.05,3.05);
	TH2F *h2_R_phi_H = new TH2F("h2_R_phi_H",";#Delta R>;|#Delta#phi|>;significance",30,0.05,3.05,30,0.05,3.05);
	TH2F *h2_R_phi_Z = new TH2F("h2_R_phi_Z",";#Delta R>;|#Delta#phi|>;significance",30,0.05,3.05,30,0.05,3.05);

	treeH1->Draw("weight","boson_mass > 60. && boson_mass < 150. && upsilon_mass > 8. && upsilon_mass < 11.");
	TH1 *htempH1 = (TH1*)gPad->GetPrimitive("htemp");
	double scale_H1 = htempH1->GetMean();
	treeH2->Draw("weight","boson_mass > 60. && boson_mass < 150. && upsilon_mass > 8. && upsilon_mass < 11.");
	TH1 *htempH2 = (TH1*)gPad->GetPrimitive("htemp");
	double scale_H2 = htempH2->GetMean();
	treeH3->Draw("weight","boson_mass > 60. && boson_mass < 150. && upsilon_mass > 8. && upsilon_mass < 11.");
	TH1 *htempH3 = (TH1*)gPad->GetPrimitive("htemp");
	double scale_H3 = htempH3->GetMean();
	treeZ1->Draw("weight","boson_mass > 60. && boson_mass < 150. && upsilon_mass > 8. && upsilon_mass < 11.");
	TH1 *htempZ1 = (TH1*)gPad->GetPrimitive("htemp");
	double scale_Z1 = htempZ1->GetMean();
	treeZ2->Draw("weight","boson_mass > 60. && boson_mass < 150. && upsilon_mass > 8. && upsilon_mass < 11.");
	TH1 *htempZ2 = (TH1*)gPad->GetPrimitive("htemp");
	double scale_Z2 = htempZ2->GetMean();
	treeZ3->Draw("weight","boson_mass > 60. && boson_mass < 150. && upsilon_mass > 8. && upsilon_mass < 11.");
	TH1 *htempZ3 = (TH1*)gPad->GetPrimitive("htemp");
	double scale_Z3 = htempZ3->GetMean();

	for (int ii=1;ii<=30;ii++) h2_eta_phi_H->GetXaxis()->SetBinLabel(ii, deltaEta_label[ii-1]);
	for (int ii=1;ii<=30;ii++) h2_eta_phi_H->GetYaxis()->SetBinLabel(ii, deltaPhi_label[ii-1]);
	for (int ii=1;ii<=30;ii++) h2_eta_phi_Z->GetXaxis()->SetBinLabel(ii, deltaEta_label[ii-1]);
	for (int ii=1;ii<=30;ii++) h2_eta_phi_Z->GetYaxis()->SetBinLabel(ii, deltaPhi_label[ii-1]);

	for (int ii=1;ii<=30;ii++) h2_eta_R_H->GetXaxis()->SetBinLabel(ii, deltaEta_label[ii-1]);
	for (int ii=1;ii<=30;ii++) h2_eta_R_H->GetYaxis()->SetBinLabel(ii, deltaR_label[ii-1]);
	for (int ii=1;ii<=30;ii++) h2_eta_R_Z->GetXaxis()->SetBinLabel(ii, deltaEta_label[ii-1]);
	for (int ii=1;ii<=30;ii++) h2_eta_R_Z->GetYaxis()->SetBinLabel(ii, deltaR_label[ii-1]);

	for (int ii=1;ii<=30;ii++) h2_R_phi_H->GetXaxis()->SetBinLabel(ii, deltaR_label[ii-1]);
	for (int ii=1;ii<=30;ii++) h2_R_phi_H->GetYaxis()->SetBinLabel(ii, deltaPhi_label[ii-1]);
	for (int ii=1;ii<=30;ii++) h2_R_phi_Z->GetXaxis()->SetBinLabel(ii, deltaR_label[ii-1]);
	for (int ii=1;ii<=30;ii++) h2_R_phi_Z->GetYaxis()->SetBinLabel(ii, deltaPhi_label[ii-1]);

	for(int i=1;i<=30;i++){
		for(int j=1;j<=30;j++){
			std::cout << "(i,j): " << i << "," << j << std::endl;
			double deltaPhicut = 0;
			double deltaEtacut = 0;
			double deltaRcut = 0;
			for(int plt=1;plt<=3;plt++){
				if(plt==1){
					deltaEtacut = deltaEta_cut[i-1];
					deltaPhicut = deltaPhi_cut[j-1];
					deltaRcut = 0.;
				}
				if(plt==2){
					deltaEtacut = deltaEta_cut[i-1];
					deltaPhicut = 0.;
					deltaRcut = deltaR_cut[j-1];
				}
				if(plt==3){
					deltaEtacut = 99.;
					deltaPhicut = deltaPhi_cut[j-1];
					deltaRcut = deltaR_cut[i-1];
				}

				string cut("");
				cut = Form("boson_mass > 60. && boson_mass < 150. && upsilon_mass > 8. && upsilon_mass < 11. && delta_eta_upsilon_photon < %f && delta_phi_upsilon_photon > %f && delta_r_upsilon_photon > %f",deltaEtacut,deltaPhicut,deltaRcut);
				const char * cut_c = cut.c_str();

				treeH1->Draw("weight",cut_c);
				TH1 *htempH1n = (TH1*)gPad->GetPrimitive("htemp");
				htempH1n->Scale(scale_H1);
				double events_H1 = htempH1n->Integral();
				treeH2->Draw("weight",cut_c);
				TH1 *htempH2n = (TH1*)gPad->GetPrimitive("htemp");
				htempH2n->Scale(scale_H2);
				double events_H2 = htempH2n->Integral();
				treeH3->Draw("weight",cut_c);
				TH1 *htempH3n = (TH1*)gPad->GetPrimitive("htemp");
				htempH3n->Scale(scale_H3);
				double events_H3 = htempH3n->Integral();
				treeZ1->Draw("weight",cut_c);
				TH1 *htempZ1n = (TH1*)gPad->GetPrimitive("htemp");
				htempZ1n->Scale(scale_Z1);
				double events_Z1 = htempZ1n->Integral();
				treeZ2->Draw("weight",cut_c);
				TH1 *htempZ2n = (TH1*)gPad->GetPrimitive("htemp");
				htempZ2n->Scale(scale_Z2);
				double events_Z2 = htempZ2n->Integral();
				treeZ3->Draw("weight",cut_c);
				TH1 *htempZ3n = (TH1*)gPad->GetPrimitive("htemp");
				htempZ3n->Scale(scale_Z3);
				double events_Z3 = htempZ3n->Integral();

				if(plt==1){
					h2_eta_phi_H->SetBinContent(i,j,((events_H1+events_H2+events_H3)/sqrt((double)tree->GetEntries(cut_c)))*1000000);
					h2_eta_phi_Z->SetBinContent(i,j,((events_Z1+events_Z2+events_Z3)/sqrt((double)tree->GetEntries(cut_c)))*100);
				}
				if(plt==2){
					h2_eta_R_H->SetBinContent(i,j,((events_H1+events_H2+events_H3)/sqrt((double)tree->GetEntries(cut_c)))*1000000);
					h2_eta_R_Z->SetBinContent(i,j,((events_Z1+events_Z2+events_Z3)/sqrt((double)tree->GetEntries(cut_c)))*100);
				}
				if(plt==3){
					h2_R_phi_H->SetBinContent(i,j,((events_H1+events_H2+events_H3)/sqrt((double)tree->GetEntries(cut_c)))*1000000);
					h2_R_phi_Z->SetBinContent(i,j,((events_Z1+events_Z2+events_Z3)/sqrt((double)tree->GetEntries(cut_c)))*100);
				}
			}
		}
	}

	/*
	   Int_t MaxBinH = h2_eta_phi_H->GetMaximumBin();
	   Int_t xH,yH,zH;
	   h2_eta_phi_H->GetBinXYZ(MaxBinH, xH, yH, zH);
	   std::cout << "xH: " << deltaEta_cut[xH-1] << "; yH: " << deltaPhi_cut[yH-1] << std::endl;

	   Int_t MaxBinZ = h2_eta_phi_Z->GetMaximumBin();
	   Int_t xZ,yZ,zZ;
	   h2_eta_phi_Z->GetBinXYZ(MaxBinZ, xZ, yZ, zZ);
	   std::cout << "xZ: " << deltaEta_cut[xZ-1] << "; yZ: " << deltaPhi_cut[yZ-1] << std::endl;
	   */

	h2_eta_phi_H->SetMarkerSize(0.5);
	h2_eta_phi_Z->SetMarkerSize(0.5);
	h2_R_phi_H->SetMarkerSize(0.5);
	h2_R_phi_Z->SetMarkerSize(0.5);
	h2_eta_R_H->SetMarkerSize(0.5);
	h2_eta_R_Z->SetMarkerSize(0.5);



	TCanvas *cH = new TCanvas("cH","",0,0,6500,4500);
	h2_eta_phi_H->Draw("COLZ text");
	cH->SaveAs("plots/H_upsilon_boson_window_large_eta_phi_.png");
	cH->SaveAs("plots/H_upsilon_boson_window_large_eta_phi_.pdf");
	TCanvas *cZ = new TCanvas("cZ","",0,0,6500,4500);
	h2_eta_phi_Z->Draw("COLZ text");
	cZ->SaveAs("plots/Z_upsilon_boson_window_large_eta_phi_.png");
	cZ->SaveAs("plots/Z_upsilon_boson_window_large_eta_phi_.pdf");

	TCanvas *cH2 = new TCanvas("cH2","",0,0,6500,4500);
	h2_eta_R_H->Draw("COLZ text");
	cH2->SaveAs("plots/H_upsilon_boson_window_large_eta_R_.png");
	cH2->SaveAs("plots/H_upsilon_boson_window_large_eta_R_.pdf");
	TCanvas *cZ2 = new TCanvas("cZ2","",0,0,6500,4500);
	h2_eta_R_Z->Draw("COLZ text");
	cZ2->SaveAs("plots/Z_upsilon_boson_window_large_eta_R_.png");
	cZ2->SaveAs("plots/Z_upsilon_boson_window_large_eta_R_.pdf");

	TCanvas *cH3 = new TCanvas("cH3","",0,0,6500,4500);
	h2_R_phi_H->Draw("COLZ text");
	cH3->SaveAs("plots/H_upsilon_boson_window_large_R_phi_.png");
	cH3->SaveAs("plots/H_upsilon_boson_window_large_R_phi_.pdf");
	TCanvas *cZ3 = new TCanvas("cZ3","",0,0,6500,4500);
	h2_R_phi_Z->Draw("COLZ text");
	cZ3->SaveAs("plots/Z_upsilon_boson_window_large_R_phi_.png");
	cZ3->SaveAs("plots/Z_upsilon_boson_window_large_R_phi_.pdf");


}
