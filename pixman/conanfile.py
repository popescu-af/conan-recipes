from conans import ConanFile, CMake, tools
import os

cmakelists_txt="""\
project(pixman LANGUAGES C)
cmake_minimum_required(VERSION 3.5)

if(CMAKE_COMPILER_IS_GNUCC)
  set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -O2")
endif()

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

if(NOT CMAKE_BUILD_TYPE)
  message(STATUS "Setting CMAKE_BUILD_TYPE to Release")
  set(CMAKE_BUILD_TYPE Release)
endif()

set(SOURCE_FILES
  ${CMAKE_CURRENT_SOURCE_DIR}/pixman/pixman/pixman.c
  ${CMAKE_CURRENT_SOURCE_DIR}/pixman/pixman/pixman-access.c
  ${CMAKE_CURRENT_SOURCE_DIR}/pixman/pixman/pixman-access-accessors.c
  ${CMAKE_CURRENT_SOURCE_DIR}/pixman/pixman/pixman-bits-image.c
  ${CMAKE_CURRENT_SOURCE_DIR}/pixman/pixman/pixman-combine32.c
  ${CMAKE_CURRENT_SOURCE_DIR}/pixman/pixman/pixman-combine-float.c
  ${CMAKE_CURRENT_SOURCE_DIR}/pixman/pixman/pixman-conical-gradient.c
  ${CMAKE_CURRENT_SOURCE_DIR}/pixman/pixman/pixman-filter.c
  ${CMAKE_CURRENT_SOURCE_DIR}/pixman/pixman/pixman-x86.c
  ${CMAKE_CURRENT_SOURCE_DIR}/pixman/pixman/pixman-mips.c
  ${CMAKE_CURRENT_SOURCE_DIR}/pixman/pixman/pixman-arm.c
  ${CMAKE_CURRENT_SOURCE_DIR}/pixman/pixman/pixman-ppc.c
  ${CMAKE_CURRENT_SOURCE_DIR}/pixman/pixman/pixman-edge.c
  ${CMAKE_CURRENT_SOURCE_DIR}/pixman/pixman/pixman-edge-accessors.c
  ${CMAKE_CURRENT_SOURCE_DIR}/pixman/pixman/pixman-fast-path.c
  ${CMAKE_CURRENT_SOURCE_DIR}/pixman/pixman/pixman-glyph.c
  ${CMAKE_CURRENT_SOURCE_DIR}/pixman/pixman/pixman-general.c
  ${CMAKE_CURRENT_SOURCE_DIR}/pixman/pixman/pixman-gradient-walker.c
  ${CMAKE_CURRENT_SOURCE_DIR}/pixman/pixman/pixman-image.c
  ${CMAKE_CURRENT_SOURCE_DIR}/pixman/pixman/pixman-implementation.c
  ${CMAKE_CURRENT_SOURCE_DIR}/pixman/pixman/pixman-linear-gradient.c
  ${CMAKE_CURRENT_SOURCE_DIR}/pixman/pixman/pixman-matrix.c
  ${CMAKE_CURRENT_SOURCE_DIR}/pixman/pixman/pixman-noop.c
  ${CMAKE_CURRENT_SOURCE_DIR}/pixman/pixman/pixman-radial-gradient.c
  ${CMAKE_CURRENT_SOURCE_DIR}/pixman/pixman/pixman-region16.c
  ${CMAKE_CURRENT_SOURCE_DIR}/pixman/pixman/pixman-region32.c
  ${CMAKE_CURRENT_SOURCE_DIR}/pixman/pixman/pixman-solid-fill.c
  ${CMAKE_CURRENT_SOURCE_DIR}/pixman/pixman/pixman-timer.c
  ${CMAKE_CURRENT_SOURCE_DIR}/pixman/pixman/pixman-trap.c
  ${CMAKE_CURRENT_SOURCE_DIR}/pixman/pixman/pixman-utils.c
  ${CMAKE_CURRENT_SOURCE_DIR}/pixman/pixman/pixman-mmx.c
  ${CMAKE_CURRENT_SOURCE_DIR}/pixman/pixman/pixman-sse2.c
  ${CMAKE_CURRENT_SOURCE_DIR}/pixman/pixman/pixman-ssse3.c
)

set_source_files_properties(${CMAKE_CURRENT_SOURCE_DIR}/pixman/pixman/pixman-ssse3.c PROPERTIES COMPILE_FLAGS -mssse3)

if(BUILD_SHARED_LIBS)
  add_library(${PROJECT_NAME} SHARED ${SOURCE_FILES})
  set_target_properties(${PROJECT_NAME} PROPERTIES POSITION_INDEPENDENT_CODE ON)
else()
  add_library(${PROJECT_NAME} STATIC ${SOURCE_FILES})
endif()

target_compile_definitions(${PROJECT_NAME} PRIVATE HAVE_CONFIG_H)
target_include_directories(${PROJECT_NAME} SYSTEM
  PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/pixman
  PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/pixman/pixman
)
target_link_libraries(${PROJECT_NAME} ${CONAN_LIBS})
"""

class PixmanConan(ConanFile):
    name = "pixman"
    version = "0.34.0"
    license = "MIT"
    url = "https://github.com/popescu-af/conan-recipes"
    settings = "os", "compiler", "build_type", "arch"
    build_policy = "missing"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        self.run("wget https://www.cairographics.org/releases/pixman-%s.tar.gz -O pixman.tar.gz" % self.version)
        self.run("tar -xvf pixman.tar.gz && mv pixman-%s pixman && cd pixman && ./configure" % self.version)

        # Create CMakeLists.txt file
        with open("CMakeLists.txt", "w") as f:
            f.write(cmakelists_txt)

    def build(self):
        cmake = CMake(self)
        shared = "-DBUILD_SHARED_LIBS=ON" if self.options.shared else ""
        self.run('cmake . %s %s' % (cmake.command_line, shared))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("pixman.h", dst="include/pixman", src="pixman/pixman")
        tools.replace_in_file("%s/include/pixman/pixman.h" % self.package_folder,
            '''#include <pixman-version.h>''',
            '''#include "pixman-version.h" // CONAN: change include type''')

        self.copy("pixman-version.h", dst="include/pixman", src="pixman/pixman")
        self.copy("*pixman.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["pixman"]
