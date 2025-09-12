import random, time
from time import sleep

from combat import Character
from pd_parameter_stats import *

class PerdMidboss(Character):
    def __init__(self):
        super().__init__(*perd_midboss_pd_stats)

    def enemy_action_random_choice(self, ally_party, enemy_party):
        available_actions = [0, 0, 1]
        choice = random.choice(available_actions)
        if choice == 0: self.na(ally_party)
        if choice == 1: self.s1(ally_party)

    def na(self, ally_party):
        """Attacks an enemy once."""
        target = random.choice(ally_party)
        print(f"{self.name} charged at {target.name} with her knife!")
        self.func_attack(target, self.na_count, self.na_mod)

    def s1(self, ally_party):
        """Attacks an enemy twice."""
        target = random.choice(ally_party)
        print(f"{self.name} swung her knife wildly at {target.name}!")
        self.func_attack(target, self.s1_count, self.s1_mod)

    def s2(self, ally_party):
        """Attacks an enemy once with great power if unopposed. Inflicts Bleed this turn and follows up with 1 Attack."""
        target = random.choice(ally_party)
        if target.df_multi <= 1:
            print(f"{self.name} dug her knife deep into {target.name}!")
            self.func_attack(target, self.s2_count, self.s2_mod + 0.5)
            target.is_bleeding += 1
            Character.do_bleed_damage(self, target)
            if target.is_bleeding > 0: print(f"{target.name} is bleeding!")
            sleep(0.5)
            print(f"{self.name} took an opportunity to attack {target.name}!")
            self.func_attack(target, self.na_count, self.na_mod + 0.5)
            sleep(0.5)
            print(f"{self.name} became invigorated! DF up!")
            self.df += 10
        else:
            print(f"{self.name} tried to stab {target.name}...")
            self.func_attack(target, self.s2_count, self.s2_mod / 2)
            print("... and failed!")
            sleep(0.5)
            print(f"{self.name} became demoralized! DF down!")
            self.df -= 10
perd_midboss_pd_stats = []
insert_stat_by_id_num(pd_stats_column_list, 110, perd_midboss_pd_stats)
perd_midboss = PerdMidboss()

class JuneMboss(Character):
    def __init__(self):
        super().__init__(*june_mboss_stats)
        self.s2_ready = False

    def enemy_action_random_choice(self, ally_party, enemy_party):
        available_actions = [0, 1]
        choice = random.choice(available_actions)
        if choice == 0: self.na(ally_party)
        if choice == 1: self.s1(ally_party)

    def na(self, ally_party):
        """Attacks an enemy twice."""
        target = random.choice(ally_party)
        print("June attacked!")
        self.func_attack(target, self.na_count, self.na_mod)

    def s1(self, ally_party):
        """Attacks an enemy thrice."""
        target = random.choice(ally_party)
        print("June attacked!")
        self.func_attack(target, self.s1_count, self.s1_mod)

    def s2(self, target):
        """Attacks an enemy once, ignoring defense."""
        print(f"June used ✦Red Dusk✦ and is charging at {target.name} with immense speed...!"); sleep(0.5)
        print(f"..."); sleep(0.5)
        print(f"...!"); sleep(0.5)
        for count in range(self.s2_count):
            damage, bleed_damage = self.calculate_true_damage(target, self.s2_mod)
            print(f"{damage} DMG")
            if bleed_damage > 0:
                target.cur_hp -= bleed_damage
                print(f"🩸 {target.name} took {bleed_damage} bleed DMG!")
june_mboss_stats = []
insert_stat_by_id_num(pd_stats_column_list, 111, june_mboss_stats)
june_mboss = JuneMboss()

class Aubrey(Character):
    def __init__(self):
        super().__init__(*aubrey_pd_stats)

    def enemy_action_random_choice(self, ally_party, enemy_party):
        available_actions = [0, 1]
        choice = random.choice(available_actions)
        if choice == 0: self.na(ally_party)
        if choice == 1: self.s1(ally_party)
        if choice == 2: self.s2(ally_party)

    def na(self, ally_party):
        """Attacks an enemy once."""
        target = random.choice(ally_party)
        print(f"{self.name} kicked {target.name}!")
        self.func_attack(target, self.na_count, self.na_mod)

    def s1(self, ally_party):
        """Attacks an enemy twice. Has a chance to inflict Poison next turn."""
        target = random.choice(ally_party)
        print(f"{self.name} fired poison darts at {target.name}!")
        self.func_attack(target, self.s1_count, self.s1_mod)
        if random.random() < 0.5:
            if target.is_poisoned <= 2: target.is_poisoned = 2
            print(f"{target.name} is poisoned!")

    def s2(self, ally_party):
        """Attacks all enemies once, inflicting Poison 2 next turns."""
        print(f"{self.name} threw a poison bomb!")
        for target in ally_party:
            print(f"{target.name} took damage!")
            self.func_attack(target, self.s2_count, self.s2_mod)
            if target.is_poisoned <= 3: target.is_poisoned = 3
            print(f"{target.name} is poisoned!")
aubrey_pd_stats = []
insert_stat_by_id_num(pd_stats_column_list, 190, aubrey_pd_stats)
aubrey = Aubrey()

class AbnoWolf(Character):
    def __init__(self):
        super().__init__(*abno_wolf_pd_stats)
        self.buff = False

    def enemy_action_random_choice(self, ally_party, enemy_party):
        available_actions = [0, 1, 3]
        if self.cur_hp <= 0.3 * self.max_hp: available_actions.append(2)
        choice = random.choice(available_actions)
        if choice == 0: self.na(ally_party)
        if choice == 1: self.s1(ally_party)
        if choice == 2: self.s2(ally_party)
        if choice == 3: self.s3(ally_party)

    def update_buff(self):
        if not self.buff:   self.na_mod = 0.4; self.s1_mod = 0.8;   self.s3_mod = 0.6
        if self.buff:       self.na_mod = 0.6; self.s1_mod = 1;     self.s3_mod = 0.8

    def na(self, ally_party):
        """Attacks an enemy thrice."""
        target = random.choice(ally_party)
        print(f"{self.name} attacked {target.name} with its claws!")
        self.func_attack(target, self.na_count, self.na_mod)

    def s1(self, ally_party):
        """Attacks an enemy once."""
        target = random.choice(ally_party)
        print(f"{self.name} attacked {target.name} with its tail!")
        self.func_attack(target, self.s1_count, self.s1_mod)

    def s2(self, ally_party):
        """Attacks all enemies thrice. If the enemy's current HP is below 50%, inflicts Furious 1 next turn."""
        print(f"{self.name} let out a visceral howl!")
        for target in ally_party:
            print(f"{target.name} took damage!")
            self.func_attack(target, self.s2_count, self.s2_mod)
            if target.cur_hp <= 0.5 * target.max_hp:
                if random.random() < 0.5:
                    target.is_furious = 2
                    print(f"{target.name} was startled and became Furious!")

    def s3(self, ally_party):
        """Attacks an enemy twice. If the enemy's current HP is below 50%, inflicts Bleed this turn and 1 next turn."""
        target = random.choice(ally_party)
        print(f"{self.name} attacked {target.name} with its fangs bare!")
        self.func_attack(target, self.s3_count, self.s3_mod)
        if target.cur_hp <= 0.5 * target.max_hp:
            if target.is_bleeding < 2: target.is_bleeding = 2
            Character.do_bleed_damage(self, target)
            if target.is_bleeding > 0: print(f"{target.name} is bleeding!")

    def s4(self, ally_party):
        """Attacks each enemy once in turn. If an enemy raises a shield, halts attacking and becomes stunned next turn."""
        for target in ally_party:
            print(f"{self.name} is ramming into {target.name}'s direction!")
            if target.shield_hp <= 0:
                if target.df_multi <= 1: self.func_attack(target, self.s4_count, self.s4_mod)
                else: self.func_attack(target, self.s4_count, self.s4_mod / 2)
            else:
                print(f"... and crashed into {target.name}'s shield!")
                self.func_attack(target, self.s4_count, self.s4_mod / 2)
                target.shield_hp = 0
                self.is_stunned = 2
                print(f"{target.name}'s shield broke! {self.name} is stunned for 1 next turn!")
                break
abno_wolf_pd_stats = []
insert_stat_by_id_num(pd_stats_column_list, 901, abno_wolf_pd_stats)
abno_wolf = AbnoWolf()

class DalRiata(Character):
    def __init__(self):
        super().__init__(*dal_riata_pd_stats)
        self.s5_follow_up = False

    def enemy_action_random_choice(self, ally_party, enemy_party):
        available_actions = [0, 1, 2, 3, 4]
        choice = random.choice(available_actions)
        if choice == 0: self.na(ally_party)
        if choice == 1: self.s1(ally_party)
        if choice == 2: self.s2(ally_party)
        if choice == 3: self.s3(ally_party)
        if choice == 4: self.s4(ally_party)

    def na(self, ally_party):
        """Attacks an enemy twice."""
        target = random.choice(ally_party)
        print(f"{self.name} attacked {target.name}!")
        self.func_attack(target, self.na_count, self.na_mod)

    def s1(self, ally_party):
        """Attacks up to 2 enemies once. Has a chance of inflicting Bleed this turn and 1 next turn."""
        if len(ally_party) > 1: target_list = random.choices(ally_party, k=2)
        else: target_list = random.choices(ally_party, k=1)
        print(f"{self.name} used ✦Azure Gale✦!")
        for target in target_list:
            print(f"{target.name} was swept up in the attack!")
            self.func_attack(target, self.s1_count, self.s1_mod)
            if random.random() < 0.33:
                if target.is_bleeding < 2: target.is_bleeding = 2
                Character.do_bleed_damage(self, target)
                if target.is_bleeding > 0: print(f"{target.name} is bleeding!")

    def s2(self, ally_party):
        """Attacks an enemy once, inflicting Bleed this turn and 1 next turn."""
        target = random.choice(ally_party)
        print(f"{self.name} struck {target.name} with frostbite!")
        self.func_attack(target, self.s2_count, self.s2_mod)
        if target.is_bleeding < 2: target.is_bleeding = 2
        Character.do_bleed_damage(self, target)
        if target.is_bleeding > 0: print(f"{target.name} is bleeding!")

    def s3(self, ally_party):
        """Attacks all enemies thrice with low damage."""
        print(f"{self.name} summoned a blizzard!")
        for ally in ally_party:
            target = ally
            print(f"{target.name} was hit!")
            self.func_attack(target, self.s3_count, self.s3_mod)

    def s4(self, ally_party):
        """Attacks an enemy twice with varying strength. Has a chance to heal by double of damage dealt."""
        target = random.choice(ally_party)
        print(f"Dullahan cast ✦Fear Of Cold✦!")
        print(f"Dullahan attacked {target.name}!")
        for count in range(self.s4_count):
            damage, bleed_damage = self.calculate_damage(target, self.s4_mod + random.uniform(-0.2, 0.2))
            print(f"{damage} DMG")
            if bleed_damage > 0:
                target.cur_hp -= bleed_damage
                print(f"🩸 {target.name} took {bleed_damage} bleed DMG!")
            if random.random() < 0.25:
                self.heal(self, damage * 2)
            if self.is_poisoned > 0: self.do_poison_damage()

    def s5(self, ally_party, target):
        """Attacks an enemy thrice and heals 100 HP.
        If target is defeated, heals another 200 HP and follows up with 2 Attacks."""
        if target not in ally_party:
            target = random.choice(ally_party)
        print(f"Dullahan used ✦Azure Blade of Fate✦ and charged at {target.name} with a deathly grin...!")
        for count in range(self.s5_count):
            time.sleep(0.5)
            damage, bleed_damage = self.calculate_damage(target, self.s5_mod)
            print(f"{damage} DMG")
            if bleed_damage > 0:
                target.cur_hp -= bleed_damage
                print(f"🩸 {target.name} took {bleed_damage} bleed DMG!")
            if self.is_poisoned > 0: self.do_poison_damage()
        self.heal(self, 100)
        if target.cur_hp <= 0 and ally_party != []:
            self.s5_follow_up = True
dal_riata_pd_stats = []
insert_stat_by_id_num(pd_stats_column_list, 290, dal_riata_pd_stats)
dal_riata = DalRiata()