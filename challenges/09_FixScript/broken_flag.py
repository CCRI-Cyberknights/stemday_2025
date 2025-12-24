#!/usr/bin/env python3

# This script should print: CCRI-SCRP-5088
# But someone broke the math!

part1 = 2142
part2 = 2946

# MATH ERROR!
code = part1 - part2  # <- wrong math

print(f"Your flag is: CCRI-SCRP-{int(code)}")
