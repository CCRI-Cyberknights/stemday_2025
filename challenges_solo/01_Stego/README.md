# Challenge 1: Steganography decode  
---
Steganography is the art of the concealment of information and messages inside of another file like embedding a text file inside an image or mp3 so it appears unchanged to the average person. Unlike encryption the aim is to make the data invisible but readable to the target.

---
During the Knights investigation into the CryptKeepers a suspicious image was found among the files that appeared normal at first, but our analysts believe it contains hidden data.

## Objective:
  uncover and decode squirrel.jpg to extract the embedded secret messages they concealed inside this picture. 

## Investigator's Journal: 
  Cryptkeepers operatives often hide things in plain sight... and they tend to reuse the same password across tools. Not all of these tools will reveal useful information, some may lead to dead ends. The challenge lies in experimenting and connecting the dots. Does the image contain metadata or embedded content? Are there readable strings or hidden files inside? Might a password be needed to reveal the payload?.Sometimes the best secrets are the ones hiding in plain sight.  

---

##  Tools & Techniques

Try out some of these Linux tools each reveals different kinds of secrets:

| Tool      | Use Case                                              | Example Command                      |
|-----------|--------------------------------------------------------|--------------------------------------|
| `strings` | View readable text inside binary files                | `strings squirrel.jpg | less`       |
| `exiftool`| Inspect metadata (camera info, author, hidden tags)   | `exiftool squirrel.jpg`              |
| `binwalk` | Detect and extract embedded files                     | `binwalk -e squirrel.jpg`            |
| `zsteg`   | Analyze LSB steganography in PNGs (JPG support limited)| `zsteg squirrel.jpg *(may not work here)*` |
| `steghide`| Embed/extract files using a passphrase                | `steghide extract -sf squirrel.jpg`  |
| `file`    | Check file type and structure                         | `file squirrel.jpg`                  |
| `xxd`     | View raw hex data                                     | `xxd squirrel.jpg | less`           |

> Tip: Use `man` or `--help` with any command to learn more.

---

## Files in This Folder

* `squirrel.jpg` — The suspicious image

All flags follow the same format: CCRI-AAAA-1111 Replace AAAA and the numbers with the code found.Then Input the flag into the website to verify the answer.  

---

 