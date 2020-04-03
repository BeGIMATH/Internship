	
#include <iostream>                   // for std::cout
#include <boost/cstdint.hpp>      // for boost::boost::uint64_t
#include <boost/chrono.hpp>           // for boost::chrono::high_resolution_clock
#include <boost/thread.hpp>           // for boost::thread and boost::mutex
#include <vector>                 // for std::vector
#include <cassert>                    // for assert
#include <boost/python.hpp>
const int threads_to_use = 1;

using namespace boost::python;


void partial_change(int start_it, int chunk_size,list l)
{
    
    Py_Initialize();
    object main_module = import("__main__");
		object main_namespace = main_module.attr("__dict__");
    
    PyGILState_STATE gstate;
    gstate = PyGILState_Ensure();
    
    exec("def f(x):\n"
       "  return x + 1\n"
       "\n", main_namespace);
   
    PyObject* f = object(main_namespace.attr("f")).ptr();
     PyGILState_Release(gstate);
    int el;
    for (int j = 0; j < 10000; ++j)
    {
        
        for (int i = start_it; i < start_it + chunk_size; i++)
        {
            
            gstate = PyGILState_Ensure();
            el  = extract<int>(l[i]);
            l[i] = call<int>(f,el);
            PyGILState_Release(gstate);
        }
        
    }
    
    
    

}

int main()
{
  
  //object main_module = import("__main__");
	//object main_namespace = main_module.attr("__dict__");
  
  list mlist;

  for (int i = 0; i < 10000; ++i)
  {
    mlist.append(i);
  }
  
  std::vector<boost::thread *> t;
  int chunk_per_thread = len(mlist) / threads_to_use;
  boost::chrono::high_resolution_clock::time_point start = boost::chrono::high_resolution_clock::now();
  
  
  for (int Start_it = 0; Start_it < len(mlist); Start_it += chunk_per_thread)
  {
    
    
    int chunk_size = chunk_per_thread;
    t.push_back(new boost::thread(partial_change,Start_it, chunk_size, mlist));
    
  }
  

  for (int i = 0; i < threads_to_use; i++){
      t[i]->join();
      delete t[i];
  }
  
  boost::chrono::high_resolution_clock::time_point end = boost::chrono::high_resolution_clock::now();
  std::cout << "Time taken: " << (end - start).count() * ((double) boost::chrono::high_resolution_clock::period::num / boost::chrono::high_resolution_clock::period::den) << std::endl;
}