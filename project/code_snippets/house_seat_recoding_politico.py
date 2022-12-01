import numpy as np
import pandas as pd
house_finances_2020 = pd.read_csv("https://raw.githubusercontent.com/Jacob-McLaughlin/Jacob-McLaughlin.github.io/main/project/data/2020_house_finances_open_secrets.csv")
house_results_2020 = pd.read_csv("https://raw.githubusercontent.com/Jacob-McLaughlin/Jacob-McLaughlin.github.io/main/project/data/politico_2020_house.csv")
#We first want to ensure that the names of the house seats are the same across both dataframes
#So we want to rename e.g. "Alabama_district_1" to "AL01" 
states_dataframe = pd.read_csv("https://raw.githubusercontent.com/Jacob-McLaughlin/Jacob-McLaughlin.github.io/main/project/data/US_state_list.csv")
states_list = states_dataframe["State"].tolist()
house_code_list = []
for i in range(len(house_results_2020)):
  #Take the actual name of the state 
  seat = house_results_2020.loc[i][0]
  state = seat.split("_")[0]
  state_index = states_list.index(state)
  state_code = states_dataframe.loc[state_index][1]
  #Take the number of the seat
  seat_number = seat.split("_")[2]
  #Add a 0 to the number if it is a single digit
  if len(seat_number) == 1: 
    seat_number = "0" + seat_number
  seat_code = state_code + seat_number
  house_code_list.append(seat_code)
#Replace the old seat format values with the updated seat format values 
house_results_2020["Seat"] = house_code_list
#Download the file with renamed house seats
house_results_2020.to_csv("politico_results_2020_recoded.csv")
