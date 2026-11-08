#!/usr/bin/env python3
"""Radar icons for TA:Recoil: one icon per (domain frame, role glyph, tech level).

    tools/icons/make_icons.py [REPO]          writes Icons/*.png, gamedata/icontypes.lua, gamedata/unit_icons.lua
    tools/icons/make_icons.py REPO --sheet OUT.png   also a contact sheet (every icon, white and two team colours)

Design: the frame says what the unit is (kbot circle, vehicle box, hover lens, ship hull, sub dome, aircraft delta,
seaplane delta over a wave, building square, defence shield, factory double box, commander star, mine, wall); the black
glyph inside says what it does; the pips under it give the tech level. White parts take the team colour in game, black
stays black. Drawn at 4x and downsampled. The unit -> icon table (UNITS) is the only hand-made part: edit it and rerun.
gamedata/unit_icons.lua maps unit name -> icon type; gamedata/alldefs_post.lua UnitDef_Post applies it.
"""
import math, os, sys
from PIL import Image, ImageDraw

REPO = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else os.path.join(os.path.dirname(__file__), '..', '..')
SS = 4                 # supersampling
N = 128                # icon size
OUTLINE = 7            # outline width (128 px scale)
INK = (0, 0, 0, 255)
FILL = (255, 255, 255, 255)

# ---------------------------------------------------------------- unit table
# name: (frame, glyph, tier[, size tweak])   tier 0 = no pips
UNITS = {
    'arm_commander': ('commander', 'none', 0), 'core_commander': ('commander', 'none', 0),
    # a decoy must read as a commander
    'arm_t2_bot_decoycommander': ('commander', 'none', 0), 'core_t2_bot_decoycommander': ('commander', 'none', 0),
    # aircraft
    'arm_t1_air_atlas': ('air', 'transport', 1), 'core_t1_air_valkyrie': ('air', 'transport', 1),
    'arm_t1_air_constructor': ('air', 'builder', 1), 'core_t1_air_constructor': ('air', 'builder', 1),
    'arm_t1_air_freedomfighter': ('air', 'aa', 1), 'core_t1_air_avenger': ('air', 'aa', 1),
    'arm_t1_air_peeper': ('air', 'scout', 1), 'core_t1_air_fink': ('air', 'scout', 1),
    'arm_t1_air_thunder': ('air', 'bomber', 1), 'core_t1_air_shadow': ('air', 'bomber', 1),
    'arm_t2_air_advancedconstructor': ('air', 'builder', 2), 'core_t2_air_advancedconstructor': ('air', 'builder', 2),
    'arm_t2_air_brawler': ('air', 'assault', 2), 'core_t2_air_rapier': ('air', 'assault', 2),
    'arm_t2_air_eagle': ('air', 'radar', 2), 'core_t2_air_vulture': ('air', 'radar', 2),
    'arm_t2_air_hawk': ('air', 'aa', 2), 'core_t2_air_vamp': ('air', 'aa', 2),
    'arm_t2_air_lancet': ('air', 'torpedo', 2), 'core_t2_air_titan': ('air', 'torpedo', 2),
    'arm_t2_air_phoenix': ('air', 'bomber', 2), 'core_t2_air_hurricane': ('air', 'bomber', 2),
    'arm_t2_air_seahawk': ('air', 'sonar', 2), 'core_t2_air_hunter': ('air', 'sonar', 2),
    # seaplanes
    'arm_t1_seapl_albatross': ('seaplane', 'torpedo', 1), 'core_t1_seapl_typhoon': ('seaplane', 'torpedo', 1),
    'arm_t1_seapl_constructor': ('seaplane', 'builder', 1), 'core_t1_seapl_constructor': ('seaplane', 'builder', 1),
    'arm_t1_seapl_tornado': ('seaplane', 'aa', 1), 'core_t1_seapl_voodoo': ('seaplane', 'aa', 1),
    # kbots
    'arm_t1_bot_constructor': ('kbot', 'builder', 1), 'core_t1_bot_constructor': ('kbot', 'builder', 1),
    'arm_t1_bot_flea': ('kbot', 'scout', 1),
    'arm_t1_bot_peewee': ('kbot', 'light', 1), 'core_t1_bot_ak': ('kbot', 'light', 1),
    'arm_t1_bot_warrior': ('kbot', 'assault', 1),
    'arm_t1_bot_hammer': ('kbot', 'artillery', 1), 'core_t1_bot_thud': ('kbot', 'artillery', 1),
    'arm_t1_bot_jethro': ('kbot', 'aa', 1), 'core_t1_bot_crasher': ('kbot', 'aa', 1),
    'arm_t1_bot_rocko': ('kbot', 'rocket', 1), 'core_t1_bot_storm': ('kbot', 'rocket', 1),
    'arm_t2_bot_advancedconstructor': ('kbot', 'builder', 2), 'core_t2_bot_advancedconstructor': ('kbot', 'builder', 2),
    'arm_t2_bot_fark': ('kbot', 'builder', 2), 'core_t2_bot_necro': ('kbot', 'builder', 2),
    'arm_t2_bot_eraser': ('kbot', 'jammer', 2), 'core_t2_bot_spectre': ('kbot', 'jammer', 2),
    'arm_t2_bot_marky': ('kbot', 'radar', 2), 'core_t2_bot_voyeur': ('kbot', 'radar', 2),
    'arm_t2_bot_infiltrator': ('kbot', 'spy', 2), 'core_t2_bot_parasite': ('kbot', 'spy', 2),
    'arm_t2_bot_invader': ('kbot', 'kamikaze', 2), 'core_t2_bot_roach': ('kbot', 'kamikaze', 2),
    'arm_t2_bot_zipper': ('kbot', 'light', 2), 'core_t2_bot_freaker': ('kbot', 'light', 2),
    'arm_t2_bot_fido': ('kbot', 'assault', 2), 'arm_t2_bot_maverick': ('kbot', 'assault', 2),
    'arm_t2_bot_zeus': ('kbot', 'assault', 2), 'core_t2_bot_pyro': ('kbot', 'assault', 2),
    'arm_t2_bot_pelican': ('amphkbot', 'assault', 2), 'core_t2_bot_gimp': ('amphkbot', 'assault', 2),
    'arm_t2_bot_shooter': ('kbot', 'sniper', 2),
    'core_t2_bot_morty': ('kbot', 'artillery', 2),
    'core_t2_bot_dominator': ('kbot', 'rocket', 2),
    'core_t2_bot_sumo': ('kbot', 'heavy', 2), 'core_t2_bot_thecan': ('kbot', 'heavy', 2),
    'core_t3_bot_krogoth': ('kbot', 'heavy', 3, 1.7),
    # vehicles
    'arm_t1_veh_constructor': ('veh', 'builder', 1), 'core_t1_veh_constructor': ('veh', 'builder', 1),
    'arm_t1_veh_podger': ('veh', 'minelayer', 1), 'core_t1_veh_spoiler': ('veh', 'minelayer', 1),
    'arm_t1_veh_jeffy': ('veh', 'scout', 1), 'core_t1_veh_weasel': ('veh', 'scout', 1),
    'arm_t1_veh_flash': ('veh', 'light', 1), 'core_t1_veh_instigator': ('veh', 'light', 1),
    'arm_t1_veh_stumpy': ('veh', 'assault', 1), 'core_t1_veh_raider': ('veh', 'assault', 1),
    'core_t1_veh_leveler': ('veh', 'assault', 1),
    'arm_t1_veh_samson': ('veh', 'rocket', 1), 'core_t1_veh_slasher': ('veh', 'rocket', 1),
    'arm_t2_veh_advancedconstructor': ('veh', 'builder', 2), 'core_t2_veh_advancedconstructor': ('veh', 'builder', 2),
    'arm_t2_veh_bulldog': ('veh', 'heavy', 2), 'core_t2_veh_reaper': ('veh', 'heavy', 2),
    'core_t2_veh_goliath': ('veh', 'heavy', 2, 1.15),
    'arm_t2_veh_jammer': ('veh', 'jammer', 2), 'core_t2_veh_deleter': ('veh', 'jammer', 2),
    'arm_t2_veh_luger': ('veh', 'artillery', 2), 'core_t2_veh_pillager': ('veh', 'artillery', 2),
    'arm_t2_veh_merl': ('veh', 'rocket', 2), 'core_t2_veh_diplomat': ('veh', 'rocket', 2),
    'arm_t2_veh_panther': ('veh', 'assault', 2),
    'arm_t2_veh_penetrator': ('veh', 'sniper', 2),
    'arm_t2_veh_phalanx': ('veh', 'aa', 2), 'core_t2_veh_copperhead': ('veh', 'aa', 2),
    'arm_t2_veh_scarab': ('veh', 'antinuke', 2), 'core_t2_veh_hedgehog': ('veh', 'antinuke', 2),
    'arm_t2_veh_seer': ('veh', 'radar', 2), 'core_t2_veh_informer': ('veh', 'radar', 2),
    'arm_t2_veh_spider': ('veh', 'emp', 2),
    'arm_t2_veh_triton': ('amphveh', 'assault', 2), 'core_t2_veh_crock': ('amphveh', 'assault', 2),
    # hovercraft
    'arm_t1_hov_constructor': ('hover', 'builder', 1), 'core_t1_hov_constructor': ('hover', 'builder', 1),
    'arm_t1_hov_anaconda': ('hover', 'assault', 1), 'core_t1_hov_snapper': ('hover', 'assault', 1),
    'arm_t1_hov_bear': ('hover', 'transport', 1), 'core_t1_hov_turtle': ('hover', 'transport', 1),
    'arm_t1_hov_skimmer': ('hover', 'scout', 1), 'core_t1_hov_scrubber': ('hover', 'scout', 1),
    'arm_t1_hov_swatter': ('hover', 'aa', 1), 'core_t1_hov_slinger': ('hover', 'aa', 1),
    'arm_t1_hov_wombat': ('hover', 'rocket', 1), 'core_t1_hov_nixer': ('hover', 'rocket', 1),
    # ships
    'arm_t1_sea_constructor': ('ship', 'builder', 1), 'core_t1_sea_constructor': ('ship', 'builder', 1),
    'arm_t1_sea_crusader': ('ship', 'assault', 1), 'core_t1_sea_enforcer': ('ship', 'assault', 1),
    'arm_t1_sea_hulk': ('ship', 'transport', 1), 'core_t1_sea_envoy': ('ship', 'transport', 1),
    'arm_t1_sea_skeeter': ('ship', 'scout', 1), 'core_t1_sea_searcher': ('ship', 'scout', 1),
    'arm_t2_sea_archer': ('ship', 'aa', 2), 'core_t2_sea_shredder': ('ship', 'aa', 2),
    'arm_t2_sea_colossus': ('ship', 'carrier', 2, 1.2), 'core_t2_sea_hive': ('ship', 'carrier', 2, 1.2),
    'arm_t2_sea_conqueror': ('ship', 'artillery', 2, 1.1), 'core_t2_sea_executioner': ('ship', 'artillery', 2, 1.1),
    'arm_t2_sea_escort': ('ship', 'jammer', 2), 'core_t2_sea_phantom': ('ship', 'jammer', 2),
    'arm_t2_sea_millenium': ('ship', 'heavy', 2, 1.25), 'core_t2_sea_warlord': ('ship', 'heavy', 2, 1.25),
    'arm_t2_sea_ranger': ('ship', 'rocket', 2), 'core_t2_sea_missilefrigate': ('ship', 'rocket', 2),
    # submarines
    'arm_t1_sea_lurker': ('sub', 'torpedo', 1), 'core_t1_sea_snake': ('sub', 'torpedo', 1),
    'arm_t2_sea_advancedconstructor': ('sub', 'builder', 2), 'core_t2_sea_advancedconstructor': ('sub', 'builder', 2),
    'arm_t2_sea_fibber': ('sub', 'jammer', 2),
    'arm_t2_sea_piranha': ('sub', 'torpedo', 2), 'core_t2_sea_shark': ('sub', 'torpedo', 2),
    'core_t2_sea_leviathan': ('sub', 'heavy', 2, 1.2),
    # defences
    'arm_t1_def_llt': ('defense', 'light', 1), 'core_t1_def_lightlasertower': ('defense', 'light', 1),
    'core_t1_def_immolator': ('defense', 'light', 1),
    'arm_t1_def_sentinel': ('defense', 'assault', 1), 'core_t1_def_gaatgun': ('defense', 'assault', 1),
    'core_t1_def_viper': ('defense', 'assault', 1),
    'arm_t1_seadef_stingray': ('defense', 'assault', 1), 'core_t1_seadef_thunderbolt': ('defense', 'assault', 1),
    'arm_t1_def_defender': ('defense', 'aa', 1), 'core_t1_def_pulverizer': ('defense', 'aa', 1),
    'arm_t1_seadef_defender': ('defense', 'aa', 1), 'core_t1_seadef_stinger': ('defense', 'aa', 1),
    'arm_t1_def_guardian': ('defense', 'artillery', 1), 'core_t1_def_punisher': ('defense', 'artillery', 1),
    'arm_t1_seadef_torpedolauncher': ('defense', 'torpedo', 1), 'core_t1_seadef_torpedolauncher': ('defense', 'torpedo', 1),
    'arm_t2_seadef_advancedtorpedolauncher': ('defense', 'torpedo', 2), 'core_t2_seadef_advancedtorpedolauncher': ('defense', 'torpedo', 2),
    'arm_t2_def_ambusher': ('defense', 'artillery', 2), 'core_t2_def_toaster': ('defense', 'artillery', 2),
    'arm_t2_def_annihilator': ('defense', 'heavy', 2), 'core_t2_def_doomsdaymachine': ('defense', 'heavy', 2),
    'arm_t2_def_bigbertha': ('defense', 'longrange', 2, 1.15), 'core_t2_def_intimidator': ('defense', 'longrange', 2, 1.15),
    'arm_t2_def_vulcan': ('defense', 'longrange', 2, 1.15), 'core_t2_def_buzzsaw': ('defense', 'longrange', 2, 1.15),
    'arm_t2_def_flakker': ('defense', 'aa', 2), 'core_t2_def_cobra': ('defense', 'aa', 2),
    'arm_t2_def_protector': ('defense', 'antinuke', 2), 'core_t2_def_fortitudemissiledefense': ('defense', 'antinuke', 2),
    'arm_t2_def_retaliator': ('defense', 'nuke', 2, 1.2), 'core_t2_def_silencer': ('defense', 'nuke', 2, 1.2),
    'core_t2_def_neutron': ('defense', 'nuke', 2),
    'arm_t2_def_stunner': ('defense', 'emp', 2, 1.2),
    # walls and mines
    'arm_t1_def_dragonsteeth': ('wall', 'none', 0), 'core_t1_def_dragonsteeth': ('wall', 'none', 0),
    'arm_t1_seadef_floatingdragonsteeth': ('wall', 'none', 0), 'core_t1_seadef_floatingdragonsteeth': ('wall', 'none', 0),
    'arm_t2_def_fortificationwall': ('wall', 'none', 0), 'core_t2_def_fortificationwall': ('wall', 'none', 0),
    # intel and support buildings
    'arm_t1_def_radartower': ('building', 'radar', 1), 'core_t1_def_radartower': ('building', 'radar', 1),
    'arm_t2_def_advancedradar': ('building', 'radar', 2), 'core_t2_def_advancedradar': ('building', 'radar', 2),
    'arm_t1_seadef_sonarstation': ('building', 'sonar', 1), 'core_t1_seadef_sonarstation': ('building', 'sonar', 1),
    'arm_t2_seadef_advancedsonar': ('building', 'sonar', 2), 'core_t2_seadef_advancedsonar': ('building', 'sonar', 2),
    'arm_t2_def_targetingfacility': ('building', 'targeting', 2), 'core_t2_def_targetingfacility': ('building', 'targeting', 2),
    'arm_t2_def_airrepairpad': ('building', 'repair', 2), 'core_t2_def_airrepairpad': ('building', 'repair', 2),
}
_hand = set(UNITS)
for side in ('arm', 'core'):
    for i in range(1, 7):
        UNITS['%s_t1_def_mine%d' % (side, i)] = ('mine', 'none', 0, 1.3 if i == 6 else 1)
    for pre in ('%s_t1_eco_' % side, '%s_t1_seaeco_' % side):
        UNITS[pre + 'energystorage'] = UNITS[pre + 'uwenergystorage'] = ('building', 'estorage', 1)
        UNITS[pre + 'metalstorage'] = UNITS[pre + 'uwmetalstorage'] = ('building', 'mstorage', 1)
        UNITS[pre + 'metalextractor'] = UNITS[pre + 'uwmetalextractor'] = ('building', 'mex', 1)
        UNITS[pre + 'metalmaker'] = UNITS[pre + 'floatingmetalmaker'] = ('building', 'mmaker', 1)
        for e in ('geothermalpowerplant', 'solarcollector', 'windgenerator', 'tidalgenerator'):
            UNITS[pre + e] = ('building', 'energy', 1)
    for e in ('cloakablefusion', 'fusionpowerplant'):
        UNITS['%s_t2_eco_%s' % (side, e)] = ('building', 'energy', 2, 1.15)
    UNITS['%s_t2_seaeco_uwfusionpowerplant' % side] = ('building', 'energy', 2, 1.15)
    UNITS['%s_t2_eco_mohometalmaker' % side] = ('building', 'mmaker', 2)
    UNITS['%s_t2_eco_mohomine' % side] = ('building', 'mex', 2)
    for lab, g in (('aircraftplant', 'air'), ('hovercraftplatform', 'hover'), ('kbotlab', 'kbot'), ('seaplaneplatform', 'seaplane'),
                   ('shipyard', 'ship'), ('vehicleplant', 'veh')):
        UNITS['%s_t1_lab_%s' % (side, lab)] = ('factory', 'f_' + g, 1)
    for lab, g in (('advancedaircraftplant', 'air'), ('advancedkbotlab', 'kbot'), ('advancedshipyard', 'ship'), ('advancedvehicleplant', 'veh')):
        UNITS['%s_t2_lab_%s' % (side, lab)] = ('factory', 'f_' + g, 2)
UNITS['core_t3_lab_krogothgantry'] = ('factory', 'f_kbot', 3, 1.15)

# base icon size (engine units) per frame; x1.1 for tech 2+
SIZE = {'commander': 2.3, 'kbot': 1.45, 'amphkbot': 1.45, 'veh': 1.55, 'amphveh': 1.55, 'hover': 1.6, 'ship': 1.75,
        'sub': 1.6, 'air': 1.45, 'seaplane': 1.45, 'building': 1.35, 'defense': 1.45, 'factory': 1.9, 'mine': 0.8,
        'wall': 0.6}

# ---------------------------------------------------------------- drawing
def S(v):
    return v * SS


def P(pts):
    return [(S(x), S(y)) for x, y in pts]


class Pen:
    def __init__(self):
        self.im = Image.new('RGBA', (S(N), S(N)), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    def poly(self, pts, fill=FILL, outline=True):
        if outline:
            # outline: draw the polygon fat in ink, then the fill inset (stroke both)
            self.d.polygon(P(pts), fill=INK)
            self.d.line(P(pts + [pts[0]]), fill=INK, width=int(S(OUTLINE * 2)), joint="curve")
            for x, y in pts:
                r = S(OUTLINE)
                self.d.ellipse((S(x) - r, S(y) - r, S(x) + r, S(y) + r), fill=INK)
        self.d.polygon(P(pts), fill=fill)

    def ell(self, box, fill=FILL, outline=True):
        x0, y0, x1, y1 = box
        if outline:
            o = OUTLINE
            self.d.ellipse((S(x0 - o), S(y0 - o), S(x1 + o), S(y1 + o)), fill=INK)
        self.d.ellipse(P([(x0, y0), (x1, y1)]), fill=fill)

    def rrect(self, box, r, fill=FILL, outline=True):
        x0, y0, x1, y1 = box
        if outline:
            o = OUTLINE
            self.d.rounded_rectangle((S(x0 - o), S(y0 - o), S(x1 + o), S(y1 + o)), S(r + o), fill=INK)
        self.d.rounded_rectangle(P([(x0, y0), (x1, y1)]), S(r), fill=fill)

    def line(self, pts, w, fill=INK):
        self.d.line(P(pts), fill=fill, width=int(S(w)), joint="curve")
        for x, y in (pts[0], pts[-1]):
            r = S(w) / 2
            self.d.ellipse((S(x) - r, S(y) - r, S(x) + r, S(y) + r), fill=fill)

    def arc(self, box, a0, a1, w, fill=INK):
        self.d.arc(P([(box[0], box[1]), (box[2], box[3])]), a0, a1, fill=fill, width=int(S(w)))

    def dot(self, x, y, r, fill=INK):
        self.d.ellipse((S(x - r), S(y - r), S(x + r), S(y + r)), fill=fill)

    def done(self):
        return self.im.resize((N, N), Image.LANCZOS)


def star(cx, cy, ro, ri, n, rot=-90):
    pts = []
    for i in range(n * 2):
        r = ro if i % 2 == 0 else ri
        a = math.radians(rot + i * 180 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def wave(p, y, x0=34, x1=94, w=6):
    pts = [(x0 + (x1 - x0) * t / 40, y + 5 * math.sin(t / 40 * 4 * math.pi)) for t in range(41)]
    p.line(pts, w + 2 * 4, fill=INK)     # dark halo so the wave reads on any ground
    p.line(pts, w, fill=FILL)


# frames: draw the frame, return (glyph centre x, y, glyph scale) and the y below the frame
def frame(p, kind):
    if kind in ('kbot', 'amphkbot'):
        p.ell((24, 12, 104, 92)); c = (64, 52, 1.0); bottom = 99
    elif kind in ('veh', 'amphveh'):
        p.rrect((10, 22, 118, 84), 10); c = (64, 53, 0.95); bottom = 91
    elif kind == 'hover':
        p.poly([(6, 52)] + [(64 - 58 * math.cos(math.pi * t / 20), 52 - 30 * math.sin(math.pi * t / 20)) for t in range(1, 20)] +
               [(122, 52)] + [(64 + 58 * math.cos(math.pi * t / 20), 52 + 30 * math.sin(math.pi * t / 20)) for t in range(1, 20)])
        c = (64, 52, 0.9); bottom = 89
    elif kind == 'ship':
        p.poly([(6, 24), (122, 24)] + [(64 + 58 * math.cos(math.pi * t / 24), 24 + 62 * math.sin(math.pi * t / 24)) for t in range(1, 24)])
        c = (64, 46, 0.95); bottom = 93
    elif kind == 'sub':
        p.poly([(122, 84), (6, 84)] + [(64 - 58 * math.cos(math.pi * t / 24), 84 - 62 * math.sin(math.pi * t / 24)) for t in range(1, 24)])
        c = (64, 60, 0.95); bottom = 92
    elif kind in ('air', 'seaplane'):
        p.poly([(64, 4), (124, 96), (64, 82), (4, 96)]); c = (64, 60, 0.82); bottom = 103
    elif kind == 'building':
        p.rrect((22, 12, 106, 96), 6); c = (64, 54, 1.0); bottom = 104
    elif kind == 'defense':
        p.poly([(18, 10), (110, 10), (110, 54), (64, 100), (18, 54)]); c = (64, 46, 0.95); bottom = 112
    elif kind == 'factory':
        p.rrect((8, 14, 120, 98), 8)
        p.d.rounded_rectangle(P([(20, 26), (108, 86)]), S(4), outline=INK, width=int(S(5)))
        c = (64, 56, 0.85); bottom = 106
    elif kind == 'commander':
        p.poly(star(64, 62, 60, 34, 4, rot=-90)); p.ell((34, 32, 94, 92))
        p.d.ellipse(P([(48, 46), (80, 78)]), fill=INK)
        c = (64, 62, 0); bottom = 124
    elif kind == 'mine':
        p.poly([(64, 18), (110, 64), (64, 110), (18, 64)])
        p.line([(48, 48), (80, 80)], 10); p.line([(80, 48), (48, 80)], 10)
        c = (64, 64, 0); bottom = 124
    elif kind == 'wall':
        p.rrect((16, 30, 112, 98), 4)
        for x in (48, 80):
            p.line([(x, 34), (x, 94)], 7)
        c = (64, 64, 0); bottom = 124
    else:
        raise ValueError(kind)
    if kind in ('amphkbot', 'amphveh', 'seaplane'):
        wave(p, bottom + 6)
        bottom += 14
    return c, bottom


def chevrons(p, cx, cy, k, n):
    h = 15 * k; w = 26 * k; gap = 17 * k
    y0 = cy + (n - 1) * gap / 2 + h / 2
    for i in range(n):
        y = y0 - i * gap
        p.line([(cx - w, y), (cx, y - h), (cx + w, y)], 10 * k)


def glyph(p, g, cx, cy, k):
    if g == 'none' or k == 0:
        return
    L = lambda pts, w=10: p.line([(cx + x * k, cy + y * k) for x, y in pts], w * k)
    if g == 'light':
        chevrons(p, cx, cy, k, 1)
    elif g == 'assault':
        chevrons(p, cx, cy, k, 2)
    elif g == 'heavy':
        chevrons(p, cx, cy, k, 3)
    elif g == 'artillery':
        p.dot(cx, cy, 15 * k)
    elif g == 'longrange':
        p.dot(cx, cy, 9 * k); p.arc((cx - 27 * k, cy - 27 * k, cx + 27 * k, cy + 27 * k), 0, 360, 8 * k)
    elif g == 'rocket':
        L([(0, 26), (0, -18)]); p.poly([(cx - 15 * k, cy - 10 * k), (cx, cy - 30 * k), (cx + 15 * k, cy - 10 * k)], fill=INK, outline=False)
        L([(-14, 26), (-6, 16)], 8); L([(14, 26), (6, 16)], 8)
    elif g == 'aa':
        p.arc((cx - 28 * k, cy - 18 * k, cx + 28 * k, cy + 38 * k), 180, 360, 10 * k)
        p.dot(cx, cy + 10 * k, 7 * k)
    elif g == 'builder':
        L([(-22, -20), (22, -20)], 12); L([(-14, -20), (-14, 24)], 11); L([(14, -20), (14, 24)], 11)
    elif g == 'minelayer':
        L([(-22, -20), (22, -20)], 12); L([(-14, -20), (-14, 24)], 11); L([(14, -20), (14, 24)], 11)
        p.dot(cx, cy + 10 * k, 6 * k)
    elif g == 'scout':
        p.arc((cx - 20 * k, cy - 20 * k, cx + 20 * k, cy + 20 * k), 0, 360, 9 * k)
    elif g == 'radar':
        p.dot(cx - 16 * k, cy + 14 * k, 6 * k)
        for r in (18, 34):
            p.arc((cx - 16 * k - r * k, cy + 14 * k - r * k, cx - 16 * k + r * k, cy + 14 * k + r * k), 270, 360, 8 * k)
    elif g == 'sonar':
        p.dot(cx, cy - 14 * k, 6 * k)
        for r in (16, 30):
            p.arc((cx - r * k, cy - 14 * k - r * k, cx + r * k, cy - 14 * k + r * k), 30, 150, 8 * k)
    elif g == 'jammer':
        L([(-26, 4), (-14, -12), (-2, 12), (10, -12), (22, 8)], 9)
    elif g == 'transport':
        L([(-22, -16), (-22, 16), (22, 16), (22, -16)], 11)
    elif g == 'bomber':
        p.poly([(cx - 22 * k, cy - 18 * k), (cx + 22 * k, cy - 18 * k), (cx, cy + 22 * k)], fill=INK, outline=False)
    elif g == 'torpedo':
        p.d.rounded_rectangle(P([(cx - 28 * k, cy - 8 * k), (cx + 22 * k, cy + 8 * k)]), S(8 * k), fill=INK)
        p.poly([(cx + 18 * k, cy), (cx + 30 * k, cy - 12 * k), (cx + 30 * k, cy + 12 * k)], fill=INK, outline=False)
    elif g == 'kamikaze':
        p.poly(star(cx, cy, 27 * k, 11 * k, 8), fill=INK, outline=False)
    elif g == 'spy':
        p.arc((cx - 20 * k, cy - 20 * k, cx + 20 * k, cy + 20 * k), 0, 360, 7 * k)
        p.d.pieslice(P([(cx - 20 * k, cy - 20 * k), (cx + 20 * k, cy + 20 * k)]), 90, 270, fill=INK)
    elif g == 'emp':
        p.poly([(cx + 6 * k, cy - 30 * k), (cx - 16 * k, cy + 4 * k), (cx - 1 * k, cy + 4 * k), (cx - 8 * k, cy + 30 * k),
                (cx + 16 * k, cy - 6 * k), (cx + 1 * k, cy - 6 * k)], fill=INK, outline=False)
    elif g == 'energy':
        p.poly([(cx + 6 * k, cy - 32 * k), (cx - 17 * k, cy + 4 * k), (cx - 1 * k, cy + 4 * k), (cx - 9 * k, cy + 32 * k),
                (cx + 17 * k, cy - 6 * k), (cx + 1 * k, cy - 6 * k)], fill=INK, outline=False)
    elif g in ('mex', 'mmaker', 'mstorage'):
        y0 = -6 if g != 'mex' else 0
        L([(-20, 20 + y0), (-20, -18 + y0), (0, 4 + y0), (20, -18 + y0), (20, 20 + y0)], 10)
        if g == 'mmaker':
            p.arc((cx - 34 * k, cy - 34 * k, cx + 34 * k, cy + 34 * k), 0, 360, 6 * k)
        if g == 'mstorage':
            L([(-24, 30), (24, 30)], 8)
    elif g == 'estorage':
        L([(16, -24), (-16, -24), (-16, 12), (16, 12)], 10); L([(-16, -6), (10, -6)], 10)
        L([(-24, 28), (24, 28)], 8)
    elif g == 'antinuke':
        p.arc((cx - 26 * k, cy - 26 * k, cx + 26 * k, cy + 26 * k), 0, 360, 8 * k)
        p.arc((cx - 13 * k, cy - 13 * k, cx + 13 * k, cy + 13 * k), 0, 360, 7 * k)
    elif g == 'nuke':
        p.dot(cx, cy, 6 * k)
        for a in (-90, 30, 150):
            p.d.pieslice(P([(cx - 28 * k, cy - 28 * k), (cx + 28 * k, cy + 28 * k)]), a - 30, a + 30, fill=INK)
        p.dot(cx, cy, 10 * k, fill=FILL); p.dot(cx, cy, 6 * k)
    elif g == 'sniper':
        p.arc((cx - 22 * k, cy - 22 * k, cx + 22 * k, cy + 22 * k), 0, 360, 7 * k)
        L([(0, -32), (0, 32)], 7); L([(-32, 0), (32, 0)], 7)
    elif g == 'targeting':
        p.arc((cx - 24 * k, cy - 24 * k, cx + 24 * k, cy + 24 * k), 0, 360, 7 * k)
        L([(0, -34), (0, -12)], 7); L([(0, 12), (0, 34)], 7); L([(-34, 0), (-12, 0)], 7); L([(12, 0), (34, 0)], 7)
    elif g == 'repair':
        L([(0, -24), (0, 24)], 14); L([(-24, 0), (24, 0)], 14)
    elif g == 'carrier':
        p.poly([(cx, cy - 26 * k), (cx + 24 * k, cy + 16 * k), (cx, cy + 6 * k), (cx - 24 * k, cy + 16 * k)], fill=INK, outline=False)
    elif g.startswith('f_'):
        mini = g[2:]
        if mini == 'kbot':
            p.dot(cx, cy, 20 * k)
        elif mini == 'veh':
            p.d.rounded_rectangle(P([(cx - 28 * k, cy - 14 * k), (cx + 28 * k, cy + 14 * k)]), S(4 * k), fill=INK)
        elif mini == 'hover':
            p.d.ellipse(P([(cx - 30 * k, cy - 14 * k), (cx + 30 * k, cy + 14 * k)]), fill=INK)
        elif mini == 'ship':
            p.d.chord(P([(cx - 30 * k, cy - 30 * k), (cx + 30 * k, cy + 22 * k)]), 0, 180, fill=INK)
        elif mini in ('air', 'seaplane'):
            p.poly([(cx, cy - 24 * k), (cx + 26 * k, cy + 18 * k), (cx, cy + 9 * k), (cx - 26 * k, cy + 18 * k)], fill=INK, outline=False)
            if mini == 'seaplane':
                L([(-26, 30), (-13, 24), (0, 30), (13, 24), (26, 30)], 6)
    else:
        raise ValueError(g)


def pips(p, tier, y):
    if tier <= 0:
        return
    w, gap = 13, 6
    total = tier * w + (tier - 1) * gap
    x = 64 - total / 2
    for i in range(tier):
        p.rrect((x, y, x + w, y + w), 2)
        x += w + gap


def icon(frame_kind, g, tier):
    p = Pen()
    (cx, cy, k), bottom = frame(p, frame_kind)
    glyph(p, g, cx, cy, k)
    pips(p, tier, bottom + 6)
    return p.done()


def type_name(f, g, t):
    return '%s_%s%s' % (f, g, '_t%d' % t if t else '')


def main():
    icons_dir = os.path.join(REPO, 'Icons')
    known = {os.path.splitext(f)[0].lower() for f in os.listdir(os.path.join(REPO, 'units')) if f.endswith('.lua')}
    for u in set(UNITS) - _hand - known:   # the eco/lab loops make every land/sea combination; keep the real ones
        del UNITS[u]
    missing = sorted(known - set(UNITS)); extra = sorted(set(UNITS) - known)
    if missing or extra:
        sys.exit('unit table out of date: missing %s, unknown %s' % (missing, extra))
    for f in os.listdir(icons_dir):
        if f.endswith('.png'):
            os.remove(os.path.join(icons_dir, f))
    types = {}
    for unit, spec in sorted(UNITS.items()):
        f, g, t = spec[:3]
        tweak = spec[3] if len(spec) > 3 else 1
        size = round(SIZE[f] * (1.1 if t >= 2 else 1) * tweak, 3)
        base = type_name(f, g, t)
        name = base if tweak == 1 else '%s_x%s' % (base, ('%g' % tweak).replace('.', ''))
        types.setdefault(name, (base, size, f, g, t))
    for base in sorted({v[0] for v in types.values()}):
        f, g, t = next((v[2], v[3], v[4]) for v in types.values() if v[0] == base)
        icon(f, g, t).save(os.path.join(icons_dir, base + '.png'), optimize=True)
    out = ['-- Radar icon types: generated by tools/icons/make_icons.py (frame = domain, glyph = role, pips = tech level).',
           '-- Do not edit by hand: change the script and rerun it. Units get theirs from gamedata/unit_icons.lua.', '',
           'return {', '\tdefault = {', '\t\tsize = 1,', '\t\tradiusadjust = 0,', '\t\tdistance = 1,', '\t},']
    for name in sorted(types):
        base, size = types[name][:2]
        out += ['\t%s = {' % name, '\t\tbitmap = "icons/%s.png",' % base, '\t\tsize = %g,' % size, '\t\tradiusadjust = 0,',
                '\t\tdistance = 1,', '\t},']
    out += ['}', '']
    open(os.path.join(REPO, 'gamedata', 'icontypes.lua'), 'w').write('\n'.join(out))
    m = ['-- Unit name -> radar icon type: generated by tools/icons/make_icons.py, applied in gamedata/alldefs_post.lua.', '', 'return {']
    for unit, spec in sorted(UNITS.items()):
        f, g, t = spec[:3]
        tweak = spec[3] if len(spec) > 3 else 1
        base = type_name(f, g, t)
        m.append('\t%s = "%s",' % (unit, base if tweak == 1 else '%s_x%s' % (base, ('%g' % tweak).replace('.', ''))))
    m += ['}', '']
    open(os.path.join(REPO, 'gamedata', 'unit_icons.lua'), 'w').write('\n'.join(m))
    print('%d icons, %d icon types, %d units' % (len({v[0] for v in types.values()}), len(types), len(UNITS)))
    if '--sheet' in sys.argv:
        sheet(icons_dir, sys.argv[sys.argv.index('--sheet') + 1])


def sheet(icons_dir, out):
    files = sorted(f for f in os.listdir(icons_dir) if f.endswith('.png'))
    cols, cell = 12, 84
    rows = (len(files) + cols - 1) // cols
    tints = [(255, 255, 255), (60, 110, 255), (230, 40, 30)]
    W = Image.new('RGBA', (cols * cell * len(tints), rows * cell), (70, 90, 60, 255))
    for ti, tint in enumerate(tints):
        for i, f in enumerate(files):
            im = Image.open(os.path.join(icons_dir, f)).convert('RGBA').resize((64, 64), Image.LANCZOS)
            px = im.load()
            for y in range(64):
                for x in range(64):
                    r, g, b, a = px[x, y]
                    px[x, y] = (r * tint[0] // 255, g * tint[1] // 255, b * tint[2] // 255, a)
            W.alpha_composite(im, (ti * cols * cell + (i % cols) * cell + 10, (i // cols) * cell + 10))
    W.save(out)


if __name__ == '__main__':
    main()
