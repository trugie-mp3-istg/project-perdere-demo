from combat import *
from characters_enemies import *
from characters_enemies_boss import *

# This file is for testing enemies' powers against one another.

def announce_hp_arena(participant_list=None):
    """Announces everyone's HP at the start of every turn."""
    # HP
    if participant_list is None:
        participant_list = []
    for person in participant_list:
        if person != -1:
            announce_shield_hp = ""; announce_shield_block = ""; announce_reflect = ""
            announce_bleeding = ""; announce_burning = ""; announce_poisoned = ""

            if person.shield_hp > 0: announce_shield_hp = f"({person.shield_hp}) "
            if person.shield_block > 0: announce_shield_block = f"[{person.shield_block}] "
            if person.dmg_reflect_chance > 0 and person.dmg_reflect_multi > 0: announce_reflect = "{⊻} "
            if person.is_bleeding > 0: announce_bleeding = "🩸 "
            if person.is_burning > 0: announce_burning = "🔥 "
            if person.is_poisoned > 0: announce_poisoned = "🧪 "
            print(f"❤ {person.name}: {person.cur_hp}/{person.max_hp} "
                  f"{announce_shield_hp}{announce_shield_block}{announce_reflect}"
                  f"{announce_bleeding}{announce_burning}{announce_poisoned}")
            if person.is_stunned <= 0:
                if person.is_blind > 0: print(f"{person.name} is Blinded! Target randomized!")
                if person.is_furious > 0: print(f"{person.name} is Furious and will automatically Attack the first enemy!")
            else: print(f"{person.name} is Stunned! Cannot act!")
        else: print("---- ---- ---- ----")

enemy_party_a = [pollux]
enemy_party_b = [dal_riata]

flavor_text_list = [
    "You watch the brawl from afar to kill some time.",
    "June seems uninterested.",
    "Lachlan watches the fight with utmost seriousness.",
    "Emily is cheering for god-knows-who.",
    "You wonder if that woman would have still scolded you for spacing out now.",
]

turn = 0
while enemy_party_a != [] and enemy_party_b != []:

    # Turn start
    turn += 1; announce_new_turn(turn)
    # Flavor text
    print(random.choice(flavor_text_list))
    # HP
    participant_list = func_participant_list(enemy_party_a, enemy_party_b)
    announce_hp_arena(participant_list)

    start_turn_input = input("(Press Enter to start this turn.) ")

    # Team A's turn
    if enemy_party_a:
        sleep(0.5); print("\n|| Team A's turn ||"); sleep(0.5)
    for person in enemy_party_a:
        if enemy_party_b:
            if person.is_stunned <= 0:
                if person.is_furious <= 0:
                    for speed in range(person.spd):
                        if enemy_party_b:
                            person.enemy_action_random_choice(enemy_party_b, enemy_party_a)
                            pop_dead_man(enemy_party_b, True)
                            sleep(1); print("")
                        else: break
                else:
                    person.na(enemy_party_b)
                    pop_dead_man(enemy_party_b, True)
                    sleep(1); print("")
            else: sleep(1); print(f"{person.name} is Stunned!\n"); sleep(1)
        else: break

    # Team B's turn
    if enemy_party_b:
        sleep(0.5); print("\n|| Team B's turn ||"); sleep(0.5)
    for person in enemy_party_b:
        if enemy_party_a:
            if person.is_stunned <= 0:
                if person.is_furious <= 0:
                    for speed in range(person.spd):
                        if enemy_party_a:
                            person.enemy_action_random_choice(enemy_party_a, enemy_party_b)
                            pop_dead_man(enemy_party_a, True)
                            sleep(1); print("")
                        else: break
                else:
                    person.na(enemy_party_a)
                    pop_dead_man(enemy_party_a, True)
                    sleep(1); print("")
            else: sleep(1); print(f"{person.name} is Stunned!\n"); sleep(1)
        else: break

    # Turn end
    sleep(0.5)
    end_turn(participant_list)
    pop_dead_man(enemy_party_a, True)
    pop_dead_man(enemy_party_b, True)

if not enemy_party_b:
    print("\n----------------------------\n#-#-#-# Team A wins! #-#-#-#\n----------------------------"); exit(0)
elif not enemy_party_a:
    print("\n----------------------------\n#-#-#-# Team B wins! #-#-#-#\n----------------------------"); exit(0)