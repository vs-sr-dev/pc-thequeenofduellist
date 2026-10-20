# 04 - Curiosities

* **Fujitsu's codenames in TBIOS.** Each TBIOS module is marked with a
  version, a date and a name. Most are plain (`graphic`, `mouse`, `sprite`,
  `System`, `warikomi` -- 割り込み, interrupts), but the sound module is
  called **ヤルヤル** ("yaruyaru") and the module behind `fs:[0xA0]`
  **ま～くん** ("ma-kun"). Ma-kun is the oldest module, V31L21 of
  1988-11-29, then the sprite module, V31L22A of 1989-02-10; the rest are
  of autumn 1992.
* **The publisher field** of the volume says `TUJI_CORP`, not Agumix.
* **An HDD install the manual does not mention**: `DUELTWN.TXT` explains it
  as a bonus "for those who understand this document", at their own risk,
  and warns that without the right CD a limited version starts (levels up
  to 3, no ending). The program checks for the CD twice: the CD BIOS, and
  `Q:\AGUMIX.PX`.
* **Ctrl-Break off, critical errors failed**: the first thing the program
  does is run 49 bytes of real-mode code that live at the start of its own
  protected-mode image.
* **The program's credit line** is "version 1.01" on the Rev A disc, whose
  volume is `..._VER2`.
* **Pictures that are not there**: the program names `d_x_07x` and `d_x_08x`
  pictures for every fighter and an `n_<fighter>.px` for four of them,
  none of which is on the disc (`02-data-formats.md`).
