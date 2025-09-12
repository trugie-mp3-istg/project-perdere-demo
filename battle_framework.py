from combat import *
from characters_allies import *
from characters_enemies import *
from characters_enemies_boss import *

ally_party = [kiri, june, lachlan, emily]
ally_party_june_retreat_s3 = []
enemy_party = [sanc_fixer_0_1, sanc_fixer_0_2, sanc_guard_a, sanc_guard_b]

flavor_text_list = [
    "Let's get this over with.",
    "Placeholder flavor text 1.",
    "Placeholder flavor text 2.",
    "Placeholder flavor text 3.",
]

turn = 0
while ally_party != [] and enemy_party != []:

    # Turn start
    turn += 1; announce_new_turn(turn)
    # Flavor text
    print(random.choice(flavor_text_list))
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
                if enemy.is_furious <= 0:
                    for speed in range(enemy.spd):
                        enemy.enemy_action_random_choice(ally_party, enemy_party)
                        pop_dead_man(ally_party, False)
                        # Kiri's Skill 2 counter.
                        if kiri in ally_party and kiri.shield_hp < kiri.polaris_s2_shield_hp_detect_hit:
                            # Detects if Kiri is still alive AND has taken shield_hp damage while it's enhanced.
                            sleep(0.5)
                            kiri.s2_counter(enemy)
                            pop_dead_man(enemy_party, True)
                        sleep(0.5); print("")
                else:
                    enemy.na(ally_party)
                    pop_dead_man(ally_party, False)
                    sleep(0.5); print("")
            else: print(f"{enemy.name} is Stunned!\n")
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