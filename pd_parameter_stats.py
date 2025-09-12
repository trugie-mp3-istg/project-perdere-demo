import pandas

stats = pandas.read_csv("stats.csv")

# Identification number for all characters.
# Serves as metadata and does not influence combat.
id_num = stats.id_num

tag = stats.tag; name = stats.name; lv = stats.lv
hp = stats.hp; atk = stats.atk; df = stats.df; spd = stats.spd
direct_res = stats.direct_res; bleed_res = stats.bleed_res; burn_res = stats.burn_res
na_count = stats.na_count; na_mod = stats.na_mod
s1_count = stats.s1_count; s1_mod = stats.s1_mod
s2_count = stats.s2_count; s2_mod = stats.s2_mod
s3_count = stats.s3_count; s3_mod = stats.s3_mod
s4_count = stats.s4_count; s4_mod = stats.s4_mod
s5_count = stats.s5_count; s5_mod = stats.s5_mod
s6_count = stats.s6_count; s6_mod = stats.s6_mod

pd_stats_column_list = [id_num, tag, name, lv,
                        hp, atk, df, spd,
                        direct_res, bleed_res, burn_res,
                        na_count, na_mod,
                        s1_count, s1_mod,
                        s2_count, s2_mod,
                        s3_count, s3_mod,
                        s4_count, s4_mod, s5_count, s5_mod, s6_count, s6_mod]

def insert_stat_by_id_num(pd_stats_col_list, char_id_num, char_stats=None):
    """Automatically inserts a character's stats by their id_num.\n
    Previously all characters' stats are inserted manually by order, which gets tedious as
    more characters are added and more backtracking is needed.\n
    pd_stats_col_list is always pd_stats_column_list if you can't tell by the parameter name."""
    if char_stats is None:
        char_stats = []
    index = stats.index[stats["id_num"] == char_id_num][0]
    for each_stat in pd_stats_col_list:
        char_stats.append(each_stat[index])
    char_stats.pop(0) # Removing id_num from stat list.
    return char_stats

# An example use of the function above:
# dummy_stat = []
# insert_stat_by_id_num(pd_stats_column_list, {dummy's id_num}, dummy_stat)