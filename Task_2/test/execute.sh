#!/bin/bash




for n in 2 4 6
do
   echo "-----------------Parallel processing------------------- for $n cores"
   mpiexec -n $n python test_mpi.py
   echo "--------------------Finished----------------------------"
done
