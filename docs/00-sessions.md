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

## Session 3 (2026-10-21): the runtime's machine; the logo, the opening and the title, pixel for pixel

* **The program's first instruction, read** (`tools/oracle.py --dump-write`: MAME stopped at
  the first push of the entry's `call`, 12.0 s after power-on): the registers RUN386 hands
  over, the image and **TBIOS byte for byte the disc's** (session 2's 265 differing bytes
  are the game's own set-up), and the machine's state -- the CRTC, palettes and video
  registers read through the ports from Lua, the PICs from MAME's save items
  (`11-runtime.md`).
* **fmtownskit's machine** (`runtime/towns*`): memory and descriptors, far calls between
  the program and TBIOS, the program's interrupt handlers at safe points through
  level-triggered PICs, VSYNC and the beam, the CRTC and video registers, palettes, the
  VRAM mask and windows, the sprite controller, the RF5C68's channels and the PCM
  interrupt, DOS and Phar Lap over the disc image, the CD BIOS's TOC, play and stop; a
  frame composed as MAME's `screen_update` composes it.
* **The game runs headless** (`src/main.cpp`, `build/rt/tqod`): the CD check passes, TBIOS
  sets up from the game's calls, the files load, the CD-DA is asked for, and the Agumix
  logo, its fades, the opening, the title screen with its menu (the font ROM's text) and
  the attract fight are drawn -- **every still snapshot of the oracle tried matches a
  runtime frame pixel for pixel** (`tools/framematch.py`). The fight runs; its bouts drift
  from the oracle's as timing does. 150 s of the game in 1.9 s.
* One more table of seeds: five routines of the opening, called through a pointer list at
  0x980E.

## Session 4 (2026-10-21): the sound, held against MAME's; the window, the pad; a fight played

* **The oracle's sound** (`tools/oracle.py --wav`, `--sound-log`): MAME's WAV and every
  write to the sound ports and the wave RAM, timed. The game's music is CD-DA, its PCM the
  fight's voices; the YM3438 is set up and never keyed on; the logo is silent
  (`12-sound.md`).
* **fmtownskit's sound** (`runtime/towns_sound.cpp`): the RF5C68, the YM3438 on ymfm
  (BSD-3, `runtime/ymfm/`), the CD's audio from the image, the volume ports, a mix at
  48 kHz as MAME's speakers have it. Held against the oracle by replaying its log
  (`tqod --replay-sound`): the CD-DA at 0.09% residual, the PCM at correlation 0.989 with
  every band's power 0.98-1.01 of MAME's, two FM notes (`tools/fmtest.lua`) at 0.03% --
  once the kit took MAME's whole stream rates (20,833 Hz, not 20,833.3) and its resampling
  (a held sample averaged over the output's span). The game's own opening track: 0.999.
* **The oracle's clock, corrected**: its Lua read whole seconds. The program's first
  instruction is at 12.308 s, not 12.0; the fractional snapshots retaken, all 15 still
  pixel-identical.
* **The window** (`runtime/towns_sdl.cpp`, SDL3 static): integer scale, the guest paced by
  the sound queue, the keyboard and gamepads as the Towns pad (Run = left+right, Select =
  up+down, as MAME's townspad). `tqod` opens it; `--headless` as before.
* **Played** (`--input`): A on START, the fighter select, Stage 1 against Shinobu, two
  rounds and her win screen, 150 s without a fault. The user played it in the window: one
  glitch, a column of the CPU's sprite at the left edge when pushed out at the right --
  MAME's clipping, copied; the kit now clips each pixel at its own x (`12-sound.md`).

## Since session 4

The kit pulled to e4c5334 (the second game's: `docs/10-fmtownskit.md`);
the game the same, frame for frame and in its sound; `--crop`.
