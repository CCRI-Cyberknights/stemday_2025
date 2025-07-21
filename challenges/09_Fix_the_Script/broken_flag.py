#!/usr/bin/env python3

# This script should print: CCRI-SCRP-8210
# But someone broke the math!

part1 = 2159
part2 = 6051

# MATH ERROR!
code = part1 - part2  # <- wrong math

print(f"Your flag is: CCRI-SCRP-{int(code)}")
