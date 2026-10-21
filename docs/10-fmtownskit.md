# 10 - fmtownskit

The kit this port is built on, and what this port has brought to it. The
kit's own README lists every module and its checks; this file is the log.

## Session 1: the kit is born

At the user's suggestion one kit covers the FM Towns and the FM Towns
Marty: the machines differ in data (memory map, machine id, speed, RAM),
which the kit keys by machine.

| Module | What this game asked of it |
|---|---|
| `disc` | cue sheets with one file per track (Redump's split), MODE1/2352 and AUDIO, INDEX 00/01 and the tracks' disc positions; ISO 9660; the IPL record in sector 0; `--extract` (with `sysarea.bin`), `--cat`, `--wav` |
| `exp` | the Phar Lap P3 header, level 1, the image as loaded |
| `towns` | both memory maps, the I/O ports, IRQs, machine ids (from MAME's driver), the selectors a program uses, DOS and Phar Lap names; confirmed by this game: pad, CRTC, sprite controller, sound status ports, IRQ13 at int 4Dh |
| `x86map` | the descent over a P3 image and the naming of every system site; selector loads through a 32-bit register's low half |

Checked on this disc only (the first). Kit at **a5910f2**, the submodule
at `fmtownskit/`.

## Session 2

| Change | What this game asked of it |
|---|---|
| `mamedump` | a running machine read from MAME's state and RAM: the page walk, GDT and LDT, bytes found -- to read RUN386's selectors on the Towns and the Marty |
| `towns.SELECTORS`, `PAGES_MARTY` | the selectors as both machines have them (the same), the Marty's page mappings; the README's "one machine for RUN386" and the Marty's TBIOS from its ROM |
| `x86map` | jump tables, `--raw` images from a far-pointer table (TBIOS), `--mnemonics` |
| `i386` | the 386 decoder, `--check` against capstone, `--sweep` of random bytes |
| `i386emu` | the interpreter, `--test`, `--check`/`--sweep` against unicorn |
| `recomp` (`discover`, `emit`, `selftest`, `__main__`) | the recompiler: functions and bodies, tables bounded or read and pruned, C++ per function, the vectors and the optest |
| `runtime/x86*` | the CPU for recompiled code, the flags' helpers, modules, the self-test (with `-DX86_TRACE_ON` a trace per instruction) |

Kit at the session's commit: see `git -C fmtownskit log -1`.

## Session 3

| Change | What this game asked of it |
|---|---|
| `runtime/towns.h`, `towns_mem` | linear memory as RUN386 leaves it (host pages for RAM, sprite RAM and VRAM while its write mask is all ones; the masked writes, the single-layer window, the PCM wave RAM's bank, the font ROM one byte at a time), the descriptors, the machine as TownsOS hands it over (CRTC, palettes, video and PIC state read at the program's first instruction) |
| `towns_cpu` | far calls and returns between the program and TBIOS as C++ calls, calls through a register by code selector, `int`, the program's protected-mode handlers taken at safe points |
| `towns_io` | the ports the game and TBIOS touch (MAME's meanings), level-triggered PICs in special fully nested mode, VSYNC and the beam for CRTC register 30, the microsecond counter, the sprite controller's flip and drawing, the RF5C68's channels and the PCM interrupt, the YM3438 as registers |
| `towns_video` | the sprite controller's drawing and the frame composed as MAME's `screen_update`; a PNG writer |
| `towns_dos` | int 21h (DOS files over the disc image and a host directory, memory blocks as RUN386 places them, Phar Lap 0Dh/0Eh/0Fh/11h/06h), the CD BIOS's 50h/52h/54h, RUN386's start of a P3 program |
| `towns_disc` | the cue sheet, the data track and the audio sectors, ISO 9660 paths |
| `towns.cmake` | the runtime as a library for a port's CMake |

Checked by the game's frames against the oracle's (`11-runtime.md`): the logo, the opening
and the title, pixel for pixel.
