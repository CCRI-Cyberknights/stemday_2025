#!/bin/bash
echo "🛑 Stopping CCRI CTF Student Hub..."
pkill -f server.pyc && echo "✅ Server stopped." || echo "⚠️ No server running."
