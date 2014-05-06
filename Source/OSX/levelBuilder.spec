# -*- mode: python -*-
a = Analysis(['levelBuilder.py'],
             pathex=['/Users/Manny/levelBuilder/Source/OSX'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='levelBuilder',
          debug=False,
          strip=None,
          upx=True,
          console=True )
