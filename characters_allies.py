import random
from combat import Character
from pd_parameter_stats import *

kiri_pd_stats = []
insert_stat_by_id_num(pd_stats_column_list, 0, kiri_pd_stats)

june_pd_stats = []
insert_stat_by_id_num(pd_stats_column_list, 1, june_pd_stats)

lachlan_pd_stats = []
insert_stat_by_id_num(pd_stats_column_list, 2, lachlan_pd_stats)

emily_pd_stats = []
insert_stat_by_id_num(pd_stats_column_list, 3, emily_pd_stats)

class Kiri(Character):
    def __init__(self):
        super().__init__(*kiri_pd_stats, 1)

    def action_choice(self, ally_party=None, enemy_party=None):
        if ally_party is None:
            ally_party = []
        if enemy_party is None:
            enemy_party = []
        action = input(f"{self.name}'s action? ").strip().lower()

        available_actions = {
            "na": lambda: self.attack_na(enemy_party[1]),
            "s1": lambda: self.s1(enemy_party[1])
        }
        if action in available_actions:
            available_actions[action]()

    def attack_na(self, target):
        """Attacks an enemy once.\n
        Spends Stella Polaris to inflict Bleed and Burn this turn."""
        super().attack_na(target)

    def s1(self, target):
        """Inspects an enemy.\n
        Spends Stella Polaris to daze the enemy;
        for 1 next turn, the enemy takes +15% damage from all direct attacks."""
        gaze_flavor_text_master = pandas.read_csv("gaze_flavor_text.csv")
        gaze_flavor_text = (gaze_flavor_text_master.loc[gaze_flavor_text_master["tag"] == target.tag, "flavor_text"]
        .values[0])
        print(f"Kiri gazed upon {target.name}!")
        print(f"- {target.name} - {target.atk} AT {target.df} DF")
        print(gaze_flavor_text)

class June(Character):
    def __init__(self):
        super().__init__(*june_pd_stats, 1)

    def action_choice(self, ally_party=None, enemy_party=None):
        if ally_party is None:
            ally_party = []
        if enemy_party is None:
            enemy_party = []
        action = input(f"{self.name}'s action? ").strip().lower()

        available_actions = {
            "na": lambda: self.attack_na(enemy_party[1]),
            "s1": lambda: self.s1(enemy_party[1])
        }
        if action in available_actions:
            available_actions[action]()

    def attack_na(self, target):
        """Attacks an enemy once."""
        super().attack_na(target)

    def s1(self, target):
        """Attacks an enemy thrice, inflicting Bleed this turn."""
        print(f"June used ✦Tearing✦ against {target.name}!")
        for turn in range(self.s1_count):
            damage, bleed_damage = self.attack(target, self.na_mod)
            print(f"{damage} DMG")
            if bleed_damage > 0:
                target.cur_hp -= bleed_damage
                print(f"🩸 {target.name} took {bleed_damage} bleed DMG!")
        target.is_bleeding += 1
        Character.do_bleed_damage(self, target)
        if target.is_bleeding > 0:
            print(f"{target.name} is bleeding!")

class Lachlan(Character):
    def __init__(self):
        super().__init__(*lachlan_pd_stats, 1)

    def action_choice(self, ally_party=None, enemy_party=None):
        if ally_party is None:
            ally_party = []
        if enemy_party is None:
            enemy_party = []
        action = input(f"{self.name}'s action? ").strip().lower()

        available_actions = {
            "na": lambda: self.attack_na(enemy_party[1]),
            "s1": lambda: self.s1(ally_party)
        }
        if action in available_actions:
            available_actions[action]()

    def attack_na(self, target):
        """Attacks an enemy twice, healing 10% HP if at least one attack connects."""
        super().attack_na(target)
        self.heal(self, 0.1 * self.max_hp)

    def s1(self, ally_party=None):
        """Heals an ally by 30% of Lachlan's Max HP."""
        if ally_party is None:
            ally_party = []
        heal_target = None
        heal_target_name = input("Who will Lachlan use ✦✦ on? ").strip().lower()
        for ally in ally_party:
            if heal_target_name == ally.name.strip().lower():
                heal_target = ally
                break
        if heal_target is not None:
            self.heal(heal_target, self.s1_mod * self.max_hp)
        else:
            pass

class Emily(Character):
    def __init__(self):
        super().__init__(*emily_pd_stats, 1)

    def action_choice(self, ally_party=None, enemy_party=None):
        if ally_party is None:
            ally_party = []
        if enemy_party is None:
            enemy_party = []
        action = input(f"{self.name}'s action? ").strip().lower()

        available_actions = {
            "na": lambda: self.attack_na(enemy_party[1]),
            "s1": lambda: self.s1(enemy_party)
        }
        if action in available_actions:
            available_actions[action]()

    def attack_na(self, target):
        """Attacks an enemy once, inflicting Burn this turn."""
        super().attack_na(target)
        target.is_burning += 1
        Character.do_burn_damage(self, target)

    def s1(self, enemy_list=None):
        """Attacks thrice at random, inflicting Burn this turn and 1 next turn."""
        if enemy_list is None:
            enemy_list = []
        print(f"Emily bombarded the battlefield with ✦✦!")
        for turn in range(self.s1_count):
            target = random.choice(enemy_list)
            damage, bleed_damage = self.attack(target, self.s1_mod)
            print(f"{target.name} was set on fire!\n{damage} DMG")
            if target.is_burning < 2:
                target.is_burning += 2
                Character.do_burn_damage(self, target)
            if bleed_damage > 0:
                target.cur_hp -= bleed_damage
                print(f"🩸 {target.name} took {bleed_damage} bleed DMG!")

kiri = Kiri()
june = June()
lachlan = Lachlan()
emily = Emily()
