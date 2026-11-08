# SinisterNux Alpha 0.1 welcome, interactive shells only
case "$-" in *i*) ;; *) return 0 ;; esac
if [ -t 1 ]; then
    printf '\n  === SinisterNux Alpha 0.1 ===\n'
    printf '  First Boot development ISO | type: sinister-info\n\n'
fi
