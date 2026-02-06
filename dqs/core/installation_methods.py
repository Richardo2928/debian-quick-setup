from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

from dqs.core.context import InstallationContext
from dqs.utils.terminal_utils import log, ok, error, run_command

# ==================================================================
'''
CONTEMPLATED INSTALLATION METHODS:
- Native package manager
    - apt
    - dnf
    - pacman
    - yum
- deb package
- Flatpak
- Homebrew
'''
# ==================================================================

# ==================================================================
# Abstract Base Class for Installation Methods
# ==================================================================
class InstallationMethod(ABC):
    '''Abstract base class for installation methods.'''
    def __init__(self, context: InstallationContext):
        self.context = context
    
    @abstractmethod
    def install(self, pkg_data: dict[str, Any]) -> bool:
        '''Abstract method that every installation method must implement.'''
        pass
    
    @abstractmethod
    def requires_setup(self) -> bool:
        '''Abstract method to determine if the method requires setup before installation.'''
        pass
    
    def setup(self) -> bool:
        '''Initial configuration or setup required before installation.'''
        return True

# ==================================================================
# Concrete Implementation: Native Package Manager
# ==================================================================
class PKGManager(InstallationMethod):
    '''Class representing the native package manager of the system.'''
    
    INSTALLATION_COMMANDS: Dict[str, str] = {
        'debian': 'sudo apt install -y {pkg}',
        'fedora': 'sudo dnf install -y {pkg}',
        'arch': 'sudo pacman -S --noconfirm {pkg}',
        'redhat': 'sudo yum install -y {pkg}',
    }
    
    def requires_setup(self) -> bool:
        '''Determine if the package manager requires setup.'''
        return False

    def install(self, pkg_data: dict[str, Any]) -> bool:
        pkg_name = pkg_data.get('name') if 'name' in pkg_data else pkg_data.get('id')
        
        command_template = self.INSTALLATION_COMMANDS.get(self.context.distro_based)        
        
        if not command_template:
            error(f"No installation command found for distro: {self.context.distro}")
            return False
        
        return run_command(command_template.format(pkg=pkg_name))
    
# ==================================================================
# Concrete Implementation: DEB Package Installation
# ==================================================================
class DebMethod(InstallationMethod):
    def requires_setup(self) -> bool:
        return False
    
    def install(self, pkg_data: Dict[str, Any]) -> bool:
        name = pkg_data.get("id", "package")
        url = pkg_data.get("url")
        if not url:
            error(f"Missing 'url' for DEB package '{name}'")
            return False
        cmd = f"curl -L '{url}' -o {name}.deb && sudo apt install -y ./{name}.deb && rm {name}.deb"
        return run_command(cmd)

# ==================================================================
# Concrete Implementation: Flatpak Installation
# ==================================================================
class FlatpakMethod(InstallationMethod):
    def requires_setup(self) -> bool:
        return True
    
    def setup(self) -> bool:
        if self.context.is_command_available("flatpak"):
            return True
        
        PKGManager(self.context).install({"id": "flatpak"})
        
        cmd = "sudo flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo"
        return run_command(cmd)
    
    def install(self, pkg_data: Dict[str, Any]) -> bool:
        package_id = pkg_data.get("flatpak_id") or pkg_data.get("id")
        cmd = f"flatpak install -y flathub {package_id}"
        return run_command(cmd)

# ==================================================================
# Concrete Implementation: Homebrew Installation
# ==================================================================
class HomebrewMethod(InstallationMethod):
    def requires_setup(self) -> bool:
        return True
    
    def setup(self) -> bool:
        if self.context.is_command_available("brew"):
            return True
        
        if not run_command('NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'):
            return False
        
        self.context.add_to_path("/home/linuxbrew/.linuxbrew/bin")
        
        return run_command("brew install gcc")
    
    def install(self, pkg_data: Dict[str, Any]) -> bool:
        package = pkg_data.get("flatpak_id") or pkg_data.get("id")
        cmd = f"brew install {package}"
        return run_command(cmd)
        