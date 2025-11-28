# 🖥️ Challenge 15: Process Inspection

Cryptkeepers operatives have deployed a covert process on a compromised system to quietly exfiltrate sensitive information.
You’ve intercepted a full snapshot of the system's running processes.

Some of them look completely ordinary.
Some, however, contain extra command-line arguments that feel… suspicious.

Cyber threat actors often bury their payloads in plain sight.
A good analyst knows to inspect everything — even the boring stuff — until something jumps out.

---

## 🧩 Your Objective

Find the **one rogue process** that contains a valid flag in its command-line arguments.

### What to Look For

* Scan the process snapshot for tools or commands that seem out of place.
* Focus on **long command strings** — especially any referencing:

  * `flag`
  * `upload`
  * `proxy`
  * `tunnel`
  * anything that feels “not standard”

Decoys may look convincing, but only **one** string uses the correct **CCRI flag format**.

> 🔎 **Tip:**
> The real flag is passed in as a `--flag=` argument to a suspicious binary.
> Look for tools that *don’t* belong on a normal system.

---

## 🛠 Tools & Techniques

| Tool / Command                            | Purpose                                        |
| ----------------------------------------- | ---------------------------------------------- |
| `less ps_dump.txt`                        | Page through the entire process snapshot       |
| `grep "CCRI-" ps_dump.txt"`               | Narrow down potential flags by prefix          |
| `grep -E "[A-Z]{4}-[0-9]{4}" ps_dump.txt` | Broader match for any flag-like patterns       |
| `grep "tunneler" ps_dump.txt"`            | Investigate suspicious binaries used by Cryptkeepers |
| `awk '{print $11,$12,$13,...}'`           | Extract command-line fields                    |
| `cut -d" " -f11-`                         | Slice off the command portion of each line     |

---

## 📂 Files in This Folder

* `ps_dump.txt` — Full snapshot of the system’s running processes.

---

## 🏁 Flag Format

All flags follow the official format:

**`CCRI-AAAA-1111`**

Replace `AAAA` and the digits with the correct values you uncover.
Then enter the flag into the website to verify your answer.