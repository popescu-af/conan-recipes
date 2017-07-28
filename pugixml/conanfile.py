from conans import ConanFile, CMake
import os
import sys

class PugixmlConan(ConanFile):
    name = "pugixml"
    description = "light-weight C++ XML processing library"
    version = "1.8.1"
    url = "https://github.com/popescu-af/conan-recipes"
    git_url = "https://github.com/zeux/pugixml.git"
    license = "MIT"
    exports = "*"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        self.run("git clone %s" % (self.git_url))
        self.run("cd pugixml && git checkout v%s" % self.version)

    def build(self):
        os.chdir("pugixml")
        cmake = CMake(self.settings)
        shared = "-DBUILD_SHARED_LIBS=ON" if self.options.shared else ""
        cxxflags = "-DCMAKE_CXX_FLAGS=\"-fPIC\""
        self.run("cmake . %s %s %s" % (cmake.command_line, shared, cxxflags))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.hpp", dst="include", src="pugixml/src")
        self.copy("*pugixml.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
      
    def package_info(self):
        self.cpp_info.libs = ["pugixml"]

