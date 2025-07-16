#!/bin/bash
clear

echo "📡 PCAP Investigation Tool"
echo "=============================="
echo
echo "You've intercepted network traffic in: traffic.pcap"
echo "Inside are **hundreds** of TCP streams between hosts — it’s noisy!"
echo
echo "🎯 Goal: Investigate the traffic and identify the REAL flag."
echo "⚠️ Four streams contain fake flags. Only ONE has the real flag (CCRI-AAAA-1111 format)."
echo
echo "🔧 Under the hood:"
echo "   1️⃣ We'll use 'tshark' to extract all TCP streams."
echo "   2️⃣ Then, we’ll scan them for flag-like patterns."
echo "   3️⃣ You’ll review candidate streams interactively."
echo
read -p "Press ENTER to begin analyzing traffic..." junk

# --- Check prerequisites ---
echo
echo "📦 Checking for tshark installation..."
if ! command -v tshark >/dev/null 2>&1; then
    echo "❌ ERROR: tshark is not installed or not in PATH."
    echo "Install it first (sudo apt install tshark) to continue."
    read -p "Press ENTER to exit..."
    exit 1
fi
echo "✅ tshark found!"
sleep 0.5

echo
echo "📂 Checking for traffic.pcap file..."
if [[ ! -f traffic.pcap ]]; then
    echo "❌ ERROR: traffic.pcap not found in this folder!"
    read -p "Press ENTER to exit..."
    exit 1
fi
echo "✅ traffic.pcap found!"
sleep 0.5

# Prepare notes file
OUTFILE="pcap_notes.txt"
rm -f "$OUTFILE"

# --- Extract TCP streams ---
echo
echo "🔍 Extracting unique TCP streams from the capture..."
mapfile -t all_streams < <(tshark -r traffic.pcap -Y 'tcp' -T fields -e tcp.stream | sort -u)
stream_count=${#all_streams[@]}

echo "✅ Found $stream_count TCP streams in the capture."
echo "📖 Example: Stream IDs range from ${all_streams[0]} to ${all_streams[-1]}"
echo "-----------------------------------------"
sleep 1

# --- Explain search step ---
echo
echo "🔎 Next, we’ll scan all streams for **flag-like patterns**."
echo "   This helps us skip unrelated traffic like pings, DNS queries, etc."
echo "   (Searching for patterns like AAAA-BBBB-1234 or AAAA-1234-BBBB)"
echo
read -p "Press ENTER to begin scanning streams..." junk

# --- Spinner function ---
spinner() {
    local delay=0.1
    local spinstr='|/-\'
    while :; do
        for i in $(seq 0 3); do
            printf "\r🔎 Scanning streams for flags... %s" "${spinstr:$i:1}"
            sleep $delay
        done
    done
}

# Start spinner
spinner &
SPINNER_PID=$!

# Search for flag-like payloads
flag_streams=()
pattern1='[A-Z]{4}-[A-Z]{4}-[0-9]{4}'
pattern2='[A-Z]{4}-[0-9]{4}-[A-Z]{4}'
for sid in "${all_streams[@]}"; do
    if tshark -r traffic.pcap -Y "tcp.stream==$sid" -T fields -e tcp.payload 2>/dev/null | \
       xxd -r -p 2>/dev/null | strings | grep -E -q "$pattern1|$pattern2"; then
        flag_streams+=("$sid")
        printf "\n🔎 Found potential flag in Stream ID: %s\n" "$sid"
    fi
done

# Stop spinner
kill "$SPINNER_PID" >/dev/null 2>&1
wait "$SPINNER_PID" 2>/dev/null
printf "\r✅ Scan complete.                                      \n"

# --- No flags found ---
if [[ "${#flag_streams[@]}" -eq 0 ]]; then
    echo "❌ No flag-like patterns found in any stream."
    read -p "Press ENTER to exit..."
    exit 1
fi

echo
echo "✅ Found ${#flag_streams[@]} stream(s) with flag-like patterns."
echo
read -p "📖 Press ENTER to review candidate streams interactively..." junk

# --- Interactive review ---
while true; do
    clear
    echo "-----------------------------------------"
    echo "📜 Flag Candidate Streams:"
    for i in "${!flag_streams[@]}"; do
        echo "$((i+1)). Stream ID: ${flag_streams[$i]}"
    done
    echo "$(( ${#flag_streams[@]} + 1 )). Exit"
    echo

    read -p "Select a stream to view (1-${#flag_streams[@]}): " choice

    if [[ "$choice" -ge 1 && "$choice" -le "${#flag_streams[@]}" ]]; then
        sid="${flag_streams[$((choice-1))]}"
        clear
        echo "🔗 Stream ID: $sid"
        echo "-----------------------------------------"

        # Show endpoints
        tshark -r traffic.pcap -Y "tcp.stream==$sid" -T fields \
            -e frame.number -e ip.src -e tcp.srcport -e ip.dst -e tcp.dstport | head -n 1 | \
            awk '{printf "📨 From: %s:%s\n📬 To: %s:%s\n", $2, $3, $4, $5}'

        echo
        echo "📝 Payload Preview:"
        tshark -r traffic.pcap -qz follow,tcp,ascii,$sid 2>/dev/null
        echo "-----------------------------------------"

        # Save option
        while true; do
            echo "Options:"
            echo "1) 🔁 Return to candidate list"
            echo "2) 💾 Save this stream’s summary to $OUTFILE"
            echo "3) 🚪 Exit tool"
            read -p "Choose an option (1-3): " sub_choice

            case "$sub_choice" in
                1) break ;;
                2)
                    echo "🔖 Saving stream $sid summary..."
                    {
                        echo "🔗 Stream ID: $sid"
                        tshark -r traffic.pcap -Y "tcp.stream==$sid" -T fields \
                            -e ip.src -e tcp.srcport -e ip.dst -e tcp.dstport | head -n 1 | \
                            awk '{printf "📨 From: %s:%s\n📬 To: %s:%s\n", $1, $2, $3, $4}'
                        echo "Payload:"
                        tshark -r traffic.pcap -qz follow,tcp,ascii,$sid 2>/dev/null
                        echo "-----------------------------------------"
                    } >> "$OUTFILE"
                    echo "✅ Saved to $OUTFILE"
                    sleep 1
                    ;;
                3)
                    echo "👋 Exiting tool."
                    exit 0
                    ;;
                *)
                    echo "⚠️ Invalid choice. Please select 1-3."
                    ;;
            esac
        done
    elif [[ "$choice" -eq $(( ${#flag_streams[@]} + 1 )) ]]; then
        echo "👋 Exiting tool. Review your findings carefully."
        break
    else
        echo "⚠️ Invalid choice. Please select a valid number."
        sleep 1
    fi
done

echo
echo "🎉 Investigation complete!"
echo "📄 Your saved notes are in: $OUTFILE"
echo "🚀 Return to the CTF hub to submit the correct flag."
read -p "Press ENTER to close..."
