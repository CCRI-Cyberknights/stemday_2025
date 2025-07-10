#!/bin/bash

clear
echo "🧪 Challenge #09 – Fix the Flag! (Bash Edition)"
echo "==============================================="
echo
echo "📄 You found a broken Bash script! Here’s what it looks like:"
echo

# Display the script contents as a code block
cat << 'EOF'
#!/bin/bash

part1=900
part2=198

# MATH ERROR!
code=$((part1 - part2))

echo "Your flag is: CCRI-SCRP-$code"
EOF

echo
echo "==============================================="

# Check for broken_flag.sh
if [[ ! -f broken_flag.sh ]]; then
    echo "❌ ERROR: missing required file 'broken_flag.sh'."
    read -p "Press ENTER to close this terminal..." junk
    exit 1
fi

# Explain
echo "🧐 The original script tries to calculate a flag code by subtracting two numbers."
echo "⚠️ But the result isn’t in the correct 4-digit format!"
echo
read -p "Press ENTER to run the script and see what happens..." junk

echo
echo "💻 Running: bash broken_flag.sh"
echo "----------------------------------------------"
bash broken_flag.sh
echo "----------------------------------------------"
echo
sleep 1
echo "😮 Uh-oh! That’s not a valid 4-digit flag code. The math must be wrong."
echo
sleep 0.5

# Interactive repair loop
while true; do
    echo "🛠️  Your task: Fix the broken line in the script."
    echo
    echo "    code=\$((part1 - part2))"
    echo
    echo "👉 Which operator should we use instead of '-' to calculate the flag?"
    echo "   Choices: +   -   *   /"
    read -p "Enter your choice: " op
    echo

    case "$op" in
        "+")
            echo "✅ Correct! Adding the two parts together gives us the proper flag code."
            sleep 0.5
            echo "🔧 Updating the script with '+'..."
            # Use a robust sed that handles whitespace
            sed -i 's/code=.*part1 - part2.*/code=$((part1 + part2))/' broken_flag.sh

            echo
            echo "🎉 Re-running the fixed script..."
            flag_output=$(bash broken_flag.sh | grep "CCRI-SCRP")

            echo "----------------------------------------------"
            echo "$flag_output"
            echo "----------------------------------------------"
            echo "📄 Flag saved to: flag.txt"
            echo "$flag_output" > flag.txt
            echo
            read -p "🎯 Copy the flag and enter it in the scoreboard when ready. Press ENTER to finish..." junk
            break
            ;;
        "-")
            echo "❌ That’s still the original mistake. Subtracting gives: CCRI-SCRP-$((900 - 198))"
            ;;
        "*")
            echo "❌ Nope! Multiplying gives: CCRI-SCRP-$((900 * 198)) (way too big!)."
            ;;
        "/")
            echo "❌ Not quite! Dividing gives: CCRI-SCRP-$((900 / 198)) (too small)."
            ;;
        *)
            echo "❌ Invalid choice. Use one of: +  -  *  /"
            continue
            ;;
    esac

    echo
    echo "🧠 That result isn’t correct. Try another operator!"
    echo
done

# Clean exit for web hub
exec $SHELL
