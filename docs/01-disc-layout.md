# 01 - The disc

## Which disc this is

| | |
|---|---|
| Title | クイーン・オブ・デュエリスト / The Queen of Duellist |
| Publisher, developer | Agumix (the volume's publisher field says `TUJI_CORP`) |
| Platform | FM Towns CD (runs on the FM Towns Marty: below) |
| Serial | **HME-166A**: the second pressing (Redump's "Rev A"); the first is HME-166 |
| Volume | `THE_QUEEN_OF_DUELLIST_VER2`, system id `HME-166`, mastered by "FUJITSU LTD HYPER MEDIA DEVELOPMENT CENTER", dated 1993-07-13 11:00 |
| Release | the FM Towns version came out on 1993-06-28 (a Japanese software list); the Rev A's volume is dated two weeks later |
| The program | `DUEL.EXP`: "Queen of Duellist for FM-TOWNS version 1.01, Copyright (c) 1993 AGUMIX." |

Checked: every track's CRC32 is the one MAME's software list (`fmtowns_cd.xml`,
entry `tqod`, "The Queen of Duellist (HME-166A)", origin redump.org) gives,
and the CHD made from the cue sheet has the list's SHA-1
(`543729bca29f426ceb807eb6ea3e5fc0cfaf064d`).

### Towns or Marty?

The question asked at the start: is this the "FM Towns Marty version"? It is
the **standard FM Towns CD, which runs on the Marty**; no separate Marty
edition of this game is known:

* MAME's software list and Redump mark the Marty-specific releases they know
  in their names and notes ("4D Driving (FM Towns Marty Rerelease)", "Only
  works on the 386SX-based models (Marty/UX)", "(Marty-compatible)"). Both
  pressings of this game are plain entries: `tqod` (HME-166A) and its parent
  `tqodo` (HME-166), each with "Requires 2 MB RAM" -- the Marty's memory.
* Nothing on the disc names the Marty: no "MARTY" in any file, and the
  program reads no machine id (port 0x31 is not among the ports it touches,
  `03-executables.md`).
* It runs on the Marty: on MAME's `fmtmarty` it boots past the Marty's logo
  to Agumix's, plays its opening, shows its title menu and runs its attract
  battle in the same order as on `fmtowns`, a little later in time (the
  Marty's 386SX is slower). `tools/oracle.py` takes both.

What differs between the two pressings, from the list: the first (HME-166)
came with a **User Disk** (a floppy, `the queen of duellist (user disk).hdm`)
and the note "Mouse must not be connected to port 2". By the list's file
sizes, its data track is 6,600 sectors to the Rev A's 6,750 and its track
2 file 150 sectors longer (the same 150 sectors on the other side of the
boundary), its last track one sector shorter, and tracks 3 to 9 the same
length. The Rev A saves to `A:dueltwn.sav` when it runs from the CD (the
program puts the current drive's letter in place of the "A" unless that
drive is Q:, the CD). *Inferred*: A: is the floppy drive, and the Rev A
did away with the separate User Disk.

## The tracks

`python -m fmtownskit.disc "disc/Queen of Duellist, The (Japan) (Rev A).cue"`:

| Track | Mode | First sector (INDEX 01) | Sectors | Length | Pregap |
|---|---|---|---|---|---|
| 01 | MODE1/2352 | 0 | 6,750 | 1:30.00 | 0 |
| 02 | AUDIO | 7,095 | 24,610 | 5:28.13 | 345 |
| 03 | AUDIO | 32,520 | 28,940 | 6:25.87 | 815 |
| 04 | AUDIO | 62,042 | 27,603 | 6:08.04 | 582 |
| 05 | AUDIO | 90,337 | 28,120 | 6:14.93 | 692 |
| 06 | AUDIO | 119,205 | 25,635 | 5:41.80 | 748 |
| 07 | AUDIO | 145,222 | 27,458 | 6:06.11 | 382 |
| 08 | AUDIO | 173,397 | 27,423 | 6:05.64 | 717 |
| 09 | AUDIO | 201,432 | 863 | 0:11.51 | 612 |
| 10 | AUDIO | 203,037 | 27,449 | 6:05.99 | 742 |

* The ISO volume is 2,932 blocks; the data track's other 3,818 sectors are
  all zero.
* The pregaps are long (4.6 to 10.9 seconds) and **seven of the nine hold
  audio** (tracks 3, 4, 5, 7, 8, 9, 10; tracks 2 and 6 are nearly silent).
  The CD BIOS plays by position, so a runtime serves the disc as one run of
  sectors with the pregaps in it.
* Nine CD-DA tracks: *inferred* the music (six fighters, menus, ending); to
  match to scenes in the oracle.

## The data track

167 files in 4 directories (`build/disc` after `--extract`), all dated
1993-07-13 10:41:40. Sector 0 is the IPL (`IPL4`, then a jump to +0x5B);
sectors 1-15 are zero.

The boot chain, as the files say it:

| Step | File | What it is |
|---|---|---|
| 1 | sector 0 | the IPL: real-mode code that compares 0040:0000 with "FBIOS", the first bytes of `IO.SYS` |
| 2 | `IO.SYS` (77,824) | Towns-DOS: "IO.SYS ( BIOS ) Multi-Mode Display Type, BIOS Version 3.58, 1992-12-15" |
| 3 | `CONFIG.SYS` | `SHELL=C:\COMMAND.COM C:\ /P`, `DEVICE=\SYS\CTL.SYS`, `DEVICE=\TBIOS.SYS /TBIOS.BIN /D`, `DEVICE=\TOWNS.SYS`, `BUFFERS=8`, `FILES=20` |
| 4 | `TBIOS.SYS` (7,050) | "Towns-BIOS Loader for TownsOS Version2.1", V31L35, 1992-10-02: loads `TBIOS.BIN` |
| 5 | `TBIOS.BIN` (94,208) | the protected-mode BIOS, "V31L31 92/11/11": `03-executables.md` |
| 6 | `TOWNS.SYS` (2,829) | an MZ driver; strings `GAIJI`, `A:OAK2USR.DIC` (the user's extra characters and kana-kanji dictionary) |
| 7 | `AUTOEXEC.BAT` | `SET TOMH=Q:\HELP`, `SET ICN=Q:\`, `\HCOPY\COCO`, `duel.com` |
| 8 | `HCOPY\COCO.EXE` | *inferred*: a resident screen hard-copy tool (the directory's name; `NSDDLOAD`, `FORRBIOS.NSD` beside it) |
| 9 | `DUEL.COM` (199) | shrinks itself (4Ah), points int 24h at a handler that fails the call, opens `A:DUEL.EXP`: if it opens, runs `RUN386.EXE A:DUEL.EXP`, otherwise `RUN386.EXE DUEL.EXP` |
| 10 | `RUN386.EXE` (78,496) | "386\|DOS-Extender Version 1.2aJ L50, Phar Lap Software, Inc. and Fujitsu Ltd." |
| 11 | `DUEL.EXP` (74,007) | the game |

`DUEL.BAT` (`RUN386 DUEL`) is for the hard-disk installation that
`DUELTWN.TXT` describes (*not in the manual*: copy the CD's root to a
directory and run `duel.bat` with the CD in the drive; without the right CD
a **limited version** starts -- game level up to 3 only, no ending). The
CD is Q: (`AUTOEXEC.BAT`'s variables, and the program's own test of the
current drive).

`HELP\` holds `SYSTEM1/3/5.HDT` and `T_SYS.HIX`: *inferred* TownsOS's help
files, there for the system software. Everything else is the game's
(`02-data-formats.md`).
