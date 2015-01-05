#!/usr/bin/env python
from ROOT import *
import ROOT as rt

def setSelection( signal, sel1='', sel2='', sel3='', sel4='', sel5='', sel6='' ):

	textBox=TLatex()
	textBox.SetNDC()
	textBox.SetTextSize(0.05) 
	textBox.SetTextColor(kBlue)
	if 'Data' in signal:
		textBox.DrawText(0.16,0.95,"CMS Preliminary ")
	else:
	 	textBox.DrawText(0.16,0.95,"CMS Preliminary Simulation")

	textBox1=TLatex()
	textBox1.SetNDC()
	textBox1.SetTextSize(0.04) 
	textBox1.DrawText(0.70,0.65, signal)
	
	textBox3=TLatex()
	textBox3.SetNDC()
	textBox3.SetTextSize(0.04) 
	textBox3.DrawLatex(0.70,0.60, sel1)
		
	textBox4=TLatex()
	textBox4.SetNDC()
	textBox4.SetTextSize(0.04) 
	textBox4.DrawLatex(0.70,0.55, sel2)
	
	textBox5=TLatex()
	textBox5.SetNDC()
	textBox5.SetTextSize(0.04) 
	textBox5.DrawLatex(0.70,0.50, sel3 )
	
	textBox6=TLatex()
	textBox6.SetNDC()
	textBox6.SetTextSize(0.04) 
	textBox6.DrawLatex(0.70,0.45, sel4)
	
	textBox7=TLatex()
	textBox7.SetNDC()
	textBox7.SetTextSize(0.04) 
	textBox7.DrawLatex(0.70,0.40, sel5 )
	
	textBox8=TLatex()
	textBox8.SetNDC()
	textBox8.SetTextSize(0.04) 
	textBox8.DrawLatex(0.70,0.35, sel6 )
	
def setSelectionTrigger2D( signal, trigger, sel1, sel2, sel3, sel4):

	textBox=TLatex()
	textBox.SetNDC()
	textBox.SetTextSize(0.05) 
	textBox.SetTextColor(kBlue)
	textBox.DrawText(0.13,0.95,"CMS Preliminary Simulation")
	#textBox.DrawText(0.16,0.95,"CMS Preliminary")

	textBox1=TLatex()
	textBox1.SetNDC()
	textBox1.SetTextSize(0.04) 
	textBox1.DrawText(0.15,0.90, signal)
	
	textBox5=TLatex()
	textBox5.SetNDC()
	textBox5.SetTextSize(0.04) 
	textBox5.DrawLatex(0.55,0.95, trigger )
	
	textBox3=TLatex()
	textBox3.SetNDC()
	textBox3.SetTextSize(0.04) 
	textBox3.DrawLatex(0.65,0.40, sel1 )
		
	textBox4=TLatex()
	textBox4.SetNDC()
	textBox4.SetTextSize(0.04) 
	textBox4.DrawLatex(0.65,0.35, sel2 )
	
	textBox5=TLatex()
	textBox5.SetNDC()
	textBox5.SetTextSize(0.04) 
	textBox5.DrawLatex(0.65,0.30, sel3 )

	textBox6=TLatex()
	textBox6.SetNDC()
	textBox6.SetTextSize(0.04) 
	textBox6.DrawLatex(0.65,0.25, sel4 )
	
	
	
def setSelectionTitle( signal ):

	textBox=TLatex()
	textBox.SetNDC()
	textBox.SetTextSize(0.05) 
	textBox.SetTextColor(kBlue)
	textBox.DrawText(0.16,0.95,"CMS Preliminary Simulation")

	textBox1=TLatex()
	textBox1.SetNDC()
	textBox1.SetTextSize(0.04) 
	textBox1.DrawText(0.75,0.65, signal)
	
	textBox3=TLatex()
	textBox3.SetNDC()
	textBox3.SetTextSize(0.04) 
	textBox3.DrawLatex(0.75,0.60,"jet p_{T} > 40 GeV ")
		
	textBox4=TLatex()
	textBox4.SetNDC()
	textBox4.SetTextSize(0.04) 
	textBox4.DrawLatex(0.75,0.55,"|jet #eta| < 2.5")
	
def setTitle( signal ):

	textBox=TLatex()
	textBox.SetNDC()
	textBox.SetTextSize(0.05) 
	textBox.SetTextColor(kBlue)
	textBox.DrawText(0.25,0.95,"CMS Preliminary Simulation")

	textBox1=TLatex()
	textBox1.SetNDC()
	textBox1.SetTextSize(0.04) 
	if 'Trigger' in signal:
		textBox1.DrawText(0.65,0.88, signal)
	else:
		textBox1.DrawText(0.70,0.65, signal)
	

def setTDRStyle():
	tdrStyle = TStyle("tdrStyle","Style for P-TDR")
	#tdrStyle.SetPalette(1)
	tdrStyle.SetPalette(55)
	# For the canvas:
	tdrStyle.SetCanvasBorderMode(0)
	tdrStyle.SetCanvasColor(0)
	tdrStyle.SetCanvasDefH(900) #Height of canvas
	tdrStyle.SetCanvasDefW(600) #Width of canvas
	tdrStyle.SetCanvasDefX(0)   #POsition on screen
	tdrStyle.SetCanvasDefY(0)

	# For the Pad:
	tdrStyle.SetPadBorderMode(0)
	tdrStyle.SetPadColor(0)
	#tdrStyle.SetPadGridX(false)
	#tdrStyle.SetPadGridY(false)
	tdrStyle.SetGridColor(0)
	tdrStyle.SetGridStyle(3)
	tdrStyle.SetGridWidth(1)

	# For the frame:
	tdrStyle.SetFrameBorderMode(0)
	tdrStyle.SetFrameBorderSize(1)
	tdrStyle.SetFrameFillColor(0)
	tdrStyle.SetFrameFillStyle(0)
	tdrStyle.SetFrameLineColor(1)
	tdrStyle.SetFrameLineStyle(1)
	tdrStyle.SetFrameLineWidth(1)

	# For the histo:
	#tdrStyle.SetHistFillColor(0)
	tdrStyle.SetHistFillStyle(0)
	#tdrStyle.SetHistLineColor(1)
	#tdrStyle.SetHistLineStyle(0)
	#tdrStyle.SetHistLineWidth(1)

	tdrStyle.SetEndErrorSize(2)
	#tdrStyle.SetErrorMarker(20)
	#tdrStyle.SetErrorX(0.)

	#tdrStyle.SetMarkerStyle(20)

	#For the fit/function:
	#tdrStyle.SetOptFit(0010) # display fit parameters values only
	tdrStyle.SetOptFit(0000)
	tdrStyle.SetFitFormat("5.4g")
	tdrStyle.SetFuncColor(2)
	tdrStyle.SetFuncStyle(1)
	tdrStyle.SetFuncWidth(2)

	# for the legends
	tdrStyle.SetLegendBorderSize(0)
	tdrStyle.SetLegendFillColor(0)
	tdrStyle.SetLegendFont(42)

	#For the date:
	tdrStyle.SetOptDate(0)
	# tdrStyle.SetDateX(Float_t x = 0.01)
	# tdrStyle.SetDateY(Float_t y = 0.01)

	# For the statistics box:
	tdrStyle.SetOptFile(0)
	#tdrStyle.SetOptStat(0) # To display the mean and RMS:   SetOptStat("mr")
	tdrStyle.SetStatColor(0)
	tdrStyle.SetStatFont(42)
	#tdrStyle.SetStatFontSize(0.025)
	tdrStyle.SetStatTextColor(1)
	tdrStyle.SetStatFormat("6.4g")
	tdrStyle.SetStatBorderSize(1)
	#tdrStyle.SetStatH(0.1)
	#tdrStyle.SetStatW(0.15)
	# tdrStyle.SetStatStyle(Style_t style = 1001)
	# tdrStyle.SetStatX(Float_t x = 0)
	# tdrStyle.SetStatY(Float_t y = 0)

	# Margins:
	tdrStyle.SetPadTopMargin(0.06)
	tdrStyle.SetPadBottomMargin(0.13)
	tdrStyle.SetPadLeftMargin(0.12)
	tdrStyle.SetPadRightMargin(0.10)

	# For the Global title:

	tdrStyle.SetOptTitle(0)
	tdrStyle.SetTitleFont(42)
	tdrStyle.SetTitleColor(1)
	tdrStyle.SetTitleTextColor(1)
	tdrStyle.SetTitleFillColor(10)
	tdrStyle.SetTitleFontSize(0.05)
	# tdrStyle.SetTitleH(0) # Set the height of the title box
	# tdrStyle.SetTitleW(0) # Set the width of the title box
	# tdrStyle.SetTitleX(0) # Set the position of the title box
	# tdrStyle.SetTitleY(0.985) # Set the position of the title box
	# tdrStyle.SetTitleStyle(Style_t style = 1001)
	# tdrStyle.SetTitleBorderSize(2)

	# For the axis titles:

	tdrStyle.SetTitleColor(1, "XYZ")
	tdrStyle.SetTitleFont(42, "XYZ")
	tdrStyle.SetTitleSize(0.05, "XYZ")
	# tdrStyle.SetTitleXSize(Float_t size = 0.02) # Another way to set the size?
	# tdrStyle.SetTitleYSize(Float_t size = 0.02)
	tdrStyle.SetTitleXOffset(0.9)
	tdrStyle.SetTitleYOffset(1.0)
	# tdrStyle.SetTitleOffset(1.1, "Y") # Another way to set the Offset

	# For the axis labels:

	tdrStyle.SetLabelColor(1, "XYZ")
	tdrStyle.SetLabelFont(42, "XYZ")
	tdrStyle.SetLabelOffset(0.007, "XYZ")
	tdrStyle.SetLabelSize(0.04, "XYZ")

	# For the axis:

	tdrStyle.SetAxisColor(1, "XYZ")
	tdrStyle.SetStripDecimals(True)
	tdrStyle.SetTickLength(0.03, "XYZ")
	tdrStyle.SetNdivisions(510, "XYZ")
	tdrStyle.SetPadTickX(1)  # To get tick marks on the opposite side of the frame
	tdrStyle.SetPadTickY(1)

	# Change for log plots:
	tdrStyle.SetOptLogx(0)
	tdrStyle.SetOptLogy(0)
	tdrStyle.SetOptLogz(0)

	# Postscript options:
	tdrStyle.SetPaperSize(20.,20.)
	# tdrStyle.SetLineScalePS(Float_t scale = 3)
	# tdrStyle.SetLineStyleString(Int_t i, const char* text)
	# tdrStyle.SetHeaderPS(const char* header)
	# tdrStyle.SetTitlePS(const char* pstitle)

	# tdrStyle.SetBarOffset(Float_t baroff = 0.5)
	# tdrStyle.SetBarWidth(Float_t barwidth = 0.5)
	# tdrStyle.SetPaintTextFormat(const char* format = "g")
	# tdrStyle.SetPalette(Int_t ncolors = 0, Int_t* colors = 0)
	# tdrStyle.SetTimeOffset(Double_t toffset)
	# tdrStyle.SetHistMinimumZero(kTRUE)

	tdrStyle.cd()
