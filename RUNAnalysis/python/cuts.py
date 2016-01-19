#!/usr/bin/env python
from collections import OrderedDict

selection = OrderedDict()
selection[ 'Dibosons' ] = [ 
		[ 'massAsym', 0.65 ], [ 'jet1Tau21', 0.55 ], [ 'jet2Tau21', 0.55 ], [ 'jet1Tau31', 0.35 ], [ 'jet2Tau31', 0.35 ] 
		]

selection[ 'RPVSt100' ] = [ 
		[ 'massAsym', 0.30 ], [ 'deltaEtaDijet', 0.7 ] , [ 'jet1Tau21', 0.5 ], [ 'jet2Tau21', 0.5 ], [ 'jet1Tau31', 0.3 ] #, [ 'jet2Tau31', 0.35 ] ]
		]

selection[ 'RPVSt200' ] = [ 
		[ 'massAsym', 0.10 ], [ 'deltaEtaDijet', 0.9 ], [ 'jet1Tau21', 0.4 ], [ 'jet2Tau21', 0.4 ] 
		]
		
