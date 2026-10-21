-- Two notes on the YM3438, written through the io space while the game is quiet (68-72 s of
-- the oracle, between the opening's track and the title's): with --sound-log they are in the
-- log, so the runtime's replay plays them through ymfm and the two WAVs can be held against
-- each other. Channel 1 (port A) algorithm 4, channel 4 (port B) algorithm 7; no timers (the
-- game's IRQ13 handler acknowledges only the PCM).
--     python tools/oracle.py --machine fmtowns --at 75 --sound-log --wav W --lua tools/fmtest.lua
local fio = manager.machine.devices[":maincpu"].spaces["io"]
local function reg(port_b, r, v)
    local a = port_b and 0x4dc or 0x4d8
    fio:write_u8(a, r)
    fio:write_u8(a + 2, v)
end
local function voice(b, algo, fb)
    local ops = {0, 4, 8, 12}
    local mul = {1, 2, 1, 4}
    local tl = algo == 7 and {0x18, 0x20, 0x1c, 0x10} or {0x20, 0x7f, 0x18, 0x00}
    for i, o in ipairs(ops) do
        reg(b, 0x30 + o, mul[i])
        reg(b, 0x40 + o, tl[i])
        reg(b, 0x50 + o, 0x1f)
        reg(b, 0x60 + o, 0x05)
        reg(b, 0x70 + o, 0x02)
        reg(b, 0x80 + o, 0x1f)
        reg(b, 0x90 + o, 0x00)
    end
    reg(b, 0xb0, (fb << 3) | algo)
    reg(b, 0xb4, 0xc0)
end
local steps = {
    {68.0, function() reg(false, 0x22, 0); voice(false, 4, 3); reg(false, 0xa4, 0x22); reg(false, 0xa0, 0x6a); reg(false, 0x28, 0xf0) end},
    {69.0, function() reg(false, 0x28, 0x00) end},
    {70.0, function() voice(true, 7, 0); reg(true, 0xa4, 0x1a); reg(true, 0xa0, 0x44); reg(false, 0x28, 0xf4) end},
    {71.0, function() reg(false, 0x28, 0x04) end},
}
local step = 1
emu.register_frame_done(function()
    if step <= #steps and manager.machine.time:as_double() >= steps[step][1] then
        steps[step][2]()
        step = step + 1
    end
end)
