#!/bin/bash

set -eu

python gen.py > tmp.c
cflags="-Wall -Werror -m32 -O2"
gcc -c $cflags tmp.c
gcc -c $cflags test.c -o test.o
gcc $cflags test.o tmp.o -o test
./test
