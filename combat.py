import random
from time import sleep

class Character:

    def __init__(self, tag, name, lv, max_hp, cur_hp, atk, df, spd,
                 direct_res, is_bleeding, bleed_res, is_burning, burn_res,
                 na_count, na_mod,
                 s1_count, s1_mod,
                 dmg_multi):
        self.tag = tag; self.name = name; self.lv = lv
        self.max_hp = int(max_hp); self.cur_hp = int(cur_hp)
        self.atk = int(atk); self.df = int(df); self.spd = int(spd)
        self.direct_res = direct_res
        self.is_bleeding = is_bleeding; self.bleed_res = bleed_res
        self.is_burning = is_burning; self.burn_res = burn_res
        self.na_count = int(na_count); self.na_mod = na_mod
        self.s1_count = int(s1_count); self.s1_mod = s1_mod
        self.dmg_multi = dmg_multi

    def compare_lv(self, target):
        """For damage calculation purposes: +10% damage per level difference."""
        if self.lv > target.lv:
            return 1 + (self.lv - target.lv) * 0.1
        elif self.lv < target.lv:
            return 1 - (target.lv - self.lv) * 0.1
        else:
            return 1

    def heal(self, target, amount):
        """Calculates a healing action."""
        if target.cur_hp < target.max_hp: # Heals if current HP is not at max
            amount_display = round(amount)
            if target.cur_hp + amount_display > target.max_hp:
                amount_display = target.max_hp - target.cur_hp # Visual indication of no overhealing
            target.cur_hp += amount_display
            if target == self:
                print(f"🞧 {self.name} recovered by {amount_display} HP!")
            else:
                print(f"🞧 {self.name} healed {target.name} by {amount_display} HP!")
        else: # If current HP is at max
            target.cur_hp = target.max_hp
            print(f"🞧 {target.name}'s HP was maxed out!")

    def do_bleed_damage(self, inflicted):
        """Calculates bleed damage every time the enemy is hit with a direct attack."""
        deviation = 1 + (random.random() / 5 * random.choice([1, -1])) # Damage deviates between 80% and 120%
        bleed_damage = round(self.lv * inflicted.bleed_res * deviation)
        return bleed_damage

    def do_burn_damage(self, inflicted):
        """Calculates burn damage at the end of each turn."""
        deviation = 1 + (random.random() / 5 * random.choice([1, -1])) # Damage deviates between 80% and 120%
        burn_damage = round((self.lv * self.atk / 2 * inflicted.burn_res - inflicted.df) * deviation)
        burning_dictionary.update({inflicted: burn_damage})

    def attack(self, target, mod):
        """Calculates attacks. Used for normal attacks and skills."""
        deviation = 1 + (random.random() / 5 * random.choice([1, -1])) # Damage deviates between 80% and 120%
        base_dmg = self.atk * mod
        """How much a hit hurts on paper, not including enemies' DEF, resistances, and damage deviation."""
        lv_diff = self.compare_lv(target)

        damage = int(round((base_dmg - target.df / 2) * lv_diff * deviation) * target.direct_res * self.dmg_multi)
        if damage < 1:
            damage = 1
        target.cur_hp -= damage

        if target.is_bleeding > 0:
            bleed_damage = self.do_bleed_damage(target)
        else:
            bleed_damage = 0
        return damage, bleed_damage

    def attack_na(self, target):
        """A normal attack."""
        for turn in range(self.na_count):
            damage, bleed_damage = self.attack(target, self.na_mod)
            print(f"{self.name} attacked {target.name}!\n{damage} DMG")
            if bleed_damage > 0:
                target.cur_hp -= bleed_damage
                print(f"🩸 {target.name} took {bleed_damage} bleed DMG!")

    def attack_na_enemy(self, target):
        """A normal attack for enemies."""
        for turn in range(self.na_count):
            damage, bleed_damage = self.attack(target, self.na_mod)
            print(f"{self.name} attacked {target.name}!\n{damage} DMG")
            if bleed_damage > 0:
                target.cur_hp -= bleed_damage
                print(f"🩸 {target.name} took {bleed_damage} bleed DMG!")

    def defend(self):
        original_df = self.df
        self.df *= 2
        return original_df

# Below is everything else that serves as part of a Turn Manager.

burning_dictionary = {} # Stores every burn damage instance in a dictionary to be accessed at turn end.

def func_participant_list(ally_party=None, enemy_party=None):
    if enemy_party is None:
        enemy_party = []
    if ally_party is None:
        ally_party = []
    participant_list = []
    for ally in ally_party:
        participant_list.append(ally)
    for enemy in enemy_party:
        participant_list.append(enemy)
    return participant_list

def announce_new_turn(turn):
    """Announces a new turn."""
    sleep(0.5)
    print(f"\n====== Turn {turn} ======")
    sleep(1)

def announce_hp(participant_list=None):
    """Announces everyone's HP at the start of every turn."""
    if participant_list is None:
        participant_list = []
    for person in participant_list:
        print(f"❤ {person.name}: {person.cur_hp}/{person.max_hp}")

def end_turn(participant_list=None):
    """Performs janitory works, such as cleaning up status effects and burning down vermin."""
    if participant_list is None:
        participant_list = []

    # Refreshes (or reduces) is_bleeding and is_burning variables.
    for i in range(len(participant_list)):
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