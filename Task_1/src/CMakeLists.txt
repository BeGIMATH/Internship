CMAKE_MINIMUM_REQUIRED(VERSION 2.8)

SET(PYTHON_LIBRARY "$CONDA_PREFIX/lib")
SET(PYTHON_INCLUDE_DIR "CONDA_PREFIX/include/python3.7m")
FIND_PACKAGE(Python3 COMPONENTS Interpreter Development REQUIRED)

SET(Boost_USE_STATIC_LIBS OFF)
SET(Boost_USE_MULTITHREADED ON)
SET(Boost_USE_STATIC_RUNTIME OFF)

FIND_PACKAGE(Boost COMPONENTS REQUIRED python chrono system thread mpi)
FIND_PACKAGE(PythonLibs)
FIND_PACKAGE(MPI)

INCLUDE_DIRECTORIES(${Boost_INCLUDE_DIRS} ${PYTHON_INCLUDE_DIRS} ${MPI_INCLUDE_PATH})

ADD_LIBRARy(benchmark benchmark.cpp)

TARGET_LINK_LIBRARIES(benchmark  Boost::python  Python3::Python Boost::system Boost::thread Boost::chrono ${MPI_C_LIBRARIES} )

message("Path: " ${CMAKE_BINARY_DIR})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/../run)


ADD_EXECUTABLE(task1_seq main_seq.cpp)
TARGET_LINK_LIBRARIES(task1_seq  benchmark) 

ADD_EXECUTABLE(task1_thread main_thread.cpp)
TARGET_LINK_LIBRARIES(task1_thread  benchmark) 

ADD_EXECUTABLE(task1_multi main_multi.cpp)
TARGET_LINK_LIBRARIES(task1_multi  benchmark) 

ADD_EXECUTABLE(task1_MPI main_MPI.cpp)
TARGET_LINK_LIBRARIES(task1_MPI benchmark)

ADD_EXECUTABLE(task1_seq_opt main_seq_opt.cpp)
TARGET_LINK_LIBRARIES(task1_seq_opt  benchmark) 

ADD_EXECUTABLE(task1_thread_opt main_thread_opt.cpp)
TARGET_LINK_LIBRARIES(task1_thread_opt  benchmark) 

ADD_EXECUTABLE(task1_multi_opt main_multi_opt.cpp)
TARGET_LINK_LIBRARIES(task1_multi_opt  benchmark) 

ADD_EXECUTABLE(task1_MPI_opt main_MPI_opt.cpp)
TARGET_LINK_LIBRARIES(task1_MPI_opt benchmark)


FILE(COPY execute.sh DESTINATION ${CMAKE_BINARY_DIR}/../run)