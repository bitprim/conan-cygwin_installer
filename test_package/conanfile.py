from conans import ConanFile
import os


class TestPackage(ConanFile):
    def test(self):
        self.run('%CYGWIN_ROOT%\\bin\\bash -c "awk --help"')
        self.run('%CYGWIN_ROOT%\\bin\\bash -c "/bin/awk --help"')
        self.run('%CYGWIN_ROOT%\\bin\\bash -c "/usr/bin/awk --help"')
        self.run('cat --version')
        self.run('make --version')
        self.run('pkg-config --version')
        self.run('windres --version')
        self.run('gcc --version')
        self.run('g++ --version')
