# stemday2025
STEM Day VM

Parrot Linux Home Edition with just installed tools for interaction, no sudo on non-admin account.

Folder structure is a Desktop folder where the kids will interact with some things to read and then the scripts will simulate either some short prompts for information or just run a "this is what would happen but visualize it for your benefit" in a game sense.

Once the script runs there will be 5 choices of flags, which the script will also export into a separate text file for easier copy/paste purposes.

Kids will paste the flag into the verification offline html file, the correct answers of which are generated in a python script that obfuscates the correct flag in base64 and further xor encrypted, since we’re showing them how to base64 decode, and the VM has internet access.

The VM runs off a script that starts the VM and waits for a shutdown signal to then reset to a given snapshot for the next group of students. There is an exit file on the desktop that is password protected with the admin password to exit the loop, since all the VirtualBox UI elements are removed, the host key will be non-default and the only way out of it would be to ctrl-alt-delete (something we can’t bypass).
