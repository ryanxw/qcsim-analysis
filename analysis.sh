#!/bin/bash
#test_array=("REL_0.1" "REL_0.01" "PW_REL_0.01" "ABS_0.001" "PW_REL_0.001" "PSNR_60")
#test_array=("PW_REL_1E-2")
test_array=("PW_REL_1E-2_256n" "zstd_256n")
test_name="qft_30_run"
test_path="/projects/QCSim/""$test_name"
base=$test_path"/baseline/"

for i in $(seq 0 $(((${#test_array[*]}-1))))
do
	sz_test=$test_path/${test_array[$i]}
	python $test_path/analyze.py $sz_test $base
done

