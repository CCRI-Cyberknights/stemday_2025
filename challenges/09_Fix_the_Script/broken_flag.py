#!/usr/bin/env python3

# This script should print: CCRI-SCRP-4429
# But someone broke the math!

part1 = 103
part2 = 43

# MATH ERROR!
code = part1 / part2  # <- wrong math

print(f"Your flag is: CCRI-SCRP-{int(code)}")
