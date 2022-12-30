import pandas as pd
import numpy as np
#Import data
df = pd.read_csv("https://raw.githubusercontent.com/Jacob-McLaughlin/Jacob-McLaughlin.github.io/main/project/data/house_2020/house_2020_results_and_finances_final.csv")
#Create list of all districts in dataset
seat_list = df["Seat"].tolist()
#Creating dictionaries ensures that we don't have duplicated seats 
dict_raised = dict.fromkeys(seat_list)
dict_spent = dict_raised
vote_margins = []
#Amend dataframe so that the money values are integers
#Turn the values in the form "$1,000,000" into an integer such as "1000000"
#The if statement deals with the case where a candidate is listed as having raised/spent negative values 
df["Amount_Raised"] = df["Amount_Raised"].apply(lambda x: x[1:].replace(",","") if x[0] == "$" else x[2:].replace(",",""))
df["Amount_Raised"] = df["Amount_Raised"].astype("int")
df["Amount_Spent"] = df["Amount_Spent"].apply(lambda x: x[1:].replace(",","") if x[0] == "$" else x[2:].replace(",",""))
df["Amount_Spent"] = df["Amount_Spent"].astype("int")
#Find the sum for each seat and add to dictionaries 
for seat in dict_raised:
    seat_df = df[df["Seat"] == seat]
    dict_raised[seat] = seat_df["Amount_Raised"].sum()
    dict_spent[seat] = seat_df["Amount_Spent"].sum()
    vote_margins.append(round(max(seat_df["Percent_Votes"]) - min(seat_df["Percent_Votes"]),2))
#Create new dataframe with relevant data
final_df = pd.DataFrame(columns = ["Seat", "Total_Raised", "Total_Spent", "Margin"])
final_df["Seat"] = list(dict_raised.keys())
final_df["Total_Raised"] = list(dict_raised.values())
final_df["Total_Spent"] = list(dict_spent.values())
final_df["Margin"] = vote_margins
final_df.to_csv("district_totals_2020.csv")
