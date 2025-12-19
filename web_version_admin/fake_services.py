import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# === Simulated Open Ports ===
GUIDED_FAKE_FLAGS = {
    8078: "CCRI-RUMD-7387",       # ✅ REAL FLAG
    8081: "LGQR-9085-OBZQ",       # fake
    8030: "RCKB-9463-NHYY",       # fake
    8045: "LXBA-8980-YRJE",       # fake
    8093: "EQKN-LLMG-7856",       # fake
}
GUIDED_JUNK_RESPONSES = {
    8014: "Server under maintenance.\nPlease retry later.",
    8042: "<html><body><h1>It works!</h1><p>Apache2 default page.</p></body></html>",
    8049: "503 Service Unavailable\nTry again later.",
    8059: "🔒 Unauthorized: API key required.",
    8064: "Hello World!\nTest endpoint active.",
    8083: "💡 Tip: Scan only the ports you really need.",
    8090: "Python HTTP Server: directory listing not allowed.",
    8097: "💻 Dev API v0.1 — POST requests only."
}
GUIDED_SERVICE_NAMES = {
    8014: "omega-stream",
    8030: "metricsd",
    8042: "delta-proxy",
    8045: "epsilon-sync",
    8049: "auth-service",
    8059: "gamma-relay",
    8064: "configd",
    8078: "sysmon-api",
    8081: "update-agent",
    8083: "lambda-api",
    8090: "theta-daemon",
    8093: "alpha-core",
    8097: "kappa-node"
}
SOLO_FAKE_FLAGS = {
    9070: "CCRI-MOZI-1661",       # ✅ REAL FLAG
    9029: "IJIG-WEDW-2842",       # fake
    9006: "HZOM-5036-OWVM",       # fake
    9077: "OFVK-7278-GQBM",       # fake
    9054: "XQOD-ZPGW-6121",       # fake
}
SOLO_JUNK_RESPONSES = {
    9000: "💻 Dev API v0.1 — POST requests only.",
    9004: "403 Forbidden: You don’t have permission to access this resource.",
    9005: "Python HTTP Server: directory listing not allowed.",
    9020: "503 Service Unavailable\nTry again later.",
    9025: "System maintenance in progress.",
    9027: "Python HTTP Server: directory listing not allowed.",
    9029: "omega-stream", # (Key moved to flags but name kept here for mapping)
    9033: "Welcome to Dev HTTP Server v1.3\nPlease login to continue.",
    9057: "💻 Dev API v0.1 — POST requests only.",
    9078: "💡 Tip: Scan only the ports you really need.",
    9088: "System maintenance in progress.",
    9097: "503 Service Unavailable\nTry again later."
}
SOLO_SERVICE_NAMES = {
    9000: "kappa-node",
    9004: "alpha-core",
    9005: "delta-proxy",
    9006: "delta-sync",
    9020: "zeta-cache",
    9025: "beta-hub",
    9027: "configd",
    9029: "omega-stream",
    9033: "metricsd",
    9054: "epsilon-sync",
    9057: "gamma-relay",
    9070: "auth-service",
    9077: "update-agent",
    9078: "theta-daemon",
    9088: "lambda-api",
    9097: "sysmon-api"
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