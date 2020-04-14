#!/bin/bash

n_procs=$(echo $sudoPW|cat - /proc/cpuinfo|grep -m 1 "cpu cores"|awk '{print $ 4;}')

echo "--------------------- Sequential --------------------"
./bench_seq 

echo "----------------- Multithreading--------------------" 
for n in $(seq 2 2 $n_procs)
do
   ./bench_thread $n
done

echo "-------- Multithreading with multiinterpreters--------"
for n in $(seq 2 2 $n_procs)
do
   ./bench_multi $n
done

echo "-----------------Parallel processing-------------------"

for n in $(seq 2 2 $n_procs)
do
   mpirun -np $n ./bench_MPI
done


echo "------------------Optimized Version-------------------"

echo "--------------------- Sequential --------------------"
./bench_seq_opt

echo "----------------- Multithreading--------------------" 
for n in $(seq 2 2 $n_procs)
do
   ./bench_thread_opt $n
done

echo "-------- Multithreading with multiinterpreters--------"
for n in $(seq 2 2 $n_procs)
do
   ./bench_multi_opt $n
done

echo "-----------------Parallel processing-------------------"

for n in $(seq 2 2 $n_procs)
do
   mpirun -np $n ./bench_MPI_opt
done



