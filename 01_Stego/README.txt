🕵️ Stego Decode Challenge
-------------------------

Your mission is to extract a secret flag hidden inside an image file.

But this flag isn’t in the visible part of the image — you won’t see it by just opening the picture. Instead, it’s been embedded in the raw data of the file using a technique called:

    Steganography

That means the image looks completely normal, but it secretly contains a message hidden beneath the surface — invisible to the eye.

🔧 A tool called `steghide` can extract that message — but only if you provide the correct password.

What to do:
1. Double-click the `extract_flag.sh` script in this folder.
2. When prompted, choose **“Run in Terminal”**.
3. Try guessing the password.
   💡 Hint: it’s the most common password in the world.

If you get it right, the hidden flag will be revealed and saved to `flag.txt`.

🏁 Flag format: CCRI-XXX-###

