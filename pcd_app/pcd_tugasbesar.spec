# PyInstaller spec for PCD_TugasBesar
# Run: pyinstaller pcd_app/main.py --onefile --noconsole --name=PCD_TugasBesar

block_cipher = None

from PyInstaller.utils.hooks import collect_submodules
hiddenimports = collect_submodules('modules')

a = Analysis(
    ['pcd_app/main.py'],
    pathex=[],
    binaries=[],
    datas=[('pcd_app/assets/sample_images/*', 'assets/sample_images')],
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PCD_TugasBesar',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PCD_TugasBesar')
