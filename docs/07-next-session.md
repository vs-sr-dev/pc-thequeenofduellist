# 07 - Next session

Goal: **the selectors and the load read on both machines, then the 386
decoder and interpreter in fmtownskit.**

1. RUN386: find where it builds its descriptors (MZ, real mode then
   protected; the strings "FDOSXT2", "DOSNAD02" are landmarks); the bases
   and limits of 0x14, 0x104, 0x110, 0x118, 0x130 on the Towns and the
   Marty. Confirm in MAME: a Lua script that stops at DUEL.EXP's entry
   (0xA7F0 in CS) and dumps the GDT/LDT and the image (the oracle's memory
   read), on `fmtowns` and on `fmtmarty`.
2. TBIOS's load: what `TBIOS.SYS` does with `TBIOS.BIN` (the table's
   pointers at 0x60-0xA0 are already in the file; what sets 0x118).
3. fmtownskit `x86`: the decoder, checked against capstone on every
   instruction the descent reaches in DUEL.EXP and TBIOS.BIN (seeded from
   the module entries and their AH jump tables).
4. fmtownskit `x86emu`: the interpreter, checked against unicorn (random
   states; the flags the 386 leaves undefined set aside and listed).
5. If time remains: discovery over both programs and the first emitted C++.

Tools: `tools/oracle.py --machine fmtowns|fmtmarty --at ...` (set MAME,
CHDMAN, FMT_ROMS); `python -m fmtownskit.x86map build/disc/DUEL.EXP --seed
103e2,c0b8,c124`.
