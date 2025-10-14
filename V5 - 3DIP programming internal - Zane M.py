import json 
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

# Loads JSON files to find information for the exercise and muscle group data for use throughout the program.
with open('V3-5BothEandM.json', 'r') as file:
    file_data = json.load(file)

exercise_data = file_data["exercises"]        # Dictionary of main muscles containing the necessary values of exercises. 
muscle_group_data = file_data["muscle_groups"]  # Dictionary of main muscles with values as sub-muscles

# variable
week_day_list = [
    ['Monday', True], ['Tuesday', True], ['Wednesday', True],
    ['Thursday', True], ['Friday', True], ['Saturday', True], ['Sunday', True]
]
days_of_week = [day_entry[0] for day_entry in week_day_list]  # Extracts day names for listboxes etc.

# Try loading previous schedule data, otherwise create a blank template.
try:
    with open("V3-5schedule.json", "r") as schedule_file:
        schedule_json_data = json.load(schedule_file)
except FileNotFoundError:
    # Creates a new schedule structure if file does not exist
    schedule_json_data = {
        "workout_schedule": [
            {"name": day_name, "rest": True, "workout_purpose": [], "exercises": []}
            for day_name in days_of_week
        ]
    }

# Initialization of classes; intensities.
# Each class represents a type of exercise with its own intensity, with reps and sets.

class Exercise:
    # Base class containing universal exercise attributes
    def __init__(self, exercise_name, muscle_group, sets, reps, focus_type):
        self.exercise_name = exercise_name
        self.muscle_group = muscle_group
        self.sets = sets
        self.reps = reps
        self.focus_type = focus_type

    def get_info(self):
        # Returns formatted string with full exercise info
        return f"{self.exercise_name} ({self.focus_type}) - {self.sets}x{self.reps}"

# Inherited classes for each intensity focus:
class StrengthExercise(Exercise):
    def __init__(self, exercise_name, muscle_group):
        super().__init__(exercise_name, muscle_group, 5, 6, "Strength")

class HypertrophyExercise(Exercise):
    def __init__(self, exercise_name, muscle_group):
        super().__init__(exercise_name, muscle_group, 4, 12, "Hypertrophy")

class EnduranceExercise(Exercise):
    def __init__(self, exercise_name, muscle_group):
        super().__init__(exercise_name, muscle_group, 3, 20, "Endurance")

# Functions here handle input processing and logic and structure mapping between GUI and JSON.
def map_existing_exercises_by_day(existing_schedule_data):
    # Converts JSON schedule into a day→exercise list dictionary for easy lookup.
    return {day_entry["name"]: list(day_entry.get("exercises", []))
            for day_entry in existing_schedule_data.get("workout_schedule", [])}

def save_schedule_to_json(filename="V3-5schedule.json"):
    # Writes the current in-memory schedule to JSON for persistence.
    existing_exercise_map = map_existing_exercises_by_day(schedule_json_data)
    updated_schedule = {"workout_schedule": []}

    for day_entry in week_day_list:
        day_name = day_entry[0]
        is_rest_day = day_entry[1]
        muscle_list = day_entry[2] if len(day_entry) > 2 else []  # Handles missing muscles safely
        preserved_exercises = existing_exercise_map.get(day_name, [])
        # Appends updated day info to schedule JSON
        updated_schedule["workout_schedule"].append({
            "name": day_name,
            "rest": is_rest_day,
            "workout_purpose": muscle_list,
            "exercises": [] if is_rest_day else preserved_exercises
        })
    # Save file to disk
    with open(filename, "w") as schedule_file:
        json.dump(updated_schedule, schedule_file, indent=2)
    # Sync in-memory data
    schedule_json_data.clear()
    schedule_json_data.update(updated_schedule)

def are_consecutive_days(first_day, second_day):
    # Utility function to detect if two days are back-to-back in the week
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return abs(day_order.index(first_day) - day_order.index(second_day)) == 1

def create_schedule():
    # Opens a pop-up window for selecting workout days
    day_selection_window = tk.Toplevel(root_window)
    day_selection_window.title("Select Workout Days")
    day_selection_window.geometry("450x310")

    # GUI text labels
    tk.Label(day_selection_window, text="Select your workout days:", font=("Arial", 12, "bold")).pack(pady=5)
    tk.Label(day_selection_window,
             text="NOTE: You require between 2 - 5 Workout days weekly for optimal growth.\n"
                  "You also cannot hit the same muscle two days in a row,\n"
                  "as individual muscles need good rest between each workout.",
             font=("Arial", 10)).pack(pady=9)

    # Multiple selection listbox for days
    day_listbox = tk.Listbox(day_selection_window, selectmode="multiple", height=7, exportselection=False)
    for day_name in days_of_week:
        day_listbox.insert(tk.END, day_name)
    day_listbox.pack(padx=10, pady=6, fill=tk.X)

    def confirm_selected_days():
        # Checks that input is valid and at least 2 rest days exist
        selected_days = [day_listbox.get(i) for i in day_listbox.curselection()]
        if not selected_days:
            messagebox.showerror("Error", "Please select at least one workout day.")
            return
        if len(selected_days) == 7 or len(selected_days) == 6:
            messagebox.showerror("Error", "You must leave at least 2 rest days.")
            return
        if len(selected_days) == 1:
            messagebox.showerror("Error", "1 Workout day a week is not enough for proper growth.")
            return

        # Update global day list with new workout/rest info
        for day_entry in week_day_list:
            if day_entry[0] in selected_days:
                day_entry[1] = False
            else:
                day_entry[1] = True
            if len(day_entry) > 2:
                day_entry.pop()  # Clears old muscles if schedule is re-created

        # Move to muscle assignment window
        day_selection_window.destroy()
        open_muscle_selection_window(selected_days)

    tk.Button(day_selection_window, text="Next ➜", command=confirm_selected_days,
              font=("Arial", 11, "bold")).pack(pady=10)

def open_muscle_selection_window(selected_days):
    # Second GUI step: assign muscles to each chosen workout day
    muscle_assignment_window = tk.Toplevel(root_window)
    muscle_assignment_window.title("Assign Muscle Groups")
    muscle_assignment_window.geometry("800x350")

    tk.Label(muscle_assignment_window, text="Select muscle groups for each workout day:",
             font=("Arial", 12, "bold")).pack(pady=6)

    container_frame = tk.Frame(muscle_assignment_window)
    container_frame.pack(padx=8, pady=6)

    # Sort days by correct weekday order
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                 'Friday', 'Saturday', 'Sunday']
    selected_days.sort(key=lambda x: day_order.index(x))

    muscle_listboxes = {}  # Maps each day to its corresponding listbox
    for column_index, day_name in enumerate(selected_days):
        day_frame = tk.LabelFrame(container_frame, text=day_name, padx=6, pady=6)
        day_frame.grid(row=0, column=column_index, padx=8, pady=6)
        listbox_muscles = tk.Listbox(day_frame, selectmode="multiple", height=7, exportselection=False)
        for muscle_name in exercise_data.keys(): # initializing the scrollable listbost for day_name
            listbox_muscles.insert(tk.END, muscle_name)
        listbox_muscles.pack()
        muscle_listboxes[day_name] = listbox_muscles

    def confirm_selected_muscles():
        # Collects selected muscles for each day and checks for consecutive duplicates
        for selected_index, day_name in enumerate(selected_days):
            chosen_muscles = [muscle_listboxes[day_name].get(i)
                              for i in muscle_listboxes[day_name].curselection()]
            if not chosen_muscles:# handles blank input error
                messagebox.showerror("Error", f"Select at least one muscle group for {day_name}.")
                return

            # Prevent hitting same muscle on consecutive days
            if selected_index > 0:
                previous_day = selected_days[selected_index - 1]
                if are_consecutive_days(previous_day, day_name):
                    prev_muscles = [muscle_listboxes[previous_day].get(i)
                                    for i in muscle_listboxes[previous_day].curselection()]
                    overlapping_muscles = set(prev_muscles) & set(chosen_muscles)
                    if overlapping_muscles:
                        messagebox.showwarning("Warning",
                            f"⚠️ You can't train these on consecutive days "
                            f"({previous_day} → {day_name}): {', '.join(overlapping_muscles)}")
                        return

            # Save chosen muscles into master week_day_list
            for day_entry in week_day_list:
                if day_entry[0] == day_name:
                    if len(day_entry) > 2:
                        day_entry[2] = chosen_muscles
                    else:
                        day_entry.append(chosen_muscles)

        # Commit data and show success popup
        save_schedule_to_json()
        update_output_box()
        messagebox.showinfo("Schedule", "✅ Schedule created successfully!")
        muscle_assignment_window.destroy()

    tk.Button(muscle_assignment_window, text="Confirm Schedule ✅", command=confirm_selected_muscles,
              font=("Arial", 11, "bold")).pack(pady=10)

def describe_muscle_hit(muscle_name):
    # Creates readable string listing all sub-muscles for a given group
    sub_muscles = muscle_group_data.get(muscle_name, [])
    last = sub_muscles[-1]
    others = ", ".join(sub_muscles[:-1])
    return f"{muscle_name}: Containing the {others}, and {last}."

def choose_exercises_for_muscle():
    # Opens list of muscles to choose before viewing their exercises
    muscle_choice_window = tk.Toplevel(root_window)
    muscle_choice_window.title("Choose Exercises for a Muscle")
    tk.Label(muscle_choice_window, text="Select a muscle group:", font=("Arial", 12, "bold")).pack(pady=4)

    # List of muscles
    muscle_listbox = tk.Listbox(muscle_choice_window, height=10, exportselection=False)
    for muscle_name in muscle_group_data.keys():
        muscle_listbox.insert(tk.END, muscle_name)
    muscle_listbox.pack(padx=10, pady=4, fill=tk.X)

    # Dynamic label to show sub-muscles hit
    description_label = tk.Label(muscle_choice_window, text="", font=("Arial", 10), wraplength=400, justify="center")
    description_label.pack(pady=5)

    def on_muscle_select(event):
        # Updates description label whenever a muscle is clicked
        selected_index = muscle_listbox.curselection()
        if selected_index:
            selected_muscle = muscle_listbox.get(selected_index)
            description_text = describe_muscle_hit(selected_muscle)
            description_label.config(text=description_text)

    muscle_listbox.bind("<<ListboxSelect>>", on_muscle_select)

    def confirm_muscle_selection():
        # Proceeds to next window only if a muscle is selected
        if not muscle_listbox.curselection():
            messagebox.showerror("Error", "Please select a muscle group.")
            return
        selected_muscle = muscle_listbox.get(muscle_listbox.curselection())
        muscle_choice_window.destroy()
        open_exercise_selection_window(selected_muscle)

    tk.Button(muscle_choice_window, text="Next ➜", command=confirm_muscle_selection,
              font=("Arial", 11, "bold")).pack(pady=8)

def open_exercise_selection_window(selected_muscle):
    # Displays exercises available for chosen muscle
    if selected_muscle not in exercise_data:
        messagebox.showerror("Error", f"No exercises found for {selected_muscle}.")
        return

    exercise_selection_window = tk.Toplevel(root_window)
    exercise_selection_window.title(f"Select Exercises for {selected_muscle}")

    # Header labels
    tk.Label(exercise_selection_window, text=f"Exercises for {selected_muscle}:",
             font=("Arial", 12, "bold")).pack(pady=5)
    tk.Label(exercise_selection_window,
             text="These are the most effective, research-backed exercises "
                  "for your target muscle.\nScientifically proven to provide optimal muscle activation.",
             font=("Arial", 10), wraplength=450, justify="center").pack(pady=6)

    exercise_frame = tk.Frame(exercise_selection_window)
    exercise_frame.pack(pady=5, padx=10)

    # Checkboxes for multiple exercises
    exercise_check_vars = []
    for exercise_name in exercise_data[selected_muscle]:
        is_selected_var = tk.IntVar()
        tk.Checkbutton(exercise_frame, text=exercise_name, variable=is_selected_var).pack(anchor="w")
        exercise_check_vars.append((exercise_name, is_selected_var))

    def confirm_exercise_selection():
        # Collects chosen exercises and opens intensity window
        selected_exercises = [exercise_name for exercise_name, var in exercise_check_vars if var.get() == 1]
        if not selected_exercises:
            messagebox.showerror("Error", "Please select at least one exercise.")
            return
        exercise_selection_window.destroy()
        open_intensity_selection_window(selected_muscle, selected_exercises)

    tk.Button(exercise_selection_window, text="Next ➜", command=confirm_exercise_selection,
              font=("Arial", 11, "bold")).pack(pady=8)

def open_intensity_selection_window(selected_muscle, selected_exercises):
    # Final step: choose intensity for each selected exercise
    intensity_window = tk.Toplevel(root_window)
    intensity_window.title(f"Set Intensities for {selected_muscle}")

    # Explanation of training types
    tk.Label(intensity_window, text=f"Select intensity for each exercise:",
             font=("Arial", 12, "bold")).pack(pady=5)
    tk.Label(intensity_window,
             text="Strength: 5x6 reps - focuses on power and heavy load.\n"
                  "Hypertrophy: 4x12 reps - maximizes muscle growth.\n"
                  "Endurance: 3x20 reps - builds stamina and tone.",
             font=("Arial", 11)).pack(pady=6)

    intensity_frame = tk.Frame(intensity_window)
    intensity_frame.pack(padx=10, pady=5)

    # Each exercise has a combobox for intensity choice
    exercise_intensity_boxes = {}
    for exercise_name in selected_exercises:
        row_frame = tk.Frame(intensity_frame)
        row_frame.pack(fill="x", pady=2)
        tk.Label(row_frame, text=exercise_name, width=30, anchor="w").pack(side="left")
        intensity_combobox = ttk.Combobox(row_frame, values=["Strength", "Hypertrophy", "Endurance"],
                                          state="readonly", width=15)
        intensity_combobox.set("Hypertrophy")  # Default value
        intensity_combobox.pack(side="left", padx=5)
        exercise_intensity_boxes[exercise_name] = intensity_combobox

    def confirm_intensity_selection():
        # Creates Exercise objects based on chosen intensities
        exercise_objects = []
        for exercise_name, combo_box in exercise_intensity_boxes.items():
            focus_type = combo_box.get() #turning inputted exercises, appending them as objects
            if focus_type == "Strength":
                exercise_objects.append(StrengthExercise(exercise_name, selected_muscle))
            elif focus_type == "Endurance":
                exercise_objects.append(EnduranceExercise(exercise_name, selected_muscle))
            else:
                exercise_objects.append(HypertrophyExercise(exercise_name, selected_muscle))

        # Adds exercise info into all schedule days that hit this muscle
        for day_entry in schedule_json_data["workout_schedule"]:
            if selected_muscle in day_entry["workout_purpose"]:
                for exercise_obj in exercise_objects:
                    exercise_info = exercise_obj.get_info()
                    if exercise_info not in day_entry["exercises"]:
                        day_entry["exercises"].append(exercise_info)

        # Save and show confirmation
        save_schedule_to_json()
        update_output_box()
        messagebox.showinfo("Success", f"✅ Added {len(exercise_objects)} exercise(s) for {selected_muscle}.")
        intensity_window.destroy()

    tk.Button(intensity_window, text="Add Exercises ✅",
              command=confirm_intensity_selection, font=("Arial", 11, "bold")).pack(pady=10)

def reset_all_data():
    # Clears all stored schedule data and resets files
    if not messagebox.askyesno("Confirm Reset", "Reset all data (clear JSON and in-memory schedule)?"):
        return
    for index in range(len(week_day_list)):
        week_day_list[index] = [days_of_week[index], True]

    empty_schedule = {#blank template of the workout schedule for when user resets
        "workout_schedule": [
            {"name": day_name, "rest": True, "workout_purpose": [], "exercises": []}
            for day_name in days_of_week
        ]
    }
    with open("V3-5schedule.json", "w") as schedule_file:
        json.dump(empty_schedule, schedule_file, indent=2)

    schedule_json_data.clear()#clears the JSON file and uploads the blank template
    schedule_json_data.update(empty_schedule)

    update_output_box()
    messagebox.showinfo("Reset", "✅ All data has been reset.")

def view_full_schedule(filename="V3-5schedule.json"):
    # Displays the full schedule (all days, muscles, and exercises) from the JSON file.
    try:
        with open(filename, "r") as schedule_file:
            json_data = json.load(schedule_file)
        summary_text = ""
        # Loop through each day and build a readable summary of the user's plan
        for day_entry in json_data["workout_schedule"]:
            day_status = "Rest Day" if day_entry["rest"] else "Workout Day"
            muscle_string = ", ".join(day_entry["workout_purpose"]) if day_entry["workout_purpose"] else "None"
            exercise_string = ", ".join(day_entry["exercises"]) if day_entry["exercises"] else "None"
            # Append formatted text for each day into one long summary string
            summary_text += f"\n{day_entry['name']}: {day_status}\n"
            summary_text += f"  Muscles: {muscle_string}\n  Exercises: {exercise_string}\n"
        # Show results in a scrollable popup
        show_text_window("Full Schedule", summary_text)
    except FileNotFoundError:
        # Display an error popup if the JSON file has not yet been created
        messagebox.showerror("Error", "Schedule file not found.")


def show_text_window(window_title, window_content):
    # Creates a scrollable text window (used to display full schedules or summaries)
    text_window = tk.Toplevel(root_window)
    text_window.title(window_title)
    # ScrolledText widget allows long multi-line content with vertical scrolling
    text_area_widget = scrolledtext.ScrolledText(
        text_window, wrap=tk.WORD, width=60, height=20, font=("Arial", 11)
    )
    text_area_widget.insert(tk.END, window_content)   # Insert schedule text
    text_area_widget.config(state="disabled")         # Make text read-only
    text_area_widget.pack(padx=8, pady=8)


def update_output_box():
    # Updates the live summary box on the main window with the current in-memory schedule
    output_textbox.config(state="normal")     # Enable editing so content can be replaced
    output_textbox.delete(1.0, tk.END)        
    summary_text = ""
    # Loop through each weekday and display whether it's a rest or workout day
    for day_entry in week_day_list:
        day_name, is_rest, *muscles = day_entry
        if is_rest:
            summary_text += f"{day_name}: Rest Day\n"
        else:
            summary_text += f"{day_name}: Workout Day → {', '.join(muscles[0]) if muscles else '(none)'}\n"
    output_textbox.insert(tk.END, summary_text)  # Show the summary
    output_textbox.config(state="disabled")      # Lock textbox to prevent user editing


# GUI Setup, configuration, and initialization.
root_window = tk.Tk()
root_window.title("Zane's Fitness App")
root_window.geometry("575x500")  # Sets the window size

# Introduction and title text, advertising the app
tk.Label(root_window, text="Welcome to Zane's Fitness App!", font=("Arial", 14, "bold")).pack(pady=8)
tk.Label(
    root_window,
    text="This app allows for you to create the perfect gym schedule,\n"
         "which is scientifically proven to help you grow.",
    font=("Arial", 11)
).pack(pady=10)

# core navigation, buttons, and function of code.
tk.Button(root_window, text="Create Workout Schedule", command=create_schedule, width=40).pack(pady=4)
tk.Button(root_window, text="Choose Exercises for Muscle", command=choose_exercises_for_muscle, width=40).pack(pady=4)
tk.Button(root_window, text="View Full Schedule (JSON)", command=view_full_schedule, width=40).pack(pady=4)
tk.Button(root_window, text="Reset all Data", command=reset_all_data, width=40).pack(pady=4)
tk.Button(root_window, text="Exit", command=root_window.quit, width=40).pack(pady=8)

# Shows current state of schedule (e.g., Rest/Workout days)
output_textbox = scrolledtext.ScrolledText(
    root_window, wrap=tk.WORD, width=70, height=10, font=("Arial", 11)
)
output_textbox.pack(padx=8, pady=8, fill=tk.BOTH, expand=True)

update_output_box()  # Populate textbox with current schedule at startup

# Initiallizing the GUI and keeps it running until the user closes it
root_window.mainloop()
