import pandas as pd	
#Create a list of all US states to iterate over 
states = pd.read_csv("https://raw.githubusercontent.com/Jacob-McLaughlin/Jacob-McLaughlin.github.io/main/project/data/US_state_list.csv")
state_list = states["State"].tolist()
#Create base URL to format for scraping
url_base_year = "https://www.politico.com/{}-election"
url_base_state = "/results/{}/house/"
#Select years to get results for 
years = ["2020"]
#Create empty dataframe to hold results
house_results = pd.DataFrame()
#Iterate over years
for year in years:
  url_year = url_base_year.format(year)
  for state in state_list:
    #Update URL
    url_state = url_base_state.format(state.lower())
    url = url_year + url_state
    #Access data from website
    politico_page = pd.read_html(url)
    num_seats = len(politico_page)
    #Iterate over each house seat in state 
    for i in range(num_seats):
      num_candidates = len(politico_page[i])
      seat = state + "_district_" + str(i+1)
      #Iterate over each candidate in seat
      for j in range(num_candidates):
        #Access candidate name and format
        candidate_name = politico_page[i].iloc[j][0]
        party = candidate_name[-3:]
        if "*" in candidate_name:
          incumbency = "Y"
          short_name = candidate_name[:-4]
        else:
          incumbency = "N"
          short_name = candidate_name[:-3]
        #Access candidate results and format
        candidate_results = politico_page[i].iloc[j][1]
        percentage = candidate_results.split("%")[0]
        votes = candidate_results.split("%")[1]
        #Create row to add to dataframe
        row = pd.DataFrame([{'Seat': seat, 'Candidate': short_name, 'Party': party, 'Incumbent': incumbency, 'Percent': percentage, 'Votes': votes, 'Year': year}])
      house_results = pd.concat([house_results, row]) 
#Show output 
print(house_results)
#Write to csv
house_results.to_csv("politico_2020_house.csv")
