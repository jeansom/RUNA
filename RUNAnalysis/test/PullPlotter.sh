#!/bin/bash

python PullPlotMaker.py -c -1 -m AfterCBDCMVAv2DATA -d /ThetaPullBefore/29172After -p_t
python PullPlotMaker.py -c -1 -m AfterBCDCMVAv2DATA -d /ThetaPullBefore/29172After -p_t
python PullPlotMaker.py -c -1 -m AfterCBDCSVv2DATA -d /ThetaPullBefore/29172After -p_t
python PullPlotMaker.py -c -1 -m AfterBCDCSVv2DATA -d /ThetaPullBefore/29172After -p_t