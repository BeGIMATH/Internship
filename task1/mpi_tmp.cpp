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

    mpi::environment env;
    mpi::communicator world;
    Py_Initialize();
    object main_module = import("__main__");
    object main_namespace = main_module.attr("__dict__");
    list mlist;

    for (int i = 0; i < 10000; ++i)
    {
        mlist.append(i);
    }

    int block_size = int(len(mlist) / world.size());
    mpi::timer T;

    for (int j = world.rank(); j < len(mlist); j = j + world.size())
    {
        for (int i = 0; i < 10000; ++i)
        {
            mlist[i] = mlist[i] + 1;
        }
    }
    world.barrier();
    double time = T.elapsed();
    if (world.rank() == 0)
    {
        std::cout << "Runtime =  " << time;
    }

    return 0;
}
