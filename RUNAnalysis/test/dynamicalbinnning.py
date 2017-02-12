binWidth = 1
NBins = int(((350-50))/binWidth)
binMass = []
var_arrayMass = [ "prunedMassAve", Xcut[0], NBins, 50., 350., Xcut[2], Xcut[3], Xcut[4] ] # For making B,D plot
for i in xrange( 0, NBins ):
    binsMass.append( [ var_arrayMass[3]+binWidth*i, var_arrayMass[3]+binWidth*(i+1) ] )

temp=100
dtemp=1

MakeFitPlots( EstMass, FMass, binsMass, "prunedMassAve", Xcut[0], var_arrayMass, presel+"&"+chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "", "outputs/Mass"+chan, False )

Ei=Est.Fit.fit.GetChisquare()/Est.Fit.fit.GetNDF()
dBinWidth=1
for i in xrange(1,temp/dtemp):
    binWidthtemp = binWidth+dBinWidth
    NBins = int(((350-50))/binWidthtemp)
    binMass = []
    var_arrayMass = [ "prunedMassAve", Xcut[0], NBins, 50., 350., Xcut[2], Xcut[3], Xcut[4] ] # For making B,D plot
    for i in xrange( 0, NBins ):
        binsMass.append( [ var_arrayMass[3]+binWidthtemp*i, var_arrayMass[3]+binWidthtemp*(i+1) ] )

    MakeFitPlots( EstMass, FMass, binsMass, "prunedMassAve", Xcut[0], var_arrayMass, presel+"&"+chanCutsTemp, Ycut[0]+">"+Ycut[1], cutsB, cutsD, cut, 0, "", "", "outputs/Mass"+chan, False )

    Ef=Est.Fit.fit.GetChisquare()/Est.Fit.fit.GetNDF()

    if Ei > Ef:
        binWidth = binWidthtemp
        Ei=Ef

    else:

        if random.random() < exp( (Ef-Ei)/temp ): 
            binWidth = binWidthtemp
            Ei=Ef
    binWidth=binWidth*-1
    temp=temp-dtemp
    print Ei
