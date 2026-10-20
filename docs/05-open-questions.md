# 05 - Open questions

1. ~~RUN386's selectors~~ -- answered in session 2 (`03-executables.md`).
   Still open: what the P3 header's 0x2009 "extra pages" mean, and the
   wrappers in the Marty's TBIOS (8 KB: what they change for the Marty).
2. **The screen mode**: which CRTC mode the game sets (MAME's snapshots are
   704x525, the raw frame), the layers' colour depths (the `.PX` pictures
   are 16-colour, *inferred*), and what the scroll writes to CRTC
   registers 0x11 and 0x15 do in the fight.
3. **"ま～くん"** (`fs:[0xA0]`, AH 0-3): what it is. The game calls it with
   AX=1, DL=0x10, DH=8 and ESI at a buffer, then writes 8x16 columns to
   VRAM itself: *inferred* the font (ANK/kanji) service.
4. **int FDh** (CX=1000): what TownsOS answers there.
5. **The CD BIOS calls**: AH=52h, 53h, 54h, 55h with AL=0xC0 -- *inferred*
   CD-DA play, stop, status and resume; their parameters (MSF in BX/CX/DX
   or a buffer at EDI).
6. **The missing pictures** (`d_x_07x`, `d_x_08x`, `n_<fighter>.px`): asked
   for in some mode (the limited version, CG MODE, an ending) or dead
   names? Does the game check the open's result?
7. **The limited version's flags** ([0x20BA]=0xFFFF, [0x63D]=4, [0x61D]=0xA0):
   which is the level cap, which the ending.
8. **The save**: what `A:dueltwn.sav` holds, when it is written (CONFIG?),
   and what the game does when A: has no disk (int 24h fails the call).
9. **The nine CD-DA tracks**: which plays where.
10. **The 3 KB of the code range the descent does not reach**: dead code, or
    reached through the 12 indirect transfers?
