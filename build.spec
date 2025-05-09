# build.spec
block_cipher = None

a = Analysis(
    ['main.py'],  # Arquivo principal do seu projeto
    pathex=[],    # Caminhos adicionais, se necessário
    binaries=[],   # Para DLLs externas, se precisar
    datas=[
        ('EFlogo.png', '.'),                   # Ícone (Imagem)
        ('ScriptsSQL/*.sql', 'ScriptsSQL'),          # Pasta com scripts SQL
        # Adiciona os arquivos Python necessários, se não estiverem na mesma pasta
        ('funcoesloja.py', '.'),  # Caso os módulos estejam em pastas diferentes
        ('funcoescaixa.py', '.'),
        ('cores.py', '.'),
    ],
    hiddenimports=[],  # Para módulos que PyInstaller não detecta automaticamente
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    name='ExecFlow',  # Nome do seu executável
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,                 # Comprime o executável (recomendado)
    console=False,            # Se False, não mostra o terminal (para apps com interface)
    icon='EFlogo.png',        # Ícone do executável
    distpath='dist'           # Garante que o executável vá para a pasta dist
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='ExecFlow'
)
