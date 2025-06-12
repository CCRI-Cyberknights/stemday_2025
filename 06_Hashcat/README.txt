🔓 Challenge 06: Hashcat ChainCrack

You’ve intercepted 3 encrypted archive segments — each one locked behind a password that isn’t given. But someone also left behind a hashes.txt file full of MD5 hashes and a wordlist.txt of likely passwords.

This means the passwords are hidden — in plain sight — if you can crack them.

Your mission:

    Run the guided script: run_chain_crack.sh

    It will use Hashcat to crack all 3 hashes using the provided wordlist.

    Each cracked password will unlock one ZIP segment.

    Each segment contains base64-encoded data.

    The script decodes each segment and assembles them into 5 possible flags.

Only one of the 5 follows the correct agency format: CCRI-AAAA-1111

📁 Files in this folder:
• hashes.txt ← 3 MD5 hashes to crack
• wordlist.txt ← Possible password candidates
• segments/ ← Folder with 3 encrypted ZIPs
• run_chain_crack.sh ← Your interactive cracking assistant

🧠 Tip: Watch how each successful crack gets you closer to the final goal. Cracking alone doesn’t solve the case — you’ll need to decode and assemble too!
