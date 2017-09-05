from conans import ConanFile, CMake, tools
import os

cmakelists_txt="""\
project(zbar LANGUAGES C)
cmake_minimum_required(VERSION 3.5)

if(CMAKE_COMPILER_IS_GNUCC)
  set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -O2 -w")
endif()

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

if(NOT CMAKE_BUILD_TYPE)
  message(STATUS "Setting CMAKE_BUILD_TYPE to Release")
  set(CMAKE_BUILD_TYPE Release)
endif()

set(SOURCE_FILES
  ${CMAKE_CURRENT_SOURCE_DIR}/zbar/zbar/config.c
  ${CMAKE_CURRENT_SOURCE_DIR}/zbar/zbar/error.c
  ${CMAKE_CURRENT_SOURCE_DIR}/zbar/zbar/symbol.c
  ${CMAKE_CURRENT_SOURCE_DIR}/zbar/zbar/image.c
  ${CMAKE_CURRENT_SOURCE_DIR}/zbar/zbar/convert.c
  ${CMAKE_CURRENT_SOURCE_DIR}/zbar/zbar/processor.c
  ${CMAKE_CURRENT_SOURCE_DIR}/zbar/zbar/processor/lock.c
  ${CMAKE_CURRENT_SOURCE_DIR}/zbar/zbar/refcnt.c
  ${CMAKE_CURRENT_SOURCE_DIR}/zbar/zbar/window.c
  ${CMAKE_CURRENT_SOURCE_DIR}/zbar/zbar/video.c
  ${CMAKE_CURRENT_SOURCE_DIR}/zbar/zbar/img_scanner.c
  ${CMAKE_CURRENT_SOURCE_DIR}/zbar/zbar/scanner.c
  ${CMAKE_CURRENT_SOURCE_DIR}/zbar/zbar/decoder.c
  ${CMAKE_CURRENT_SOURCE_DIR}/zbar/zbar/jpeg.c
  ${CMAKE_CURRENT_SOURCE_DIR}/zbar/zbar/decoder/ean.c
  ${CMAKE_CURRENT_SOURCE_DIR}/zbar/zbar/decoder/code128.c
  ${CMAKE_CURRENT_SOURCE_DIR}/zbar/zbar/decoder/code39.c
  ${CMAKE_CURRENT_SOURCE_DIR}/zbar/zbar/decoder/i25.c
  ${CMAKE_CURRENT_SOURCE_DIR}/zbar/zbar/decoder/qr_finder.c
  ${CMAKE_CURRENT_SOURCE_DIR}/zbar/zbar/qrcode/qrdec.c
  ${CMAKE_CURRENT_SOURCE_DIR}/zbar/zbar/qrcode/qrdectxt.c
  ${CMAKE_CURRENT_SOURCE_DIR}/zbar/zbar/qrcode/rs.c
  ${CMAKE_CURRENT_SOURCE_DIR}/zbar/zbar/qrcode/isaac.c
  ${CMAKE_CURRENT_SOURCE_DIR}/zbar/zbar/qrcode/bch15_5.c
  ${CMAKE_CURRENT_SOURCE_DIR}/zbar/zbar/qrcode/binarize.c
  ${CMAKE_CURRENT_SOURCE_DIR}/zbar/zbar/qrcode/util.c
  ${CMAKE_CURRENT_SOURCE_DIR}/zbar/zbar/processor/posix.c
  ${CMAKE_CURRENT_SOURCE_DIR}/zbar/zbar/video/null.c
  ${CMAKE_CURRENT_SOURCE_DIR}/zbar/zbar/processor/null.c
  ${CMAKE_CURRENT_SOURCE_DIR}/zbar/zbar/window/null.c
)

if(BUILD_SHARED_LIBS)
  add_library(${PROJECT_NAME} SHARED ${SOURCE_FILES})
  set_target_properties(${PROJECT_NAME} PROPERTIES POSITION_INDEPENDENT_CODE ON)
else()
  add_library(${PROJECT_NAME} STATIC ${SOURCE_FILES})
endif()

target_include_directories(${PROJECT_NAME} SYSTEM
  PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/zbar/include
  PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/zbar/zbar
)
target_link_libraries(${PROJECT_NAME} ${CONAN_LIBS})
"""

class ZbarConan(ConanFile):
    name = "zbar"
    description = "Software suite for reading bar codes from various sources"
    version = "0.10.0"
    short_version = "0.10"
    license = "LGPL 2.1"
    exports = "*"
    url = "https://github.com/popescu-af/conan-recipes"
    settings = "os", "compiler", "build_type", "arch"
    requires = "libjpeg-turbo/1.5.1@lasote/stable", "libiconv/1.14@lasote/stable"
    build_policy = "missing"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"
    configure_options = "--disable-video --without-imagemagick --without-python --without-qt --without-x --without-gtk"

    def source(self):
        self.run("wget https://downloads.sourceforge.net/project/zbar/zbar/%s/zbar-%s.tar.bz2 -O zbar.tar.bz2" % (self.short_version, self.short_version))
        self.run("tar -xvf zbar.tar.bz2 && mv zbar-%s zbar && cd zbar && ./configure %s" % (self.short_version, self.configure_options))
        # Create CMakeLists.txt file
        with open("CMakeLists.txt", "w") as f:
            f.write(cmakelists_txt)

    def build(self):
        cmake = CMake(self.settings)
        shared = "-DBUILD_SHARED_LIBS=ON" if self.options.shared else ""
        self.run('cmake . %s %s' % (cmake.command_line, shared))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("zbar.h", dst="include/zbar", src="zbar/include")
        self.copy("[A-Z]*.h", dst="include/zbar", src="zbar/include/zbar")
        self.copy("*zbar.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["zbar"]
