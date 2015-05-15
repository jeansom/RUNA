dictXS = { 
		#### QCD in Pt
		'170to300' : 120300. ,
		'300to470' : 7475. , 
		'470to600' : 587.1 ,
		'600to800' : 167. ,
		'800to1000' : 28.25 ,
		'1000to1400' : 8.195 ,
		'1400to1800' : 0.7346 ,
		#### QCD in HT
		'HT250to500' : 670500. ,
		'500To1000' : 26740. ,
		'1000ToInf' : 769.7 ,			
		#### RPV
		'RPVSt100' : 1521.11 ,
		'RPVSt350' : 3.78661
		}

dictEvents = {
		#### QCD in Pt [ Generated,	PU40bx50 (CSA14),	PU30BX50 (PHYS14), 	PU20BX25 (PHYS25) ]
		'170to300' :   [ 2794554., 	1490834. ,		2794244. ,		2000704. ],
		'300to470' :   [ 2705941., 	576268. ,		2676717. ,		1986177. ], 
		'470to600' :   [ 2926313., 	1500297. , 		2925561. , 		2001071. ],
		'600to800' :   [ 2857014., 	1465278. , 		2857014. , 		1997744. ],
		'800to1000' :  [ 2916394., 	1500369. , 		499998. , 		1000065. ],
		'1000to1400' : [ 2884228., 	1500642. , 		499986. , 		500550. ],
		'1400to1800' : [ 2931706., 	499994. , 		499994. , 		199627. ],
		#### QCD in HT
		'500To1000' :  [ 19500000., 	1. , 			1. , 			4063345. ],
		'1000ToInf' :  [ 1500000., 	1. , 			1. , 			1130720. ],
		#### RPV Stop
		'RPVSt100tojj' :  [ 100000., 	98208. ,		1. ,			98300. ],	
		'RPVSt100tobj' :  [ 100000., 	49500. ,		1. ,			91100. ],	
		'RPVSt350tojj' :  [ 100000., 	1. ,		1. ,			1. ],	
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
