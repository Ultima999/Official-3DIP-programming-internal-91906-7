import json
import tkinter as tk
from tkinter import messagebox, scrolledtext

# --- Load exercise and muscle data from JSON file ---
with open('V3-5BothEandM.json', 'r') as file:
    data = json.load(file)

# Try to load existing schedule JSON; if not found, start empty
try:
    with open("V3-5schedule.json", "r") as schedule_file:
        json_schedule_data = json.load(schedule_file)
except FileNotFoundError:
    json_schedule_data = {"workout_schedule": []}

# Separate JSON data into respective variables
exercises = data["exercises"]
muscle_groups = data["muscle_groups"]

# List structure for the week: [day name, rest/workout status]
day_list = [
    ['Monday', True], ['Tuesday', True], ['Wednesday', True],
    ['Thursday', True], ['Friday', True], ['Saturday', True], ['Sunday', True]
]
chosen_day_list = []
days_of_the_week = [day[0] for day in day_list]

def update_output_box():
    # Updates on-screen summary of all workout and rest days
    output_display.config(state="normal")
    output_display.delete(1.0, tk.END)
    text_content = ""
    for day_entry in day_list:
        weekday_name, rest, *muscles = day_entry
        if rest:
            text_content += f"{weekday_name}: Rest Day\n"
        else:
            if muscles:
                text_content += f"{weekday_name}: Workout Day → {', '.join(muscles[0])}\n"
    output_display.insert(tk.END, text_content)
    output_display.config(state="disabled")

def find_exercises_by_muscle():
    # Opens popup to allow user to select a muscle and view related exercises
    popup_window = tk.Toplevel(root)
    popup_window.title("Choose a Muscle Group")

    tk.Label(popup_window, text="Select a muscle group:", font=("Arial", 12, "bold")).pack(pady=5)
    muscle_listbox = tk.Listbox(popup_window, selectmode="single", height=10, exportselection=False)

    # Populate the listbox with all muscle names from the JSON data
    for muscle_name in muscle_groups.keys():
        muscle_listbox.insert(tk.END, muscle_name)
    muscle_listbox.pack(padx=10, pady=5)

    def confirm_muscle_selection():
        # Triggered when user clicks confirm; retrieves selected muscle and displays exercises
        selected_index = muscle_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a muscle group.")
            return

        selected_muscle = muscle_listbox.get(selected_index)

        # Check if the chosen muscle has recorded exercises
        if selected_muscle in exercises:
            related_exercises = exercises[selected_muscle]
            sub_muscles = muscle_groups.get(selected_muscle, [])
            last_sub_muscle = sub_muscles[-1] if sub_muscles else ""
            other_sub_muscles = ", ".join(sub_muscles[:-1]) if len(sub_muscles) > 1 else ""

            # Display either a single or multiple exercise recommendations
            if len(related_exercises) == 1:
                result = f"For {selected_muscle}, a recommended exercise is: {related_exercises[0]}.\nHits: {other_sub_muscles}, {last_sub_muscle}"
            else:
                result = f"For {selected_muscle}, you can do {', '.join(related_exercises[:-1])} and {related_exercises[-1]}.\nHits: {other_sub_muscles}, {last_sub_muscle}"
        else:
            result = f"Sorry, no exercises found for {selected_muscle}."

        # Show the result in a popup window
        messagebox.showinfo("Exercises", result)
        popup_window.destroy()

    tk.Button(popup_window, text="Confirm", command=confirm_muscle_selection).pack(pady=5)


def create_schedule():
    # Opens a new window where the user chooses workout days and muscles for each
    schedule_window = tk.Toplevel(root)
    schedule_window.title("Create Schedule")

    tk.Label(schedule_window, text="Select workout days:", font=("Arial", 12, "bold")).pack(pady=5)
    day_listbox = tk.Listbox(schedule_window, selectmode="multiple", exportselection=False)
    for day_name in days_of_the_week:
        day_listbox.insert(tk.END, day_name)
    day_listbox.pack(padx=10, pady=5)

    muscle_selection_frames = {}  # Stores each day’s muscle listbox frame

    def confirm_selected_days():
        # Validates and saves the selected workout days
        selected_days = [day_listbox.get(i) for i in day_listbox.curselection()]
        if not selected_days:
            messagebox.showerror("Error", "Please select at least one workout day.")
            return

        chosen_day_list.clear()

        # Update global list with workout/rest day information
        for day_entry in day_list:
            if day_entry[0] in selected_days:
                day_entry[1] = False
                chosen_day_list.append(day_entry[0])
            else:
                day_entry[1] = True
            if len(day_entry) > 2:
                day_entry.pop()

        # Reset any previous day-muscle frames
        for frame in muscle_selection_frames.values():
            frame.destroy()
        muscle_selection_frames.clear()

        # Create a section for each workout day where the user picks muscles
        for selected_day in selected_days:
            day_frame = tk.LabelFrame(schedule_window, text=f"Muscles for {selected_day}", padx=5, pady=5)
            day_frame.pack(padx=10, pady=5, fill="x")

            muscle_listbox = tk.Listbox(day_frame, selectmode="multiple", exportselection=False, height=6)
            for muscle_group_name in muscle_groups.keys():
                muscle_listbox.insert(tk.END, muscle_group_name)
            muscle_listbox.pack()
            muscle_selection_frames[selected_day] = muscle_listbox

    def confirm_all_muscles():
        # Saves all chosen muscle groups into the day_list structure
        for selected_day_name, muscle_listbox in muscle_selection_frames.items():
            selected_muscles = [muscle_listbox.get(i) for i in muscle_listbox.curselection()]
            if not selected_muscles:
                messagebox.showerror("Error", f"Please select at least one muscle group for {selected_day_name}.")
                return
            for day_entry in day_list:
                if day_entry[0] == selected_day_name:
                    if len(day_entry) > 2:
                        day_entry[2] = selected_muscles
                    else:
                        day_entry.append(selected_muscles)

        save_schedule_to_json()
        update_output_box()
        messagebox.showinfo("Schedule", "✅ Workout schedule updated!")
        schedule_window.destroy()

    tk.Button(schedule_window, text="Next", command=confirm_selected_days).pack(pady=5)
    tk.Button(schedule_window, text="Confirm All", command=confirm_all_muscles).pack(pady=5)


def save_schedule_to_json(filename="V3-5schedule.json"):
    # Converts the current schedule into JSON format and saves to file
    json_schedule_data = {"workout_schedule": []}
    for day_entry in day_list:
        day_name = day_entry[0]
        rest_status = day_entry[1]
        muscle_day = day_entry[2] if len(day_entry) > 2 else []
        json_schedule_data["workout_schedule"].append({ # Appending all the inputs ot the JSON file
            "name": day_name,
            "rest": rest_status,
            "workout_purpose": muscle_day,
            "exercises": []  # Exercises to be added in later versions
        })
    # Write the updated schedule to the JSON file
    with open(filename, "w") as json_file:
        json.dump(json_schedule_data, json_file, indent=2)


def view_full_schedule(filename="V3-5schedule.json"):
    # Displays all days and their workout/rest status in a scrollable text window
    try:
        with open(filename, "r") as json_file:
            json_schedule_data = json.load(json_file)

        schedule_output = ""
        for day_entry in json_schedule_data["workout_schedule"]:
            status = "Rest Day" if day_entry["rest"] else "Workout Day"
            purposes = ", ".join(day_entry["workout_purpose"]) if day_entry["workout_purpose"] else "None"
            exercises = ", ".join(day_entry["exercises"]) if day_entry["exercises"] else "None"
            schedule_output += f"\n{day_entry['name']}: {status}\n"
            schedule_output += f"  Muscles: {purposes}\n"
            schedule_output += f"  Exercises: {exercises}\n"

        show_text_window("Full Schedule", schedule_output)
    except FileNotFoundError:
        messagebox.showerror("Error", f"{filename} not found.")


def show_text_window(title, content):
    # Creates a new window with a scrollable text display (for full schedule view)
    popup_window = tk.Toplevel(root)
    popup_window.title(title)
    text_display = scrolledtext.ScrolledText(popup_window, wrap=tk.WORD, width=60, height=20, font=("Arial", 11))
    text_display.insert(tk.END, content)
    text_display.config(state="disabled")
    text_display.pack(padx=10, pady=10)


# Main GUI initialization
root = tk.Tk()
root.title("Zane's Fitness App")
root.geometry("600x600")

tk.Label(root, text="Welcome to Zane's Fitness App!", font=("Arial", 14, "bold")).pack(pady=10)

# Buttons for all core features of the app
tk.Button(root, text="Create Workout Schedule", command=create_schedule, width=40).pack(pady=5)
tk.Button(root, text="Find Exercises for Muscle Group", command=find_exercises_by_muscle, width=40).pack(pady=5)
tk.Button(root, text="Save Schedule to JSON", command=save_schedule_to_json, width=40).pack(pady=5)
tk.Button(root, text="View Full Schedule on JSON", command=view_full_schedule, width=40).pack(pady=5)
tk.Button(root, text="Exit", command=root.quit, width=40).pack(pady=10)

# Scrolled text box that displays current workout/rest setup live
output_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=15, font=("Arial", 11))
output_display.pack(padx=10, pady=10)

update_output_box()  # Initialize display with current data
root.mainloop()       # Starts GUI loop (keeps window active)
