#!/usr/bin/env python3

# This script should print: CCRI-SCRP-9881
# But someone broke the math!

part1 = 10819
part2 = 938

# MATH ERROR!
code = part1 * part2  # <- wrong math

print(f"Your flag is: CCRI-SCRP-{int(code)}")
