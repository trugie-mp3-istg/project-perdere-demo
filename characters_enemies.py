import random
from combat import Character
from pd_parameter_stats import *

dal_riata_pd_stats = []
insert_stat_by_id_num(pd_stats_column_list, 290, dal_riata_pd_stats)

class Dummy(Character):
    def __init__(self):
        super().__init__(tag[4], name[4], lv[4], max_hp[4], cur_hp[4], atk[4], df[4], spd[4],
                         direct_res[4], 0, bleed_res[4], 0, burn_res[4],
                         na_count[4], na_mod[4],
                         s1_count[4], s1_mod[4],
                         1)

class Goon(Character):
    def __init__(self):
        super().__init__(tag[5], name[5], lv[5], max_hp[5], cur_hp[5], atk[5], df[5], spd[5],
                         direct_res[5], 0, bleed_res[5], 0, burn_res[5],
                         na_count[5], na_mod[5],
                         s1_count[5], s1_mod[5],
                         1)

class Goon2(Character):
    def __init__(self):
        super().__init__(tag[6], name[6], lv[6], max_hp[6], cur_hp[6], atk[6], df[6], spd[6],
                         direct_res[6], 0, bleed_res[6], 0, burn_res[6],
                         na_count[6], na_mod[6],
                         s1_count[6], s1_mod[6],
                         1)

class DalRiata(Character):
    def __init__(self):
        super().__init__(*dal_riata_pd_stats,1)

dummy = Dummy()
goon = Goon()
goon2 = Goon2()
dal_riata = DalRiata()