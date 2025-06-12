import random
import datetime
import os

# Get script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(script_dir, "auth.log")

# Sample data
usernames = ["alice", "bob", "charlie", "dave", "eve"]
ip_addresses = [
    "192.168.1.10", "192.168.1.20", "10.0.0.5", "172.16.0.3", "203.0.113.42",
    "198.51.100.17", "192.0.2.91", "8.8.8.8", "127.0.0.1"
]
auth_methods = ["password", "publickey"]
flags = [
    "FLAG-NUL0-0000",
    "CCRI-LOGS-9310",
    "CODE-4NOM-7722",
    "AUTH-WARN-6633",
    "FAIL-2222-EXCP"
]

# Shuffle flags to ensure randomness
random.shuffle(flags)
used_flags = set()

# Select random lines to insert flags
lines = []
base_time = datetime.datetime.now()

flag_insertion_indices = sorted(random.sample(range(50, 230), len(flags)))
flag_index = 0

for i in range(250):
    timestamp = (base_time - datetime.timedelta(seconds=random.randint(0, 3600))).strftime("%b %d %H:%M:%S")
    user = random.choice(usernames)
    ip = random.choice(ip_addresses)
    method = random.choice(auth_methods)
    result = "Accepted" if random.random() > 0.2 else "Failed"

    # Insert fake or real flag PID at predetermined indices
    if flag_index < len(flag_insertion_indices) and i == flag_insertion_indices[flag_index]:
        pid = flags[flag_index]
        used_flags.add(pid)
        flag_index += 1
    else:
        pid = str(random.randint(1000, 99999))

    line = f"{timestamp} myhost sshd[{pid}]: {result} {method} for {user} from {ip} port {random.randint(1000, 65000)} ssh2"
    lines.append(line)

# Write to file
with open(log_path, "w") as f:
    f.write("\n".join(lines))

print(f"[✅] Fake auth.log written to {log_path}")
