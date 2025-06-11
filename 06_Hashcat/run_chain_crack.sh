#!/bin/bash

clear
echo "🔓 Hashcat ChainCrack Demo"
echo "==========================="
echo
echo "📂 Hashes to crack:     hashes.txt"
echo "📖 Wordlist to use:     wordlist.txt"
echo "📦 Encrypted segments:  segments/part*.zip"
echo
echo "🧠 Goal: Crack all 3 hashes, unlock 3 segment files, decode them, and reassemble the flag!"
echo
echo "🔧 Quick Note:"
echo "   Hashcat is a password recovery tool that cracks hashes using known words."
echo "   We'll match words from the wordlist to hash values — like solving a digital lock."
echo
read -p "Press ENTER to begin Hashcat cracking..." junk

echo -e "\n[🧹] Clearing previous Hashcat outputs and decoded data..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || { echo "❌ Failed to change to script directory: $SCRIPT_DIR"; exit 1; }

HASHES="$SCRIPT_DIR/hashes.txt"
WORDLIST="$SCRIPT_DIR/wordlist.txt"
POTFILE="$SCRIPT_DIR/hashcat.potfile"
SEGMENTS="$SCRIPT_DIR/segments"
EXTRACTED="$SCRIPT_DIR/extracted"
ASSEMBLED="$SCRIPT_DIR/assembled_flag.txt"
DECODED_SEGMENTS="$SCRIPT_DIR/decoded_segments"

rm -f "$POTFILE" "$ASSEMBLED"
rm -rf "$EXTRACTED" "$DECODED_SEGMENTS"
mkdir -p "$EXTRACTED" "$DECODED_SEGMENTS"

echo -e "\n[⚙️] Running: hashcat -m 0 -a 0 hashes.txt wordlist.txt"
echo "   -m 0 = MD5 hash mode"
echo "   -a 0 = dictionary attack (wordlist-based)"
echo "   --potfile-path stores cracked results"
read -p "Press ENTER to launch Hashcat..." junk

hashcat -m 0 -a 0 "$HASHES" "$WORDLIST" --potfile-path "$POTFILE" --force >/dev/null 2>&1

echo -e "\n[✅] Cracking complete! Here's what we found:"
grep -Ff "$HASHES" "$POTFILE" | while IFS=: read -r hash pass; do
    echo "🔓 $hash : $pass"
done

echo
read -p "Press ENTER to extract and decode the encrypted ZIP segments..." junk

declare -A hash_to_file
hash_to_file["4e14b4bed16c945384faad2365913886"]="part1.zip"  # brightmail
hash_to_file["ceabb18ea6bbce06ce83664cf46d1fa8"]="part2.zip"  # letacla
hash_to_file["08f5b04545cbf7eaa238621b9ab84734"]="part3.zip"  # Password12

grep -Ff "$HASHES" "$POTFILE" | while IFS=: read -r hash pass; do
    zipfile="${hash_to_file[$hash]}"
    if [[ -z "$zipfile" ]]; then
        echo "❌ No zip mapping found for hash: $hash"
        continue
    fi

    echo "🔑 Using cracked password '$pass' for $zipfile"
    echo "📦 Extracting: $SEGMENTS/$zipfile"
    unzip -P "$pass" "$SEGMENTS/$zipfile" -d "$EXTRACTED" >/dev/null 2>&1

    segment_file=$(unzip -P "$pass" -l "$SEGMENTS/$zipfile" | awk '{print $4}' | grep -i 'encoded_segment' | head -n 1 | xargs basename)
    segfile="$EXTRACTED/$segment_file"

    if [[ -f "$segfile" ]]; then
        echo "✅ Found encoded segment: $segment_file"
        echo "ℹ️  This file uses Base64 — a way to represent binary data in text. Let's decode it to get the actual content."
        sleep 1

        decoded_file="$DECODED_SEGMENTS/decoded_${segment_file%.txt}.txt"
        echo -e "🔽 Decoding with: base64 --decode $segfile"
        echo -n "   Progress: ["
        for i in {1..24}; do
            echo -n "█"
            sleep 0.05
        done
        echo "]"

        base64 --decode "$segfile" > "$decoded_file" 2>/dev/null

        if [[ -s "$decoded_file" ]]; then
            echo "📄 Decoded → $decoded_file"
            echo
            echo "🧾 Decoded Content:"
            echo "-----------------------------"
            cat "$decoded_file"
            echo "-----------------------------"
        else
            echo "⚠️  Failed to decode: $segfile"
        fi
    else
        echo "❌ Segment file not found in $zipfile"
    fi

    echo
    sleep 1

done

echo "🧩 Reassembling flag from decoded segments..."
echo
seg1_file="$DECODED_SEGMENTS/decoded_encoded_segments1.txt"
seg2_file="$DECODED_SEGMENTS/decoded_encoded_segments2.txt"
seg3_file="$DECODED_SEGMENTS/decoded_encoded_segments3.txt"

if [[ -f "$seg1_file" && -f "$seg2_file" && -f "$seg3_file" ]]; then
    mapfile -t seg1 < "$seg1_file"
    mapfile -t seg2 < "$seg2_file"
    mapfile -t seg3 < "$seg3_file"

    rm -f "$ASSEMBLED"
    echo "🔧 Each decoded segment file contains 5 candidate parts."
    echo "   We'll stitch together each line: part1-part2-part3 to form 5 full flags."
    echo
    for i in {0..4}; do
        flag="${seg1[$i]}-${seg2[$i]}-${seg3[$i]}"
        echo "- $flag" | tee -a "$ASSEMBLED"
    done
    echo
    echo "✅ All 5 flags saved to: $ASSEMBLED"
else
    echo "❌ One or more decoded segment files are missing. Cannot assemble final flags."
fi

echo
read -p "🔎 Review the flags above. Only ONE matches the CCRI format: CCRI-AAAA-1111
Press ENTER to close this terminal..." junk
