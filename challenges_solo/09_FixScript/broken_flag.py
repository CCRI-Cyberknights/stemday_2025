#!/usr/bin/env python3

# This script should print: CCRI-SCRP-1811
# But someone broke the math!

part1 = 204
part2 = 1607

# MATH ERROR!
code = part1 * part2  # <- wrong math

print(f"Your flag is: CCRI-SCRP-{int(code)}")
