; DDT Manager NSIS Installer Script
; Configurazioni personalizzate per l'installer

!macro preInit
  ; Pre-inizializzazione
  SetRegView 64
  WriteRegExpandStr HKLM "${INSTALL_REGISTRY_KEY}" InstallLocation "$INSTDIR"
  WriteRegExpandStr HKCU "${INSTALL_REGISTRY_KEY}" InstallLocation "$INSTDIR"
!macroend

!macro customInstall
  ; Installazione personalizzata
  DetailPrint "Configurazione DDT Manager..."
  
  ; Crea collegamento desktop
  CreateShortCut "$DESKTOP\DDT Manager.lnk" "$INSTDIR\DDT Manager.exe"
  
  ; Crea collegamento menu Start
  CreateDirectory "$SMPROGRAMS\DDT Manager"
  CreateShortCut "$SMPROGRAMS\DDT Manager\DDT Manager.lnk" "$INSTDIR\DDT Manager.exe"
  CreateShortCut "$SMPROGRAMS\DDT Manager\Uninstall DDT Manager.lnk" "$INSTDIR\Uninstall DDT Manager.exe"
  
  ; Registra l'applicazione
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\DDT Manager" "DisplayName" "DDT Manager"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\DDT Manager" "UninstallString" "$INSTDIR\Uninstall DDT Manager.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\DDT Manager" "InstallLocation" "$INSTDIR"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\DDT Manager" "Publisher" "Azienda Agricola BB&F"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\DDT Manager" "DisplayVersion" "1.0.0"
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\DDT Manager" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\DDT Manager" "NoRepair" 1
!macroend

!macro customUnInstall
  ; Disinstallazione personalizzata
  DetailPrint "Rimozione DDT Manager..."
  
  ; Rimuovi collegamenti
  Delete "$DESKTOP\DDT Manager.lnk"
  RMDir /r "$SMPROGRAMS\DDT Manager"
  
  ; Rimuovi chiavi di registro
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\DDT Manager"
!macroend

!macro customHeader
  ; Header personalizzato
  !system "echo DDT Manager Installer v1.0.0" > "${BUILD_RESOURCES_DIR}\customHeader.txt"
!macroend

!macro customWelcomePage
  ; Pagina di benvenuto personalizzata
  !insertmacro MUI_PAGE_WELCOME
!macroend

!macro customFinishPage
  ; Pagina di completamento personalizzata
  !define MUI_FINISHPAGE_RUN "$INSTDIR\DDT Manager.exe"
  !define MUI_FINISHPAGE_RUN_TEXT "Avvia DDT Manager"
  !insertmacro MUI_PAGE_FINISH
!macroend
