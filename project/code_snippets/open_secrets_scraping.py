import pandas as pd
import numpy as np
import requests
#This code snippet scrapes data for the 2020 House election from OpenSecrets
#Import the number of house districts for each state 
congress_numbers = pd.read_csv("https://raw.githubusercontent.com/Jacob-McLaughlin/Jacob-McLaughlin.github.io/main/project/data/US_state_congress_numbers.csv")
#Generate the codes for each district in the format "AL01"
house_codes = []
for i in range(len(congress_numbers)):
  for j in range(1,congress_numbers.iloc[i][17]+1):
    if j < 10:
      short_code = congress_numbers.iloc[i][1] + "0" + str(j)
    else:
      short_code = congress_numbers.iloc[i][1] + str(j)
    house_codes.append(short_code)
url_base_year = "https://www.opensecrets.org/races/summary?cycle={}"
url_base_house = "&id={}"
#Select years to get results for 
years = ["2020"]
#Create empty dataframe to hold results
house_finances = pd.DataFrame()
for year in years:
  url_year = url_base_year.format(year)
  #Iterate over the different house seats 
  for code in house_codes:
    url_house = url_base_house.format(code)
    url = url_year + url_house
    r = requests.get(url)
    #Access the webpage for that house seat
    secrets_page = pd.read_html(r.text)
    for j in range(len(secrets_page[0])):
      #Reformat the candidate name 
      candidate = secrets_page[0].iloc[j][0]
      if "Winner" in candidate: 
        winner = "Y"
      else:
        winner = "N"
      if "Incumbent" in candidate:
        incumbent = "Y"
      else:
        incumbent = "N"
      if "(R)" in candidate:
        party = "gop"
      elif "(D)" in candidate:
        party = "dem"
      short_name = candidate.split("(")[0]
      amount_raised = secrets_page[0].iloc[j][1]
      amount_spent = secrets_page[0].iloc[j][2]
      row = pd.DataFrame([{'Seat': code, 'Candidate': short_name, 'Party': party, 'Raised': amount_raised, 'Spent': amount_spent, 'Winner': winner, 'Incumbent': incumbent}])
      house_finances = pd.concat([house_finances, row]) 
house_finances.to_csv("2020_house_finances_open_secrets.csv")
