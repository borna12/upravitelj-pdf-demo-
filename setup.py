import cx_Freeze, os, sys

base = None
os.environ['TCL_LIBRARY'] = r"D:\py32\tcl\tcl8.6" 
os.environ['TK_LIBRARY'] = r"D:\py32\tcl\tk8.6" 

if sys.platform=='win32':
    base="Win32GUI"

executables=[cx_Freeze.Executable("PDFmanager.py",base=base,icon='favicon.ico')]

cx_Freeze.setup(
    name="rjecnik",
    options={"build_exe":{"packages":["tkinter","matplotlib","os","datetime","PyPDF2","shutil","PIL"],
    "include_files":["favicon.ico","tcl86t.dll", "tk86t.dll","dokumenti"]}},
    version="0.1",
    description="program za osnovno šifriranje dokumenta te pregled i izmjenu njihovih osnovnih metapodataka",
    executables=executables
)


