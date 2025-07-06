#!/bin/bash

clear
echo "🧪 Challenge #09 – Fix the Flag! (Bash Edition)"
echo "----------------------------------------------"
echo
echo "You found a broken Bash script! Here’s what it looks like:"
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
echo "----------------------------------------------"

# Check for broken_flag.sh
if [[ ! -f broken_flag.sh ]]; then
    echo "❌ ERROR: missing required file 'broken_flag.sh'."
    read -p "Press ENTER to close this terminal..." junk
    exit 1
fi

echo "Let’s run that script and see what happens:"
echo
bash broken_flag.sh
echo
echo "⚠️  Uh-oh! That’s not a 4-digit flag. The math must be wrong."
echo

# Loop until correct operator
while true; do
    echo "----------------------------------------------"
    echo "🛠️  Fix the broken line:"
    echo "    code=\$((part1 - part2))"
    echo
    echo "Which operator should we use instead of '-'?"
    echo "Choices: +   -   *   /"
    read -p "Enter your choice: " op
    echo "----------------------------------------------"

    case "$op" in
        "+")
            echo "✅ Correct! Updating the script..."

            # Use a robust sed that handles whitespace
            sed -i 's/code=.*part1 - part2.*/code=$((part1 + part2))/' broken_flag.sh

            echo
            echo "🎉 Re-running the fixed script..."
            flag_output=$(bash broken_flag.sh | grep "CCRI-SCRP")

            echo "$flag_output"
            echo "$flag_output" > flag.txt
            echo
            echo "📄 Flag saved to: flag.txt"
            echo
            read -p "Press ENTER to finish..." junk
            break
            ;;
        "-")
            echo "❌ Still wrong! That’s the original problem."
            result=$((900 - 198))
            ;;
        "*")
            echo "❌ Nope! That multiplies them."
            result=$((900 * 198))
            ;;
        "/")
            echo "❌ Not quite! That divides them."
            result=$((900 / 198))
            ;;
        *)
            echo "❌ Invalid choice. Use one of: +  -  *  /"
            continue
            ;;
    esac

    echo
    echo "If you used '$op', the result would be: CCRI-SCRP-$result"
    echo "That’s not the correct flag. Try again!"
    echo
done

# Clean exit for web hub
exec $SHELL
