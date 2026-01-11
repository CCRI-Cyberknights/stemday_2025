import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# === Simulated Open Ports ===
GUIDED_FAKE_FLAGS = {
    8036: "CCRI-VRCW-0314",       # ✅ REAL FLAG
    8056: "EVCP-DZRP-6977",       # fake
    8067: "FGMG-8495-YEMT",       # fake
    8035: "NHYZ-6213-LSFM",       # fake
    8015: "OCCU-VXPZ-2219",       # fake
}
GUIDED_JUNK_RESPONSES = {
    8004: "System maintenance in progress.",
    8038: "Error 418: I’m a teapot.",
    8046: "<html><body><h1>It works!</h1><p>Apache2 default page.</p></body></html>",
    8057: "Server under maintenance.\nPlease retry later.",
    8077: "403 Forbidden: You don’t have permission to access this resource.",
    8085: "Welcome to Experimental IoT Server (beta build).",
    8088: "Hello World!\nTest endpoint active.",
    8091: "Error 418: I’m a teapot."
}
GUIDED_SERVICE_NAMES = {
    8004: "delta-sync",
    8015: "update-agent",
    8035: "configd",
    8036: "omega-stream",
    8038: "gamma-relay",
    8046: "sysmon-api",
    8056: "zeta-cache",
    8057: "delta-proxy",
    8067: "auth-service",
    8077: "metricsd",
    8085: "beta-hub",
    8088: "lambda-api",
    8091: "theta-daemon"
}
SOLO_FAKE_FLAGS = {
    9021: "CCRI-LWUT-6974",       # ✅ REAL FLAG
    9043: "PBVS-VVLZ-2464",       # fake
    9028: "EZWA-4564-YJXB",       # fake
    9032: "PJXJ-VCBS-0886",       # fake
    9080: "UELY-HFVK-9631",       # fake
}
SOLO_JUNK_RESPONSES = {
    9008: "Server under maintenance.\nPlease retry later.",
    9040: "System maintenance in progress.",
    9046: "System maintenance in progress.",
    9065: "Error 418: I’m a teapot.",
    9076: "Hello World!\nTest endpoint active.",
    9077: "System maintenance in progress.",
    9086: "Error 418: I’m a teapot.",
    9096: "Error 418: I’m a teapot."
}
SOLO_SERVICE_NAMES = {
    9008: "theta-daemon",
    9021: "update-agent",
    9028: "configd",
    9032: "auth-service",
    9040: "delta-proxy",
    9043: "metricsd",
    9046: "epsilon-sync",
    9065: "lambda-api",
    9076: "gamma-relay",
    9077: "delta-sync",
    9080: "zeta-cache",
    9086: "beta-hub",
    9096: "sysmon-api"
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