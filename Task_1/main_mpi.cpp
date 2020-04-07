
#include <iostream>
#include <boost/mpi.hpp>
#include <boost/mpi/python.hpp>
#include <boost/serialization/string.hpp>
#include <fstream>
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
  
    
    exec("def f(x):\n"
         "  return x + 1\n"
         "\n", main_namespace);
    
    PyObject* f = object(main_module.attr("f")).ptr();
    object my_pickle = import("pickle");

    PyObject* m_dumps = object(my_pickle.attr("dumps")).ptr();
    PyObject* m_loads = object(my_pickle.attr("loads")).ptr();
   
    mpi::timer T;
    //list mlist;
    

    
    
    
    //std::cout << chunk << std::endl;
    
    list global_l;
    
    if(world.rank() != 0){  
        list local_l;
        int il;
        std::string s_mlist;
        
        world.recv(0,0,s_mlist);
        PyObject* ps_Local_l = PyBytes_FromStringAndSize(s_mlist.c_str(), s_mlist.size());
        auto retval = boost::python::object(boost::python::handle<>(ps_Local_l));
        list mlist = call<list>(m_loads,retval);

        int chunk = int(len(mlist)/size);
        for (int i = 0; i < chunk; ++i)
        {
             il  = extract<int>(mlist[i + chunk*rank]);
             local_l.append(il);
        }
        
        int el;
        for (int j = 0; j < 10000; ++j)
        {
           for (int i = rank; i < len(local_l); i++)
            {
                el  = extract<int>(local_l[i]);
                local_l[i] = call<int>(f,el);
            }
        }
        
        std::string s_Local_l = call<std::string>(m_dumps,local_l);  
                                 
        world.send(0,rank,s_Local_l);
    }
    
    else{
         list mlist;
         for (int i = 0; i < 10000; ++i)
         {
             mlist.append(i);
         }
        std::string s_mlist = call<std::string>(m_dumps,mlist);
        for(int i = 1; i < size; i++){
            world.send(i,0,s_mlist);
        }
        
        int chunk = int(len(mlist)/size);
        list local_l;
        int il;
        for (int i = 0; i < chunk; ++i)
        {
             il  = extract<int>(mlist[i]);
             local_l.append(il);
        }
        int el;
        for (int j = 0; j < 10000; ++j)
        {
           for (int i = 0; i < len(local_l); i++)
            {
                el  = extract<int>(local_l[i]);
                local_l[i] = call<int>(f,el);
            }
        }
       
        global_l += local_l;
        
        std::string s_Local_l;
        for(int i = 1; i < size; i++){
            world.recv(i,i,s_Local_l);
            PyObject* ps_Local_l = PyBytes_FromStringAndSize(s_Local_l.c_str(), s_Local_l.size());
            auto retval = boost::python::object(boost::python::handle<>(ps_Local_l));
            list LOCAL_l = call<list>(m_loads,retval);
            global_l += LOCAL_l;
        }
        
        std::ofstream myfile;
        myfile.open("example.txt");
        
        
        for(int i=0; i < len(global_l); i++){
            myfile << "Nr " << i << " " << extract<int>(global_l[i]) << std::endl;
        }
        
        myfile.close();
        
        
        
    }
    
    double time = T.elapsed();
    
    if (world.rank() == 0)
    {
        std::cout << "Time it takes " << time << std::endl;
    }
    return 0;
}

