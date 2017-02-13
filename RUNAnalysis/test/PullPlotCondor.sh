#!/bin/sh

export SCRAM_ARCH=slc6_amd64_gcc491
export VO_CMS_SW_DIR=/cms/base/cmssoft
export COIN_FULL_INDIRECT_RENDERING=1
source $VO_CMS_SW_DIR/cmsset_default.sh
eval `scramv1 runtime -sh`

# 1:  0 0 0 0 1
# ...
# 10: 0 1 0 0 1
# ...
# 20: 0 0 1 0 1
# ...
# 30: 0 1 1 0 1
# ...
# 40: 0 0 0 1 1
# ...
# 50: 0 1 0 1 1
# ...
# 60: 0 0 1 1 1
# ...
# 70: 0 1 1 1 1

chan=$(($1))

#if [ $chan -lt 10 ];
#then
#    c=$(($chan%10))
#    if [ $c -lt 9 ];
#	then
#	./PullPlotMaker.sh $c 0 0 0 1
#    fi
#elif [ $chan -lt 20 ];
#then
#    c=$(($chan%10))
#        if [ $c -lt 9 ];
#	then
#	    ./PullPlotMaker.sh $c 1 0 0 1
#	fi
#elif [ $chan -lt 30 ];
#then
#    c=$(($chan%10))
#        if [ $c -lt 9 ];
#	then
#	    ./PullPlotMaker.sh $c 0 1 0 1
#	fi
#elif [ $chan -lt 40 ];
#then
#    c=$(($chan%10))
#        if [ $c -lt 9 ];
#	then
#	    ./PullPlotMaker.sh $c 1 1 0 1
#	fi
if [ $chan -lt 40 ];
then
    echo "Over"
elif [ $chan -lt 50 ];
then
    c=$(($chan%10))
        if [ $c -lt 9 ];
	then
	    ./PullPlotMaker.sh $c 0 0 0 1
	fi
elif [ $chan -lt 60 ];
then
    c=$(($chan%10))
        if [ $c -lt 9 ];
	then
	    ./PullPlotMaker.sh $c 1 0 0 1
	fi
elif [ $chan -lt 70 ];
then
    c=$(($chan%10))
        if [ $c -lt 9 ];
	then
	    ./PullPlotMaker.sh $c 0 1 0 1
	fi
elif [ $chan -lt 80 ];
then
    c=$(($chan%10))
        if [ $c -lt 9 ];
	then
	    ./PullPlotMaker.sh $c 1 1 0 1
	fi
fi