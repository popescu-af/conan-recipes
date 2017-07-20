from conans import ConanFile, CMake, tools
import os, shutil

cmakelists_txt="""\
project(cairo LANGUAGES C)
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

# @todo: Hardcoded list for now - sources should be chosen based on compile flags/options.
set(CAIRO_SRC
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-analysis-surface.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-arc.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-array.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-atomic.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-base64-stream.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-base85-stream.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-bentley-ottmann.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-bentley-ottmann-rectangular.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-bentley-ottmann-rectilinear.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-botor-scan-converter.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-boxes.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-boxes-intersect.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-cache.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-clip.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-clip-boxes.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-clip-polygon.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-clip-region.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-clip-surface.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-color.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-composite-rectangles.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-compositor.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-contour.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-damage.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-debug.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-default-context.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-device.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-error.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-fallback-compositor.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-fixed.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-font-face.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-font-face-twin.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-font-face-twin-data.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-font-options.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-freelist.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-freed-pool.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-gstate.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-hash.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-hull.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-image-compositor.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-image-info.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-image-source.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-image-surface.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-line.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-lzw.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-matrix.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-mask-compositor.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-mesh-pattern-rasterizer.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-mempool.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-misc.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-mono-scan-converter.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-mutex.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-no-compositor.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-observer.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-output-stream.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-paginated-surface.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-path-bounds.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-path.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-path-fill.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-path-fixed.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-path-in-fill.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-path-stroke.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-path-stroke-boxes.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-path-stroke-polygon.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-path-stroke-traps.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-path-stroke-tristrip.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-pattern.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-pen.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-polygon.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-polygon-intersect.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-polygon-reduce.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-raster-source-pattern.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-recording-surface.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-rectangle.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-rectangular-scan-converter.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-region.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-rtree.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-scaled-font.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-shape-mask-compositor.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-slope.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-spans.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-spans-compositor.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-spline.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-stroke-dash.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-stroke-style.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-surface.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-surface-clipper.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-surface-fallback.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-surface-observer.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-surface-offset.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-surface-snapshot.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-surface-subsurface.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-surface-wrapper.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-time.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-tor-scan-converter.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-tor22-scan-converter.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-clip-tor-scan-converter.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-toy-font-face.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-traps.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-tristrip.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-traps-compositor.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-unicode.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-user-font.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-version.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-wideint.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-cff-subset.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-scaled-font-subsets.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-truetype-subset.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-type1-fallback.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-type1-glyph-names.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-type1-subset.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-type3-glyph-surface.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-pdf-operators.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-pdf-shading.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-deflate-stream.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-xlib-display.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-xlib-core-compositor.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-xlib-fallback-compositor.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-xlib-render-compositor.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-xlib-screen.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-xlib-source.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-xlib-surface.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-xlib-surface-shm.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-xlib-visual.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-xlib-xcb-surface.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-xcb-connection.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-xcb-connection-core.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-xcb-connection-render.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-xcb-connection-shm.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-xcb-screen.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-xcb-shm.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-xcb-surface.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-xcb-surface-core.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-xcb-surface-render.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-xcb-resources.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-png.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-script-surface.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-ft-font.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-ps-surface.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-pdf-surface.c
  ${CMAKE_CURRENT_SOURCE_DIR}/cairo/src/cairo-svg-surface.c
)

if(BUILD_SHARED_LIBS)
  add_library(${PROJECT_NAME} SHARED ${CAIRO_SRC})
  set_target_properties(${PROJECT_NAME} PROPERTIES POSITION_INDEPENDENT_CODE ON)
else()
  add_library(${PROJECT_NAME} STATIC ${CAIRO_SRC})
endif()

target_compile_definitions(${PROJECT_NAME} PRIVATE HAVE_CONFIG_H=1)
target_include_directories(${PROJECT_NAME} SYSTEM
  PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/cairo
  PRIVATE ${CONAN_INCLUDE_DIRS_PIXMAN}/pixman      #Hack for #include <pixman.h> in cairo sources
)
target_link_libraries(${PROJECT_NAME} ${CONAN_LIBS})
"""

class CairoConan(ConanFile):
    name = "cairo"
    description = "2D graphics library with support for multiple output devices"
    version = "1.14.8"
    license = "LGPL 2.1"
    exports = "*"
    url = "https://github.com/popescu-af/conan-recipes"
    settings = "os", "compiler", "build_type", "arch"
    requires = "pixman/0.34.0@popescu-af/testing", "freetype/2.6.3@lasote/stable"
    build_policy = "missing"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"

    def configure(self):
        self.options["freetype"].shared = "True"
        self.options["pixman"].shared = "True"

    def source(self):
        self.run("wget https://www.cairographics.org/releases/cairo-%s.tar.xz -O cairo.tar.xz" % self.version)
        self.run("tar -xvf cairo.tar.xz && mv cairo-%s cairo && cd cairo && ./configure" % self.version)
        # Create CMakeLists.txt file
        with open("CMakeLists.txt", "w") as f:
            f.write(cmakelists_txt)

    def build(self):
        cmake = CMake(self.settings)
        shared = "-DBUILD_SHARED_LIBS=ON" if self.options.shared else ""
        self.run('cmake . %s %s' % (cmake.command_line, shared))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("cairo.h", dst="include/cairo", src="cairo/src")
        self.copy("cairo-deprecated.h", dst="include/cairo", src="cairo/src")
        self.copy("cairo-features.h", dst="include/cairo", src="cairo/src")
        self.copy("cairo-ft.h", dst="include/cairo", src="cairo/src")
        self.copy("cairo-pdf.h", dst="include/cairo", src="cairo/src")
        self.copy("cairo-ps.h", dst="include/cairo", src="cairo/src")
        self.copy("cairo-script.h", dst="include/cairo", src="cairo/src")
        self.copy("cairo-svg.h", dst="include/cairo", src="cairo/src")
        self.copy("cairo-version.h", dst="include/cairo", src="cairo/src")
        self.copy("cairo-xcb.h", dst="include/cairo", src="cairo/src")
        self.copy("cairo-xlib.h", dst="include/cairo", src="cairo/src")
        self.copy("cairo-xlib-xrender.h", dst="include/cairo", src="cairo/src")
        self.copy("*cairo.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["cairo"]
