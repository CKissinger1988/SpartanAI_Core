[Setup]
AppName=JarvisAI Backend
AppVersion=1.0
DefaultDirName={pf}\JarvisAI_Backend
DefaultGroupName=JarvisAI
OutputDir=.
OutputBaseFilename=JarvisBackendInstaller
Compression=lzma
SolidCompression=yes

[Files]
Source: "cloud_backend\*"; DestDir: "{app}"; Flags: recursesubdirs

[Run]
; Run the setup script to install dependencies
Filename: "{app}\venv\Scripts\python.exe"; Parameters: "-m pip install -r {app}\requirements.txt"; StatusMsg: "Installing dependencies..."

; Register as a service using NSSM
Filename: "{app}\nssm.exe"; Parameters: "install JarvisBackend ""{app}\venv\Scripts\python.exe"" ""{app}\main.py"""; Flags: runhidden
Filename: "{app}\nssm.exe"; Parameters: "start JarvisBackend"; Flags: runhidden
