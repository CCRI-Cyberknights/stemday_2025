#!/usr/bin/env python3

# This script should print: CCRI-SCRP-5224
# But someone broke the math!

part1 = 1701
part2 = 3523

# MATH ERROR!
code = part1 - part2  # <- wrong math

print(f"Your flag is: CCRI-SCRP-{int(code)}")
