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
		'TTJets' : 670.3, #  831.0 this is from twiki, 670.3 is from MCM
		'WJetsToQQ' : 95.14,
		'WWTo4Q' : 45.20,
		'ZJetsToQQ' : 5.67,
		#### RPV
		'RPVSt100' : 1521.11,
		'RPVSt200' : 64.5085,
		'RPVSt350' : 3.78661
		}

dictEvents = {
		#### DATA
		'JetHT' :	[ 1., ],


		#### QCD in Pt (TuneCUETP8M1)
		#	        (Asympt50ns)   (Asympt25ns)	
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

		'TTJets' :	[ 4994250., 	42730273. 	 ],
		'WJetsToQQ' : 	[ 0., 		1006060. 	 ],
		'WWTo4Q' : 	[ 0., 		1995200. 	 ],
		'ZJetsToQQ' : 	[ 0., 		982095. 	 ],

		#### RPV Stop
		'RPVSt100' :  	[ 200000., 	200000. 	],	
		'RPVSt200' :  	[ 200000., 	200000. 	],	
		'RPVSt350' :  	[ 200000., 	200000. 	],	
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
		#events = search( dictEvents, NAME )[0]
		if '50ns' in NAME: events = search( dictEvents, NAME )[0]
		elif '25ns' in NAME: events = search( dictEvents, NAME )[1]
		else: events = 1.

		SF = XS / events
		print 'For sample '+NAME+': XS = '+str(XS)+', nEvents = '+str(events)+' and SF = '+str(SF)
		return SF

	except:
		print 'Scale factor not found.'
