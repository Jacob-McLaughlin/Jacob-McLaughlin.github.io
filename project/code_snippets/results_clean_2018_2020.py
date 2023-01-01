import pandas as pd
import numpy as np
#This code snippet takes results (in number form) for 2018 and 2020 House Elections
#And produces a file which gives the winner of each seat in those years 
#Load the data
df = pd.read_csv("https://raw.githubusercontent.com/Jacob-McLaughlin/Jacob-McLaughlin.github.io/main/project/data/2018_2020_house_results.csv")
#Create two new dataframes for the separate 2018 and 2020 data
#The following variables are Booleans which can be used to filter the data
is_2018 = df["year"] == 2018
is_2020 = df["year"] == 2020
df_2018 = df[is_2018]
df_2020 = df[is_2020]
#We now want to find the winner of each seat (in each year)
#Create list of seat
seat_list = df["seat"]
#Turn list into dictionary to remove duplicates (then turn back into list)
seat_list = list(dict.fromkeys(seat_list))
dict_2018 = dict.fromkeys(seat_list)
dict_2020 = dict.fromkeys(seat_list)
#We then iterate over our dataframes to find the winner in each seat
#First for 2018
for seat in seat_list:
    seat_df = df_2018[df_2018["seat"] == seat]
    if len(seat_df) > 0:
        winner_index = seat_df["candidatevotes"].tolist().index(max(seat_df["candidatevotes"]))
        winner_party = seat_df.iloc[winner_index][3]
        dict_2018[seat] = winner_party[0]
#Then for 2020
for seat in seat_list:
    seat_df = df_2020[df_2020["seat"] == seat]
    if len(seat_df) > 0:
        winner_index = seat_df["candidatevotes"].tolist().index(max(seat_df["candidatevotes"]))
        winner_party = seat_df.iloc[winner_index][3]
        dict_2020[seat] = winner_party[0]
#Then combine into a single dataframe and write to csv
final_df = pd.DataFrame.from_dict(dict_2018, orient="index", columns = ["winner_2018"])
final_df["winner_2020"] = list(dict_2020.values())
final_df.to_csv("house_winners_2018_2020.csv")
