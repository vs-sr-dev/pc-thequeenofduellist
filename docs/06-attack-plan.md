# 06 - The attack plan

## What the port is

A native PC program that runs **the game's own code and TBIOS's own code,
recompiled from 386 to C++**, on a runtime that stands in for the FM Towns
under them: its VRAM and CRTC, its sprite controller, its YM3438 and
RF5C68, its CD with the CD-DA music, its interrupts, its pad. DOS, Phar
Lap and the CD BIOS are answered at their interrupt boundary, from the disc
image. Everything shared goes into fmtownskit; what is this game's stays
here.

Why this shape:

* **The program is small and self-contained**: 27 KB of hand-written 386
  code, four selectors, 23 DOS calls of nine kinds, six Phar Lap calls, the
  CD BIOS, nine far calls into TBIOS, 24 port accesses
  (`03-executables.md`). Its whole contract with the machine fits in one
  page.
* **TBIOS is on the disc and is clean 32-bit code**: each module saves
  its registers, loads its own data selector (0x118) and dispatches on AH
  through a jump table (the sound module's has 82 entries, AH 0-0x51;
  "ま～くん"'s 4). Running it recompiled is less work than imitating it --
  the sound module alone has 82 functions -- and it is the real behaviour.
  Its jump tables are discovery's seeds.
* **DOS is real mode and the program uses little of it**: files on the CD
  (open, read, close), the save file (create, write), memory, the drive
  letter. Answering those at int 21h from the disc image is a page of
  runtime. Same for Phar Lap's six calls and the real-mode routine at the
  image's start (int 23h/24h only: nothing to do on a PC).
* **The Marty comes free**: the program touches the machine only through
  selectors, so the runtime maps selectors, not addresses. A "Marty mode"
  is the 386SX's speed and 2 MB, for the oracle's comparisons, not a
  different port.

## The road

1. **The selectors and the load, read** (next session). RUN386's set-up of
   0x14, 0x104, 0x110, 0x118, 0x130 (base, limit, what lies there) on the
   Towns and on the Marty; MAME's debugger at the game's entry to confirm
   the image at its base and the descriptors (the oracle's Lua reads
   memory). TBIOS's load as `TBIOS.SYS` does it (where 0x110 and 0x118
   point; what fills its table).
2. **The decoder and the interpreter** (fmtownskit, layer 4). An IA-32
   decoder for what 386 code can hold (16/32-bit operand and address sizes,
   segment overrides, the string instructions with `rep`, the 0F opcodes
   the 386 has), checked against capstone on every byte the descent reaches
   in `DUEL.EXP` and `TBIOS.BIN`; an interpreter as the reference, checked
   against unicorn on random states (flags included: the 386's undefined
   flags as the hardware leaves them is a question to settle, unicorn
   answers as a later CPU does).
3. **Discovery and the recompiler** (fmtownskit). Functions from the entry,
   the IRQ handler, the function pointers, and TBIOS's jump tables; C++ per
   function, a module per program (the game, TBIOS), selectors resolved at
   run time through the runtime's descriptor table; a self-test (the
   interpreter records, the C++ replays) as the other kits have.
4. **The runtime, headless** (fmtownskit `runtime/`, C++20, CMake, Ninja,
   clang): memory and selectors, int 21h / 25xxh / 93h / FDh, the PICs and
   IRQ13, VSYNC; the VRAM and the CRTC, the sprite controller, a frame as a
   PNG; then the YM3438 and RF5C68 (a WAV), the CD-DA from the disc
   (pregaps included). Frames compared with the oracle's at the same
   moments (the opening and the title screen are deterministic).
5. **The window**: SDL3, the picture at an integer scale (the Towns' 640x480
   at 2x or 3x, *to measure* what the game's mode is), the pad from the
   keyboard and a gamepad (the Towns pad: two buttons, Run, Select), sound
   in real time.
6. **Playable**: a fight from the title to the ending with both players;
   the save (`dueltwn.sav`) kept on the host; then publication at the
   user's word.

## What is new here for the kit

Everything: fmtownskit is born with this game. The pieces a second Towns
game would reuse are the disc and the boot (done), RUN386 and the P3 load,
the 386 recompiler, TBIOS run from the disc, and the machine. What stays
here: the game's formats (`.PX`, `.TIB`, `.SPT`, ...) if a tool needs them,
and the game's fixes.

## Better than the Towns

To weigh with the user once it runs: no load times (the CD's speed is the
runtime's choice: as fast as the host, or the Towns' for the oracle), a
choice of integer and smooth scaling, both players on gamepads, the
"limited version" never in the way (the runtime serves the CD the game
looks for). Nothing that changes the game's own code.

## The risks

* **Timing**: the game is driven by the VSYNC and by the sound IRQ (the
  YM3438's timers); the fight's pace is the IRQs' pace. The runtime keeps a
  guest clock, as the 3DO and Saturn runtimes do.
* **The 386's flags**: hand-written assembly uses them freely (e.g. carry
  through `adc`, flags read after `inc`). The emitter computes them where
  they are read; the interpreter is the reference.
* **What the descent does not reach**: 3 KB of the code range so far
  (CD BIOS 53h and 55h live there) and whatever the indirect calls reach;
  the runtime stops with the address when it meets code it has not
  compiled, as the other kits do.
