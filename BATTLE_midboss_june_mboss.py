from combat import *
from characters_allies import *
from characters_enemies import *
from characters_enemies_boss import *

ally_party = [kiri]
enemy_party = [june_mboss]
enemy_party_june_retreat = []

flavor_text_list = [
    "The hunt begins.",
    "But you haven't escaped the clutch of the Babel Hotel!",
    "Here she comes."
]

turn = 0
while ally_party != [] and enemy_party != []:

    # Turn start
    turn += 1; announce_new_turn(turn)
    # Flavor text
    if turn <= 2: print(flavor_text_list[0])
    else:
        if not june_mboss.s2_ready: print(flavor_text_list[1])
        else: print(flavor_text_list[2])
    # Special battle condition: Kiri heals 10 HP every turn and gains a damage boost, starting from turn 2.
    if turn > 1 and not june_mboss.s2_ready:
        print(f"{kiri.name} took a hasty breather!")
        kiri.heal(kiri, 10)
        kiri.dmg_multi = 1.5
    if turn == 3:
        enemy_party.append(perd_hunter_1)
        enemy_party.append(perd_goon_1_1)
        enemy_party.pop(0)
        enemy_party_june_retreat.append(june_mboss)
    if turn == 6:
        enemy_party.append(perd_hunter_2)
        print(f"{perd_hunter_2.name} joined the hunt!")
    if turn == 9:
        enemy_party.append(perd_goon_1_2)
        print(f"{perd_goon_1_2.name} joined the hunt!")
    if turn == 11:
        enemy_party.append(perd_goon_2_1)
        print(f"{perd_goon_2_1.name} joined the hunt!")
    if turn == 13:
        enemy_party.append(perd_goon_2_2)
        print(f"{perd_goon_2_2.name} joined the hunt!")
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

    # Enemies' turn
    if enemy_party:
        sleep(0.5); print("\n|| Enemies' turn ||"); sleep(0.5)
    for enemy in enemy_party:
        if ally_party:
            if not june_mboss.s2_ready:
                if enemy.is_stunned <= 0:
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
                else: print(f"{enemy.name} is Stunned!\n")
            else: june_mboss.s2(ally_party)
        else: break

    if turn == 2: print("Kiri managed to get away... for now!")

    if not enemy_party and enemy_party_june_retreat == [june_mboss]:
        enemy_party.append(june_mboss)
        enemy_party_june_retreat.pop(0)
        sleep(1)
        print("... But June has already caught up long ago!")
        june_mboss.s2_ready = True

    # Turn end
    sleep(0.5)
    end_turn(participant_list)
    pop_dead_man(ally_party, False)
    pop_dead_man(enemy_party, True)

if not enemy_party:
    print("\n-----------------------\n#-#-#-# Victory #-#-#-#\n-----------------------"); exit(0)
elif not ally_party:
    if june_mboss.s2_ready:
        print("\n--------------------------\n#-#-#-# Defeat...? #-#-#-#\n--------------------------"); exit(0)
    else: print("\n.-- .... . .-. .\n.- .-. .\n-.-- --- ..- ..--.."); exit(0)