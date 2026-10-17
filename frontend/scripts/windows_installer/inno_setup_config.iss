[Setup]
AppName=Musk Melon
AppVersion={#AppVersion}
AppPublisher=Musk Melon
WizardStyle=modern
Compression=lzma2
SolidCompression=yes
DefaultDirName={autopf}\MuskMelon\
DefaultGroupName=Musk Melon
SetupIconFile=flowy_logo.ico
UninstallDisplayIcon={app}\MuskMelon.exe
UninstallDisplayName=Musk Melon
VersionInfoVersion={#AppVersion}
UsePreviousAppDir=no

[Files]
Source: "MuskMelon\MuskMelon.exe"; DestDir: "{app}"; DestName: "MuskMelon.exe"; Flags: ignoreversion
Source: "MuskMelon\*";DestDir: "{app}"
Source: "MuskMelon\data\*";DestDir: "{app}\data\"; Flags: recursesubdirs

[Icons]
Name: "{userdesktop}\MuskMelon"; Filename: "{app}\MuskMelon.exe"
Name: "{group}\MuskMelon"; Filename: "{app}\MuskMelon.exe"

[Registry]
Root: HKCR; Subkey: "AppFlowy"; ValueType: "string"; ValueData: "URL:Custom Protocol"; Flags: uninsdeletekey
Root: HKCR; Subkey: "AppFlowy"; ValueType: "string"; ValueName: "URL Protocol"; ValueData: ""
Root: HKCR; Subkey: "AppFlowy\DefaultIcon"; ValueType: "string"; ValueData: "{app}\MuskMelon.exe,0"
Root: HKCR; Subkey: "AppFlowy\shell\open\command"; ValueType: "string"; ValueData: """{app}\MuskMelon.exe"" ""%1"""