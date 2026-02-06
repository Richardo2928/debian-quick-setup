# ==================================================================
'''
- TODO set yum package manager distros
- TODO do something about get_distro_based if the distro doesn't match anything
'''
# ==================================================================
import os, platform
from typing import Any
from dqs.utils.terminal_utils import log, error, run_command, ok
from dqs.core.installation_methods import PKGManager, DebMethod, FlatpakMethod, HomebrewMethod


DEBIAN_BASED = ["debian", "ubuntu", "linuxmint", "pop", "elementary", "kali", "mx", "zorin"]
FEDORA_BASED = ["fedora", "centos", "rhel"]
ARCH_BASED = ["arch", "manjaro", "endeavouros"]
# TODO !!!

# ==================================================================
# INSTALLATION CONTEXT
# ==================================================================
class InstallationContext:
    """
    Context class providing necessary information for installation methods
    """
    def __init__(self):
        self.distro = self.get_linux_distribution()
        self.distro_based = self.get_distro_based()
        self.env = os.environ.copy()
        self.results = {"completed": [], "failed": []}
        
        # Supported installation methods
        self.methods = {
            "pkg_manager": PKGManager(self),
            "deb": DebMethod(self),
            "flatpak": FlatpakMethod(self),
            "homebrew": HomebrewMethod(self)
        }
        
    
    def get_linux_distribution(self) -> str :
        """
        Returns the name of the Linux distribution in lowercase.
        """
        return platform.freedesktop_os_release().get("ID", "unknown").lower()
    
    def get_distro_based(self) -> str :
        distro = self.distro
        
        if distro in DEBIAN_BASED:
            return "debian"
        elif distro in FEDORA_BASED:
            return "fedora"
        elif self.distro in ARCH_BASED:
            return "arch"
        else:
            raise # TODO !!!

    
    def add_to_path(self, new_path: str) -> None:
        """Adds a new path to the system PATH environment variable."""
        current_path = self.env.get("PATH", "")
        if new_path not in current_path:
            self.env["PATH"] = f"{new_path}{os.pathsep}{current_path}"
    
    def install_package(self, pkg_data: dict[str, any], method_name: str) -> bool:
        """Installs a package using the specified installation method."""
        method = self.methods.get(method_name)
        if not method:
            error(f"Method: '{method_name}', not found.")
            return False

        # Check if setup is required
        if method.requires_setup():
            log(f"Setting up method: '{method_name}'...")
            if not method.setup():
                error(f"Setup for method: '{method_name}' failed.")
                return False
        
        # Install the package
        log(f"Installing package: '{pkg_data.get('name')}' using method: '{method_name}'...")
        
        pkg_id = pkg_data.get("id", "unknown")
        
        success = method.install(pkg_data)
        
        if success:
            self.results["completed"].append(pkg_id)
        else:
            self.results["failed"].append(pkg_id)
            return False
        
        return success
    
    def is_command_available(self, command: str) -> bool:
        """Checks if a command is available in the system PATH."""
        return run_command(f"command -v {command}")