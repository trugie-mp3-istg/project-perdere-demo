import random; from time import sleep
from combat import Character
from pd_parameter_stats import *

# For skills that don't appear outside each boss' respective battle, paste the comment below:
# Exclusive skill, doesn't actually appear outside scripted battles

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

    def s2(self, ally_party):   # Exclusive skill, doesn't actually appear outside scripted battles
        """Attacks an enemy once. If defended against, deals no damage.
        Else, inflicts Bleed this turn and follows up with 1 Attack."""
        target = random.choice(ally_party)
        if not target.is_defending:
            print(f"{self.name} dug her knife deep into {target.name}!")
            self.func_attack(target, self.s2_count, self.s2_mod + 0.5)
            target.is_bleeding += 1
            Character.do_bleed_damage(self, target)
            if target.is_bleeding > 0: print(f"{target.name} is bleeding!")
            sleep(0.5)
            print(f"{self.name} took an opportunity to attack {target.name}!")
            self.func_attack(target, self.na_count, self.na_mod)
            sleep(0.5)
            print(f"{self.name} became invigorated! DF up!")
            self.df += 10
        else:
            print(f"{self.name} tried to stab {target.name}...")
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
        self.red_dusk = 0

    def enemy_action_random_choice(self, ally_party, enemy_party):
        available_actions_no_red_dusk = [0]
        available_actions_red_dusk = [2]
        if self.red_dusk >= 7: available_actions = available_actions_red_dusk
        else: available_actions = available_actions_no_red_dusk
        choice = random.choice(available_actions)
        if choice == 0: self.na(ally_party); self.red_dusk += 1
        if choice == 2: self.s2(ally_party); self.red_dusk = 0

    def na(self, ally_party):
        """Attacks an enemy twice or thrice."""
        target = random.choice(ally_party)
        random_count_mod_list = [[self.na_count, self.na_mod],
                                 [self.s1_count, self.s1_mod]]
        random_count_mod = random.choice(random_count_mod_list)
        print(f"{self.name} attacked {target.name}!")
        self.func_attack(target, *random_count_mod)

    def s2(self, ally_party):
        """Attacks an enemy once, dealing massive damage and ignoring defense."""
        target = random.choice(ally_party)
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

    def s2(self, ally_party):   # Exclusive skill, doesn't actually appear outside scripted battles
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

    def s4(self, ally_party):   # Exclusive skill, doesn't actually appear outside scripted battles
        """Attacks each enemy once in turn. If defended against, deals less damage.
        If an enemy raises a heavy Shield, halts attacking and becomes stunned next turn."""
        for target in ally_party:
            print(f"{self.name} is ramming into {target.name}'s direction!")
            if target.shield_block <= 1:
                if not target.is_defending: self.func_attack(target, self.s4_count, self.s4_mod)
                else: self.func_attack(target, self.s4_count, self.s4_mod / 2)
            else:
                print(f"... and crashed into {target.name}'s shield!")
                self.func_attack(target, self.s4_count, self.s4_mod / 2)
                target.shield_hp = 0; target.shield_block = 0
                self.is_stunned = 2
                print(f"{target.name}'s shield broke! {self.name} is stunned for 1 next turn!")
                break
abno_wolf_pd_stats = []
insert_stat_by_id_num(pd_stats_column_list, 901, abno_wolf_pd_stats)
abno_wolf = AbnoWolf()

class Pollux(Character):
    def __init__(self):
        super().__init__(*pollux_pd_stats)
        self.babel_office = True

    def enemy_action_random_choice(self, ally_party, enemy_party):
        available_actions = [0, 0, 0, 1, 2]
        choice = random.choice(available_actions)
        if choice == 0: self.na(ally_party, enemy_party)
        if choice == 1:
            anyone_need_healing = False
            for enemy in enemy_party:
                if enemy.cur_hp < 0.8 * enemy.max_hp:
                    anyone_need_healing = True; break
            if anyone_need_healing: self.s1(ally_party, enemy_party)
            else: self.na(ally_party, enemy_party)
        if choice == 2: self.s2(enemy_party)

    def na(self, ally_party, enemy_party):
        """Attacks an enemy once. Heals all allies 5 HP."""
        target = random.choice(ally_party)
        print(f"{self.name} casted ✦Rising Spear✦ at {target.name}'s location!")
        self.func_attack(target, self.na_count, self.na_mod)
        for enemy in enemy_party:
            self.heal(enemy, 5)

    def s1(self, ally_party, enemy_party):
        """Heals 20 HP and other allies by 10 HP. If HP is at 80% or lower after healing, orders Castor to Attack."""
        print(f"{self.name} casted ✦Savior✦!")
        for enemy in enemy_party:
            if enemy == self: self.heal(enemy, self.s1_mod)
            else: self.heal(enemy, self.s1_mod / 2)
        if self.cur_hp <= 0.9 * self.max_hp and castor in enemy_party:
            print(f"{self.name} ordered {castor.name} to attack!")
            castor.na(ally_party)

    def s2(self, enemy_party):
        """Casts a shield around all allies, defending from 1 attack. If an ally's HP is at 30% or less, shield defends
        from 2 attacks instead."""
        print(f"{self.name} casted ✦Half-life✦! All enemies gained Shield!")
        for enemy in enemy_party:
            if enemy.shield_block < 1:
                enemy.shield_block += 1
                if enemy.cur_hp <= 0.3 * enemy.max_hp: enemy.shield_block += 1
pollux_pd_stats = []
insert_stat_by_id_num(pd_stats_column_list, 211, pollux_pd_stats)
pollux = Pollux()

class Castor(Character):
    def __init__(self):
        super().__init__(*castor_pd_stats)
        self.babel_office = True

    def enemy_action_random_choice(self, ally_party, enemy_party):
        available_actions = [0, 0, 1, 2]
        choice = random.choice(available_actions)
        if choice == 0: self.na(ally_party)
        if choice == 1: self.s1(ally_party, enemy_party)
        if choice == 2: self.s2(ally_party, enemy_party)

    def na(self, ally_party):
        """Attacks an enemy thrice. If HP is at 30% or lower, weakens attack."""
        target = random.choice(ally_party)
        if self.cur_hp > 0.3 * self.max_hp:
            print(f"{self.name} struck {target.name}!")
            self.func_attack(target, self.na_count, self.na_mod)
        else:
            print(f"{self.name} weakly struck {target.name}!")
            self.func_attack(target, self.na_count, self.na_mod - 0.2)

    def s1(self, ally_party, enemy_party):
        """Attacks an enemy twice. If HP is at 50% or lower after attacking, orders Pollux to Attack."""
        target = random.choice(ally_party)
        print(f"{self.name} used ✦Shipwreck✦ and struck {target.name}!")
        self.func_attack(target, self.s1_count, self.s1_mod)
        if self.cur_hp <= 0.5 * self.max_hp and pollux in enemy_party:
            print(f"{self.name} ordered {pollux.name} to attack!")
            pollux.na(ally_party, enemy_party)

    def s2(self, ally_party, enemy_party):
        """Attacks up to 3 enemies twice and heals all allies by 15 HP.
        If HP is at 50% or lower, weakens attack and healing effect."""
        print(f"{self.name} used ✦Bon Voyage✦!")
        non_repeating_target_list = []
        for x in range(min(len(ally_party), 3)):
            nr_target = random.choice(ally_party)
            if nr_target not in non_repeating_target_list: non_repeating_target_list.append(nr_target)
        for target in non_repeating_target_list:
            print(f"{target.name} was swept away!")
            if self.cur_hp > 0.5 * self.max_hp: self.func_attack(target, self.s2_count, self.s2_mod)
            else: self.func_attack(target, self.s2_count, self.s2_mod - 0.2)
        if self.cur_hp > 0.5 * self.max_hp:
            for enemy in enemy_party: self.heal(enemy, 15)
        else:
            for enemy in enemy_party: self.heal(enemy, 5)
castor_pd_stats = []
insert_stat_by_id_num(pd_stats_column_list, 212, castor_pd_stats)
castor = Castor()

class LachlanMboss(Character):
    def __init__(self):
        super().__init__(*lachlan_mboss_pd_stats)
        self.teal_blade = 0
        self.almost_disarmed = 0
        self.disarmed = False
        self.disarmed_retrieving_sabers = 0

    # For Lachlan's scripted midboss battle, he doesn't actually use the action roulette. This is here solely for
    # testing purposes.
    def enemy_action_random_choice(self, ally_party, enemy_party):
        available_actions_sword = [0, 0, 0, 1, 1]
        available_actions_fist = [2]
        available_actions_fist_ulti = [3]
        available_action_sword_ulti = [4]
        if not self.disarmed:
            if self.teal_blade < 10: available_actions = available_actions_sword
            else: available_actions = available_action_sword_ulti
        else:
            if self.disarmed_retrieving_sabers < 3: available_actions = available_actions_fist
            else: available_actions = available_actions_fist_ulti
        choice = random.choice(available_actions)
        if choice == 0: self.na(ally_party); self.teal_blade += 1
        if choice == 1: self.s1(ally_party); self.teal_blade += 1
        if choice == 2: self.s2(ally_party); self.disarmed_retrieving_sabers += 1
        if choice == 3: self.s3(ally_party); self.disarmed_retrieving_sabers = 0
        if choice == 4: self.s4(ally_party); self.teal_blade = 0

    def na(self, ally_party):
        """Attacks an enemy twice, healing 15 HP."""
        target = random.choice(ally_party)
        print(f"{self.name} struck {target.name}!")
        self.func_attack(target, self.na_count, self.na_mod)
        self.heal(self, 15)

    def s1(self, ally_party):
        """Attacks an enemy once. If the enemy raises a Shield, deals no damage.
        Else, deals 5 fixed damage twice and heals 20 HP."""
        target = random.choice(ally_party)
        print(f"{self.name} and {target.name} clashed!")
        if target.shield_block <= 0:
            print(f"{target.name} lost the clash!")
            self.func_attack(target, self.s1_count, self.s1_mod)
            self.do_fixed_damage(target, 2, 5)
            self.heal(self, 20)
            self.teal_blade += 1
        else:
            print(f"{target.name} deflected {self.name}'s blades!")
            self.almost_disarmed += 1
            if self.almost_disarmed == 2:
                print(f"{target.name} sent {self.name}'s blades flying!")
                self.disarmed = True
                self.almost_disarmed = 0

    def s2(self, ally_party):
        """Attacks an enemy once. If the enemy raises a Shield, deals 5 fixed damage."""
        target = random.choice(ally_party)
        print(f"{self.name} punched {target.name}!")
        self.func_attack(target, self.s2_count, self.s2_mod)
        if target.shield_block > 0:
            self.do_fixed_damage(target, 1, 5)

    def s3(self, ally_party):
        """Attacks an enemy once. If the enemy raises a heavy Shield, damages and stuns self. Else, stuns target."""
        target = random.choice(ally_party)
        print(f"{self.name} activated his gauntlet booster and punched {target.name}!")
        if target.shield_block <= 1:
            self.func_attack(target, self.s3_count, self.s3_mod)
            target.is_stunned = 2
            print(f"{target.name} was stunned from the impact!")
            self.disarmed = False
        else:
            print(f"... But {target.name} deflected the attack!")
            self.is_stunned = 2
            print(f"{self.name} took recoil damage!")
            self.func_attack(self, self.s3_count, self.s3_mod)
            print(f"{self.name} was stunned from the recoil!")
        target.shield_block = 0

    def s4(self, ally_party):
        """Attacks an enemy four times. If HP is at 80% or more, consumes 20% HP to deal significantly more damage."""
        if self.cur_hp >= 0.8 * self.max_hp: s3_buff = True
        else: s3_buff = False
        target = random.choice(ally_party)
        if s3_buff:
            self.cur_hp -= 0.2 * self.max_hp
            print(f"{self.name} cast ✦Raging Riptide✦! {self.name} took 180 DMG!")
        print(f"{self.name} used ✦Teal Blade of Fate✦ and took a flash step toward {target.name}...!")
        if s3_buff: self.func_attack(target, self.s4_count, self.s4_mod + 0.5)
        else: self.func_attack(target, self.s4_count, self.s4_mod)
lachlan_mboss_pd_stats = []
insert_stat_by_id_num(pd_stats_column_list, 222, lachlan_mboss_pd_stats)
lachlan_mboss = LachlanMboss()

class DalRiata(Character):
    def __init__(self):
        super().__init__(*dal_riata_pd_stats)
        self.s5_ready = 0
        self.s5_follow_up = False

    def enemy_action_random_choice(self, ally_party, enemy_party):
        available_actions_no_s5 = [0, 1, 2, 3, 4]
        available_actions_s5 = [5]
        if self.s5_ready >= 9: available_actions = available_actions_s5
        else: available_actions = available_actions_no_s5
        choice = random.choice(available_actions)
        if choice == 0: self.na(ally_party); self.s5_ready += 1
        if choice == 1: self.s1(ally_party); self.s5_ready += 1
        if choice == 2: self.s2(ally_party); self.s5_ready += 1
        if choice == 3: self.s3(ally_party); self.s5_ready += 1
        if choice == 4: self.s4(ally_party); self.s5_ready += 1
        if choice == 5: self.s5(ally_party); self.s5_ready = 0

    def na(self, ally_party):
        """Attacks an enemy twice."""
        target = random.choice(ally_party)
        print(f"{self.name} attacked {target.name}!")
        self.func_attack(target, self.na_count, self.na_mod)

    def s1(self, ally_party):
        """Attacks up to 3 enemies once. Has a chance of inflicting Bleed this turn and 1 next turn."""
        non_repeating_target_list = []
        for x in range(min(len(ally_party), 3)):
            nr_target = random.choice(ally_party)
            if nr_target not in non_repeating_target_list: non_repeating_target_list.append(nr_target)
        print(f"{self.name} used ✦Azure Gale✦!")

        # If the attack targets more enemies, the less chance they are inflicted with Bleed. Default value: 0.33
        bleed_chance = 0.33
        if len(non_repeating_target_list) == 3: bleed_chance = 0.2
        elif len(non_repeating_target_list) == 2: bleed_chance = 0.33
        elif len(non_repeating_target_list) == 1: bleed_chance = 0.5

        for target in non_repeating_target_list:
            print(f"{target.name} was swept up in the attack!")
            self.func_attack(target, self.s1_count, self.s1_mod)
            if random.random() < bleed_chance:
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
            if target.shield_block > 0: display_damage = False
            else: display_damage = True
            damage, bleed_damage = self.calculate_damage(target, self.s4_mod + random.uniform(-0.2, 0.2))
            if display_damage:
                print(f"{damage} DMG")
            if bleed_damage > 0:
                if target.shield_block > 0:
                    target.shield_block -= 1
                    print(f"🩸 {target.name}'s shield absorbed Bleed damage!")
                else:
                    target.cur_hp -= bleed_damage
                    print(f"🩸 {target.name} took {bleed_damage} bleed DMG!")
            if self.cur_hp <= 0.5 * self.max_hp: heal_chance = 0.45
            else: heal_chance = 0.3
            if random.random() < heal_chance:
                self.heal(self, damage * 2)
            if self.is_poisoned > 0: self.do_poison_damage()
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

    def s5_cutscene(self, ally_party, target):   # Exclusive skill, doesn't actually appear outside scripted battles
        # To see the version Dullahan uses in test battles, see s5 below.
        """Attacks an enemy thrice and heals 100 HP. If defended against, deals less damage.
        If target is defeated, heals another 200 HP and follows up with 2 Attacks at random enemies."""
        if target not in ally_party:
            target = random.choice(ally_party)
        print(f"Dullahan used ✦Azure Blade of Fate✦ and charged at {target.name} with a deathly grin...!")
        for count in range(self.s5_count):
            sleep(0.5)
            if target.shield_block > 0: display_damage = False
            else: display_damage = True
            if not target.is_defending: damage, bleed_damage = self.calculate_damage(target, self.s5_mod)
            else: damage, bleed_damage = self.calculate_damage(target, self.s5_mod - 0.3)
            if display_damage: print(f"{damage} DMG")
            if bleed_damage > 0:
                if target.shield_block > 0:
                    target.shield_block -= 1
                    print(f"🩸 {target.name}'s shield absorbed Bleed damage!")
                else:
                    target.cur_hp -= bleed_damage
                    print(f"🩸 {target.name} took {bleed_damage} bleed DMG!")
            if self.is_poisoned > 0: self.do_poison_damage()
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
        self.heal(self, 100)
        if target.cur_hp <= 0 and ally_party != []:
            self.s5_follow_up = True

    def s5(self, ally_party):
        """Attacks an enemy thrice and heals 100 HP. If defended against, deals less damage.
        If target is defeated, heals another 200 HP and follows up with 2 Attacks at random enemies."""
        target = random.choice(ally_party)
        print(f"Dullahan used ✦Azure Blade of Fate✦ and charged at {target.name} with a deathly grin...!")
        for count in range(self.s5_count):
            sleep(0.5)
            if target.shield_block > 0: display_damage = False
            else: display_damage = True
            if not target.is_defending: damage, bleed_damage = self.calculate_damage(target, self.s5_mod)
            else: damage, bleed_damage = self.calculate_damage(target, self.s5_mod - 0.3)
            if display_damage: print(f"{damage} DMG")
            if bleed_damage > 0:
                if target.shield_block > 0:
                    target.shield_block -= 1
                    print(f"🩸 {target.name}'s shield absorbed Bleed damage!")
                else:
                    target.cur_hp -= bleed_damage
                    print(f"🩸 {target.name} took {bleed_damage} bleed DMG!")
            if self.is_poisoned > 0: self.do_poison_damage()
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
        self.heal(self, 100)
        if target.cur_hp <= 0 and ally_party != []:
            self.s5_follow_up = True
            print("Dullahan is on a streak of bloodlust!"); sleep(0.5); dal_riata.heal(dal_riata, 200)
            for i in range(2):
                dal_riata.na(ally_party)
            dal_riata.s5_follow_up = False
dal_riata_pd_stats = []
insert_stat_by_id_num(pd_stats_column_list, 290, dal_riata_pd_stats)
dal_riata = DalRiata()