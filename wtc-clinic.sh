#!/bin/bash
declare -a my_array
while (( "$#" )); do 
    my_array+=($1)
    shift 
done
python3 main.py "${my_array[@]}"