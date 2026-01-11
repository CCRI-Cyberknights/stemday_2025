#!/usr/bin/env python3

# This script should print: CCRI-SCRP-9614
# But someone broke the math!

part1 = 391
part2 = 9223

# MATH ERROR!
code = part1 - part2  # <- wrong math

print(f"Your flag is: CCRI-SCRP-{int(code)}")
