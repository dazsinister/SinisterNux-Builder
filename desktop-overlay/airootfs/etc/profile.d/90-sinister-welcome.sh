# SinisterNux Alpha 0.2 KDE live image terminal welcome
case "$-" in *i*) ;; *) return 0 ;; esac
if [ -t 1 ]; then
    printf '\n  === SinisterNux Alpha 0.2 KDE ===\n'
    printf '  Live desktop development ISO | type: sinister-info\n\n'
fi
