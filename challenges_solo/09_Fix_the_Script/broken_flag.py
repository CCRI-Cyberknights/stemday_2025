#!/usr/bin/env python3

# This script should print: CCRI-SCRP-1899
# But someone broke the math!

part1 = 1199
part2 = 700

# MATH ERROR!
code = part1 * part2  # <- wrong math

print(f"Your flag is: CCRI-SCRP-{int(code)}")
