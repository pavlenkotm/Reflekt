cmake_minimum_required(VERSION 3.15)
project(Keccak256Utils VERSION 1.0)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Optimization flags
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3 -march=native")
endif()

# Main executable
add_executable(keccak256 keccak256.cpp)

# Install
install(TARGETS keccak256 DESTINATION bin)
