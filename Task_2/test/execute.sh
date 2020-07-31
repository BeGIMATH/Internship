#!/bin/bash


echo "-----------------Parallel processing-------------------"

for n in 2 4 6
do
   mpiexec -n $n python test_mpi.py 
done
