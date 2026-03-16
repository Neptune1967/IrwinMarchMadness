from bs4 import BeautifulSoup
import requests

page_to_scrape = requests.get("https://www.ncaa.com/march-madness-live/bracket")

class Player:
    def __init__(self, name, email, teams, paid=True):
        self.name = name
        self.email = email
        self.teams = teams
        self.paid = paid

class Team:
    def __init__(self, name, seed):
        self.name = name
        self.seed = seed
        self.counter = -1  # counts appearances of the team name

    def __repr__(self):
        return f"{self.name} ({self.seed}) [{self.counter}]"
    


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

team_lookup = {team.name: team for team in teams_list}
# Build list of visible team names
visible_team_names = [team for team, seed in zip(teams[:68], seeds[:68])]

# Identify play-in teams
game_pods_teams = [p.get_text(strip=True)
                   for p in soup.select(".game-pods p.body.body_2")
                   if p.get_text(strip=True)]

# Initialize counters
for team_obj in teams_list:
    if team_obj.name in game_pods_teams:
        team_obj.counter = -2
    else:
        team_obj.counter = -1

# Add +1 for every appearance
for name in visible_team_names:
    team_obj = team_lookup.get(name)
    if team_obj:
        team_obj.counter += 1

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
    
    paid_status = "PAID" if is_paid_var.get() else "UNPAID"

    line = ",".join([name, email, paid_status] + [f"{t.name} ({t.seed})" for t in selected])
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

    root.update_idletasks()

def mark_as_paid(player_name):
    for filename in ["records_company.txt", "records_external.txt"]:

        try:
            rows = []

            with open(filename, "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[0] == player_name:
                        row[2] = "PAID"
                    rows.append(row)

            with open(filename, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(rows)

        except FileNotFoundError:
            pass

def show_leaderboard():
    leaderboard_win = tk.Toplevel(root)
    leaderboard_win.title("Leaderboard")
    leaderboard_win.geometry("700x700")

    tk.Label(leaderboard_win, text="Leaderboard", font=("Arial", 14, "bold")).pack(pady=5)

    text_frame = tk.Frame(leaderboard_win)
    text_frame.pack(fill="both", expand=True, padx=10, pady=10)

    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side="right", fill="y")

    text_widget = tk.Text(text_frame, width=60, yscrollcommand=scrollbar.set)
    text_widget.pack(side="left", fill="both", expand=True)
    text_widget.bind("<MouseWheel>", lambda e: text_widget.yview_scroll(int(-1*(e.delta/120)), "units"))

    scrollbar.config(command=text_widget.yview)

    # ---- ADD THE PAY FRAME HERE ----
    pay_frame = tk.Frame(leaderboard_win)
    pay_frame.pack(pady=5)

    tk.Label(pay_frame, text="Mark Player as Paid:").pack(side="left")

    player_entry = tk.Entry(pay_frame)
    player_entry.pack(side="left", padx=5)

    tk.Button(
        pay_frame,
        text="Mark Paid",
        command=lambda: (
            mark_as_paid(player_entry.get().strip()),
            messagebox.showinfo("Updated", "Player marked as PAID")
        )
    ).pack(side="left")

    # leaderboard refresh function
    def refresh_leaderboard():
        # Save current scroll position
        scroll_pos = text_widget.yview()

        text_widget.config(state="normal")
        text_widget.delete("1.0", tk.END)

        unpaid_players = []

        for filename, title in [("records_company.txt", "Company Employees"),
                                ("records_external.txt", "External Users")]:

            text_widget.insert(tk.END, f"{title}:\n")

            paid_leaderboard = []

            try:
                with open(filename, "r") as f:
                    reader = csv.reader(f)

                    for row in reader:
                        name = row[0]
                        paid_status = row[2]
                        team_entries = row[3:]

                        score = 0

                        for entry in team_entries:
                            if "(" in entry:
                                team_name = entry.rsplit("(", 1)[0].strip()
                                team_obj = team_lookup.get(team_name)

                                if team_obj:
                                    score += (team_obj.seed + 3) * team_obj.counter

                        if paid_status == "PAID":
                            paid_leaderboard.append((name, score))
                        else:
                            unpaid_players.append(name)

            except FileNotFoundError:
                continue

            paid_leaderboard.sort(key=lambda x: x[1], reverse=True)

            for rank, (name, score) in enumerate(paid_leaderboard, start=1):
                text_widget.insert(tk.END, f"{rank}. {name} — {score} points\n")

            text_widget.insert(tk.END, "\n")

        text_widget.insert(tk.END, "Unpaid Players:\n")

        for name in unpaid_players:
            text_widget.insert(tk.END, f"{name}\n")

        # Restore previous scroll position
        text_widget.yview_moveto(scroll_pos[0])
        text_widget.config(state="disabled")

        leaderboard_win.after(2000, refresh_leaderboard)

    refresh_leaderboard()



def show_emails():
    email_win = tk.Toplevel(root)
    email_win.title("All Emails")
    email_win.geometry("400x500")

    tk.Label(email_win, text="All Unique Emails (Ctrl + a)", font=("Arial", 14, "bold")).pack(pady=5)

    text_widget = tk.Text(email_win, width=50, height=30, state="normal")
    text_widget.pack(padx=10, pady=10, fill="both", expand=True)

    emails = set()  # ensures uniqueness

    for filename in ["records_company.txt", "records_external.txt"]:
        try:
            with open(filename, "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) > 1:
                        emails.add(row[1].strip())
        except FileNotFoundError:
            pass

    text_widget.delete("1.0", tk.END)

    for email in sorted(emails):
        text_widget.insert(tk.END, f"{email}\n")

    text_widget.config(state="disabled")
# ----------------- GUI -----------------
root = tk.Tk()
root.title("March Madness Selector")
root.geometry("900x720")

# ---------- Top Section ----------
# Top frame for Record Name, Email, Checkbox, Leaderboard, Save
top_frame = tk.Frame(root)
top_frame.pack(anchor="w", padx=10, pady=5)

# Record Name
tk.Label(top_frame, text="Name:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
name_entry = tk.Entry(top_frame, width=25)
name_entry.grid(row=0, column=1, padx=5, pady=2)

# Email
tk.Label(top_frame, text="Email:").grid(row=0, column=2, sticky="w", padx=5, pady=2)
email_entry = tk.Entry(top_frame, width=25)
email_entry.grid(row=0, column=3, padx=5, pady=2)

# External User checkbox
is_external_var = tk.BooleanVar(value=False)
employee_checkbox = tk.Checkbutton(top_frame, text="External User", variable=is_external_var)
employee_checkbox.grid(row=0, column=4, padx=5, pady=2)

# Paid checkbox (checked by default)
is_paid_var = tk.BooleanVar(value=True)
paid_checkbox = tk.Checkbutton(top_frame, text="Paid", variable=is_paid_var)
paid_checkbox.grid(row=0, column=5, padx=5, pady=2)

# Leaderboard button
leaderboard_btn = tk.Button(top_frame, text="Show Leaderboard", command=show_leaderboard)
leaderboard_btn.grid(row=0, column=6, padx=5, pady=2)

emails_btn = tk.Button(top_frame, text="Show Emails", command=show_emails)
emails_btn.grid(row=0, column=7, padx=5, pady=2)

# Save button (right after leaderboard)
save_btn = tk.Button(top_frame, text="Save", command=save_record, width=10, bg="lightgreen")
save_btn.grid(row=0, column=8, padx=5, pady=2)

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



root.mainloop()
