#include "tools.h"
#include "pyth_object.h"
#include "pyconfig.h"

boost::mutex mutex;

void seq_function(int list_length){
    Py_Initialize();
    object main_module = import("__main__");
    object main_namespace = main_module.attr("__dict__");
    list mlist;
   
    for (int i = 0; i < list_length; ++i)
    {
        mlist.append(i);
    }
    
    object f = initialize_function();

    boost::chrono::high_resolution_clock::time_point start = boost::chrono::high_resolution_clock::now();
  

    
    int el;

    for(int j = 0; j < 10000; ++j)
        for (int i = 0; i < list_length; ++i)
        {
            el  = extract<int>(mlist[i]);
            mlist[i] = call<int>(f.ptr(),el);
        }               
    boost::chrono::high_resolution_clock::time_point end = boost::chrono::high_resolution_clock::now();
    std::cout << "List length " << list_length  << " time " << (end - start).count() * ((double) boost::chrono::high_resolution_clock::period::num / boost::chrono::high_resolution_clock::period::den) << std::endl;
  }


void partial_change(int start_it, int chunk_size,list l)
{
    
    
    PyGILState_STATE gstate;
    gstate = PyGILState_Ensure();    
    object f = initialize_function();
 
    PyGILState_Release(gstate);
    int el;
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
    

void threads_function(int threads_to_use,int list_length){
  
  Py_Initialize();
  PyEval_InitThreads();
  
  object main_module = import("__main__");
  object main_namespace = main_module.attr("__dict__");
  list mlist;
  
  for (int i = 0; i < list_length; ++i)
  {
    mlist.append(i);
  }
  
  std::vector<boost::thread *> t;
  int chunk_per_thread = list_length / threads_to_use;
  boost::chrono::high_resolution_clock::time_point start = boost::chrono::high_resolution_clock::now();
  
  Py_BEGIN_ALLOW_THREADS
  for (int Start_it = 0; Start_it < list_length; Start_it += chunk_per_thread)
  {
    int chunk_size = chunk_per_thread;
    t.push_back(new boost::thread(partial_change,Start_it, chunk_size, mlist)); 
  }
  
  for (int i = 0; i < threads_to_use; i++){
      t[i]->join();
      
  }
  for (int i = 0; i < threads_to_use; i++){
      delete t[i];
  }
  Py_END_ALLOW_THREADS
  
  boost::chrono::high_resolution_clock::time_point end = boost::chrono::high_resolution_clock::now();
  std::cout << "List length " << list_length  << " nr of threads " << threads_to_use << " time " << (end - start).count() * ((double) boost::chrono::high_resolution_clock::period::num / boost::chrono::high_resolution_clock::period::den) << std::endl;
  }

struct initialize
{
    initialize()
    {
        Py_InitializeEx(1);
        PyEval_InitThreads();
    }

    ~initialize()
    {
        Py_Finalize();
    }
};

// allow other threads to run
class enable_threads_scope
{
public:
    enable_threads_scope()
    {
        _state = PyEval_SaveThread();
    }

    ~enable_threads_scope()
    {
        PyEval_RestoreThread(_state);
    }

private:

    PyThreadState* _state;
};

// restore the thread state when the object goes out of scope
class restore_tstate_scope
{
public:

    restore_tstate_scope()
    {
        _ts = PyThreadState_Get();
    }

    ~restore_tstate_scope()
    {
        PyThreadState_Swap(_ts);
    }

private:

    PyThreadState* _ts;
};

// swap the current thread state with ts, restore when the object goes out of scope
class swap_tstate_scope
{
public:

    swap_tstate_scope(PyThreadState* ts)
    {
        _ts = PyThreadState_Swap(ts);
    }

    ~swap_tstate_scope()
    {
        PyThreadState_Swap(_ts);
    }

private:

    PyThreadState* _ts;
};

// create new thread state for interpreter interp, make it current, and clean up on destruction
class thread_state
{
public:

    thread_state(PyInterpreterState* interp)
    {
        _ts = PyThreadState_New(interp);
        PyEval_RestoreThread(_ts);
    }

    ~thread_state()
    {
        PyThreadState_Clear(_ts);
        PyThreadState_DeleteCurrent();
    }

    operator PyThreadState*()
    {
        return _ts;
    }

    static PyThreadState* current()
    {
        return PyThreadState_Get();
    }

private:

    PyThreadState* _ts;
};

// represent a sub interpreter
class sub_interpreter
{
public:

    // perform the necessary setup and cleanup for a new thread running using a specific interpreter
    struct thread_scope
    {
        thread_state _state;
        swap_tstate_scope _swap{ _state };

        thread_scope(PyInterpreterState* interp) :
            _state(interp)
        {
        }
    };

    sub_interpreter()
    {
        restore_tstate_scope restore;

        _ts = Py_NewInterpreter();
    }

    ~sub_interpreter()
    {
        if( _ts )
        {
            swap_tstate_scope sts(_ts);

            Py_EndInterpreter(_ts);
        }
    }

    PyInterpreterState* interp()
    {
        return _ts->interp;
    }

    static PyInterpreterState* current()
    {
        return thread_state::current()->interp;
    }

private:

    PyThreadState* _ts;
};


void partial_change_multi(PyInterpreterState* interp,int start_it,int chunk,list *final,list* l,int id)
{
  sub_interpreter::thread_scope scope(interp);

  PyGILState_STATE gstate;
  gstate = PyGILState_Ensure();    
  object f = initialize_function();
  PyGILState_Release(gstate);
  list local_l;
  list Local_l;
  
  int max_l = chunk;
  mutex.lock();
  Local_l += *l;
  mutex.unlock();
  
  int il;
  
  
        //printf("ready for loop %i\n", start_it);
        int el;
        for (int j = 0; j < 10000; ++j)
        {
            
            for (int i = 0; i < max_l; i++)
            {
                el  = extract<int>(Local_l[i]);
                Local_l[i] = call<int>(f.ptr(),el);
            }
            
        }
         
        mutex.lock();
        *final += Local_l;
        mutex.unlock();
        

}

void threads_multi_function(int threads_to_use,int list_length)
{
    initialize init;
    boost::chrono::high_resolution_clock::time_point start = boost::chrono::high_resolution_clock::now();
    sub_interpreter si[threads_to_use];
    
    list mlist;
    
    for (int i = 0; i < list_length; ++i)
    {
        mlist.append(i);
    }
    list global_l;
    
    std::vector<boost::thread *> m_threads;
    list part_list[threads_to_use];
    
    int chunk_size = list_length / threads_to_use;
 
     
    for (int start_val = 0, i = 0; start_val < list_length; start_val += chunk_size, i++)
    {
        int sums_to_do = chunk_size;

        m_threads.push_back(new boost::thread(partial_change_multi, si[i].interp(), start_val, sums_to_do,&part_list[i],&mlist,i));
 
    }
    enable_threads_scope t;

    for (int i = 0; i < threads_to_use; i++){
      m_threads[i]->join();
    }
    
    
    
    for (int i = 0; i < threads_to_use; i++)
    {
        delete m_threads[i];
    }
    
    for (int i = 0; i < threads_to_use; i++){
        global_l +=part_list[i];
    }
    
   boost::chrono::high_resolution_clock::time_point end = boost::chrono::high_resolution_clock::now();
   std::cout << "List length " << list_length  << " nr of threads " << threads_to_use << " time " << (end - start).count() * ((double) boost::chrono::high_resolution_clock::period::num / boost::chrono::high_resolution_clock::period::den) << std::endl;
  
}


void pure_mpi_function(int list_length)
{ 
    int size;
    int rank;
    
    
    int mpiAlreadyInitialized=0;
    MPI_Initialized( &mpiAlreadyInitialized );
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Status  status;
     
    Py_Initialize();
    
    object main_module = import("__main__");
    object main_namespace = main_module.attr("__dict__");
    
    
    object f = initialize_function();
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

        int chunk = list_length/size;
    
        for (int i = 0; i < chunk; ++i)
        {
                il  = extract<int>(mlist[i + chunk*rank]);
                local_l.append(il);
            }
    
        
        
        int el;
        for(int j = 0; j < 10000; j++){
             for (int i = 0; i < chunk; i++)
            {
                el  = extract<int>(local_l[i]);
                local_l[i] = call<int>(f.ptr(),el);
            }
        }
          
        
                         
        std::string s_Local_l = call<std::string>(m_dumps,local_l);  
                                 
        
        MPI_Send(&s_Local_l[0], s_Local_l.size() + 1, MPI_CHAR, 0, rank, MPI_COMM_WORLD);
    }
    
    else{
         list mlist;
         for (int i = 0; i < list_length; ++i)
         {
             mlist.append(i);
         }
        std::string s_mlist = call<std::string>(m_dumps,mlist);
        for(int i = 1; i < size; i++){
            
            MPI_Send(&s_mlist[0],s_mlist.size()+1,MPI_CHAR,i,0,MPI_COMM_WORLD);

        }
         
        int chunk = list_length/size;
        list local_l;
        int il;
        for (int i = 0; i < chunk; ++i)
        {
             il  = extract<int>(mlist[i]);
             local_l.append(il);
        }
        int el;
        for(int j = 0; j < 10000; j++){
            for (int i = 0; i < chunk; i++)
            {
                el  = extract<int>(local_l[i]);
                local_l[i] = call<int>(f.ptr(),el);
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
        
    }
    double end = MPI_Wtime();
    if (rank == 0)
    {
        std::cout << "List length " << list_length << " nr of processes " << size << " time " <<end - start << " seconds" << std::endl;
    }
   
    
}



