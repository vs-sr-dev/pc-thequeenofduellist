# 00 - Sessions

## Session 1 (2026-10-20): the disc, the code's surface, the plan; fmtownskit born

* **The disc identified**: Redump's "Queen of Duellist, The (Japan) (Rev
  A)", serial HME-166A, the second pressing of the FM Towns CD; every
  track's CRC32 and the CHD's SHA-1 match MAME's software list (`tqod`).
  It is the standard Towns CD, not a separate Marty edition (none is known
  for this game); it **runs on the Marty**: the oracle on MAME's `fmtmarty`
  reaches the title menu and the attract fight as on `fmtowns`
  (`01-disc-layout.md`).
* **The boot chain** read from the files: IPL, Towns-DOS, TBIOS, RUN386
  (Phar Lap 1.2aJ L50), `DUEL.EXP`; an HDD install with a CD check and a
  limited version.
* **The program's surface** (`03-executables.md`): `DUEL.EXP` is a P3
  image of 73,495 bytes, 27 KB of hand-written 386 code, four selectors,
  a handful of DOS/Phar Lap calls, the CD BIOS, nine far calls into TBIOS,
  24 port accesses, and its own sound IRQ handler (IRQ13, int 4Dh).
* **TBIOS.BIN read**: the table behind selector 0x110, its modules and
  their codenames; clean 32-bit code dispatching on AH. The plan: recompile
  the game *and* TBIOS, answer DOS/Phar Lap/CD BIOS at their interrupts
  (`06-attack-plan.md`).
* **The formats at a glance** (`02-data-formats.md`): RF5C68 samples,
  Agumix's `.PX`, `TIB0`, per-fighter sets for six fighters, nine CD-DA
  tracks with audio in their pregaps.
* **fmtownskit** created as a repository of its own (one kit for the Towns
  and the Marty, at the user's suggestion): `disc`, `exp`, `towns`,
  `x86map` (`10-fmtownskit.md`).
* **The oracle**: `tools/oracle.py`, MAME headless with its own
  configuration, snapshots at emulated times, a contact sheet.

Both repositories put under git at the end: fmtownskit at a5910f2, a
submodule of this port at `fmtownskit/`.

## Session 2 (2026-10-20): the machines read running; the 386 recompiler, checked

* **RUN386 on both machines** (MAME dumps, `fmtownskit.mamedump`): paging on, on both;
  the Towns' high pages 1:1, the Marty's remapped onto its 24-bit addresses; the
  descriptors the same base for base. The game's image at linear 0x200000, its code the
  file's byte for byte. The Towns runs the disc's `TBIOS.BIN`; the Marty runs its own
  ROM's build of the same version (`03-executables.md`). The port runs the disc's: the
  Towns path, no ROM.
* **fmtownskit's 386 recompiler** (`09-recompiler.md`): the decoder (0 differences from
  capstone on 24,023 instructions of the game and TBIOS), the interpreter (0 differences
  from unicorn on 246,261 vectors), discovery (the game 157 functions, TBIOS 355, both
  without conflicts, after TBIOS's jump tables taught it which comparison bounds a table),
  the emitter and the runtime's CPU, and the self-test: the optest 22,340 vectors, the
  game's functions 135, TBIOS's 682, **0 failures**.
* The oracle dumps state and RAM (`tools/oracle.py --dump SECONDS`).
