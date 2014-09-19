
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
__asm__(".global leaf; leaf: mov %ecx, %esp; andl $0xfffffff & (~3), %esp; ret");

#define DO_CALL __asm__("\
mov %ebp, %esp; \
mov $1f, %ecx; \
call leaf; \
0:; \
.data; \
1: .long 0b; \
.text")
"""

print 'void entry(void) {'
print '__asm__("push %ebp; mov %esp, %ebp");'
for _ in range(100):
    print '  DO_CALL;'
print '__asm__("mov %ebp, %esp; pop %ebp");'
print '}'
