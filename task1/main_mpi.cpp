#include <iostream>
#include <boost/python.hpp>
#include <mpi.h>

using namespace boost::python;


int main()
{
    
    
   
    int rank, comm_size;
    MPI_Init(NULL, NULL);
    MPI_Comm_size(MPI_COMM_WORLD, &comm_size);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    Py_Initialize();
    object main_module = import("__main__");
    object main_namespace = main_module.attr("__dict__");
    list mlist;

    for (int i = 0; i < 10000; ++i)
    {
        mlist.append(i);
    }

    int block_size = int(len(mlist) / comm_size);
    double start, end;
    start = MPI_Wtime(); 
   
   

    for (int j = rank; j < len(mlist); j = j + comm_size)
    {
        for (int i = 0; i < 10000; ++i)
        {
            mlist[i] = mlist[i] + 1;
        }
    }
    MPI_Barrier(MPI_COMM_WORLD);
    end  = MPI_Wtime(); 
    if(rank == 0){
        std::cout << end-start << "seconds" << std::endl; 
    }
    
    MPI_Finalize();

    
    return 0;
}
