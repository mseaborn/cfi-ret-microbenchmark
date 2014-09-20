#ifndef TEST_H
#define TEST_H

struct test_info {
  const char *test_name;
  void (*test_func)(void);
};

extern struct test_info g_tests[];
extern int g_test_count;

#endif
