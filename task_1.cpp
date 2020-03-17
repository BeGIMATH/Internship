#include <iostream>
#include <boost/python.hpp>
#include <boost/mpi.hpp>
#include <boost/mpi/communicator.hpp>
#include <boost/mpi/environment.hpp>

using namespace boost::python;
namespace mpi = boost::mpi;

int main(int argc, char* argv[]){
    

    mpi::environment env;
    mpi::communicator world;
    Py_Initialize();
    object main_module = import("__main__");
    object main_namespace = main_module.attr("__dict__");
    list mlist;
    
    for(int i=0; i< 10000;++i){
         mlist.append(i);
    }
    
    //block_size = int(world.size()/len(mlist));
    
    //for(int j=world.rank(); j < world.rank() + block_size;++j){
    for(int j=0; j<10000; j++){
        for(int i=0; i< 10000;++i)
        {
            mlist[i]= mlist[i] + 1;
        }
    }
            
    //}

    
    return 0;
}