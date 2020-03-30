


#include <boost/mpi/python/config.hpp>

#include <boost/python/object.hpp>
#include <boost/python/str.hpp>
#include <boost/python/extract.hpp>

#include <map>

#include <boost/function/function3.hpp>

#include <boost/mpl/bool.hpp>
#include <boost/mpl/if.hpp>

#include <boost/serialization/split_free.hpp>
#include <boost/serialization/array.hpp>
#include <boost/serialization/array_wrapper.hpp>
#include <boost/smart_ptr/scoped_array.hpp>

#include <boost/assert.hpp>

#include <boost/type_traits/is_fundamental.hpp>

#define BOOST_MPI_PYTHON_FORWARD_ONLY
#include <boost/mpi/python.hpp>


namespace boost { namespace python {


class BOOST_MPI_PYTHON_DECL pickle {
  struct data_t;

public:
  static str dumps(object obj, int protocol = -1);
  static object loads(str s);
  
private:
  static void initialize_data();

  static data_t* data;
};

struct pickle::data_t {
  object module;
  object dumps;
  object loads;
};


pickle::data_t* pickle::data;

str pickle::dumps(object obj, int protocol)
{
  if (!data) initialize_data();
  return extract<str>((data->dumps)(obj, protocol));
}

object pickle::loads(str s)
{
  if (!data) initialize_data();
  return ((data->loads)(s));
}

void pickle::initialize_data()
{
  data = new data_t;
  data->module = object(handle<>(PyImport_ImportModule("pickle")));
  data->dumps = data->module.attr("dumps");
  data->loads = data->module.attr("loads");
}

} } 

