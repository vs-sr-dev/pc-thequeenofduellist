# 07 - Next session

Goal: **the runtime's machine, headless, until the game draws its first
picture** -- the Agumix logo -- and the frame matches the oracle's.

1. The boot as RUN386 leaves it: the game's image at linear 0x200000 under
   selectors 0x0C/0x14 (80 KB, stack top 0x13F20), the disc's TBIOS at
   0x100000 under 0x110/0x118 with its table filled as the Towns' load
   leaves it (the 265 bytes that differ: read them in the Towns dump of
   session 2, `build/oracle/dump_fmtowns_20`), the LDT/GDT selectors of
   `towns.SELECTORS` as bases, the registers at the entry as RUN386 sets
   them (a dump at the entry: a Lua breakpoint on CS=0x0C, EIP=0xA7F0).
2. The services, each from what the game and TBIOS ask (`03-executables.md`):
   int 21h's nine DOS functions over the disc image (`fmtownskit.disc`'s
   reader in C++, Q: the CD), Phar Lap's six, int 93h's CD-DA calls, int
   FDh; the real-mode routine at the image's start (int 23h/24h) answered
   as nothing to do.
3. The machine under TBIOS: VRAM (512 KB, both access windows), the CRTC
   and video output registers, the sprite RAM and controller, the palettes;
   a frame as a PNG from the CRTC's layers. Then the PICs, the timer, VSYNC
   (IRQ11) and the sound IRQ (13) with the YM3438 timers, delivered at safe
   points.
4. Compare the logo, the title and the attract fight with the oracle's
   frames (`tools/oracle.py --machine fmtowns --at ...`).

The step limit makes the game's own vectors few (135 of 471 runs): a
second seed and a higher `--limit` are cheap once the machine stubs answer
the interrupts the runs stop at.

Tools: `tools/oracle.py --dump SECONDS` (state and RAM) and
`python -m fmtownskit.mamedump DIR`; the recompiler as `09-recompiler.md`
shows; MSYS2's clang, CMake and Ninja on PATH (`export
PATH=/c/msys64/mingw64/bin:$PATH`).
