# Balance notes: where TA 3.1c in Recoil may want tuning (suggestions only, none applied)

The `ta-values` branch puts TA 3.1c's numbers in as exactly as Recoil allows (DEVIATIONS.md lists where it can't).
These are the places where I expect TA's numbers to play differently here than they did in 1998, or where TA itself
had known weak spots. Each says what to watch for and a cheap fix if it turns out to matter. Test in game first.

## Things Recoil does differently, so TA's numbers may feel off

1. **Sight ranges feel short.** TA's sight radii (Commander 290, Peewee 280, Flash 225, buildings 210) are back. In TA,
   height also extended what a unit saw, and Recoil has no such bonus: it only uses height to decide what terrain hides.
   Many units now out-range their own sight (Stumpy 320 range vs 250 sight). That was true in TA too: radar and
   spotters mattered. Units on hills will feel more short-sighted than in TA. If it plays too blind, the cheapest
   fixes are a flat +15-25 % on `sightdistance` in `unitdefs_post.lua`, or raising `sightEmitHeight`.
2. **Build range 60 for the commanders and many builders** (was 128). Recoil measures it from the builder to the edge
   of what is built, as TA did. The remodelled S3Os are chunkier than the TA models, so check builders don't have to
   shove into the build site. If they do, add the model radius difference, not 128.
3. **Cannons keep TA's own velocities and gravity**, so arcs are higher and slower than in BOTA (gravity 0.124 vs 0.25
   per frame^2). Slow shells are dodgeable again, which TA players will expect. The Cruiser/Battleship cannons
   (v^2/g = 84-88 % of their listed range) can't quite reach full range on flat ground. TA used the same physics,
   so I left them. Raising their velocity ~9 % would give the listed range.
4. **No idle self-repair** any more (TA had none). Repairing with builders and nano towers matters again. If
   skirmishes feel too attritional, a small idle regen (BOTA had 0.5 HP/s after 73 s) is the knob.
5. **Construction decay is on** (your call). TA nanoframes never decayed, so abandoned frames now vanish.
6. **Energy upkeep, metal makers, extractors and wind only run while a unit is "on"** (Recoil rule). TA's
   values are in, and every eco unit that has them activates when built or is toggleable, but any new eco unit needs
   `activatewhenbuilt = 1`.

## TA's own quirks that are now back (TA-faithful; decide whether you want them)

7. **The EMP (Stunner) only stuns Core units, and the Tron/Neutron only hurts Arm units.** TA did this with
   per-unit lists so they couldn't hurt their own side. In an Arm-vs-Arm or Core-vs-Core game they are near useless.
   Fix: give the stunner and neutron the same damage against both `*_mobile` classes in `armor.py`, i.e. symmetric
   classes by role rather than by side.
8. **Flak has no bonus against aircraft** (130-146 against everything; BOTA had 180 vs planes). Flak is strong
   against ground targets again and only average against air. TA players will remember it that way.
9. **Turret speeds that are slow on purpose**: Penetrator 8 deg/s traverse and 4 deg/s elevation, Doomsday main gun
   10 deg/s, Big Bertha 5/2, Pillager 50, Leveler elevation 20. BOTA sped up the Penetrator (50) and Doomsday (50).
   Fast targets can now outrun them, as in TA.
10. **Shorter air ranges**: Freedom Fighter missile 300 (BOTA 480), Albatross torpedo 510 (630), Hawk/Vamp TA values.
   Fighters have to close in again. The headless aim probe hits fewer circling targets with them.
11. **Death explosions**: TA's again. The Geothermal self-destructs like a nuke and the Thunder explodes with lightning.
    Energy storages and metal makers are dangerous to stand next to.

## Known TA 3.1c balance points worth watching

12. **Early raiders**: Flash (106 M, 625 HP, speed 2.0, EMG) and Instigator (110 M, 653 HP) were the classic T1 rush
    units. With TA's lower sight and higher-arc cannons, raider rushes may be stronger here than on BOTA's values.
13. **Peewee vs A.K.**: nearly identical in TA (53/56 M, 250/265 HP, 1.8/1.72 speed). The Peewee's EMG now does 8 x 3
    per 0.4 s with a Cannon arc; check it still lands hits on moving targets at the edge of its 180 range (it did in
    the headless probe).
14. **Commander**: 3000 HP, speed 1.2, 25 E/s and 1 M/s income, D-Gun 30000 damage / 400 E per shot, build range 60.
    It is a much slower, more fragile commander than BOTA's (3500 HP, speed 1.8), so commander rushes are weaker.
15. **Experimental / long-range economy**: Vulcan (45 k M / 479 k E) and Buzzsaw (35 k M / 463 k E) vs Big Bertha /
    Intimidator (~4.2 k M / ~63 k E). In TA, multiple Berthas usually beat one Vulcan per metal spent; watch whether
    Recoil's targeting accuracy changes that.
16. **Fusion**: 1000 E/s for 5130 M (Cloakable/UW variants alike). TA's eco curve was steep; metal makers (0 M, 687 E)
    make Fusion + makers the standard T2 metal source, as in TA.

## Visual knobs (not balance)

17. **Cannon shells are faint**: Recoil draws cannons at alpha = `intensity` (0.2 for all here, as in BOTA). Sizes
    now scale with damage (2.5..16) and read well up close. At normal zoom, `intensity = 0.4-0.6` in
    `CannonSize`'s block of `weapondefs_post.lua` would make shells easier to follow.
18. **Laser bolt length** is still BOTA's `duration` on 10 weapons; TA's were shorter (e.g. 0.02 vs 0.04).
