
#include <stdint.h>
#include <stdio.h>


void run_tests(void);

static inline uint64_t rdtsc(void) {
  uint32_t edx;  /* top 32 bits of timestamp */
  uint32_t eax;  /* bottom 32 bits of timestamp */
  __asm__ volatile("rdtsc" : "=d"(edx), "=a"(eax));
  return (((uint64_t) edx) << 32) | eax;
}

const int calls = 100;
const int iterations = 100000;

void run_test(const char *name, void (*func)(void)) {
  int i;

  /* Attempt to warm up first before measuring. */
  for (i = 0; i < iterations; i++)
    func();

  uint64_t t0 = rdtsc();
  for (i = 0; i < iterations; i++)
    func();
  uint64_t t1 = rdtsc();
  uint64_t cycles = t1 - t0;
  printf("test %-20s cycles %.3f\n",
         name, (double) cycles / (calls * iterations));
}

int main(void) {
  run_tests();
  return 0;
}
