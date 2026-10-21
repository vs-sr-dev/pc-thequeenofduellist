# 12 - The sound, the window and the pad

Session 4. The runtime's sound (`fmtownskit/runtime/towns_sound.cpp`), held
against MAME's `fmtowns` sample by sample; the window and the pad
(`towns_sdl.cpp`); the game played from the title into a fight.

```sh
build/rt/tqod                                   # the window (SDL3), sound and pad
build/rt/tqod --headless --frames 9000 --wav build/sound/rt.wav
python tools/oracle.py --machine fmtowns --at 150 --sound-log --wav build/oracle/sound/towns.wav \
    --out build/oracle/sound/towns
build/rt/tqod --replay-sound build/oracle/sound/towns/sound.log --seconds 150 --wav build/sound/replay.wav
```

## What the game plays (the oracle, its first 150 seconds)

`tools/oracle.py --sound-log` logs every write to ports 0x4C0-0x4FF (the CD
controller, the pad mask, the YM3438, the volumes, the RF5C68) and to the
wave RAM, timed in microseconds; `--wav` keeps MAME's own output
(`-wavwrite`, 48 kHz).

* **The YM3438 is never keyed on.** TBIOS's set-up writes every channel's
  registers and keys them all off, and that is all: no FM in the logo, the
  opening, the title or the attract fight.
* **The music is CD-DA**: the CD controller's command 0x24 (play, status
  asked) at 20.947 s from 45:09:12 to 51:15:10 (track 10, the opening's),
  0xA4 (stop; MAME pauses) at 66.970, 0x24 at 76.419 from 26:31:30 to
  32:18:21 (track 6, the attract fight's), stop at 116.069, 0x24 at 146.953
  from 07:15:45 to 13:49:16 (track 3: the next bout). The runtime's int 93h 50h asks for the same MSFs
  (the third differs as the attract bouts drift, `05-open-questions.md` 11).
* **The PCM is the fight's voices and hits**, from 77 s: channels keyed on
  and off through 0x4F8, their samples streamed into the wave RAM 4 KB at a
  time on the block-end interrupt.
* **The logo has no sound**: the oracle is silent until the opening's track.
* TBIOS sets the volumes: 0x4E3/0x4E2 for the CD's left (4) and right (5) to
  0x3F (0 dB), the others muted.

## The runtime's sound (fmtownskit)

As MAME's driver has it (fmtowns.cpp, rf5c68.cpp, cdda.cpp, read):

* the **RF5C68** at 8 MHz / 384, stepped as an event on the guest clock (its
  IRQ13 at a block's last byte must come on time), a 10-bit DAC;
* the **YM3438**: ymfm's core (Aaron Giles, BSD-3, in `runtime/ymfm/`,
  unchanged from MAME's 3rdparty copy), at 8 MHz / 144, its timers and busy
  flag on the guest clock, its interrupt shared with the PCM's on IRQ13
  (0x4E9 bit 0 and bit 3);
* the **CD's audio** from the image's sectors at 44.1 kHz, a play from a
  sector to a sector both included; the CD's left and right volume as MAME's
  `cdda_db_to_gain` reads 0x4E2/0x4E3;
* the **mix** at 48 kHz: FM and PCM at 1.0, the CD at 0.30, as MAME's routes.

Two things the oracle taught, measured on its WAV:

1. **MAME's streams run at whole rates**: 8,000,000 / 384 is 20,833 Hz for
   MAME, not 20,833.3. At the true rate the replay's PCM drifted against the
   oracle's by 0.04 of a 48 kHz sample every 50 ms (16 ppm); at MAME's it
   holds still (-0.04 samples over the whole stretch). The kit takes MAME's.
2. **MAME's resampling holds each sample and averages it over the output
   frame's span.** Linear interpolation lost the PCM's highs (0.70 of the
   oracle's power at 6-8 kHz, 0.31 at 12-14 kHz: sinc² against MAME's
   sinc · sinc), a plain hold had too many (1.11, 1.38); the averaged hold
   gives 0.98-1.01 in every band from 0 to 24 kHz.

## Held against the oracle

**The replay** (`tqod --replay-sound`): the oracle's sound log played into a
fresh machine's chips at its times, from power-on, the CD's play and stop as
MAME's driver takes the controller's commands. It is the oracle's sound
without the game, so the two WAVs line up sample by sample:

| Stretch | Against MAME's WAV |
|---|---|
| the opening's CD-DA (25-60 s) | correlation 0.9995, gain 1.0004; residual 0.09% of the energy (a lag of 2 samples, MAME's) |
| the attract fight's PCM (88-92 s, the CD taken out) | correlation 0.989, power 0.98-1.01 of the oracle's in every band; residual 2.2%, in the highs: a fraction of a sample of phase (the log's microseconds) |
| two FM notes (68-72 s, `tools/fmtest.lua`: algorithm 4 on channel 1, 7 on channel 4) | residual 0.03% of the energy |

`tools/fmtest.lua` writes the notes from Lua while the game is quiet; the
log has them, so the replay plays them through ymfm: the FM's clock, its two
register ports, its levels and pans in the mix are MAME's.

**The game** (`tqod --headless --wav`): the opening's CD-DA matches the
oracle's at correlation 0.999, gain 1.000, 4.506 s sooner -- exactly the
time the runtime's play call comes sooner (frame 248, 12.308 + 4.133 s,
against MAME's command at 20.947 s): the loads.

## The window and the pad

`fmtownskit/runtime/towns_sdl.cpp` (SDL3 3.4, linked statically: `tqod.exe`
needs no DLL). At each VSYNC: the events, the keyboard and gamepads read as
the Towns pad, the 704x525 frame at the largest whole scale the desktop has
room for (resizable, integer scaling, F11 or Alt+Enter full screen), the
frame's 800 sound frames queued, and the guest held until no more than three
frames of sound wait: the game keeps the sound card's time. Tab held runs
unpaced. 300 frames took 6.3 s from launch (5.0 s of game, SDL's start and
the queue's filling).

The pad (MAME's townspad): active low at 0x4D0/0x4D2, A and B through the
0x4D6 mask, bit 7 read as 0; **Run is left and right at once, Select up and
down at once**. The game reads it itself (0xCDA8: 0x3F to 0x4D6, 0x4D0 and
0x4D2 into AX, `not ax`). Keyboard: arrows, X = A, Z = B, Enter = Run, Right
Shift or Backspace = Select; gamepads: d-pad or left stick, East = A, South
= B, Start = Run, Back = Select (positions: the Towns pad's A is on the
right).

## A glitch MAME has, mended

The user saw it in the window: **the CPU's fighter pushed out at the right,
a column of her sprite at the left edge**, a line lower. It is MAME's
drawing, which the kit had copied: a 16-colour sprite's byte holds two
pixels and MAME clips both at the first one's x, so a mirrored sprite's
second pixel at x 256 is written at the next line's x 0 (the sprite page's
lines are 256 pixels). The kit now clips each pixel at its own x
(`towns_video.cpp`): the column is gone, the sprite's last column at the
right is drawn; 10 frames of 900 in a pushed fight change, only in the two
edge columns, and the 15 still snapshots still match the oracle pixel for
pixel. The oracle itself still shows it: here the port leaves MAME on
purpose.

## Played

`tqod --headless --input F-G:BUTTONS` holds buttons for a run. **A on the
title's START** (frame 2700, Run does nothing there) stops the CD and opens
the fighter select (Miyuki and Emily on the screen); A again: "STAGE 1 Moon
light garden", the opponent's picture (Shinobu), ROUND 1, the fight, ROUND
2, Shinobu's win screen and its line of text -- to 150 s with no fault and
no code missing (the files: `s_miyuki.px`, `s_emily.px`, `stage1.px`,
`st_12.snd`, `d_o_04_z.tib`, `n_13.snd`, `d_o_02_s.px`, `w_09.snd`; the
stage's caption on track 9, 44:47:57 to 45:09:11, then the fight on
track 6).
