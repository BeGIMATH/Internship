#include <iostream>

#include <fstream>
#include <boost/python.hpp>
#include <chrono>
#include <boost/mpi/python/serialize.hpp>
using namespace boost::python;

int main(int argc, char *argv[])
{
    Py_Initialize();
    object main_module = import("__main__");
    object main_namespace = main_module.attr("__dict__");
    list mlist;
   
    
    for (int i = 0; i < 10000; ++i)
    {
        mlist.append(i);
    }
    

    exec("def f(x):\n"
         "  return x + 1\n"
         "\n", main_namespace);
    
    PyObject* f = object(main_module.attr("f")).ptr();
    object my_pickle = import("pickle");


    PyObject* m_dumps = object(my_pickle.attr("dumps")).ptr();
    PyObject* m_loads = object(my_pickle.attr("loads")).ptr();
    PyObject* m_dump = object(my_pickle.attr("dump")).ptr();
    PyObject* m_load = object(my_pickle.attr("load")).ptr();
    
    auto start = std::chrono::high_resolution_clock::now();

    
    int el;

    
    
    
    
    for (int j = 0; j < 10000; j++)
    {
        for (int i = 0; i < 10000; ++i)
        {
            el  = extract<int>(mlist[i]);
            mlist[i] = call<int>(f,el);
        }
    }

    
    
                                                                            
    auto stop = std::chrono::high_resolution_clock::now();
    auto elapsed = std::chrono::duration<double>(stop - start).count();
    
    std::cout << elapsed << " seconds." << std::endl;
    std::ofstream myfile;
        myfile.open("example.txt");
        if(myfile.is_open()){

        for(int i=0; i < len(mlist); i++){
            myfile << "Nr " << i << " " << extract<int>(mlist[i]) << std::endl;
        }
        
        myfile.close();
        }
        else std::cout << "Unable to open file";
    std::cout << len(mlist) << std::endl;
    return 0;
  
}
