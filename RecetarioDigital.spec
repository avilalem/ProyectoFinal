# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('pagina_principal.ui', '.'), ('pagina_principal_admin.ui', '.'), ('pagina_principal_contraseña.ui', '.'), ('pagina_agregar_receta.ui', '.'), ('pagina_busqueda.ui', '.'), ('pagina_lista.ui', '.'), ('pagina_lista_compras.ui', '.'), ('pagina_receta.ui', '.'), ('pagina_editar_receta.ui', '.'), ('*.png', '.'), ('recetario.db', '.')],
    hiddenimports=['reportlab', 'reportlab.pdfgen', 'reportlab.lib.pagesizes'],
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
    [],
    exclude_binaries=True,
    name='RecetarioDigital',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icono.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='RecetarioDigital',
)
