#!/bin/bash
# stop_web_hub.sh - Stop the CCRI CTF Hub cleanly (project-root aware)

echo "🛑 Stopping CCRI CTF Hub..."

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
    echo "❌ ERROR: Could not find .ccri_ctf_root marker. Are you inside the CTF folder?" >&2
    exit 1
}

PROJECT_ROOT="$(find_project_root)"

# === Detect mode: Admin vs Student ===
if [[ -d "$PROJECT_ROOT/web_version_admin" ]]; then
    echo "🛠️  Admin/Dev mode detected (web_version_admin found)."
    SERVER_FILE="$PROJECT_ROOT/web_version_admin/server.py"
    SERVER_FILEC="$PROJECT_ROOT/web_version_admin/server.pyc"
else
    echo "🎓 Student mode detected (web_version_admin not found)."
    SERVER_FILE="$PROJECT_ROOT/web_version/server.pyc"
fi

# === Safer process kill ===
echo "🔍 Searching for running server processes..."
for file in "$SERVER_FILE" "$SERVER_FILEC"; do
    if [[ -f "$file" ]]; then
        pids=$(pgrep -f "python3.*$file")
        if [[ -n "$pids" ]]; then
            echo "⚠️ Found server process(es) for $file: $pids"
            read -p "❓ Kill these processes? [y/N]: " confirm
            if [[ "$confirm" =~ ^[Yy]$ ]]; then
                echo "$pids" | xargs kill -9
                echo "✅ Killed server process(es) for $file."
            else
                echo "🚫 Skipping kill for $file."
            fi
        else
            echo "⚠️ No server process found for $file."
        fi
    fi
done

# === Kill Flask on port 5000 ===
if command -v lsof >/dev/null 2>&1; then
    if lsof -i:5000 >/dev/null 2>&1; then
        echo "🔪 Killing processes on port 5000..."
        lsof -ti:5000 | xargs -r kill -9
        echo "✅ Port 5000 cleared."
    else
        echo "⚠️ No processes found on port 5000."
    fi
else
    echo "⚠️ WARNING: 'lsof' not found. Skipping port cleanup."
fi

# === Kill simulated services on ports 8000–8100 ===
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

echo
echo "🎯 All cleanup complete."
