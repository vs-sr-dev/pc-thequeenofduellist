# 05 - Open questions

1. ~~RUN386's selectors~~ -- answered in session 2 (`03-executables.md`).
   Still open: what the P3 header's 0x2009 "extra pages" mean, and the
   wrappers in the Marty's TBIOS (8 KB: what they change for the Marty).
2. **The screen mode**: the logo and the opening run in the 640x480 mode of
   two 16-colour layers TownsOS leaves (video register 0 = 0x15; MAME's
   snapshots, and the runtime's frames, are the CRTC's whole 704x525 frame:
   session 3). Still open: the fight's mode, the layers' colour depths (the `.PX` pictures
   are 16-colour, *inferred*), and what the scroll writes to CRTC
   registers 0x11 and 0x15 do in the fight.
3. **"ま～くん"** (`fs:[0xA0]`, AH 0-3): what it is. The game calls it with
   AX=1, DL=0x10, DH=8 and ESI at a buffer, then writes 8x16 columns to
   VRAM itself: *inferred* the font (ANK/kanji) service.
4. **int FDh** (CX=1000): what TownsOS answers there. Session 3: it comes
   before the text windows are drawn, with AX 5400h, CCCCh, 0100h and 0000h;
   the runtime does nothing and the frames still match the oracle's.
5. **The CD BIOS calls**: 54h (the TOC), 50h (play) and 52h (stop)
   answered in session 3 (`03-executables.md`); 53h and 55h are not met yet,
   nor what byte 0 of the TOC (3) and CX=0xFE01 of a play mean.
6. **The missing pictures** (`d_x_07x`, `d_x_08x`, `n_<fighter>.px`): asked
   for in some mode (the limited version, CG MODE, an ending) or dead
   names? Does the game check the open's result?
7. **The limited version's flags** ([0x20BA]=0xFFFF, [0x63D]=4, [0x61D]=0xA0):
   which is the level cap, which the ending.
8. **The save**: what `A:dueltwn.sav` holds, when it is written (CONFIG?),
   and what the game does when A: has no disk (int 24h fails the call).
9. **The nine CD-DA tracks**: which plays where. Track 10 is the opening's
   and the title's (session 3); track 6 the attract fight's and Stage 1's
   (Shinobu), track 9 (11.5 s) the stage's caption, track 3 the oracle's
   second attract bout (session 4). Tracks 2, 4, 5, 7, 8: the other stages
   and the endings, *inferred*.
10. **The 3 KB of the code range the descent does not reach**: dead code, or
    reached through the 12 indirect transfers?
11. **The attract fight's timing**: its bouts drift from the oracle's (other
    fighters, another stage) as the runtime's timing differs from MAME's --
    loads at once, the 386's clocks a datasheet figure a form, the CD's play
    not timed. Which of these the computer's choices hang on.
12. **The font ROM**: the menus' text comes from it (ANK at +0x3D000, kanji
    at +0x4000), so the port needs the user's own; whether the game needs
    more of it than the menus, and whether a font drawn anew could stand in.
