import numpy as np
import pandas as pd
#This code snippet combines both the dataset showing the results of the 2020 House Elections and the dataset showing their finances
#Ensuring that the candidate's names are in the same format, and removing data points where we don't have both results and finances data
results_df = pd.read_csv("https://raw.githubusercontent.com/Jacob-McLaughlin/Jacob-McLaughlin.github.io/main/project/data/house_2020/politico_results_2020_recoded.csv")
finances_df = pd.read_csv("https://raw.githubusercontent.com/Jacob-McLaughlin/Jacob-McLaughlin.github.io/main/project/data/house_2020/2020_house_finances_open_secrets.csv")
#Create lists of candidate names for each dataset
results_candidates = results_df["Candidate"].tolist()
finances_candidates = finances_df["Candidate"].tolist()
used_results_indices = []
used_finances_indices = []
combined_df = pd.DataFrame()
#Iterate over both lists
for i in range(len(results_candidates)):
    for j in range(len(finances_candidates)):
        #If the candidates appear to be the same (i.e. the surname is in the full name) then check they are the same candidate (same seat and party)
        if results_candidates[i] in finances_candidates[j] and results_df.loc[i][1] == finances_df.loc[j][1] and results_df.loc[i][3] == finances_df.loc[j][3]:
            #Create new combined dataset with relevant data from both datasets
            code = finances_df.loc[j][1]
            name = finances_candidates[j]
            party = finances_df.loc[j][3]
            amount_raised = finances_df.loc[j][4]
            amount_spent = finances_df.loc[j][5]
            winner = finances_df.loc[j][6]
            incumbent = finances_df.loc[j][7]
            percent = results_df.loc[i][5]
            votes = results_df.loc[i][6]
            row = pd.DataFrame([{'Seat': code, 'Candidate': name, 'Party': party, 'Raised': amount_raised, 'Spent': amount_spent, 'Percent': percent, 'Votes': votes, 'Winner': winner, 'Incumbent': incumbent}])
            combined_df = pd.concat([combined_df, row])
            used_results_indices.append(i)
            used_finances_indices.append(j)
#Find candidates where we only have either finances or results data 
unused_results_candidates = []
unused_finances_candidates = []
#Find unused indices
for i in range(len(results_candidates)):
    if i not in used_results_indices:
        unused_results_candidates.append(results_candidates[i])
for i in range(len(finances_candidates)):
    if i not in used_finances_indices:
        unused_finances_candidates.append(finances_candidates[i])
unused_results_df = pd.DataFrame()
unused_finances_df = pd.DataFrame()
#Create new dataset for candidates where we have results but not finances data
for i in range(len(results_candidates)):
    if i not in used_results_indices:
        unused_results_df = unused_results_df.append(results_df.loc[i])
#Create new dataset for candidates where we have finances but not results data
for i in range(len(finances_candidates)):
    if i not in used_finances_indices:
        unused_finances_df = unused_finances_df.append(finances_df.loc[i])
combined_df.to_csv("house_2020_finances_results.csv")
unused_results_df.to_csv("house_2020_results_no_finances.csv")
unused_finances_df.to_csv("house_2020_finances_no_results.csv")


