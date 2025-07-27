#!/usr/bin/env python3

# This script should print: CCRI-SCRP-5929
# But someone broke the math!

part1 = 509
part2 = 5420

# MATH ERROR!
code = part1 - part2  # <- wrong math

print(f"Your flag is: CCRI-SCRP-{int(code)}")
