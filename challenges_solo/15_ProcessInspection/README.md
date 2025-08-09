# 🖥️ Challenge 15: Process Inspection

Liber8 operatives have deployed a covert process on a compromised system to quietly exfiltrate sensitive information.

You’ve intercepted a full snapshot of the system's running processes.

Some of them look completely ordinary.  
Some, however, have extra arguments that feel... suspicious.

---

## 🎯 Your Mission

Find the one rogue process that contains a valid flag in its command-line arguments.

The flag will be in this format:

**CCRI-AAAA-1111**

All others are decoys — using wrong prefixes, altered spacing, or subtle typos to fool you.

---

## 🛠 Suggested Tactics

| Tool/Command                                          | Purpose                                                |
|-------------------------------------------------------|--------------------------------------------------------|
| `less ps_dump.txt`                                    | Page through the entire process snapshot               |
| `grep "CCRI-" ps_dump.txt`                            | Narrow down potential flags by prefix                  |
| `grep -E "[A-Z]{4}-[0-9]{4}" ps_dump.txt`             | Broader match for any flag-like strings                |
| `grep "tunneler" ps_dump.txt`                         | Investigate specific tools or binaries used by Liber8  |
| `awk '{print $11,$12,$13,...}'`                       | Extract command-line columns from each process         |
| `cut -d" " -f11-`                                      | Slice off the command portion of each line             |

💡 The real flag is passed in as a `--flag=` argument to a suspicious binary.  
Look for tools that sound like they don’t belong on a normal system.

---

## 📝 Analyst Strategy

1. Scan the snapshot and look for tools or command lines that seem out of place.
2. Focus on long command strings — especially anything referencing “flag”, “upload”, “proxy”, “tunnel”, etc.
3. Decoys may look convincing, but remember: **only one string uses the correct CCRI format**.

---

## 🗂️ Files in This Folder

- `ps_dump.txt` – Full snapshot of the system’s processes.

---

## 🏁 Flag Format

The authentic flag will always match this structure:

**CCRI-AAAA-1111**

If you're confident you’ve found it, save it with:

```
echo "CCRI-AAAA-1111" > flag.txt
```

Replace `AAAA-1111` with what you discover.

---

## 🧠 Final Thought

Cyber threat actors often bury their payloads in plain sight.
A good analyst knows to inspect **everything** — even the boring stuff — until something jumps out.

Good hunting.
