#!/usr/bin/env python3

# This script should print: CCRI-SCRP-5612
# But someone broke the math!

part1 = 2131
part2 = 3481

# MATH ERROR!
code = part1 - part2  # <- wrong math

print(f"Your flag is: CCRI-SCRP-{int(code)}")
