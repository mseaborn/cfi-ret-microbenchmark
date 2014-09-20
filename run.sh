#!/bin/bash

set -eu

mkdir -p out

python gen.py > out/asm.S
cflags="-Wall -Werror -m32 -O2"
gcc -c $cflags out/asm.S -o out/asm.o
gcc -c $cflags -I. out/runner.c -o out/runner.o
gcc -c $cflags test.c -o out/test.o
gcc $cflags out/asm.o out/runner.o out/test.o -o out/test -lm
./out/test
