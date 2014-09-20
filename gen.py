
fh_asm = open('out/asm.S', 'w')
tests = []


def PutLabel(label):
  fh_asm.write('.global %s\n' % label)
  fh_asm.write('.p2align 5\n')
  fh_asm.write('%s:\n' % label)


def EmitTest(name, func_asm, caller_asm):
  leaf = 'leaf_%s' % name
  PutLabel(leaf)
  fh_asm.write(func_asm + '\n')

  caller = 'caller_%s' % name
  PutLabel(caller)
  caller_asm = caller_asm.replace('DEST', leaf)
  for i in xrange(100):
    fh_asm.write(caller_asm + '\n')
  fh_asm.write('ret\n')

  tests.append(name)


def EmitCCode():
  fh = open('out/runner.c', 'w')
  fh.write('void run_test(const char *name, void (*func)(void));\n')
  for name in tests:
    fh.write('void caller_%s(void);\n' % name)
  fh.write('void run_tests(void) {\n')
  for name in tests:
    fh.write('  run_test("%s", caller_%s);\n' % (name, name))
  fh.write('}\n')
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

EmitTest('new',
         'xchg %ecx, %esp; ret',
         ('mov $1f, %ecx; call DEST; 0: lea 4(%ecx), %esp; '
          '.data; 1: .long 0b; .text'))

EmitCCode()
fh_asm.close()
