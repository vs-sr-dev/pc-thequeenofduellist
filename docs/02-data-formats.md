# 02 - The data formats, at a first look

Every file of the data track that is not system software is the game's.
This is a first look at their first bytes and their names, to be read
properly as the port reaches each one; nearly everything here is
*inferred*.

| Kind | Files | What they look like |
|---|---|---|
| `.SND` | 43 | headerless 8-bit samples whose silence is 0x80/0x81 and whose small values are 0x03, 0x04: **sign-magnitude, the RF5C68's own sample format** (*inferred*). Names by kind: `E_` (6), `L_` (9), `N_` (10), `ST_` (6), `W_` (12) |
| `.PCL` | 8 | 8-bit unsigned samples around 0x80 (*inferred*), one per fighter plus `SE.PCL` and `SET.PCL`: voices and effects as a bank |
| `.PX` | 38 | Agumix's picture format: width and height as big-endian words, then 48 bytes (*inferred*: 16 colours as RGB bytes, 4 bits used), then compressed pixels. Sizes: 640x400 screens (title, stages, VS screens, continue), 320x320 and 320x400 portraits, 512x320, 640x80 (`SELECT.PX`), 304x116 (`AGUMIX.PX`, the logo) |
| `.TIB` | 18 | "TIB0", then (big-endian) 640 and 400: three per fighter, `D_x_04_Z` to `06_Z` (*inferred*: the large pictures; Z for their size) |
| `.SPT` | 9 | one per fighter, plus `LOGO`, `DEMO`, `MISC`: *inferred* sprite patterns for the sprite controller |
| `.MOT` | 6 | per fighter, a table of big-endian word offsets first: *inferred* motion scripts |
| `.BG` | 6 | per fighter: *inferred* the stage background |
| `.HCK` | 6 | per fighter, zeros first: *inferred* hit-check boxes |
| `.THK` | 6 | per fighter, pairs of little-endian words: *inferred* another table |
| `.ANM` | 1 | `EOP.ANM` ("C1" first): *inferred* the ending's animation |
| `.L` | 1 | `OPANM.L`: an archive whose index names `U_A_1B.PX`, `U_B_1B.PX`, ... with offsets: the opening |
| `DRIVE_R.IMG` | 1 | 131,072 bytes: *inferred* a RAM-drive image for the system |

The six fighters, from the per-character file sets and the strings in
`DUEL.EXP`: **Miyuki** (`D_U_`), **Emily** (`D_M_`), **Ryuhou** (`D_R_`),
**Shinobu** (`D_O_`), **Marcia** (`D_Z_`), **Katana** (`D_N_`); each has a
stage (`STAGE0` to `STAGE5`).

## Files the program names that are not on the disc

`DUEL.EXP` carries the names of files the disc does not have:
`d_u_07x.tib`, `d_u_08x.tib`, `d_m_07x.px`, `d_m_08x.px` and their
counterparts for the four other fighters, `n_ryuhou.px`, `n_shinob.px`,
`n_marcia.px`, `n_katana.px`, and `u_a_1b.px`, `u_b_1b.px`, `mop1.anm`,
`mop2.anm`, `u_c.px` to `u_f.px`, `m_c8_1.px`, `m_c_1.px` to `m_c_4.px`
(these with `opanm.l` and `eop.anm`: *inferred* the parts of the opening
inside `OPANM.L`, whose index has the same names). Whether the 07x/08x
pictures are ever asked for, and what the game does without them, is for
the oracle and the trace (`05-open-questions.md`).

## Text

`DUELTWN.TXT` (Shift-JIS) is the hard-disk installation note
(`01-disc-layout.md`). The in-game text of the character profiles (seen in
the oracle: name, age, height, the illustrator) is drawn, not yet found as
text.
