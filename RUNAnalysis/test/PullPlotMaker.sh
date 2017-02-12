export SCRAM_ARCH=slc6_amd64_gcc491
export VO_CMS_SW_DIR=/cms/base/cmssoft
export COIN_FULL_INDIRECT_RENDERING=1
source $VO_CMS_SW_DIR/cmsset_default.sh
eval `scramv1 runtime -sh`

#    $1 is channel
#    $2 is CBD or BCD (0 = CBD, 1 = BCD)
#    $3 is btag (0 = CMVAv2, 1 = CSVv2 )
#    $4 is MC or DATA (0 = MC, 1 = DATA)
#    $5 is plot (0 = True, 1 = False)

str="Before"

if [ $2 -eq "0" ];
then
    str+="CBD"
fi
if [ $2 -eq "1" ];
then
    str+="BCD"
fi
if [ $3 -eq "0" ];
then
    str+="CMVAv2"
fi
if [ $3 -eq "1" ];
then
    str+="CSVv2"
fi
if [ $4 -eq "0" ];
then
    str+="MC"
fi
if [ $4 -eq "1" ];
then
    str+="DATA"
fi
if [ $5 -eq "0" ];
then
    python PullPlotMaker.py -c $1 -p_t -m $str -d "/ThetaPullBefore/29172Before"$1
fi
if [ $5 -eq "1" ];
then 
    echo $str
    python PullPlotMaker.py -c $1 -p_f -m $str -d "/ThetaPullBefore/29172Before"$1
fi