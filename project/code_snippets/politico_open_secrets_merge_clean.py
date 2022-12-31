import numpy as np
import pandas as pd
finances_df = pd.read_csv("https://raw.githubusercontent.com/Jacob-McLaughlin/Jacob-McLaughlin.github.io/main/project/data/house_2020/house_finances_2020_open_secrets.csv")
results_df = pd.read_csv("https://raw.githubusercontent.com/Jacob-McLaughlin/Jacob-McLaughlin.github.io/main/project/data/house_2020/politico_2020_house.csv")
#This code snippet cleans and combines the results data from Politico
#And the finances data from OpenSecrets
#First, we ensure that the house seats are in the same format
#So for the Politico Data to rename e.g. "Alabama_district_1" to "AL01"
#We use some data showing each state and their relevant postal code 
states_dataframe = pd.read_csv("https://raw.githubusercontent.com/Jacob-McLaughlin/Jacob-McLaughlin.github.io/main/project/data/US_state_list.csv")
states_list = states_dataframe["State"].tolist()
house_code_list = []
for i in range(len(results_df)):
  #Take the actual name of the state 
  seat = results_df.loc[i][0]
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
results_df["Seat"] = house_code_list


#We now want to merge the two datasets
results_candidates = results_df["Candidate"].tolist()
finances_candidates = finances_df["Candidate"].tolist()
used_results_indices = []
used_finances_indices = []
combined_df = pd.DataFrame()
#Iterate over both lists
for i in range(len(results_candidates)):
    for j in range(len(finances_candidates)):
        #If the candidates appear to be the same (i.e. the surname is in the full name) then check they are the same candidate (same seat and party)
        if results_candidates[i] in finances_candidates[j] and results_df.loc[i][0] == finances_df.loc[j][1] and results_df.loc[i][2] == finances_df.loc[j][3]:
            #Create new combined dataset with relevant data from both datasets
            code = finances_df.loc[j][1]
            name = finances_candidates[j]
            party = finances_df.loc[j][3]
            amount_raised = finances_df.loc[j][4]
            amount_spent = finances_df.loc[j][5]
            winner = finances_df.loc[j][6]
            incumbent = finances_df.loc[j][7]
            percent = results_df.loc[i][4]
            votes = results_df.loc[i][5]
            row = pd.DataFrame([{'Seat': code, 'Candidate': name, 'Party': party, 'Raised': amount_raised, 'Spent': amount_spent, 'Percent': percent, 'Votes': votes, 'Winner': winner, 'Incumbent': incumbent}])
            combined_df = pd.concat([combined_df, row])
combined_df = combined_df.set_index(np.arange(len(combined_df)))

#We now want to drop trivial data, i.e. data-points where we have only one candidate per seat
#Then either the candidate ran unopposed or we have nothing to compare their spending to
#We first want to iterate over the seats and make sure they occur twice
seats = combined_df["Seat"].tolist()
non_trivial_seats = []
#Create list of seats where we have at least two candidates standing 
for seat in seats:
    if seats.count(seat) != 1 and seat not in non_trivial_seats:
        non_trivial_seats.append(seat)
#Calculate the total spent on each seat
seat_raised = []
seat_spent = []
for seat in non_trivial_seats:
    #Find first index of seat
    index_1 = seats.index(seat)
    number_candidates = seats.count(seat)
    raised = 0
    spent = 0
    for i in range(number_candidates):
        raised += int(combined_df.loc[i+index_1][3].replace("$","").replace(",",""))
        spent += int(combined_df.loc[i+index_1][4].replace("$","").replace(",",""))
    seat_raised.append(raised)
    seat_spent.append(spent)
#Iterate over our dataset and check that the seat is not trivial and we have relevant spending/voting data
final_df = pd.DataFrame()
for i in range(len(combined_df)):
    seat = combined_df.loc[i][0]
    votes = combined_df.loc[i][6]
    #Check there are at least two candidates in the seat and the candidate received non-zero votes
    if seat in non_trivial_seats and votes != 0:
        index_seat = non_trivial_seats.index(seat)
        raised_total = seat_raised[index_seat]
        spent_total = seat_spent[index_seat]
        candidate = combined_df.loc[i][1]
        party = combined_df.loc[i][2]
        raised = combined_df.loc[i][3]
        spent = combined_df.loc[i][4]
        percent = combined_df.loc[i][5]
        winner = combined_df.loc[i][7]
        incumbent = combined_df.loc[i][8]
        raised_numerical = int(raised.replace("$","").replace(",",""))
        spent_numerical = int(spent.replace("$","").replace(",",""))
        raised_percent = (100*raised_numerical)/raised_total
        spent_percent = (100*spent_numerical)/spent_total
        row = pd.DataFrame([{'Seat': seat, 'Candidate': candidate, 'Party': party, 'Amount_Raised': raised, 'Percent_Raised': raised_percent,
                             'Amount_Spent': spent, 'Percent_Spent': spent_percent, 'Percent_Votes': percent, 'Votes': votes, 'Winner': winner, 'Incumbent': incumbent}])
        final_df = pd.concat([final_df, row])
final_df.to_csv("house_2020_results_and_finances_final.csv")
