# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['cv2', 'pyvirtualcam', 'numpy', 'pyaudio', 'rumps'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ZoomFX',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_dir=None,
    name='ZoomFX',
)

app = BUNDLE(
    coll,
    name='VirtualFX.app',
    icon='icon.icns',
    bundle_identifier='com.andre.zoomfx',
    info_plist={
        'NSCameraUsageDescription': 'ZoomFX membutuhkan akses kamera untuk efek visual Thanos.',
        'NSMicrophoneUsageDescription': 'ZoomFX membutuhkan akses mikrofon untuk efek pengubah suara Chipmunk.',
        'LSUIElement': True,
    },
)