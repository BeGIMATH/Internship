// Author: Baruch Sterin <baruchs@gmail.com>

#include <Python.h>

#include <string>
#include <vector>
#include <boost/thread.hpp>
#include <boost/python.hpp>
// initialize and clean up python
#include <iostream>
using namespace boost::python;
struct initialize
{
    initialize()
    {
        PyEval_InitThreads();
        Py_Initialize();
        
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

// runs in a new thread
void f(PyInterpreterState* interp, list l,int start_it)
{
  for(int i = start_it; i < start_it + 25; i++)
    {
        l[i] = 0;
    
}
}

int main()
{
    initialize init;

    sub_interpreter s1;
    sub_interpreter s2;
    sub_interpreter s3;
    sub_interpreter s4;

     
    list local_l_1;
    int max_l = 100;
    for(int i = 0; i < max_l; i++){
        local_l_1.append(i);
    }
    list local_l_2;
    for(int i = 0; i < max_l; i++){
        local_l_2.append(i);
    }
    list local_l_3;
    for(int i = 0; i < max_l; i++){
        local_l_3.append(i);
    }
    list local_l_4;
    for(int i = 0; i < max_l; i++){
        local_l_4.append(i);
    }

    boost::thread t1{f, s1.interp(), local_l_1,0};
    boost::thread t2{f, s2.interp(), local_l_2,0};
    boost::thread t3{f, s3.interp(), local_l_3,0};
    boost::thread t4{f, s4.interp(), local_l_4,0};
     
    enable_threads_scope t;

    t1.join();
    t2.join();
    t3.join();
    t4.join();

    std::cout <<"finished " << std::endl;
    return 0;
}
