#include <iostream>
#include <vector>
#include <boost/thread.hpp>
#include <boost/python.hpp>
int threads_to_use = 1;

using namespace boost::python;
class ScopedGILRelease {
public:
  inline ScopedGILRelease() { m_thread_state = PyEval_SaveThread(); }
  inline ~ScopedGILRelease() { PyEval_RestoreThread(m_thread_state); m_thread_state = NULL; }
private:
  PyThreadState* m_thread_state;
};


void do_stuff_in_thread(PyInterpreterState* interp)
{
    // create a new thread state for the the sub interpreter interp
    PyThreadState* ts = PyThreadState_New(interp);

    // make it the current thread state and acquire the GIL
    PyEval_RestoreThread(ts);

    // at this point:
    // 1. You have the GIL
    // 2. You have the right thread state - a new thread state (this thread was not created by python) in the context of interp

    // PYTHON WORK HERE

    // clear ts
    PyThreadState_Clear(ts);

    // delete the current thread state and release the GIL
    PyThreadState_DeleteCurrent();
}


void partial_change(int start_it, int chunk_size,list l)
{ 
    int a;
    for (int i = start_it; i < start_it + chunk_size; i++)
            {
                
                a =1;// extract<int>(l[i]);
            }
  
     
}


int main(int argc, char *argv[]) 
{
  
   
  //PyEval_InitThreads();
  Py_Initialize();
  boost::chrono::high_resolution_clock::time_point start = boost::chrono::high_resolution_clock::now();
  
  
  list mlist;
  for (int i = 0; i < 100; ++i)
  {
    mlist.append(boost::python::object(i));
  }
  
  int lenght = len(mlist);
  ScopedGILRelease release_gil = ScopedGILRelease();
  //Py_BEGIN_ALLOW_THREADS
  //int chunk = len(mlist) / threads_to_use;
  
  std::vector<boost::thread *> v_threads;
  //int chunk_per_thread = len(mlist) / threads_to_use;
  int chunk = 250;
  for (int Start_it = 0; Start_it < 1000 ; Start_it += chunk)
  {
    
    
    
    v_threads.push_back(new boost::thread(partial_change,Start_it, chunk, mlist));
    
  }

  for (int i = 0; i < threads_to_use; i++){
      v_threads[i]->join();
      delete v_threads[i];
  }
  /*
  for(int i = 0; i < 100; i++){
      std::cout << "Element "  << i << " " << extract<int>(mlist[i]) << std::endl;
  }
  */
  //Py_END_ALLOW_THREADS
   
  ///nogil(threads_to_use,mlist);

  boost::chrono::high_resolution_clock::time_point end = boost::chrono::high_resolution_clock::now();
  std::cout << "Time taken: " << (end - start).count() * ((double) boost::chrono::high_resolution_clock::period::num / boost::chrono::high_resolution_clock::period::den) << std::endl;
  
}
