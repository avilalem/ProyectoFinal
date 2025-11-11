# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    datas=[
    ('icono-agregar.png', '.'),
    ('icono-atras.png', '.'),
    ('icono-buscar.png', '.'),
    ('icono-carro.png', '.'),
    ('icono-editar.png', '.'),
    ('icono-eliminar.png', '.'),
    ('icono-guardar.png', '.'),
    ('icono-informacion.png', '.'),
    ('icono-salir.png', '.'),
    ('recetario.db', '.'),
    ('*.ui', '.'),
],
binaries=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='RecetarioDigital',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
