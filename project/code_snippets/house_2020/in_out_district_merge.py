import numpy as np
import pandas as pd
in_out_df = pd.read_csv("https://raw.githubusercontent.com/Jacob-McLaughlin/Jacob-McLaughlin.github.io/main/project/data/house_2020/house_2020_in_out_district_open_secrets.csv")
results_finances_df = pd.read_csv("https://raw.githubusercontent.com/Jacob-McLaughlin/Jacob-McLaughlin.github.io/main/project/data/house_2020/house_2020_results_and_finances_final.csv")
#Our in-district dataset has many more values than our other dataset
#And we are restricted to the dataset with fewer values
in_out_candidates = in_out_df["Name"].tolist()
results_candidates = results_finances_df["Candidate"].tolist()
#We need to account for situations where there are two different people with the same name
#We do this by adding the seat number to the name 
for i,v in enumerate(in_out_candidates):
    #Remove the party name (e.g. (R)) in name to get in same format
    short_name = v.rsplit(" ",1)[0] + " "
    seat_code = in_out_df.iloc[i][1][-2:]
    in_out_candidates[i] = short_name + seat_code
#in_out_df["Name"] = in_out_candidates
final_df = pd.DataFrame()
#Create new dataframe with combined data from both sets for candidates where we have all relevant data
for i,v in enumerate(results_candidates):
    #Check that the candidate appears in both datasets 
    name_with_code = v + results_finances_df.iloc[i][0][2:]
    if name_with_code in in_out_candidates:
        #Find the relevant data 
        in_index = in_out_candidates.index(name_with_code)
        in_percentage = in_out_df.iloc[in_index][2][:-1]
        seat = results_finances_df.iloc[i][0]
        candidate = results_finances_df.iloc[i][1]
        amount_raised = results_finances_df.iloc[i][3]
        votes_percent = results_finances_df.iloc[i][7]
        winner = results_finances_df.iloc[i][9]
        incumbent = results_finances_df.iloc[i][10]
        in_raised = round(int(amount_raised.replace(",","").replace("$",""))*float(in_percentage)/100*(10**(-3)),2)
        row = pd.DataFrame([{'Seat': seat, 'Candidate': candidate, 'Raised': amount_raised, 'In_Distr_Perc': in_percentage, 'In_Distr_Raised_000': in_raised,
                             'Vote_Share': votes_percent,'Winner': winner, 'Incumbent': incumbent}])
        final_df = pd.concat([final_df, row])
final_df = final_df.set_index(np.arange(len(final_df)))
#We want to drop values where we only have data for one candidate in a seat as we cannot consider the proportion raised
#Otherwise we want to find the total spent for each seat so we can find how much each individual raised relative to their opponents
seat_list = final_df["Seat"].tolist()
dict_total= dict.fromkeys(seat_list)
for seat in seat_list:
    seat_df = final_df[final_df["Seat"] == seat]
    #Drop values where we have data for only one candidate
    if len(seat_df) < 2:
        seat_index = final_df.index[final_df["Seat"] == seat]
        final_df = final_df.drop(seat_index)
    else:
        dict_total[seat] = round(seat_df['In_Distr_Raised_000'].sum(),2)
#Now calculate the proportion of money raised in-district compared to their opponent
in_distr_proportions = []
for i,v in enumerate(final_df["Candidate"].tolist()):
    seat = final_df.iloc[i][0]
    candidate_in_raised = final_df.iloc[i][4]
    in_distr_proportions.append(round((candidate_in_raised/dict_total[seat])*100,2))
final_df["In_Distr_Prop_Versus_Opponent"] = in_distr_proportions
final_df.to_csv("in_distr_raised_2020.csv")
