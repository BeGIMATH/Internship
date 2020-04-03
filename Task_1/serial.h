#include <boost/python/module.hpp>
#include <boost/python/def.hpp>
#include <boost/python/to_python_converter.hpp>

namespace boost { namespace serial_python {

class custom_string
{
  public:
    custom_string() {}
    custom_string(std::string const &value) : value_(value) {}
    std::string const &value() const { return value_; }
  private:
    std::string value_;
};

struct custom_string_to_python_str
{
  static PyObject* convert(custom_string const &s)
  {
    return boost::python::incref(boost::python::object(s.value()).ptr());
  }
};


}} 
