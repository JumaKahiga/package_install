import unittest

from script import Packager


class ScriptUnitTests(unittest.TestCase):
    def test_list_packages(self):
        self.assertFalse(Packager().list_packages())

    def test_add_dep_pkg(self):
        self.assertEqual(Packager()._add_dep_pkg(
            dep='NETCARD', package_name='TCPIP'), {'NETCARD': {'TCPIP'}})

    def test_add_dependency(self):
        pkg_deps_map = Packager().add_dependency(
            'TELNET', ['TCPIP', 'NETCARD'])

        self.assertEqual(pkg_deps_map, {'TELNET': {'TCPIP', 'NETCARD'}})

    def test_is_installed(self):
        self.assertFalse(Packager()._is_installed('TCPIP'))

    def test__install_package(self):
        pkg = Packager()
        installed_packages = pkg._install_package('NETCARD')

        self.assertCountEqual(installed_packages, ['NETCARD'])

        installed_packages_2 = pkg._install_package('TCPIP')

        self.assertCountEqual(installed_packages, ['NETCARD', 'TCPIP'])

    def test_install_package(self):
        pkg = Packager()
        pkg.add_dependency('BROWSER', ['TCPIP', 'HTML'])

        installed_packages = pkg.install_package('BROWSER')

        self.assertCountEqual(installed_packages, ['BROWSER', 'HTML', 'TCPIP'])

    # def test__uninstall_package(self):
    #     pkg = Packager()
    #     pkg.add_dependency('BROWSER', ['TCPIP', 'HTML'])
    #     pkg.add_dependency('TELNET', ['TCPIP', 'NETCARD'])
    #     pkg._install_package('BROWSER')
    #     pkg._install_package('TELNET')

    #     installed_packages = pkg._uninstall_package('BROWSER')


    #     self.assertCountEqual(installed_packages, ['TELNET', 'TCPIP', 'NETCARD'])