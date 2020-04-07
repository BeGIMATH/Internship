	
#include <iostream>                   // for std::cout
#include <boost/cstdint.hpp>      // for boost::boost::uint64_t
#include <boost/chrono.hpp>           // for boost::chrono::high_resolution_clock
#include <boost/thread.hpp>           // for boost::thread and boost::mutex
#include <vector>                 // for std::vector
#include <cassert>                    // for assert
#include <boost/python.hpp>
#include <fstream>

int threads_to_use = 4;

using namespace boost::python;

const char * code = "def f(x):\n"
             "    return x + 1\n"
             "\n";

object initialize_function(const char * mcode = code) {
    // object main_module = import("__main__");
    dict main_namespace; // = main_module.attr("__dict__");
    exec(mcode, main_namespace);
    return main_namespace["f"];
}

using namespace boost::python;



void partial_change(int start_it, int chunk_size,list l)
{
    printf("launched %i\n", start_it);

    PyGILState_STATE gstate;
    gstate = PyGILState_Ensure();    
    object f = initialize_function();
    printf("end init %i\n", start_it);

    int el;
    if (f != object()){
        PyGILState_Release(gstate);
        printf("ready for loop %i\n", start_it);
        
        gstate = PyGILState_Ensure();
        for (int j = 0; j < 10000; ++j)
        {
            
            for (int i = start_it; i < start_it + chunk_size; i++)
            {
                el  = extract<int>(l[i]);
                l[i] = call<int>(f.ptr(),el);
            }
            
        }
        PyGILState_Release(gstate);
    }
    else 
    {
        PyGILState_Release(gstate);
        printf("abort loop %i\n", start_it);        
    }

}
int main()
{
  /*
  printf("nb param : %i\n", argc);
  if(argc >= 2){
        threads_to_use = atoi(argv[1]);
        printf("Nb of threads : %i\n", threads_to_use);
  }
  */
  /*
  PyEval_InitThreads();
  Py_Initialize();
 
  boost::chrono::high_resolution_clock::time_point start = boost::chrono::high_resolution_clock::now();
 
  list mlist;
  
  for (int i = 0; i < 10000; i++)
  {
    mlist.append(boost::python::object(i));
  }
 
  std::vector<boost::thread *> t;
  
  int list_per_thread = int(len(mlist) / threads_to_use);
  Py_BEGIN_ALLOW_THREADS
  for (int start_it = 0, i = 0; start_it < len(mlist); start_it += list_per_thread, i++)
  {
    
    int work_to_do = list_per_thread;
 
    if (start_it + list_per_thread < len(mlist) && start_it + list_per_thread * 2 > len(mlist))
        work_to_do = len(mlist) - start_it;
 
    t.push_back(new boost::thread(partial_change,mlist,start_it, work_to_do, i));
     
    if (work_to_do != list_per_thread)
        break;
  }
  
  for (int i = 0; i < threads_to_use; i++){
    t[i]->join();
    delete t[i]; 
  }
  Py_END_ALLOW_THREADS
  list global_l;
  /*
  for (std::vector<list *>::iterator it = list_part.begin(); it != list_part.end(); ++it)
      global_l += **it;
  
  std::ofstream myfile;
        myfile.open("example.txt");
        
        
        for(int i=0; i < len(global_l); i++){
            myfile << "Nr " << i << " " << extract<int>(global_l[i]) << std::endl;
        }
        
        myfile.close();
  */
  /*
  boost::chrono::high_resolution_clock::time_point end = boost::chrono::high_resolution_clock::now();
  std::cout << "Time taken: " << (end - start).count() * ((double) boost::chrono::high_resolution_clock::period::num / boost::chrono::high_resolution_clock::period::den) << std::endl;
  */
}