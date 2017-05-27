#scaleArray =  {'TopScale': [(-0.14905187405512166, 0.9930755975266417)], 'WJScale': [(2.634664756153592, 0.6630173179748597)], '__nll': [-21130.76480552672], 'TTAlphaScale': [(0.597049356035253, 0.971193112711008)], 'TTScale': [(2.2105268091198322, 0.5431018731879389)]}
#scaleArray = {'TopScale': [(-0.15633633132677538, 0.9881814857433922)], 'WJScale': [(2.6147605727579535, 0.6647215553050838)], '__nll': [-21131.80957102475], 'TTAlphaScale': [(0.5081724977842228, 0.989212816902568)], 'TTScale': [(1.9859607916708146, 0.525368999823943)]}
scaleArray = {'TopScale': [(-0.09064291065255148, 0.9888946907171432)], 'WJScale': [(-0.7185517829174408, 0.4573153144692581)], '__nll': [-24096.682957255027], 'TTScale': [(-0.29163685871914424, 0.29538230054656545)]}
#scaleArray = {'TopScale': [(-0.14905187405512166, 0.9930755975266417)], 'WJScale': [(2.634664756153592, 0.6630173179748597)], '__nll': [-21130.76480552672], 'TTAlphaScale': [(0.597049356035253, 0.971193112711008)], 'TTScale': [(2.2105268091198322, 0.5431018731879389)]}

def printScale(scaleArray):
    scaleTT = 1.*(1.0+0.5*scaleArray['TTScale'][0][0])
    scaleTTErr = 1.*(0.5*scaleArray['TTScale'][0][1])
    scaleW = 1.0+.5*scaleArray['WJScale'][0][0]
    scaleWErr = 0.5*scaleArray['WJScale'][0][1]
#scaleAlpha = 1.0-0.5*scaleArray[ 'TTAlphaScale' ][0][0]
#scaleAlphaErr = 0.5*scaleArray[ 'TTAlphaScale' ][0][1]
    scaleTop = 1.0+0.5*scaleArray[ 'TopScale' ][0][0]
    scaleTopErr = 0.5*scaleArray[ 'TopScale' ][0][1]
    
    print "TT Normalization: " + str( round( scaleTT, 2 ) ) + " +- " + str( round(scaleTTErr, 2) )
#print "TT Alpha: " + str( round( scaleAlpha, 2 ) ) + " #pm " + str( round(scaleAlphaErr, 2) )
#    print "Single Top Norm.: " + str( round( scaleTop, 2 ) ) + " #pm " + str( round(scaleTop, 2) )
#    print "W+Jets Norm.: " + str( round( scaleW, 2 ) ) + " #pm " + str( round(scaleW, 2) )

scaleArray = {'TopScale': [(0,0)], 'WJScale': [(0,0)], 'TTAlphaScale': [(0,0)], 'TTScale': [(0.5706078540713371, 0.734205203396586)], '__nll': [-30024.697817138327]} #CBD HT
print "C*(B/D) HT Binned QCD"
printScale(scaleArray)
scaleArray = {'TopScale': [(0,0)], 'WJScale': [(0,0)], 'TTAlphaScale': [(0,0)],'TTScale': [(1.8275083028923884, 0.710145730189816)], '__nll': [-30001.181670480753]} #BCD HT
print "B*(C/D) HT Binned QCD"
printScale(scaleArray)
scaleArray = {'TopScale': [(0,0)], 'WJScale': [(0,0)], 'TTAlphaScale': [(0,0)], 'TTScale': [(2.6746074966255016, 0.644286134931515)], '__nll': [-26436.74040023357]} #BCD PT
print "B*(C/D) pT Binned QCD"
printScale(scaleArray)
scaleArray = {'TopScale': [(0,0)], 'WJScale': [(0,0)], 'TTAlphaScale': [(0,0)], 'TTScale': [(3.1534765848215294, 0.6836354949279393)], '__nll': [-16366.299262966217]}
print "C*(B/D) pT Binned QCD"
printScale(scaleArray)

