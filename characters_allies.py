import random
from time import sleep
from combat import Character, burning_dictionary, calculate_mp_cost, ally_mp_gauge
# Despite gray-outs, ally_mp_gauge is used
from pd_parameter_stats import *

class Kiri(Character):
    def __init__(self):
        super().__init__(*kiri_pd_stats, 1, 1)
        self.polaris = False
        self.polaris_s2_shield_hp_detect_hit = 0
        self.amber_moth = 0

    def action_choice(self, ally_party, enemy_party):
        action = input(f"{self.name}'s action? [na/s1/s2/s3/df] ").strip().lower()

        available_actions = {
            "na": lambda: self.na(enemy_party),
            "s1": lambda: self.s1(enemy_party),
            "s2": lambda: self.s2(),
            "s3": lambda: self.s3(enemy_party),
            "df": lambda: self.defend()
        }
        action_cost = {
            "na": -1,
            "s1": 0,
            "s2": 2,
            "s3": 3,
            "df": -1
        }
        global ally_mp_gauge
        if action in available_actions and action_cost[action] <= ally_mp_gauge:
            available_actions[action]()
            ally_mp_gauge = calculate_mp_cost(action_cost[action])
        else:
            if action not in available_actions: print("(Invalid action!)")
            elif action_cost[action] > ally_mp_gauge: print("(Insufficient MP!)")
            self.action_choice(ally_party, enemy_party)

    def na(self, enemy_party):
        """Attacks an enemy once.\n
        Spends Stella Polaris to inflict Bleed and Burn this turn."""
        target = self.select_target_from_enemy_party(enemy_party)
        print(f"{self.name} attacked {target.name}!")
        self.func_attack(target, self.na_count, self.na_mod)

        # Stella Polaris' effect.
        if self.polaris:
            print("Kiri consumed Stella Polaris!")
            target.is_bleeding += 1
            Character.do_bleed_damage(self, target)
            if target.is_bleeding > 0: print(f"{target.name} is bleeding!")
            target.is_burning += 1
            Character.do_burn_damage(self, target)
            if target.is_burning > 0: print(f"{target.name} is burning!")
            self.polaris = False

    def s1(self, enemy_party):
        """Inspects an enemy.\n
        Spends Stella Polaris to daze the enemy;
        for 1 next turn, the enemy takes +15% damage from all direct attacks."""
        target = self.select_target_from_enemy_party(enemy_party)
        gaze_flavor_text_master = pandas.read_csv("gaze_flavor_text.csv")
        gaze_flavor_text = (gaze_flavor_text_master.loc[gaze_flavor_text_master["tag"] == target.tag, "flavor_text"]
        .values[0])
        print(f"Kiri gazed at {target.name}!")
        print(f"- {target.name} - {target.atk} AT {target.df} DF")
        print(gaze_flavor_text)

        # Stella Polaris' effect.
        if self.polaris:
            target.df_mod *= 0.7
            print("Kiri consumed Stella Polaris!")
            print(f"{target.name} was dazed and will take more damage!")
            self.polaris = False

    def s2(self):
        """Casts a shield and gains bonus Shield HP this turn and 1 next turn. Counts as a Defend this turn.\n
        Spends Stella Polaris to gain even more bonus Shield HP and perform 1 counter-Attack when hit."""
        super().defend()
        self.shield_duration = 2
        if self.polaris:    kiri_s2_mod = 0.3
        else:               kiri_s2_mod = 0.2
        shield_hp_add = int(self.max_hp * kiri_s2_mod)
        self.shield_hp = shield_hp_add
        print(f"Kiri activated his energy shield! Shield can take up to {shield_hp_add} DMG!")

        # Stella Polaris' effect.
        if self.polaris:
            if self.shield_duration > 0:
                self.polaris_s2_shield_hp_detect_hit = shield_hp_add

    def s2_counter(self, target):
        print("Kiri consumed Stella Polaris!")
        print(f"{self.name} counter-attacked {target.name}!")
        self.func_attack(target, self.na_count, self.na_mod)
        self.polaris_s2_shield_hp_detect_hit = 0
        self.polaris = False

    def s3(self, enemy_party):
        """Attacks an enemy twice. Kiri gains Stella Polaris."""
        target = self.select_target_from_enemy_party(enemy_party)
        print(f"{self.name} took aim at {target.name}!")
        self.func_attack(target, self.s3_count, self.s3_mod)
        if not self.polaris:
            self.polaris = True
            print("Kiri gained Stella Polaris!")

    def defend(self):
        super().defend()
        print(f"{self.name} guarded himself!")

kiri_pd_stats = []
insert_stat_by_id_num(pd_stats_column_list, 0, kiri_pd_stats)
kiri = Kiri()

class June(Character):
    def __init__(self):
        super().__init__(*june_pd_stats, 1, 1)
        self.red_dusk = 0
        self.red_dusk_s2_retreat = False
        self.amber_moth = 0

    def action_choice(self, ally_party, enemy_party):
        action = input(f"{self.name}'s action? [na/s1/s2/s3/df] ").strip().lower()

        available_actions = {
            "na": lambda: self.na(enemy_party),
            "s1": lambda: self.s1(enemy_party),
            "s2": lambda: self.s2(ally_party),
            "s3": lambda: self.s3(enemy_party),
            "df": lambda: self.defend()
        }
        action_cost = {
            "na": -1,
            "s1": 3,
            "s2": 3,
            "s3": 0,
            "df": -1
        }
        global ally_mp_gauge
        if action in available_actions and action_cost[action] <= ally_mp_gauge:
            available_actions[action]()
            ally_mp_gauge = calculate_mp_cost(action_cost[action])
        else:
            if action not in available_actions: print("(Invalid action!)")
            elif action_cost[action] > ally_mp_gauge: print("(Insufficient MP!)")
            self.action_choice(ally_party, enemy_party)

    def na(self, enemy_party):
        """Attacks an enemy once."""
        self.s2_update_mod()
        target = self.select_target_from_enemy_party(enemy_party)
        print(f"{self.name} attacked {target.name}!")
        self.func_attack(target, self.na_count, self.na_mod)

    def s1(self, enemy_party):
        """Attacks an enemy thrice, inflicting Bleed this turn."""
        self.s2_update_mod()
        target = self.select_target_from_enemy_party(enemy_party)
        print(f"June used ✦Relentless✦ against {target.name}!")
        self.func_attack(target, self.s1_count, self.s1_mod)
        target.is_bleeding += 1
        Character.do_bleed_damage(self, target)
        if target.is_bleeding > 0: print(f"{target.name} is bleeding!")

    def s2(self, ally_party):
        """LV1: Charges up. Attacks deal slightly more damage.\n
        LV2: Charges up. Attacks deal moderately more damage.\n
        LV3: Retreats this turn.
        Enemies cannot target June, nor can the party order June to act.
        Cannot charge up to LV3 if June is the only remaining ally."""

        self.red_dusk += 1
        self.s2_update_mod()
        if self.red_dusk == 1: print("June used ✦Heartless✦! ATK up!")
        if self.red_dusk == 2: print("June used ✦Heartless✦ again! ATK up even more!")
        if self.red_dusk == 3:
            if ally_party != [june]:
                print("June is retreating to prepare a powerful strike...")
                self.red_dusk_s2_retreat = True
            else:
                self.red_dusk = 2
                print("Cannot act, as June is the only party member left!")
        if self.red_dusk > 3:
            self.red_dusk = 3
            print("June has already retreated!")

    def s2_update_mod(self):
        if self.red_dusk == 0: self.na_mod = 0.8;   self.s1_mod = 0.6;  self.s3_mod = 0
        if self.red_dusk == 1: self.na_mod = 0.9;   self.s1_mod = 0.75; self.s3_mod = 0
        if self.red_dusk == 2: self.na_mod = 1;     self.s1_mod = 1;    self.s3_mod = 0
        if self.red_dusk == 3: self.na_mod = 1;     self.s1_mod = 1;    self.s3_mod = 6

    def s3(self, enemy_party):
        """Only usable with Skill 2's LV3 effect active. Automatically activates.\n
        Attacks the enemy with the highest HP once, dealing massive damage and ignoring enemy's defense.
        On use, resets Skill 2's charges to LV0."""
        if self.red_dusk != 3: print("June has yet found the right opportunity to strike!")
        else:
            # Select target.
            max_hp_find = []
            for enemy in enemy_party: max_hp_find.append(enemy.cur_hp)
            max_hp_found = max(max_hp_find)
            for enemy in enemy_party:
                if enemy.cur_hp == max_hp_found:
                    target = enemy; break
            print("..."); sleep(0.5); print("...!"); sleep(0.5)
            print(f"June used ✦Endless Red✦ and is charging at {target.name} with immense speed...!"); sleep(0.5)
            for count in range(self.s3_count):
                damage, bleed_damage = self.calculate_true_damage(target, self.s3_mod)
                print(f"{damage} DMG")
                if bleed_damage > 0:
                    target.cur_hp -= bleed_damage
                    print(f"🩸 {target.name} took {bleed_damage} bleed DMG!")
            self.red_dusk = 0
            self.s2_update_mod()
            self.red_dusk_s2_retreat = False
            print("June lost ATK up!")

    def defend(self):
        super().defend()
        print(f"{self.name} guarded herself!")

june_pd_stats = []
insert_stat_by_id_num(pd_stats_column_list, 1, june_pd_stats)
june = June()

class Lachlan(Character):
    def __init__(self):
        super().__init__(*lachlan_pd_stats, 1, 1)
        self.teal_blade = 0
        self.amber_moth = 0

    def action_choice(self, ally_party, enemy_party):
        action = input(f"{self.name}'s action? [na/s1/s2/s3/df] ").strip().lower()

        available_actions = {
            "na": lambda: self.na(enemy_party),
            "s1": lambda: self.s1(ally_party),
            "s2": lambda: self.s2(),
            "s3": lambda: self.s3(ally_party),
            "df": lambda: self.defend()
        }
        action_cost = {
            "na": -1,
            "s1": 3,
            "s2": 2,
            "s3": 7,
            "df": -1
        }
        global ally_mp_gauge
        if action in available_actions and action_cost[action] <= ally_mp_gauge:
            available_actions[action]()
            ally_mp_gauge = calculate_mp_cost(action_cost[action])
        else:
            if action not in available_actions: print("(Invalid action!)")
            elif action_cost[action] > ally_mp_gauge: print("(Insufficient MP!)")
            self.action_choice(ally_party, enemy_party)

    def na(self, enemy_party):
        """Attacks an enemy twice, healing 10% HP if at least one attack connects."""
        self.s2_update_mod()
        target = self.select_target_from_enemy_party(enemy_party)
        print(f"{self.name} attacked {target.name}!")
        self.func_attack(target, self.na_count, self.na_mod)
        self.heal(self, 0.05 * self.max_hp)

    def s1(self, ally_party):
        """Heals an ally by 30% of Lachlan's Max HP."""
        heal_target = None
        heal_target_name = input("Who will Lachlan use ✦Maritime Mist✦ on? ").strip().lower()
        for ally in ally_party:
            if heal_target_name == ally.name.strip().lower():
                heal_target = ally; break
        if heal_target is not None:
            self.s2_update_mod()
            self.heal(heal_target, self.s1_mod * self.max_hp)
        else: pass

    def s2(self):
        """For 3 turns starting this turn, inflicts Bleed onto self.
        While this effect lasts, enhances Attack in exchange for -50% healing efficiency."""
        if self.is_bleeding < 3: self.is_bleeding = 3
        Character.do_bleed_damage(self, self)
        self.teal_blade = 3
        self.s2_update_mod()
        print("Lachlan used ✦Riptide✦! Healing down! His Attack was enhanced!")

    def s2_update_mod(self):
        if self.teal_blade == 0:    self.na_count = 2; self.na_mod = 0.5; self.heal_multi = 1
        else:                       self.na_count = 3; self.na_mod = 0.6; self.heal_multi = 0.5

    def s3(self, ally_party):
        """Heals all allies by 50% of Lachlan's Max HP."""
        print("Lachlan cast ✦Ex Undis✦!")
        self.s2_update_mod()
        for ally in ally_party: self.heal(ally, self.s3_mod * self.max_hp)

    def defend(self):
        super().defend()
        print(f"{self.name} guarded himself!")

lachlan_pd_stats = []
insert_stat_by_id_num(pd_stats_column_list, 2, lachlan_pd_stats)
lachlan = Lachlan()

class Emily(Character):
    def __init__(self):
        super().__init__(*emily_pd_stats, 1, 1)
        self.amber_moth = 0

    def action_choice(self, ally_party, enemy_party):
        action = input(f"{self.name}'s action? [na/s1/s2/s3/df] ").strip().lower()

        available_actions = {
            "na": lambda: self.na(enemy_party),
            "s1": lambda: self.s1(enemy_party),
            "s2": lambda: self.s2(ally_party),
            "s3": lambda: self.s3(enemy_party),
            "df": lambda: self.defend()
        }
        action_cost = {
            "na": -1,
            "s1": 3,
            "s2": 2,
            "s3": 7,
            "df": -1
        }
        global ally_mp_gauge
        if action in available_actions and action_cost[action] <= ally_mp_gauge:
            available_actions[action]()
            ally_mp_gauge = calculate_mp_cost(action_cost[action])
        else:
            if action not in available_actions: print("(Invalid action!)")
            elif action_cost[action] > ally_mp_gauge: print("(Insufficient MP!)")
            self.action_choice(ally_party, enemy_party)

    def na(self, enemy_party):
        """Attacks an enemy once, inflicting Burn this turn."""
        target = self.select_target_from_enemy_party(enemy_party)
        print(f"{self.name} attacked {target.name}!")
        self.func_attack(target, self.na_count, self.na_mod)
        target.is_burning += 1
        Character.do_burn_damage(self, target)
        if target.is_burning > 0: print(f"{target.name} is burning!")

    def s1(self, enemy_party):
        """Attacks thrice at random, inflicting Burn this turn and 1 next turn."""
        print(f"Emily used ✦Improv Act✦!")
        for count in range(self.s1_count):
            target = random.choice(enemy_party)
            print(f"{target.name} got hit!")
            self.func_attack(target, 1, self.s1_mod)
            if target.is_burning < 2:
                target.is_burning += 2
                Character.do_burn_damage(self, target)
                print(f"{target.name} is burning!")

    def s2(self, ally_party):
        """Selects an ally to cheer, removing all negative status effects from said ally.
        Said ally deals +30% damage with direct attacks 1 next turn.\n
        Heals 15 HP if Emily cheers herself."""
        cheer_target = None
        cheer_target_name = input("Who will Emily use ✦Rehearsal✦ on? ").strip().lower()
        for ally in ally_party:
            if cheer_target_name == ally.name.strip().lower():
                cheer_target = ally; break
        if cheer_target is not None:
            if cheer_target.is_bleeding > 0:
                cheer_target.is_bleeding = 0
                if cheer_target == self: print("Emily cured herself of bleeding!")
                else: print(f"Emily cured {cheer_target.name} of bleeding!")
            if cheer_target.is_burning > 0:
                cheer_target.is_burning = 0
                if cheer_target in burning_dictionary: del burning_dictionary[cheer_target]
                if cheer_target == self: print("Emily absorbed her burning!")
                else: print(f"Emily cured {cheer_target.name} of burning!")
            if cheer_target.is_poisoned > 0:
                cheer_target.is_poisoned = 0
                if cheer_target == self: print("Emily cured herself of poison!")
                else: print(f"Emily cured {cheer_target.name} of poison!")
            if cheer_target.is_blind > 0:
                cheer_target.is_blind = 0
                if cheer_target == self: print("Emily cured herself of blindness!")
                else: print(f"Emily cured {cheer_target.name} of blindness!")
            if cheer_target.is_furious > 0:
                cheer_target.is_furious = 0
                if cheer_target == self: print("Emily calmed down!")
                else: print(f"Emily calmed {cheer_target.name} down!")
            if cheer_target == self:
                self.heal(self, 15)
            cheer_target.amber_moth = 2
            print(f"{cheer_target.name} felt encouraged! ATK up next turn!")
        else: pass

    def s3(self, enemy_party):
        """Attacks all enemies once, inflicting Burn this turn and healing 10 HP per hit.
        This skill deals more damage depending on Burn on enemies."""
        print("Emily used ✦Curtain Call✦ and bombarded the battlefield!")
        for target in enemy_party:
            original_dmg_multi = self.dmg_multi
            self.dmg_multi *= 1 + (target.is_burning / 10)
            self.func_attack(target, self.s3_count, self.s3_mod)
            target.is_burning += 1
            Character.do_burn_damage(self, target)
            if target.is_burning > 0:
                print(f"{target.name} is burning!")
                self.heal(self, 10)
            self.dmg_multi = original_dmg_multi

    def defend(self):
        super().defend()
        print(f"{self.name} guarded herself!")

emily_pd_stats = []
insert_stat_by_id_num(pd_stats_column_list, 3, emily_pd_stats)
emily = Emily()