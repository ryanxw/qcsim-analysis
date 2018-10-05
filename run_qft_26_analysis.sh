#!/bin/bash
#COBALT -t 10:00:00
#COBALT -n 1
#COBALT -A IntelQS
#COBALT -q knl_7210
#COBALT -O qft_26_analysis

# Various env settings are provided by Cobalt
# echo $COBALT_JOBID  $COBALT_PARTNAME  $COBALT_JOBSIZE

#aprun -n 4 -N 4 -d 1 -j 1 -cc depth /home/xinchuan/analysis.sh

#cd /home/xinchuan/intel-qs-ryan/error_eval/h_c_30
cd /home/xinchuan/intel-qs-ryan/error_eval/qft_26
/home/xinchuan/intel-qs-ryan/error_eval/qft_26/analysis.sh
#cd /home/xinchuan/intel-qs-ryan/error_eval/qft_20/baseline
#cd /home/xinchuan/intel-qs-ryan/error_eval/qft_20/PW_REL_5-3

#EXE=/home/xinchuan/intel-qs-ryan/bin/
#CIR=/home/xinchuan/intel-qs-ryan/error_eval/qft_20/qft_20.qasmf
#mpirun -n 8  -ppn 32 $EXE < $CIR
#$EXE/baseline_with_output.exe < $CIR
#$EXE/zstd_with_output.exe < $CIR
#$EXE/sz_no_output_abs_10-4.exe < $CIR
#$EXE/sz_no_output_pw_5-3.exe < $CIR

status=$?

# could do another aprun here...

exit $status
