from selenium import webdriver
from selenium.webdriver.common.by import By

import csv, time

season = "2025-2026"
stat_dict = {
    "keepers": "keeper",
    "keepersadv": "keeper_adv", 
    "passing_types": "passing_types", 
    "passing": "passing", 
    "shooting": "shooting", 
    "gca": "gca", 
    "defense": "defense", 
    "possession": "possession", 
    # "playingtime": "playingtime", 
    # "misc": "misc",
}
league_dict = {
    "Premier-League": 9,
    "Bundesliga": 20,
    "Serie-A": 11,
    "Ligue-1": 13,
    "La-Liga": 12,
    "Championship": 10,
    "Belgian Pro-League": 37,
    "Eredivisie": 23,
}

start_time = time.time()
time_dict = {

}
for stat in stat_dict.keys():
    time_dict[stat] = {

    }
    for league in league_dict.keys():
        driver = webdriver.Chrome()
        url = f"https://fbref.com/en/comps/{league_dict[league]}/{stat}/{league}-Stats"
        # Past Seasons
        # url = f"https://fbref.com/en/comps/{league_dict[league]}/{season}/{stat}/{season}-{league}-Stats"        
        print(url)
        driver.get(url)
        driver.implicitly_wait(30)
        data_table = driver.find_element(By.ID, f"stats_{stat_dict[stat]}")
        print(data_table.text)
        rows = data_table.find_elements(By.TAG_NAME, "tr")
        print(rows, len(rows))
        # input()
        with open(f"C:\\Users\\kinso\\Documents\\SUTD\\Term 5\\Football Data\\{season}_{league}_{stat}.csv", mode="w", encoding="utf-8", newline="") as f:
            writer=csv.writer(f)
            row_list = []
            print(len(rows))
            for i, row in enumerate(rows):
                if i == 1 or (i - 1) % 26 != 0:
                    print("START")
                    print(row.text)
                    # input()
                    # print("\n")
                    col_list = []
                    cols = row.find_elements(By.XPATH, ".//td | .//th")
                    print(cols)
                    for col in cols:
                        if col != cols[-1]:
                            col_part = col.text
                            print(col_part)
                            col_list.append(col_part)
                            print("END")
            #             input()
                    print(col_list)
                    row_list.append(col_list)
                    print("ACTUAL END")
            row_list.pop(0)
            writer.writerows(row_list)
        time_now = time.time()
        driver.quit()
        time.sleep(10)
        time_dict[stat][league] = start_time - time_now
print(time_dict)