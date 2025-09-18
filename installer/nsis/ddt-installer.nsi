; DDT Manager - Installer NSIS per Windows
; Script di installazione con interfaccia grafica

!define APP_NAME "DDT Manager"
!define APP_VERSION "1.1.0"
!define APP_PUBLISHER "Azienda Agricola BB&F"
!define APP_WEB_SITE "https://github.com/aziendaagricola/ddt-manager"
!define APP_EXECUTABLE "DDT Manager.exe"
!define APP_DESCRIPTION "Sistema di gestione Documenti di Trasporto per aziende agricole"

; Include le librerie necessarie
!include "MUI2.nsh"
!include "FileFunc.nsh"
!include "LogicLib.nsh"
!include "WinVer.nsh"
!include "x64.nsh"

; Configurazione generale
Name "${APP_NAME}"
OutFile "DDT_Manager_Setup_${APP_VERSION}.exe"
InstallDir "$PROGRAMFILES64\${APP_NAME}"
InstallDirRegKey HKLM "Software\${APP_NAME}" "Install_Dir"
RequestExecutionLevel admin
Unicode True

; Configurazione interfaccia
!define MUI_ICON "..\..\static\images\icons\icon-512x512.ico"
!define MUI_UNICON "..\..\static\images\icons\icon-512x512.ico"
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "..\..\static\images\logo1.bmp"
!define MUI_WELCOMEFINISHPAGE_BITMAP "..\..\static\images\logo1.bmp"
!define MUI_UNWELCOMEFINISHPAGE_BITMAP "..\..\static\images\logo1.bmp"

; Pagine dell'installer
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "..\..\LICENSE"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; Pagine di disinstallazione
!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

; Lingue
!insertmacro MUI_LANGUAGE "Italian"

; Sezioni dell'installer
Section "Applicazione Principale" SecMain
    SectionIn RO
    
    SetOutPath "$INSTDIR"
    
    ; File dell'applicazione
    File /r "..\..\electron\*"
    File /r "..\..\static\*"
    File /r "..\..\templates\*"
    File /r "..\..\ddt_app\*"
    File /r "..\..\ddt_project\*"
    File "..\..\manage.py"
    File "..\..\requirements.txt"
    File "..\..\db.sqlite3"
    File "..\..\package.json"
    
    ; Crea directory necessarie
    CreateDirectory "$INSTDIR\logs"
    CreateDirectory "$INSTDIR\backup"
    CreateDirectory "$INSTDIR\static\pdf"
    CreateDirectory "$INSTDIR\templates\pdf"
    
    ; Crea script di avvio
    FileOpen $0 "$INSTDIR\start_ddt.bat" w
    FileWrite $0 "@echo off$\r$\n"
    FileWrite $0 "echo Avvio DDT Manager...$\r$\n"
    FileWrite $0 "cd /d $\"$INSTDIR$\"$\r$\n"
    FileWrite $0 "npm run electron$\r$\n"
    FileClose $0
    
    ; Crea script di installazione dipendenze
    FileOpen $0 "$INSTDIR\install_dependencies.bat" w
    FileWrite $0 "@echo off$\r$\n"
    FileWrite $0 "echo Installazione dipendenze DDT Manager...$\r$\n"
    FileWrite $0 "cd /d $\"$INSTDIR$\"$\r$\n"
    FileWrite $0 "pip install -r requirements.txt$\r$\n"
    FileWrite $0 "npm install$\r$\n"
    FileWrite $0 "python manage.py migrate$\r$\n"
    FileWrite $0 "python manage.py collectstatic --noinput$\r$\n"
    FileWrite $0 "echo Installazione completata!$\r$\n"
    FileWrite $0 "pause$\r$\n"
    FileClose $0
    
    ; Registra l'installazione
    WriteRegStr HKLM "Software\${APP_NAME}" "Install_Dir" "$INSTDIR"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayName" "${APP_NAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "UninstallString" "$INSTDIR\uninstall.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayIcon" "$INSTDIR\${APP_EXECUTABLE}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "Publisher" "${APP_PUBLISHER}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayVersion" "${APP_VERSION}"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "NoModify" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "NoRepair" 1
    
    ; Crea disinstallatore
    WriteUninstaller "$INSTDIR\uninstall.exe"
SectionEnd

Section "Shortcut Desktop" SecDesktop
    CreateShortCut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\start_ddt.bat" "" "$INSTDIR\static\images\icons\icon-512x512.ico"
SectionEnd

Section "Shortcut Menu Start" SecStartMenu
    CreateDirectory "$SMPROGRAMS\${APP_NAME}"
    CreateShortCut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\start_ddt.bat" "" "$INSTDIR\static\images\icons\icon-512x512.ico"
    CreateShortCut "$SMPROGRAMS\${APP_NAME}\Disinstalla.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe"
SectionEnd

Section "Python e Node.js" SecDependencies
    ; Verifica Python
    nsExec::ExecToLog 'python --version'
    Pop $0
    ${If} $0 != 0
        MessageBox MB_YESNO "Python non trovato. Vuoi scaricare Python automaticamente?" IDYES download_python IDNO skip_python
        download_python:
            ExecShell "open" "https://www.python.org/downloads/"
            MessageBox MB_OK "Scarica e installa Python, poi riavvia l'installer."
        skip_python:
    ${EndIf}
    
    ; Verifica Node.js
    nsExec::ExecToLog 'node --version'
    Pop $0
    ${If} $0 != 0
        MessageBox MB_YESNO "Node.js non trovato. Vuoi scaricare Node.js automaticamente?" IDYES download_node IDNO skip_node
        download_node:
            ExecShell "open" "https://nodejs.org/"
            MessageBox MB_OK "Scarica e installa Node.js, poi riavvia l'installer."
        skip_node:
    ${EndIf}
SectionEnd

; Descrizioni delle sezioni
LangString DESC_SecMain ${LANG_ITALIAN} "File principali dell'applicazione DDT Manager"
LangString DESC_SecDesktop ${LANG_ITALIAN} "Crea un collegamento sul desktop"
LangString DESC_SecStartMenu ${LANG_ITALIAN} "Crea collegamenti nel menu Start"
LangString DESC_SecDependencies ${LANG_ITALIAN} "Verifica e installa Python e Node.js"

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${SecMain} $(DESC_SecMain)
    !insertmacro MUI_DESCRIPTION_TEXT ${SecDesktop} $(DESC_SecDesktop)
    !insertmacro MUI_DESCRIPTION_TEXT ${SecStartMenu} $(DESC_SecStartMenu)
    !insertmacro MUI_DESCRIPTION_TEXT ${SecDependencies} $(DESC_SecDependencies)
!insertmacro MUI_FUNCTION_DESCRIPTION_END

; Sezione di disinstallazione
Section "Uninstall"
    ; Rimuovi file
    RMDir /r "$INSTDIR"
    
    ; Rimuovi collegamenti
    Delete "$DESKTOP\${APP_NAME}.lnk"
    RMDir /r "$SMPROGRAMS\${APP_NAME}"
    
    ; Rimuovi chiavi di registro
    DeleteRegKey HKLM "Software\${APP_NAME}"
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
SectionEnd

; Funzioni
Function .onInit
    ; Verifica versione Windows
    ${IfNot} ${AtLeastWin7}
        MessageBox MB_OK "Questo software richiede Windows 7 o superiore."
        Quit
    ${EndIf}
    
    ; Verifica architettura
    ${If} ${RunningX64}
        ; OK, sistema a 64 bit
    ${Else}
        MessageBox MB_YESNO "Questo software è ottimizzato per sistemi a 64 bit. Continuare comunque?" IDYES continue_install IDNO quit_install
        continue_install:
        Goto end_arch_check
        quit_install:
        Quit
        end_arch_check:
    ${EndIf}
FunctionEnd

Function .onInstSuccess
    MessageBox MB_YESNO "Installazione completata! Vuoi avviare DDT Manager ora?" IDYES start_app IDNO end_install
    start_app:
        Exec "$INSTDIR\start_ddt.bat"
    end_install:
FunctionEnd
