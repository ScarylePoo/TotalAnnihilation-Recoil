#!/usr/bin/env python3
"""Extract turret/aim turn speeds from TA COB scripts and Recoil Lua unit scripts.

COB: within each Aim* function, every TURN instruction whose speed operand was a
PUSH_CONSTANT is recorded. COB angular units: 65536 = 360 deg, so deg/s = v / 182.044.
Lua: Turn(piece, axis, angle, speed) with speed in rad/s.
"""
import math, os, re, struct

TURN, PUSH_CONST, PUSH_STATIC, PUSH_LOCAL = 0x10002000, 0x10021001, 0x10021004, 0x10021002
TURN_NOW = 0x1000C000
AXES = {0: 'x', 1: 'y', 2: 'z'}
AIM_RE = re.compile(r'^aim(primary|secondary|tertiary|weapon\d+|fromweapon)?', re.I)


def cstr(d, o):
    return d[o:d.index(b'\0', o)].decode('latin-1')


# opcode -> (inline operand count, stack pops, stack pushes); pops of -1 = take from 2nd operand
OPS = {
    0x10001000: (2, 2, 0), 0x10002000: (2, 2, 0), 0x10003000: (2, 2, 0), 0x10004000: (2, 1, 0),
    0x10005000: (1, 0, 0), 0x10006000: (1, 0, 0), 0x10007000: (1, 0, 0), 0x10008000: (1, 0, 0),
    0x1000A000: (1, 0, 0), 0x1000B000: (2, 1, 0), 0x1000C000: (2, 1, 0), 0x1000D000: (1, 0, 0),
    0x1000E000: (1, 0, 0), 0x1000F000: (1, 1, 0), 0x10011000: (2, 0, 0), 0x10012000: (2, 0, 0),
    0x10013000: (0, 1, 0), 0x10021001: (1, 0, 1), 0x10021002: (1, 0, 1), 0x10021004: (1, 0, 1),
    0x10022000: (0, 0, 0), 0x10023002: (1, 1, 0), 0x10023004: (1, 1, 0), 0x10024000: (0, 1, 0),
    0x10041000: (0, 2, 1), 0x10042000: (0, 1, 1), 0x10043000: (0, 5, 1),
    0x1005A000: (0, 1, 1), 0x10038000: (0, 1, 1),
    0x10061000: (2, -1, 0), 0x10062000: (2, -1, 0), 0x10063000: (2, -1, 0),
    0x10064000: (1, 0, 0), 0x10065000: (0, 1, 0), 0x10066000: (1, 1, 0), 0x10067000: (0, 1, 0),
    0x10068000: (0, 1, 0), 0x10071000: (1, 1, 0), 0x10072000: (1, 1, 0), 0x10082000: (0, 2, 0),
    0x10083000: (0, 3, 0), 0x10084000: (0, 1, 0),
}
for _op in list(range(0x10031000, 0x10038000, 0x1000)) + list(range(0x10051000, 0x1005A000, 0x1000)):
    OPS[_op] = (0, 2, 1)


def cob_aim(path):
    d = open(path, 'rb').read()
    (ver, nscripts, npieces, codelen, nstatics, _u, o_idx, o_names, o_pieces, o_code) = struct.unpack('<10i', d[:40])
    idx = struct.unpack('<%di' % nscripts, d[o_idx:o_idx + 4 * nscripts])
    names = [cstr(d, o) for o in struct.unpack('<%di' % nscripts, d[o_names:o_names + 4 * nscripts])]
    pieces = [cstr(d, o) for o in struct.unpack('<%di' % npieces, d[o_pieces:o_pieces + 4 * npieces])]
    words = struct.unpack('<%dI' % codelen, d[o_code:o_code + 4 * codelen])
    bounds = sorted(set(idx) | {codelen})
    out = []
    for name, start in zip(names, idx):
        if not AIM_RE.match(name):
            continue
        end = bounds[bounds.index(start) + 1]
        i, stack = start, []
        while i < end:
            op = words[i]
            if op not in OPS:
                out.append((name, '?', '?', 'unparsed opcode %#x' % op))
                break
            nops, pops, pushes = OPS[op]
            args = words[i + 1:i + 1 + nops]
            if pops == -1:
                pops = args[1]
            if op == TURN:
                stack.pop() if stack else None          # target
                speed = stack.pop() if stack else None  # speed
                stack[:] = []
                piece, axis = args
                if speed is None:
                    sp = 'expr'
                elif isinstance(speed, tuple):
                    sp = 'var'
                else:
                    sp = round(speed / 182.044, 1)
                out.append((name, pieces[piece].lower() if piece < npieces else '?', AXES.get(axis, '?'), sp))
            else:
                popped = [stack.pop() if stack else None for _ in range(pops)]
                if op == PUSH_CONST:
                    v = args[0]
                    stack.append(v - (1 << 32) if v & 0x80000000 else v)
                elif op in (PUSH_STATIC, PUSH_LOCAL):
                    stack.append(('var',))
                elif pushes:
                    a = popped
                    # fold constant arithmetic (e.g. <30> * 2)
                    if len(a) == 2 and all(isinstance(x, int) for x in a) and op in (0x10031000, 0x10032000, 0x10033000, 0x10034000):
                        b, c = a[1], a[0]
                        v = {0x10031000: b + c, 0x10032000: b - c, 0x10033000: b * c,
                             0x10034000: (b // c if c else 0)}[op]
                        stack.append(v)
                    else:
                        stack.append(('expr',))
            i += 1 + nops
    return out


def lua_aim(path):
    src = open(path, encoding='latin-1').read()
    src = re.sub(r'--\[\[.*?\]\]', '', src, flags=re.S)
    src = re.sub(r'--[^\n]*', '', src)
    consts = {m.group(1): float(m.group(2)) for m in re.finditer(r'local\s+(\w+)\s*=\s*([-\d.]+)\s*\n', src)}
    out = []
    parts = re.split(r'\n\s*(?:local\s+)?function\s+', src)
    for part in parts:
        m = re.match(r'(?:script\.)?(\w+)\s*\(', part)
        if not m or not AIM_RE.match(m.group(1)):
            continue
        for t in re.finditer(r'\bTurn\s*\(\s*(\w+)\s*,\s*(\w)_axis\s*,\s*([^,\n]+|[^,\n]*\([^)\n]*\)[^,\n]*),\s*(.+?)\)\s*(?:--.*)?$', part, re.M):
            sp = t.group(4).strip()
            val = None
            try:
                val = float(eval(sp.replace('math.rad', 'rad').replace('math.pi', 'pi'), {'rad': math.radians, 'pi': math.pi, '__builtins__': {}}, dict(consts)))
            except Exception:
                rad = re.match(r'math\.rad\(\s*([-\d.]+)\s*\)', sp)
                if rad:
                    val = math.radians(float(rad.group(1)))
            speed = round(math.degrees(val), 1) if val is not None else 'var'
            out.append((m.group(1), t.group(1).lower(), t.group(2).lower(), speed))
    return out
