# 07 - Next session

Where session 4 left it: the game runs in a window with its sound and the
pad (`build/rt/tqod`), and headless for checks. Its sound is MAME's sample
for sample where it can be compared (`12-sound.md`); a fight was played from
the title through two rounds and the opponent's win screen. Nothing yet past
the first stage, nor the save.

Goal: **playable to the end**.

1. **The user's eyes and ears on the window**: the picture's scale, the
   sound's latency (three frames queued), the keys and the gamepad mapping
   (X = A, Z = B, Enter = Run; East = A, South = B), and anything that sounds
   or looks other than the Towns.
2. **The game played through**, headless with `--input` and by hand: the
   fighter select's both sides, every stage and opponent, the endings, VS
   MODE (two pads), CONFIG, CG MODE; each new file and CD-DA track noted
   (`05-open-questions.md` 9); the code the descent does not reach found as
   the runtime stops on it (seeds, as 0x980E's).
3. **The save** (`A:dueltwn.sav`, in `save/a/`): when it is written and what
   it holds (`05-open-questions.md` 8).
4. **The CD BIOS's other calls** if the game makes them: 53h and 55h (a
   status, *inferred*: the end of a track; the code at 0xC778 and 0xC796),
   and what a play's CX=0xFE01 asks (a repeat?) once a track is let run out.

Worth doing on the way:

* the window: a choice of the 640x480 inside the frame (the game draws in
  x 42-681, y 33-480 of the 704x525), smooth scaling, a key for a PNG;
* a "Towns speed" for loads, to hold the attract fight against the oracle
  (`05-open-questions.md` 11);
* the README's sweep before publishing (no personal paths), on the user's
  word.

Tools: `tools/oracle.py` (`--at`, `--dump`, `--dump-write`, `--wav`,
`--sound-log`, `--lua`), `tools/framematch.py` (the entry at 12.308 s),
`tqod --headless --input F-G:BUTTONS --trace-int --trace-from F`,
`tqod --replay-sound LOG`; the build as `11-runtime.md` shows, with MSYS2's
clang, CMake, Ninja and SDL3 (its mingw64 `bin` first on the PATH).
