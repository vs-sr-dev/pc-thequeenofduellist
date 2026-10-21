// The Queen of Duellist, natively: the game's code and TBIOS's, recompiled, on fmtownskit's
// FM Towns runtime. Headless for now: it runs the game from its entry and saves frames.
//
//     tqod --cue "disc/....cue" [--frames N] [--png F,F,...] [--png-every N] [--out DIR]
//          [--font FILE] [--trace-int] [--trace-io]
//
// --font: the Towns' font ROM (FMT_FNT.ROM, 256 KB), which the game reads for its menus' text;
// by default bios/fmtowns/fmt_fnt.rom (the one in MAME's fmtowns set), if it is there.
//
// Frames are counted in VSYNCs from the program's first instruction; on the oracle (MAME's
// fmtowns) that instruction runs 12.0 seconds after power-on, so frame F here is MAME's
// 12.0 + F/60 s.
#include "towns.h"
#include <cstdlib>
#include <cstring>
#include <filesystem>
#include <set>
#include <string>

int main(int argc, char** argv) {
    std::string cue = "disc/Queen of Duellist, The (Japan) (Rev A).cue", out = "build/frames";
    std::string font = "bios/fmtowns/fmt_fnt.rom";
    long frames = 600, every = 0;
    std::set<long> at;
    bool trace_int = false, trace_io = false;
    for (int i = 1; i < argc; ++i) {
        std::string a = argv[i];
        auto next = [&]() -> std::string { if (i + 1 >= argc) { std::fprintf(stderr, "%s: a value\n", a.c_str()); std::exit(2); } return argv[++i]; };
        if (a == "--cue") cue = next();
        else if (a == "--frames") frames = std::atol(next().c_str());
        else if (a == "--out") out = next();
        else if (a == "--png-every") every = std::atol(next().c_str());
        else if (a == "--png") {
            std::string s = next();
            for (size_t p = 0; p < s.size();) {
                size_t q = s.find(',', p);
                at.insert(std::atol(s.substr(p, q - p).c_str()));
                p = q == std::string::npos ? s.size() : q + 1;
            }
        }
        else if (a == "--font") font = next();
        else if (a == "--trace-int") trace_int = true;
        else if (a == "--trace-io") trace_io = true;
        else { std::fprintf(stderr, "unknown option %s\n", a.c_str()); return 2; }
    }

    towns::Machine m;
    std::string err;
    if (!m.disc.open(cue, err)) { std::fprintf(stderr, "%s\n", err.c_str()); return 1; }
    std::vector<uint8_t> exe, tbios;
    if (!m.disc.file("DUEL.EXP", exe) || !m.disc.file("TBIOS.BIN", tbios)) {
        std::fprintf(stderr, "DUEL.EXP or TBIOS.BIN not on the disc\n");
        return 1;
    }
    towns::P3 p;
    if (!towns::parse_p3(exe, p, err)) { std::fprintf(stderr, "DUEL.EXP: %s\n", err.c_str()); return 1; }
    // the recompiled code is this disc's code
    for (auto [name, img] : {std::pair<const char*, const std::vector<uint8_t>*>{"DUEL", &p.image}, {"TBIOS", &tbios}}) {
        const X86Module* mod = x86_module(name);
        uint32_t crc = x86_crc32(img->data(), img->size());
        if (!mod || mod->crc != crc || mod->size != img->size()) {
            std::fprintf(stderr, "%s on this disc is not the one recompiled (crc %08x)\n", name, crc);
            return 1;
        }
    }
    if (FILE* f = std::fopen(font.c_str(), "rb")) {
        m.font.resize(0x40000);
        m.font.resize(std::fread(m.font.data(), 1, m.font.size(), f));
        std::fclose(f);
    } else {
        std::fprintf(stderr, "no font ROM (%s): the menus will have no text\n", font.c_str());
    }
    m.trace_int = trace_int;
    m.trace_io = trace_io;
    std::filesystem::create_directories(out);
    m.on_vsync = [&](towns::Machine& mm) {
        long f = (long)mm.frame;
        if (at.count(f) || (every && f % every == 0)) {
            std::vector<uint32_t> rgb;
            int w, h;
            mm.render(rgb, w, h);
            char name[64];
            std::snprintf(name, sizeof name, "/f%06ld.png", f);
            towns::write_png(out + name, rgb, w, h);
        }
        if (f >= frames) throw towns::Stop{0};
    };

    X86Cpu c;
    towns::boot_run386(m, c, p, tbios);
    X86Func entry = x86_lookup_cs(0x0C, c.eip);
    if (!entry) { std::fprintf(stderr, "no recompiled function at the entry %x\n", c.eip); return 1; }
    int code = 0;
    try {
        entry(c);
        std::fprintf(stderr, "the program returned from its entry\n");
    } catch (const towns::Stop& s) {
        code = s.code;
    }
    std::fprintf(stderr, "%s after %llu frames, %.2f s of the guest (the last safe point %04x:%08x)\n",
                 m.exited ? "exit" : "stopped", (unsigned long long)m.frame, (double)c.clocks / towns::kClock,
                 c.sreg[1], c.eip);
    return m.exited ? 0 : code;
}
