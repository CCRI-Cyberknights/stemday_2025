#!/bin/bash
# stop_web_hub.sh - Stop the CCRI CTF Student Hub cleanly (project-root aware)

echo "🛑 Stopping CCRI CTF Student Hub..."

# === Helper: Find Project Root ===
find_project_root() {
    local dir="$PWD"
    while [[ "$dir" != "/" ]]; do
        if [[ -f "$dir/.ccri_ctf_root" ]]; then
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    echo "❌ ERROR: Could not find .ccri_ctf_root marker. Are you inside the CTF repo?" >&2
    exit 1
}

# === Resolve project directories ===
PROJECT_ROOT="$(find_project_root)"
WEB_ADMIN_DIR="$PROJECT_ROOT/web_version_admin"

# === Kill server.pyc and server.py processes in this repo ===
echo "🔍 Searching for server.pyc and server.py processes..."
pkill -f "$WEB_ADMIN_DIR/server.pyc" 2>/dev/null && echo "✅ Killed server.pyc" || echo "⚠️ No server.pyc process running."
pkill -f "$WEB_ADMIN_DIR/server.py"  2>/dev/null && echo "✅ Killed server.py"  || echo "⚠️ No server.py process running."

# === Check prerequisites ===
if ! command -v lsof >/dev/null 2>&1; then
    echo "⚠️ WARNING: 'lsof' not found. Cannot check ports. Skipping port cleanup."
    exit 0
fi

# === Kill any Flask/Gunicorn processes on port 5000 ===
if lsof -i:5000 >/dev/null 2>&1; then
    echo "🔪 Killing processes on port 5000..."
    lsof -ti:5000 | xargs -r kill -9
    echo "✅ Port 5000 cleared."
else
    echo "⚠️ No processes found on port 5000."
fi

# === Kill all simulated services on ports 8000–8100 ===
ports_killed=0
for port in $(seq 8000 8100); do
    if lsof -iTCP:$port -sTCP:LISTEN >/dev/null 2>&1; then
        lsof -tiTCP:$port -sTCP:LISTEN | xargs -r kill -9
        ports_killed=$((ports_killed + 1))
    fi
done

if [[ $ports_killed -gt 0 ]]; then
    echo "✅ Cleared $ports_killed simulated service(s) on ports 8000–8100."
else
    echo "⚠️ No simulated services running on ports 8000–8100."
fi

echo "🎯 All cleanup complete."
