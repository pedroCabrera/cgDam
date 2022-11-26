; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "Djed"
#define MyAppVersion "0.1.1"
#define MyAppPublisher "Djed Tools."
#define MyAppURL "https://github.com/Michaelredaa/Djed"
#define MyAppExeName "Djed.exe"
#define ROOT "C:\Users\michael\Documents\work\Djed"
#define SPP "C:\Program Files\Adobe\Adobe Substance 3D Painter\Adobe Substance 3D Painter.exe"
#define BuildName "build\exe.win-amd64-3.9"


[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{368A11E6-3768-462A-841B-E8D9BBAC12CD}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
; Uncomment the following line to run in non administrative install mode (install for current user only.)
;PrivilegesRequired=lowest
OutputBaseFilename=Djed
SetupIconFile={#ROOT}\src\utils\resources\icons\djed.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
; Tell Windows Explorer to reload the environment
ChangesEnvironment=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "{#ROOT}\{#BuildName}\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#ROOT}\{#BuildName}\lib\*";  Excludes: "__pycache__"; DestDir: "{app}\lib"; Flags: ignoreversion recursesubdirs
Source: "{#ROOT}\build\exe.win-amd64-3.9\python39.dll"; DestDir: "{app}";
Source: "{#ROOT}\build\exe.win-amd64-3.9\python3.dll"; DestDir: "{app}";
Source: "{#ROOT}\build\exe.win-amd64-3.9\qt.conf"; DestDir: "{app}";

Source: "{#ROOT}\docs\*";  Excludes: "__pycache__"; DestDir: "{app}\docs"; Flags: ignoreversion recursesubdirs
Source: "{#ROOT}\src\*"; Excludes: "__pycache__"; DestDir: "{app}\src"; Flags: ignoreversion recursesubdirs
Source: "{#ROOT}\venv\*"; Excludes: "__pycache__"; DestDir: "{app}\venv"; Flags: ignoreversion recursesubdirs
;Source: "{#ROOT}\venv\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Registry]
Root: "HKLM"; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; ValueType: string; ValueName: "DJED_ROOT"; ValueData: "{autopf}\{#MyAppName}"; Flags: preservestringtype deletevalue



[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{commonprograms}\Djed Adobe Substance 3D Painter"; Filename: "{#SPP}"; Check: Not FileExists(ExpandConstant('{commonprograms}\spp.lnk')); Parameters: "--enable-remote-scripting"; IconFilename: "{#SPP}";


[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

