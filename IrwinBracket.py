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
    "Kansas": 0, "Tennessee": 0, "Oregon": 0, "Michigan": 1,
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

class Team:
    def __init__(self, name, seed):
        self.name = name
        self.seed = seed
        self.counter = 0  # counts appearances of the team name

    def __repr__(self):
        return f"{self.name} ({self.seed}) [{self.counter}]"
    
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

soup = BeautifulSoup(page_to_scrape.text, "html.parser")

# team names
teams = [p.get_text(strip=True) for p in soup.select("p.body.body_2") if p.get_text(strip=True)]

# seeds (only digits)
seeds = [s.get_text(strip=True) for s in soup.select("span.overline") if s.get_text(strip=True).isdigit()]


# Print teams and seeds
for team, seed in zip(teams, seeds):
    print(f"{team} {seed}", end=", ")

# Only take the first 68 teams and seeds
teams_list = []
for team, seed in zip(teams[:68], seeds[:68]):
    team_obj = Team(team, int(seed))
    teams_list.append(team_obj)

# Build a list of visible team names
visible_team_names = [team for team, seed in zip(teams[:68], seeds[:68])]

# Count exact occurrences
for team_obj in teams_list:
    team_obj.counter = visible_team_names.count(team_obj.name)

# Reduce counters for teams in the play-in game-pods
game_pods_teams = [p.get_text(strip=True) 
                   for p in soup.select(".game-pods p.body.body_2") 
                   if p.get_text(strip=True)]

for team_obj in teams_list:
    if team_obj.name in game_pods_teams:
        team_obj.counter = 0

# Print results
if teams_list:
    print("Teams successfully stored:\n")
    for i, team in enumerate(teams_list, start=1):
        print(f"{i}. Team: {team.name}, Seed: {team.seed}, Count: {team.counter}")
else:
    print("No teams were stored.")

print(f"\nTotal teams stored: {len(teams_list)}")



import csv

# Create lookup dictionary
team_lookup = {team.name: team for team in teams_list}

leaderboard = []

with open("records.txt", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        name = row[0]
        email = row[1]
        team_entries = row[2:]  # list of "Team Name (Seed)" strings
        score = 0
        for entry in team_entries:
            if "(" in entry:
                team_name = entry.rsplit("(", 1)[0].strip()  # "Houston"
                # Lookup the Team object
                team_obj = team_lookup.get(team_name)
                if team_obj:
                    score += (team_obj.seed + 3) * team_obj.counter
        leaderboard.append((name, score))

# Sort by score descending
leaderboard.sort(key=lambda x: x[1], reverse=True)

# Print leaderboard
print("Leaderboard:")
for rank, (name, score) in enumerate(leaderboard, start=1):
    print(f"{rank}. {name} — {score} points")
## Example string
##text = "This is an example <!--[first]--> and another <!--[second]--> with extra <!--[third]< more."

## Regular expression to find all characters between <!--[ and the next <
#matches = re.findall(r'<!-->\[(.*?)<', AllSeeds)

## Print the matches
#print(matches) 
#####################################################
import tkinter as tk
from tkinter import messagebox
import csv

# ----------------- Use your actual teams_list from scraping -----------------
# teams_list = [...]  <- This comes from your scraping code
teams_list_sorted = sorted(teams_list, key=lambda t: t.seed)
team_lookup = {team.name: team for team in teams_list}

selected = set()
MAX_SELECTION = 10

# ----------------- Functions -----------------
def toggle(team_obj, btn):
    if team_obj in selected:
        selected.remove(team_obj)
        btn.config(relief="raised", bg="SystemButtonFace")
    else:
        if len(selected) >= MAX_SELECTION:
            messagebox.showwarning("Limit reached", f"You can only select {MAX_SELECTION} teams.")
            return
        selected.add(team_obj)
        btn.config(relief="sunken", bg="lightblue")
    update_list()

def update_list():
    listbox.delete(0, tk.END)
    for item in sorted(selected, key=lambda x: x.name):
        listbox.insert(tk.END, f"{item.name} ({item.seed})")

def save_record():
    name = name_entry.get().strip()
    email = email_entry.get().strip()
    
    if not name:
        messagebox.showerror("Error", "Please enter a record name.")
        return
    if not email:
        messagebox.showerror("Error", "Please enter an email.")
        return
    if len(selected) != 10:
        messagebox.showerror("Error", "You must select exactly 10 teams before saving.")
        return
    
    # Inverted logic: checked = external, unchecked = company
    filename = "records_external.txt" if is_external_var.get() else "records_company.txt"
    
    line = ",".join([name, email] + [f"{t.name} ({t.seed})" for t in selected])
    with open(filename, "a") as f:
        f.write(line + "\n")
    
    messagebox.showinfo("Saved", f"Record saved to {filename}!")
    
    # Reset entries (name/email), but keep checkbox as is
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    
    selected.clear()
    update_list()
    for btn in buttons:
        btn.config(relief="raised", bg="SystemButtonFace")

def show_leaderboard():
    leaderboard_win = tk.Toplevel(root)
    leaderboard_win.title("Leaderboard")
    leaderboard_win.geometry("500x500")
    
    tk.Label(leaderboard_win, text="Leaderboard", font=("Arial", 14, "bold")).pack(pady=5)
    
    text_widget = tk.Text(leaderboard_win, width=60, height=30, state="normal")
    text_widget.pack(padx=10, pady=10, fill="both", expand=True)
    
    for filename, title in [("records_company.txt", "Company Employees"), ("records_external.txt", "External Users")]:
        text_widget.insert(tk.END, f"{title}:\n")
        leaderboard = []
        try:
            with open(filename, "r") as f:
                import csv
                reader = csv.reader(f)
                for row in reader:
                    name = row[0]
                    team_entries = row[2:]
                    score = 0
                    for entry in team_entries:
                        if "(" in entry:
                            team_name = entry.rsplit("(", 1)[0].strip()
                            team_obj = team_lookup.get(team_name)
                            if team_obj:
                                score += (team_obj.seed + 3) * team_obj.counter
                    leaderboard.append((name, score))
            leaderboard.sort(key=lambda x: x[1], reverse=True)
        except FileNotFoundError:
            text_widget.insert(tk.END, "No records found.\n")
            continue
        
        for rank, (name, score) in enumerate(leaderboard, start=1):
            text_widget.insert(tk.END, f"{rank}. {name} — {score} points\n")
        text_widget.insert(tk.END, "\n")
    
    text_widget.config(state="disabled")

# ----------------- GUI -----------------
root = tk.Tk()
root.title("March Madness Selector")
root.geometry("900x720")

# ---------- Top Section ----------
# Top frame for Record Name, Email, Checkbox, and Leaderboard button
top_frame = tk.Frame(root)
top_frame.pack(anchor="w", padx=10, pady=5)

# Record Name
tk.Label(top_frame, text="Record Name:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
name_entry = tk.Entry(top_frame, width=25)
name_entry.grid(row=0, column=1, padx=5, pady=2)

# Email
tk.Label(top_frame, text="Email:").grid(row=0, column=2, sticky="w", padx=5, pady=2)
email_entry = tk.Entry(top_frame, width=25)
email_entry.grid(row=0, column=3, padx=5, pady=2)

# Checkbox now means "External User"
is_external_var = tk.BooleanVar(value=False)  # default unchecked = company

employee_checkbox = tk.Checkbutton(
    top_frame, text="External User", variable=is_external_var
)
employee_checkbox.grid(row=0, column=4, padx=5, pady=2)

# Leaderboard button
leaderboard_btn = tk.Button(top_frame, text="Show Leaderboard", command=show_leaderboard, bg="yellow")
leaderboard_btn.grid(row=0, column=5, padx=5, pady=2)

# ---------- Main Content ----------
frame = tk.Frame(root)
frame.pack(fill="both", expand=True, padx=10, pady=10)

# Left side: Team buttons in multi-column layout
button_frame = tk.Frame(frame)
button_frame.pack(side="left", fill="both", expand=True)

buttons = []
cols = 4
for idx, team_obj in enumerate(teams_list_sorted):
    b = tk.Button(button_frame, text=f"{team_obj.name} ({team_obj.seed})", width=20)
    b.config(command=lambda t=team_obj, btn=b: toggle(t, btn))
    row = idx // cols
    col = idx % cols
    b.grid(row=row, column=col, padx=5, pady=5, sticky="w")
    buttons.append(b)

# Right side: Selected teams list
list_frame = tk.Frame(frame)
list_frame.pack(side="right", fill="y")
tk.Label(list_frame, text="Selected Teams:").pack()
listbox = tk.Listbox(list_frame, width=30)
listbox.pack()

# Save button
save_btn = tk.Button(root, text="Save", command=save_record, width=10)
save_btn.pack(side="right", padx=10, pady=10)

root.mainloop()
