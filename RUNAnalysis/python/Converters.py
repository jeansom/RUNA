#
import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy
from math import exp, expm1, sqrt
############################################################################################
### This class provides different types of functions which can be used to fit pass/fail. ###
### It also provides the errors up and down for those functions,                         ###
### and can create a string to weight a plot made with TCuts/TChains.                    ###
############################################################################################

#### CONSTANT ####
class ConstantFit:

    # Sets basic variables
    #### init_var: initial parameters, should be of form [x]
    #### range_min: Minimum value of range to fit to
    #### range_max: Maximum value of range to fit to
    #### name: Name for fit function
    #### Opt: Options for fit; 
    ####      FOR range_min, range_max TO BE APPLIED, Opt MUST INCLUDE "R"!!!
    def __init__(self, init_var, range_min, range_max, name, Opt):
        self.Opt = Opt
        self.rm = range_min
        self.rp = range_max
        self.name = name
        self.fit = TF1("ConstantFit_"+self.name, "[0]",self.rm,self.rp)
        self.fit.SetParameter(0, init_var[0]) 

    # Makes the fit function with error up and error down
    def Converter(self, fitter):
        self.ErrUp = TF1("LinearFitErrorUp"+self.name, "[0] + [1]",self.rm,self.rp)
        self.ErrUp.SetParameter(0, self.fit.GetParameter(0))
        self.ErrUp.SetParameter(1, self.fit.GetParErrors()[0])
        self.ErrDn = TF1("LinearFitErrorDn"+self.name, "[0] - [1]",self.rm,self.rp)
        self.ErrDn.SetParameter(0, self.fit.GetParameter(0))
        self.ErrDn.SetParameter(1, self.fit.GetParErrors()[0])

    # Makes a string which can be used with TCuts/TChains to weight a plot
    #### var: Variable fit is binned in
    #### center: The x-var is recentered about the middle of the blinded region. This tells where to recenter to. Can be left as 0.
    def MakeConvFactor(self, var, center):
        X = var + "-" + str(center)
        self.ConvFact = "({0:2.9f})".format(self.ErrUp.GetParameter(0),self.ErrUp.GetParameter(1),X)
        self.ConvFactUp = "({0:2.9f} + {1:2.9f})".format(self.ErrUp.GetParameter(0),self.ErrUp.GetParameter(1))
        self.ConvFactDn = "({0:2.9f} - {1:2.9f})".format(self.ErrUp.GetParameter(0),self.ErrUp.GetParameter(1),X)


#### LINEAR ####
class LinearFit:

    # Sets basic variables
    #### init_var: initial parameters, should be of form [x,y]
    #### range_min: Minimum value of range to fit to
    #### range_max: Maximum value of range to fit to
    #### name: Name for fit function
    #### Opt: Options for fit; 
    ####      FOR range_min, range_max TO BE APPLIED, Opt MUST INCLUDE "R"!!!
    def __init__(self, init_var, range_min, range_max, name, Opt):
        self.Opt = Opt
        self.rm = range_min
        self.rp = range_max
        self.name = name
        self.fit = TF1("LinearFit_"+self.name, "[0]+ [1]*x",self.rm,self.rp)
        self.fit.SetParameter(0, init_var[0]) 
        self.fit.SetParameter(1, init_var[1])

    # Makes the fit function with error up and error down
    def Converter(self, fitter):
        self.ErrUp = TF1("LinearFitErrorUp"+self.name, "[0]+ [1]*x + sqrt((x*x*[3]*[3])+(x*2*[4])+([2]*[2]))",self.rm,self.rp)
        self.ErrUp.SetParameter(0, self.fit.GetParameter(0))
        self.ErrUp.SetParameter(1, self.fit.GetParameter(1))
        self.ErrUp.SetParameter(2, self.fit.GetParErrors()[0])
        self.ErrUp.SetParameter(3, self.fit.GetParErrors()[1])
        self.ErrUp.SetParameter(4, fitter.GetCovarianceMatrixElement(0,1))
        self.ErrDn = TF1("LinearFitErrorDn"+self.name, "[0]+ [1]*x - sqrt((x*x*[3]*[3])+(x*2*[4])+([2]*[2]))",self.rm,self.rp)
        self.ErrDn.SetParameter(0, self.fit.GetParameter(0))
        self.ErrDn.SetParameter(1, self.fit.GetParameter(1))
        self.ErrDn.SetParameter(2, self.fit.GetParErrors()[0])
        self.ErrDn.SetParameter(3, self.fit.GetParErrors()[1])
        self.ErrDn.SetParameter(4, fitter.GetCovarianceMatrixElement(0,1))

    # Makes a string which can be used with TCuts/TChains to weight a plot
    #### var: Variable fit is binned in
    #### center: The x-var is recentered about the middle of the blinded region. This tells where to recenter to. Can be left as 0.
    def MakeConvFactor(self, var, center):
        X = var + "-" + str(center)
        self.ConvFact = "({0:2.9f} + (({2})*{1:2.9f}))".format(self.ErrUp.GetParameter(0),self.ErrUp.GetParameter(1),X)
        self.ConvFactUp = "({0:2.9f} + (({5})*{1:2.9f}) + (({5})*({5})*{3:2.9f}*{3:2.9f}+(({5})*2*{4:2.9f})+({2:2.9f}*{2:2.9f}))^0.5)".format(self.ErrUp.GetParameter(0),self.ErrUp.GetParameter(1),self.ErrUp.GetParameter(2),self.ErrUp.GetParameter(3),self.ErrUp.GetParameter(4),X)
        self.ConvFactDn = "({0:2.9f} + (({5})*{1:2.9f}) - (({5})*({5})*{3:2.9f}*{3:2.9f}+(({5})*2*{4:2.9f})+({2:2.9f}*{2:2.9f}))^0.5)".format(self.ErrUp.GetParameter(0),self.ErrUp.GetParameter(1),self.ErrUp.GetParameter(2),self.ErrUp.GetParameter(3),self.ErrUp.GetParameter(4),X)

#### QUADRATIC ####
class QuadraticFit:

    # Sets basic variables
    #### init_var: initial parameters, should be of form [x,y,z]
    #### range_min: Minimum value of range to fit to
    #### range_max: Maximum value of range to fit to
    #### name: Name for fit function
    #### Opt: Options for fit; 
    ####      FOR range_min, range_max TO BE APPLIED, Opt MUST INCLUDE "R"!!!
    def __init__(self, init_var, range_min, range_max, name, Opt):
        self.Opt = Opt
        self.rm = range_min
        self.rp = range_max
        self.name = name
        self.fit = TF1("QuadraticFit", "[0]+ [1]*x + [2]*x*x",self.rm,self.rp)
        self.fit.SetParameter(0, init_var[0]) 
        self.fit.SetParameter(1, init_var[0])
        self.fit.SetParameter(2, init_var[0])

    # Makes the fit function with error up and error down
    def Converter(self, fitter):
        self.ErrUp = TF1("QuadrarticFitErrorUp"+self.name, "[0]+ [1]*x + [2]*x*x + sqrt(([3]*[3]) + (2*x*[6]) + (x*x*[4]*[4]) + (2*x*x*[7]) + (2*x*x*x*[8]) + (x*x*x*x*[5]*[5]))",self.rm,self.rp)
        self.ErrUp.SetParameter(0, self.fit.GetParameter(0))
        self.ErrUp.SetParameter(1, self.fit.GetParameter(1))
        self.ErrUp.SetParameter(2, self.fit.GetParameter(2))
        self.ErrUp.SetParameter(3, self.fit.GetParErrors()[0])
        self.ErrUp.SetParameter(4, self.fit.GetParErrors()[1])
        self.ErrUp.SetParameter(5, self.fit.GetParErrors()[2])
        self.ErrUp.SetParameter(6, fitter.GetCovarianceMatrixElement(0,1))
        self.ErrUp.SetParameter(7, fitter.GetCovarianceMatrixElement(0,2))
        self.ErrUp.SetParameter(8, fitter.GetCovarianceMatrixElement(1,2))
        self.ErrDn = TF1("QuadrarticFitErrorDn"+self.name, "[0]+ [1]*x + [2]*x*x - sqrt(([3]*[3]) + (2*x*[6]) + (x*x*[4]*[4]) + (2*x*x*[7]) + (2*x*x*x*[8]) + (x*x*x*x*[5]*[5]))",self.rm,self.rp)
        self.ErrDn.SetParameter(0, self.fit.GetParameter(0))
        self.ErrDn.SetParameter(1, self.fit.GetParameter(1))
        self.ErrDn.SetParameter(2, self.fit.GetParameter(2))
        self.ErrDn.SetParameter(3, self.fit.GetParErrors()[0])
        self.ErrDn.SetParameter(4, self.fit.GetParErrors()[1])
        self.ErrDn.SetParameter(5, self.fit.GetParErrors()[2])
        self.ErrDn.SetParameter(6, fitter.GetCovarianceMatrixElement(0,1))
        self.ErrDn.SetParameter(7, fitter.GetCovarianceMatrixElement(0,2))
        self.ErrDn.SetParameter(8, fitter.GetCovarianceMatrixElement(1,2))

    # Makes a string which can be used with TCuts/TChains to weight a plot
    #### var: Variable fit is binned in
    #### center: The x-var is recentered about the middle of the blinded region. This tells where to recenter to. Can be left as 0.
    def MakeConvFactor(self, var, center):
        X = var + "-" + str(center)
        self.ConvFact = "({0:2.9f} + (({3})*{1:2.9f}) + (({3})*({3})*{2:2.9f}))".format(self.ErrUp.GetParameter(0),self.ErrUp.GetParameter(1),self.ErrUp.GetParameter(2),X)
        self.ConvFactUp = "({0:2.9f} + (({9})*{1:2.9f}) + (({9})*({9})*{2:2.9f}) + (({3:2.9f}*{3:2.9f}) + (2*({9})*{6:2.9f}) + (({9})*({9})*{4:2.9f}*{4:2.9f}) + (2*({9})*({9})*{7:2.9f}) + (2*({9})*({9})*({9})*{8:2.9f}) + (({9})*({9})*({9})*({9})*{5:2.9f}*{5:2.9f}))^0.5)".format(self.ErrUp.GetParameter(0),self.ErrUp.GetParameter(1),self.ErrUp.GetParameter(2),self.ErrUp.GetParameter(3),self.ErrUp.GetParameter(4),self.ErrUp.GetParameter(5),self.ErrUp.GetParameter(6),self.ErrUp.GetParameter(7),self.ErrUp.GetParameter(8),X)
        self.ConvFactDn = "({0:2.9f} + (({9})*{1:2.9f}) + (({9})*({9})*{2:2.9f}) - (({3:2.9f}*{3:2.9f}) + (2*({9})*{6:2.9f}) + (({9})*({9})*{4:2.9f}*{4:2.9f}) + (2*({9})*({9})*{7:2.9f}) + (2*({9})*({9})*({9})*{8:2.9f}) + (({9})*({9})*({9})*({9})*{5:2.9f}*{5:2.9f}))^0.5)".format(self.ErrUp.GetParameter(0),self.ErrUp.GetParameter(1),self.ErrUp.GetParameter(2),self.ErrUp.GetParameter(3),self.ErrUp.GetParameter(4),self.ErrUp.GetParameter(5),self.ErrUp.GetParameter(6),self.ErrUp.GetParameter(7),self.ErrUp.GetParameter(8),X)

#### CUBIC ####
class CubicFit:

    # Sets basic variables
    #### init_var: initial parameters, should be of form [x,y,z,a]
    #### range_min: Minimum value of range to fit to
    #### range_max: Maximum value of range to fit to
    #### name: Name for fit function
    #### Opt: Options for fit; 
    ####      FOR range_min, range_max TO BE APPLIED, Opt MUST INCLUDE "R"!!!
    def __init__(self, init_var, range_min, range_max, name, Opt):
        self.Opt = Opt
        self.rm = range_min
        self.rp = range_max
        self.name = name
        self.fit = TF1("CubicFit"+self.name, "[0]+ [1]*x + [2]*x*x + [3]*x*x*x",self.rm,self.rp)
        self.fit.SetParameter(0, init_var[0]) 
        self.fit.SetParameter(1, init_var[1])
        self.fit.SetParameter(2, init_var[2])
        self.fit.SetParameter(3, init_var[3])

    # Makes the fit function with error up and error down
    def Converter(self, fitter):
        errTerm = "[4]^2+((2*[8])*x)+(([5]^2+2*[9])*x^2)+((2*[10]+2*[11])*x^3)+(([6]^2+2*[12])*x^4)+((2*[13])*x^5)+(([7]^2)*x^6)"
        self.ErrUp = TF1("CubicFitErrorUp"+self.name, "[0]+ [1]*x + [2]*x*x + [3]*x*x*x + sqrt("+errTerm+")",self.rm,self.rp)
        self.ErrUp.SetParameter(0, self.fit.GetParameter(0))
        self.ErrUp.SetParameter(1, self.fit.GetParameter(1))
        self.ErrUp.SetParameter(2, self.fit.GetParameter(2))
        self.ErrUp.SetParameter(3, self.fit.GetParameter(3))
        self.ErrUp.SetParameter(4, self.fit.GetParErrors()[0])
        self.ErrUp.SetParameter(5, self.fit.GetParErrors()[1])
        self.ErrUp.SetParameter(6, self.fit.GetParErrors()[2])
        self.ErrUp.SetParameter(7, self.fit.GetParErrors()[3])
        self.ErrUp.SetParameter(8, fitter.GetCovarianceMatrixElement(0,1))
        self.ErrUp.SetParameter(9, fitter.GetCovarianceMatrixElement(0,2))
        self.ErrUp.SetParameter(10, fitter.GetCovarianceMatrixElement(0,3))
        self.ErrUp.SetParameter(11, fitter.GetCovarianceMatrixElement(1,2))
        self.ErrUp.SetParameter(12, fitter.GetCovarianceMatrixElement(1,3))
        self.ErrUp.SetParameter(13, fitter.GetCovarianceMatrixElement(2,3))
        self.ErrDn = TF1("CubicFitErrorUp"+self.name, "[0]+ [1]*x + [2]*x*x + [3]*x*x*x - sqrt("+errTerm+")",self.rm,self.rp)
        self.ErrDn.SetParameter(0, self.fit.GetParameter(0))
        self.ErrDn.SetParameter(1, self.fit.GetParameter(1))
        self.ErrDn.SetParameter(2, self.fit.GetParameter(2))
        self.ErrDn.SetParameter(3, self.fit.GetParameter(3))
        self.ErrDn.SetParameter(4, self.fit.GetParErrors()[0])
        self.ErrDn.SetParameter(5, self.fit.GetParErrors()[1])
        self.ErrDn.SetParameter(6, self.fit.GetParErrors()[2])
        self.ErrDn.SetParameter(7, self.fit.GetParErrors()[3])
        self.ErrDn.SetParameter(8, fitter.GetCovarianceMatrixElement(0,1))
        self.ErrDn.SetParameter(9, fitter.GetCovarianceMatrixElement(0,2))
        self.ErrDn.SetParameter(10, fitter.GetCovarianceMatrixElement(0,3))
        self.ErrDn.SetParameter(11, fitter.GetCovarianceMatrixElement(1,2))
        self.ErrDn.SetParameter(12, fitter.GetCovarianceMatrixElement(1,3))
        self.ErrDn.SetParameter(13, fitter.GetCovarianceMatrixElement(2,3))
        for i in [self.ErrUp, self.ErrDn]:
            i.SetLineStyle(2)

    # Makes a string which can be used with TCuts/TChains to weight a plot
    #### var: Variable fit is binned in
    #### center: The x-var is recentered about the middle of the blinded region. This tells where to recenter to. Can be left as 0.
    def MakeConvFactor(self, var, center):
        X = var + "-" + str(center)
        print X
        self.ConvFact = "({0:6.36f} + (({4})*{1:6.36f}) + (({4})*({4})*{2:6.36f}) + (({4})*({4})*({4})*{3:6.36f}))".format(self.ErrUp.GetParameter(0),self.ErrUp.GetParameter(1),self.ErrUp.GetParameter(2),self.ErrUp.GetParameter(3),X)
        ErrTerm =  "( {0:6.36f}*{0:6.36f} + 2*{4:6.36f}*{10} + ( {1:6.36f}*{1:6.36f} + 2*{5:6.36f} )*({10})*({10}) + ( 2*{6:6.36f} + 2*{7:6.36f} )*({10})*({10})*({10}) + ( {2:6.36f}*{2:6.36f} + 2*{8:6.36f} )*({10})*({10})*({10})*({10}) + (2*{9:6.36f})*({10})*({10})*({10})*({10})*({10}) + ({3:6.36f}*{3:6.36f})*({10})*({10})*({10})*({10})*({10})*({10})  )".format( self.ErrUp.GetParameter(4),self.ErrUp.GetParameter(5),self.ErrUp.GetParameter(6),self.ErrUp.GetParameter(7),self.ErrUp.GetParameter(8),self.ErrUp.GetParameter(9),self.ErrUp.GetParameter(10),self.ErrUp.GetParameter(11),self.ErrUp.GetParameter(12),self.ErrUp.GetParameter(13),X)
        self.ConvFactUp = "(" + self.ConvFact + " + sqrt(" + ErrTerm + ") )"
        self.ConvFactDn = "(" + self.ConvFact + " - sqrt(" + ErrTerm + ") )"

#### LOGARITHMIC ####

#### EXPONENTIAL ####

#### GAUSSIAN ####

#CUSTOM =========--------------=============------------=============-------------===============

#### SIGMOID ####
class SigmoidFit:

    # Sets basic variables
    #### init_var: initial parameters, should be of form [x,y,z]
    #### range_min: Minimum value of range to fit to
    #### range_max: Maximum value of range to fit to
    #### name: Name for fit function
    #### Opt: Options for fit; 
    ####      FOR range_min, range_max TO BE APPLIED, Opt MUST INCLUDE "R"!!!
    def __init__(self, init_var, range_min, range_max, name, Opt):
        self.Opt = Opt
        self.rm = range_min
        self.rp = range_max
        self.name = name
        D = "exp( [1] + [2]*x*x*x )"
        Q = "(1/([0] + "+D+"))"
        self.fit = TF1("SigmoidFit"+self.name, Q, self.rm,self.rp)
        self.fit.SetParameter(0, init_var[0]) 
        self.fit.SetParameter(1, init_var[1])
        self.fit.SetParameter(2, init_var[2])

    # Makes the fit function with error up and error down
    def Converter(self, fitter):
        D = "exp( [1] + [2]*x*x*x )"
        Q = "(1/([0] + "+D+"))^(4)"
#        dfa = Q+"*"+Q
#        dfb = dfa+"*"+D
#        dfc = dfb+"*x*x*x"
#        err1 = (dfa+"*"+dfa+"*[3]*[3]") + "+" + (dfb+"*"+dfb+"*[4]*[4]") + "+" + (dfc+"*"+dfc+"*[4]*[4]")
#        err2 = (dfa+"*"+dfb+"*[6]") + "+" + (dfa+"*"+dfc+"*[7]") + "+" + (dfb+"*"+dfc+"*[8]")
#        errTerm = "math.sqrt(" + err1 + "+" + "2*" + err2 + ")"
        errTerm = "( " + Q + " * ([3]^2 + " + D + "^2 * ([4]^2 + [5]^2*x^6 + 2*[8]*x^3 ) + " + D + " * (2*[6] + 2*[7]*x^3) ))^0.5"
        self.ErrUp = TF1("SigmoidFitErrorUp"+self.name, "(([0]+ exp([1] + [2]*x*x*x))^(-1) + " + errTerm + ")",self.rm,self.rp)
#        self.ErrUp = TF1("SigmoidFitErrorUp"+self.name, Q + "+" + errTerm,self.rm,self.rp)
        self.ErrUp.SetParameter(0, self.fit.GetParameter(0))
        self.ErrUp.SetParameter(1, self.fit.GetParameter(1))
        self.ErrUp.SetParameter(2, self.fit.GetParameter(2))
        self.ErrUp.SetParameter(3, self.fit.GetParErrors()[0])
        self.ErrUp.SetParameter(4, self.fit.GetParErrors()[1])
        self.ErrUp.SetParameter(5, self.fit.GetParErrors()[2])
        self.ErrUp.SetParameter(6, fitter.GetCovarianceMatrixElement(0,1))
        self.ErrUp.SetParameter(7, fitter.GetCovarianceMatrixElement(0,2))
        self.ErrUp.SetParameter(8, fitter.GetCovarianceMatrixElement(1,2))

#        self.ErrDn = TF1("SigmoidFitErrorDn"+self.name,  Q + " - " + errTerm,self.rm,self.rp)
        self.ErrDn = TF1("SigmoidFitErrorDn"+self.name,  "(([0]+ exp([1] + [2]*x*x*x))^(-1) - " + errTerm + ")",self.rm,self.rp)
        self.ErrDn.SetParameter(0, self.fit.GetParameter(0))
        self.ErrDn.SetParameter(1, self.fit.GetParameter(1))
        self.ErrDn.SetParameter(2, self.fit.GetParameter(2))
        self.ErrDn.SetParameter(3, self.fit.GetParErrors()[0])
        self.ErrDn.SetParameter(4, self.fit.GetParErrors()[1])
        self.ErrDn.SetParameter(5, self.fit.GetParErrors()[2])
        self.ErrDn.SetParameter(6, fitter.GetCovarianceMatrixElement(0,1))
        self.ErrDn.SetParameter(7, fitter.GetCovarianceMatrixElement(0,2))
        self.ErrDn.SetParameter(8, fitter.GetCovarianceMatrixElement(1,2))

    # Makes a string which can be used with TCuts/TChains to weight a plot
    #### var: Variable fit is binned in
    #### center: The x-var is recentered about the middle of the blinded region. This tells where to recenter to. Can be left as 0.
    def MakeConvFactor(self, var, center):
        X = var + "-" + str(center)
        self.ConvFact = "( (({0:6.53f}) + exp( ({1:6.53f}) + ({2:6.53f})*({3})*({3})*({3})))**(-1) )".format(self.ErrUp.GetParameter(0),self.ErrUp.GetParameter(1),self.ErrUp.GetParameter(2),X)
        D = "exp( ({0:6.53f}) + ({1:6.53f})*({2})*({2})*({2}) )".format( self.ErrUp.GetParameter(1), self.ErrUp.GetParameter(2), X )
        Q = (" 1/((({0:6.53f}) + "+D+")**4) ").format( self.ErrUp.GetParameter(0) )
        self.ErrTerm = ("sqrt( " + Q + " * (({3:6.53f})*({3:6.53f}) + " + D + " * " + D + " * (({4:6.53f})*({4:6.53}) + ({5:6.53f})*({5:6.53})*({9})*({9})*({9})*({9})*({9})*({9}) + 2*({8:6.53f})*({9})*({9})*({9}) ) + " + D + " * (2*({6:6.53f}) + 2*({7:6.53f})*({9})*({9})*({9})) ))").format(self.ErrUp.GetParameter(0),self.ErrUp.GetParameter(1),self.ErrUp.GetParameter(2),self.ErrUp.GetParameter(3),self.ErrUp.GetParameter(4),self.ErrUp.GetParameter(5),self.ErrUp.GetParameter(6),self.ErrUp.GetParameter(7),self.ErrUp.GetParameter(8),X)
        for i in xrange(0,9):
            print self.ErrUp.GetParameter(i)
#        prunedMassAve=100
#        print "D"
#        print eval(D)
#        print "Q"
#        print eval(Q)
        
        self.ConvFactUp = "("+self.ConvFact + " + " +  self.ErrTerm+")"
        self.ConvFactDn = self.ConvFact + " - " + self.ErrTerm
#        print "ErrTerm"
#        print eval(self.ErrTerm)
#        print "ConvFact"
#        print eval(self.ConvFact)
