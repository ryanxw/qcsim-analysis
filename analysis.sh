#!/bin/bash
#test_array=("REL_0.1" "REL_0.01" "PW_REL_0.01" "ABS_0.001" "PW_REL_0.001" "PSNR_60")
test_array=("PW_REL_1E-1")
#test_array=("PW_REL_5E-2" "PW_REL_1E-2" "zstd")
test_name="qft_20"
test_path="/home/xinchuan/intel-qs-ryan/error_eval/""$test_name"
base=$test_path"/baseline/"

for i in $(seq 0 $(((${#test_array[*]}-1))))
do
	sz_test=$test_path/${test_array[$i]}
	#python $test_path/analyze.py $sz_test $base
	mpiexec -np 64 python $test_path/analyze.py $sz_test $base
done

