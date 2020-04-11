CMAKE_MINIMUM_REQUIRED(VERSION 2.8)

ADD_EXECUTABLE(task1_seq main_seq.cpp)
TARGET_LINK_LIBRARIES(task1_seq  benchmark) 

ADD_EXECUTABLE(task1_thread main_thread.cpp)
TARGET_LINK_LIBRARIES(task1_thread  benchmark) 

ADD_EXECUTABLE(task1_multi main_multi.cpp)
TARGET_LINK_LIBRARIES(task1_multi  benchmark) 

ADD_EXECUTABLE(task1_MPI main_MPI.cpp)
TARGET_LINK_LIBRARIES(task1_MPI benchmark)