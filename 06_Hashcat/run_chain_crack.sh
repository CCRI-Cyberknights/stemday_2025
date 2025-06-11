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
hash_to_file["4e14b4bed16c945384faad2365913886"]="part1.zip"  # brightmail
hash_to_file["ceabb18ea6bbce06ce83664cf46d1fa8"]="part2.zip"  # letacla
hash_to_file["08f5b04545cbf7eaa238621b9ab84734"]="part3.zip"  # Password12

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

# Extract and decode all segment files
grep -Ff "$HASHES" "$POTFILE" | while IFS=: read -r hash pass; do
    zipfile="${hash_to_file[$hash]}"
    if [[ -z "$zipfile" ]]; then
        echo "❌ No zip mapping found for hash: $hash"
        continue
    fi

    echo "🔑 Using password for hash $hash → $pass"
    echo "📦 Extracting $SEGMENTS/$zipfile..."

    unzip -P "$pass" "$SEGMENTS/$zipfile" -d "$EXTRACTED" >/dev/null 2>&1

    segment_file=$(unzip -P "$pass" -l "$SEGMENTS/$zipfile" | awk '{print $4}' | grep -i 'encoded_segment' | head -n 1 | xargs basename)
    segfile="$EXTRACTED/$segment_file"

    if [[ -f "$segfile" ]]; then
        echo "✅ $(basename "$segfile") recovered."

        decoded_file="$DECODED_SEGMENTS/decoded_${segment_file%.txt}.txt"
        base64 --decode "$segfile" > "$decoded_file" 2>/dev/null

        if [[ -s "$decoded_file" ]]; then
            echo "📄 Decoded → $decoded_file"
        else
            echo "⚠️  Failed to decode: $segfile"
        fi
    else
        echo "❌ Segment file not found in $zipfile"
    fi

    echo
done

echo "🧩 Assembled Flag Candidates:"
echo "---------------------------"

seg1_file="$DECODED_SEGMENTS/decoded_encoded_segments1.txt"
seg2_file="$DECODED_SEGMENTS/decoded_encoded_segments2.txt"
seg3_file="$DECODED_SEGMENTS/decoded_encoded_segments3.txt"

if [[ -f "$seg1_file" && -f "$seg2_file" && -f "$seg3_file" ]]; then
    mapfile -t seg1 < "$seg1_file"
    mapfile -t seg2 < "$seg2_file"
    mapfile -t seg3 < "$seg3_file"

    rm -f "$ASSEMBLED"

    for i in {0..4}; do
        flag="${seg1[$i]}-${seg2[$i]}-${seg3[$i]}"
        echo "- $flag" | tee -a "$ASSEMBLED"
    done

    echo "---------------------------"
    echo "✅ All 5 flags saved to: $ASSEMBLED"
else
    echo "❌ Missing one or more decoded segment files."
fi

echo
read -p "Press ENTER to close this terminal..." junk
