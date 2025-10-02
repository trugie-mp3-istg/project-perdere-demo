import random
from time import sleep

class Character:

    def __init__(self, tag, name, lv, hp, atk, df, spd,
                 direct_res, bleed_res, burn_res,
                 na_count, na_mod, s1_count, s1_mod,
                 s2_count, s2_mod, s3_count, s3_mod,
                 s4_count, s4_mod, s5_count, s5_mod, s6_count, s6_mod):
        # Identification tag and displayed name:
        self.tag = tag; self.name = name

        # Raw stats attributes:
        self.lv = lv; self.max_hp = int(hp); self.cur_hp = int(hp)
        self.atk = int(atk); self.df = int(df); self.spd = int(spd)

        # Direct attacks, bleed, and burn resistance attributes:
        self.direct_res = direct_res
        self.bleed_res = bleed_res
        self.burn_res = burn_res

        # Status effect attributes:
        self.is_bleeding = 0; self.is_burning = 0
        self.is_poisoned = 0
        self.is_blind = 0; self.is_furious = 0; self.is_stunned = 0

        # Attacks and skills' attributes:
        self.na_count = int(na_count); self.na_mod = na_mod
        self.s1_count = int(s1_count); self.s1_mod = s1_mod
        self.s2_count = int(s2_count); self.s2_mod = s2_mod
        self.s3_count = int(s3_count); self.s3_mod = s3_mod
        self.s4_count = int(s4_count); self.s4_mod = s4_mod
        self.s5_count = int(s5_count); self.s5_mod = s5_mod
        self.s6_count = int(s6_count); self.s6_mod = s6_mod

        # Miscellaneous attributes:
        self.dmg_multi = 1; self.heal_multi = 1; self.df_multi = 1
        self.is_defending = False
        # For positive DF, the higher df_multi is, the lower damage one takes.
        # The opposite goes for negative DF.
        self.shield_hp = 0; self.shield_hp_duration = 0; self.shield_block = 0
        self.dmg_reflect_chance = 0; self.dmg_reflect_multi = 0

    def compare_lv(self, target):
        """For damage calculation purposes: +10% damage per level difference."""
        if self.lv > target.lv:     return 1 + (self.lv - target.lv) * 0.1
        elif self.lv < target.lv:   return 1 - (target.lv - self.lv) * 0.1
        else:                       return 1

    def calculate_damage(self, target, mod):
        """Calculates attacks. Used for normal attacks and skills."""
        deviation = random.uniform(0.8, 1.2) # Damage deviates between 80% and 120%
        base_dmg = self.atk * mod
        lv_diff = self.compare_lv(target)

        damage = int(round((base_dmg - target.df / 2 * target.df_multi) * lv_diff * deviation) * target.direct_res * self.dmg_multi)
        if damage < 1: damage = 1
        if target.shield_block > 0:
            target.shield_block -= 1
            print(f"{target.name}'s shield absorbed a direct attack!")
        else:
            if target.shield_hp > 0:
                if target.shield_hp >= damage: target.shield_hp -= damage
                else:
                    damage_left = damage - target.shield_hp
                    target.shield_hp -= damage - damage_left
                    target.cur_hp -= damage_left
            else: target.cur_hp -= damage

        if target.is_bleeding > 0: bleed_damage = self.do_bleed_damage(target)
        else: bleed_damage = 0
        return damage, bleed_damage

    def calculate_true_damage(self, target, mod):
        """Calculates attacks that ignore defense. Used for certain attacks."""
        deviation = random.uniform(0.8, 1.2) # Damage deviates between 80% and 120%
        base_dmg = self.atk * mod
        lv_diff = self.compare_lv(target)

        target_df_final = target.df / 2 * target.df_multi
        if target_df_final > 0: target_df_final = 0
        damage = int(round((base_dmg - target_df_final) * lv_diff * deviation) * target.direct_res * self.dmg_multi)
        if damage < 1: damage = 1
        if target.shield_block > 0:
            target.shield_block -= 1
            print(f"{target.name}'s shield absorbed a direct attack!")
        else:
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
        """Serves as a target picker for ally skills. Does not work if ally is blinded or furious."""
        global target
        if self.is_blind <= 0 and self.is_furious <= 0:
            target_list = []
            for i in enemy_party:
                target_list.append(i.name)
            target_select_wip = input(f"=> Who will {self.name} target? {target_list} <= ")
            if target_select_wip.strip().isdigit() and 1 <= int(target_select_wip) <= len(target_list):
                target_select = int(target_select_wip)
                for i in enemy_party:
                    if enemy_party.index(i) == target_select - 1: target = i; break
            else: print("(Invalid target!)"); self.select_target_from_enemy_party(enemy_party)

        elif self.is_blind > 0:
            target = random.choice(enemy_party)
        elif self.is_furious > 0:
            target = enemy_party[0]
        return target

    def func_attack(self, target, count, mod):
        """An attack. Needs target choosing mechanics and a text indicator to work."""
        for count in range(count):
            if target.shield_block > 0: display_damage = False
            else: display_damage = True
            damage, bleed_damage = self.calculate_damage(target, mod)
            if display_damage:
                print(f"{damage} DMG")
            if bleed_damage > 0:
                if target.shield_block > 0:
                    target.shield_block -= 1
                    print(f"🩸 {target.name}'s shield absorbed Bleed damage!")
                else:
                    target.cur_hp -= bleed_damage
                    print(f"🩸 {target.name} took {bleed_damage} bleed DMG!")
            # If an attack skill does not directly inherit func_attack, copy the 12 lines above
            # Poison damage:
            if self.is_poisoned > 0: self.do_poison_damage()
            # If target has damage reflection:
            if target.dmg_reflect_multi > 0:
                if random.random() < target.dmg_reflect_chance:
                    damage_reflected = round(damage * target.dmg_reflect_multi)
                    if self.shield_block > 0:
                        target.shield_block -= 1
                        print(f"{target.name}'s shield absorbed reflected damage! ⊻")
                    else:
                        self.cur_hp -= damage_reflected
                        print(f"{self.name}'s attack was reflected back to sender!")
                        print(f"{damage_reflected} DMG ⊻")
            # If an attack skill does not directly inherit func_attack, copy the 7 lines above

    def do_fixed_damage(self, target, count, fdamage):
        """Like func_attack, but deals fixed damage. Is a special effect on its own, so does not trigger
        Bleed, Poison, or Reflect."""
        for count in range(count):
            if target.shield_block > 0:
                target.shield_block -= 1
                print(f"{target.name}'s shield absorbed fixed damage! ⦿")
            else:
                if target.shield_hp > 0:
                    if target.shield_hp >= fdamage:
                        target.shield_hp -= fdamage
                    else:
                        damage_left = fdamage - target.shield_hp
                        target.shield_hp -= fdamage - damage_left
                        print(f"{target.name}'s shield broke!")
                        target.cur_hp -= damage_left
                else: target.cur_hp -= fdamage
                print(f"{fdamage} DMG ⦿")

    def do_bleed_damage(self, inflicted):
        """Calculates bleed damage every time the enemy is hit with a direct attack."""
        deviation = random.uniform(0.8, 1.2) # Damage deviates between 80% and 120%
        bleed_damage = round(self.lv * inflicted.bleed_res * deviation)
        if bleed_damage < 0: bleed_damage = 0
        return bleed_damage

    def do_burn_damage(self, inflicted):
        """Calculates burn damage at the end of each turn."""
        deviation = random.uniform(0.8, 1.2) # Damage deviates between 80% and 120%
        burn_damage = round((self.lv * self.atk / 2 - inflicted.df * inflicted.df_multi) * inflicted.burn_res * deviation)
        if burn_damage < 0: burn_damage = 0
        burning_dictionary.update({inflicted: burn_damage})

    def do_poison_damage(self):
        """Calculates poison damage every time the enemy attacks."""
        deviation = random.uniform(0.8, 1.2) # Damage deviates between 80% and 120%
        poison_damage = round(self.lv * deviation)
        if poison_damage < 0: poison_damage = 0
        if self.shield_block > 0:
            self.shield_block -= 1
            print(f"🧪 {self.name}'s shield absorbed Poison damage!")
        else:
            self.cur_hp -= poison_damage
            print(f"🧪 {self.name} took {poison_damage} poison DMG!")

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
        self.is_defending = True
        self.df_multi *= 2
        return self.df_multi

# Below is everything else that serves as part of a Turn Manager.

ally_mp_gauge = 0
def calculate_mp_cost(mp_cost):
    """Deducts skills' MP cost from MP gauge. Normal Attacks have a default cost of -1."""
    global ally_mp_gauge
    ally_mp_gauge -= mp_cost
    if ally_mp_gauge > 10: ally_mp_gauge = 10
    elif ally_mp_gauge < 0: ally_mp_gauge = 0
    return ally_mp_gauge

def func_participant_list(ally_party, enemy_party):
    participant_list = []
    for ally in ally_party: participant_list.append(ally)
    participant_list.append(-1)
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
        else:
            # MP
            print(f"★ MP: {ally_mp_gauge}/10")
            print("---- ---- ---- ----")

burning_dictionary = {} # Stores every burn damage instance in a dictionary to be accessed at turn end.
def end_turn(participant_list):
    """Performs janitory works, such as cleaning up status effects and burning down vermin."""

    # Refreshes (or reduces) temporary variables.
    for i in range(len(participant_list)):
        if participant_list[i] != -1:
            participant_list[i].dmg_multi = 1
            participant_list[i].df_multi = 1

            participant_list[i].shield_hp_duration -= 1
            if participant_list[i].shield_hp_duration <= 0:
                participant_list[i].shield_hp_duration = 0
                participant_list[i].shield_hp = 0

            participant_list[i].is_defending = False

            participant_list[i].is_bleeding -= 1
            if participant_list[i].is_bleeding < 0: participant_list[i].is_bleeding = 0

            participant_list[i].is_burning -= 1
            if participant_list[i].is_burning < 0: participant_list[i].is_burning = 0

            participant_list[i].is_poisoned -= 1
            if participant_list[i].is_poisoned < 0: participant_list[i].is_poisoned = 0

            participant_list[i].is_blind -= 1
            if participant_list[i].is_blind < 0: participant_list[i].is_blind = 0

            participant_list[i].is_furious -= 1
            if participant_list[i].is_furious < 0: participant_list[i].is_furious = 0

            participant_list[i].is_stunned -= 1
            if participant_list[i].is_stunned < 0: participant_list[i].is_stunned = 0

    # Burn baby burn
    burn_no_more = [] # A list of those who are spared from burning (for now)
    for victim in burning_dictionary:
        if victim.shield_block > 0:
            victim.shield_block -= 1
            print(f"🔥 {victim.name}'s shield absorbed Burn damage!")
        else:
            victim.cur_hp -= burning_dictionary[victim]
            print(f"🔥 {victim.name} took {burning_dictionary[victim]} burn DMG!")
        if victim.is_burning == 0: burn_no_more.append(victim)
    for unvictim in burn_no_more: # Remove them out of the burndict after iteration
        del burning_dictionary[unvictim]

def pop_dead_man(person_party, is_enemy):
    """Pops characters from their party list if they are defeated."""
    for person in reversed(person_party):
        if person.cur_hp <= 0:
            person_party.pop(person_party.index(person))
            if person in burning_dictionary: # Removes person's name from burndict if in there
                burning_dictionary.pop(person)  # since they are already defeated.
            if is_enemy: print(f"■■■■ {person.name} was defeated! ■■■■")
            else: print(f"■■■■ {person.name} retreated! ■■■■")
