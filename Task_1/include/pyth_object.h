#include <boost/python.hpp>

using namespace boost::python;

const char * code = "def f(x):\n"
             "    return x + 1\n"
             "\n";

object initialize_function(const char * mcode = code) {
    dict main_namespace; 
    exec(mcode, main_namespace);
    return main_namespace["f"];
}

