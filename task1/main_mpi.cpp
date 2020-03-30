
#include <iostream>
#include <boost/mpi.hpp>
#include <boost/python.hpp>
#include <boost/serialization/string.hpp>
//#include <string>

using namespace boost::python;
namespace mpi = boost::mpi;

#include "serial.h"
//BOOST_IS_MPI_DATATYPE(boost::python::list);
int main()
{
    double start, end;
    boost::mpi::environment env;
    boost::mpi::communicator world;
    int size = world.size();
    int rank = world.rank();
    Py_Initialize();
    object main_module = import("__main__");
    object main_namespace = main_module.attr("__dict__");
    mpi::timer T;
    
    exec("def f(x):\n"
         "  return x + 1\n"
         "\n", main_namespace);
    
    PyObject* f = object(main_module.attr("f")).ptr();
    
    //int block_size = int(len(mlist) / world.size());
    
    
    
    
    int el;
    int local_el;
   
    list local_l;
    list global_l;
    list mlist;
    
    std::string string_l;

    int len_l;
    if(world.rank() != 0){  
        
        for (int i = 0; i < 100; ++i)
        {
             local_l.append(i);
        }
                                                                                  
        boost::python::str py_string = boost::python::pickle::dumps(local_l);
        len_l = boost::python::extract<int>(py_string.attr("__len__")());
        string_l = boost::python::extract<std::string>(py_string);
        //ar << len << boost::spickle::data;pickle::data;erialization::make_array(string, len);

        
        world.send(0,0,string_l);
        world.send(0,1,len_l);
         
    }
    
    else{
        
        for(int i=1; i < world.size(); i++){
            world.recv(i,0,string_l);
            world.recv(i,0,len_l);
            
            //boost::python::str py_string(string_l);
            //global_l += boost::python::pickle::loads(py_string);
            
        }
     
        
    }
    
    double time = T.elapsed();
    
    if (world.rank() == 0)
    {
        std::cout << "Runtime =  " << time << std::endl;
        for(int i=0; i < 1000; i++){
            std::cout << extract<int>(global_l[i]) << std::endl;
        }
    }
    
    return 0;
}
