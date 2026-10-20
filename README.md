# pc-thequeenofduellist

A native PC port of **The Queen of Duellist** (Agumix, 1993; FM Towns CD,
also playable on the FM Towns Marty), by static recompilation of its 386
code to C++ on fmtownskit (a submodule at
`fmtownskit/`; `git clone --recursive`). **BYOA**: nothing from the disc
is in this repository; you bring your own.

Status: **session 1** -- the disc identified and read, the program's
surface mapped, the plan written. Nothing runs natively yet.

## The disc

Redump's *Queen of Duellist, The (Japan) (Rev A)* (HME-166A): a cue sheet
and ten track files, in `disc/`. `docs/01-disc-layout.md` has its hashes.

## Tools

```sh
python -m fmtownskit.disc "disc/Queen of Duellist, The (Japan) (Rev A).cue"
python -m fmtownskit.disc "disc/Queen of Duellist, The (Japan) (Rev A).cue" --extract build/disc
python -m fmtownskit.x86map build/disc/DUEL.EXP --seed 103e2,c0b8,c124
python tools/oracle.py --machine fmtmarty --at 5-120/5    # MAME, CHDMAN, FMT_ROMS
```

## Documents

`docs/00-sessions.md` (the log), `01-disc-layout.md`, `02-data-formats.md`,
`03-executables.md`, `04-curiosities.md`, `05-open-questions.md`,
`06-attack-plan.md`, `07-next-session.md`, `10-fmtownskit.md`.

## Licence

MIT (`LICENSE`). The game and its system software are their owners'.
