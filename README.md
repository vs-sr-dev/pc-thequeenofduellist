# pc-thequeenofduellist

A native PC port of **The Queen of Duellist** (Agumix, 1993; FM Towns CD,
also playable on the FM Towns Marty), by static recompilation of its 386
code to C++ on fmtownskit (a submodule at
`fmtownskit/`; `git clone --recursive`). **BYOA**: nothing from the disc
is in this repository; you bring your own.

Status: **session 3** -- the game runs, headless, on fmtownskit's FM Towns
runtime: its code and TBIOS's recompiled, from its first instruction through
the Agumix logo, the opening, the title screen and the attract fight, and
every still picture held against MAME's matches pixel for pixel. Nothing is
heard and nothing can be pressed yet: the sound and the window are next.

## The disc

Redump's *Queen of Duellist, The (Japan) (Rev A)* (HME-166A): a cue sheet
and ten track files, in `disc/`. `docs/01-disc-layout.md` has its hashes.

## Tools

```sh
python -m fmtownskit.disc "disc/Queen of Duellist, The (Japan) (Rev A).cue"
python -m fmtownskit.disc "disc/Queen of Duellist, The (Japan) (Rev A).cue" --extract build/disc
python -m fmtownskit.x86map build/disc/DUEL.EXP --seed 103e2,c0b8,c124
python tools/oracle.py --machine fmtmarty --at 5-120/5    # MAME, CHDMAN, FMT_ROMS
python tools/oracle.py --machine fmtowns --dump 20        # CPU state and RAM, for fmtownskit.mamedump
python -m fmtownskit.recomp --out build/recomp --exp duel=build/disc/DUEL.EXP@0c+103e2,c0b8,c124 \
    --raw tbios=build/disc/TBIOS.BIN@110:20-100 --optest --selftest 3
cmake -S build/recomp -B build/recomp/b -G Ninja -DCMAKE_CXX_COMPILER=clang++
ninja -C build/recomp/b && build/recomp/b/selftest build/recomp/selftest/*.txt
# the game, headless (docs/11-runtime.md)
python -m fmtownskit.recomp --out build/game \
    --exp duel=build/disc/DUEL.EXP@0c+103e2,c0b8,c124,11322,11476,111cd,1157f,10ff6 \
    --raw tbios=build/disc/TBIOS.BIN@110:20-100
cmake -S . -B build/rt -G Ninja -DCMAKE_CXX_COMPILER=clang++
ninja -C build/rt && build/rt/tqod --frames 3600 --png-every 60 --out build/frames
python tools/framematch.py build/oracle/cmp/fmtowns build/frames --at 13,15.5,19
```

The menus' text comes from the Towns' font ROM: bring your own
(`--font`, default `bios/fmtowns/fmt_fnt.rom`, the one in MAME's `fmtowns`
set).

## Documents

`docs/00-sessions.md` (the log), `01-disc-layout.md`, `02-data-formats.md`,
`03-executables.md`, `04-curiosities.md`, `05-open-questions.md`,
`06-attack-plan.md`, `07-next-session.md`, `09-recompiler.md`, `10-fmtownskit.md`,
`11-runtime.md`.

## Licence

MIT (`LICENSE`). The game and its system software are their owners'.
