#include <iostream>
#include <boost/python.hpp>
#include <boost/mpi/communicator.hpp>
#include <boost/mpi/environment.hpp>
#include <boost/mpi/timer.hpp>

using namespace boost::python;
namespace mpi = boost::mpi;

int main(int argc, char *argv[])
{
    double start, end;
    int rank,size;
    
    mpi::environment env;
    mpi::communicator world;
    rank = rank;
    size = world.size();
    Py_Initialize();
    object main_module = import("__main__");
    object main_namespace = main_module.attr("__dict__");
    list mlist; 
    
    
    exec("def f(x):\n"
         "  return x + 1\n"
         "\n", main_namespace);
    
    PyObject* f = object(main_module.attr("f")).ptr();
    
    mpi::timer T;
    for (int i = 0; i < 10000; ++i)
    {
        mlist.append(i);
    }
    
    int block_size = int(len(mlist) / size);
    
    int el;
    
    for (int j = 0; j < 10000; ++j)
    {
           
        for (int i = world.rank(); i < len(mlist); i = i + world.size())
        {
                el  = extract<int>(mlist[i]);
                mlist[i] = call<int>(f,el);
        }
    }
        
    
    
    world.barrier();
    double time = T.elapsed();
    if (world.rank() == 0)
    {
        std::cout << "Runtime =  " << time << std::endl;
        for(int i=0; i < 1000; i++){
        std::cout << extract<int>(mlist[i]) << std::endl;
    }
    }

    
    
    return 0;
}
