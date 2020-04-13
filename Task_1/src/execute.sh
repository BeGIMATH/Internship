#!/bin/bash

n_procs=$(echo $sudoPW|cat - /proc/cpuinfo|grep -m 1 "cpu cores"|awk '{print $ 4;}')

echo "------------------- Sequential -------------------"
./task1_seq 

echo "------------------- Multithreading-------------------"
for n in $(seq 2 2 $n_procs)
do
   ./task1_thread $n
done

echo "------------------- Multithreading with multiinterpreters-------------------"
for n in $(seq 2 2 $n_procs)
do
   ./task1_multi $n
done

echo "------------------- Parallel processing-------------------"

for n in $(seq 2 2 $n_procs)
do
   mpirun -np $n ./task1_MPI
done



