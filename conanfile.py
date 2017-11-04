#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools
import os
import ctypes

FILE_ATTRIBUTE_SYSTEM = 4


class CygwinInstallerConan(ConanFile):
    name = "cygwin_installer"
    version = "2.9.0"
    settings = {"os": ["Windows"], "arch": ["x86", "x86_64"]}
    url = "https://github.com/bincrafters/conan-cygwin_installer"
    description = "Cygwin is a distribution of popular GNU and other Open Source tools running on Microsoft Windows"
    license = "https://cygwin.com/COPYING"
    install_dir = 'cygwin-install'
    short_paths = True

    def build(self):
        filename = "setup-%s.exe" % self.settings.arch
        url = "https://cygwin.com/%s" % filename
        tools.download(url, filename)

        if not os.path.isdir(self.install_dir):
            os.makedirs(self.install_dir)

        # https://cygwin.com/faq/faq.html#faq.setup.cli
        command = filename
        command += ' --arch %s' % self.settings.arch
        # Disable creation of desktop and start menu shortcuts
        command += ' --no-shortcuts'
        # Do not check for and enforce running as Administrator
        command += ' --no-admin'
        # Unattended setup mode
        command += ' --quiet-mode'
        command += ' --root %s' % os.path.abspath(self.install_dir)
        # TODO : download and parse mirror list, probably also select the best one
        command += ' -s http://cygwin.mirror.constant.com'
        packages = ['pkg-config', 'make', 'libtool', 'binutils', 'gcc-core', 'gcc-g++']
        command += ' --packages %s' % ','.join(packages)
        self.run(command)

        os.unlink(filename)

        # create /tmp dir in order to avoid
        # bash.exe: warning: could not find /tmp, please create!
        tmp_dir = os.path.join(self.install_dir, 'tmp')
        if not os.path.isdir(tmp_dir):
            os.makedirs(tmp_dir)
        tmp_name = os.path.join(tmp_dir, 'dummy')
        with open(tmp_name, 'a'):
            os.utime(tmp_name, None)

    def package(self):
        self.copy(pattern="*", dst=".", src=self.install_dir)

    def fix_symlinks(self):
        for root, _, files in os.walk(self.package_folder):
            for file in files:
                filename = os.path.join(root, file)
                with open(filename, 'rb') as f:
                    try:
                        signature = f.read(10).decode()
                        if signature == '!<symlink>':
                            attributes = ctypes.windll.kernel32.GetFileAttributesW(filename)
                            if not attributes & FILE_ATTRIBUTE_SYSTEM:
                                self.output.warn('setting system attribute on "%s"' % filename)
                                ctypes.windll.kernel32.SetFileAttributesW(filename, attributes | FILE_ATTRIBUTE_SYSTEM)
                    except UnicodeDecodeError:
                        pass

    def package_info(self):
        # workaround for error "cannot execute binary file: Exec format error"
        # symbolic links must have system attribute in order to work properly
        self.fix_symlinks()

        self.env_info.CYGWIN_ROOT = self.package_folder
        self.env_info.path.append(os.path.join(self.package_folder, 'bin'))
