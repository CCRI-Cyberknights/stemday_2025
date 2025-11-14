#!/usr/bin/env python3

# This script should print: CCRI-SCRP-4324
# But someone broke the math!

part1 = 1743
part2 = 2581

# MATH ERROR!
code = part1 * part2  # <- wrong math

print(f"Your flag is: CCRI-SCRP-{int(code)}")
