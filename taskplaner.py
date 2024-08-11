"""
Taskplaner Generator
Prüft alle *.py dateien im aktuellen Verzeichnis (excl. venv) nach einer Zeile mit #TaskPlaner [PARAMS]
und generiert dazu passend schtasks.exe - Befehle die im Windows-Taskplaner angelegt werden können.
Diese stehen dann in der taskplaner.cmd-Datei im gleichen Verzeichnis.

Beispiel:
#TaskPlaner: /ST "07:00" /RI 15 /DU 12:00 /SC DAILY
Start 7 Uhr, Wiederholung alle 15 Minuten, Duration 12 Stunden, Täglich

# schtasks /create /tn "(py) cp abc_lineitems"
    /tr "C:\Program Files (x86)\Python36-32\python.exe d:\Work\sf_sync_wwwdb\abc_lineitems.py"
    /ST "07:00" /RI 15 /DU 12:00 /SC DAILY


2020        DJE: init
2021-02-25: DJE: refacator
2023-08-17: DJE: Dokumentation, Pfad-Fix
"""
import os
import sys
from pathlib import Path
# import win32api


xToken = "#TaskPlaner:"
fileName = os.path.dirname(os.path.realpath(__file__)) + "/../taskplaner.cmd"  # im höheres Verzeichnis
prefix = ""


def readToken(filename:str, xToken:str)->str:
    with open(filename, "r") as checkfile:
        if xToken in checkfile.read():  # Prüft ob Token in Datei ist
            with open(filename, "r") as pyfile:
                lines = pyfile.readlines()
                for line in lines:
                    if line.startswith(xToken):  # Zeile mit Token wird ausgelesen
                        return line.replace(xToken, "")
    return ""

def getPythonExecutable():
    exedir = sys.executable
    if " " in exedir:
        # Leerzeichen in Pfaden oder Dateinahmen erzeugen falsche Progrmmaufrufe
        # daher "sicherere" 8.3-Pfadkonvertierung.
        # exedir = win32api.GetShortPathName(exedir)
        pass
    return exedir

def createSchtaskFromFile(filename, name=""):
    EXE_DIR = getPythonExecutable()
    if name == "":
        name = os.path.basename(filename)
        name = f"{name}"
    token = readToken(filename, xToken)
    if token != "":

        param = readToken(filename, xToken)

        return f'schtasks /create /tn "{prefix}{name}" /tr "{EXE_DIR} {filename}" {param}', name
    else:
        return f"REM Kein token in {filename}", name

def main():
    # ROOT_DIR
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    for filename in Path(ROOT_DIR).glob('**/*.py'):
        if "venv" in str(filename):
            continue
        if __file__ == str(filename):
            continue
        if "zzz" in str(filename):
            continue
        #print(filename)
        line = readToken(filename=str(filename), xToken=xToken)
        if line != "":
            name = f"{Path(filename).parent.name}\\{Path(filename).name.replace('.py','')}"
            #print(name)
            print(createSchtaskFromFile(filename=str(filename),name=name)[0])

if __name__ == '__main__':
    main()

