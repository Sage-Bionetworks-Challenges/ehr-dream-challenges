#!/bin/bash

file_path=/data/users/yanyao/myproj/synpuf/omop/data_collection/1_random/feature_extraction

for f in $file_path/*.py
do
	nohup python $f&
done
