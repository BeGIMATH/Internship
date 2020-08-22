#!/bin/bash

n_procs=$(echo $sudoPW|cat - /proc/cpuinfo|grep -m 1 "cpu cores"|awk '{print $ 4;}')

echo "--------------------- Sequential --------------------"
./bench_seq 

echo "----------------- Multithreading--------------------" 
for n in 4 8 16 32 64 128
do
   ./bench_thread $n
done

echo "-------- Multithreading with multiinterpreters--------"
for n in 4 8 16 32 64 128
do
   ./bench_multi $n
done

echo "-----------------Parallel processing-------------------"

for n in 4 8 16 32 64 128
do
   mpirun -np $n ./bench_MPI
done

