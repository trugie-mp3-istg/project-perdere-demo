from combat import *
from characters_allies import *
from characters_enemies_boss import *

ally_party = [kiri, june, lachlan]
ally_party_june_retreat_s3 = []
enemy_party = [dal_riata]

dal_riata_flavor_text_list = [
    "Dullahan crackled loudly.",
    "The air turned bristly cold.",
    "Lachlan grew impatient.",
    "Lachlan appeared restless.",
    "Lachlan was losing his composure.",
    "Dullahan broke a sweat. A grin bloomed on his face.",
    "The cold wind turned hostile. They'll have to hurry.",
    "Both sides grew weary, one of the cold, and one of the heat."
]

turn = 0
while ally_party != [] and enemy_party != []:

    # Turn start
    turn += 1; announce_new_turn(turn)
    # Flavor text
    if turn <= 7: print(dal_riata_flavor_text_list[turn - 1])
    else: print(dal_riata_flavor_text_list[7])
    # HP
    if turn == 7 and emily not in ally_party:
        ally_party.append(emily)
        sleep(0.5)
        print("💬 Hang in there! Y'all better be thankful I'm coming to bail your asses out of winter!\nEmily joined the battle!")
        sleep(0.5)
    participant_list = func_participant_list(ally_party, enemy_party)
    announce_hp_mp(participant_list)

    # Special battle condition
    if turn >= 7:
        if turn == 7: print("Dullahan appeared to be exhausted...!")
        dal_riata.df_mod *= 0.7

    # Allies' turn
    if ally_party:
        sleep(0.5); print("\n|| Your turn ||"); sleep(0.5)
    for ally in ally_party:
        for speed in range(ally.spd):
            if enemy_party:
                ally.action_choice(ally_party, enemy_party)
                pop_dead_man(enemy_party, True)
    pop_dead_man(enemy_party, True)

    # June's Skill 2 LV3 charge.
    if june.red_dusk_s2_retreat:
        ally_party.pop(ally_party.index(june))
        ally_party_june_retreat_s3.append(june)

    # Enemies' turn
    if enemy_party:
        sleep(0.5); print("\n|| Enemies' turn ||"); sleep(0.5)
    for enemy in enemy_party:
        for speed in range(enemy.spd):
            if ally_party:
                enemy.enemy_action_random_choice(ally_party, enemy_party)
                pop_dead_man(ally_party, False)

                # Kiri's Skill 2 counter.
                if kiri in ally_party and kiri.shield_hp < kiri.polaris_s2_shield_hp_detect_hit:
                    # Detects if Kiri is still alive AND has taken shield_hp damage while it's enhanced.
                    sleep(0.5)
                    kiri.s2_counter(enemy)
                    pop_dead_man(enemy_party, True)
                    sleep(0.5)
                print("")
            else: break

        # Dal Riata's scripted Skill 5 attack.
        sleep(0.5)
        if turn % 5 == 0:
            if turn == 5:
                if lachlan not in ally_party: dal_riata_s5_target = random.choice(ally_party)
                else: dal_riata_s5_target = lachlan
                print(f"💬 Huff... Huff... Still standing, huh...! Then s'pose all bets are off the table!")
            else: dal_riata_s5_target = random.choice(ally_party)
            print(f"Dullahan is preparing an attack against {dal_riata_s5_target.name}...\n")
        if turn % 5 == 1 and turn != 1:
            dal_riata.s5(ally_party, dal_riata_s5_target)
        pop_dead_man(ally_party, False)

        if dal_riata.s5_follow_up:
            sleep(0.5)
            print("Dullahan is on a streak of bloodlust!")
            for i in range(2):
                dal_riata.na(ally_party)
                pop_dead_man(ally_party, False)
            dal_riata.s5_follow_up = False

    # June's Skill 3
    if ally_party_june_retreat_s3 == [june]:
        sleep(0.5)
        june.s3(enemy_party)
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