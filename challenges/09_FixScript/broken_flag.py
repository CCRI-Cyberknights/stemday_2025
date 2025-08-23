#!/usr/bin/env python3

# This script should print: CCRI-SCRP-7603
# But someone broke the math!

part1 = 3293
part2 = 4310

# MATH ERROR!
code = part1 / part2  # <- wrong math

print(f"Your flag is: CCRI-SCRP-{int(code)}")
