cmake_minimum_required(VERSION 3.10)

project(dm_Linux_Drive)

set(CMAKE_CXX_STANDARD 14)

# include
include_directories(${PROJECT_SOURCE_DIR}/include)

# library path
link_directories(${PROJECT_SOURCE_DIR}/lib)

add_executable(test_damiao src/test_damiao.cpp)
add_executable(test_can src/eef_can_demo.cpp)

target_link_libraries(test_damiao
    MarvinSDK
)

target_link_libraries(test_can
    MarvinSDK
)
