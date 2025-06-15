import cx_Freeze
import sys

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executaveis = [
    cx_Freeze.Executable(
        script="main.py",
        icon="recursos/icone.ico",
        base=base
    )
]

cx_Freeze.setup(
    name="Space Defender",
    options={
        "build_exe": {
            "packages": [
                "pygame",
                "tkinter",
                "speech_recognition",
                "pyttsx3"
            ],
            "includes": [
                "aifc",
                "chunk",
                "audioop",
                "http",
                "urllib",
                "queue",
                "sre_parse",
                "sre_constants",
                "sre_compile"
            ],
            "include_files": [
                ("recursos", "recursos")
            ],
            "excludes": [
                "unittest",
                "email",
                "html",
                "xml",
                "pydoc"
            ]
        }
    },
    executables=executaveis
)