import random
from time import sleep

class Character:

    def __init__(self, tag, name, lv, hp, atk, df, spd,
                 direct_res, bleed_res, burn_res,
                 na_count, na_mod,
                 s1_count, s1_mod,
                 s2_count, s2_mod,
                 s3_count, s3_mod,
                 s4_count, s4_mod,
                 s5_count, s5_mod,
                 dmg_multi, heal_multi):
        self.tag = tag; self.name = name; self.lv = lv
        self.max_hp = int(hp); self.cur_hp = int(hp)
        self.shield_hp = 0; self.shield_duration = 0
        self.atk = int(atk); self.df = int(df); self.df_mod = 1; self.spd = int(spd)
        self.direct_res = direct_res
        self.is_bleeding = 0; self.bleed_res = bleed_res
        self.is_burning = 0; self.burn_res = burn_res
        self.na_count = int(na_count); self.na_mod = na_mod
        self.s1_count = int(s1_count); self.s1_mod = s1_mod
        self.s2_count = int(s2_count); self.s2_mod = s2_mod
        self.s3_count = int(s3_count); self.s3_mod = s3_mod
        self.s4_count = int(s4_count); self.s4_mod = s4_mod
        self.s5_count = int(s5_count); self.s5_mod = s5_mod

        # Miscellaneous attributes:
        self.is_poisoned = 0; self.is_blind = 0; self.is_furious = 0

        self.dmg_multi = dmg_multi; self.heal_multi = heal_multi

    def compare_lv(self, target):
        """For damage calculation purposes: +10% damage per level difference."""
        if self.lv > target.lv:     return 1 + (self.lv - target.lv) * 0.1
        elif self.lv < target.lv:   return 1 - (target.lv - self.lv) * 0.1
        else:                       return 1

    def calculate_damage(self, target, mod):
        """Calculates attacks. Used for normal attacks and skills."""
        deviation = 1 + (random.random() / 5 * random.choice([1, -1])) # Damage deviates between 80% and 120%
        base_dmg = self.atk * mod
        """How much a hit hurts on paper, not including enemies' DEF, resistances, and damage deviation."""
        lv_diff = self.compare_lv(target)

        damage = int(round((base_dmg - target.df / 2 * target.df_mod) * lv_diff * deviation) * target.direct_res * self.dmg_multi)
        if damage < 1: damage = 1
        if target.shield_hp > 0:
            if target.shield_hp >= damage:
                target.shield_hp -= damage
            else:
                damage_left = damage - target.shield_hp
                target.shield_hp -= damage - damage_left
                target.cur_hp -= damage_left
        else: target.cur_hp -= damage

        if target.is_bleeding > 0: bleed_damage = self.do_bleed_damage(target)
        else: bleed_damage = 0
        return damage, bleed_damage

    def calculate_true_damage(self, target, mod):
        """Calculates attacks that ignore defense. Used for special attacks."""
        deviation = 1 + (random.random() / 5 * random.choice([1, -1])) # Damage deviates between 80% and 120%
        base_dmg = self.atk * mod
        """How much a hit hurts on paper, not including enemies' DEF, resistances, and damage deviation."""
        lv_diff = self.compare_lv(target)

        damage = int(round(base_dmg * lv_diff * deviation) * target.direct_res * self.dmg_multi)
        if damage < 1: damage = 1
        if target.shield_hp > 0:
            if target.shield_hp >= damage:
                target.shield_hp -= damage
            else:
                damage_left = damage - target.shield_hp
                target.shield_hp -= damage - damage_left
                target.cur_hp -= damage_left
        else: target.cur_hp -= damage

        if target.is_bleeding > 0: bleed_damage = self.do_bleed_damage(target)
        else: bleed_damage = 0
        return damage, bleed_damage

    def select_target_from_enemy_party(self, enemy_party):
        global target
        target_list = []
        for i in enemy_party:
            target_list.append(i.name)
        target_select = int(input(f"=> Who will {self.name} target? {target_list} <= "))
        for i in enemy_party:
            if enemy_party.index(i) == target_select - 1:
                target = i; break
        return target

    def func_attack(self, target, count, mod):
        """A normal attack. Needs target choosing mechanics and a text indicator to work."""
        for count in range(count):
            damage, bleed_damage = self.calculate_damage(target, mod)
            print(f"{damage} DMG")
            if bleed_damage > 0:
                target.cur_hp -= bleed_damage
                print(f"🩸 {target.name} took {bleed_damage} bleed DMG!")

    def do_bleed_damage(self, inflicted):
        """Calculates bleed damage every time the enemy is hit with a direct attack."""
        deviation = 1 + (random.random() / 5 * random.choice([1, -1])) # Damage deviates between 80% and 120%
        bleed_damage = round(self.lv * inflicted.bleed_res * deviation)
        if bleed_damage < 0: bleed_damage = 0
        return bleed_damage

    def do_burn_damage(self, inflicted):
        """Calculates burn damage at the end of each turn."""
        deviation = 1 + (random.random() / 5 * random.choice([1, -1])) # Damage deviates between 80% and 120%
        burn_damage = round((self.lv * self.atk / 2 * inflicted.burn_res - inflicted.df * inflicted.df_mod) * deviation)
        if burn_damage < 0: burn_damage = 0
        burning_dictionary.update({inflicted: burn_damage})

    def heal(self, target, amount):
        """Calculates a healing action."""
        if target.cur_hp < target.max_hp: # Heals if current HP is not at max
            amount_display = round(amount * self.heal_multi)
            if target.cur_hp + amount_display > target.max_hp:
                amount_display = target.max_hp - target.cur_hp # Visual indication of no overhealing
            target.cur_hp += amount_display
            if target == self: print(f"🞧 {self.name} recovered by {amount_display} HP!")
            else: print(f"🞧 {self.name} healed {target.name} by {amount_display} HP!")
        else: # If current HP is at max
            target.cur_hp = target.max_hp
            print(f"🞧 {target.name}'s HP was maxed out!")

    def defend(self):
        self.df_mod *= 2
        return self.df_mod

########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################

# Below is everything else that serves as part of a Turn Manager.

ally_mp_gauge = 0
def calculate_mp_cost(mp_cost):
    """Deducts skills' MP cost from MP gauge. Normal Attacks have a default cost of -1."""
    global ally_mp_gauge
    ally_mp_gauge -= mp_cost
    if ally_mp_gauge > 10: ally_mp_gauge = 10
    elif ally_mp_gauge < 0: ally_mp_gauge = 0
    return ally_mp_gauge

burning_dictionary = {} # Stores every burn damage instance in a dictionary to be accessed at turn end.

def func_participant_list(ally_party, enemy_party):
    participant_list = []
    for ally in ally_party: participant_list.append(ally)
    for enemy in enemy_party: participant_list.append(enemy)
    return participant_list

def announce_new_turn(turn):
    """Announces a new turn."""
    sleep(0.5); print(f"\n====== TURN {turn} ======"); sleep(0.5)

def announce_hp_mp(participant_list=None):
    """Announces everyone's HP and allies' MP at the start of every turn."""
    # HP
    if participant_list is None:
        participant_list = []
    for person in participant_list:
        if person.shield_hp <= 0:
            if person.is_bleeding > 0 >= person.is_burning:
                print(f"❤ {person.name}: {person.cur_hp}/{person.max_hp} 🩸")
            elif person.is_burning > 0 >= person.is_bleeding:
                print(f"❤ {person.name}: {person.cur_hp}/{person.max_hp} 🔥")
            elif person.is_bleeding > 0 and person.is_burning > 0:
                print(f"❤ {person.name}: {person.cur_hp}/{person.max_hp} 🩸🔥")
            else: print(f"❤ {person.name}: {person.cur_hp}/{person.max_hp}")
        else:
            if person.is_bleeding > 0 >= person.is_burning:
                print(f"❤ {person.name}: {person.cur_hp}/{person.max_hp} ({person.shield_hp}) 🩸")
            elif person.is_burning > 0 >= person.is_bleeding:
                print(f"❤ {person.name}: {person.cur_hp}/{person.max_hp} ({person.shield_hp}) 🔥")
            elif person.is_bleeding > 0 and person.is_burning > 0:
                print(f"❤ {person.name}: {person.cur_hp}/{person.max_hp} ({person.shield_hp}) 🩸🔥")
            else: print(f"❤ {person.name}: {person.cur_hp}/{person.max_hp} ({person.shield_hp})")
    # MP
    print(f"★ MP: {ally_mp_gauge}/10")

def end_turn(participant_list):
    """Performs janitory works, such as cleaning up status effects and burning down vermin."""

    # Refreshes (or reduces) temporary variables.
    for i in range(len(participant_list)):
        participant_list[i].df_mod = 1

        participant_list[i].shield_duration -= 1
        if participant_list[i].shield_duration <= 0:
            participant_list[i].shield_duration = 0
            participant_list[i].shield_hp = 0

        participant_list[i].is_bleeding -= 1
        if participant_list[i].is_bleeding < 0:
            participant_list[i].is_bleeding = 0

        participant_list[i].is_burning -= 1
        if participant_list[i].is_burning < 0:
            participant_list[i].is_burning = 0

    # Burn baby burn
    burn_no_more = [] # A list of those who are spared from burning (for now)
    for victim in burning_dictionary:
        victim.cur_hp -= burning_dictionary[victim]
        print(f"🔥 {victim.name} took {burning_dictionary[victim]} burn DMG!")
        if victim.is_burning == 0:
            burn_no_more.append(victim)
    for unvictim in burn_no_more: # Remove them out of the burndict after iteration
        del burning_dictionary[unvictim]

def pop_dead_man(person_party, is_enemy):
    """Pops characters from their party list if they are defeated."""
    for person in person_party:
        if person.cur_hp <= 0:
            person_party.pop(person_party.index(person))
            if person in burning_dictionary: # Removes person's name from burndict if in there
                burning_dictionary.pop(person)  # since they are already defeated.
            if is_enemy: print(f"■■■■ {person.name} was defeated! ■■■■")
            else: print(f"■■■■ {person.name} retreated! ■■■■")
