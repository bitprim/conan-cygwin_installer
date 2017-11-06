#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools
import os


class TestPackage(ConanFile):
    def test(self):
        new_path = os.path.join(self.deps_env_info['cygwin_installer'].CYGWIN_BIN)
        with tools.environment_append({'PATH': new_path}):
            self.run(r'%CYGWIN_BIN%\bash -c "awk --help"')
            self.run(r'%CYGWIN_BIN%\bash -c "/bin/awk --help"')
            self.run(r'%CYGWIN_BIN%\bash -c "/usr/bin/awk --help"')
            self.run(r'cat --version')
            self.run(r'make --version')
            self.run(r'pkg-config --version')
            self.run(r'windres --version')
            self.run(r'gcc --version')
            self.run(r'g++ --version')
