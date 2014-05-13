# -*- mode: python -*-
a = Analysis(['.\\levelBuilder.py'],
             pathex=['C:\\Users\\Emmanuel\\Desktop\\SchoolFiles\\levelBuilder\\Source\\Windows'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='levelBuilder.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
