import os
import itertools
import subprocess


class Packager:
    """
    Contains methods for installing packages
    """

    def __init__(self):
        self.installed_packages = None
        self.pkg_deps_map = None
        self.dep_pkgs_map = None

    def list_packages(self):
        """
        Lists currently installed packages

        Returns
        -------
        self.installed_packages or []: list
            Returns a list of installed packages. 
            Empty if no packages installed

        """

        if not self.installed_packages:
            return []

        return self.installed_packages

    def _add_dep_pkg(self, dep, package_name):
        """
        Creates an inverse hash_map, where each dependency is grouped with its packages

        Parameters
        ----------
        dep : str
            Dependency name
        package_name : str
            Package name

        Returns
        -------
        self.dep_pkgs_map : dict
            A dict containing dependencies and packages using them

        """

        if not self.dep_pkgs_map:
            self.dep_pkgs_map = {}

        if dep not in self.dep_pkgs_map:
            self.dep_pkgs_map[dep] = set()

        self.dep_pkgs_map[dep].add(package_name)

        return self.dep_pkgs_map

    def add_dependency(self, package_name: str, pkg_deps: list):
        """
        Adds dependencies to a package. If the package is not present 
        in the dependencies variable, it is added to the dict

        Parameters
        ----------
        package_name : str
            The primary package
        pkg_deps : list
            A list of dependencies for the primary package

        Returns

        """

        if not pkg_deps:
            return self.pkg_deps_map

        if not self.pkg_deps_map:
            self.pkg_deps_map = {}

        if package_name not in self.pkg_deps_map:
            self.pkg_deps_map[package_name] = set()

        self.pkg_deps_map[package_name].update(pkg_deps)

        for dep in pkg_deps:
            self._add_dep_pkg(dep, package_name)

        return self.pkg_deps_map


    def _is_installed(self, package_name):
        """
        Checks if a package is already installed

        Parameters
        ----------
        package_name ; str
            Package to be check

        Returns
        -------
            : bool
            True if installed, False if not

        """

        if not self.installed_packages:
            return False

        if package_name in self.installed_packages:
            return True

        return False

    def _install_package(self, package_name: str):
        """
        Installs a package

        Paramaters
        ----------
        package_name : str
            Package to be installed

        Returns
        -------
        self.installed_packages or None : list or None
            If the package was successfully installed, or is already installed,
            the return is a list of current packages
            
            if there was an error in installation, None is returned

        """

        if self._is_installed(package_name):
            return self.installed_packages

        # try:
        #     subprocess.run(['apt', 'install', '-y', package_name], check=True)
        # except Exception as e:
        #     subprocess.run(['echo', f'installation of {e} failed with error {e}'])
        #     return

        if not self.installed_packages:
            self.installed_packages = []

        self.installed_packages.append(package_name)

        return self.installed_packages

    def install_package(self, package_name: str):
        """
        Manages package installation process i.e.
        It checks for dependencies and installs them before package

        Paramaters
        ----------
        package_name : str
            Package to be installed

        Returns
        -------
        self.installed_packages or None : list or None
            If the package was successfully installed, or is already installed,
            the return is a list of current packages
            
            if there was an error in installation, None is returned

        """

        if self._is_installed(package_name):
            return self.installed_packages

        if package_name not in self.pkg_deps_map:
            return self._install_package(package_name)

        deps = self.pkg_deps_map[package_name]

        for dep in deps:
            self.install_package(dep)

        self._install_package(package_name)

        return self.installed_packages

    def _uninstall_package(self, package_name: str):
        """
        Uninstalls a package

        Paramaters
        ----------
        package_name : str
            Package to be uninstalled

        Returns
        -------
        self.installed_packages or None : list or None
            If the package was successfully uninstalled, or was not installed,
            the return is a list of current packages
            
            if there was an error in installation, None is returned

        """

        if not self._is_installed(package_name):
            return self.installed_packages

        # try:
        #     subprocess.run(['apt', 'uninstall', '-y', package_name], check=True)
        # except Exception as e:
        #     subprocess.run(['echo', f'installation of {e} failed with error {e}'])
        #     return

        self.installed_packages.remove(package_name)

        return self.installed_packages

    def uninstall_package(self, package_name):
        """
        Manages package uninstallation process i.e.
        It checks for dependencies and uninstalls them before package

        Paramaters
        ----------
        package_name : str
            Package to be uninstalled

        Returns
        -------
        self.installed_packages or None : list or None
            If the package was successfully uninstalled, or was not installed,
            the return is a list of current packages
            
            if there was an error in installation, None is returned

        """ 

        if not self._is_installed(package_name):
            return self.installed_packages

        if package_name not in self.pkg_deps_map:
            return self._uninstall_package(package_name)

        deps = self.pkg_deps_map[package_name]

        for dep in deps:
            if len(self.dep_pkgs_map[dep]) <= 1:
                self.uninstall_package(dep)
            else:
                self.dep_pkgs_map[dep].remove(package_name)

        self._uninstall_package(package_name)

        return self.installed_packages        


if __name__ == '__main__':
    pkg_installer = Packager()
    print(pkg_installer.add_dependency('TCPIP', ['NETCARD']))
    print(pkg_installer.add_dependency('BROWSER', ['TCPIP', 'HTML']))
    print(pkg_installer.add_dependency('TELNET', ['TCPIP', 'NETCARD']))
    print(pkg_installer.install_package('BROWSER'))
    print(pkg_installer.install_package('TELNET'))
    print(pkg_installer.install_package('BROWSER'))
    print(pkg_installer.uninstall_package('BROWSER'))

