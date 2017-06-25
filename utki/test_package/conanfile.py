from conans import ConanFile, CMake
import os

channel = os.getenv("CONAN_CHANNEL", "testing")
username = os.getenv("CONAN_USERNAME", "popescu-af")

class UtkiTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "utki/1.1.7@%s/%s" % (username, channel)
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_dir=self.conanfile_directory, build_dir="./")
        cmake.build()

    def imports(self):
        self.copy("*.dll", "bin", "bin")
        self.copy("*.dylib", "bin", "bin")

    def test(self):
        os.chdir("bin")
        self.run(".%sutki_test" % os.sep)
