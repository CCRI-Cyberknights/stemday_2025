import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# === Simulated Open Ports ===
GUIDED_FAKE_FLAGS = {
    8008: "CCRI-HPWG-2471",       # ✅ REAL FLAG
    8085: "SPBH-PRLY-2652",       # fake
    8041: "QXIB-SDLD-3531",       # fake
    8093: "RHVF-5083-REDP",       # fake
    8091: "PUDU-3694-OVCX",       # fake
}
GUIDED_JUNK_RESPONSES = {
    8030: "503 Service Unavailable\nTry again later.",
    8036: "DEBUG: Connection established successfully.",
    8046: "Python HTTP Server: directory listing not allowed.",
    8056: "Error 418: I’m a teapot.",
    8057: "Server under maintenance.\nPlease retry later.",
    8059: "Welcome to Experimental IoT Server (beta build).",
    8066: "ERROR 400: Bad request syntax.",
    8072: "<html><body><h1>It works!</h1><p>Apache2 default page.</p></body></html>"
}
GUIDED_SERVICE_NAMES = {
    8008: "auth-service",
    8030: "update-agent",
    8036: "metricsd",
    8041: "alpha-core",
    8046: "theta-daemon",
    8056: "kappa-node",
    8057: "sysmon-api",
    8059: "configd",
    8066: "zeta-cache",
    8072: "delta-sync",
    8085: "beta-hub",
    8091: "omega-stream",
    8093: "delta-proxy"
}
SOLO_FAKE_FLAGS = {
    9075: "CCRI-OODF-7185",       # ✅ REAL FLAG
    9025: "TIYL-DFJI-9727",       # fake
    9068: "GIPX-6007-BVEQ",       # fake
    9034: "KYCS-VOKV-5770",       # fake
    9001: "DEAY-TNAD-5867",       # fake
}
SOLO_JUNK_RESPONSES = {
    9008: "Python HTTP Server: directory listing not allowed.",
    9010: "Hello World!\nTest endpoint active.",
    9033: "💡 Tip: Scan only the ports you really need.",
    9035: "Welcome to Dev HTTP Server v1.3\nPlease login to continue.",
    9036: "ERROR 400: Bad request syntax.",
    9038: "403 Forbidden: You don’t have permission to access this resource.",
    9040: "Welcome to Dev HTTP Server v1.3\nPlease login to continue.",
    9049: "403 Forbidden: You don’t have permission to access this resource.",
    9050: "Error 418: I’m a teapot.",
    9091: "💡 Tip: Scan only the ports you really need.",
    9092: "💻 Dev API v0.1 — POST requests only.",
    9096: "💡 Tip: Scan only the ports you really need."
}
SOLO_SERVICE_NAMES = {
    9001: "kappa-node",
    9008: "configd",
    9010: "epsilon-sync",
    9025: "metricsd",
    9033: "beta-hub",
    9034: "alpha-core",
    9035: "zeta-cache",
    9036: "sysmon-api",
    9038: "lambda-api",
    9040: "gamma-relay",
    9049: "delta-sync",
    9050: "update-agent",
    9068: "theta-daemon",
    9075: "update-agent",
    9091: "delta-proxy",
    9092: "omega-stream",
    9096: "auth-service"
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