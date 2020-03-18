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

    for (int i = 0; i < 10000; ++i)
    {
        mlist.append(i);
    }

    auto start = std::chrono::high_resolution_clock::now();
    for (int j = 0; j < 10000; j++)
    {
        for (int i = 0; i < 10000; ++i)
        {
            mlist[i] = mlist[i] + 1;
        }
    }
    auto stop = std::chrono::high_resolution_clock::now();
    auto elapsed = std::chrono::duration<double>(stop - start).count();

    std::cout << elapsed << " seconds." << std::endl;

    return 0;
}
