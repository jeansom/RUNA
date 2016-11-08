#!/usr/bin/env python
from collections import OrderedDict

bkgVariables = OrderedDict()

###### [ variable name, cut value, below, minValue, maxValue, binWidth ]


#bkgVariables[ 'RPVStopStopToJets_UDD323_M-100' ] = [
 #   [ 'prunedMassAsym', [ 'prunedMassAsym'], 0.10, True, 0., 1., 20 ], [ 'deltaEtaDijet', ['deltaEtaDijet'], 1.0, True, 0., 5., 50 ] 
  #  ]

bkgVariables[ 'RPVStopStopToJets_UDD323_M-100' ] = [
    [ 'btagJet1', 0.800, False, 0., 1., 20, 1, [ 'subjet11btagCSVv2', 'subjet12btagCSVv2' ] ],  [ 'btagJet2', 0.800, False, 0., 1., 20, 1, [ 'subjet21btagCSVv2', 'subjet22btagCSVv2' ] ]
    ]
