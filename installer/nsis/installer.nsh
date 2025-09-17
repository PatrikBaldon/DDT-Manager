; DDT Manager - Configurazione NSIS personalizzata
; File di configurazione per installer Windows

;--------------------------------
; Configurazioni personalizzate

; Nome dell'applicazione
!define APP_NAME "DDT Manager"
!define APP_VERSION "1.0.0"
!define APP_PUBLISHER "Azienda Agricola BB&F"
!define APP_URL "https://github.com/PatrikBaldon/DDT-Application"

; Icone
!define APP_ICON "static\images\icons\icon-512x512.ico"
!define APP_ICON_PNG "static\images\icons\icon-512x512.png"

; Directory di installazione
!define INSTALL_DIR "$PROGRAMFILES\${APP_NAME}"

;--------------------------------
; Funzioni personalizzate

; Funzione per verificare Python
Function CheckPython
    ; Verifica se Python è installato
    ReadRegStr $R0 HKLM "SOFTWARE\Python\PythonCore\3.11\InstallPath" ""
    ${If} $R0 == ""
        ReadRegStr $R0 HKLM "SOFTWARE\Python\PythonCore\3.10\InstallPath" ""
    ${EndIf}
    ${If} $R0 == ""
        ReadRegStr $R0 HKLM "SOFTWARE\Python\PythonCore\3.9\InstallPath" ""
    ${EndIf}
    ${If} $R0 == ""
        ReadRegStr $R0 HKLM "SOFTWARE\Python\PythonCore\3.8\InstallPath" ""
    ${EndIf}
    
    ${If} $R0 == ""
        StrCpy $R1 "false"
    ${Else}
        StrCpy $R1 "true"
    ${EndIf}
FunctionEnd

; Funzione per verificare Node.js
Function CheckNode
    ; Verifica se Node.js è installato
    ReadRegStr $R0 HKLM "SOFTWARE\Node.js" "InstallPath"
    
    ${If} $R0 == ""
        StrCpy $R1 "false"
    ${Else}
        StrCpy $R1 "true"
    ${EndIf}
FunctionEnd

; Funzione per installare Python
Function InstallPython
    DetailPrint "Installazione Python..."
    
    ; Download Python installer
    NSISdl::download "https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe" "$TEMP\python-installer.exe"
    Pop $R0
    
    ${If} $R0 == "success"
        ; Install Python silently
        ExecWait '"$TEMP\python-installer.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0'
        Delete "$TEMP\python-installer.exe"
        DetailPrint "Python installato con successo!"
    ${Else}
        MessageBox MB_OK "Errore nel download di Python. Installazione fallita."
        Abort
    ${EndIf}
FunctionEnd

; Funzione per installare Node.js
Function InstallNode
    DetailPrint "Installazione Node.js..."
    
    ; Download Node.js installer
    NSISdl::download "https://nodejs.org/dist/v20.10.0/node-v20.10.0-x64.msi" "$TEMP\node-installer.msi"
    Pop $R0
    
    ${If} $R0 == "success"
        ; Install Node.js silently
        ExecWait 'msiexec /i "$TEMP\node-installer.msi" /quiet'
        Delete "$TEMP\node-installer.msi"
        DetailPrint "Node.js installato con successo!"
    ${Else}
        MessageBox MB_OK "Errore nel download di Node.js. Installazione fallita."
        Abort
    ${EndIf}
FunctionEnd

; Funzione per creare shortcut
Function CreateShortcuts
    ; Desktop shortcut
    CreateShortCut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${APP_NAME}.exe"
    
    ; Start Menu shortcuts
    CreateDirectory "$SMPROGRAMS\${APP_NAME}"
    CreateShortCut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\${APP_NAME}.exe"
    CreateShortCut "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
    CreateShortCut "$SMPROGRAMS\${APP_NAME}\README.lnk" "$INSTDIR\README.txt"
    
    ; Quick Launch shortcut
    CreateShortCut "$QUICKLAUNCH\${APP_NAME}.lnk" "$INSTDIR\${APP_NAME}.exe"
FunctionEnd

; Funzione per rimuovere shortcut
Function RemoveShortcuts
    ; Desktop shortcut
    Delete "$DESKTOP\${APP_NAME}.lnk"
    
    ; Start Menu shortcuts
    Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"
    Delete "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk"
    Delete "$SMPROGRAMS\${APP_NAME}\README.lnk"
    RMDir "$SMPROGRAMS\${APP_NAME}"
    
    ; Quick Launch shortcut
    Delete "$QUICKLAUNCH\${APP_NAME}.lnk"
FunctionEnd

; Funzione per verificare prerequisiti
Function CheckPrerequisites
    ; Verifica Python
    Call CheckPython
    ${If} $R1 == "false"
        MessageBox MB_YESNO "Python non trovato. Vuoi installarlo automaticamente?" IDYES install_python IDNO skip_python
        install_python:
            Call InstallPython
        skip_python:
    ${EndIf}
    
    ; Verifica Node.js
    Call CheckNode
    ${If} $R1 == "false"
        MessageBox MB_YESNO "Node.js non trovato. Vuoi installarlo automaticamente?" IDYES install_node IDNO skip_node
        install_node:
            Call InstallNode
        skip_node:
    ${EndIf}
FunctionEnd

; Funzione per configurare l'applicazione
Function ConfigureApplication
    ; Crea directory per dati utente
    CreateDirectory "$APPDATA\${APP_NAME}"
    CreateDirectory "$APPDATA\${APP_NAME}\logs"
    CreateDirectory "$APPDATA\${APP_NAME}\data"
    
    ; Crea file di configurazione
    FileOpen $R0 "$APPDATA\${APP_NAME}\config.ini" w
    FileWrite $R0 "[General]$\r$\n"
    FileWrite $R0 "AppName=${APP_NAME}$\r$\n"
    FileWrite $R0 "Version=${APP_VERSION}$\r$\n"
    FileWrite $R0 "InstallDir=$INSTDIR$\r$\n"
    FileWrite $R0 "DataDir=$APPDATA\${APP_NAME}$\r$\n"
    FileClose $R0
FunctionEnd

; Funzione per pulire configurazione
Function CleanupConfiguration
    ; Rimuovi file di configurazione
    Delete "$APPDATA\${APP_NAME}\config.ini"
    
    ; Rimuovi directory se vuota
    RMDir "$APPDATA\${APP_NAME}\logs"
    RMDir "$APPDATA\${APP_NAME}\data"
    RMDir "$APPDATA\${APP_NAME}"
FunctionEnd
