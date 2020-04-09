cmake_minimum_required(VERSION 2.8)

project(task1)
#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")



set(PYTHON_LIBRARY "$CONDA_PREFIX/lib")
set(PYTHON_INCLUDE_DIR "CONDA_PREFIX/include/python3.7m")
FIND_PACKAGE(Python3 COMPONENTS Interpreter Development REQUIRED)

set(Boost_USE_STATIC_LIBS OFF)
set(Boost_USE_MULTITHREADED ON)
set(Boost_USE_STATIC_RUNTIME OFF)

FIND_PACKAGE(Boost COMPONENTS REQUIRED python chrono system thread mpi serialization mpi_python)
FIND_PACKAGE(PythonLibs)
FIND_PACKAGE(MPI)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
INCLUDE_DIRECTORIES(${Boost_INCLUDE_DIRS} ${PYTHON_INCLUDE_DIRS} ${MPI_INCLUDE_PATH})


ADD_EXECUTABLE(task1_seq main_seq.cpp)
TARGET_LINK_LIBRARIES(task1_seq Boost::python Python3::Python Boost::mpi_python) 

ADD_EXECUTABLE(task1_mpi main_mpi.cpp)
TARGET_LINK_LIBRARIES(task1_mpi  Boost::python  Python3::Python Boost::mpi_python Boost::serialization Boost::system)  

ADD_EXECUTABLE(task1_thread main_thread.cpp)
TARGET_LINK_LIBRARIES(task1_thread Boost::chrono Boost::thread Boost::python  Python3::Python) 

ADD_EXECUTABLE(nogil nogil.cpp)
TARGET_LINK_LIBRARIES(nogil Boost::chrono Boost::thread Boost::python  Python3::Python) 

#ADD_EXECUTABLE(task1_mint main_minterp.cpp)
#TARGET_LINK_LIBRARIES(task1_mint Boost::chrono Boost::thread Boost::python  Python3::Python) 

ADD_EXECUTABLE(task1_MPI main_MPI.cpp)
TARGET_LINK_LIBRARIES(task1_MPI  Boost::python  Python3::Python Boost::system ${MPI_C_LIBRARIES})  

