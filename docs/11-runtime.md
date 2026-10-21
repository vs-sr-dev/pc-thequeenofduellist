# 11 - The runtime

The game's code and TBIOS's, recompiled (`09-recompiler.md`), running on
fmtownskit's FM Towns runtime (`fmtownskit/runtime/towns*`), headless:
`build/rt/tqod` runs the program from its first instruction and saves frames.

```sh
python -m fmtownskit.recomp --out build/game \
    --exp duel=build/disc/DUEL.EXP@0c+103e2,c0b8,c124,11322,11476,111cd,1157f,10ff6 \
    --raw tbios=build/disc/TBIOS.BIN@110:20-100
cmake -S . -B build/rt -G Ninja -DCMAKE_CXX_COMPILER=clang++
ninja -C build/rt
build/rt/tqod --frames 3600 --png-every 60 --out build/frames
```

Options: `--cue` (the default is the cue sheet in `disc/`), `--frames N` (stop
after N VSYNCs), `--png F,F,...` and `--png-every N` (frames to save),
`--out DIR`, `--font FILE`, `--trace-int` (DOS, Phar Lap and CD BIOS calls),
`--trace-io` (every port access). The recompiled code is checked against the
disc at the start (each module's CRC32 against the file's).

## Where it starts: the program's first instruction, read

`tools/oracle.py --dump-write 5cf1c=a7f5` stops MAME's `fmtowns` at the first
write of 0xA7F5 to physical 0x5CF1C: the program's first instruction, `call
0xcf07` at 0xA7F0, pushing its return address (the image is at physical
0x49000, its stack top 0x13F20). That happens **12.308 seconds** after
power-on (session 4: session 3's Lua read `machine.time.seconds`, the whole
seconds only, and wrote 12.0; `time:as_double()` gives the fraction), and
there:

* every general register is 0, EFLAGS 0x202, ESP 0x13F20; CS 0x0C, and DS, ES,
  FS, GS and SS all 0x14;
* the image in RAM is the file's byte for byte, the rest of the segment zero
  (but for RUN386's own leftovers on the stack below its top);
* **TBIOS in RAM is the disc's `TBIOS.BIN` byte for byte**: the 265 bytes that
  differed in session 2's dump, 20 seconds in, are the game's own doing
  (TBIOS's set-up, called by the game);
* the descriptors are session 2's (`towns.SELECTORS`), but for the memory
  blocks, which the program has not asked for yet;
* the machine (read through its ports from Lua, and MAME's save items for the
  PICs): the CRTC in a 640x480 mode of two 16-colour layers (video register 0
  0x15, register 1 0x28), both 16-colour palettes the standard ones, the
  256-colour one the eight full colours 32 times over, the VRAM write mask all
  ones; the PICs level-triggered, the master at int 40h with mask 0x3C in
  special fully nested mode, the slave at 48h with mask 0xEE, OCW3 reading the
  in-service register.

The runtime starts from that state (`Machine::townsos`, `boot_run386`). MAME's
driver registers its own state under a module name with a slash in it ("FM
Towns (Model 1/2)"), which hides it from Lua's `device.items`: the video
registers are read through the ports instead (`ports.txt`).

## What the program asked for, and the answers

* **Memory**: ten blocks from int 21h AH=48h, given LDT selectors 0x44 to
  0x8C at linear 0x214000 up, page after page: the same selectors, bases and
  sizes as RUN386 gave on the Towns.
* **Phar Lap**: 250Dh (the real-mode buffer: the values RUN386 returned,
  read in the oracle's RAM: ES:EDX 0060:000408C0, EBX 408C:0000), 250Fh and
  250Eh (the real-mode routine at the image's start: nothing to run), 2511h
  (int 93h through the buffer), 2506h (int 4Dh, the sound IRQ).
* **Files**: in the first 150 seconds `Q:\AGUMIX.PX` (the CD check),
  `AGUMIX.PX`, `TITLE.PX`, `EOP.ANM`, `OPANM.L`, `N_01/02/03/08.SND`,
  `SET.PCL`, `D_M_OP1.PX`, `D_U_OP1.PX`, the `.SPT` files of the logo, the
  demo and `MISC`, and three fighters' sets (`.HCK`, `.MOT`, `.PCL`, `.SPT`,
  `.THK` of Shinobu, Miyuki and Emily, and Shinobu's `.BG`): every one found
  on the image, read at once. (`Q:\AGUMIX.PX` is the start's test for the
  limited version: it opens, so the full game runs.)
* **The CD BIOS** (`03-executables.md`): 54h, the table of contents, in the
  format the oracle's buffer shows; 50h, play from an MSF to an MSF (the
  opening and the title play track 10, from its INDEX 01 to the frame before
  the lead-out); 52h, stop. Heard since session 4 (`12-sound.md`).
* **The font ROM**: the menus' text is drawn from the Towns' font ROM, read
  at 0xC2100000 (ANK at +0x3D000, kanji at +0x4000): `--font`, the user's own
  (BYOA); the default is `bios/fmtowns/fmt_fnt.rom`, the one in MAME's
  `fmtowns` set (CRC32 955C6B75). A loose `FMT_FNT.ROM` from another model
  (DD6FD544) is a different dump: with it the text would differ from the
  oracle's.
* **int FDh** with CX=1000, before the text windows are drawn (AX 5400h,
  CCCCh, 0100h, 0000h): answered with nothing; the frames that follow match
  the oracle's, so whatever it does is not seen (`05-open-questions.md`).
* **One more set of seeds**: the opening is a list of five routines the
  program calls one after the other through `call eax`, a null-ended table
  of pointers at 0x980E (0x11322, 0x11476, 0x111CD, 0x1157F, 0x10FF6). The
  runtime stopped at the first with its address; the table gave the rest.

TBIOS needed nothing of the kind: its graphic, sprite and sound modules ran
recompiled from their first call, through their jump tables and far calls.

## Held against the oracle

`tools/framematch.py`: for each of the oracle's snapshots, the runtime frame
closest to it. Frames are 704x525 on both (the CRTC's whole frame, as MAME
snapshots it).

* **The Agumix logo, its fades, the opening, the title screen with its menu,
  and every other still picture tried: the same, pixel for pixel**, at 13,
  14, 15.5, 18, 19 (the logo half faded), 22, 25, 28, 32, 37, 42, 52, 62, 63
  and 70 seconds of the oracle (retaken in session 4: session 3's 15.5 was in
  fact taken at 16, its Lua reading whole seconds; all 15 match again).
* **The attract fight** (from about 80 seconds of the oracle): it runs, its
  sprites, the HUD, the backgrounds and their scroll all drawn; the frames
  closest to the oracle's differ in 4 to 7% of their pixels in the first
  bout, then the bouts themselves differ (other fighters, another stage): the
  computer's play depends on timing that is not the oracle's yet.
* **Timing**: the same picture comes sooner here -- 1 second at the logo, 3
  at its fade, 6 to 7 in the opening, 11 at the title. The runtime loads at
  once; MAME reads its CD at the drive's pace (2,048 bytes at 300 kHz per
  sector, by DMA, a status interrupt per sector) and runs DOS and the CD
  BIOS's real-mode code to do it. A "Towns speed" for loads would bring the
  two closer; it is not needed for the pictures.

150 seconds of the game run in 1.9 seconds on this machine (clang -O2,
headless, a frame rendered only when saved).

## The machine, as far as it goes (fmtownskit)

Memory and the descriptors; far calls between the program and TBIOS as C++
calls; the program's interrupt handlers (Phar Lap 2506h) taken at safe points
through level-triggered PICs; VSYNC at 60 Hz, the vertical blank 2.5 ms, the
beam's position for CRTC register 30 and the FM-R status ports; the
free-running microsecond counter; the CRTC, video output and FM-R registers,
the three palettes, the VRAM write mask and its two windows; the sprite
controller (its page flip at VSYNC and its drawing after it, as MAME's); the
sound (session 4, `12-sound.md`: the RF5C68, the YM3438 on ymfm, the CD's
audio, their mix); the pad (session 4). The frame is composed as MAME's `screen_update`
does it (its 16-colour, 256-colour and 15-bit scan lines, layer priority and
transparency): what the oracle shows is what MAME draws, so the runtime draws
it the same way.
