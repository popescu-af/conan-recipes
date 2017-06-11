project(zbar_test CXX)
cmake_minimum_required(VERSION 3.5)

set(CMAKE_CXX_STANDARD 11)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(${PROJECT_NAME} ${PROJECT_NAME}.cpp)

target_compile_definitions(${PROJECT_NAME}
    PRIVATE QR_CODE_FILE=${CMAKE_SOURCE_DIR}/test.jpg
)
target_link_libraries(${PROJECT_NAME} ${CONAN_LIBS} jpeg z)
