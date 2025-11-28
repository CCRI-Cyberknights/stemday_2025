#!/usr/bin/env python3

# This script should print: CCRI-SCRP-5435
# But someone broke the math!

part1 = 1790
part2 = 3645

# MATH ERROR!
code = part1 + part2  # <- fixed math

print(f"Your flag is: CCRI-SCRP-{int(code)}")
