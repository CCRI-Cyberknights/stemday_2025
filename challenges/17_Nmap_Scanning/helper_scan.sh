#!/bin/bash
clear
echo "🛰️ Nmap Scan Puzzle"
echo "--------------------------------------"
echo "Several simulated services are running locally (inside your CTF app)."
echo
echo "🎯 Your goal: Scan localhost (127.0.0.1) for open ports in the range 8000–8100, and find the REAL flag."
echo "⚠️ Some ports contain random junk responses. Only one flag is correct."
echo
echo "🔧 Under the hood:"
echo "   We'll use 'nmap' to scan the ports and see what services respond."
echo "   Then you'll connect to each open port with 'curl' to check for hidden flags."
echo

read -p "Press ENTER to begin your scan..." junk

# Run nmap and capture raw results
echo
echo "📡 Running: nmap -sV --version-light -p8000-8100 localhost"
raw_scan=$(nmap -sV --version-light -p8000-8100 localhost)

# Map ports to simulated service names
declare -A port_services
port_services=(
  [8001]="dev-http"
  [8004]="flag-api"
  [8009]="secure-api"
  [8015]="maintenance"
  [8020]="apache"
  [8023]="flag-api"
  [8028]="debug-service"
  [8033]="help-service"
  [8039]="http"
  [8045]="maintenance"
  [8047]="flag-api"
  [8051]="iot-server"
  [8058]="http"
  [8064]="dev-api"
  [8072]="flag-api"
  [8077]="secure-api"
  [8083]="http"
  [8089]="test-service"
  [8095]="flag-api"
  [8098]="maintenance"
)

# Pretty print the scan results
echo
echo "📝 Nmap Scan Results:"
echo "--------------------------------------"
echo "$raw_scan" | while IFS= read -r line; do
    if [[ "$line" =~ ^8[0-9]{3}/tcp[[:space:]]+open ]]; then
        port=$(echo "$line" | awk '{split($1,p,"/"); print p[1]}')
        service="${port_services[$port]:-unknown}"
        printf "%-9s %-5s %-15s %s\n" "$port/tcp" "open" "$service" "CustomSim/1.0"
    else
        echo "$line"
    fi
done

echo
echo "✅ Scan complete."
echo
read -p "📖 Review the scan results above. Press ENTER to explore the open ports interactively..." junk

# Extract list of open ports
mapfile -t open_ports < <(echo "$raw_scan" | awk '/open/{split($1,p,"/"); print p[1]}')

# Check if any ports were found
if [[ "${#open_ports[@]}" -eq 0 ]]; then
    echo "❌ No open ports found in the range 8000–8100."
    read -p "Press ENTER to exit..." junk
    exit 1
fi

# Interactive exploration
while true; do
    clear
    echo "--------------------------------------"
    echo "Open ports detected:"
    for i in "${!open_ports[@]}"; do
        port="${open_ports[$i]}"
        service="${port_services[$port]:-unknown}"
        printf "%2d. %s (%s)\n" $((i+1)) "$port" "$service"
    done
    echo "$(( ${#open_ports[@]} + 1 )). Exit"
    echo

    read -p "Select a port to explore (1-$(( ${#open_ports[@]} + 1 ))): " choice

    if [[ "$choice" -ge 1 && "$choice" -le "${#open_ports[@]}" ]]; then
        port="${open_ports[$((choice-1))]}"
        service="${port_services[$port]:-unknown}"
        echo
        echo "🌐 Connecting to http://localhost:$port ..."
        echo "Service: $service"
        echo "--------------------------------------"
        response=$(curl -s http://localhost:$port)

        if [[ -z "$response" ]]; then
            echo "❌ No response received from port $port."
        else
            echo "$response"
        fi

        echo "--------------------------------------"
        echo

        # Offer to save response
        while true; do
            echo "Options:"
            echo "1. 🔁 Return to port list"
            echo "2. 💾 Save this response to nmap_flag_response.txt"
            echo

            read -p "Choose an option (1-2): " sub_choice
            if [[ "$sub_choice" == "1" ]]; then
                break
            elif [[ "$sub_choice" == "2" ]]; then
                out_file="nmap_flag_response.txt"
                {
                    echo "Port: $port"
                    echo "Service: $service"
                    echo "Response:"
                    echo "$response"
                    echo "--------------------------------------"
                } >> "$out_file"
                echo "✅ Response saved to $out_file"
                sleep 1
                break
            else
                echo "❌ Invalid choice. Please select 1 or 2."
            fi
        done

    elif [[ "$choice" -eq $(( ${#open_ports[@]} + 1 )) ]]; then
        echo "👋 Exiting helper. Return to the CTF portal to submit your flag."
        break
    else
        echo "❌ Invalid choice. Please select a valid port."
        sleep 1
    fi
done

exit 0
