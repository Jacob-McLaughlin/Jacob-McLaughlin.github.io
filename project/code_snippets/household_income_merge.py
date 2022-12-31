import numpy as np
import pandas as pd
#This code merges census data showing household income per district
#And our dataset showing how much was spent on each district in 2020
#Load data from GitHub
total_df = pd.read_csv("https://raw.githubusercontent.com/Jacob-McLaughlin/Jacob-McLaughlin.github.io/main/project/data/house_2020/district_totals_2020.csv")
census_df = pd.read_csv("https://raw.githubusercontent.com/Jacob-McLaughlin/Jacob-McLaughlin.github.io/main/project/data/house_2020/census_household_income_2019.csv")
states_df = pd.read_csv("https://raw.githubusercontent.com/Jacob-McLaughlin/Jacob-McLaughlin.github.io/main/project/data/US_state_list.csv")
states_list = states_df["State"].tolist()
codes_list = states_df["state_po"].tolist()
states_dict = dict(zip(states_list, codes_list))
seat_codes = []
seat_incomes = []
#Iterate over the entries
for i in range(len(census_df)):
    seat_incomes.append(census_df.iloc[i][1])
    #We need to account for states with two-word names
    words = census_df.iloc[i][0].split(" ")
    #Ensure we only have relevant states (only PR and DC have more than 8 words)
    if len(words) < 9:
        #Account for states with only one district
        #As these have "at large" rather than a number
        #And consider whether states have two-word names or one-word names 
        if "(at" in words and len(words) == 8:
            state = words[6] + "-" + words[7]
            district_num = "01"
        elif "(at" in words and len(words) == 7:
            state = words[6]
            district_num = "01"
        #We still need to account for states with two-word names 
        elif len(words) == 7:
            state = words[5] + "-" + words[6]
            district_num = words[2]
        elif len(words) == 6:
            state = words[5]
            district_num = words[2]
    if len(district_num) == 1:
        district_num = "0" + district_num
    state_code = states_dict[state]
    seat_codes.append(state_code + district_num)
incomes_dict = dict(zip(seat_codes, seat_incomes))
#We now need to find the seats for which we had requisite data for votes/finances
relevant_incomes = []
for district in total_df["Seat"].tolist():
    relevant_incomes.append(incomes_dict[district])
#Add column of incomes to dataframe and write to csv 
total_df["Median_Household_Income"] = relevant_incomes
total_df.to_csv("district_totals_household_income_2020.csv")
            
