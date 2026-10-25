"""Compiled COB script reader: piece names and what the script does to each piece.

TA:Recoil ships compiled .cob files without their BOS sources, so the piece usage summary (what turns/moves on
which axis, what is hidden/shown, exploded, emitted from, queried) is read from the bytecode. Opcodes and their
inline operand counts are taken from the Recoil engine (rts/Sim/Units/Scripts/CobOpCodes.h and CobThread.cpp).
"""
import struct

# opcode -> (name, number of inline operands that follow the opcode word)
OPS = {
    0x10001000: ('move', 2), 0x10002000: ('turn', 2), 0x10003000: ('spin', 2), 0x10004000: ('stop-spin', 2),
    0x10005000: ('show', 1), 0x10006000: ('hide', 1), 0x10007000: ('cache', 1), 0x10008000: ('dont-cache', 1),
    0x1000B000: ('move', 2), 0x1000C000: ('turn', 2),            # move-now / turn-now: same usage as move/turn
    0x1000D000: ('shade', 1), 0x1000E000: ('dont-shade', 1), 0x1000F000: ('emit-sfx', 1),
    0x100A0000: ('scale', 1), 0x100A1000: ('scale', 1), 0x100A2000: ('wait-scale', 1),
    0x10011000: ('wait-turn', 2), 0x10012000: ('wait-move', 2), 0x10013000: ('sleep', 0),
    0x10021001: ('pushc', 1), 0x10021002: ('pushl', 1), 0x10021004: ('pushs', 1), 0x10022000: ('clv', 0),
    0x10023002: ('popl', 1), 0x10023004: ('pops', 1), 0x10024000: ('pop-stack', 0),
    0x10031000: ('add', 0), 0x10032000: ('sub', 0), 0x10033000: ('mul', 0), 0x10034000: ('div', 0),
    0x10034001: ('mod', 0), 0x10035000: ('and', 0), 0x10036000: ('or', 0), 0x10037000: ('xor', 0),
    0x10038000: ('not', 0), 0x10041000: ('rand', 0), 0x10042000: ('get-unit-value', 0), 0x10043000: ('get', 0),
    0x10051000: ('lt', 0), 0x10052000: ('le', 0), 0x10053000: ('gt', 0), 0x10054000: ('ge', 0),
    0x10055000: ('eq', 0), 0x10056000: ('ne', 0), 0x10057000: ('land', 0), 0x10058000: ('lor', 0),
    0x10059000: ('lxor', 0), 0x1005A000: ('lnot', 0),
    0x10061000: ('start', 2), 0x10062000: ('call', 2), 0x10062001: ('call', 2), 0x10062002: ('lua-call', 2),
    0x10062004: ('batch-lua', 2), 0x10064000: ('jump', 1), 0x10065000: ('return', 0), 0x10066000: ('jne', 1),
    0x10067000: ('signal', 0), 0x10068000: ('set-signal-mask', 0),
    0x10071000: ('explode', 1), 0x10072000: ('play-sound', 1),
    0x10082000: ('set', 0), 0x10083000: ('attach', 0), 0x10084000: ('drop', 0),
    0x10090000: ('lua-signature', 0),
}
PIECE_OPS = {'move', 'turn', 'spin', 'stop-spin', 'show', 'hide', 'cache', 'dont-cache', 'shade', 'dont-shade',
             'emit-sfx', 'scale', 'explode'}
AXES = 'xyz'


def _cstr(d, o):
    return d[o:d.index(b'\0', o)].decode('latin-1')


def read(path):
    """-> dict(pieces=[...], scripts={name: [(op, operands), ...]}, unknown=[opcode, ...])"""
    d = open(path, 'rb').read()
    (ver, nscr, npc, codelen, nstatic, _u2, o_codeidx, o_scrnames, o_pcnames, o_code) = struct.unpack('<10i', d[:40])
    if ver not in (4, 6):
        raise ValueError(f'{path}: not a COB file (version {ver})')
    code = struct.unpack(f'<{codelen}i', d[o_code:o_code + codelen * 4])
    names = [_cstr(d, struct.unpack_from('<i', d, o_scrnames + 4 * i)[0]) for i in range(nscr)]
    starts = [struct.unpack_from('<i', d, o_codeidx + 4 * i)[0] for i in range(nscr)]
    pieces = [_cstr(d, struct.unpack_from('<i', d, o_pcnames + 4 * i)[0]).lower() for i in range(npc)]
    bounds = sorted(set(starts + [codelen]))
    scripts, unknown = {}, []
    for name, s in zip(names, starts):
        e = next(b for b in bounds if b > s) if s < codelen else s
        ins, pc = [], s
        while pc < e:
            op = code[pc]
            if op not in OPS:
                # some compilers leave data after a script's final return (e.g. ARM_T1_BOT_Hammer's Killed);
                # the engine never executes it, so only an unknown opcode inside live code is an error
                if not (ins and ins[-1][0] == 'return'):
                    unknown.append(op)
                break
            nm, n = OPS[op]
            ins.append((nm, code[pc + 1:pc + 1 + n])); pc += 1 + n
        scripts[name] = ins
    return dict(pieces=pieces, scripts=scripts, unknown=unknown)


def summary(path):
    """(pieces, {piece: sorted usage}) in the same form as the old BOS summary."""
    c = read(path)
    P = c['pieces']
    use = {p: set() for p in P}
    for name, ins in c['scripts'].items():
        q = name.lower().startswith(('query', 'aimfrom', 'sweetspot'))
        for i, (nm, ops) in enumerate(ins):
            if nm in PIECE_OPS and ops and 0 <= ops[0] < len(P):
                tag = nm
                if nm in ('move', 'turn', 'spin', 'stop-spin') and len(ops) > 1 and 0 <= ops[1] < 3:
                    tag = f'{nm} {AXES[ops[1]]}'
                use[P[ops[0]]].add(tag)
            # Query*/AimFrom* return the piece number through the argument: pushc <piece>; popl <arg>
            if q and nm == 'pushc' and i + 1 < len(ins) and ins[i + 1][0] in ('popl', 'pops') \
                    and 0 <= ops[0] < len(P):
                use[P[ops[0]]].add('query/aimfrom')
    return P, {k: sorted(v) for k, v in use.items()}


def dump(path):
    """Readable listing (for porting a COB to a Lua unit script): one line per instruction, piece names and axes
    resolved, constants shown as integers and as COB linear (/65536 elmo) or angular (*360/65536 deg) values."""
    c = read(path)
    P = c['pieces']
    out = [f'-- {path}', f'-- pieces: {", ".join(P)}']
    for name, ins in c['scripts'].items():
        out.append(f'\n{name}:')
        pc = 0
        for nm, ops in ins:
            if nm in PIECE_OPS or nm in ('wait-turn', 'wait-move'):
                arg = P[ops[0]] if ops and 0 <= ops[0] < len(P) else ops
                ax = f' {AXES[ops[1]]}-axis' if len(ops) > 1 and 0 <= ops[1] < 3 else ''
                out.append(f'  {pc:4d} {nm} {arg}{ax}')
            elif nm == 'pushc':
                v = ops[0]
                out.append(f'  {pc:4d} pushc {v}  (lin {v / 65536:.3f}, ang {v * 360 / 65536:.2f}deg)')
            elif nm in ('start', 'call', 'lua-call'):
                out.append(f'  {pc:4d} {nm} {list(c["scripts"])[ops[0]] if 0 <= ops[0] < len(c["scripts"]) else ops[0]} args={ops[1]}')
            else:
                out.append(f'  {pc:4d} {nm} {" ".join(map(str, ops))}'.rstrip())
            pc += 1 + len(ops)
    return '\n'.join(out)


if __name__ == '__main__':
    import sys
    print(dump(sys.argv[1]))
