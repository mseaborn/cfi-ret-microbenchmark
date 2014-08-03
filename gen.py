
print 'void leaf(void);'

print r"""
//#define DO_CALL __asm__("push $0f; jmp leaf; 0:\n")
//#define DO_CALL __asm__("call leaf\n")
"""
print """
#define DO_CALL __asm__("\
mov $1f, %ecx; \
call leaf; \
0:; \
mov %ecx, %esp; \
.data; \
1: .long 0b; \
.text")
"""

print 'void entry(void) {'
for _ in range(100):
    print '  DO_CALL;'
print '}'
