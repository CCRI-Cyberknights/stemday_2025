🕵️ Challenge 08: Fake Auth Log Investigation

You've recovered a suspicious-looking system log named auth.log.

It contains hundreds of fake SSH login records — but somewhere within the noise, one line hides a real flag. The trick? Some of the log entries have weird-looking process IDs (PIDs) that don’t follow normal number formatting. Only one of them is a valid CCRI flag.

Your mission:

    Run investigate_authlog.sh in the terminal.

    The script will scan the log and flag suspicious entries for you.

    Use the guided prompts to examine the log and uncover anomalies.

    Identify the correct flag in this format: CCRI-AAAA-1111

🧠 Tip: Not all strange-looking entries are real. Only one matches the agency’s standard. Trust the format — not the noise.
