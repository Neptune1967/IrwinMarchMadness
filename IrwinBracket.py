from bs4 import BeautifulSoup
import requests
#import re

page_to_scrape = requests.get("https://www.ncaa.com/march-madness-live/bracket")
soup = BeautifulSoup(page_to_scrape.text, "html.parser")
AllTeams = soup.findAll("p", attrs={"class":"body body_2 color_lvl_-5"})
AllSeeds = soup.find_all("span", attrs={"class":"overline color_lvl_-5"})

win_points = {
    "Duke": 4, "Auburn": 4, "Michigan St.": 5, "Bryant": 18, "Houston": 4, "Gonzaga": 11,
    "UConn": 11, "Oklahoma": 12, "Kentucky": 6, "Troy": 17, "Florida": 4, "Norfolk St.": 19,
    "Saint Mary's": 10, "Vanderbilt": 13, "Arizona": 7, "Akron": 16, "Marquette": 10, "New Mexico": 13,
    "Purdue": 7, "McNeese": 15, "Wisconsin": 6, "BYU": 9, "Texas Tech": 6, "Drake": 14,
    "Ole Miss": 9, "North Carolina": 14, "Memphis": 8, "Colorado St.": 15, "Alabama": 5,
    "Robert Morris": 18, "Mississippi St.": 11, "Baylor": 12, "Louisville": 11, "Iowa St.": 6,
    "Lipscomb": 17, "Creighton": 12, "Arkansas": 13, "Maryland": 7, "Grand Canyon": 16, "Liberty": 15,
    "SIU Edwardsville": 19, "UCLA": 10, "Xavier": 14, "Texas A&M": 7, "High Point": 16, "Montana": 17,
    "VCU": 14, "Clemson": 8, "St. John's": 5, "Illinois": 9, "American": 19,
    "Mount St. Mary's": 19, "Alabama St.": 19, "Saint Francis U": 19, "UC San Diego": 15,
    "Kansas": 10, "Tennessee": 5, "Oregon": 8, "Michigan": 8,
    "Yale": 16, "Missouri": 9, "UNC Wilmington": 17,
    "Omaha": 18, "Georgia": 12, "Utah St.": 13, "Wofford": 18, "Texas": 14, "San Diego St.": 14,
}

team_counters = {
    "Duke": 0, "Auburn": 0, "Michigan St.": 0, "Bryant": 0, "Houston": 0, "Gonzaga": 0,
    "UConn": 0, "Oklahoma": 0, "Kentucky": 0, "Troy": 0, "Florida": 0, "Norfolk St.": 0,
    "Saint Mary's": 0, "Vanderbilt": 0, "Arizona": 0, "Akron": 0, "Marquette": 0, "New Mexico": 0,
    "Purdue": 0, "McNeese": 0, "Wisconsin": 0, "BYU": 0, "Texas Tech": 0, "Drake": 0,
    "Ole Miss": 0, "North Carolina": -1, "Memphis": 0, "Colorado St.": 0, "Alabama": 0,
    "Robert Morris": 0, "Mississippi St.": 0, "Baylor": 0, "Louisville": 0, "Iowa St.": 0,
    "Lipscomb": 0, "Creighton": 0, "Arkansas": 0, "Maryland": 0, "Grand Canyon": 0, "Liberty": 0,
    "SIU Edwardsville": 0, "UCLA": 0, "Xavier": 0, "Texas A&M": 0, "High Point": 0, "Montana": 0,
    "VCU": 0, "Clemson": 0, "St. John's": 0, "Illinois": 0, "American": -1,
    "Mount St. Mary's": -1, "Alabama St.": -1, "Saint Francis U": -1, "UC San Diego": 0,
    "Kansas": 0, "Tennessee": 0, "Oregon": 0, "Michigan": 0,
    "Yale": 0, "Missouri": 0, "UNC Wilmington": 0,
    "Omaha": 0, "Georgia": 0, "Utah St.": 0, "Wofford": 0, "Texas": -1, "San Diego St.": -1,
}

# Function to simulate a switch statement
def count_team(team_name):
    if team_name.strip() in team_counters:
        team_counters[team_name.strip()] += 1
    #else:
        #print(f"Team '{team_name}' not found.")

count = 0
def count_points(team_name):
    cpoints = 0
    #print("in method")
    if team_name in win_points:
        #print("in loop")
        cpoints = win_points.get(team_name.strip())
    return cpoints

for team in AllTeams:

    # print(team.text)
    #if (team.text == "Michigan State"):
    count_team(team.text)

class Player:
    def __init__(self, name, email, teams):
        self.name = name  # String attribute
        self.email = email  # String attribute
        self.teams = teams  # Array attribute
    
Isaac = Player(name="Isaac", email="isaac.bouwkamp@irwinseating.com", teams = ["Michigan","Iowa St.", "Memphis", "Texas Tech", "Oregon", "Wisconsin", "Clemson", "Kentucky", "VCU", "Drake" ])

print(Isaac.teams)

for team in Isaac.teams:
    print(team)
    value = count_points(team)
    timesOnBracket = team_counters[team]
    while(int(timesOnBracket) > 1):
        count = count + int(value)
        timesOnBracket = timesOnBracket - 1
    print("The current value of count is " + str(count))

#win_points("Michigan")

print(count)

#for team, count in team_counters.items():
    #print(f"{team}: {count}")

#print(AllSeeds)




## Example string
##text = "This is an example <!--[first]--> and another <!--[second]--> with extra <!--[third]< more."

## Regular expression to find all characters between <!--[ and the next <
#matches = re.findall(r'<!-->\[(.*?)<', AllSeeds)

## Print the matches
#print(matches) 

