#!/bin/bash
# start_web_hub.sh - Launch the CTF student hub

echo "🚀 Starting the CCRI CTF Student Hub..."
cd "$(dirname "$0")" || exit 1

# === Check if Flask server is already running on port 5000 ===
if lsof -i:5000 >/dev/null 2>&1; then
    echo "🌐 Web server already running on port 5000."
    flask_running=true
else
    echo "🌐 Starting web server on port 5000..."
    flask_running=false
    if [ -f "server.pyc" ]; then
        nohup python3 server.pyc >/dev/null 2>&1 &
    else
        nohup python3 server.py >/dev/null 2>&1 &
    fi
    sleep 2  # Give it a moment to start
fi

# === Check if any ports 8000–8100 are already in use ===
ports_in_use=0
for port in $(seq 8000 8100); do
    if lsof -iTCP:$port -sTCP:LISTEN >/dev/null 2>&1; then
        ports_in_use=$((ports_in_use + 1))
    fi
done

if [[ $ports_in_use -gt 0 ]]; then
    echo "🛰️ Simulated services on ports 8000–8100 are already running ($ports_in_use ports bound)."
else
    if [ "$flask_running" = true ]; then
        echo "⚠️ Flask is running but no simulated services detected on ports 8000–8100."
        echo "   (These are started by server.py when the hub launches.)"
    else
        echo "🛰️ Simulated services on ports 8000–8100 will be started by the Flask server."
    fi
fi

echo
echo "📡 Note: All simulated ports (8000–8100) for Nmap scanning are handled *inside* the CTF hub."
echo "         You don’t need to start any additional services."

# === Wait for Flask server to respond before launching browser ===
echo "⏳ Waiting for web server to start..."
for i in {1..10}; do
    if curl -s http://localhost:5000 >/dev/null 2>&1; then
        echo "🌐 Web server is up!"
        break
    else
        sleep 1
    fi
done

# === Launch browser to the hub ===
export DISPLAY=:0

if command -v xdg-open >/dev/null 2>&1; then
    echo "🌐 Opening default browser to http://localhost:5000..."
    setsid xdg-open http://localhost:5000 >/dev/null 2>&1 &
else
    echo "🦊 Opening Firefox to http://localhost:5000..."
    setsid firefox http://localhost:5000 >/dev/null 2>&1 &
fi

echo
echo "✅ CCRI CTF Student Hub is ready!"

# === Keep script alive for a moment to avoid launcher killing child processes ===
sleep 2
