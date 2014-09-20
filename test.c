
#include <math.h>
#include <stdint.h>
#include <stdio.h>

#include "test.h"


static inline uint64_t rdtsc(void) {
  uint32_t edx;  /* top 32 bits of timestamp */
  uint32_t eax;  /* bottom 32 bits of timestamp */
  __asm__ volatile("rdtsc" : "=d"(edx), "=a"(eax));
  return (((uint64_t) edx) << 32) | eax;
}

const int calls = 100;
const int iterations = 100000;

void run_test(struct test_info *test) {
  int i;

  /* Attempt to warm up first before measuring. */
  for (i = 0; i < iterations; i++)
    test->test_func();

  uint64_t t0 = rdtsc();
  for (i = 0; i < iterations; i++)
    test->test_func();
  uint64_t t1 = rdtsc();
  uint64_t diff = t1 - t0;
  double cycles = (double) diff / (calls * iterations);

  test->time_sum += cycles;
  test->time_square_sum += cycles * cycles;
  test->run_count++;

  test->time_mean = test->time_sum / test->run_count;
  test->time_stddev = sqrt(test->time_square_sum / test->run_count
                           - test->time_mean * test->time_mean);
  struct test_info *baseline = &g_tests[0];
  printf("test %-20s cycles %6.3f (stddev %.3f)  "
         "slowdown factor: %.2f (%.2f-%.2f)\n",
         test->test_name, test->time_mean, test->time_stddev,
         test->time_mean / baseline->time_mean,
         (test->time_mean - test->time_stddev)
         / (baseline->time_mean + baseline->time_stddev),
         (test->time_mean + test->time_stddev)
         / (baseline->time_mean - baseline->time_stddev));
}

int main(void) {
  int j;
  for (j = 0; j < 10; j++) {
    printf("\niteration %i\n", j);

    int i;
    for (i = 0; i < g_test_count; i++)
      run_test(&g_tests[i]);
  }
  return 0;
}
