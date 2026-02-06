
import os
import subprocess
import platform

# --------------------------------
# -------- Helpers ---------------
# --------------------------------
def log(msg): print(f"\n👉 {msg}")
def ok(msg): print(f"✅ {msg}")
def fail(msg): print(f"❌ {msg}")


def run_cmd(cmd: str) -> bool:
    log(f"Ejecutando: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode == 0:
        ok("Comando exitoso")
        return True
    else:
        fail(f"Error ejecutando: {cmd}")
        return False

# ---------------------------------------------
# -------- Package Managers per Distro --------
# ---------------------------------------------

DEBIAN_BASED = ["debian", "ubuntu", "linuxmint", "pop", "elementary", "kali", "mx", "zorin"]
FEDORA_BASED = ["fedora", "centos", "rhel"]
ARCH_BASED = ["arch", "manjaro", "endeavouros"]

DISTRO = platform.freedesktop_os_release().get("ID", "unknown").lower()

def set_distro_based():
    global DISTRO
    if DISTRO in DEBIAN_BASED:
       DISTRO = "debian"
    elif DISTRO in FEDORA_BASED:
        DISTRO = "fedora"
    elif DISTRO in ARCH_BASED:
        DISTRO = "arch"

PKG_MANAGERS = {
    "debian": {
        "install": "sudo apt install -y {pkg}",
        "update": "sudo apt update && sudo apt upgrade -y",
    },
    "fedora": {
        "install": "sudo dnf install -y {pkg}",
        "update": "sudo dnf upgrade -y",
    },
    "arch": {
        "install": "sudo pacman -S --noconfirm {pkg}",
        "update": "sudo pacman -Syu --noconfirm",
    },
}

def install_pkg(pkg: str) -> bool:
    if DISTRO in PKG_MANAGERS:
        cmd = PKG_MANAGERS[DISTRO]["install"].format(pkg=pkg)
        return run_cmd(cmd)
    else:
        fail(f"No hay soporte aún para esta distro: {DISTRO}")
        return False

def update_system():
    if DISTRO in PKG_MANAGERS:
        return run_cmd(PKG_MANAGERS[DISTRO]["update"])

# ------------------------------------------
# -------- Setup Dictionary ----------------
# ------------------------------------------

TASKS_DICT = {
    #------------------------
    # Install utilities tasks
    #------------------------
    "install_curl":{
        "req":[],
        "type":"python",
        "func":lambda:install_pkg("curl")
    },
    "install_extrepo":{
        "req":[],
        "type":"python",
        "func":lambda:install_pkg("extrepo")
    },
    "install_git":{
        "req":[],
        "type":"python",
        "func":lambda:install_pkg("git")
    },
    "install_fastfetch":{
        "req":[],
        "type":"python",
        "func":install_pkg("fastfetch")
    },
    "install_btop":{
        "req":[],
        "type":"python",
        "func":lambda:install_pkg("btop")
    },
    "install_ffmpeg":{
        "req":[],
        "type":"python",
        "func":lambda:install_pkg("ffmpeg")
    },
    "install_tmux":{
        "req":[],
        "type":"python",
        "func":lambda:install_pkg("tmux")
    },
    "install_cpu_checker":{
        "req":[],
        "type":"python",
        "func":lambda:install_pkg("cpu-checker")
    },
    "install_build_essential":{
        "req":[],
        "type":"python",
        "func":lambda:install_pkg("build-essential")
    },

    # 

    #------------------------
    # Intall Homebrew tasks
    #------------------------
    "install_homebrew":{
        "req":[
            "install_curl",
            "install_git"
        ],
        "type":"command",
        "cmd":'NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
    },
    "add_homebrew_to_path":{
        "req":[
            "install_homebrew"
        ],
        "type":"python",
        "func":lambda: os.environ.__setitem__(
            "PATH",
            os.environ["PATH"] + ":/home/linuxbrew/.linuxbrew/bin:" + os.path.expanduser("~/.linuxbrew/bin")
        )
    },
    "brew_install_gcc":{
        "req":[
            "add_homebrew_to_path"
        ],
        "type":"command",
        "cmd":"brew install gcc"
    },
    "brew_install_dysk":{
        "req":[
            "add_homebrew_to_path"
        ],
        "type":"command",
        "cmd":"brew install dysk"
    },
    "brew_install_neovim":{
        "req":["add_homebrew_to_path"],
        "type":"command",
        "cmd":"brew install neovim"
    },

    #------------------------
    # Flatpak
    #------------------------
    "install_&_configure_flatpak":{
        "req":[],
        "type":"command",
        "cmd":"sudo apt install -y flatpak && flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo"
    },

    #------------------------
    # Work apps
    #------------------------
    # Rclone
    "install_rclone":{
        "req":["install_curl"],
        "type":"command",
        "cmd":"curl -O https://rclone.org/install.sh | sudo bash && rm install.sh"
    },
    # Obsidian
    "install_obsidian":{
        "req":["install_curl"],
        "type":"command",
        "cmd":"""curl -L https://github.com/obsidianmd/obsidian-releases/releases/download/v1.9.14/obsidian_1.9.14_amd64.deb \\
                -o obsidian.deb \\
                && sudo apt install -y ./obsidian.deb \\
                && rm obsidian.deb"""
    },
    # VS Code
    "install_vscode":{
        "req":["install_curl"],
        "type":"command",
        "cmd":"curl -L 'https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64' -o vscode.deb && sudo apt install -y ./vscode.deb && rm vscode.deb"
    },
    # JetBrains Tool Box TODO execute the binary after extraction
    "install_jb_tool_box":{
        "req":["install_curl"],
        "type":"command",
        "cmd":"""curl -L 'https://download.jetbrains.com/toolbox/jetbrains-toolbox-2.4.2.32922.tar.gz' \\
                -o jb-toolbox.tar.gz \\
                && tar -xvzf jb-toolbox.tar.gz \\
                && rm ../jb-toolbox.tar.gz \\"""
    },
    # Qt Creator & Qt Designer
    "install_qtcreator_qtdesigner":{
        "req":["install_&_configure_flatpak"],
        "type":"command",
        "cmd": """flatpak install -y flathub io.qt.QtCreator \\
                && flatpak install -y flathub io.qt.qtdesignstudio"""
    },
    # PlantUML
    "install_plantuml":{
        "req":[],
        "type":"python",
        "func":lambda:install_pkg("plantuml")
    },
    # Docker
    "setup_apt_for_docker":{
        "req":["install_curl"],
        "type":"command",
        "cmd":"""sudo apt install -y ca-certificates \\
                && sudo install -m 0755 -d /etc/apt/keyrings \\
                && sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc \\
                && sudo chmod a+r /etc/apt/keyrings/docker.asc \\
                && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \\
                | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null \\
                && sudo apt update
        """
    },
    "install_docker":{
        "req":["setup_apt_for_docker"],
        "type":"command",
        "cmd":"""curl -L 'https://desktop.docker.com/linux/main/amd64/docker-desktop-amd64.deb?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-linux-amd64' \\
                -o docker.deb \\
                && sudo apt install -y ./docker.deb \\
                && rm docker.deb"""
    },

    #------------------------
    # Office
    #------------------------
    # LaTeX
    #"install-texlive":{
    #    "req":[],
    #    "type":"python",
    #    "func":lambda:install_pkg("texlive-full")
    #},
    # Draw.io
    "install-drawio":{
        "req":["install_curl"],
        "type":"command",
        "cmd":"""curl -L https://github.com/jgraph/drawio-desktop/releases/download/v27.0.9/drawio-amd64-27.0.9.deb \\
                -o drawio.deb \\
                && sudo apt install -y ./drawio.deb \\
                && rm drawio.deb"""
    },
    # ONLYOFFICE
    "install_onlyoffice":{
        "req":["install_curl"],
        "type":"command",
        "cmd":"""curl -L https://github.com/ONLYOFFICE/DesktopEditors/releases/latest/download/onlyoffice-desktopeditors_amd64.deb \\
                -o onlyoffice.deb \\
                && sudo apt install -y ./onlyoffice.deb \\
                && rm onlyoffice.deb"""
    },

    #------------------------
    # Others
    #------------------------
    # Spotify
    "install_spotify":{
        "req":["install_curl"],
        "type":"command",
        "cmd":"""curl -sS https://download.spotify.com/debian/pubkey_C85668DF69375001.gpg | sudo gpg --dearmor --yes -o /etc/apt/trusted.gpg.d/spotify.gpg \\
                && echo "deb https://repository.spotify.com stable non-free" | sudo tee /etc/apt/sources.list.d/spotify.list \\
                && sudo apt update \\
                && sudo apt install -y spotify-client"""
    },
}

# -------------------------------
# -------- Setup ----------------
# -------------------------------

def run_task(task_name: str, executed: set, results: dict) -> bool:
    
    # Avoid loops
    if task_name in executed:
        return True
    
    task = TASKS_DICT.get(task_name)
    if not task:
        log(f"⚠️ Tarea '{task_name}' no encontrada en TASKS_DICT.")
        results["Errores"].append(task_name)
        fail(f"Falló la tarea: {task_name}")
        return False

    # Run requirements first
    log(f"Ejecutando rquisitos para la tarea: {task_name}")
    for req in task.get("req", []):
        if not run_task(req, executed, results):
            fail(f"Falló la tarea requerida: {req} para la tarea: {task_name}")
            results["Errores"].append(task_name)
            return False
        
    # execute the main task
    log(f"Ejecutando tarea: {task_name}")
    task_type = task.get("type")

    try:
        if task_type == "command":
            ok_ = run_cmd(task.get("cmd", ""))
        elif task_type == "python":
            func = task.get("func")
            if callable(func):
                func()
                ok_ = True
            else:
                fail(f"La función para la tarea {task_name} no es valida.")
                ok_ = False
        else:
            fail(f"Tipo de tarea desconocida para {task_name}: {task_type}")
            ok_ = False
            
    except Exception as e:
        fail(f"Error al ejecutar: {task_name} : {str(e)}")
        ok_ = False

    if ok_:
        executed.add(task_name)
        results["Completado"].append(task_name)
        ok(f"Tarea completada: {task_name}")
        return True
    else:
        results["Errores"].append(task_name)
        fail(f"Falló la tarea: {task_name}")
        return False

def setup():
    results_dict = {
        "Errores": [],
        "Completado": []
    }
    executed = set()

    log(f"Distribución detectada: {DISTRO}")
    set_distro_based()
    
    log("Iniciando Setup...")
    # updating system
    log("Actualizando sistema...")
    if not update_system():
        fail("Algo inesperado sucedio durante la actualización del sistema")
        log("Saliendo del setup")
        return

    # running tasks
    for task_name in TASKS_DICT.keys():
        run_task(task_name=task_name, executed=executed, results=results_dict)


    # final summary
    log("\n📋 --- Resumen de ejecución ---")
    log(f"✅ Completadas: {len(results_dict['Completado'])}")
    log(f"❌ Con errores: {len(results_dict['Errores'])}")

    # Printing errors
    if results_dict["Errores"]:
        log("Tareas con error:")
        for t in results_dict["Errores"]:
            print(f"  - {t}")

    log("\n✨ Setup finalizado.")


# ----------------------
# -------- Main --------
# ----------------------
if __name__ == "__main__":
    setup()
