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
		'170to300' : 120300.,
		'300to470' : 7475. , 
		'470to600' : 587.1 ,
		'600to800' : 167. ,
		'800to1000' : 28.25 ,
		'1000to1400' : 8.195 ,
		'1400to1800' : 0.7346 ,
		'1800to2400' : 0.114943,
		# QCD HT
		'500to700' : 29370. ,
		'700to1000' : 6524. , 
		'1000to1500' : 1064.,
		#### TTJets
		'TTJets' : 831.0,
		'WJetsToQQ' : 95.14,
		'ZJetsToQQ' : 5.67,
		#### RPV
		'RPVSt100' : 1521.11,
		'RPVSt200' : 64.5085,
		'RPVSt350' : 3.78661
		}

dictEvents = {
		#### DATA
		'JetHT' :	[ 1., ],


		#### QCD in Pt [ (TuneCUETP8M1)	Generated (Tune4C),	PU40bx50 (CSA14),	PU30BX50 (PHYS14), 	PU20BX25 (PHYS25) ]
		'170to300' :   [ 3714174., 	2794554., 	1490834. ,		2794244. ,		2000704. ],
		'300to470' :   [ 3232893.,	2705941., 	576268. ,		2676717. ,		1986177. ], 
		'470to600' :   [ 2136826.,	2926313., 	1500297. , 		2925561. , 		2001071. ],
		'600to800' :   [ 2164008.,	2857014., 	1465278. , 		2857014. , 		1997744. ],
		'800to1000' :  [ 2137088.,	2916394., 	1500369. , 		499998. , 		1000065. ],
		'1000to1400' : [ 1637088.,	2884228., 	1500642. , 		499986. , 		500550. ],
		'1400to1800' : [ 217898.,	2931706., 	499994. , 		499994. , 		199627. ],
		'1800to2400' : [ 212094.,	],
		#### QCD in HT
		'500to700' :  [ 19722604., 	],
		'700to1000' :  [ 15416052., 	],
		'1000to1500' :  [ 4909636., 	],

		'TTJets' : [ 41137533., ],
		'WJetsToQQ' : [ 1006060., ],
		'ZJetsToQQ' : [ 982095., ],

		#### RPV Stop
		'RPVSt100' :  [ 200000.],	
		'RPVSt200' :  [ 200000.],	
		'RPVSt350' :  [ 200000.],	
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
		events = search( dictEvents, NAME )[0]
		'''
		if 'PU40bx50' in NAME: events = search( dictEvents, NAME )[1]
		elif 'PU30BX50' in NAME: events = search( dictEvents, NAME )[2]
		elif 'PU20bx25' in NAME: events = search( dictEvents, NAME )[3]
		else: events = 1.
		'''

		SF = XS / events
		print 'For sample '+NAME+': XS = '+str(XS)+', nEvents = '+str(events)+' and SF = '+str(SF)
		return SF

	except:
		print 'Scale factor not found.'
