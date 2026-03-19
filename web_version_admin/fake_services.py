import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# === Simulated Open Ports ===
GUIDED_FAKE_FLAGS = {
    8085: "CCRI-UWKT-1905",       # ✅ REAL FLAG
    8056: "DJRZ-SADS-4449",       # fake
    8018: "ANHG-ULJA-5510",       # fake
    8044: "GLZI-8601-HIEG",       # fake
    8030: "JFXW-THAJ-6456",       # fake
}
GUIDED_JUNK_RESPONSES = {
    8000: "🔒 Unauthorized: API key required.",
    8003: "System maintenance in progress.",
    8012: "503 Service Unavailable\nTry again later.",
    8016: "Hello World!\nTest endpoint active.",
    8017: "💻 Dev API v0.1 — POST requests only.",
    8023: "System maintenance in progress.",
    8026: "System maintenance in progress.",
    8051: "Python HTTP Server: directory listing not allowed.",
    8053: "Hello World!\nTest endpoint active.",
    8069: "DEBUG: Connection established successfully.",
    8084: "Python HTTP Server: directory listing not allowed.",
    8092: "Hello World!\nTest endpoint active."
}
GUIDED_SERVICE_NAMES = {
    8000: "epsilon-sync",
    8003: "beta-hub",
    8012: "update-agent",
    8016: "auth-service",
    8017: "theta-daemon",
    8018: "delta-proxy",
    8023: "configd",
    8026: "alpha-core",
    8030: "metricsd",
    8044: "lambda-api",
    8051: "zeta-cache",
    8053: "sysmon-api",
    8056: "delta-sync",
    8069: "kappa-node",
    8084: "gamma-relay",
    8085: "beta-hub",
    8092: "omega-stream"
}
SOLO_FAKE_FLAGS = {
    9015: "CCRI-LFSB-7333",       # ✅ REAL FLAG
    9024: "LHTK-1221-CNNQ",       # fake
    9075: "PAGS-AVZP-3923",       # fake
    9034: "OUJF-VQKM-7629",       # fake
    9094: "MNXZ-SZKI-1612",       # fake
}
SOLO_JUNK_RESPONSES = {
    9016: "💻 Dev API v0.1 — POST requests only.",
    9025: "Python HTTP Server: directory listing not allowed.",
    9035: "Error 418: I’m a teapot.",
    9040: "Welcome to Experimental IoT Server (beta build).",
    9047: "Welcome to Experimental IoT Server (beta build).",
    9076: "💡 Tip: Scan only the ports you really need.",
    9081: "Hello World!\nTest endpoint active.",
    9085: "Hello World!\nTest endpoint active."
}
SOLO_SERVICE_NAMES = {
    9015: "metricsd",
    9016: "delta-sync",
    9024: "lambda-api",
    9025: "theta-daemon",
    9034: "configd",
    9035: "sysmon-api",
    9040: "alpha-core",
    9047: "kappa-node",
    9075: "zeta-cache",
    9076: "update-agent",
    9081: "auth-service",
    9085: "omega-stream",
    9094: "gamma-relay"
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