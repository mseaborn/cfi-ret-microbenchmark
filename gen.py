
import random


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
mov %rcx, %rsp; \
.data; \
1: .quad 0b; \
.text")
"""

count = 50
for idx in range(count):
    #print 'void caller%i(void) { leaf(); }' % idx
    print 'void caller%i(void) { DO_CALL; }' % idx

rand = random.Random(0)
print 'void entry(void) {'
for _ in range(100):
    print '  caller%i();' % rand.randrange(0, count)
print '}'
