################################
#### agora general section
################################

# check the minimum version
cmake_minimum_required( VERSION 2.8 )

# the project name
project( agora )

# The version number.
set( PROJECT_VERSION_MAJOR 2 )
set( PROJECT_VERSION_MINOR 9 )










################################
#### Option section
################################

# obtain the kind of lib
option( LIB_STATIC "Build static library" ON )










################################
#### Dependencies check
################################

# Check for MQTT library
list( APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake" )
find_package( MQTT )










################################
#### Compile flags
################################

# force the Release build if not already setted
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif(NOT CMAKE_BUILD_TYPE)

# setting common c++ flags
set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x" )

# setting debug flags
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -Wall -g -O0 -fdiagnostics-color=always")

# setting release with debug info flags
set(CMAKE_CXX_FLAGS_RELWITHDEBINFO "${CMAKE_CXX_FLAGS_RELWITHDEBINFO} -march=native -g3 -O2")

# setting release flags
set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -march=native -Ofast -funroll-loops -fprefetch-loop-arrays")










################################
#### Build section
################################

# building the framework
add_subdirectory( framework )
