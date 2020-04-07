	
#include <iostream>                   // for std::cout
#include <boost/cstdint.hpp>      // for boost::boost::uint64_t
#include <boost/chrono.hpp>           // for boost::chrono::high_resolution_clock

#include <vector>                 // for std::vector
#include <cassert>                    // for assert
#include <boost/python.hpp>
#include <omp.h>
#include <fstream>
const int threads_to_use = 4;

using namespace boost::python;
omp_lock_t writelock;
list partial_change()
{
    int el;
        object main_module = import("__main__");
	    object main_namespace = main_module.attr("__dict__");
         exec("def f(x):\n"
       "  return x + 1\n"
       "\n", main_namespace);
        PyObject* f = object(main_module.attr("f")).ptr();
       
    
   
       list local_l ;
         for (int j = 0; j < 2500; ++j)
         {
            local_l.append(j);
         }
         for (int j = 0; j < 10000; ++j)
        {
           for (int i = 0; i < len(local_l); i++)
            {
                el  = extract<int>(local_l[i]);
                local_l[i] = call<int>(f,el);
            }
     } 
     return local_l;
        
        
}

int main()
{
  Py_Initialize();
 
  list mlist;
  list local_l;
  list global_l;
  double seconds = omp_get_wtime ( );
  
  int id;
  #pragma omp parallel
  {
  
      
    
  omp_set_num_threads(threads_to_use);
  id = omp_get_thread_num();
  
   #pragma omp critical
   {
      
      local_l = partial_change();
      global_l += local_l;
   }
  
  }
  
      
  

  /*
  std::ofstream myfile;
  myfile.open("example.txt");
  if(myfile.is_open())
  {
    for(int i=0; i < len(mlist); i++){
            myfile << "Nr " << i << " " << extract<int>(mlist[i]) << std::endl;
    }
        
    myfile.close();
}
else std::cout << "Unable to open file";
std::cout << len(mlist) << std::endl;
*/
seconds = omp_get_wtime ( ) - seconds;
std::cout << "Time taken: " << seconds << std::endl;

}