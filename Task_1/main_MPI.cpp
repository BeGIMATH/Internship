
#include <iostream>
#include <mpi.h>
#include <fstream>
#include <string>
#include <boost/python.hpp>
using namespace boost::python;

int main()
{
   
    
    int size,rank;
    MPI_Init(NULL, NULL);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Status  status;

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
   
    double start = MPI_Wtime();
    

    
    list global_l;
    
    if(rank != 0){  
        list local_l;
        int il;
    
        MPI_Probe(0, 0,MPI_COMM_WORLD, &status);
        int count;
        MPI_Get_count(&status,MPI_CHAR,&count);
        char buf [count];
        MPI_Recv(&buf,count,MPI_CHAR,0,0,MPI_COMM_WORLD,&status);
        
        
        PyObject* ps_Local_l = PyBytes_FromStringAndSize(buf, count);
        
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
                                 
        
        MPI_Send(&s_Local_l[0], s_Local_l.size() + 1, MPI_CHAR, 0, rank, MPI_COMM_WORLD);
    }
    
    else{
         list mlist;
         for (int i = 0; i < 10000; ++i)
         {
             mlist.append(i);
         }
        std::string s_mlist = call<std::string>(m_dumps,mlist);
        for(int i = 1; i < size; i++){
            
            MPI_Send(&s_mlist[0],s_mlist.size()+1,MPI_CHAR,i,0,MPI_COMM_WORLD);

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

            
            MPI_Status status;
            MPI_Probe(i, i,MPI_COMM_WORLD, &status);
            int count;
            MPI_Get_count(&status,MPI_CHAR,&count);
            char buf [count];
            MPI_Recv(&buf,count,MPI_CHAR,i,i,MPI_COMM_WORLD,&status);
            

            PyObject* ps_Local_l = PyBytes_FromStringAndSize(buf, count);
           
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
    
    double end = MPI_Wtime();
    
    if (rank == 0)
    {
        std::cout << "The process took " << end - start << " seconds to run." << std::endl;
    }
    MPI_Finalize();
    return 0;
}

