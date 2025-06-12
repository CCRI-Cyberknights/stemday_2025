#include <stdio.h>
#include <string.h>

// Make sure to keep these in order so they're not optimized out
char flag1[] = "FLAG-NULL-0000";
char junk1[300] = "ABCD1234XYZ!@#%$^&*()_+=?><~";

char flag2[] = "CCRI-BINA-7091";
char junk2[500] = "longgarbage....data...not...readable....random";

char flag3[] = "RAND-EXEC-1337";
char junk3[400] = "G@rb@g3StuffDataThatLooksBinaryButIsn't....";

char flag4[] = "CODE-3333-DATA";
char junk4[600] = {0};  // binary noise

char flag5[] = "GARB-7777-DUMP";
char junk5[350] = "%%%%%%%//////??????^^^^^*****&&&&&";

void keep_strings_alive() {
    volatile char dummy = 0;
    dummy += flag1[0] + flag2[0] + flag3[0] + flag4[0] + flag5[0];
    dummy += junk1[0] + junk2[0] + junk3[0] + junk4[0] + junk5[0];
}

int main() {
    printf("Hello, world!\n");
    keep_strings_alive();
    return 0;
}
