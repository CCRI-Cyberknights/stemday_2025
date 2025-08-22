#!/usr/bin/env python3

# This script should print: CCRI-SCRP-3824
# But someone broke the math!

part1 = 2411
part2 = 1413

# MATH ERROR!
code = part1 - part2  # <- wrong math

print(f"Your flag is: CCRI-SCRP-{int(code)}")
