#!/bin/bash

clear
echo "🔓 Hashcat ChainCrack Demo"
echo "==============================="
echo
echo "📂 Hashes to crack:     hashes.txt"
echo "📖 Wordlist to use:     wordlist.txt"
echo "📦 Encrypted segments:  segments/part*.zip"
echo
echo "🎯 Goal: Crack all 3 hashes, unlock 3 ZIP segment files, decode them, and reassemble the flag!"
echo
echo "💡 What’s happening here?"
echo "   ➡️ Hashcat will match words from the wordlist to hash values (like solving digital locks)."
echo "   ➡️ Each cracked hash unlocks a ZIP segment file."
echo "   ➡️ Segments contain base64-encoded data we'll need to decode and stitch together."
echo
read -p "Press ENTER to begin cracking the hashes..." junk

# --- Pre-flight checks ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || { echo "❌ Failed to change to script directory: $SCRIPT_DIR"; exit 1; }

HASHES="$SCRIPT_DIR/hashes.txt"
WORDLIST="$SCRIPT_DIR/wordlist.txt"
POTFILE="$SCRIPT_DIR/hashcat.potfile"
SEGMENTS="$SCRIPT_DIR/segments"
EXTRACTED="$SCRIPT_DIR/extracted"
DECODED_SEGMENTS="$SCRIPT_DIR/decoded_segments"
ASSEMBLED="$SCRIPT_DIR/assembled_flag.txt"

if [[ ! -f "$HASHES" || ! -f "$WORDLIST" ]]; then
    echo "❌ ERROR: Required files hashes.txt or wordlist.txt are missing."
    read -p "Press ENTER to close this terminal..."
    exit 1
fi

if [[ ! -d "$SEGMENTS" ]]; then
    echo "❌ ERROR: Segments folder is missing."
    read -p "Press ENTER to close this terminal..."
    exit 1
fi

# Clean up any old results
echo
echo "[🧹] Clearing previous Hashcat outputs and decoded data..."
rm -f "$POTFILE" "$ASSEMBLED"
rm -rf "$EXTRACTED" "$DECODED_SEGMENTS"
mkdir -p "$EXTRACTED" "$DECODED_SEGMENTS"

# Explain hashcat
echo
echo "🛠️ Behind the Scenes: Hashcat Command"
echo "-------------------------------------------"
echo "hashcat -m 0 -a 0 hashes.txt wordlist.txt"
echo
echo "   -m 0 = MD5 hash mode"
echo "   -a 0 = dictionary attack (uses wordlist.txt)"
echo "   --potfile-path = where cracked hashes are stored"
echo
read -p "Press ENTER to launch Hashcat..." junk

# Run hashcat
hashcat -m 0 -a 0 "$HASHES" "$WORDLIST" --potfile-path "$POTFILE" --force >/dev/null 2>&1

echo
echo "[✅] Hashcat finished cracking. Cracked hashes:"
grep -Ff "$HASHES" "$POTFILE" | while IFS=: read -r hash pass; do
    echo "🔓 $hash : $pass"
done

# Proceed to segment extraction
echo
read -p "Press ENTER to extract and decode encrypted ZIP segments..." junk

# Mapping hashes to zip files
declare -A hash_to_file
hash_to_file["4e14b4bed16c945384faad2365913886"]="part1.zip"  # brightmail
hash_to_file["ceabb18ea6bbce06ce83664cf46d1fa8"]="part2.zip"  # letacla
hash_to_file["08f5b04545cbf7eaa238621b9ab84734"]="part3.zip"  # Password12

# Extract segments and decode
grep -Ff "$HASHES" "$POTFILE" | while IFS=: read -r hash pass; do
    zipfile="${hash_to_file[$hash]}"
    if [[ -z "$zipfile" ]]; then
        echo "❌ No ZIP mapping found for hash: $hash"
        continue
    fi

    echo
    echo "🔑 Unlocking $zipfile with password: $pass"
    unzip -P "$pass" "$SEGMENTS/$zipfile" -d "$EXTRACTED" >/dev/null 2>&1

    segment_file=$(unzip -P "$pass" -l "$SEGMENTS/$zipfile" | awk '{print $4}' | grep -i 'encoded_segment' | head -n 1 | xargs basename)
    segfile="$EXTRACTED/$segment_file"

    if [[ -f "$segfile" ]]; then
        echo "✅ Extracted encoded segment: $segment_file"
        echo "ℹ️  This file uses Base64 encoding. Let's decode it to reveal the real content."
        sleep 0.5

        decoded_file="$DECODED_SEGMENTS/decoded_${segment_file%.txt}.txt"
        echo
        echo "🔽 Decoding Base64 with: base64 --decode $segfile"
        sleep 0.5
        base64 --decode "$segfile" > "$decoded_file" 2>/dev/null

        if [[ -s "$decoded_file" ]]; then
            echo "📄 Decoded → $decoded_file"
            echo "-----------------------------"
            cat "$decoded_file"
            echo "-----------------------------"
        else
            echo "⚠️  Decoding failed for: $segfile"
        fi
    else
        echo "❌ Segment file not found in $zipfile"
    fi
    echo
done

# Assemble flag from decoded segments
echo
echo "🧩 Reassembling final flag..."
sleep 1
if [[ -f "$DECODED_SEGMENTS/decoded_encoded_segments1.txt" && \
      -f "$DECODED_SEGMENTS/decoded_encoded_segments2.txt" && \
      -f "$DECODED_SEGMENTS/decoded_encoded_segments3.txt" ]]; then

    rm -f "$ASSEMBLED"
    for i in {1..5}; do
        part1=$(sed -n "${i}p" "$DECODED_SEGMENTS/decoded_encoded_segments1.txt")
        part2=$(sed -n "${i}p" "$DECODED_SEGMENTS/decoded_encoded_segments2.txt")
        part3=$(sed -n "${i}p" "$DECODED_SEGMENTS/decoded_encoded_segments3.txt")
        flag="${part1}-${part2}-${part3}"
        echo "- $flag" | tee -a "$ASSEMBLED"
    done

    echo
    echo "✅ All candidate flags saved to: $ASSEMBLED"
else
    echo "❌ One or more decoded segments are missing. Cannot assemble final flags."
fi

echo
read -p "🔎 Review the candidate flags above. Only ONE matches the CCRI format: CCRI-AAAA-1111
Press ENTER to close this terminal..." junk
exec $SHELL
