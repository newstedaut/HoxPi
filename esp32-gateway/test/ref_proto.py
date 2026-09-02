#!/usr/bin/env python3
"""Referenzausgabe fuer test_proto.c — nutzt die ECHTEN Funktionen aus bridge/hoval_bridge.py
(decode_value, to_registers, Konstanten) und baut GET/SET-Frames genau wie poll_targets()/on_write().
`make test` vergleicht diese Ausgabe mit der des C-Programms (die Zeilen bis vor 'REASM')."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "bridge"))
import hoval_bridge as hb  # noqa: E402


def get(fg, fn, dp):
    return bytes([0x01, hb.OP_GET, fg & 0xFF, fn & 0xFF, (dp >> 8) & 0xFF, dp & 0xFF])


def sett(fg, fn, dp, typ, v):
    data = bytes([v & 0xFF]) if typ in ("U8", "S8", "LIST") else bytes([(v >> 8) & 0xFF, v & 0xFF])
    return bytes([0x01, hb.OP_SET, fg & 0xFF, fn & 0xFF, (dp >> 8) & 0xFF, dp & 0xFF]) + data


def hexline(tag, b):
    print(tag + "".join(" %02x" % x for x in b))


def arb(unit_id, write):
    if unit_id == 520:
        return hb.ARB_HV_POLL
    return hb.ARB_WRITE if write else hb.ARB_POLL


hexline("GET 1-0-2051     ", get(1, 0, 2051))
hexline("GET 60-254-27    ", get(60, 254, 27))
hexline("GET 50-0-40650   ", get(50, 0, 40650))
hexline("SET LIST 4       ", sett(1, 0, 3050, "LIST", 4))
hexline("SET S16 250      ", sett(1, 0, 7036, "S16", 250))
hexline("SET S16 0        ", sett(1, 0, 7036, "S16", 0))
hexline("SET S16 80       ", sett(2, 0, 5077, "S16", 80))
hexline("SET S16 -100     ", sett(1, 0, 3051, "S16", -100 & 0xFFFF))
hexline("SET U8 255       ", sett(60, 254, 27, "U8", 255))
print("ARB WEZ read  %08x" % arb(1, False))
print("ARB WEZ write %08x" % arb(1, True))
print("ARB HV read   %08x" % arb(520, False))
print("ARB HV write  %08x" % arb(520, True))
print("ARB PS write  %08x" % arb(143, True))

DEC = [("U8", b"\x16"), ("S8", b"\xF6"), ("U16", b"\x01\x2C"), ("S16", b"\xFF\x9C"),
       ("S16", b"\x80\x00"), ("LIST", b"\x00\x04"), ("U32", b"\x00\x01\x19\x2B"),
       ("S32", b"\xFF\xFF\xFF\x38"), ("U32", b"\x12\x34\x56\x78"),
       ("U16", b"\xFF\xFF"), ("S16", b"\x05"), ("U32", b"\x01\x02")]
for t, b in DEC:
    v = hb.decode_value(t, b)
    regs = hb.to_registers(t, v)
    print("DEC %-4s%s -> %d regs %s" % (t, "".join(" %02x" % x for x in b), v, " ".join(str(w) for w in regs)))


def chk(typ, v):   # Bereichspruefung in on_write(): S16-Sicht auf das Modbus-Wort
    return v - 65536 if (typ == "S16" and v > 32767) else v


print("CHK S16 65436 -> %d" % chk("S16", 65436))
print("CHK S16 250 -> %d" % chk("S16", 250))
print("CHK U16 65436 -> %d" % chk("U16", 65436))
