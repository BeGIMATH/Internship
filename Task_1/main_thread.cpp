	
#define BOOST_THREAD_PROVIDES_FUTURE
#include <boost/thread.hpp>
#include <boost/thread/future.hpp>
#include <utility>
#include <iostream>
#include <boost/chrono.hpp>           // for boost::chrono::high_resolution_clock
#include <boost/thread.hpp>           // for boost::thread and boost::mutex
#include <vector>                 // for std::vector
#include <cassert>                    // for assert
#include <boost/python.hpp>
#include <Python.h>
#include <fstream>
const int threads_to_use = 4;
std::vector<boost::python::list *> list_part;
using namespace boost::python;

boost::mutex   _pyMutex; 


void partial_change(list LOCAL_L,list l, list *final, int start_it, int chunk_size,int id)
{
    
    
    PyGILState_STATE  gstate;
   
    gstate = PyGILState_Ensure(); 
    
    object main_module = import("__main__");
	  object main_namespace = main_module.attr("__dict__");
     
    PyGILState_Release(gstate);
    
    //PyGILState_STATE  gstate;
    gstate = PyGILState_Ensure(); 
    exec("def f(x):\n"
       "  return x + 1\n"
       "\n", main_namespace);
         int il;
    
    PyObject* f = object(main_module.attr("f")).ptr();
        
        
    
    PyGILState_Release(gstate);
    gstate = PyGILState_Ensure();
    for (int j = 0; j < 100 ; ++j)
        {
          
          il  = extract<int>(l[j + chunk_size*id]);
          LOCAL_L.append(j);
          
        }
    PyGILState_Release(gstate);
    
    /*
    gstate = PyGILState_Ensure(); 

    list local_l;   
    for (int j = 0; j < 100 ; ++j)
    {
      il  = extract<int>(l[j + chunk_size*id]);
      local_l.append(j);
    }
    PyGILState_Release(gstate);
    
    exec("def f(x):\n"
       "  return x + 1\n"
       "\n", main_namespace);
    PyObject* f = object(main_module.attr("f")).ptr();
   
   PyGILState_Release(gstate);
    
    int el;

    //_pyMutex.lock();

    for (int j = 0; j < 100; ++j)
        {
           for (int i = 0; i < len(local_l); i++)
            {
                
              
                gstate = PyGILState_Ensure(); 
              
                el  = extract<int>(local_l[i]);
                local_l[i] = call<int>(f,el);
                PyGILState_Release(gstate);

            }
        }
        
        gstate = PyGILState_Ensure(); 
        
        *final += local_l;  
        PyGILState_Release(gstate);*/
           
}

int main()
{
  PyEval_InitThreads();
  Py_Initialize();
  PyThreadState* m_thread_state;
  boost::chrono::high_resolution_clock::time_point start = boost::chrono::high_resolution_clock::now();
  list_part.clear();
  list mlist;
  list local_l;
  for (int i = 0; i < 100; i++)
  {
    mlist.append(i);
  }
  for (int i = 0; i < threads_to_use; i++){
    list_part.push_back(new list);
  }
  std::vector<boost::thread *> t;
  
  int list_per_thread = int(len(mlist) / threads_to_use);
  m_thread_state = PyEval_SaveThread();
  for (int start_it = 0, i = 0; start_it < len(mlist); start_it += list_per_thread, i++)
  {
    // Lump extra bits onto last thread if work items is not equally divisible by number of threads
    int work_to_do = list_per_thread;
 
    if (start_it + list_per_thread < len(mlist) && start_it + list_per_thread * 2 > len(mlist))
        work_to_do = len(mlist) - start_it;
 
    t.push_back(new boost::thread(partial_change,local_l,mlist, list_part[i], start_it, work_to_do, i));
     
    if (work_to_do != list_per_thread)
        break;
  }
  
  for (int i = 0; i < threads_to_use; i++){
    t[i]->join();
    delete t[i]; 
  }
  PyEval_RestoreThread(m_thread_state);
  list global_l;
  for (std::vector<list *>::iterator it = list_part.begin(); it != list_part.end(); ++it)
      global_l += **it;
  /*
  std::ofstream myfile;
        myfile.open("example.txt");
        
        
        for(int i=0; i < len(global_l); i++){
            myfile << "Nr " << i << " " << extract<int>(global_l[i]) << std::endl;
        }
        
        myfile.close();
  */
  boost::chrono::high_resolution_clock::time_point end = boost::chrono::high_resolution_clock::now();
  std::cout << "Time taken: " << (end - start).count() * ((double) boost::chrono::high_resolution_clock::period::num / boost::chrono::high_resolution_clock::period::den) << std::endl;
}