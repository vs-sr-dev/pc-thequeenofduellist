# 03 - The executables

## DUEL.EXP

`python -m fmtownskit.exp build/disc/DUEL.EXP`: a Phar Lap **P3** file,
level 1 (flat), 74,007 bytes; the image is 73,495 bytes at file offset
0x200, loaded at 0, **entry 0xA7F0**, stack top 0x13F20; no relocations,
no segment table, no symbols. The header's "extra pages" fields both say
0x2009 (not yet understood). The run-time parameters begin "DX".

### Layout of the image

| Range | What |
|---|---|
| 0x0000-0x0030 | a **real-mode** routine (16-bit): points int 23h at an `iret` and int 24h at a handler that fails the call -- no Ctrl-Break, no "Abort, Retry, Fail". The program runs it at its start through Phar Lap's 250Fh (the address made real-mode) and 250Eh (call real-mode procedure) |
| 0x0040 | "Queen of Duellist for FM-TOWNS version 1.01 / Copyright (c) 1993 AGUMIX." |
| 0x01D0-0x3860 | data: `Q:\AGUMIX.PX`, file names per fighter, tables |
| ...-0xA7F0 | data (strings up to 0x0A3A8; tables) |
| 0xA7F0-0x11B98 | **code**: 27,124 bytes reached from the entry and three seeds |

The code is **hand-written assembly** (*inferred*): no compiler prologue
(`push ebp; mov ebp, esp`) anywhere, registers saved with `pushal`, 16-bit
operations (`66` prefix) all through, and subroutines that pass arguments
in AX/BX/CX/DX.

### What it touches

`python -m fmtownskit.x86map build/disc/DUEL.EXP --seed 103e2,c0b8,c124`:
157 functions, 7,903 instructions. Its whole system surface:

| What | Where | Sites |
|---|---|---|
| DOS (int 21h) | 19h current drive; 3Ch, 3Dh (4), 3Eh (3), 3Fh, 40h files; 48h memory (10 sites); 09h and 4Ch (the "Not enough memory." exit). Two more 4Ch exits lie in code the descent does not reach yet | 23 |
| Phar Lap (int 21h AH=25h) | 0Dh real-mode link information (2), 0Eh call real-mode procedure, 0Fh convert address, 11h issue real-mode interrupt, **06h** (int 4Dh, the sound IRQ, taken in protected mode) | 6 |
| CD BIOS (int 93h, AL=0xC0) | AH=52h directly (3 sites); 54h through 2511h (issue real-mode interrupt); 53h and 55h in code not reached yet (a linear sweep finds them at 0xC778 and 0xC796) | 3 + 1 |
| int FDh | one site, CX=1000 (*inferred*: a wait) | 1 |
| TBIOS, `call far fs:[n]`, FS=0x110 | 0x20 graphic (1), 0x60 sprite (4: AH=0, 1), 0x80 sound (1, from the IRQ handler with AH=51h, and with AH=15h/16h at its setup), 0xA0 "ま～くん" (3: AH=0, 1, 2) | 9 |
| ports | pad: out 0x4D6, in 0x4D0 and 0x4D2; CRTC: 0x440, 0x442, 0x443 (register 0x11 and 0x15: the scroll, *inferred*); sprite controller: 0x450, 0x452; PICs: 0x00, 0x10, 0x12 (end of interrupt, unmask IRQ13); sound status 0x4E9 | 24 |
| selectors | only four in the whole program: 0x14 (its own data, 8 loads), 0x104 (VRAM, 10), 0x110 (TBIOS, 8), 0x130 (sprite RAM, 22: 8-byte records written down from 0x2000) | 48 |

It reads no machine id and touches no memory by linear address: everything
goes through RUN386's selectors and TBIOS, which is why it runs on the
Marty.

### The start (0xA7F0), read

1. the real-mode routine (int 23h/24h); the drive test (int 21h AH=19h): if
   the current drive is not Q:, its letter replaces the "A" of
   `A:dueltwn.sav`;
2. two function pointers stored (0xC0B8 at [0xA50], 0xC124 at [0xA8C]: the
   indirect `call eax`/`call edx` later);
3. **the CD check**: 0xC5D6 asks the CD BIOS (int 93h AX=54C0h through
   2511h, then AX=52C0h) up to five times; if that fails, or if
   `Q:\AGUMIX.PX` does not open, it sets [0x20BA]=0xFFFF, [0x63D]=4,
   [0x61D]=0xA0 -- *inferred*: the limited version `DUELTWN.TXT` describes;
4. memory (int 21h AH=48h, eight blocks), TBIOS set-up, the sound IRQ
   (0x103A8: int 4Dh hooked with 2506h, IRQ13 unmasked in port 0x12), then
   the logo and the main loop.

### The sound interrupt (0x103E2)

Switches to a stack of its own the first time in (a nesting count at
[0x3876]), reads 0x4E9 and, when bit 3 (PCM) is set, calls the sound
module (`fs:[0x80]`, AH=51h); then end-of-interrupt to both PICs, with the
in-service registers read (OCW3 0x0B) to send the master's only when no
other slave interrupt is in service. The music itself is CD-DA.

## TBIOS.BIN

94,208 bytes, "V31L31 92/11/11 towns tbios", Fujitsu, loaded by
`TBIOS.SYS` ("Towns-BIOS Loader for TownsOS Version2.1"). Its first bytes
are the table programs call through with FS=0x110 -- far pointers with
selector 0x110, so the selector is TBIOS's own segment, the file laid at
its 0:

| fs:[n] | Lands at | Module (its own mark: version, date, name) |
|---|---|---|
| 0x20 | 0110:0D20 | V31L31 92/10/08 graphic |
| 0x40 | 0110:11B60 | V31L31 92/11/11 mouse |
| 0x48 | 0110:1261C | (mouse) |
| 0x50 | 0110:127A0 | (mouse) |
| 0x60 | 0110:12B60 | V31L22A 89/02/10 sprite |
| 0x80 | 0110:12F90 | V31L31 1992-10-08 "ヤルヤル" (yaruyaru): the sound module (it is what the sound IRQ calls) |
| 0xA0 | 0110:15F60 | V31L21 88/11/29 "ま～くん" (ma-kun) |
| -- | 0x160D0 | V31L31 1992-09-29 System |
| -- | 0x16660 | V31L31 1992-10-02 warikomi (割り込み: interrupts) |

All of it is 386 code on the disc: the port can run it recompiled, as the
3DO ports run the OS's own code, rather than imitate it.

## RUN386.EXE

78,496 bytes, an MZ executable: "386|DOS-Extender Version 1.2aJ L50,
Copyright (C) 1986-1991 Phar Lap Software, Inc. and Fujitsu Ltd." Its
descriptors are built at run time (no table of the Towns' addresses in the
file). Read instead from the machines running (session 2:
`tools/oracle.py --dump 20` on `fmtowns` and `fmtmarty`, then
`python -m fmtownskit.mamedump`):

* **Paging is on, on both machines.** On the Towns the hardware's pages
  map 1:1; on the Marty RUN386 maps the Towns' high addresses onto the
  Marty's 24-bit ones (0x80000000 to 0xA00000, 0x81000000 to 0xC00000,
  0xC2000000 to 0x600000, ...). The descriptors are **the same, base for
  base, on both**: the program sees one machine.
* The program's selectors (LDT): **0x0C code and 0x14 data, base
  0x200000, limit 0x13FFF** -- the image (0x11F17) and the stack to
  0x13F20, 80 KB in all; at physical 0x49000 on the Towns, 0x47000 on the
  Marty. In RAM its code is the file's byte for byte (4.9 KB of data
  differ, set by the program). 0x104 is VRAM at 0x80000000 (512 KB), 0x10C
  VRAM single-layer at 0x80100000, 0x114 sprite RAM at 0x81000000; the
  ten memory blocks of int 21h AH=48h are LDT 0x44 to 0x8C (256, 128,
  128, 128, 24, 32, 20, 96, 96 and 64 KB, linear 0x214000 up).
* The system's (GDT): **0x110 code and 0x118 data, base 0x100000**:
  TBIOS, the table at its 0; 0x130 sprite RAM (128 KB); 0x138 the font
  ROM, 0x140 the PCM wave RAM window, 0x148 the OS ROM, 0x100/0x108 the
  system ROM, 0x40 all of RAM.
* **The TBIOS differs**: on the Towns, the RAM at 0x100000 is the disc's
  `TBIOS.BIN` (limit 0x16FFF, its size) but for 265 bytes of data the
  load fills in (among them `fs:[0x98]` = 0x387C, in the graphic module).
  On the Marty it is **not the disc's**: the same version and modules
  (V31L31 92/11/11), from the sprite module on 16 bytes lower, with 8 KB more
  (limit 0x18FFF) holding wrappers -- `fs:[0x20]` lands at 0x17BE0, which
  calls the graphic module's 0xD20 -- and it is in the Marty's ROM
  (`MAR_EX1.ROM` at 0x19C00). The port runs the disc's: the Towns path,
  no ROM needed.

## The others

`DUEL.COM` (199 bytes, real mode) starts RUN386 (`01-disc-layout.md`).
`IO.SYS`, `TOWNS.SYS`, `SYS\CTL.SYS`, `HCOPY\*` are Towns-DOS and its
drivers: the port need not run them (`06-attack-plan.md`).
