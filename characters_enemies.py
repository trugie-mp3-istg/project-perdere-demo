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
        print(f"{self.name} attacked {target.name}!")
        self.func_attack(target, self.na_count, self.na_mod)
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
        """Attacks an enemy twice."""
        target = random.choice(ally_party)
        print(f"{self.name} attacked {target.name}!")
        self.func_attack(target, self.na_count, self.na_mod)
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
        super().__init__(*sanc_fixer_0_pd_stats)

    def enemy_action_random_choice(self, ally_party, enemy_party):
        available_actions = [0, 1]
        choice = random.choice(available_actions)
        if choice == 0: self.na(ally_party)
        if choice == 1: self.s1(ally_party)

    def na(self, ally_party):
        """Attacks an enemy once. Has a chance to heal 3 HP."""
        target = random.choice(ally_party)
        print(f"{self.name} attacked {target.name}!")
        self.func_attack(target, self.na_count, self.na_mod)
        if random.random() < 0.4:
            self.heal(self, 3)

    def s1(self, ally_party):
        """Attacks an enemy twice. Has a chance to deal an extra 3 damage."""
        target = random.choice(ally_party)
        print(f"{self.name} attacked {target.name}!")
        self.func_attack(target, self.s1_count, self.s1_mod)
        if random.random() < 0.5:
            self.do_fixed_damage(target, 1, 3)
sanc_fixer_0_pd_stats = []
insert_stat_by_id_num(pd_stats_column_list, 200, sanc_fixer_0_pd_stats)
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
        print(f"{self.name} slammed {target.name} from above with its hammer!")
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
        print(f"{self.name} zapped {target.name}!")
        self.func_attack(target, self.na_count, self.na_mod)

    def s1(self, ally_party, enemy_party):
        """Attacks an enemy thrice. Heals by damage dealt.
        Has a chance to share healing to a random ally."""
        target = random.choice(ally_party)
        print(f"{self.name} electrocuted {target.name}!")
        for count in range(self.s1_count):
            if target.shield_block > 0: display_damage = False
            else: display_damage = True
            damage, bleed_damage = self.calculate_damage(target, self.s1_mod)
            if display_damage: print(f"{damage} DMG")
            if bleed_damage > 0:
                if target.shield_block > 0:
                    target.shield_block -= 1
                    print(f"🩸 {target.name}'s shield absorbed Bleed damage!")
                else:
                    target.cur_hp -= bleed_damage
                    print(f"🩸 {target.name} took {bleed_damage} bleed DMG!")
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
            self.heal(self, damage)
            if random.random() < 0.25:
                heal_choice = [x for x in enemy_party if x != self] # It doesn't heal itself.
                if heal_choice != []: self.heal(random.choice(heal_choice), damage)
sanc_guard_b_pd_stats = []
insert_stat_by_id_num(pd_stats_column_list, 202, sanc_guard_b_pd_stats)
sanc_guard_b = SancGuardB()

class SancBabelFixer(Character):
    def __init__(self):
        super().__init__(*sanc_babel_fixer_pd_stats)
        self.babel_office = True
        self.s2_ready = 0
        self.babel_s3_followup = True

    def enemy_action_random_choice(self, ally_party, enemy_party):
        available_actions = [0, 1]
        if self.s2_ready >= 2: available_actions.append(2)
        else:
            if len(available_actions) == 3: available_actions.pop()
        choice = random.choice(available_actions)
        if choice == 0: self.na(ally_party); self.s2_ready += 1
        if choice == 1: self.s1(ally_party); self.s2_ready += 1
        if choice == 2: self.s2(ally_party, enemy_party); self.s2_ready = 0

    def na(self, ally_party):
        """Attacks an enemy twice. If this attack triggers Bleed, deal an extra 3 damage."""
        target = random.choice(ally_party)
        print(f"{self.name} attacked {target.name}!")
        self.func_attack(target, self.na_count, self.na_mod)
        if target.is_bleeding > 0:
            self.do_fixed_damage(target, 1, 3)

    def s1(self, ally_party):
        """Attacks an enemy once. Has a chance to inflict any of the following:
        Bleed this turn and 1 next turn, Burn this turn, or Poison next turn."""
        target = random.choice(ally_party)
        print(f"{self.name} attacked {target.name}!")
        self.func_attack(target, self.s1_count, self.s1_mod)
        if random.random() < 0.5:
            effect_random = [1, 2, 3]
            effect_choice = random.choice(effect_random)
            if effect_choice == 1:
                if target.is_bleeding < 2: target.is_bleeding = 2
                Character.do_bleed_damage(self, target)
                if target.is_bleeding > 0: print(f"{target.name} is bleeding!")
            elif effect_choice == 2:
                if target.is_burning < 1: target.is_burning += 1
                Character.do_burn_damage(self, target)
                if target.is_burning > 0: print(f"{target.name} is burning!")
            elif effect_choice == 3:
                if target.is_poisoned <= 2: target.is_poisoned = 2
                print(f"{target.name} is poisoned!")

    def s2(self, ally_party, enemy_party):
        """Attacks an enemy twice. If there is at least 1 other Babel Fixer in the team, attack an additional time."""
        target = random.choice(ally_party)
        s2_count_bonus = -1
        for enemy in enemy_party:
            if hasattr(enemy, "babel_office"):
                s2_count_bonus += 1
                if s2_count_bonus > 1: s2_count_bonus = 1
        print(f"{self.name} imbued their weapon with a bright light and attacked {target.name}!")
        self.func_attack(target, self.s2_count + s2_count_bonus, self.s2_mod)

        """Attacks an enemy once in a coordinated attack when another Babel Fixer ally uses Skill 3 on said enemy."""
        babel_fixer_ally = [x for x in enemy_party
                            if x != self and hasattr(x, "babel_s3_followup")]
        if babel_fixer_ally != []:
            for enemy in babel_fixer_ally:
                print(f"{enemy.name} followed up with an attack at {target.name}!")
                enemy.func_attack(target, enemy.s3_count, enemy.s3_mod)
sanc_babel_fixer_pd_stats = []
insert_stat_by_id_num(pd_stats_column_list, 203, sanc_babel_fixer_pd_stats)
sanc_babel_fixer_1 = SancBabelFixer()
sanc_babel_fixer_2 = SancBabelFixer()
sanc_babel_fixer_3 = SancBabelFixer()

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