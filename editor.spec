# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/editor/Main.py'],
    pathex=['src'],
    binaries=[],
    datas=[('src', 'src')],
    hiddenimports=['json',
		   'secrets',
                   'pyparsing',
                   'torch',
                   'omegaconf', 
                   'PySide6.QtMultimedia',
                   'whisper',
                   'speech_recognition',
		   'pydub'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SYOA_Editor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    icon='icons/editor.ico'
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='editor',
)
