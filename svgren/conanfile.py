from conans import ConanFile, CMake, tools
import os

cmakelists_txt="""\
project(svgren LANGUAGES CXX)
cmake_minimum_required(VERSION 3.5)

set(CMAKE_CXX_STANDARD 11)

if(CMAKE_COMPILER_IS_GNUCXX)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O2 -w -fPIC")
endif()

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

if(NOT CMAKE_BUILD_TYPE)
  message(STATUS "Setting CMAKE_BUILD_TYPE to Release")
  set(CMAKE_BUILD_TYPE Release)
endif()

set(SVGREN_SRC ${CMAKE_CURRENT_SOURCE_DIR}/svgren/src/svgren/render.cpp)

if(BUILD_SHARED_LIBS)
  add_library(${PROJECT_NAME} SHARED ${SVGREN_SRC})
  set_target_properties(${PROJECT_NAME} PROPERTIES POSITION_INDEPENDENT_CODE ON)
else()
  add_library(${PROJECT_NAME} STATIC ${SVGREN_SRC})
endif()

target_link_libraries(${PROJECT_NAME} ${CONAN_LIBS})
"""

class SvgrenConan(ConanFile):
    name = "svgren"
    description = "SVG renderer library in C++"
    version = "0.4.12"
    license = "MIT"
    exports = "*"
    url = "https://github.com/popescu-af/conan-recipes"
    git_url = "https://github.com/igagis/svgren.git"
    settings = "os", "compiler", "build_type", "arch"
    requires = "svgdom/0.2.32@popescu-af/testing", "cairo/1.14.8@popescu-af/testing"
    build_policy = "missing"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def configure(self):
        self.options["cairo"].shared = True
        self.options["svgdom"].shared = self.options.shared

    def source(self):
        self.run("git clone %s" % (self.git_url))
        self.run("cd svgren && git checkout 0.4.12")
        # Create CMakeLists.txt file
        with open("CMakeLists.txt", "w") as f:
            f.write(cmakelists_txt)

    def build(self):
        cmake = CMake(self.settings)
        shared = "-DBUILD_SHARED_LIBS=ON" if self.options.shared else ""
        self.run('cmake . %s %s' % (cmake.command_line, shared))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.hpp", dst="include/svgren", src="svgren/src/svgren")
        self.copy("*svgren.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["svgren"]
