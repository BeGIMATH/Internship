
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

void seq_function_opt(int list_length);

void partial_change(int start_it, int chunk_size, list l);

void partial_change_opt(int start_it, int chunk_size, list l);

void threads_function(int threads_to_use, int list_length);

void threads_function_opt(int threads_to_use, int list_length);

void partial_change_multi(PyInterpreterState *interp, int start_it, int chunk, list *final, list *l, int id);

void partial_change_multi_opt(PyInterpreterState *interp, int start_it, int chunk, list *final, list *l, int id);

void threads_multi_function(int threads_to_use, int list_length);

void threads_multi_function_opt(int threads_to_use, int list_length);

void pure_mpi_function(int list_length);

void pure_mpi_function_opt(int list_length);

void pickle_dump_function(int list_length); 