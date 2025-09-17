; DDT Manager - Installer NSIS
; Script per creare installer Windows professionale

;--------------------------------
; Include Modern UI
!include "MUI2.nsh"
!include "FileFunc.nsh"
!include "LogicLib.nsh"
!include "WinVer.nsh"

;--------------------------------
; General

; Name and file
Name "DDT Manager"
OutFile "DDT_Manager_Setup.exe"
Unicode True

; Default installation folder
InstallDir "$PROGRAMFILES\DDT Manager"

; Get installation folder from registry if available
InstallDirRegKey HKCU "Software\DDT Manager" "Install_Dir"

; Request application privileges for Windows Vista
RequestExecutionLevel admin

;--------------------------------
; Variables

Var StartMenuFolder
Var PythonInstalled
Var NodeInstalled
Var PythonPath
Var NodePath

;--------------------------------
; Interface Settings

!define MUI_ABORTWARNING
!define MUI_ICON "..\..\static\images\icons\icon-512x512.png"
!define MUI_UNICON "..\..\static\images\icons\icon-512x512.png"

;--------------------------------
; Pages

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "..\..\LICENSE"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY

; Start Menu Folder Page Configuration
!define MUI_STARTMENUPAGE_REGISTRY_ROOT "HKCU"
!define MUI_STARTMENUPAGE_REGISTRY_KEY "Software\DDT Manager"
!define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "Start Menu Folder"

!insertmacro MUI_PAGE_STARTMENU Application $StartMenuFolder
!insertmacro MUI_PAGE_INSTFILES

; Finish page
!define MUI_FINISHPAGE_RUN "$INSTDIR\DDT Manager.exe"
!define MUI_FINISHPAGE_RUN_TEXT "Avvia DDT Manager"
!define MUI_FINISHPAGE_SHOWREADME "$INSTDIR\README.txt"
!define MUI_FINISHPAGE_SHOWREADME_TEXT "Mostra README"
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

;--------------------------------
; Languages

!insertmacro MUI_LANGUAGE "Italian"

;--------------------------------
; Installer Sections

Section "DDT Manager (Required)" SecMain
    SectionIn RO
    
    SetOutPath "$INSTDIR"
    
    ; Copy application files
    File /r "..\..\dist\win-unpacked\*"
    
    ; Copy additional files
    File "..\..\LICENSE"
    File "..\..\README.md"
    
    ; Store installation folder
    WriteRegStr HKCU "Software\DDT Manager" "Install_Dir" "$INSTDIR"
    
    ; Create uninstaller
    WriteUninstaller "$INSTDIR\Uninstall.exe"
    
    ; Add to Add/Remove Programs
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\DDT Manager" "DisplayName" "DDT Manager"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\DDT Manager" "UninstallString" "$INSTDIR\Uninstall.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\DDT Manager" "InstallLocation" "$INSTDIR"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\DDT Manager" "DisplayIcon" "$INSTDIR\DDT Manager.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\DDT Manager" "Publisher" "Patrik Baldon"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\DDT Manager" "DisplayVersion" "1.0.0"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\DDT Manager" "NoModify" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\DDT Manager" "NoRepair" 1
    
    ; Create Start Menu shortcuts
    !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
        CreateDirectory "$SMPROGRAMS\$StartMenuFolder"
        CreateShortCut "$SMPROGRAMS\$StartMenuFolder\DDT Manager.lnk" "$INSTDIR\DDT Manager.exe"
        CreateShortCut "$SMPROGRAMS\$StartMenuFolder\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
        CreateShortCut "$SMPROGRAMS\$StartMenuFolder\README.lnk" "$INSTDIR\README.txt"
    !insertmacro MUI_STARTMENU_WRITE_END
    
    ; Create Desktop shortcut
    CreateShortCut "$DESKTOP\DDT Manager.lnk" "$INSTDIR\DDT Manager.exe"
    
    ; Create Quick Launch shortcut
    CreateShortCut "$QUICKLAUNCH\DDT Manager.lnk" "$INSTDIR\DDT Manager.exe"
SectionEnd

Section "Python Runtime" SecPython
    ; Check if Python is already installed
    Call CheckPython
    
    ${If} $PythonInstalled == "false"
        DetailPrint "Python non trovato. Installazione Python..."
        ; Download and install Python
        Call InstallPython
    ${Else}
        DetailPrint "Python già installato: $PythonPath"
    ${EndIf}
SectionEnd

Section "Node.js Runtime" SecNode
    ; Check if Node.js is already installed
    Call CheckNode
    
    ${If} $NodeInstalled == "false"
        DetailPrint "Node.js non trovato. Installazione Node.js..."
        ; Download and install Node.js
        Call InstallNode
    ${Else}
        DetailPrint "Node.js già installato: $NodePath"
    ${EndIf}
SectionEnd

;--------------------------------
; Descriptions

; Language strings
LangString DESC_SecMain ${LANG_ITALIAN} "Componenti principali dell'applicazione DDT Manager."
LangString DESC_SecPython ${LANG_ITALIAN} "Runtime Python necessario per il funzionamento dell'applicazione."
LangString DESC_SecNode ${LANG_ITALIAN} "Runtime Node.js necessario per l'applicazione Electron."

; Assign language strings to sections
!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${SecMain} $(DESC_SecMain)
    !insertmacro MUI_DESCRIPTION_TEXT ${SecPython} $(DESC_SecPython)
    !insertmacro MUI_DESCRIPTION_TEXT ${SecNode} $(DESC_SecNode)
!insertmacro MUI_FUNCTION_DESCRIPTION_END

;--------------------------------
; Functions

Function CheckPython
    ; Check if Python is installed
    ReadRegStr $PythonPath HKLM "SOFTWARE\Python\PythonCore\3.11\InstallPath" ""
    ${If} $PythonPath == ""
        ReadRegStr $PythonPath HKLM "SOFTWARE\Python\PythonCore\3.10\InstallPath" ""
    ${EndIf}
    ${If} $PythonPath == ""
        ReadRegStr $PythonPath HKLM "SOFTWARE\Python\PythonCore\3.9\InstallPath" ""
    ${EndIf}
    ${If} $PythonPath == ""
        ReadRegStr $PythonPath HKLM "SOFTWARE\Python\PythonCore\3.8\InstallPath" ""
    ${EndIf}
    
    ${If} $PythonPath == ""
        StrCpy $PythonInstalled "false"
    ${Else}
        StrCpy $PythonInstalled "true"
    ${EndIf}
FunctionEnd

Function CheckNode
    ; Check if Node.js is installed
    ReadRegStr $NodePath HKLM "SOFTWARE\Node.js" "InstallPath"
    
    ${If} $NodePath == ""
        StrCpy $NodeInstalled "false"
    ${Else}
        StrCpy $NodeInstalled "true"
    ${EndIf}
FunctionEnd

Function InstallPython
    ; Download Python installer
    DetailPrint "Download Python installer..."
    NSISdl::download "https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe" "$TEMP\python-installer.exe"
    Pop $0
    
    ${If} $0 == "success"
        DetailPrint "Installazione Python..."
        ExecWait '"$TEMP\python-installer.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0'
        Delete "$TEMP\python-installer.exe"
        DetailPrint "Python installato con successo!"
    ${Else}
        MessageBox MB_OK "Errore nel download di Python. Installazione fallita."
        Abort
    ${EndIf}
FunctionEnd

Function InstallNode
    ; Download Node.js installer
    DetailPrint "Download Node.js installer..."
    NSISdl::download "https://nodejs.org/dist/v20.10.0/node-v20.10.0-x64.msi" "$TEMP\node-installer.msi"
    Pop $0
    
    ${If} $0 == "success"
        DetailPrint "Installazione Node.js..."
        ExecWait 'msiexec /i "$TEMP\node-installer.msi" /quiet'
        Delete "$TEMP\node-installer.msi"
        DetailPrint "Node.js installato con successo!"
    ${Else}
        MessageBox MB_OK "Errore nel download di Node.js. Installazione fallita."
        Abort
    ${EndIf}
FunctionEnd

Function .onInit
    ; Check if already installed
    ReadRegStr $R0 HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\DDT Manager" "UninstallString"
    StrCmp $R0 "" done
    
    MessageBox MB_OKCANCEL|MB_ICONEXCLAMATION "DDT Manager è già installato. $\n$\nClicca OK per disinstallare la versione precedente o Annulla per annullare l'installazione." IDOK uninst
    Abort
    
    uninst:
        ClearErrors
        ExecWait '$R0 _?=$INSTDIR'
        
        IfErrors no_remove_uninstaller done
        no_remove_uninstaller:
    
    done:
FunctionEnd

;--------------------------------
; Uninstaller Section

Section "Uninstall"
    ; Remove files and uninstaller
    Delete "$INSTDIR\Uninstall.exe"
    Delete "$INSTDIR\DDT Manager.exe"
    Delete "$INSTDIR\LICENSE"
    Delete "$INSTDIR\README.txt"
    
    ; Remove directories
    RMDir /r "$INSTDIR"
    
    ; Remove Start Menu shortcuts
    !insertmacro MUI_STARTMENU_GETFOLDER "Application" $StartMenuFolder
    Delete "$SMPROGRAMS\$StartMenuFolder\DDT Manager.lnk"
    Delete "$SMPROGRAMS\$StartMenuFolder\Uninstall.lnk"
    Delete "$SMPROGRAMS\$StartMenuFolder\README.lnk"
    RMDir "$SMPROGRAMS\$StartMenuFolder"
    
    ; Remove Desktop shortcut
    Delete "$DESKTOP\DDT Manager.lnk"
    
    ; Remove Quick Launch shortcut
    Delete "$QUICKLAUNCH\DDT Manager.lnk"
    
    ; Remove registry keys
    DeleteRegKey HKCU "Software\DDT Manager"
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\DDT Manager"
    
    ; Remove application data
    RMDir /r "$APPDATA\DDT Manager"
SectionEnd

;--------------------------------
; Uninstaller Functions

Function un.onInit
    MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "Sei sicuro di voler disinstallare DDT Manager?" IDYES +2
    Abort
FunctionEnd
