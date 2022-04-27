
//double x_cut[11] = {1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.,2.1,2.2};
//double y_cut[11] = {3.,2.9,2.8,2.7,2.6,2.5,2.4,2.3,2.2,2.1,2.};
double x_cut[30] = {0.2,0.4,0.6,0.8,1.,1.2,1.4,1.6,1.8,2.,2.2,2.4,2.6,2.8,3.,3.2,3.4,3.6,3.8,4.,4.2,4.4,4.6,4.8,5.,5.2,5.4,5.6,5.8,6.};
double y_cut[30] = {3.,2.9,2.8,2.7,2.6,2.5,2.4,2.3,2.2,2.1,2.,1.9,1.8,1.7,1.6,1.5,1.4,1.3,1.2,1.1,1.,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1};

//const char * x_label[11] = {"1.2","1.3","1.4","1.5","1.6","1.7","1.8","1.9","2.","2.1","2.2"};
//const char * y_label[11] = {"3.","2.9","2.8","2.7","2.6","2.5","2.4","2.3","2.2","2.1","2."};

const char * x_label[30] = {"0.2","0.4","0.6","0.8","1.","1.2","1.4","1.6","1.8","2.","2.2","2.4","2.6","2.8","3.","3.2","3.4","3.6","3.8","4.","4.2","4.4","4.6","4.8","5.","5.2","5.4","5.6","5.8","6."};
const char * y_label[30] = {"3.","2.9","2.8","2.7","2.6","2.5","2.4","2.3","2.2","2.1","2.","1.9","1.8","1.7","1.6","1.5","1.4","1.3","1.2","1.1","1.","0.9","0.8","0.7","0.6","0.5","0.4","0.3","0.2","0.1"};

void make_plot_2d_ver2(){
	gStyle->SetOptStat(0);
	gStyle->SetPaintTextFormat("5.2f");

	TFile *_file0 = TFile::Open("../preselected_Run2018.root");
	TTree * tree = (TTree*)_file0->Get("Events");



	TFile *_file1 = TFile::Open("../preselected_ggH_HToUps1SG_M125_NNPDF31_TuneCP5_13TeV-powheg-pythia8_2018.root");
	TFile *_file2 = TFile::Open("../preselected_ggH_HToUps2SG_M125_NNPDF31_TuneCP5_13TeV-powheg-pythia8_2018.root");
	TFile *_file3 = TFile::Open("../preselected_ggH_HToUps3SG_M125_NNPDF31_TuneCP5_13TeV-powheg-pythia8_2018.root");
	TFile *_file4 = TFile::Open("../preselected_ZToUpsilon1SGamma_TuneCP5_13TeV-amcatnloFXFX-pythia8_2018.root");
	TFile *_file5 = TFile::Open("../preselected_ZToUpsilon2SGamma_TuneCP5_13TeV-amcatnloFXFX-pythia8_2018.root");
	TFile *_file6 = TFile::Open("../preselected_ZToUpsilon3SGamma_TuneCP5_13TeV-amcatnloFXFX-pythia8_2018.root");

	TTree * treeZ3 = (TTree*)_file6->Get("Events");
	TTree * treeZ2 = (TTree*)_file5->Get("Events");
	TTree * treeZ1 = (TTree*)_file4->Get("Events");
	TTree * treeH3 = (TTree*)_file3->Get("Events");
	TTree * treeH2 = (TTree*)_file2->Get("Events");
	TTree * treeH1 = (TTree*)_file1->Get("Events");
/*
	Double_t var_w_H1;
	treeH1->SetBranchAddress("weight",&var_w_H1);
	Double_t var_w_H2;
	treeH2->SetBranchAddress("weight",&var_w_H2);
	Double_t var_w_H3;
	treeH3->SetBranchAddress("weight",&var_w_H3);
	Double_t var_w_Z1;
	treeZ1->SetBranchAddress("weight",&var_w_Z1);
	Double_t var_w_Z2;
	treeZ2->SetBranchAddress("weight",&var_w_Z2);
	Double_t var_w_Z3;
	treeZ3->SetBranchAddress("weight",&var_w_Z3);
*/


	TH2F *h2_H = new TH2F("h2_H",";|#Delta#eta|<;|#Delta#phi|>",30,0.15,6.05,30,0.05,3.05);
	TH2F *h2_Z = new TH2F("h2_Z",";|#Delta#eta|<;|#Delta#phi|>",30,0.15,6.05,30,0.05,3.05);

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

	for (int ii=1;ii<=30;ii++) h2_H->GetXaxis()->SetBinLabel(ii, x_label[ii-1]);
	for (int ii=1;ii<=30;ii++) h2_H->GetYaxis()->SetBinLabel(ii, y_label[ii-1]);
	for (int ii=1;ii<=30;ii++) h2_Z->GetXaxis()->SetBinLabel(ii, x_label[ii-1]);
	for (int ii=1;ii<=30;ii++) h2_Z->GetYaxis()->SetBinLabel(ii, y_label[ii-1]);
	for(int i=1;i<=30;i++){
		for(int j=1;j<=30;j++){
			string cut("");
			cut = Form("boson_mass > 60. && boson_mass < 150. && upsilon_mass > 8. && upsilon_mass < 11. && delta_eta_upsilon_photon < %f && delta_phi_upsilon_photon > %f",x_cut[i-1],y_cut[j-1]);
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

			h2_H->SetBinContent(i,j,((events_H1+events_H2+events_H3)/sqrt((double)tree->GetEntries(cut_c)))*1000000);
			h2_Z->SetBinContent(i,j,((events_Z1+events_Z2+events_Z3)/sqrt((double)tree->GetEntries(cut_c)))*100);
		}
	}

	Int_t MaxBinH = h2_H->GetMaximumBin();
	Int_t xH,yH,zH;
	h2_H->GetBinXYZ(MaxBinH, xH, yH, zH);
	std::cout << "xH: " << x_cut[xH-1] << "; yH: " << y_cut[yH-1] << std::endl;

	Int_t MaxBinZ = h2_Z->GetMaximumBin();
	Int_t xZ,yZ,zZ;
	h2_Z->GetBinXYZ(MaxBinZ, xZ, yZ, zZ);
	std::cout << "xZ: " << x_cut[xZ-1] << "; yZ: " << y_cut[yZ-1] << std::endl;

	h2_H->SetMarkerSize(0.5);
	h2_Z->SetMarkerSize(0.5);

	TCanvas *cH = new TCanvas("cH","",0,0,4500,4500);
	h2_H->Draw("COLZ text");
	cH->SaveAs("H_upsilon_boson_window_large_ver2.png");

	TCanvas *cZ = new TCanvas("cZ","",0,0,2500,2500);
	h2_Z->Draw("COLZ text");
	cZ->SaveAs("Z_upsilon_boson_window_large_ver2.png");

}
