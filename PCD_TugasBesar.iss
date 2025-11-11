; Inno Setup script for PCD Tugas Besar
[Setup]
AppName=PCD Tugas Besar
AppVersion=1.0
DefaultDirName={pf}\PCD_TugasBesar
DefaultGroupName=PCD Tugas Besar
OutputBaseFilename=PCD_TugasBesar_Installer
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\PCD_TugasBesar.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\PCD Tugas Besar"; Filename: "{app}\PCD_TugasBesar.exe"
Name: "{commondesktop}\PCD Tugas Besar"; Filename: "{app}\PCD_TugasBesar.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"
