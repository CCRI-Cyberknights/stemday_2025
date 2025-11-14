#!/usr/bin/env python3

# This script should print: CCRI-SCRP-9275
# But someone broke the math!

part1 = 4167
part2 = 5108

# MATH ERROR!
code = part1 - part2  # <- wrong math

print(f"Your flag is: CCRI-SCRP-{int(code)}")
