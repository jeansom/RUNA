# A bunch of CONVERTERS for the Fit part of Alphabet.

import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy

#### LINEAR ####
class LinearFit:
    def __init__(self, init_var, range_min, range_max, name, Opt):
        self.Opt = Opt
        self.rm = range_min
        self.rp = range_max
        self.name = name
        self.fit = TF1("LinearFit_"+self.name, "[0]+ [1]*x",self.rm,self.rp)
        self.fit.SetParameter(0, init_var[0]) 
        self.fit.SetParameter(1, init_var[1])
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
    def MakeConvFactor(self, var, center):
        X = var + "-" + str(center)
        self.ConvFact = "({0:2.9f} + (({2})*{1:2.9f}))".format(self.ErrUp.GetParameter(0),self.ErrUp.GetParameter(1),X)
        self.ConvFactUp = "({0:2.9f} + (({5})*{1:2.9f}) + (({5})*({5})*{3:2.9f}*{3:2.9f}+(({5})*2*{4:2.9f})+({2:2.9f}*{2:2.9f}))^0.5)".format(self.ErrUp.GetParameter(0),self.ErrUp.GetParameter(1),self.ErrUp.GetParameter(2),self.ErrUp.GetParameter(3),self.ErrUp.GetParameter(4),X)
        self.ConvFactDn = "({0:2.9f} + (({5})*{1:2.9f}) - (({5})*({5})*{3:2.9f}*{3:2.9f}+(({5})*2*{4:2.9f})+({2:2.9f}*{2:2.9f}))^0.5)".format(self.ErrUp.GetParameter(0),self.ErrUp.GetParameter(1),self.ErrUp.GetParameter(2),self.ErrUp.GetParameter(3),self.ErrUp.GetParameter(4),X)

#### QUADRATIC ####

class QuadraticFit:
    def __init__(self, init_var, range_min, range_max, name, Opt):
        self.Opt = Opt
        self.rm = range_min
        self.rp = range_max
        self.name = name
        self.fit = TF1("QuadraticFit", "[0]+ [1]*x + [2]*x*x",self.rm,self.rp)
#        self.fit.SetParameter(0, init_var[0]) 
#        self.fit.SetParameter(1, init_var[0])
#        self.fit.SetParameter(2, init_var[0])
        #self.fit.SetParLimits(2,0,20)
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
    def MakeConvFactor(self, var, center):
        X = var + "-" + str(center)
        self.ConvFact = "({0:2.9f} + (({3})*{1:2.9f}) + (({3})*({3})*{2:2.9f}))".format(self.ErrUp.GetParameter(0),self.ErrUp.GetParameter(1),self.ErrUp.GetParameter(2),X)
        self.ConvFactUp = "({0:2.9f} + (({9})*{1:2.9f}) + (({9})*({9})*{2:2.9f}) + (({3:2.9f}*{3:2.9f}) + (2*({9})*{6:2.9f}) + (({9})*({9})*{4:2.9f}*{4:2.9f}) + (2*({9})*({9})*{7:2.9f}) + (2*({9})*({9})*({9})*{8:2.9f}) + (({9})*({9})*({9})*({9})*{5:2.9f}*{5:2.9f}))^0.5)".format(self.ErrUp.GetParameter(0),self.ErrUp.GetParameter(1),self.ErrUp.GetParameter(2),self.ErrUp.GetParameter(3),self.ErrUp.GetParameter(4),self.ErrUp.GetParameter(5),self.ErrUp.GetParameter(6),self.ErrUp.GetParameter(7),self.ErrUp.GetParameter(8),X)
        self.ConvFactDn = "({0:2.9f} + (({9})*{1:2.9f}) + (({9})*({9})*{2:2.9f}) - (({3:2.9f}*{3:2.9f}) + (2*({9})*{6:2.9f}) + (({9})*({9})*{4:2.9f}*{4:2.9f}) + (2*({9})*({9})*{7:2.9f}) + (2*({9})*({9})*({9})*{8:2.9f}) + (({9})*({9})*({9})*({9})*{5:2.9f}*{5:2.9f}))^0.5)".format(self.ErrUp.GetParameter(0),self.ErrUp.GetParameter(1),self.ErrUp.GetParameter(2),self.ErrUp.GetParameter(3),self.ErrUp.GetParameter(4),self.ErrUp.GetParameter(5),self.ErrUp.GetParameter(6),self.ErrUp.GetParameter(7),self.ErrUp.GetParameter(8),X)

#### CUBIC ####
class CubicFit:
    def __init__(self, init_var, range_min, range_max, name, Opt):
        self.Opt = Opt
        self.rm = range_min
        self.rp = range_max
        self.name = name
        self.fit = TF1("CubicFit"+self.name, "[0]+ [1]*x + [2]*x^2 + [3]*x^3",self.rm,self.rp)
        self.fit.SetParameter(0, init_var[0]) 
        self.fit.SetParameter(1, init_var[1])
#        self.fit.SetParameter(2, init_var[2])
#        self.fit.SetParameter(3, init_var[3])
    def Converter(self, fitter):
        #errTerm = "[4]^2 +((2*[8])*x) + (([5]^2+2*[9])*x^2) + ((2*[11])*x^3)"
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
    def MakeConvFactor(self, var, center):
        X = var + "-" + str(center)
        print X
        self.ConvFact = "({0:2.9f} + (({4})*{1:2.9f}) + (({4})*({4})*{2:2.9f}) + (({4})*({4})*({4})*{3:2.9f}))".format(self.ErrUp.GetParameter(0),self.ErrUp.GetParameter(1),self.ErrUp.GetParameter(2),self.ErrUp.GetParameter(3),X)
#        self.ConvFactUp = "({0:2.9f} + (({9})*{1:2.9f}) + (({9})*({9})*{2:2.9f}) + (({3:2.9f}*{3:2.9f}) + (2*({9})*{6:2.9f}) + (({9})*({9})*{4:2.9f}*{4:2.9f}) + (2*({9})*({9})*{7:2.9f}) + (2*({9})*({9})*({9})*{8:2.9f}) + (({9})*({9})*({9})*({9})*{5:2.9f}*{5:2.9f}))^0.5)".format(self.ErrUp.GetParameter(0),self.ErrUp.GetParameter(1),self.ErrUp.GetParameter(2),self.ErrUp.GetParameter(3),self.ErrUp.GetParameter(4),self.ErrUp.GetParameter(5),self.ErrUp.GetParameter(6),self.ErrUp.GetParameter(7),self.ErrUp.GetParameter(8),X)
#        self.ConvFactDn = "({0:2.9f} + (({9})*{1:2.9f}) + (({9})*({9})*{2:2.9f}) - (({3:2.9f}*{3:2.9f}) + (2*({9})*{6:2.9f}) + (({9})*({9})*{4:2.9f}*{4:2.9f}) + (2*({9})*({9})*{7:2.9f}) + (2*({9})*({9})*({9})*{8:2.9f}) + (({9})*({9})*({9})*({9})*{5:2.9f}*{5:2.9f}))^0.5)".format(self.ErrUp.GetParameter(0),self.ErrUp.GetParameter(1),self.ErrUp.GetParameter(2),self.ErrUp.GetParameter(3),self.ErrUp.GetParameter(4),self.ErrUp.GetParameter(5),self.ErrUp.GetParameter(6),self.ErrUp.GetParameter(7),self.ErrUp.GetParameter(8),X)
        self.ConvFactUp = "({0:2.9f} + (({14})*{1:2.9f}) + (({14})*({14})*{2:2.9f}) + (({14})*({14})*({14})*{3:2.9f}) + (( ({4:2.9f}*{4:2.9f}) + (2*{8:2.9f}*({14})) + (( {5:2.9f}*{5:2.9f}+2*{9:2.9f})*(({14})*({14}))) + ((2*{10:2.9f}+2*{11:2.9f})*(({14})*({14})*({14}))) + ((({6:2.9f}*{6:2.9f}) + 2*{12:2.9f} )*(({14})*({14})*({14})*({14}))) + ( 2*{13:2.9f}*(({14})*({14})*({14})*({14})*({14}))) + ( ({7:2.9f}*{7:2.9f})*(({14})*({14})*({14})*({14})*({14})*({14}))) )^0.5))".format(self.ErrUp.GetParameter(0),self.ErrUp.GetParameter(1),self.ErrUp.GetParameter(2),self.ErrUp.GetParameter(3),self.ErrUp.GetParameter(4),self.ErrUp.GetParameter(5),self.ErrUp.GetParameter(6),self.ErrUp.GetParameter(7),self.ErrUp.GetParameter(8),self.ErrUp.GetParameter(9),self.ErrUp.GetParameter(10),self.ErrUp.GetParameter(11),self.ErrUp.GetParameter(12),self.ErrUp.GetParameter(13),X)
        self.ConvFactDn = "({0:2.9f} + (({14})*{1:2.9f}) + (({14})*({14})*{2:2.9f}) + (({14})*({14})*({14})*{3:2.9f}) - (( ({4:2.9f}*{4:2.9f}) + (2*{8:2.9f}*({14})) + (( {5:2.9f}*{5:2.9f}+2*{9:2.9f})*(({14})*({14}))) + ((2*{10:2.9f}+2*{11:2.9f})*(({14})*({14})*({14}))) + ((({6:2.9f}*{6:2.9f}) + 2*{12:2.9f} )*(({14})*({14})*({14})*({14}))) + ( 2*{13:2.9f}*(({14})*({14})*({14})*({14})*({14}))) + ( ({7:2.9f}*{7:2.9f})*(({14})*({14})*({14})*({14})*({14})*({14}))) )^0.5))".format(self.ErrUp.GetParameter(0),self.ErrUp.GetParameter(1),self.ErrUp.GetParameter(2),self.ErrUp.GetParameter(3),self.ErrUp.GetParameter(4),self.ErrUp.GetParameter(5),self.ErrUp.GetParameter(6),self.ErrUp.GetParameter(7),self.ErrUp.GetParameter(8),self.ErrUp.GetParameter(9),self.ErrUp.GetParameter(10),self.ErrUp.GetParameter(11),self.ErrUp.GetParameter(12),self.ErrUp.GetParameter(13),X)
#### LOGARITHMIC ####

#### EXPONENTIAL ####

#### GAUSSIAN ####

#CUSTOM =========--------------=============------------=============-------------===============

#### SIGMOID ####
class SigmoidFit:
    def __init__(self, init_var, range_min, range_max, name, Opt):
        self.Opt = Opt
        self.rm = range_min
        self.rp = range_max
        self.name = name
        self.fit = TF1("SigmoidFit"+self.name, "([0]+ exp([1] + [2]*x*x*x))^(-1)",self.rm,self.rp)
        self.fit.SetParameter(0, init_var[0]) 
        self.fit.SetParameter(1, init_var[1])
#        self.fit.SetParameter(2, init_var[2])
#        self.fit.SetParameter(3, init_var[3])
    def Converter(self, fitter):
        errTerm = "( sqrt(( exp( [1] + [2]*x*x*x )^2)*( [4]*[4] + x*x*x*x*x*x*[5]*[5] + x*x*x*[8]*[8]) + 2*( exp( [1] + [2]*x*x*x ) )*( [6]*[6] + x*x*x*[7]*[7] ) + [3]*[3] ) / ( [0] + exp( [1] + [2]*x*x*x ) )^2)"
        self.ErrUp = TF1("SigmoidFitErrorUp"+self.name, "(([0]+ exp([1] + [2]*x*x*x))^(-1) + " + errTerm + ")",self.rm,self.rp)
        self.ErrUp.SetParameter(0, self.fit.GetParameter(0))
        self.ErrUp.SetParameter(1, self.fit.GetParameter(1))
        self.ErrUp.SetParameter(2, self.fit.GetParameter(2))
        self.ErrUp.SetParameter(3, self.fit.GetParErrors()[0])
        self.ErrUp.SetParameter(4, self.fit.GetParErrors()[1])
        self.ErrUp.SetParameter(5, self.fit.GetParErrors()[2])
        self.ErrUp.SetParameter(6, fitter.GetCovarianceMatrixElement(0,1))
        self.ErrUp.SetParameter(7, fitter.GetCovarianceMatrixElement(0,2))
        self.ErrUp.SetParameter(8, fitter.GetCovarianceMatrixElement(1,2))
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
    def MakeConvFactor(self, var, center):
        X = var + "-" + str(center)
        self.ConvFact = "( ({0:2.9f} + exp( {1:2.9f} + {2:2.9f}*({3})*({3})*({3})))^(-1) )".format(self.ErrUp.GetParameter(0),self.ErrUp.GetParameter(1),self.ErrUp.GetParameter(2),X)
        self.ConvFactUp = "(( ({0:2.9f} + exp( {1:2.9f} + {2:2.9f}*({9})*({9})*({9})))^(-1) ) + (( sqrt(( exp( ({1:2.9f}) + ({2:2.9f})*({9})*({9})*({9}) )^2)*( ({4})*({4}) + ({9})*({9})*({9})*({9})*({9})*({9})*({5})*({5}) + ({9})*({9})*({9})*({8})*({8})) + 2*( exp( ({1:2.9f}) + ({2:2.9f})*({9})*({9})*({9}) ) )*( ({6})*({6}) + ({9})*({9})*({9})*({7})*({7}) ) + ({3})*({3}) ) / ( ({0}) + exp( ({1:2.9f}) + ({2:2.9f})*({9})*({9})*({9}) ) )^2)) )".format(self.ErrUp.GetParameter(0),self.ErrUp.GetParameter(1),self.ErrUp.GetParameter(2),self.ErrUp.GetParameter(3),self.ErrUp.GetParameter(4),self.ErrUp.GetParameter(5),self.ErrUp.GetParameter(6),self.ErrUp.GetParameter(7),self.ErrUp.GetParameter(8),X)
        self.ConvFactDn = "(( ({0:2.9f} + exp( {1:2.9f} + {2:2.9f}*({9})*({9})*({9})))^(-1) ) + (( sqrt(( exp( ({1:2.9f}) + ({2:2.9f})*({9})*({9})*({9}) )^2)*( ({4})*({4}) + ({9})*({9})*({9})*({9})*({9})*({9})*({5})*({5}) + ({9})*({9})*({9})*({8})*({8})) + 2*( exp( ({1:2.9f}) + ({2:2.9f})*({9})*({9})*({9}) ) )*( ({6})*({6}) + ({9})*({9})*({9})*({7})*({7}) ) + ({3})*({3}) ) / ( ({0}) + exp( ({1:2.9f}) + ({2:2.9f})*({9})*({9})*({9}) ) )^2)) )".format(self.ErrUp.GetParameter(0),self.ErrUp.GetParameter(1),self.ErrUp.GetParameter(2),self.ErrUp.GetParameter(3),self.ErrUp.GetParameter(4),self.ErrUp.GetParameter(5),self.ErrUp.GetParameter(6),self.ErrUp.GetParameter(7),self.ErrUp.GetParameter(8),X)
