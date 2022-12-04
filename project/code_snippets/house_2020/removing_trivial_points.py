import pandas as pd
import numpy as np
#This code snippet drops trivial data, i.e. data-points where we have only one candidate per seat
#Then either the candidate ran unopposed or we have nothing to compare their spending to
combined_df = pd.read_csv("https://raw.githubusercontent.com/Jacob-McLaughlin/Jacob-McLaughlin.github.io/main/project/data/house_2020/house_2020_finances_results.csv")
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
