"""The oracle: the game on MAME's FM Towns or FM Towns Marty, with snapshots.

MAME runs headless and unthrottled with its configuration kept under
build/oracle (never the user's own), the CD as a CHD made once from the cue
sheet, and a Lua script that saves a snapshot at each time asked for, in
emulated seconds, then quits. A contact sheet of the snapshots is written
next to them.

    python tools/oracle.py --machine fmtmarty --at 5-120/5
    python tools/oracle.py --machine fmtowns  --at 30,60,90 --out build/oracle/towns

Environment: MAME (mame.exe; default: `mame` on PATH), CHDMAN (likewise),
FMT_ROMS (a directory with fmtowns.zip / fmtmarty.zip; default bios/).
"""
import argparse
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CUE = os.path.join(ROOT, 'disc', 'Queen of Duellist, The (Japan) (Rev A).cue')
CHD = os.path.join(ROOT, 'build', 'oracle', 'tqod.chd')
CHD_SHA1 = '543729bca29f426ceb807eb6ea3e5fc0cfaf064d'   # MAME's software list, tqod

LUA = """local times = {%s}
local i = 1
emu.register_frame_done(function()
    if i <= #times and manager.machine.time.seconds >= times[i] then
        manager.machine.video:snapshot()
        i = i + 1
        if i > #times then manager.machine:exit() end
    end
end)
"""

# At the first frame after AT seconds that ends in protected mode with paging
# on (RUN386 drops to real mode for DOS), the CPU state and physical RAM.
DUMP_LUA = """local at, size, done = %g, %d, false
emu.register_frame_done(function()
    if done or manager.machine.time.seconds < at then return end
    local cpu = manager.machine.devices[":maincpu"]
    if (cpu.state["CR0"].value & 0x80000001) ~= 0x80000001 then return end
    done = true
    local f = io.open("state.txt", "w")
    for k, v in pairs(cpu.state) do f:write(string.format("%%s=%%x\\n", k, v.value)) end
    f:write(string.format("TIME=%%x\\n", math.floor(manager.machine.time.seconds * 1000)))
    f:close()
    local sp, r = cpu.spaces["program"], io.open("ram.bin", "wb")
    for a = 0, size - 1, 0x10000 do r:write(sp:read_range(a, a + 0xffff, 8)) end
    r:close()
    manager.machine:exit()
end)
"""


def times(spec):
    out = []
    for part in spec.split(','):
        if '-' in part:
            span, _, step = part.partition('/')
            a, b = (float(x) for x in span.split('-'))
            t = a
            while t <= b + 1e-9:
                out.append(t)
                t += float(step or 1)
        else:
            out.append(float(part))
    return sorted(out)


def tool(env, name):
    path = os.environ.get(env) or shutil.which(name)
    if not path:
        sys.exit('%s not found: set %s' % (name, env))
    return path


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--machine', default='fmtmarty', help='fmtowns, fmtmarty, fmtmarty2, fmtownsux...')
    ap.add_argument('--at', default='5-120/5', help='seconds: a,b,c or a-b/step')
    ap.add_argument('--out', help='output directory (default build/oracle/<machine>, or dump_<machine>_<t>)')
    ap.add_argument('--dump', type=float, metavar='SECONDS',
                    help='instead of snapshots: state.txt and ram.bin (read with fmtownskit.mamedump)')
    ap.add_argument('--ram', type=lambda x: int(x, 0), default=0x200000, help='bytes of RAM to dump')
    a = ap.parse_args()
    mame = tool('MAME', 'mame')
    work = os.path.join(ROOT, 'build', 'oracle')
    os.makedirs(work, exist_ok=True)
    if not os.path.exists(CHD):
        subprocess.check_call([tool('CHDMAN', 'chdman'), 'createcd', '-i', CUE, '-o', CHD])
    roms = os.environ.get('FMT_ROMS', os.path.join(ROOT, 'bios'))
    if a.dump is not None:
        out = a.out or os.path.join(work, 'dump_%s_%g' % (a.machine, a.dump))
    else:
        out = a.out or os.path.join(work, a.machine)
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    lua = os.path.join(work, 'oracle.lua')
    ts = times(a.at)
    with open(lua, 'w') as f:
        f.write(DUMP_LUA % (a.dump, a.ram) if a.dump is not None else LUA % ', '.join('%g' % t for t in ts))
    cmd = [mame, a.machine, '-rompath', roms, '-cdrom', CHD,
           '-inipath', work, '-cfg_directory', os.path.join(work, 'cfg'),
           '-nvram_directory', os.path.join(work, 'nvram'), '-snapshot_directory', out,
           '-video', 'none', '-sound', 'none', '-nothrottle', '-skip_gameinfo',
           '-autoboot_script', lua]
    subprocess.check_call(cmd, cwd=out if a.dump is not None else work)
    if a.dump is not None:
        print('state.txt and ram.bin in %s' % out)
        return
    snaps = os.path.join(out, a.machine)
    names = sorted(n for n in os.listdir(snaps) if n.endswith('.png'))
    print('%d snapshots in %s' % (len(names), snaps))
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return
    cols, w, h = 6, 320, 240
    rows = (len(names) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * w, rows * (h + 14)), (40, 40, 40))
    dr = ImageDraw.Draw(sheet)
    for i, (n, t) in enumerate(zip(names, ts)):
        im = Image.open(os.path.join(snaps, n)).convert('RGB')
        x, y = (i % cols) * w, (i // cols) * (h + 14)
        sheet.paste(im.resize((w, h)), (x, y + 14))
        dr.text((x + 4, y + 1), '%gs  %dx%d' % (t, im.width, im.height), fill=(255, 255, 0))
    sheet.save(os.path.join(out, 'sheet.png'))
    print(os.path.join(out, 'sheet.png'))


if __name__ == '__main__':
    main()
