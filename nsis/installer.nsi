Outfile "gtmp3.exe"
Icon "gtmp3.ico"

Section
    SetOutPath "$INSTDIR"

    File "cli.exe"
    File "gtmp3.ico"

    CreateShortCut "$DESKTOP\gtmp3.lnk" "$INSTDIR\cli.exe" ""  "$INSTDIR\gtmp3.ico"
SectionEnd