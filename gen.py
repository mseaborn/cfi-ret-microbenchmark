
fh_asm = open('out/asm.S', 'w')
tests = []


def PutLabel(label):
  fh_asm.write('.global %s\n' % label)
  fh_asm.write('.p2align 5\n')
  fh_asm.write('%s:\n' % label)


def EmitTest(name, func_asm, caller_asm, prologue='', epilogue=''):
  leaf = 'leaf_%s' % name
  PutLabel(leaf)
  fh_asm.write(func_asm + '\n')

  caller = 'caller_%s' % name
  PutLabel(caller)
  fh_asm.write(prologue + '\n')
  caller_asm = caller_asm.replace('DEST', leaf)
  for i in xrange(100):
    fh_asm.write(caller_asm + '\n')
  fh_asm.write(epilogue + '\n')
  fh_asm.write('ret\n')

  tests.append(name)


def EmitCCode():
  fh = open('out/runner.c', 'w')
  fh.write('#include "test.h"\n')
  for name in tests:
    fh.write('void caller_%s(void);\n' % name)
  fh.write('struct test_info g_tests[] = {\n')
  for name in tests:
    fh.write('  { "%s", caller_%s },\n' % (name, name))
  fh.write('};\n')
  fh.write('int g_test_count = %i;\n' % len(tests))
  fh.close()


EmitTest('unsandboxed', 'ret', 'call DEST')

EmitTest('nacl_noalign', 'pop %ecx; jmp *%ecx', 'call DEST')
EmitTest('nacl_jmpfill',
         'pop %ecx; andl $~31, %ecx; jmp *%ecx',
         'jmp 1f; .fill 32-5-2, 1, 0x90; 1: call DEST')
EmitTest('nacl_longnopfill',
         'pop %ecx; andl $~31, %ecx; jmp *%ecx',
         (r'.ascii "\x66\x66\x66\x2e\x0f\x1f\x84\x00\x00\x00\x00\x00"; '
          r'.ascii "\x66\x66\x66\x66\x66\x66\x2e\x0f\x1f\x84\x00\x00\x00\x00\x00"; '
          'call DEST'))

EmitTest('pnacl_noalign', 'pop %ecx; jmp *%ecx', 'push $0f; jmp DEST; 0:')
EmitTest('pnacl', 'pop %ecx; andl $~31, %ecx; jmp *%ecx',
         'push $0f; jmp DEST; .p2align 5; 0:')

# Defines label "1".
SAVE_ADDR = '.data; 1: .long 0f; .text; 0:'

# ecx_after = esp_before + 4.
EmitTest('new_nomask',
         'xchg %ecx, %esp; ret',
         'mov $1f, %ecx; call DEST; '+SAVE_ADDR+' lea 4(%ecx), %esp')

EmitTest('new',
         'xchg %ecx, %esp; andl $((1<<31) - 1) & ~3, %esp; ret',
         'mov $1f, %ecx; call DEST; '+SAVE_ADDR+' lea 4(%ecx), %esp')

# In this version, the callee clobbers %esp and does not save it into
# another register.
EmitTest('new_callee_save_esp',
         'mov %ecx, %esp; andl $((1<<31) - 1) & ~3, %esp; ret',
         'mov %ebp, %esp; mov $1f, %ecx; call DEST; '+SAVE_ADDR,
         prologue='push %ebp; mov %esp, %ebp',
         epilogue='mov %ebp, %esp; pop %ebp')

EmitCCode()
fh_asm.close()
