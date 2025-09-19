from combat import *
from characters_allies import *
from characters_enemies_boss import *

ally_party = [kiri]
ally_party_june_retreat_s3 = []
enemy_party = [lachlan_mboss]

flavor_text_list = [
    "This won't prove to be a pleasant experience.",
    "Lachlan glares at you, his blood boiling with rage. If his body has blood."
]

first_time_disarm = False
disarmed_focus = 2
disarmed_aggro = -1
s3_ready = False
enter_scripted_loss = False; enter_scripted_loss_june = False
turn = 0
while ally_party != [] and enemy_party != []:

    # If Lachlan has his blades, resets these values.
    if not lachlan_mboss.disarmed:
        disarmed_focus = 2
        disarmed_aggro = -1

    # Turn start
    turn += 1; announce_new_turn(turn)
    # Flavor text
    print(random.choice(flavor_text_list))
    if turn % 3 == 1 and turn != 1 and not lachlan_mboss.disarmed:
        print(f"He's ever-so-slightly losing his grip. Use your energy shield and bash his blades away.")
    if lachlan_mboss.disarmed:
        if disarmed_aggro < 3: print("Keep attacking to keep Lachlan distracted from his blades!")
        else: print("Lachlan looks particularly irritated."); s3_ready = True
    # HP
    participant_list = func_participant_list(ally_party, enemy_party)
    announce_hp_mp(participant_list)
    if not first_time_disarm and lachlan_mboss.disarmed:
        print("💬 Very well. You have grown so much since our last spar, and that is all I'm willing to commend you for.")
        first_time_disarm = True; sleep(1)
        print("You shuddered at the thoughts of him going melee with nothing but metal gauntlets, but here we are.")
        sleep(1); kiri.heal(kiri, 15)

    # Checks Lachlan's HP before action.
    if lachlan_mboss.disarmed:
        lachlan_cur_hp_snapshot = lachlan_mboss.cur_hp
    else: lachlan_cur_hp_snapshot = -1

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

    # If Lachlan's HP dropped (i.e. he was attacked) when unarmed, his focus stays and his aggro goes up.
    if lachlan_cur_hp_snapshot > lachlan_mboss.cur_hp or not lachlan_mboss.disarmed:
        disarmed_focus += 0
        disarmed_aggro += 1
    else: disarmed_focus -= 1
    # If disarmed_focus drops to 0, Lachlan regains blades. Battle re-enters phase 1.
    if lachlan_mboss.disarmed and disarmed_focus == 0:
        lachlan_mboss.disarmed = False
        print(f"... {lachlan_mboss.name} snatched his blades before you realized it!")

    # Enemies' turn
    if enemy_party:
        sleep(0.5); print("\n|| Enemies' turn ||"); sleep(0.5)
    for enemy in enemy_party:
        if ally_party:
            if enemy.is_stunned <= 0:
                if enemy.is_furious <= 0:
                    for speed in range(enemy.spd):
                        if ally_party:
                            if not enter_scripted_loss:
                                if not lachlan_mboss.disarmed:
                                    if turn % 3 != 1:
                                        if turn != 11: lachlan_mboss.na(ally_party)
                                        else: lachlan_mboss.s4(ally_party)
                                    else:
                                        if turn == 1: lachlan_mboss.na(ally_party)
                                        else: lachlan_mboss.s1(ally_party)
                                else:
                                    if not s3_ready: lachlan_mboss.s2(ally_party)
                                    else:
                                        if kiri.shield_block >= 2: enter_scripted_loss = True
                                        lachlan_mboss.s3(ally_party)
                                        if not enter_scripted_loss:
                                            lachlan_mboss.disarmed = False
                                            print(f"{lachlan_mboss.name} picked up his blades!")
                                        disarmed_focus = 2
                                        disarmed_aggro = -1
                                        s3_ready = False
                            else:
                                if lachlan_mboss.is_stunned <= 0:
                                    print("You briefly saw a red glimmer outside.")
                                    sleep(1); enter_scripted_loss_june = True
                                    print("💬 You have truly exceeded my expectation, KIRISAME CAMPBELL!")
                                    sleep(1); lachlan_mboss.s4(ally_party)
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
            else: print(f"{enemy.name} managed to get to his blades!\n")
        else: break

    # June's intervention
    if enter_scripted_loss_june:
        sleep(1.5)
        june_mboss.s2(enemy_party)

    # Turn end
    sleep(0.5)
    end_turn(participant_list)
    pop_dead_man(ally_party, False)
    pop_dead_man(enemy_party, True)

if not enter_scripted_loss_june:
    if not enemy_party:
        print("\n-----------------------\n#-#-#-# Victory #-#-#-#\n-----------------------"); exit(0)
    elif not ally_party:
        print("\n.-- .... . .-. .\n.- .-. .\n-.-- --- ..- ..--.."); exit(0)
else: print("\n------------------------\n#-#-#-# Survived #-#-#-#\n------------------------"); exit(0)