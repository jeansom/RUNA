dictXS = { 
		##### DATA
		'JetHT' : 1.,
		#### QCD in Pt
		# QCD_Pt-*_Tune4C_13TeV_pythia8
		#'170to300' : 120300. ,
		#'300to470' : 7475. , 
		#'470to600' : 587.1 ,
		#'600to800' : 167. ,
		#'800to1000' : 28.25 ,
		#'1000to1400' : 8.195 ,
		#'1400to1800' : 0.7346 ,
		#### QCD in HT
		#'HT250to500' : 670500. ,
		#'500To1000' : 26740. ,
		#'1000ToInf' : 769.7 ,			

		# QCD_Pt_*_TuneCUETP8M1_13TeV_pythia8
		'120to170' : 471100.,
		'170to300' : 117276.,
		'300to470' : 7823. , 
		'470to600' : 648.2 ,
		'600to800' : 186.9 ,
		'800to1000' : 32.293 ,
		'1000to1400' : 9.4183 ,
		'1400to1800' : 0.8426 ,
		'1800to2400' : 0.1149 ,
		'2400to3200' : 0.006829 ,
		'3200toInf' : 0.00016544 ,
		# QCD HT
		'500to700' : 29370. ,
		'700to1000' : 6524. , 
		'1000to1500' : 1064.,
		'1500to2000' : 121.5 ,
		'2000toInf' : 25.42 ,
		#### TTJets
		'TTJets_TuneCUETP8M1' : 831.76,
		'TTJets_HT-600to800' : 1.61, 
		'TTJets_HT-80to1200' : 0.663, 
		'TTJets_HT-1200to2500' : 0.12, 
		'TTJets_HT-2500toInf' : 0.00143, 
		#### W
		'WJetsToQQ' : 95.14,
		'WWTo4Q' : 51.723,
		#### Z
		'ZJetsToQQ' : 5.67,
		'ZZTo4Q' : 6.842,
		'WZ' : 22.82,
		#### RPV
		'RPVStopStopToJets_UDD312_M-80' : 1,
		'RPVStopStopToJets_UDD312_M-90' : 1,
		'RPVStopStopToJets_UDD312_M-100' : 1521.11,
		'RPVStopStopToJets_UDD312_M-110' : 1013.76,
		'RPVStopStopToJets_UDD312_M-120' : 689.799,
		'RPVStopStopToJets_UDD312_M-130' : 481.397,
		'RPVStopStopToJets_UDD312_M-140' : 342.865,
		'RPVStopStopToJets_UDD312_M-150' : 249.409,
		'RPVStopStopToJets_UDD312_M-160' : 184.623,
		'RPVStopStopToJets_UDD312_M-170' : 139.252,
		'RPVStopStopToJets_UDD312_M-180' : 106.194,
		'RPVStopStopToJets_UDD312_M-190' : 82.2541,
		'RPVStopStopToJets_UDD312_M-200' : 64.5085,
		'RPVStopStopToJets_UDD312_M-210' : 50.9226,
		'RPVStopStopToJets_UDD312_M-220' : 40.5941,
		'RPVStopStopToJets_UDD312_M-230' : 32.6679,
		'RPVStopStopToJets_UDD312_M-240' : 26.4761,
		'RPVStopStopToJets_UDD312_M-250' : 21.5949,
		'RPVStopStopToJets_UDD312_M-300' : 8.51615,
		'RPVStopStopToJets_UDD312_M-350' : 3.78661,
		'RPVStopStopToJets_UDD312_M-400' : 1.83537,
		'RPVStopStopToJets_UDD312_M-450' : 0.948333,
		'RPVStopStopToJets_UDD312_M-500' : 0.51848,
		'RPVStopStopToJets_UDD312_M-550' : 0.296128,
		'RPVStopStopToJets_UDD312_M-600' : 0.174599,
		'RPVStopStopToJets_UDD312_M-650' : 0.107045,
		'RPVStopStopToJets_UDD312_M-700' : 0.0670476,
		'RPVStopStopToJets_UDD312_M-750' : 0.0431418,
		'RPVStopStopToJets_UDD312_M-800' : 0.0283338,
		'RPVStopStopToJets_UDD312_M-850' : 0.0189612,
		'RPVStopStopToJets_UDD312_M-900' : 0.0128895,
		'RPVStopStopToJets_UDD312_M-950' : 0.00883465,
		'RPVStopStopToJets_UDD312_M-1000' : 0.00615134,
		'RPVStopStopToJets_UDD312_M-1100' : 0.00307413,
		'RPVStopStopToJets_UDD312_M-1200' : 0.00159844,
		'RPVStopStopToJets_UDD312_M-1300' : 0.000850345,
		'RPVStopStopToJets_UDD312_M-1400' : 0.000461944,
		'RPVStopStopToJets_UDD312_M-1500' : 0.000256248,
		}

dictEvents = {
		#### DATA
		'JetHT' :	[ 1., ],


		#### QCD in Pt (TuneCUETP8M1)
		#	        (Asympt50ns)   (Asympt25ns)	
		'120to170' :	[ 1., 	3452896. ],
		'170to300' :	[ 3438066., 	3364368. ],
		'300to470' :	[ 2930578.,	2933611. ], 
		'470to600' :	[ 1939229.,	1936832. ],
		'600to800' :   	[ 1890256.,	1964128. ],
		'800to1000' :  	[ 1911296.,	1937216. ],
		'1000to1400' : 	[ 1461216.,	1487136. ],
		'1400to1800' : 	[ 197959.,	197959.  ],
		'1800to2400' : 	[ 194924., 	193608.	 ],
		'2400to3200' : 	[ 198383., 	194456.  ],
		'3200toInf' : 	[ 188696., 	192944. ],
		#### QCD in HT
		'500to700' :  	[ 19722604., 	19542847.	],
		'700to1000' :  	[ 15416052., 	15011016.	],
		'1000to1500' :  [ 4909636., 	4963895.	],
		'1500to2000' :  [ 0., 		3848411.	],
		'2000toInf' : 	[ 0., 		1961774.	],

		'TTJets_TuneCUETP8M1' : [ 0., 42784971 ],
		'TTJets_HT-600to800' :	[ 0., 	5119009. 	 ],
		'TTJets_HT-800to1200' :	[ 0., 	3510897. 	 ],
		'TTJets_HT-1200to2500' :	[ 0., 	1014678. 	 ],
		'TTJets_HT-2500toInf' :	[ 0., 	507842. 	 ],
		'WJetsToQQ' : 	[ 0., 		1006060. 	 ],
		'WWTo4Q' : 	[ 0., 		1995200. 	 ],
		'ZJetsToQQ' : 	[ 0., 		982095. 	 ],
		'ZZTo4Q' : 	[ 0., 		35917388. 	 ],
		'WZ' : 	[ 0., 		991232. 	 ],

		#### RPV Stop
		##### Privately produced
		#'RPVStopStopToJets_UDD312_M-100' :  	[ 0., 	166722. 	],	
		#'RPVStopStopToJets_UDD312_M-200' :  	[ 0., 	138907. 	],	
		#'RPVStopStopToJets_UDD312_M-350' :  	[ 0., 	11293. 	],	
		#'RPVStopStopToJets_UDD312_M-800' :  	[ 0., 	4784. 	],	
		##### Centrally produced
		'RPVStopStopToJets_UDD312_M-80' :	[ 0.,	22624434.],
		'RPVStopStopToJets_UDD312_M-90' :	[ 0.,	17412935.],
		'RPVStopStopToJets_UDD312_M-100' :	[ 0.,	11557789.],
		'RPVStopStopToJets_UDD312_M-110' :	[ 0.,	9562842.],
		'RPVStopStopToJets_UDD312_M-120' :	[ 0.,	6896552.],
		'RPVStopStopToJets_UDD312_M-130' :	[ 0.,	4971098.],
		'RPVStopStopToJets_UDD312_M-140' :	[ 0.,	4267516.],
		'RPVStopStopToJets_UDD312_M-150' :	[ 0.,	2530864.],
		'RPVStopStopToJets_UDD312_M-160' :	[ 0.,	2171053.],
		'RPVStopStopToJets_UDD312_M-170' :	[ 0.,	1845638.],
		'RPVStopStopToJets_UDD312_M-180' :	[ 0.,	1094891.],
		'RPVStopStopToJets_UDD312_M-190' :	[ 0.,	1514085.],
		'RPVStopStopToJets_UDD312_M-200' :	[ 0.,	1454545.],
		'RPVStopStopToJets_UDD312_M-210' :	[ 0.,	1212121.],
		'RPVStopStopToJets_UDD312_M-220' :	[ 0.,	1102941.],
		'RPVStopStopToJets_UDD312_M-230' :	[ 0.,	1015038.],
		'RPVStopStopToJets_UDD312_M-240' :	[ 0.,	937500.],
		'RPVStopStopToJets_UDD312_M-250' :	[ 0.,	859375.],
		'RPVStopStopToJets_UDD312_M-300' :	[ 0.,	763359.],
		'RPVStopStopToJets_UDD312_M-350' :	[ 0.,	813008.],
		'RPVStopStopToJets_UDD312_M-400' :	[ 0.,	813008.],
		'RPVStopStopToJets_UDD312_M-450' :	[ 0.,	1098901.],
		'RPVStopStopToJets_UDD312_M-500' :	[ 0.,	458716.],
		'RPVStopStopToJets_UDD312_M-550' :	[ 0.,	476190.],
		'RPVStopStopToJets_UDD312_M-600' :	[ 0.,	495050.],
		'RPVStopStopToJets_UDD312_M-650' :	[ 0.,	471698.],
		'RPVStopStopToJets_UDD312_M-700' :	[ 0.,	101010.],
		'RPVStopStopToJets_UDD312_M-750' :	[ 0.,	113636.],
		'RPVStopStopToJets_UDD312_M-800' :	[ 0.,	101010.],
		'RPVStopStopToJets_UDD312_M-850' :	[ 0.,	108696.],
		'RPVStopStopToJets_UDD312_M-900' :	[ 0.,	111111.],
		'RPVStopStopToJets_UDD312_M-950' :	[ 0.,	105263.],
		'RPVStopStopToJets_UDD312_M-1000' :	[ 0.,	113636.],
		'RPVStopStopToJets_UDD312_M-1100' :	[ 0.,	87719.],
		'RPVStopStopToJets_UDD312_M-1200' :	[ 0.,	95238.],
		'RPVStopStopToJets_UDD312_M-1300' :	[ 0.,	103093.],
		'RPVStopStopToJets_UDD312_M-1400' :	[ 0.,	97087.],
		'RPVStopStopToJets_UDD312_M-1500' :	[ 0.,	84034.],
		}

def search(DICT, searchFor):
	for k in DICT:
		if k in searchFor:
			return DICT[k]
	return None

def scaleFactor( NAME ):
	"""Calculate scale factor for QCD and RPV Stop"""

	try:
		XS = search( dictXS, NAME )
		events = search( dictEvents, NAME )[1]
		#if '50ns' in NAME: events = search( dictEvents, NAME )[0]
		#elif '25ns' in NAME: events = search( dictEvents, NAME )[1]
		#else: events = 1.

		SF = XS / events
		print 'For sample '+NAME+': XS = '+str(XS)+', nEvents = '+str(events)+' and SF = '+str(SF)
		return SF

	except:
		print 'Scale factor not found.'
