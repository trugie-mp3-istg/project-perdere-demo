from combat import *
from characters_allies import *
from characters_enemies import *

ally_party = [kiri, june, lachlan, emily]
enemy_party = [dal_riata, dummy]

dal_riata_flavor_text_list = [
    "Dullahan crackled loudly.",
    "Dullahan readied his glacier greatsword.",
    "The air turned bristly cold.",
    "Lachlan appeared restless.",
    "Lachlan grew impatient.",
    "Lachlan was losing his composure."
]

turn = 1

while dal_riata.cur_hp > 0:
    announce_new_turn(turn)
    print(random.choice(dal_riata_flavor_text_list))
    participant_list = func_participant_list(ally_party, enemy_party)
    announce_hp(participant_list)

    print("\n|| Your turn ||")
    for ally in ally_party:
        if ally.cur_hp > 0:
            ally.action_choice(ally_party, enemy_party)

    sleep(1)
    print("\n|| Enemies' turn ||")
    sleep(0.5)
    for enemy in enemy_party:
        target = random.choice(ally_party)
        enemy.attack_na_enemy(target)

    sleep(0.5)
    end_turn(participant_list)
    turn += 1
