🧠 Challenge #06 – Hashcat ChainCrack
-------------------------------------

Your mission is to recover the final agency flag by:

  1. Cracking multiple MD5 hashes with Hashcat.
  2. Using each cracked password to “unlock” a segment.
  3. Decoding the base64-encoded segment.
  4. Assembling the parts into the final flag.

Files in this folder:
  • hashes.txt              ← MD5 hashes (one per line)
  • wordlist.txt            ← Possible plaintexts for Hashcat
  • segments/part1.zip      ← Encrypted ZIP containing segment1.txt
  • segments/part2.zip      ← …segment2.txt
  • segments/part3.zip      ← …segment3.txt
  • run_chain_crack.sh      ← Guided Bash script

🔧 Tool: hashcat (mode 0: MD5, attack 0: straight)

🚀 Let’s see how chaining multiple cracks can reveal a bigger secret!
