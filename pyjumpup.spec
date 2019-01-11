# -*- mode: python -*-
#
# To build executable: $ pyinstaller pyjumpup.spec

NAME = 'pyjumpup'
ASSETS = [('resources', 'resources')]
CODE = [
    'main.py',
    'settings.py'
]

DEBUG = False
CONSOLE = DEBUG

### PyInstaller configuration below

block_cipher = None
from os import getcwd
a = Analysis(CODE,
             pathex=[getcwd()],
             binaries=[],
             datas=ASSETS,
             hiddenimports=['pygame'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
            cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name=NAME,
          debug=DEBUG,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=CONSOLE)
