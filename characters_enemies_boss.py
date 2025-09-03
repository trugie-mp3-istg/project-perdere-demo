import random, time
from time import sleep

from combat import Character
from pd_parameter_stats import *

class PerdMidboss(Character):
    def __init__(self):
        super().__init__(*perd_midboss_pd_stats, 1, 1)

    def enemy_action_random_choice(self, ally_party, enemy_party):
        available_actions = [0, 1]
        choice = random.choice(available_actions)
        if choice == 0: self.na(ally_party)
        if choice == 1: self.s1(ally_party)
        if choice == 2: self.s2(ally_party)

    def na(self, ally_party):
        """Attacks an enemy once."""
        target = random.choice(ally_party)
        print(f"{self.name} attacked {target.name}!")
        self.func_attack(target, self.na_count, self.na_mod)

    def s1(self, ally_party):
        """Attacks an enemy twice."""
        target = random.choice(ally_party)
        print(f"{self.name} swung her knife wildly at {target.name}!")
        self.func_attack(target, self.s1_count, self.s1_mod)

    def s2(self, ally_party):
        """Attacks an enemy once with great power if unopposed. Inflicts Bleed this turn and follows up with 1 Attack."""
        target = random.choice(ally_party)
        if target.df_mod <= 1:
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
insert_stat_by_id_num(pd_stats_column_list, 102, perd_midboss_pd_stats)
perd_midboss = PerdMidboss()

########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################

class DalRiata(Character):
    def __init__(self):
        super().__init__(*dal_riata_pd_stats,1, 1)
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
        """Attacks an enemy twice with varying strength. Has a low chance to heal by damage dealt."""
        target = random.choice(ally_party)
        print(f"Dullahan cast ✦Fear Of Cold✦!")
        print(f"Dullahan attacked {target.name}!")
        for count in range(self.s4_count):
            s4_mod_deviation = random.uniform(self.s4_mod - 0.2, self.s4_mod + 0.2)
            damage, bleed_damage = self.calculate_damage(target, s4_mod_deviation)
            print(f"{damage} DMG")
            if bleed_damage > 0:
                target.cur_hp -= bleed_damage
                print(f"🩸 {target.name} took {bleed_damage} bleed DMG!")
            if random.random() < 0.2:
                self.heal(self, damage)

    def s5(self, ally_party, target):
        """Attacks an enemy thrice. If target is defeated, follows up with an Attack."""
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
        if target.cur_hp <= 0 and ally_party != []:
            self.s5_follow_up = True

dal_riata_pd_stats = []
insert_stat_by_id_num(pd_stats_column_list, 290, dal_riata_pd_stats)
dal_riata = DalRiata()