#!/bin/bash

clear
echo "🔓 Hashcat ChainCrack Demo"
echo "==========================="
echo
echo "Hashes to crack: hashes.txt"
echo "Wordlist:        wordlist.txt"
echo "Segments in:     segments/part*.zip"
echo

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HASHES="$SCRIPT_DIR/hashes.txt"
WORDLIST="$SCRIPT_DIR/wordlist.txt"
POTFILE="$SCRIPT_DIR/hashcat.potfile"
SEGMENTS="$SCRIPT_DIR/segments"
EXTRACTED="$SCRIPT_DIR/extracted"
ASSEMBLED="$SCRIPT_DIR/assembled_flag.txt"
DECODED_SEGMENTS="$SCRIPT_DIR/decoded_segments"

# Map hash to segment zip
declare -A hash_to_file
hash_to_file["e99a18c428cb38d5f260853678922e03"]="part1.zip"  # abc123
hash_to_file["0d107d09f5bbe40cade3de5c71e9e9b7"]="part2.zip"  # letmein
hash_to_file["2ab96390c7dbe3439de74d0c9b0b1767"]="part3.zip"  # hunter2

echo -e "\n[🧹] Clearing previous Hashcat cache and outputs..."
rm -f "$POTFILE" "$ASSEMBLED"
rm -rf "$EXTRACTED" "$DECODED_SEGMENTS"
mkdir -p "$EXTRACTED" "$DECODED_SEGMENTS"

read -p "Press ENTER to launch Hashcat and crack all hashes..." junk

echo "[⚙️] Running Hashcat dictionary attack..."
hashcat -m 0 -a 0 "$HASHES" "$WORDLIST" --potfile-path "$POTFILE" --force >/dev/null 2>&1

echo -e "\n[✅] Cracking complete. Results:"
grep -Ff "$HASHES" "$POTFILE" | while IFS=: read -r hash pass; do
    echo "$hash:$pass"
done
echo

# Extract and decode all segments
grep -Ff "$HASHES" "$POTFILE" | while IFS=: read -r hash pass; do
    zipfile="${hash_to_file[$hash]}"
    if [[ -z "$zipfile" ]]; then
        echo "❌ No zip mapping found for hash: $hash"
        continue
    fi

    echo "🔑 Using password for hash $hash → $pass"
    echo "📦 Extracting $SEGMENTS/$zipfile..."

    rm -rf "$EXTRACTED"/*
    unzip -P "$pass" "$SEGMENTS/$zipfile" -d "$EXTRACTED" >/dev/null 2>&1

    segment_file=$(unzip -P "$pass" -l "$SEGMENTS/$zipfile" | awk '{print $4}' | grep -i 'segment' | head -n 1)
    segfile="$EXTRACTED/$segment_file"

    if [[ -f "$segfile" ]]; then
        echo "✅ $(basename "$segfile") recovered."

        echo -e "\n📦 Raw Base64 from $(basename "$segfile"):"
        echo "--------------------"
        cat "$segfile"
        echo -e "\n--------------------"

        echo -n "🔽 Decoding: "
        for i in {1..20}; do echo -n "█"; sleep 0.03; done
        echo

        decoded=$(base64 --decode "$segfile" 2>/dev/null)
        if [[ -n "$decoded" ]]; then
            segnum=$(echo "$segfile" | grep -oE 'segment([0-9]+)\.txt' | grep -oE '[0-9]+')
            echo "$decoded" > "$DECODED_SEGMENTS/decoded_segment$segnum.txt"
        fi
    else
        echo "❌ Failed to recover segment from $zipfile"
    fi

    echo
done

# Assemble final flag in segment order
echo "🧩 Final Assembled Flag:"
echo "---------------------------"

rm -f "$ASSEMBLED"
touch "$ASSEMBLED"

first=1
for seg in $(ls "$DECODED_SEGMENTS"/decoded_segment*.txt 2>/dev/null | sort -V); do
    part=$(cat "$seg")
    if [[ $first -eq 1 ]]; then
        echo -n "$part" >> "$ASSEMBLED"
        first=0
    else
        echo -n "-$part" >> "$ASSEMBLED"
    fi
done

if [[ -s "$ASSEMBLED" ]]; then
    cat "$ASSEMBLED"
    echo -e "\n---------------------------"
    echo "✅ Flag saved to: $ASSEMBLED"
else
    echo "❌ No decoded segments were saved."
fi

echo
read -p "Press ENTER to close this terminal..." junk
