#!/bin/bash
# generate_hex_flag.sh

# Create 1KB of random data
dd if=/dev/urandom of=hex_flag.bin bs=1 count=1024

# Insert real flag
echo -n "CCRI-HEXG-2718" | dd of=hex_flag.bin bs=1 seek=615 conv=notrunc

# Insert fake flags
echo -n "NULL-DEAD-2718" | dd of=hex_flag.bin bs=1 seek=137 conv=notrunc
echo -n "HEXG-1337-ABCD" | dd of=hex_flag.bin bs=1 seek=312 conv=notrunc
echo -n "BEEF-CAFE-9999" | dd of=hex_flag.bin bs=1 seek=479 conv=notrunc
echo -n "FAKE-2718-KEYS" | dd of=hex_flag.bin bs=1 seek=870 conv=notrunc

echo "✅ hex_flag.bin generated with 1 real flag and 4 decoys!"