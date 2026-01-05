# 🖥️ Challenge 15: Process Inspection

**Mission Briefing:**
CryptKeepers operatives have deployed a covert process on a compromised system to quietly exfiltrate sensitive information.
We were unable to capture the malware itself, but we managed to grab a **Process Snapshot** (`ps_dump.txt`) just before the connection closed.
Somewhere in that list of running programs is a rogue agent executing a command with the flag passed as an argument.

## 🧠 Intelligence Report
* **The Concept:** **Process Listing**. Every program running on a computer (browser, system clock, malware) is a "process."
* **The Vulnerability:** **Command Line Arguments**. When a program is launched, it often takes arguments (e.g., `python3 script.py --password=SECRET`). On Linux, these arguments are visible to anyone who lists the running processes. 
* **The Strategy:** We need to scan the "COMMAND" column of the snapshot for suspicious activity or sensitive strings.

## 📝 Investigator’s Journal
*Notes from the field:*

> "A good analyst looks at the boring stuff. This file is just a text dump of the `ps aux` command.
>
> Most of it is standard system noise—kernel threads, web servers, cron jobs. You need to look for the anomaly.
>
> I've seen these guys use custom tools like `tunneler` or `exfil_tool`. They are sloppy; they often pass the flag directly into the command using a flag like `--token=` or `--flag=`. Grep is your best friend here."

## 📂 Files in This Folder
* `ps_dump.txt` — A text file containing the snapshot of running processes.

---

## 🛠 Tools & Techniques

You are analyzing a static text file that *represents* system activity.

| Tool | Purpose | Usage Example |
| :--- | :--- | :--- |
| **grep** | The fastest way to find the needle. Filter for the flag format directly. | `grep "CCRI-" ps_dump.txt` |
| **less -S** | View the file manually. The `-S` flag prevents lines from wrapping, making it easier to read wide process lists. | `less -S ps_dump.txt` |
| **awk** | Advanced. Print only the Command column (usually the last column). | `awk '{print $11}' ps_dump.txt` |

> 💡 **Tip:** A normal process looks like this:
> `root  123  0.0  0.1  /usr/sbin/sshd -D`
>
> A suspicious process might look like this:
> `user  999  1.5  2.0  ./malware --target=10.0.0.1 --flag=CCRI-XXXX`

---

## 🏁 Flag Format
**`CCRI-AAAA-1111`**

Search the process dump and identify the rogue command.