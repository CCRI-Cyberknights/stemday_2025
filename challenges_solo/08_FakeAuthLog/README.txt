# 🕵️ Challenge 08: Fake Auth Log Investigation

You’ve intercepted a suspicious system log: `auth.log`.

It looks like a normal SSH activity log... except something’s off. Among the login entries is a hidden flag, disguised in plain sight.

---

## 🧠 What’s Going On?

System logs like `auth.log` record login attempts, user authentication, and session activity. But logs can be noisy — especially on compromised systems where attackers might try to blend false entries in with real ones.

Sometimes the trick isn’t *what’s* in the log, but *where*.

---

## 🛠 Tools & Techniques

Here are some tools commonly used to slice and search through log files:

| Tool       | Use Case                                           | Example Command                                |
|------------|----------------------------------------------------|------------------------------------------------|
| `grep`     | Search for text patterns in log entries            | `grep sshd auth.log`                           |
| `awk`      | Extract structured fields like usernames or PIDs   | `awk '{print $5}' auth.log`                    |
| `less`     | Scroll and inspect large log files interactively   | `less auth.log`                                |
| `head`     | Preview the beginning of a file                    | `head auth.log`                                |
| `grep -E`  | Use regular expressions for smarter filtering      | `grep -E 'CCRI-[A-Z0-9]{4}-[0-9]{4}' auth.log` |

> 💡 Tip: SSH logs often follow this format:
> `sshd[PID]: Accepted/Failed ... from IP ...`

Can you spot something unusual about the PIDs?

---

## 🧩 Investigator’s Journal

🗒️ *“The log was filled with noise, but I noticed the patterns didn’t make sense. Some process IDs looked... off. Not numeric. That’s where I started digging.”*

---

## 📝 Your Objective

1. Explore the `auth.log` file.
2. Look for login entries with strange or non-numeric process IDs.
3. Use tools like `grep` or `awk` to narrow your search.
4. One line contains a hidden flag that fits the agency format.

To capture your finding:

```bash
echo "CCRI-AAAA-1111" > flag.txt
````

---

## 📂 Files in This Folder

* `auth.log` – Simulated log file for forensic analysis.

---

## 🏁 Flag Format

The correct flag will match this format:

**CCRI-AAAA-1111**

Replace `AAAA` and `1111` with the correct values you uncover.

---

🔎 Trust your instincts and follow the clues in the logs — sometimes the system tells more than it means to.
