#!/bin/bash

# This script should output: CCRI-SCRP-1098
# But someone broke the math!

part1=900
part2=198

# MATH ERROR!
code=$((part1 - part2))  # <- wrong math

echo "Your flag is: CCRI-SCRP-$code"

