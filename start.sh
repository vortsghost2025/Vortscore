#!/bin/bash
ROOT="$HOME/vitalis_devcore"
SESSION="vitalis"

echo "╔══════════════════════════════════════════╗"
echo "║     VITALIS FSI — SOVEREIGN BOOT        ║"
echo "║     Local. Private. Autonomous.         ║"
echo "╚══════════════════════════════════════════╝"

if ! command -v tmux &>/dev/null; then
    sudo apt-get install -y tmux -q
fi

tmux kill-session -t $SESSION 2>/dev/null
tmux new-session -d -s $SESSION -n daemon  "cd $ROOT && python3 -m src.ide_kernel.daemon; bash"
tmux new-window     -t $SESSION -n gateway "cd $ROOT && python3 -m flask --app src.ide_kernel.gateway run --port 5001; bash"
tmux new-window     -t $SESSION -n healing "cd $ROOT && python3 -m src.loop.self_healing; bash"
tmux new-window     -t $SESSION -n trainer "cd $ROOT && python3 -m src.loop.trainer; bash"
tmux new-window     -t $SESSION -n dream   "cd $ROOT && python3 -m src.loop.dream; bash"
tmux new-window     -t $SESSION -n shell   "cd $ROOT; bash"

echo ""
echo "[+] ALL SYSTEMS ONLINE"
echo "[+] Dashboard  → http://localhost:5001"
echo "[+] Daemon     → task execution + resonance learning"
echo "[+] Gateway    → REST API"
echo "[+] Healer     → failure recovery"
echo "[+] Trainer    → pattern learning"
echo "[+] Dream      → memory consolidation"
echo ""
sleep 2
tmux attach -t $SESSION
