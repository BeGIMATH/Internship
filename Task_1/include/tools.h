
#include <chrono>
#include <iostream>                   
#include <boost/chrono.hpp>           
#include <boost/thread.hpp>           
#include <vector>                 
#include <string>
#include <mpi.h>
#include <boost/python.hpp>
#include <Python.h>
using namespace boost::python;

void seq_function(int list_length);

void partial_change(int start_it, int chunk_size,list l);

void threads_function(int threads_to_use,int list_length);

void f(PyInterpreterState* interp,int start_it,int chunk,list *final,list* l,int id);

void threads_multi_function(int threads_to_use,int list_length);

void pure_mpi_function(int length);