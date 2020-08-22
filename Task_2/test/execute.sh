#!/bin/bash




for n in 10 20 100
do
   echo "-----------------Parallel processing------------------- for $n cores"
   mpiexec -n $n python test_mpi.py
   echo "--------------------Finished----------------------------"
done
