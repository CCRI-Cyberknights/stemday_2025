#!/usr/bin/env python3

# This script should print: CCRI-SCRP-5759
# But someone broke the math!

part1 = 2619
part2 = 3140

# MATH ERROR!
code = part1 * part2  # <- wrong math

print(f"Your flag is: CCRI-SCRP-{int(code)}")
