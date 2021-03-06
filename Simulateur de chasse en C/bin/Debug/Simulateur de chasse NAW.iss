; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{38BA56E6-F31F-48AA-A4E5-C14A0EC79B09}
AppName=Simulateur de chasse NAW
AppVersion=1
;AppVerName=Simulateur de chasse NAW 1
AppPublisher=EvilAnt
AppPublisherURL=www.natureatwar.fr
AppSupportURL=www.natureatwar.fr
AppUpdatesURL=www.natureatwar.fr
DefaultDirName={pf}\Simulateur de chasse NAW
DisableProgramGroupPage=yes
OutputDir=D:\Mes documents\Programmation C\Simulateur de chasse NAW
OutputBaseFilename=Simulateur_ de_chasse_NAW_setup
Compression=lzma
SolidCompression=yes

[Languages]
Name: "french"; MessagesFile: "compiler:Languages\French.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "D:\Mes documents\Programmation C\Simulateur de chasse NAW\bin\Debug\Simulateur de chasse NAW.exe"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{commonprograms}\Simulateur de chasse NAW"; Filename: "{app}\Simulateur de chasse NAW.exe"
Name: "{commondesktop}\Simulateur de chasse NAW"; Filename: "{app}\Simulateur de chasse NAW.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\Simulateur de chasse NAW.exe"; Description: "{cm:LaunchProgram,Simulateur de chasse NAW}"; Flags: nowait postinstall skipifsilent

