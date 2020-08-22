CMAKE_MINIMUM_REQUIRED(VERSION 2.8)

SET(PYTHON_LIBRARY "$CONDA_PREFIX/lib")
SET(PYTHON_INCLUDE_DIR "CONDA_PREFIX/include/python3.7m")
FIND_PACKAGE(Python3 COMPONENTS Interpreter Development REQUIRED)


FIND_PACKAGE(Boost COMPONENTS REQUIRED python chrono system thread mpi)
FIND_PACKAGE(PythonLibs)
FIND_PACKAGE(MPI)

INCLUDE_DIRECTORIES(${Boost_INCLUDE_DIRS} ${PYTHON_INCLUDE_DIRS} ${MPI_INCLUDE_PATH})

ADD_LIBRARy(benchmark benchmark.cpp)

TARGET_LINK_LIBRARIES(benchmark  Boost::python  Python3::Python Boost::system Boost::thread Boost::chrono ${MPI_C_LIBRARIES} )

message("Path: " ${CMAKE_BINARY_DIR})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/../run)


ADD_EXECUTABLE(bench_seq bench_seq.cpp)
TARGET_LINK_LIBRARIES(bench_seq  benchmark) 

ADD_EXECUTABLE(bench_thread bench_thread.cpp)
TARGET_LINK_LIBRARIES(bench_thread  benchmark) 

ADD_EXECUTABLE(bench_multi bench_multi.cpp)
TARGET_LINK_LIBRARIES(bench_multi  benchmark) 

ADD_EXECUTABLE(bench_MPI bench_MPI.cpp)
TARGET_LINK_LIBRARIES(bench_MPI benchmark)


FILE(COPY execute.sh DESTINATION ${CMAKE_BINARY_DIR}/../run)
