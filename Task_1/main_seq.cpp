#include <iostream>

#include <fstream>
#include <boost/python.hpp>
#include <chrono>

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
    
    
    int el;
    auto start = std::chrono::high_resolution_clock::now();
    for (int j = 0; j < 100; j++)
    {
        for (int i = 0; i < 100; ++i)
        {
            el  = extract<int>(mlist[i]);
            mlist[i] = call<int>(f,el);
        }
    }
    /*
    exec("file = open('text.obj', 'w')"
         "\n", main_namespace);
    PyObject* file = object(main_module.attr("file")).ptr();
    call<std::fstream>(m_dump,mlist,file);
    */
    std::string s_Local_l = call<std::string>(m_dumps,mlist);  
    
                                                        
    
    PyObject* ps_Local_l = PyBytes_FromStringAndSize(s_Local_l.c_str(), s_Local_l.size());
    
    
    object LOCAL_l = call<boost::python::object>(m_loads,&ps_Local_l);
     
    auto stop = std::chrono::high_resolution_clock::now();
    auto elapsed = std::chrono::duration<double>(stop - start).count();
    
    std::cout << elapsed << " seconds." << std::endl;

   
  
    return 0;
  
}
