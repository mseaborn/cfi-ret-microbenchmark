#ifndef TEST_H
#define TEST_H

struct test_info {
  const char *test_name;
  void (*test_func)(void);

  /* Results */
  int run_count;  /* Number of runs. */
  double time_sum;  /* Sum of times, across all runs. */
  double time_square_sum;  /* Sum of squares of times, across all runs. */

  /* Computed from above */
  double time_mean;
  double time_stddev;
};

extern struct test_info g_tests[];
extern int g_test_count;

#endif
