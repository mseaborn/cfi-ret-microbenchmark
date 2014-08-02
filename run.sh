#!/bin/bash

set -eu

python gen.py > tmp.c
cflags="-Wall -Werror"
gcc -c $cflags -O2 tmp.c
gcc -c $cflags -O2 test.c -o test.o
gcc test.o tmp.o -o test
./test
