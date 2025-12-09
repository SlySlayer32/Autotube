# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller Specification File for Autotube

This file defines how to build a standalone executable for Autotube.

To build the executable:
    1. Install PyInstaller: pip install pyinstaller
    2. Run: pyinstaller autotube.spec
    3. Find the executable in the 'dist' folder

Note: Building executables with all dependencies (especially TensorFlow, librosa)
can result in very large files (500MB+). This is optional and mainly for
distributing to users who don't have Python installed.
"""

block_cipher = None

a = Analysis(
    ['cli.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Include any data files your application needs
        ('project_name', 'project_name'),
    ],
    hiddenimports=[
        'project_name',
        'project_name.cli',
        'project_name.core',
        'project_name.api',
        'project_name.gui',
        'project_name.utils',
        'tkinter',
        'PIL._tkinter_finder',
        'librosa',
        'tensorflow',
        'openl3',
        'sklearn',
        'scipy',
        'numpy',
        'matplotlib',
        'pydub',
        'click',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib.tests',
        'numpy.tests',
        'scipy.tests',
    ],
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
    name='autotube',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Set to False for GUI-only version
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add your icon file here if you have one
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='autotube',
)
