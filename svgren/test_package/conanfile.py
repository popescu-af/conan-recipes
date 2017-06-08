from conans import ConanFile, CMake
import os

class SvgrenTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "svgren/0.4.12@popescu-af/testing", "OpenCV/3.2.0@ohhi/stable"
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
        self.run(".%ssvgren_test" % os.sep)
