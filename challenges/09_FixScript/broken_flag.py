#!/usr/bin/env python3

# This script should print: CCRI-SCRP-2329
# But someone broke the math!

part1 = 1169
part2 = 1160

# MATH ERROR!
code = part1 / part2  # <- wrong math

print(f"Your flag is: CCRI-SCRP-{int(code)}")
