import csv
import pandas as pd

stat_dict = {
    # "keepers": "keeper",
    # "keepersadv": "keeper_adv", 
    "passing_types": "passing_types", 
    "passing": "passing", 
    "shooting": "shooting", 
    "gca": "gca", 
    "defense": "defense", 
    "possession": "possession", 
    # "playingtime": "playingtime", 
    # "misc": "misc",
}

league_choice_dict = {
    "1": "Premier-League",
    "2": "Bundesliga",
    "3": "Serie-A",
    "4": "Ligue-1",
    "5": "La-Liga",
    "6": "Championship",
    "7": "Belgian Pro-League",
    "8": "Eredivisie",
}

# Sending HTTP Request to Obtain FPL Data
MIN_TACKLES = 10
MIN_TAKEONS = 30
season_default = "2025-2026"
league_choice = input(f"Hi! Which league would you like to analyse?\nPlease pick from the following: \n{league_choice_dict} ")
# stat_choice = input(f"Hi! Which stat would you like to analyse?\nPlease pick from the following: \n{stat_dict.keys()}")

# FOOTBALL_DF = pd.read_csv(f"C:\\Users\\kinso\\Documents\\SUTD\\Term 5\\Football Data\\{season_default}_{league_choice}_possession.csv")
# print(FOOTBALL_DF)

FOOTBALL_DF = pd.read_csv(f"C:\\Users\\kinso\\Documents\\SUTD\\Term 5\\Football Data\\{season_default}_{league_choice_dict[league_choice]}_passing_types.csv")
collated_cols_list = [FOOTBALL_DF["Rk"], FOOTBALL_DF["Player"], FOOTBALL_DF["Pos"]]

for stat in stat_dict.keys():
    FOOTBALL_DF = pd.read_csv(f"C:\\Users\\kinso\\Documents\\SUTD\\Term 5\\Football Data\\{season_default}_{league_choice_dict[league_choice]}_{stat}.csv")
    if stat == "passing_types":
        pass
    elif stat == "passing":
        xAG = FOOTBALL_DF["xAG"]
        xA = FOOTBALL_DF["xA"]
        KP = FOOTBALL_DF["KP"]
        collated_cols_list.extend([xAG, xA, KP])
    elif stat == "shooting":
        goals = FOOTBALL_DF["Gls"]
        shots = FOOTBALL_DF["Sh"]
        shots_on_target = FOOTBALL_DF["SoT"]
        xG = FOOTBALL_DF["xG"]
        npxG = FOOTBALL_DF["npxG"]
        clinicality = FOOTBALL_DF["G-xG"]
        dist = FOOTBALL_DF["Dist"]
        collated_cols_list.extend([goals, shots, shots_on_target, xG, npxG, clinicality, dist])
    elif stat == "gca":
        sca = FOOTBALL_DF["SCA"]
        gca = FOOTBALL_DF["GCA"]
        def_actions_to_attack = FOOTBALL_DF["Def.1"]
        collated_cols_list.extend([sca, gca, def_actions_to_attack])
    elif stat == "defense":
        tackles_won = FOOTBALL_DF[FOOTBALL_DF["Tkl"] > MIN_TACKLES]["Tkl%"]
        tackle_interceptions = FOOTBALL_DF["Tkl+Int"]
        clearances = FOOTBALL_DF["Clr"]
        err = FOOTBALL_DF["Err"]
        tackles_def_3rd = FOOTBALL_DF["Def 3rd"]
        tackles_mid_3rd = FOOTBALL_DF["Mid 3rd"]
        tackles_opp_3rd = FOOTBALL_DF["Att 3rd"]
        collated_cols_list.extend([tackles_won, tackle_interceptions, clearances, err, tackles_def_3rd, tackles_mid_3rd, tackles_opp_3rd])
    elif stat == "possession":
        carries = FOOTBALL_DF["Carries"]
        succ_takeons = FOOTBALL_DF[FOOTBALL_DF["Att"] > MIN_TAKEONS]["Succ"]
        touches_in_opp_pen = FOOTBALL_DF["Att Pen"]
        carries_into_18_yard_box = FOOTBALL_DF["CPA"]
        progessive_carries = FOOTBALL_DF["PrgC"]
        progressive_carries_dist = FOOTBALL_DF["PrgDist"]
        collated_cols_list.extend([carries, succ_takeons, touches_in_opp_pen, carries_into_18_yard_box, progessive_carries, progressive_carries_dist])
    else:
        raise SystemError

reformatted_df = pd.DataFrame(collated_cols_list).transpose()
print(reformatted_df.columns)

stat_choice_dict = {}

for num in range(3, len(reformatted_df.columns)):
    stat_choice_dict[str(num - 2)] = reformatted_df.columns[num]

# print(stat_choice_dict)

stat_num_choice = input(f"What statistic would you like to find? \n{stat_choice_dict}\n ")
chosen_stat = stat_choice_dict[stat_num_choice]
top_or_bottom = input(f"Would you like to see the best or worst players for {chosen_stat}?\nB/W (B-Best, W-Worst) ").upper()
top = True if top_or_bottom == "W" else False
top_num = int(input(f"You would like to see the top __ players for this statistic. e.g. 20\n "))

print(reformatted_df[["Rk", "Player", "Pos", chosen_stat]].sort_values(by=chosen_stat, ascending=top)[:top_num])