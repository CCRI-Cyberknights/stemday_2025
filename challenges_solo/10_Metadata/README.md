# 🧠 Challenge 10: Metadata Mystery

You’ve recovered a suspicious image file: `capybara.jpg`.

At first glance it seems harmless — just a goofy capybara. But appearances can be deceiving. Investigators believe someone embedded a flag inside the image's metadata, where it won’t show up just by opening the file.

---

## 🧠 What Is Metadata?

Metadata is “data about data.” In images, metadata can include things like:

- Camera model and lens
- Author and comments
- Creation date and GPS location

...and sometimes, secrets.

Cybercriminals often hide sensitive or incriminating details in the metadata fields, knowing they’re rarely checked by casual viewers.

---

## 🛠 Tools & Techniques

Here are some helpful commands for analyzing metadata:

| Tool       | Purpose                                      |
|------------|----------------------------------------------|
| `exiftool` | Inspect or edit metadata from media files    |
| `strings`  | Search for readable text in any file         |
| `identify` | Basic image info from ImageMagick suite      |
| `grep`     | Filter specific fields from metadata dumps   |

> 💡 Some metadata fields are rarely used — and perfect for hiding things.

---

## 📝 Challenge Instructions

1. Use `exiftool` (or a similar tool) to examine the metadata in `capybara.jpg`.  
2. Look for anything resembling a flag — but be cautious!  
3. This image contains **four fake flags** and **one real one**. Only the correct one follows the agency’s format and feels authentic.

⚠️ Just because something *looks* like a flag doesn’t mean it’s real. Metadata lies.

When you’re confident you've found the real one, save it like this:

```bash
echo "CCRI-AAAA-1111" > flag.txt
````

---

## 📂 Files in This Folder

* `capybara.jpg` – Image file hiding something important.

---

## 🏁 Flag Format

The valid flag will match this format:

**CCRI-AAAA-1111**

Replace `AAAA` and `1111` with the actual values you uncover.

---

🎯 Sometimes the most revealing information isn’t in the image — it’s in the silence between pixels.
