# Challenge 6: Hashcat ChainCrack Challenge

This challenge combines multiple skills: Hash Cracking- MD5 hashes are outdated and vulnerable. Tools like Hashcat can rapidly test passwords against them. ZIP Decryption- password-protected ZIP segments must be unlocked using the cracked passwords. Base64 Decoding- Each ZIP contains Base64-encoded content. Flag Reassembly- After decoding, you'll need to piece the segments back together to identify the real flag.

Cryptkeeper operatives encrypted a message and split it into parts. Each part is locked behind a password, and each password is hidden inside an MD5 hash.  
 You've recovered:

- `hashes.txt`: 3 password hashes  
- `wordlist.txt`: Possible passwords  
- `segments/`: Three ZIP archives (one per password)

## Objective: 
Examine the files 
Crack the hashes using a hash cracking tool.
Use the recovered passwords to extract each ZIP archive. Decode each extracted file using Base64. 
Reassemble the decoded outputs to form possible flags.  

## Investigator’s Journal: 
Three parts. Three locks. Three keys hidden in plain sight. They were sloppy enough to leave the hashes all you need to do is match them to the right keys. Once inside, the truth is scattered across the fragments. You’ll need to chain together several techniques crack, extract, decode, and reconstruct to reveal the hidden message. Each archive, once unlocked, contains a scrambled part of a flag. Crack the hashes, extract and decode the segments, and reassemble the true flag. 

---

## Tools & Techniques

Here’s a selection of tools that may help you complete each phase:

| Phase               | Tool         | Example Use Case / Command                                          |
|--------------------|--------------|---------------------------------------------------------------------|
| Crack MD5 Hashes    | `hashcat`    | `hashcat -m 0 -a 0 hashes.txt wordlist.txt`                         |
|                    | `john` + `--format=raw-md5` | Alternative cracking approach                                 |
| Extract ZIPs       | `unzip`      | `unzip -P password segments/part1.zip`                              |
| Base64 Decoding    | `base64`     | `base64 --decode decoded_file.txt`                                  |
| Reassemble Segments| `cat` or script | Concatenate decoded parts and review them                           |

> Tip: Order matters when reassembling the flag. The decoded parts likely correspond to different sections of the flag.

---

##  Files in This Folder

* `hashes.txt` — List of MD5 hashes to crack
* `wordlist.txt` — Potential password candidates
* `segments/` — Folder containing 3 encrypted ZIP files (part1.zip, part2.zip, part3.zip)

All flags follow the same format: CCRI-AAAA-1111 Replace AAAA and the numbers with the code you uncover Input the flag into the website to verify the answer. 

--- 