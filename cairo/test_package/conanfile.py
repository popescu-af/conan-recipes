from conans import ConanFile, CMake
import os

class CairoTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "cairo/1.14.8@popescu-af/testing"
    generators = "cmake"

    def build(self):
        cmake = CMake(self.settings)
        cmake.configure(self, source_dir=self.conanfile_directory, build_dir="./")
        cmake.build(self)

    def imports(self):
        self.copy("*.dll", "bin", "bin")
        self.copy("*.dylib", "bin", "bin")

    def test(self):
        os.chdir("bin")
        self.run(".%scairo_test" % os.sep)
