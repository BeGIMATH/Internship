#include <iostream>
#include <boost/python.hpp>
#include <chrono>

using namespace boost::python;

int main(int argc, char *argv[])
{
    Py_Initialize();
    object main_module = import("__main__");
    object main_namespace = main_module.attr("__dict__");
    list mlist;
    list mlist1;
    list mlist2;

    
    for (int i = 0; i < 10000; ++i)
    {
        mlist.append(i);
    }
    std::cout << len(mlist) << std::endl;
    for (int i = 0; i < 10000; ++i)
    {
        mlist1.append(i);
    }
    
    
    exec("def f(x):\n"
         "  return x + 1\n"
         "\n", main_namespace);
    
    PyObject* f = object(main_module.attr("f")).ptr();
    
    
    
    int el;
    auto start = std::chrono::high_resolution_clock::now();
    for (int j = 0; j < 10000; j++)
    {
        for (int i = 0; i < 10000; ++i)
        {

            el  = extract<int>(mlist[i]);
            mlist[i] = call<int>(f,el);
            

        }
    }

    std::cout << len(mlist1) << std::endl;
    auto stop = std::chrono::high_resolution_clock::now();
    auto elapsed = std::chrono::duration<double>(stop - start).count();
          
    std::cout << elapsed << " seconds." << std::endl;

   
  
    return 0;
  
}
