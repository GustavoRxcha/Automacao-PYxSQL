import sys
from cx_Freeze import setup, Executable

# Opções de build
build_exe_options = {
    "packages": ["os", "tkinter", "pyodbc", "dotenv", "paramiko", "PIL"],
    "include_files": [".env", ("style/EFlogo.png", "style/EFlogo.png")]  # Coloque aqui arquivos externos, se tiver (como .env, .ico etc)
}

# Base GUI para evitar abrir terminal no Windows
base = "Win32GUI" if sys.platform == "win32" else None

# Setup
setup(
    name="ExecFlow",
    version="0.1",
    description="Automação de processos do HelpDesk",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base, target_name="ExecFlow.exe")]
)