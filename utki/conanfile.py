from conans import ConanFile, CMake, tools
import os

class PapkiConan(ConanFile):
    name = "utki"
    version = "1.1.7"
    license = "MIT"
    exports = "*"
    url = "https://github.com/popescu-af/conan-recipes"
    git_url = "https://github.com/igagis/utki.git"
    build_policy = "missing"

    def source(self):
        self.run("git clone %s" % (self.git_url))
        self.run("cd utki && git checkout %s" % self.version)

    def package(self):
        self.copy("*.hpp", dst="include/utki", src="utki/src/utki")

