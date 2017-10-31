from conans import ConanFile
import os


class TestPackage(ConanFile):
    def test(self):
        self.run('cat --version')
        self.run('make --version')
        self.run('pkg-config --version')
        self.run('windres --version')
        self.run('gcc --version')
        self.run('g++ --version')
