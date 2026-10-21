# 07 - Next session

Where session 3 left it: the game runs headless on fmtownskit's machine from
its first instruction through the logo, the opening, the title and the
attract fight, and every still picture matches the oracle's pixel for pixel
(`11-runtime.md`). Nothing is heard and nothing can be pressed yet.

Goal: **the sound, for the user's ears, then the window and the pad**.

1. **Sound, headless first** (a WAV next to the frames):
   * the RF5C68: its samples are already kept (`towns::pcm_take`); mix them
     at its 20,833 Hz, with the volume ports (0x4E0-0x4E3);
   * the YM3438: a core for its FM (ymfm, BSD-3, is MAME's own; whatever is
     taken goes in the kit with its licence), its timers and its status, and
     IRQ13 for FM if TBIOS turns it on (the game's handler only acts on PCM);
   * the CD-DA from the image, pregaps included (`Disc::read_audio`), as int
     93h 50h asks, with its end and repeat (CX=0xFE01: to read);
   * held against the oracle's sound: `tools/oracle.py` with `-wavwrite` for
     the same stretch (the logo's jingle, the title's track 10).
2. **The window**: SDL3, the 704x525 frame at an integer scale (or the
   640x480 inside it), sound in real time, the guest clock paced by the
   host's; the pad from the keyboard and a gamepad (the Towns pad: four
   directions, A, B, Run and Select, active low at 0x4D0/0x4D2 as MAME's
   townspad answers through the 0x4D6 mask).
3. **Playable**: a fight from the title, CONFIG, the save (`A:dueltwn.sav` in
   `save/a/`), the endings; the code the descent does not reach found as the
   runtime stops on it (the five routines of 0x980E were found that way).

Worth doing on the way:

* discovery finding lists of code pointers like 0x980E itself (a word that
  points at the start of a decodable function in the code range);
* a "Towns speed" for loads (the CD at the drive's pace), to hold the attract
  fight against the oracle frame by frame (`05-open-questions.md` 11).

Tools: `tools/oracle.py` (`--at`, `--dump`, `--dump-write ADDR=VALUE`: state,
RAM, every device's save items and the video registers through the ports),
`tools/framematch.py`; the build as `11-runtime.md` shows, with MSYS2's clang,
CMake and Ninja on PATH (`export PATH=/c/msys64/mingw64/bin:$PATH`) and, while
the kit is being worked on, `-DFMT_RUNTIME=D:/Homebrew6/fmtownskit/runtime`.
