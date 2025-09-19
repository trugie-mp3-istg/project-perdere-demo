from combat import *
from characters_allies import *
from characters_enemies_boss import *

ally_party = [kiri, june, lachlan, emily]
ally_party_june_retreat_s3 = []
enemy_party = [abno_wolf]

flavor_text_list = [
    "The beast appeared before you.",
    "The beast looked at you with its blood-red eyes.",
    "The beast wreaked havoc upon this land, and countless other nameless land.",
    "The beast struck down any attempts to fell it with its pitch black claws.",
    "The beast were bound to this destructive role since long, long ago.",
    "The beast were needed to give sword-wielding humans their purposes.",
    "The beast were used to justify sword-wielding humans' thirst for violence.",
    "After all, what uses are hunters of without a prey?",
    "What are heroes without a villain?",
    "It was never spared from its fate. Never another choice.",
    "And thus it gave in, and became the villain for others to die to.",
    "Perhaps, you possess the strength to free it from its shackles."
]

turn = 0
while ally_party != [] and enemy_party != []:

    abno_wolf.dmg_multi = 0.5
    # Turn start
    turn += 1; announce_new_turn(turn)
    # Flavor text
    if turn <= 12: print(flavor_text_list[turn - 1])
    else: print(flavor_text_list[-1])

    # Special battle condition: Lurking Beast's SPD and damage multipliers increase after reaching 60% HP.
    # At 30% HP, SPD increases even more; has a chance to reflect damage back to attackers.
    # Increases damage taken when stunned.
    if abno_wolf.is_stunned > 0: abno_wolf.df_multi = 1.75
    else: abno_wolf.df_multi = 1.25
    if 0.3 * abno_wolf.max_hp < abno_wolf.cur_hp <= 0.6 * abno_wolf.max_hp:
        print(f"{abno_wolf.name} became stronger!")
        abno_wolf.spd = 3
        abno_wolf.buff = True
        abno_wolf.update_buff()
    if abno_wolf.cur_hp <= 0.3 * abno_wolf.max_hp:
        print(f"{abno_wolf.name} became devastatingly stronger!")
        abno_wolf.spd = 4
        abno_wolf.dmg_reflect_chance = 0.5
        abno_wolf.dmg_reflect_multi = 0.25

    if turn % 6 == 0 and abno_wolf.buff: print(f"\nThe beast glared at {ally_party[0].name} with wrathful eyes...")
    # HP
    participant_list = func_participant_list(ally_party, enemy_party)
    announce_hp_mp(participant_list)

    # Allies' turn
    if ally_party:
        sleep(0.5); print("\n|| Your turn ||"); sleep(0.5)
    for ally in ally_party:
        if enemy_party:
            if ally.is_stunned <= 0:
                if ally.is_furious <= 0:
                    for speed in range(ally.spd):
                        ally.action_choice(ally_party, enemy_party)
                        pop_dead_man(enemy_party, True)
                        print("")
                else:
                    ally.na(enemy_party)
                    pop_dead_man(enemy_party, True)
                    sleep(0.5); print("")
            else: sleep(0.5); print(f"{ally.name} is Stunned!\n"); sleep(0.5)
        else: break

    # June's Skill 3 LV3 charge.
    if june.red_dusk_s3_retreat:
        ally_party.pop(ally_party.index(june))
        ally_party_june_retreat_s3.append(june)

    # Enemies' turn
    if enemy_party:
        sleep(0.5); print("\n|| Enemies' turn ||"); sleep(0.5)
    for enemy in enemy_party:
        if ally_party:
            if enemy.is_stunned <= 0:
                if turn % 6 == 0:
                    if not abno_wolf.buff: abno_wolf.s2(ally_party)
                    else: abno_wolf.s4(ally_party)
                    print("")
                else:
                    if enemy.is_furious <= 0:
                        for speed in range(enemy.spd):
                            if ally_party:
                                enemy.enemy_action_random_choice(ally_party, enemy_party)
                                pop_dead_man(ally_party, False)
                                # Kiri's Skill 2 counter.
                                if (kiri in ally_party and kiri.shield_block == 0
                                        and kiri.polaris_s2_shield_broken_wait_trigger):
                                    # Detects if Kiri is still alive AND has his Shield broken while it's enhanced.
                                    sleep(0.5)
                                    kiri.s2_counter(enemy)
                                    pop_dead_man(enemy_party, True)
                                sleep(0.5); print("")
                            else: break
                    else:
                        enemy.na(ally_party)
                        pop_dead_man(ally_party, False)
                        sleep(0.5); print("")
            else: print("Lurking Beast is recovering from the impact...!\n");
        else: break

    # June's Skill 3
    if ally_party_june_retreat_s3 == [june]:
        sleep(0.5)
        june.s3_strike(enemy_party)
        ally_party_june_retreat_s3.pop(0)
        if kiri in ally_party: ally_party.insert(1, june)
        else: ally_party.insert(0, june)
        pop_dead_man(enemy_party, True)

    # Turn end
    sleep(0.5)
    end_turn(participant_list)
    pop_dead_man(ally_party, False)
    pop_dead_man(enemy_party, True)
    if lachlan in ally_party and lachlan.teal_blade > 0: # Lachlan's Skill 2 expires.
        lachlan.teal_blade -= 1
        if lachlan.teal_blade == 0: print("Lachlan's Attack enhancement expired!\n")
    for ally in ally_party: # Emily's Skill 2 expires.
        if ally.amber_moth > 0:
            ally.amber_moth -= 1
            ally.dmg_multi = 1
        if ally.amber_moth == 1:
            ally.dmg_multi *= 1.3

if not enemy_party:
    print("\n-----------------------\n#-#-#-# Victory #-#-#-#\n-----------------------"); exit(0)
elif not ally_party:
    print("\n.-- .... . .-. .\n.- .-. .\n-.-- --- ..- ..--.."); exit(0)