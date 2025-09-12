import random
from combat import Character
from pd_parameter_stats import *

class Dummy(Character):
    def __init__(self):
        super().__init__(*dummy_pd_stats)

    def enemy_action_random_choice(self, ally_party, enemy_party):
        available_actions = [0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 5, 6]
        choice = random.choice(available_actions)
        if choice == 0: self.na(ally_party)
        elif choice == 1: self.s1(ally_party)
        elif choice == 2: self.s2(ally_party)
        elif choice == 3: self.s3(ally_party)
        elif choice == 4: self.s4(ally_party)
        elif choice == 5: self.s5(ally_party)
        elif choice == 6: self.s6(ally_party)

    def na(self, ally_party):
        """Barely attacks an enemy once."""
        target = random.choice(ally_party)
        print(f"{self.name} bounced back at {target.name}!")
        self.func_attack(target, self.na_count, self.na_mod)
        self.heal(self, 5)

    def s1(self, ally_party):
        """Barely attacks an enemy once, inflicting Bleed this turn and 1 next turn."""
        target = random.choice(ally_party)
        print(f"{self.name} poked {target.name} with a sewing needle!")
        self.func_attack(target, self.s1_count, self.s1_mod)
        if target.is_bleeding < 2: target.is_bleeding = 2
        Character.do_bleed_damage(self, target)
        if target.is_bleeding > 0: print(f"{target.name} is bleeding!")

    def s2(self, ally_party):
        """Barely attacks an enemy twice, inflicting Burn this turn and 1 next turn."""
        target = random.choice(ally_party)
        print(f"{self.name} poked {target.name} with a lit match!")
        self.func_attack(target, self.s2_count, self.s2_mod)
        if target.is_burning < 2: target.is_burning += 2
        Character.do_burn_damage(self, target)
        if target.is_burning > 0: print(f"{target.name} is burning!")

    def s3(self, ally_party):
        """Barely attacks an enemy thrice, inflicting Poison this turn and 1 next turn."""
        target = random.choice(ally_party)
        print(f"{self.name} sprayed expired perfume at {target.name}!")
        self.func_attack(target, self.s3_count, self.s3_mod)
        if target.is_poisoned <= 2: target.is_poisoned = 2
        print(f"{target.name} is poisoned!")

    def s4(self, ally_party):
        """Barely attacks an enemy once. Has a chance to inflict Blind 1 next turn."""
        target = random.choice(ally_party)
        print(f"{self.name} tear-gassed {target.name}!")
        self.func_attack(target, self.s4_count, self.s4_mod)
        if random.random() < 0.5:
            if target.is_blind <= 2: target.is_blind = 2
            print(f"{target.name} is blinded!")

    def s5(self, ally_party):
        """Barely attacks an enemy twice. Has a chance to inflict Furious 1 next turn."""
        target = random.choice(ally_party)
        print(f"{self.name} taunted {target.name}!")
        self.func_attack(target, self.s5_count, self.s5_mod)
        if random.random() < 0.5:
            if target.is_furious <= 2: target.is_furious = 2
            print(f"{target.name} is furious!")

    def s6(self, ally_party):
        """Barely attacks an enemy twice. Has a chance to inflict Furious 1 next turn."""
        target = random.choice(ally_party)
        print(f"{self.name} smacked {target.name} with a pillow!")
        self.func_attack(target, self.s6_count, self.s6_mod)
        if random.random() < 0.5:
            if target.is_stunned <= 2: target.is_stunned = 2
            print(f"{target.name} is stunned!")
dummy_pd_stats = []
insert_stat_by_id_num(pd_stats_column_list, 9, dummy_pd_stats)
dummy = Dummy()

class PerdGoon1(Character):
    def __init__(self):
        super().__init__(*perd_goon_1_pd_stats)

    def enemy_action_random_choice(self, ally_party, enemy_party):
        available_actions = [0]
        choice = random.choice(available_actions)
        if choice == 0: self.na(ally_party)

    def na(self, ally_party):
        """Attacks an enemy once."""
        target = random.choice(ally_party)
        random_count_mod_list = [[self.na_count, self.na_mod],
                                 [self.s1_count, self.s1_mod]]
        random_count_mod = random.choice(random_count_mod_list)
        print(f"{self.name} attacked {target.name}!")
        self.func_attack(target, *random_count_mod)
perd_goon_1_pd_stats = []
insert_stat_by_id_num(pd_stats_column_list, 100, perd_goon_1_pd_stats)
perd_goon_1_1 = PerdGoon1()
perd_goon_1_2 = PerdGoon1()

class PerdGoon2(Character):
    def __init__(self):
        super().__init__(*perd_goon_2_pd_stats)

    def enemy_action_random_choice(self, ally_party, enemy_party):
        available_actions = [0]
        choice = random.choice(available_actions)
        if choice == 0: self.na(ally_party)

    def na(self, ally_party):
        """Attacks an enemy once or twice."""
        target = random.choice(ally_party)
        random_count_mod_list = [[self.na_count, self.na_mod],
                                 [self.s1_count, self.s1_mod]]
        random_count_mod = random.choice(random_count_mod_list)
        print(f"{self.name} attacked {target.name}!")
        self.func_attack(target, *random_count_mod)
perd_goon_2_pd_stats = []
insert_stat_by_id_num(pd_stats_column_list, 101, perd_goon_2_pd_stats)
perd_goon_2_1 = PerdGoon2()
perd_goon_2_2 = PerdGoon2()

class PerdHunter(Character):
    def __init__(self):
        super().__init__(*perd_hunter_pd_stats)

    def enemy_action_random_choice(self, ally_party, enemy_party):
        available_actions = [0, 0, 1]
        choice = random.choice(available_actions)
        if choice == 0: self.na(ally_party)
        if choice == 1: self.s1(ally_party)

    def na(self, ally_party):
        """Attacks an enemy twice. Has a chance to miss."""
        target = random.choice(ally_party)
        print(f"{self.name} fired two bolts from their crossbow at {target.name}!")
        if random.random() < 0.33:
            self.func_attack(target, self.na_count - 1, self.na_mod)
            print(f"{self.name} missed one shot!")
        else: self.func_attack(target, self.na_count, self.na_mod)

    def s1(self, ally_party):
        """Attacks an enemy thrice. Has a chance to miss. May inflict Bleed this turn."""
        target = random.choice(ally_party)
        print(f"{self.name} fired three bolts from their crossbow at {target.name}!")
        if random.random() < 0.33:
            self.func_attack(target, self.s1_count - 1, self.s1_mod)
            print(f"{self.name} missed one shot!")
        else: self.func_attack(target, self.s1_count, self.s1_mod)
        if random.random() < 0.25:
            target.is_bleeding += 1
            Character.do_bleed_damage(self, target)
            if target.is_bleeding > 0: print(f"{target.name} is bleeding!")
perd_hunter_pd_stats = []
insert_stat_by_id_num(pd_stats_column_list, 102, perd_hunter_pd_stats)
perd_hunter_1 = PerdHunter()
perd_hunter_2 = PerdHunter()

class SancFixer0(Character):
    def __init__(self):
        super().__init__(*sanc_fixer_pd_stats)

    def enemy_action_random_choice(self, ally_party, enemy_party):
        available_actions = [0, 1]
        choice = random.choice(available_actions)
        if choice == 0: self.na(ally_party)
        if choice == 1: self.s1(ally_party)

    def na(self, ally_party):
        """Attacks an enemy once."""
        target = random.choice(ally_party)
        print(f"{self.name} attacked {target.name}!")
        self.func_attack(target, self.na_count, self.na_mod)

    def s1(self, ally_party):
        """Attacks an enemy twice. Has a chance to inflict Bleed this turn and 1 next turn."""
        target = random.choice(ally_party)
        print(f"{self.name} attacked {target.name}!")
        self.func_attack(target, self.s1_count, self.s1_mod)
        if random.random() < 0.5:
            if target.is_bleeding < 2: target.is_bleeding = 2
            Character.do_bleed_damage(self, target)
            if target.is_bleeding > 0: print(f"{target.name} is bleeding!")
sanc_fixer_pd_stats = []
insert_stat_by_id_num(pd_stats_column_list, 200, sanc_fixer_pd_stats)
sanc_fixer_0_1 = SancFixer0()
sanc_fixer_0_2 = SancFixer0()
sanc_fixer_0_3 = SancFixer0()

class SancGuardA(Character):
    def __init__(self):
        super().__init__(*sanc_guard_a_pd_stats)

    def enemy_action_random_choice(self, ally_party, enemy_party):
        available_actions = [0, 0, 1]
        choice = random.choice(available_actions)
        if choice == 0: self.na(ally_party)
        if choice == 1: self.s1(ally_party)

    def na(self, ally_party):
        """Attacks an enemy once."""
        target = random.choice(ally_party)
        print(f"{self.name} attacked {target.name}!")
        self.func_attack(target, self.na_count, self.na_mod)

    def s1(self, ally_party):
        """Attacks an enemy once. Has a chance to inflict Stun. Becomes Stunned next turn."""
        target = random.choice(ally_party)
        print(f"{self.name} attacked {target.name} with its hammer!")
        self.func_attack(target, self.s1_count, self.s1_mod)
        if random.random() < 0.5:
            if target.is_stunned < 2: target.is_stunned = 2
            print(f"{target.name} was stunned from the impact!")
        self.is_stunned = 2
        print(f"{self.name} is temporarily paralyzed!")
sanc_guard_a_pd_stats = []
insert_stat_by_id_num(pd_stats_column_list, 201, sanc_guard_a_pd_stats)
sanc_guard_a = SancGuardA()

class SancGuardB(Character):
    def __init__(self):
        super().__init__(*sanc_guard_b_pd_stats)

    def enemy_action_random_choice(self, ally_party, enemy_party):
        available_actions = [0, 0, 1]
        choice = random.choice(available_actions)
        if choice == 0: self.na(ally_party)
        if choice == 1: self.s1(ally_party, enemy_party)

    def na(self, ally_party):
        """Attacks an enemy twice."""
        target = random.choice(ally_party)
        print(f"{self.name} attacked {target.name}!")
        self.func_attack(target, self.na_count, self.na_mod)

    def s1(self, ally_party, enemy_party):
        """Attacks an enemy thrice. Heals by damage dealt and inflicts Bleed this turn and 1 next turn.
        Has a chance to share healing to a random ally."""
        target = random.choice(ally_party)
        print(f"{self.name} attacked {target.name} with its drill!")
        for count in range(self.s1_count):
            damage, bleed_damage = self.calculate_damage(target, self.s1_mod)
            print(f"{damage} DMG")
            if bleed_damage > 0:
                target.cur_hp -= bleed_damage
                print(f"🩸 {target.name} took {bleed_damage} bleed DMG!")
            self.heal(self, damage)
            if random.random() < 0.25:
                heal_choice = [x for x in enemy_party if x != self] # It doesn't heal itself.
                self.heal(random.choice(heal_choice), damage)
sanc_guard_b_pd_stats = []
insert_stat_by_id_num(pd_stats_column_list, 202, sanc_guard_b_pd_stats)
sanc_guard_b = SancGuardB()

class Marcy(Character):
    def __init__(self):
        super().__init__(*marcy_pd_stats)

    def enemy_action_random_choice(self, ally_party, enemy_party):
        available_actions = [0, 1]
        choice = random.choice(available_actions)
        if choice == 0: self.na(ally_party)
        if choice == 1: self.s1(ally_party)

    def na(self, ally_party):
        """..."""
        target = random.choice(ally_party)
        print("The wind blew gently through the endless pasture.")
        random_count_mod_list = [[self.na_count, self.na_mod],
                                 [self.s1_count, self.s1_mod]]
        random_count_mod = random.choice(random_count_mod_list)
        self.func_attack(target, *random_count_mod)

    def s1(self, ally_party):
        """..."""
        target = random.choice(ally_party)
        print("The sun shone brightly through her cloud-white hair.")
        for count in range(self.s2_count):
            self.heal(target, self.s2_mod)
marcy_pd_stats = []
insert_stat_by_id_num(pd_stats_column_list, 744, marcy_pd_stats)
marcy = Marcy()