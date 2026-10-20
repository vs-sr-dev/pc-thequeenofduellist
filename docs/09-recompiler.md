# 09 - The recompiler

The game's code and TBIOS's, recompiled from 386 to C++ by fmtownskit
(`python -m fmtownskit.recomp`). This file records what each piece was
checked against, on this disc.

## The decoder (`fmtownskit.i386`)

The 386's integer instruction set, decoded by the kit itself; capstone is
only the check.

* Every instruction discovery reaches: **7,903 of `DUEL.EXP`'s and 16,120
  of `TBIOS.BIN`'s agree with capstone** field by field (mnemonic, operands,
  registers, memory fields, immediates, length). The one refusal is an x87
  `fdivr` reached through a TBIOS jump table read too far (data, gone once
  discovery prunes its tables: below).
* 300,000 sequences of random bytes: 281,740 agree; 11 differ, every one
  capstone's: a `jmp rel32` after a 67h prefix truncated to 16 bits (the
  operand size, not the address size, decides that on a 386), `F2 A5` and
  `F0 F2 ...` with a prefix dropped, and the 386's test registers TR6/TR7,
  which capstone does not know. What this decoder refuses and capstone
  decodes is the x87 (8,698), later CPUs' instructions (CMOV, BSWAP, CPUID,
  CMPXCHG, XADD, RDTSC, SYSCALL...), LOCK on what cannot be locked, both REP
  prefixes at once, and reserved encodings.
* Conventions set aside in the comparison, each a naming of capstone's:
  string instructions' implicit DS, LEA's operand size, far pointers
  (`lcall`/`ljmp` through memory, which capstone calls `call`/`jmp`; m16:32
  operands it sizes 4), 16-bit displacements compared modulo 64 KB, later
  CPUs' readings of prefixes a 386 ignores (BND, NOTRACK, XACQUIRE,
  XRELEASE, `repz ret`).

## The interpreter (`fmtownskit.i386emu`)

The reference the recompiled code is held against.

* 10 known answers of what a 386 does (RCL of a byte by 9, shift counts
  modulo 32, `push esp`, `pop [esp]`, BT with a register offset past the
  operand, IDIV toward zero, REP with ECX 0, LOOP with ECX 1, 16-bit INC
  wrapping, NEG of 0).
* Against unicorn, from random registers and flags, memory mapped on demand:
  **30,020 vectors over `DUEL.EXP`'s instructions, 46,545 over TBIOS's,
  169,696 over random instructions: 0 differences.** Set aside: the
  machine's instructions (interrupts, ports, far transfers, segment loads,
  CLI/STI, POPF) -- the runtime's to answer --, the flags Intel leaves
  undefined (listed in `UNDEFINED`), a 16-bit SHLD/SHRD by more than 16, and
  two of unicorn's own errors: `ret imm16` with the immediate sign-extended
  (the 386 zero-extends it: Intel's pseudo-code, Bochs) and `F6/F7 /1`, the
  undocumented second encoding of TEST, which unicorn refuses.
* QEMU runs a REP instruction one iteration at a time; the check runs
  unicorn on to the next instruction for those.

## Discovery (`fmtownskit.recomp.discover`)

* `DUEL.EXP` from its entry, the IRQ13 handler (0x103E2) and the two
  function pointers its start stores (0xC0B8, 0xC124): **157 functions,
  7,903 instructions, 0 conflicts**, no jump table, three calls through a
  register.
* `TBIOS.BIN` from the far pointers at 0x20-0xFF: **355 functions, 14,385
  instructions, 33 jump tables (11 bounded), 0 refusals, 0 conflicts**, 42
  indirect transfers (mostly calls through a vector in its data,
  `gs:[ebp + 0x2xx]`).
* What it took on TBIOS: a table's bound is the `cmp idx, N` / `ja` that
  guards it only when nothing writes the index in between (a `cmp al, 0x10`
  read as the bound of a table indexed by a later `setb al` sent the descent
  into data: 260 conflicts); `setcc` gives 2 entries, `and idx, N` N+1, and
  `movzx idx, r8` moves the question to r8 (which also corrected a table at
  0x11BC from 2 entries to its real 4). A table with no bound is read while
  its entries hold, and cut short at the first entry whose code conflicts
  or is refused, the descent run again until it is clean (one cut, 0x675B: 5
  entries to 4).

## The emitter and the self-test (`fmtownskit.recomp`)

`python -m fmtownskit.recomp --out build/recomp --exp duel=build/disc/DUEL.EXP@0c+103e2,c0b8,c124
--raw tbios=build/disc/TBIOS.BIN@110:20-100 --optest --selftest 3` writes a C++ module per
program -- the game under code selector 0x0C, TBIOS under 0x110 -- and the self-test's
vectors; every generated file compiles with clang at the first build.

* The optest -- every distinct instruction of the game, of TBIOS and of a random sweep,
  each made a one-instruction function: 7,464 functions, **22,340 vectors from the
  interpreter, 0 failures** on the C++.
* What the first replay found was the vectors' generator's, not the emitter's: a `push`
  then `ret` returns to the pushed value, which the C++ does (it returns) and the
  interpreter's run did not (it went on until it met the sentinel). The generator now
  follows the C++ frames: a `ret` that no frame expects ends the function.
* Two slownesses met on the way, both the test's: the image loaded byte by byte for
  each vector (Python and C++), and random ECX values under REP (a `rep stosd` of four
  billion words inside one step); ECX is now 0-63 in a random state.
* The functions themselves, 3 random states each, every call, jump table and return as the
  game runs them: **`DUEL.EXP` 135 vectors, TBIOS 682, 0 failures** (TBIOS's 32 more stop in
  the C++ at a call to an address that is no entry, which the self-test does not follow;
  the other runs reached the machine -- an interrupt, a port, a far call -- or the step limit
  in the interpreter, and are not vectors).
* What the function vectors found was the test's again: with every selector at base 0, a
  write through ES = 0x130 (sprite RAM) landed on the code it was running, which the
  interpreter then decoded anew and the C++ did not. In a self-test now only the program's
  own selectors (CS and CS+8) are at base 0; any other is at `sel << 16`, the same rule in
  Python and C++. A differential trace (`-DX86_TRACE_ON`: each instruction's address and
  registers, as the interpreter prints them) found it in one diff.
