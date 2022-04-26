
// double x_cut[11] = {1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.,2.1,2.2};
// double y_cut[11] = {3.,2.9,2.8,2.7,2.6,2.5,2.4,2.3,2.2,2.1,2.};
double x_cut[30] = {0.2, 0.4, 0.6, 0.8, 1., 1.2, 1.4, 1.6, 1.8, 2., 2.2, 2.4, 2.6, 2.8, 3., 3.2, 3.4, 3.6, 3.8, 4., 4.2, 4.4, 4.6, 4.8, 5., 5.2, 5.4, 5.6, 5.8, 6.};
double y_cut[30] = {3., 2.9, 2.8, 2.7, 2.6, 2.5, 2.4, 2.3, 2.2, 2.1, 2., 1.9, 1.8, 1.7, 1.6, 1.5, 1.4, 1.3, 1.2, 1.1, 1., 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1};

// const char * x_label[11] = {"1.2","1.3","1.4","1.5","1.6","1.7","1.8","1.9","2.","2.1","2.2"};
// const char * y_label[11] = {"3.","2.9","2.8","2.7","2.6","2.5","2.4","2.3","2.2","2.1","2."};

const char *x_label[30] = {"0.2", "0.4", "0.6", "0.8", "1.", "1.2", "1.4", "1.6", "1.8", "2.", "2.2", "2.4", "2.6", "2.8", "3.", "3.2", "3.4", "3.6", "3.8", "4.", "4.2", "4.4", "4.6", "4.8", "5.", "5.2", "5.4", "5.6", "5.8", "6."};
const char *y_label[30] = {"3.", "2.9", "2.8", "2.7", "2.6", "2.5", "2.4", "2.3", "2.2", "2.1", "2.", "1.9", "1.8", "1.7", "1.6", "1.5", "1.4", "1.3", "1.2", "1.1", "1.", "0.9", "0.8", "0.7", "0.6", "0.5", "0.4", "0.3", "0.2", "0.1"};

void make_plot_2d()
{
	gStyle->SetOptStat(0);
	gStyle->SetPaintTextFormat("5.2f");
	gStyle->SetPalette(53);

	TString selection = "../preselected";

	TFile *_file1 = TFile::Open(selection + "_ggH_HToUps1SG_M125_NNPDF31_TuneCP5_13TeV-powheg-pythia8_2018.root");
	TFile *_file2 = TFile::Open(selection + "_ggH_HToUps2SG_M125_NNPDF31_TuneCP5_13TeV-powheg-pythia8_2018.root");
	TFile *_file3 = TFile::Open(selection + "_ggH_HToUps3SG_M125_NNPDF31_TuneCP5_13TeV-powheg-pythia8_2018.root");
	TFile *_file4 = TFile::Open(selection + "_ZToUpsilon1SGamma_TuneCP5_13TeV-amcatnloFXFX-pythia8_2018.root");
	TFile *_file5 = TFile::Open(selection + "_ZToUpsilon2SGamma_TuneCP5_13TeV-amcatnloFXFX-pythia8_2018.root");
	TFile *_file6 = TFile::Open(selection + "_ZToUpsilon3SGamma_TuneCP5_13TeV-amcatnloFXFX-pythia8_2018.root");
	TFile *_file0 = TFile::Open(selection + "_Run2018.root");
	TTree *treeZ3 = (TTree *)_file6->Get("Events");
	TTree *treeZ2 = (TTree *)_file5->Get("Events");
	TTree *treeZ1 = (TTree *)_file4->Get("Events");
	TTree *treeH3 = (TTree *)_file3->Get("Events");
	TTree *treeH2 = (TTree *)_file2->Get("Events");
	TTree *treeH1 = (TTree *)_file1->Get("Events");
	TTree *treedata = (TTree *)_file0->Get("Events");

	//        TH2F *h2_H = new TH2F("h2_H",";delta_eta;delta_phi",11,1.15,2.25,11,1.95,3.05);
	//        TH2F *h2_Z = new TH2F("h2_Z",";delta_eta;delta_phi",11,1.15,2.25,11,1.95,3.05);
	TH2F *h2_H = new TH2F("h2_H", ";delta_eta;delta_phi", 30, 0.15, 6.05, 30, 0.05, 3.05);
	TH2F *h2_Z = new TH2F("h2_Z", ";delta_eta;delta_phi", 30, 0.15, 6.05, 30, 0.05, 3.05);
	for (int ii = 1; ii <= 30; ii++)
		h2_H->GetXaxis()->SetBinLabel(ii, x_label[ii - 1]);
	for (int ii = 1; ii <= 30; ii++)
		h2_H->GetYaxis()->SetBinLabel(ii, y_label[ii - 1]);
	for (int ii = 1; ii <= 30; ii++)
		h2_Z->GetXaxis()->SetBinLabel(ii, x_label[ii - 1]);
	for (int ii = 1; ii <= 30; ii++)
		h2_Z->GetYaxis()->SetBinLabel(ii, y_label[ii - 1]);
	for (int ii = 1; ii <= 30; ii++)
	{
		for (int j = 1; j <= 30; j++)
		{
			std::cout << "(i,j): (" << ii << "," << j << ")" << std::endl;

			TH1F *h1_H1 = new TH1F("h1_H1", "weigth", 2, 0, 2);
			Double_t var_w_H1;
			treeH1->SetBranchAddress("weight", &var_w_H1);
			Float_t var_delta_eta_upsilon_photon_H1;
			treeH1->SetBranchAddress("delta_eta_upsilon_photon", &var_delta_eta_upsilon_photon_H1);
			Float_t var_delta_phi_upsilon_photon_H1;
			treeH1->SetBranchAddress("delta_phi_upsilon_photon", &var_delta_phi_upsilon_photon_H1);
			for (int i = 0; i < treeH1->GetEntries(); i++)
			{
				treeH1->GetEntry(i);
				if (var_delta_eta_upsilon_photon_H1 < x_cut[ii] and var_delta_phi_upsilon_photon_H1 > y_cut[ii])
					h1_H1->Fill(1, var_w_H1);
			}
			TH1F *h1_H2 = new TH1F("h1_H2", "weigth", 2, 0, 2);
			Double_t var_w_H2;
			treeH2->SetBranchAddress("weight", &var_w_H2);
			Float_t var_delta_eta_upsilon_photon_H2;
			treeH2->SetBranchAddress("delta_eta_upsilon_photon", &var_delta_eta_upsilon_photon_H2);
			Float_t var_delta_phi_upsilon_photon_H2;
			treeH2->SetBranchAddress("delta_phi_upsilon_photon", &var_delta_phi_upsilon_photon_H2);
			for (int i = 0; i < treeH2->GetEntries(); i++)
			{
				treeH2->GetEntry(i);
				if (var_delta_eta_upsilon_photon_H2 < x_cut[ii] and var_delta_phi_upsilon_photon_H2 > y_cut[ii])
					h1_H2->Fill(1, var_w_H2);
			}
			TH1F *h1_H3 = new TH1F("h1_H3", "weigth", 2, 0, 2);
			Double_t var_w_H3;
			treeH3->SetBranchAddress("weight", &var_w_H3);
			Float_t var_delta_eta_upsilon_photon_H3;
			treeH3->SetBranchAddress("delta_eta_upsilon_photon", &var_delta_eta_upsilon_photon_H3);
			Float_t var_delta_phi_upsilon_photon_H3;
			treeH3->SetBranchAddress("delta_phi_upsilon_photon", &var_delta_phi_upsilon_photon_H3);
			for (int i = 0; i < treeH3->GetEntries(); i++)
			{
				treeH3->GetEntry(i);
				if (var_delta_eta_upsilon_photon_H3 < x_cut[ii] and var_delta_phi_upsilon_photon_H3 > y_cut[ii])
					h1_H3->Fill(1, var_w_H3);
			}
			h1_H1->Add(h1_H2);
			h1_H1->Add(h1_H3);

			TH1F *h1_Z1 = new TH1F("h1_Z1", "weigth", 2, 0, 2);
			Double_t var_w_Z1;
			treeZ1->SetBranchAddress("weight", &var_w_Z1);
			Float_t var_delta_eta_upsilon_photon_Z1;
			treeZ1->SetBranchAddress("delta_eta_upsilon_photon", &var_delta_eta_upsilon_photon_Z1);
			Float_t var_delta_phi_upsilon_photon_Z1;
			treeZ1->SetBranchAddress("delta_phi_upsilon_photon", &var_delta_phi_upsilon_photon_Z1);
			for (int i = 0; i < treeZ1->GetEntries(); i++)
			{
				treeZ1->GetEntry(i);
				if (var_delta_eta_upsilon_photon_Z1 < x_cut[ii] and var_delta_phi_upsilon_photon_Z1 > y_cut[ii])
					h1_Z1->Fill(1, var_w_Z1);
			}
			TH1F *h1_Z2 = new TH1F("h1_Z2", "weigth", 2, 0, 2);
			Double_t var_w_Z2;
			treeZ2->SetBranchAddress("weight", &var_w_Z2);
			Float_t var_delta_eta_upsilon_photon_Z2;
			treeZ2->SetBranchAddress("delta_eta_upsilon_photon", &var_delta_eta_upsilon_photon_Z2);
			Float_t var_delta_phi_upsilon_photon_Z2;
			treeZ2->SetBranchAddress("delta_phi_upsilon_photon", &var_delta_phi_upsilon_photon_Z2);
			for (int i = 0; i < treeZ2->GetEntries(); i++)
			{
				treeZ2->GetEntry(i);
				if (var_delta_eta_upsilon_photon_Z2 < x_cut[ii] and var_delta_phi_upsilon_photon_Z2 > y_cut[ii])
					h1_Z2->Fill(1, var_w_Z2);
			}
			TH1F *h1_Z3 = new TH1F("h1_Z3", "weigth", 2, 0, 2);
			Double_t var_w_Z3;
			treeZ3->SetBranchAddress("weight", &var_w_Z3);
			Float_t var_delta_eta_upsilon_photon_Z3;
			treeZ3->SetBranchAddress("delta_eta_upsilon_photon", &var_delta_eta_upsilon_photon_Z3);
			Float_t var_delta_phi_upsilon_photon_Z3;
			treeZ3->SetBranchAddress("delta_phi_upsilon_photon", &var_delta_phi_upsilon_photon_Z3);
			for (int i = 0; i < treeZ3->GetEntries(); i++)
			{
				treeZ3->GetEntry(i);
				if (var_delta_eta_upsilon_photon_Z3 < x_cut[ii] and var_delta_phi_upsilon_photon_Z3 > y_cut[ii])
					h1_Z3->Fill(1, var_w_Z3);
			}
			h1_Z1->Add(h1_Z2);
			h1_Z1->Add(h1_Z3);

			TH1F *h1_data = new TH1F("h1_data", "weigth", 2, 0, 2);
			Double_t var_w_data;
			treedata->SetBranchAddress("weight", &var_w_data);
			Float_t var_delta_eta_upsilon_photon_data;
			treedata->SetBranchAddress("delta_eta_upsilon_photon", &var_delta_eta_upsilon_photon_data);
			Float_t var_delta_phi_upsilon_photon_data;
			treedata->SetBranchAddress("delta_phi_upsilon_photon", &var_delta_phi_upsilon_photon_data);
			for (int i = 0; i < treedata->GetEntries(); i++)
			{
				treedata->GetEntry(i);
				if (var_delta_eta_upsilon_photon_data < x_cut[ii] and var_delta_phi_upsilon_photon_data > y_cut[ii])
					h1_data->Fill(1, var_w_data);
			}

			h2_H->SetBinContent(ii, j, h1_H1->Integral() * 1000000000 / h1_data->Integral());
			h2_Z->SetBinContent(ii, j, h1_Z1->Integral() * 100000 / h1_data->Integral());
			std::cout << "h1_H1->Integral()*1000000000/h1_data->Integral(): " << h1_H1->Integral() * 1000000000 / h1_data->Integral() << std::endl;
			std::cout << "h1_Z1->Integral()*100000/h1_data->Integral(): " << h1_Z1->Integral() * 100000 / h1_data->Integral() << std::endl;

			delete h1_H1;
			delete h1_H2;
			delete h1_H3;
			delete h1_Z1;
			delete h1_Z2;
			delete h1_Z3;
			delete h1_data;
		}
	}

	Int_t MaxBinH = h2_H->GetMaximumBin();
	Int_t xH, yH, zH;
	h2_H->GetBinXYZ(MaxBinH, xH, yH, zH);
	std::cout << "xH: " << x_cut[xH - 1] << "; yH: " << y_cut[yH - 1] << std::endl;

	Int_t MaxBinZ = h2_Z->GetMaximumBin();
	Int_t xZ, yZ, zZ;
	h2_Z->GetBinXYZ(MaxBinZ, xZ, yZ, zZ);
	std::cout << "xZ: " << x_cut[xZ - 1] << "; yZ: " << y_cut[yZ - 1] << std::endl;

	h2_H->SetMarkerSize(0.5);
	h2_Z->SetMarkerSize(0.5);

	TCanvas *cH = new TCanvas("cH", "", 0, 0, 4500, 9000);
	h2_H->Draw("COLZ text");
	cH->SaveAs("H_upsilon_boson_window_large.png");
	cH->SaveAs("H_upsilon_boson_window_large.pdf");

	TCanvas *cZ = new TCanvas("cZ", "", 0, 0, 4500, 9000);
	h2_Z->Draw("COLZ text");
	cZ->SaveAs("Z_upsilon_boson_window_large.png");
	cZ->SaveAs("Z_upsilon_boson_window_large.pdf");
}
