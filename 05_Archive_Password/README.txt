🔐 Challenge 05: ZIP File Crack & Decode
----------------------------------------

You’ve recovered a mysterious ZIP archive named `secret.zip`.

It’s password-protected — and the password isn’t obvious. Fortunately, you’ve also found a wordlist with possible passwords (`wordlist.txt`), but only one of them works.

Inside the archive is a **base64-encoded** message file with multiple potential flags. Only one of them matches the agency format.

Your mission:
  1. Run `crack_zip.sh` in the terminal.
  2. The script will try common passwords automatically.
  3. Once cracked, it will extract and decode the hidden message.
  4. Pick out the real flag: Format `CCRI-XXX-###`

🧠 Tip: Watch the wordlist scroll to see how brute-force tools operate!
