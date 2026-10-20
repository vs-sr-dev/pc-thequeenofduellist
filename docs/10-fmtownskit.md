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
