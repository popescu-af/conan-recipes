project(zbar_test CXX)
cmake_minimum_required(VERSION 3.5)

set(CMAKE_CXX_STANDARD 11)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(${PROJECT_NAME} ${PROJECT_NAME}.cpp)

target_compile_definitions(${PROJECT_NAME}
    PRIVATE QR_CODE_FILE=${CMAKE_SOURCE_DIR}/test.png
)
target_link_libraries(${PROJECT_NAME} opencv_imgcodecs opencv_imgproc opencv_core libpng libjasper libtiff libwebp IlmImf ippicv zbar jpeg z dl pthread)
