#!/usr/bin/env python3

# This script should print: CCRI-SCRP-9495
# But someone broke the math!

part1 = 2680
part2 = 6815

# MATH ERROR!
code = part1 / part2  # <- wrong math

print(f"Your flag is: CCRI-SCRP-{int(code)}")
