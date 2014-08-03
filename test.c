
#include <stdint.h>
#include <stdio.h>


void entry(void);

static inline uint64_t rdtsc(void) {
  uint32_t edx;  /* top 32 bits of timestamp */
  uint32_t eax;  /* bottom 32 bits of timestamp */
  __asm__ volatile("rdtsc" : "=d"(edx), "=a"(eax));
  return (((uint64_t) edx) << 32) | eax;
}

const int calls = 100;
const int iterations = 10000;

int time_it(void) {
  uint64_t t0 = rdtsc();
  int i = 0;
  for (i = 0; i < iterations; i++)
    entry();
  uint64_t t1 = rdtsc();
  return t1 - t0;
}

int main(void) {
  int i;
  for (i = 0; i < 20; i++) {
    int cycles = time_it();
    printf("cycles %.3f\n", (double) cycles / (calls * iterations));
  }
  return 0;
}
