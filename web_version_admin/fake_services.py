import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# === Simulated Open Ports ===
GUIDED_FAKE_FLAGS = {
    8061: "CCRI-ZUEZ-3786",       # ✅ REAL FLAG
    8044: "ZAJA-7753-AKJX",       # fake
    8020: "DEMM-3965-YPBC",       # fake
    8035: "UDJV-LOSD-8248",       # fake
    8047: "YFAT-UOYZ-0754",       # fake
}
GUIDED_JUNK_RESPONSES = {
    8002: "💻 Dev API v0.1 — POST requests only.",
    8023: "503 Service Unavailable\nTry again later.",
    8030: "Error 418: I’m a teapot.",
    8038: "503 Service Unavailable\nTry again later.",
    8042: "Python HTTP Server: directory listing not allowed.",
    8045: "💻 Dev API v0.1 — POST requests only.",
    8046: "ERROR 400: Bad request syntax.",
    8049: "System maintenance in progress.",
    8062: "🔒 Unauthorized: API key required.",
    8064: "Python HTTP Server: directory listing not allowed.",
    8078: "Error 418: I’m a teapot."
}
GUIDED_SERVICE_NAMES = {
    8002: "beta-hub",
    8020: "auth-service",
    8023: "alpha-core",
    8030: "lambda-api",
    8035: "gamma-relay",
    8038: "delta-sync",
    8042: "update-agent",
    8044: "metricsd",
    8045: "kappa-node",
    8046: "delta-proxy",
    8047: "sysmon-api",
    8049: "omega-stream",
    8061: "theta-daemon",
    8062: "configd",
    8064: "zeta-cache",
    8078: "epsilon-sync"
}
SOLO_FAKE_FLAGS = {
    9073: "CCRI-GQZB-4817",       # ✅ REAL FLAG
    9048: "GFMR-PRFX-7389",       # fake
    9036: "ZFAU-3624-YDOA",       # fake
    9046: "MQVP-ULXK-7722",       # fake
    9025: "ITOK-5144-JDNW",       # fake
}
SOLO_JUNK_RESPONSES = {
    9005: "<html><body><h1>It works!</h1><p>Apache2 default page.</p></body></html>",
    9014: "🔒 Unauthorized: API key required.",
    9040: "💡 Tip: Scan only the ports you really need.",
    9055: "Server under maintenance.\nPlease retry later.",
    9068: "Hello World!\nTest endpoint active.",
    9080: "System maintenance in progress.",
    9085: "System maintenance in progress.",
    9098: "403 Forbidden: You don’t have permission to access this resource."
}
SOLO_SERVICE_NAMES = {
    9005: "alpha-core",
    9014: "metricsd",
    9025: "delta-proxy",
    9036: "omega-stream",
    9040: "zeta-cache",
    9046: "lambda-api",
    9048: "epsilon-sync",
    9055: "delta-sync",
    9068: "update-agent",
    9073: "theta-daemon",
    9080: "sysmon-api",
    9085: "configd",
    9098: "kappa-node"
}

GUIDED_ALL_PORTS = {**GUIDED_JUNK_RESPONSES, **GUIDED_FAKE_FLAGS}
SOLO_ALL_PORTS = {**SOLO_JUNK_RESPONSES, **SOLO_FAKE_FLAGS}

# === Dynamic HTTP Handler Factory ===
def PortHandlerFactory(response_map, service_map):
    class CustomPortHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            response = response_map.get(self.server.server_port, "Connection refused")
            service_name = service_map.get(self.server.server_port, "http")
            banner = f"👋 Welcome to {service_name} Service\n\n"
            self.send_response(200)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.send_header("Server", service_name)
            self.send_header("X-Service-Name", service_name)
            self.end_headers()
            try:
                self.wfile.write((banner + response).encode("utf-8"))
            except BrokenPipeError:
                pass

        def log_message(self, format, *args):
            return
    return CustomPortHandler

def start_fake_service(port, response_map, service_map):
    try:
        server = HTTPServer(('0.0.0.0', port), PortHandlerFactory(response_map, service_map))
        threading.Thread(target=server.serve_forever, daemon=True).start()
        print(f"🚁️  Simulated service running on port {port} ({service_map.get(port, 'http')})")
    except OSError as e:
        print(f"❌ Could not bind port {port}: {e}")

def start_all_services(available_modes):
    """Starts fake services based on which modes are available."""
    if "regular" in available_modes:
        for port in GUIDED_ALL_PORTS.keys():
            start_fake_service(port, GUIDED_ALL_PORTS, GUIDED_SERVICE_NAMES)

    if "solo" in available_modes:
        for port in SOLO_ALL_PORTS.keys():
            start_fake_service(port, SOLO_ALL_PORTS, SOLO_SERVICE_NAMES)