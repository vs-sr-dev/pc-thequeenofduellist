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

## Session 4

| Change | What this game asked of it |
|---|---|
| `runtime/towns_sound.cpp` | the sound out of `towns_io`: the RF5C68 (an event at MAME's whole 20,833 Hz), the YM3438 on ymfm with its timers, busy flag and IRQ13 share, the CD's audio from the image (play, stop, its end), the volume ports as MAME's `cdda_db_to_gain`, the mix at 48 kHz (MAME's routes, its held-and-averaged resampling), `audio_take`, `audio_mute`, a WAV writer, `replay_sound_log` (an oracle's log into the chips) |
| `runtime/ymfm/` | ymfm's OPN files (Aaron Giles, BSD-3, its LICENSE), unchanged from MAME's 3rdparty copy |
| `towns_io`, `towns.h` | the sound ports handed to `towns_sound`; `set_pad` and the `kPad*` buttons (Run and Select as MAME's townspad wires them) |
| `towns_dos` | int 93h 50h/52h play and stop the CD's audio |
| `towns_video` | a 16-colour sprite's second pixel clipped at its own x, not at the first's as MAME does (a column of a mirrored sprite at x 256 wrapped to the left edge) |
| `runtime/towns_sdl.*`, `towns.cmake` | the window as an optional library (`fmt_towns_sdl`, SDL3 when found): integer scale, the sound queue as the clock, keyboard and gamepads as the pad |

Checked by the oracle's own sound replayed (`12-sound.md`).

## Since: the kit's second game

fmtownskit grew with its second game, pc-4ddriving (4D Driving; that
port's `docs/10-fmtownskit.md` has each change): a 386 program's P3 symbol
table and the x87's escapes (a33c4f2), the machine as a profile (9c1ccd3),
tables placed after their jump and DOS, Phar Lap and FORRBIOS.NSD services
(959818b), DOS's finds and free space, the CD BIOS while a track plays,
and the window's picture and mouse (e4c5334). The submodule is pulled to
**e4c5334**.

Checked on this game: rebuilt on each, its C++ byte for byte the same; on
e4c5334 its 3,600 frames and 150 seconds of sound the same as on 959818b,
byte for byte. The window now shows the picture only (the CRTC's layer
windows, not MAME's whole frame) at one scale, and has the host's mouse;
`tqod --crop` saves PNGs the same way.
