/*
* This example is inspired by the OWASP example
* at https://owasp.org/www-community/attacks/Buffer_overflow_attack
* and the CTF Handbook example at
* https://ctf101.org/binary-exploitation/buffer-overflow/
*/
#include <stdio.h>

int main(int argc, char **argv) {
    int secret = 0xdeadbeef;
    char buf[8];
    printf("Enter your name to see if you deserve an easter egg: ");
    fgets(buf, sizeof buf, stdin);
    if (secret == 0x1337) {
        printf("Here, have an easter egg!");
    } else {
        printf("You do not deserve an easter egg, %s.\n", buf);
    }
    return 0;
}
