#!/bin/bash
echo "🛑 Stopping CCRI CTF Student Hub..."
pkill -f server.py && echo "✅ Server stopped." || echo "⚠️ No server running."
