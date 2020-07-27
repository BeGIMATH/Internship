#include <boost/python.hpp>

using namespace boost::python;

const char *code = "def f(x):\n"
                   "    return x + 1\n"
                   "\n";

object initialize_function(const char *mcode = code)
{
    dict main_namespace;
    exec(mcode, main_namespace);
    return main_namespace["f"];
}

const char *code_opt = "def f_opt(x):\n"
                       "   counter = 0\n"
                       "   while counter < 10000:\n"
                       "      x += 1\n"
                       "      counter += 1\n"
                       "   return x\n"
                       "\n";

object initialize_function_opt(const char *mcode = code_opt)
{
    dict main_namespace;
    exec(mcode, main_namespace);
    return main_namespace["f_opt"];
}

const char *open_file = "file = open(“testfile.txt”,”w”) \n"
                        "\n";

object Open_file(const char *mcode = open_file)
{
    dict main_namespace;
    exec(mcode, main_namespace);
    return main_namespace["file"];
}
