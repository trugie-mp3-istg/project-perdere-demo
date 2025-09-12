from combat import *
from characters_allies import *
from characters_enemies_boss import *

ally_party = [kiri]
ally_party_june_retreat_s3 = []
enemy_party = [perd_midboss]

flavor_text_list = [
    "You won't have to listen to this giggle for long.",
    "... She might be mad.",
    "You don't feel any particular strong emotion toward this situation you're in."
]

turn = 0
while ally_party != [] and enemy_party != []:

    # Turn start
    turn += 1; announce_new_turn(turn)
    # Flavor text
    if turn != 3: print(random.choice(flavor_text_list))
    else: print("You should try to block this attack.")
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
            if enemy.is_stunned <= 0:
                if turn != 3:
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
                else: perd_midboss.s2(ally_party); pop_dead_man(ally_party, False)
            else: print(f"{enemy.name} is Stunned!\n")
        else: break
        if turn == 2: print("💬 Take this seriously! Do you want to bid your head farewell?!\n")

    # Turn end
    sleep(0.5)
    end_turn(participant_list)
    pop_dead_man(ally_party, False)
    pop_dead_man(enemy_party, True)

if not enemy_party:
    print("\n-----------------------\n#-#-#-# Victory #-#-#-#\n-----------------------"); exit(0)
elif not ally_party:
    print("\n.-- .... . .-. .\n.- .-. .\n-.-- --- ..- ..--.."); exit(0)