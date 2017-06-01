from conans import ConanFile, CMake, tools
import os

cmakelists_txt="""\
project(svgdom LANGUAGES CXX)
cmake_minimum_required(VERSION 3.5)

set(CMAKE_CXX_STANDARD 11)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

if(NOT CMAKE_BUILD_TYPE)
  message(STATUS "Setting CMAKE_BUILD_TYPE to Release")
  set(CMAKE_BUILD_TYPE Release)
endif()

set(SVGDOM_SRC ${CMAKE_CURRENT_SOURCE_DIR}/svgdom/src/svgdom/dom.cpp)

if(BUILD_SHARED_LIBS)
  add_library(${PROJECT_NAME} SHARED ${SVGDOM_SRC})
  set_target_properties(${PROJECT_NAME} PROPERTIES POSITION_INDEPENDENT_CODE ON)
else()
  add_library(${PROJECT_NAME} STATIC ${SVGDOM_SRC})
endif()

target_link_libraries(${PROJECT_NAME} ${CONAN_LIBS})
"""

class SvgdomConan(ConanFile):
    name = "svgdom"
    version = "0.2.32"
    license = "MIT"
    url = "<Package recipe repository url here, for issues about the package>"
    settings = "os", "compiler", "build_type", "arch"
    requires = "pugixml/1.7@a_teammate/testing"
    build_policy = "missing"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def configure(self):
        # pugixml/1.7@a_teammate/testing conanfile.py does not handle shared builds now,
        # but this line will be useful when this is fixed.
        self.options["pugixml"].shared = self.options.shared

    def source(self):
        self.run("git clone https://github.com/igagis/svgdom.git")
        self.run("cd svgdom && git checkout 0.2.32")
        # Create CMakeLists.txt file
        with open("CMakeLists.txt", "w") as f:
            f.write(cmakelists_txt)

    def build(self):
        cmake = CMake(self.settings)
        shared = "-DBUILD_SHARED_LIBS=ON" if self.options.shared else ""
        self.run('cmake . %s %s' % (cmake.command_line, shared))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.hpp", dst="include", src="svgdom/src/svgdom")
        self.copy("*svgdom.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["svgdom"]
