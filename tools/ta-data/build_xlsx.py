#!/usr/bin/env python3
"""Build the TA 3.1c vs TA:Recoil review workbook from finalize.py output."""
import csv, os, statistics, sys
from collections import defaultdict
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.comments import Comment

CMP, OUT = sys.argv[1], sys.argv[2]
FONT = 'Arial'
H = Font(name=FONT, bold=True, color='FFFFFF')
HFILL = PatternFill('solid', start_color='2F3B4C')
INFILL = PatternFill('solid', start_color='FFF2CC')
KINDFILL = {'Balance': None, 'Convention': PatternFill('solid', start_color='EDEDED'),
            'Recoil-only tag': PatternFill('solid', start_color='EDEDED'), 'Note': PatternFill('solid', start_color='FCE4D6')}
thin = Side(style='thin', color='BFBFBF')
DECISIONS = '"Revert to TA,Keep repo,Custom value,Not applicable"'


def numify(v):
    if v in ('', None):
        return None
    try:
        f = float(v)
        return int(f) if f == int(f) else f
    except ValueError:
        return v


def table(ws, headers, rows, widths, pct_col=None, text_cols=()):
    ws.append(headers)
    for c in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=c)
        cell.font = H; cell.fill = HFILL
        cell.alignment = Alignment(vertical='center', wrap_text=True)
    for r in rows:
        ws.append(r)
    n = len(rows) + 1
    for row in ws.iter_rows(min_row=2, max_row=n):
        kind = row[headers.index('Kind')].value if 'Kind' in headers else None
        for cell in row:
            cell.font = Font(name=FONT, size=10)
            if KINDFILL.get(kind):
                cell.fill = KINDFILL[kind]
        if pct_col is not None:
            row[pct_col].number_format = '+0.0%;-0.0%;0.0%'
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = 'A2'
    ws.auto_filter.ref = 'A1:%s%d' % (get_column_letter(len(headers)), n)
    ws.row_dimensions[1].height = 30
    return n


wb = Workbook()
readme = wb.active
readme.title = 'Read Me'

# ---------------- Units
units = list(csv.DictReader(open(f'{CMP}/units_final.csv')))
ws = wb.create_sheet('Units')
hdr = ['Repo unit', 'TA id', 'Group', 'Stat', 'Tag', 'TA 3.1c', 'Repo', 'Change', 'Status', 'Kind', 'Decision', 'Notes']
rows = []
for u in sorted(units, key=lambda r: (r['kind'] != 'Balance', r['unit'], r['group'], r['stat'])):
    pct = numify(u['pct'])
    rows.append([u['unit'], u['ta_id'], u['group'], u['stat'], u['tag'], numify(u['ta']), numify(u['repo']),
                 pct / 100 if isinstance(pct, (int, float)) else None, u['status'], u['kind'], None, None])
nu = table(ws, hdr, rows, [34, 10, 11, 22, 30, 11, 11, 9, 16, 15, 15, 30], pct_col=7)
for r in range(2, nu + 1):
    ws.cell(row=r, column=11).fill = INFILL
    ws.cell(row=r, column=12).fill = INFILL
dv = DataValidation(type='list', formula1=DECISIONS, allow_blank=True)
ws.add_data_validation(dv); dv.add('K2:K%d' % nu)

# ---------------- Weapons
weaps = list(csv.DictReader(open(f'{CMP}/weapons_final.csv')))
ww = wb.create_sheet('Weapons')
hdr = ['Repo weapon', 'TA weapon', 'Repo file', 'Stat', 'Tag', 'TA 3.1c', 'Repo', 'Change', 'Status', 'Kind',
       'Used by', 'Decision', 'Notes']
rows = []
for w in sorted(weaps, key=lambda r: (r['kind'] != 'Balance', r['weapon'], r['stat'])):
    pct = numify(w['pct'])
    rows.append([w['weapon'], w['ta_weapon'], w['file'], w['stat'], w['tag'], numify(w['ta']), numify(w['repo']),
                 pct / 100 if isinstance(pct, (int, float)) else None, w['status'], w['kind'],
                 w['used_by'].replace(' ', ', '), None, None])
nw = table(ww, hdr, rows, [30, 22, 26, 20, 18, 20, 20, 9, 26, 15, 40, 15, 30], pct_col=7)
for r in range(2, nw + 1):
    ww.cell(row=r, column=12).fill = INFILL
    ww.cell(row=r, column=13).fill = INFILL
    ww.cell(row=r, column=9).alignment = Alignment(wrap_text=False)
dv2 = DataValidation(type='list', formula1=DECISIONS, allow_blank=True)
ww.add_data_validation(dv2); dv2.add('L2:L%d' % nw)

# ---------------- Turret speeds
aim = []
for a in csv.DictReader(open(f'{CMP}/aim_diff.csv')):
    pct = numify(a['pct'])
    if isinstance(pct, (int, float)) and abs(pct) < 1:
        continue  # compiler rounding (e.g. 300 -> 299.9)
    ta_s, rp_s = numify(a['ta_speed']), numify(a['repo_speed'])
    if isinstance(ta_s, (int, float)) and isinstance(rp_s, (int, float)):
        status = 'changed'
    elif '(no constant speed)' in (ta_s, rp_s):
        status = 'speed computed in script'
    else:
        status = 'piece renamed/moved: pair by hand'
    aim.append([a['unit'], a['ta_id'], a['script'], a['piece'], a['axis'], ta_s, rp_s,
                pct / 100 if isinstance(pct, (int, float)) else None, status,
                a['ta_pieces'], a['repo_pieces'], None, None])
wa = wb.create_sheet('Turret Speeds', 3)
hdr = ['Repo unit', 'TA id', 'Script', 'Piece', 'Axis', 'TA 3.1c (deg/s)', 'Repo (deg/s)', 'Change', 'Status',
       'TA pieces', 'Repo pieces', 'Decision', 'Notes']
na = table(wa, hdr, aim, [32, 10, 7, 12, 14, 12, 12, 9, 18, 18, 18, 15, 30], pct_col=7)
for rr in range(2, na + 1):
    wa.cell(row=rr, column=12).fill = INFILL
    wa.cell(row=rr, column=13).fill = INFILL
dv3 = DataValidation(type='list', formula1=DECISIONS, allow_blank=True)
wa.add_data_validation(dv3); dv3.add('L2:L%d' % na)

# ---------------- Mapping
mp = list(csv.DictReader(open(f'{CMP}/unit_mapping.csv')))
wm = wb.create_sheet('Unit Mapping')
rows = [[m['repo_file'], m['ta_id'], m['matched_by'], m['model_vs_ta']] for m in sorted(mp, key=lambda m: m['repo_file'])]
table(wm, ['Repo unit', 'TA id', 'Matched by', 'Model vs TA original'], rows, [36, 12, 12, 22])

# ---------------- Read Me
r = readme
r.column_dimensions['A'].width = 34
for c in 'BCDE':
    r.column_dimensions[c].width = 16
r['A1'] = 'TA 3.1c vs TA:Recoil — unit and weapon stat review'
r['A1'].font = Font(name=FONT, bold=True, size=14)
lines = [
    'Source: Cavedog archives totala1.hpi, ccdata.ccx, btdata.ccx, Cavedog_units.ufo and rev31.gp3 (3.1c patch), '
    'layered in that order. Compared against TotalAnnihilation-Recoil @ %s.' % os.environ.get('TA_REPO_REV', 'unknown'),
    'Each row is one stat that differs. "Change" is the repo value relative to TA (+40% = repo is 40% higher).',
    'Kind: Balance = a gameplay value differs. Convention = same behaviour written the Recoil way (weapontype instead '
    'of lineofsight/beamweapon, engine defaults). Recoil-only tag = repo sets a tag TA never had. Grey rows are not balance.',
    'Movement rows compare the effective slope/depth/footprint after resolving each side\'s movement class.',
    'Cannon "Projectile speed" rows are marked: BOTA\'s weapondefs_post.lua recomputes cannon velocity from range '
    'and gravity at load, so the def value is not what the game uses.',
    'To fill in: the yellow Decision and Notes columns on Units and Weapons. Decision choices: Revert to TA, Keep repo, '
    'Custom value (put the value in Notes), Not applicable.',
    'Turret Speeds: aim turn speeds read from the unit scripts (COB bytecode, or Turn() calls in Lua scripts), '
    'fastest speed per piece and axis inside the aim functions. TA side = Cavedog COB; repo side = the Lua unit scripts '
    '(all 266 units are LUS on main). Unchanged pieces and 300 -> 299.9 style rounding are not listed.',
    'Example: ARM_T1_BOT_Peewee | Hit points | TA 250 | Repo 325 | +30.0% | Decision "Revert to TA".',
]
row = 3
for ln in lines:
    r.cell(row=row, column=1, value=ln).font = Font(name=FONT, size=10)
    r.merge_cells(start_row=row, start_column=1, end_row=row, end_column=6)
    r.cell(row=row, column=1).alignment = Alignment(wrap_text=True, vertical='top')
    r.row_dimensions[row].height = 30
    row += 1

row += 1
r.cell(row=row, column=1, value='Review progress').font = Font(name=FONT, bold=True, size=12)
row += 1
for c, h in enumerate(['', 'Units sheet', 'Weapons sheet', 'Turret Speeds'], 1):
    cell = r.cell(row=row, column=c, value=h); cell.font = H; cell.fill = HFILL
row += 1
for label, crit in [('Balance rows', None), ('Revert to TA', 'Revert to TA'), ('Keep repo', 'Keep repo'),
                    ('Custom value', 'Custom value'), ('Not applicable', 'Not applicable')]:
    r.cell(row=row, column=1, value=label).font = Font(name=FONT, size=10)
    if crit is None:
        fu = '=COUNTIF(Units!J2:J%d,"Balance")' % nu
        fw = '=COUNTIF(Weapons!J2:J%d,"Balance")' % nw
        fa = '=COUNTA(\'Turret Speeds\'!A2:A%d)' % na
    else:
        fu = '=COUNTIF(Units!K2:K%d,"%s")' % (nu, crit)
        fw = '=COUNTIF(Weapons!L2:L%d,"%s")' % (nw, crit)
        fa = '=COUNTIF(\'Turret Speeds\'!L2:L%d,"%s")' % (na, crit)
    r.cell(row=row, column=2, value=fu).font = Font(name=FONT, size=10)
    r.cell(row=row, column=3, value=fw).font = Font(name=FONT, size=10)
    r.cell(row=row, column=4, value=fa).font = Font(name=FONT, size=10)
    row += 1
r.cell(row=row, column=1, value='Undecided balance rows').font = Font(name=FONT, size=10, bold=True)
r.cell(row=row, column=2, value='=COUNTIFS(Units!J2:J%d,"Balance",Units!K2:K%d,"")' % (nu, nu)).font = Font(name=FONT, size=10, bold=True)
r.cell(row=row, column=3, value='=COUNTIFS(Weapons!J2:J%d,"Balance",Weapons!L2:L%d,"")' % (nw, nw)).font = Font(name=FONT, size=10, bold=True)
r.cell(row=row, column=4, value='=COUNTBLANK(\'Turret Speeds\'!L2:L%d)' % na).font = Font(name=FONT, size=10, bold=True)
row += 2

# Pattern summary: which stats moved and in which direction (balance rows only).
r.cell(row=row, column=1, value='Where the repo departs from TA (balance rows)').font = Font(name=FONT, bold=True, size=12)
row += 1
for c, h in enumerate(['Stat', 'Rows changed', 'Repo higher', 'Repo lower', 'Median change'], 1):
    cell = r.cell(row=row, column=c, value=h); cell.font = H; cell.fill = HFILL
row += 1
agg = defaultdict(list)
for u in units:
    if u['kind'] == 'Balance':
        agg[('Unit', u['stat'])].append(u)
for w in weaps:
    if w['kind'] == 'Balance' and w['stat'] != 'Per-target damage':
        agg[('Weapon', w['stat'])].append(w)
first = row
for (scope, stat), v in sorted(agg.items(), key=lambda x: -len(x[1]))[:24]:
    sheet, col_stat, col_chg, col_kind, n = ('Units', 'D', 'H', 'J', nu) if scope == 'Unit' else ('Weapons', 'D', 'H', 'J', nw)
    r.cell(row=row, column=1, value='%s: %s' % (scope, stat))
    r.cell(row=row, column=2, value='=COUNTIFS(%s!%s2:%s%d,A%d_STAT,%s!%s2:%s%d,"Balance")' % (sheet, col_stat, col_stat, n, row, sheet, col_kind, col_kind, n))
    r.cell(row=row, column=2).value = '=COUNTIFS(%s!$D$2:$D$%d,"%s",%s!$J$2:$J$%d,"Balance")' % (sheet, n, stat, sheet, n)
    r.cell(row=row, column=3).value = '=COUNTIFS(%s!$D$2:$D$%d,"%s",%s!$J$2:$J$%d,"Balance",%s!$H$2:$H$%d,">0")' % (sheet, n, stat, sheet, n, sheet, n)
    r.cell(row=row, column=4).value = '=COUNTIFS(%s!$D$2:$D$%d,"%s",%s!$J$2:$J$%d,"Balance",%s!$H$2:$H$%d,"<0")' % (sheet, n, stat, sheet, n, sheet, n)
    pcts = [float(x['pct']) / 100 for x in v if x['pct']]
    if pcts:
        r.cell(row=row, column=5, value=statistics.median(pcts)).number_format = '+0.0%;-0.0%;0.0%'
    for c in range(1, 6):
        r.cell(row=row, column=c).font = Font(name=FONT, size=10)
    row += 1
r.cell(row=first, column=5).comment = Comment('Median computed in Python from the balance rows at build time; '
                                              'it does not update when you edit the sheets.', 'Claude')
r.column_dimensions['A'].width = 40

wb.save(OUT)
print('units rows', nu - 1, 'weapon rows', nw - 1)
