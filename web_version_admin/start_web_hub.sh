#!/bin/bash
# start_web_hub.sh - Launch the CTF student hub

echo "🚀 Starting the CCRI CTF Student Hub..."
cd "$(dirname "$0")" || exit 1

# Check if Flask server is already running on port 5000
if lsof -i:5000 >/dev/null 2>&1; then
    echo "🌐 Web server already running on port 5000."
else
    echo "🌐 Starting web server on port 5000..."
    if [ -f "server.pyc" ]; then
        nohup python3 server.pyc >/dev/null 2>&1 &
    else
        nohup python3 server.py >/dev/null 2>&1 &
    fi
    sleep 2  # Give it a moment to start
fi

echo
echo "📡 Note: All simulated ports (8000–8100) for Nmap scanning are handled *inside* the CTF hub."
echo "         You don’t need to start any additional services."

# Launch Firefox to the hub (reuse window if already running)
if pgrep -x "firefox" >/dev/null 2>&1; then
    echo "🦊 Firefox already running. Opening new tab..."
    firefox --new-tab http://localhost:5000 >/dev/null 2>&1 &
else
    echo "🦊 Launching Firefox to http://localhost:5000..."
    firefox http://localhost:5000 >/dev/null 2>&1 &
fi

echo
echo "✅ CCRI CTF Student Hub is ready!"
