
# # Standard unsandboxed calling sequence.
# print r"""
# __asm__(".global leaf; leaf: ret");
# #define DO_CALL __asm__("call leaf\n")
# """

# print r"""
# // naclret
# __asm__(".global leaf; leaf: pop %ecx; jmp *%ecx");

# // Standard call (as used by NaCl)
# #define DO_CALL __asm__("call leaf\n")
# // PNaCl call
# //#define DO_CALL __asm__("push $0f; jmp leaf; 0:\n")
# """

# Proposed new sandboxing.
print r"""
__asm__(".global leaf; leaf: pop %eax; xchg %ecx, %esp; ret");

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
