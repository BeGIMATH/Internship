
#include <iostream>
#include <boost/mpi.hpp>
#include <boost/mpi/python.hpp>
#include <boost/serialization/string.hpp>
using namespace boost::python;
namespace mpi = boost::mpi;

//#include "serial.h"
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
    object my_pickle = import("pickle");


    PyObject* m_dumps = object(my_pickle.attr("dumps")).ptr();
    PyObject* m_loads = object(my_pickle.attr("dumps")).ptr();
    // >>> dog.bark("woof");
    
    
    exec("def f(x):\n"
         "  return x + 1\n"
         "\n", main_namespace);
    
    PyObject* f = object(main_module.attr("f")).ptr();

    mpi::timer T;
    list mlist;
    
    int el;
    int local_el;
   
    
    
    

    /*
    for (int i = 0; i < 10000; ++i)
    {
             mlist.append(i);
    }
     */
    /*
    for (int j = 0; j < 10000; ++j)
    {
           
        for (int i = world.rank(); i < len(mlist); i = i + world.size())
        {
                el  = extract<int>(mlist[i]);
                mlist[i] = call<int>(f,el);
        }
    }
    
    */

    list local_l;

    
    if(world.rank() == 0){  
        list local_l;
        for (int i = 0; i < 100; ++i)
        {
             local_l.append(i);
        }
        object Local_l;
        
        std::string s_Local_l = call<std::string>(m_dumps,Local_l);  
        int len = s_Local_l.length();  
        world.send(1,0,s_Local_l);
    }
    /*}
    else{
        object Local_l;
        //boost::mpi::content c;
        //boost::mpi::python::communicator_recv_content(world,0,0,c);
        world.recv(0,0,Local_l);
    }
    */
    double time = T.elapsed();
    
    if (world.rank() == 0)
    {
        std::cout << "Runtime =  " << time << std::endl;   
    }
    return 0;
}

