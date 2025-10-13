import json 
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

# --- Load Data ---
with open('V3-5BothEandM.json', 'r') as file:
    file_data = json.load(file)

exercise_data = file_data["exercises"]
muscle_group_data = file_data["muscle_groups"]

week_day_list = [
    ['Monday', True], ['Tuesday', True], ['Wednesday', True],
    ['Thursday', True], ['Friday', True], ['Saturday', True], ['Sunday', True]
]
days_of_week = [day_entry[0] for day_entry in week_day_list]

try:
    with open("V3-5schedule.json", "r") as schedule_file:
        schedule_json_data = json.load(schedule_file)
except FileNotFoundError:
    schedule_json_data = {
        "workout_schedule": [
            {"name": day_name, "rest": True, "workout_purpose": [], "exercises": []}
            for day_name in days_of_week
        ]
    }

# ----------------- Exercise Classes -----------------
class Exercise:
    def __init__(self, exercise_name, muscle_group, sets, reps, focus_type):
        self.exercise_name = exercise_name
        self.muscle_group = muscle_group
        self.sets = sets
        self.reps = reps
        self.focus_type = focus_type

    def get_info(self):
        return f"{self.exercise_name} ({self.focus_type}) - {self.sets}x{self.reps}"

class StrengthExercise(Exercise):
    def __init__(self, exercise_name, muscle_group):
        super().__init__(exercise_name, muscle_group, 5, 6, "Strength")

class HypertrophyExercise(Exercise):
    def __init__(self, exercise_name, muscle_group):
        super().__init__(exercise_name, muscle_group, 4, 12, "Hypertrophy")

class EnduranceExercise(Exercise):
    def __init__(self, exercise_name, muscle_group):
        super().__init__(exercise_name, muscle_group, 3, 20, "Endurance")

# ----------------- Utility / JSON Sync -----------------
def map_existing_exercises_by_day(existing_schedule_data):
    return {day_entry["name"]: list(day_entry.get("exercises", []))
            for day_entry in existing_schedule_data.get("workout_schedule", [])}

def save_schedule_to_json(filename="V3-5schedule.json"):
    existing_exercise_map = map_existing_exercises_by_day(schedule_json_data)
    updated_schedule = {"workout_schedule": []}
    for day_entry in week_day_list:
        day_name = day_entry[0]
        is_rest_day = day_entry[1]
        muscle_list = day_entry[2] if len(day_entry) > 2 else []
        preserved_exercises = existing_exercise_map.get(day_name, [])
        updated_schedule["workout_schedule"].append({
            "name": day_name,
            "rest": is_rest_day,
            "workout_purpose": muscle_list,
            "exercises": [] if is_rest_day else preserved_exercises
        })
    with open(filename, "w") as schedule_file:
        json.dump(updated_schedule, schedule_file, indent=2)
    schedule_json_data.clear()
    schedule_json_data.update(updated_schedule)

def are_consecutive_days(first_day, second_day):
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return abs(day_order.index(first_day) - day_order.index(second_day)) == 1

# ----------------- Create Schedule -----------------
def create_schedule():
    day_selection_window = tk.Toplevel(root_window)
    day_selection_window.title("Select Workout Days")
    day_selection_window.geometry("450x310")

    tk.Label(day_selection_window, text="Select your workout days:",
             font=("Arial", 12, "bold")).pack(pady=5)
    tk.Label(day_selection_window, text="NOTE: You require between 2 - 5 Workout days weekly for optimal growth.\n"
    "You also cannot hit the same muscle two days in a row, \n"
    "as individual muscles need good rest between each workout.",
         font=("Arial", 10)).pack(pady=9)
    day_listbox = tk.Listbox(day_selection_window, selectmode="multiple", height=7, exportselection=False)
    for day_name in days_of_week:
        day_listbox.insert(tk.END, day_name)
    day_listbox.pack(padx=10, pady=6, fill=tk.X)

    def confirm_selected_days():
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

        for day_entry in week_day_list:
            if day_entry[0] in selected_days:
                day_entry[1] = False
            else:
                day_entry[1] = True
            if len(day_entry) > 2:
                day_entry.pop()

        day_selection_window.destroy()
        open_muscle_selection_window(selected_days)

    tk.Button(day_selection_window, text="Next ➜", command=confirm_selected_days,
              font=("Arial", 11, "bold")).pack(pady=10)

def open_muscle_selection_window(selected_days):
    muscle_assignment_window = tk.Toplevel(root_window)
    muscle_assignment_window.title("Assign Muscle Groups")
    muscle_assignment_window.geometry("800x350")

    tk.Label(muscle_assignment_window, text="Select muscle groups for each workout day:",
             font=("Arial", 12, "bold")).pack(pady=6)

    container_frame = tk.Frame(muscle_assignment_window)
    container_frame.pack(padx=8, pady=6)

    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                  'Friday', 'Saturday', 'Sunday']
    selected_days.sort(key=lambda x: day_order.index(x))

    muscle_listboxes = {}
    for column_index, day_name in enumerate(selected_days):
        day_frame = tk.LabelFrame(container_frame, text=day_name, padx=6, pady=6)
        day_frame.grid(row=0, column=column_index, padx=8, pady=6)
        listbox_muscles = tk.Listbox(day_frame, selectmode="multiple", height=7, exportselection=False)
        for muscle_name in exercise_data.keys():
            listbox_muscles.insert(tk.END, muscle_name)
        listbox_muscles.pack()
        muscle_listboxes[day_name] = listbox_muscles

    def confirm_selected_muscles():
        for selected_index, day_name in enumerate(selected_days):
            chosen_muscles = [muscle_listboxes[day_name].get(i)
                              for i in muscle_listboxes[day_name].curselection()]
            if not chosen_muscles:
                messagebox.showerror("Error", f"Select at least one muscle group for {day_name}.")
                return

            if selected_index > 0:
                previous_day = selected_days[selected_index - 1]
                if are_consecutive_days(previous_day, day_name):
                    prev_muscles = [muscle_listboxes[previous_day].get(i)
                                    for i in muscle_listboxes[previous_day].curselection()]
                    overlapping_muscles = set(prev_muscles) & set(chosen_muscles)
                    if overlapping_muscles:
                        messagebox.showwarning(
                            "Warning",
                            f"⚠️ You can't train these on consecutive days ({previous_day} → {day_name}): {', '.join(overlapping_muscles)}"
                        )
                        return

            for day_entry in week_day_list:
                if day_entry[0] == day_name:
                    if len(day_entry) > 2:
                        day_entry[2] = chosen_muscles
                    else:
                        day_entry.append(chosen_muscles)

        save_schedule_to_json()
        update_output_box()
        messagebox.showinfo("Schedule", "✅ Schedule created successfully!")
        muscle_assignment_window.destroy()

    tk.Button(muscle_assignment_window, text="Confirm Schedule ✅", command=confirm_selected_muscles,
              font=("Arial", 11, "bold")).pack(pady=10)

# ----------------- Exercise Selection -----------------
def choose_exercises_for_muscle():
    muscle_choice_window = tk.Toplevel(root_window)
    muscle_choice_window.title("Choose Exercises for a Muscle")
    tk.Label(muscle_choice_window, text="Select a muscle group:", font=("Arial", 12, "bold")).pack(pady=4)

    muscle_listbox = tk.Listbox(muscle_choice_window, height=10, exportselection=False)
    for muscle_name in muscle_group_data.keys():
        muscle_listbox.insert(tk.END, muscle_name)
    muscle_listbox.pack(padx=10, pady=4, fill=tk.X)

    def confirm_muscle_selection():
        if not muscle_listbox.curselection():
            messagebox.showerror("Error", "Please select a muscle group.")
            return
        selected_muscle = muscle_listbox.get(muscle_listbox.curselection())
        muscle_choice_window.destroy()
        open_exercise_selection_window(selected_muscle)

    tk.Button(muscle_choice_window, text="Next ➜", command=confirm_muscle_selection,
              font=("Arial", 11, "bold")).pack(pady=8)

def open_exercise_selection_window(selected_muscle):
    if selected_muscle not in exercise_data:
        messagebox.showerror("Error", f"No exercises found for {selected_muscle}.")
        return
    exercise_selection_window = tk.Toplevel(root_window)
    exercise_selection_window.title(f"Select Exercises for {selected_muscle}")

    tk.Label(exercise_selection_window, text=f"Exercises for {selected_muscle}:",
             font=("Arial", 12, "bold")).pack(pady=5)
    tk.Label(exercise_selection_window, text="These are the most effective, research-backed exercises for your target muscle.\n" \
        "Scientifically proven to provide the most muscle growth.",
         font=("Arial", 11)).pack(pady=10)
    exercise_frame = tk.Frame(exercise_selection_window)
    exercise_frame.pack(pady=5, padx=10)

    exercise_check_vars = []
    for exercise_name in exercise_data[selected_muscle]:
        is_selected_var = tk.IntVar()
        tk.Checkbutton(exercise_frame, text=exercise_name, variable=is_selected_var).pack(anchor="w")
        exercise_check_vars.append((exercise_name, is_selected_var))

    def confirm_exercise_selection():
        selected_exercises = [exercise_name for exercise_name, var in exercise_check_vars if var.get() == 1]
        if not selected_exercises:
            messagebox.showerror("Error", "Please select at least one exercise.")
            return
        exercise_selection_window.destroy()
        open_intensity_selection_window(selected_muscle, selected_exercises)

    tk.Button(exercise_selection_window, text="Next ➜", command=confirm_exercise_selection,
              font=("Arial", 11, "bold")).pack(pady=8)

def open_intensity_selection_window(selected_muscle, selected_exercises):
    intensity_window = tk.Toplevel(root_window)
    intensity_window.title(f"Set Intensities for {selected_muscle}")

    tk.Label(intensity_window, text=f"Select intensity for each exercise:",
             font=("Arial", 12, "bold")).pack(pady=5)
    tk.Label(intensity_window, text="Strength: 5 sets of 6 reps. This intensity is using heavy weight with shorter sets to focus on explosiveness and strength gain\n"
    "Hypertrophy: 4 sets of 12 reps. This intensity is designed to challenge your muscles with an ideal weight to build the most muscle.\n" 
    "Endurance: 3 sets of 20+ reps. This intensity is using much lighter weight but demands a very high rep range, best for athletes and overall endurance.",
             font=("Arial", 11)).pack(pady=6)
    intensity_frame = tk.Frame(intensity_window)
    intensity_frame.pack(padx=10, pady=5)

    exercise_intensity_boxes = {}
    for exercise_name in selected_exercises:
        row_frame = tk.Frame(intensity_frame)
        row_frame.pack(fill="x", pady=2)
        tk.Label(row_frame, text=exercise_name, width=30, anchor="w").pack(side="left")
        intensity_combobox = ttk.Combobox(row_frame,
                                          values=["Strength", "Hypertrophy", "Endurance"],
                                          state="readonly", width=15)
        intensity_combobox.set("Hypertrophy")
        intensity_combobox.pack(side="left", padx=5)
        exercise_intensity_boxes[exercise_name] = intensity_combobox

    def confirm_intensity_selection():
        exercise_objects = []
        for exercise_name, combo_box in exercise_intensity_boxes.items():
            focus_type = combo_box.get()
            if focus_type == "Strength":
                exercise_objects.append(StrengthExercise(exercise_name, selected_muscle))
            elif focus_type == "Endurance":
                exercise_objects.append(EnduranceExercise(exercise_name, selected_muscle))
            else:
                exercise_objects.append(HypertrophyExercise(exercise_name, selected_muscle))

        for day_entry in schedule_json_data["workout_schedule"]:
            if selected_muscle in day_entry["workout_purpose"]:
                for exercise_obj in exercise_objects:
                    exercise_info = exercise_obj.get_info()
                    if exercise_info not in day_entry["exercises"]:
                        day_entry["exercises"].append(exercise_info)

        save_schedule_to_json()
        update_output_box()
        messagebox.showinfo("Success", f"✅ Added {len(exercise_objects)} exercise(s) for {selected_muscle}.")
        intensity_window.destroy()

    tk.Button(intensity_window, text="Add Exercises ✅",
              command=confirm_intensity_selection, font=("Arial", 11, "bold")).pack(pady=10)

# ----------------- Helpers -----------------
def reset_all_data():
    if not messagebox.askyesno("Confirm Reset", "Reset all data (clear JSON and in-memory schedule)?"):
        return
    for index in range(len(week_day_list)):
        week_day_list[index] = [days_of_week[index], True]
    empty_schedule = {
        "workout_schedule": [
            {"name": day_name, "rest": True, "workout_purpose": [], "exercises": []}
            for day_name in days_of_week
        ]
    }
    with open("V3-5schedule.json", "w") as schedule_file:
        json.dump(empty_schedule, schedule_file, indent=2)
    schedule_json_data.clear()
    schedule_json_data.update(empty_schedule)
    update_output_box()
    messagebox.showinfo("Reset", "✅ All data has been reset.")

def view_full_schedule(filename="V3-5schedule.json"):
    try:
        with open(filename, "r") as schedule_file:
            json_data = json.load(schedule_file)
        summary_text = ""
        for day_entry in json_data["workout_schedule"]:
            day_status = "Rest Day" if day_entry["rest"] else "Workout Day"
            muscle_string = ", ".join(day_entry["workout_purpose"]) if day_entry["workout_purpose"] else "None"
            exercise_string = ", ".join(day_entry["exercises"]) if day_entry["exercises"] else "None"
            summary_text += f"\n{day_entry['name']}: {day_status}\n"
            summary_text += f"  Muscles: {muscle_string}\n  Exercises: {exercise_string}\n"
        show_text_window("Full Schedule", summary_text)
    except FileNotFoundError:
        messagebox.showerror("Error", "Schedule file not found.")

def show_text_window(window_title, window_content):
    text_window = tk.Toplevel(root_window)
    text_window.title(window_title)
    text_area_widget = scrolledtext.ScrolledText(text_window, wrap=tk.WORD, width=60, height=20, font=("Arial", 11))
    text_area_widget.insert(tk.END, window_content)
    text_area_widget.config(state="disabled")
    text_area_widget.pack(padx=8, pady=8)

def update_output_box():
    output_textbox.config(state="normal")
    output_textbox.delete(1.0, tk.END)
    summary_text = ""
    for day_entry in week_day_list:
        day_name, is_rest, *muscles = day_entry
        if is_rest:
            summary_text += f"{day_name}: Rest Day\n"
        else:
            summary_text += f"{day_name}: Workout Day → {', '.join(muscles[0]) if muscles else '(none)'}\n"
    output_textbox.insert(tk.END, summary_text)
    output_textbox.config(state="disabled")

# ----------------- GUI -----------------
root_window = tk.Tk()
root_window.title("Zane's Fitness App")
root_window.geometry("575x500")

tk.Label(root_window, text="Welcome to Zane's Fitness App!", font=("Arial", 14, "bold")).pack(pady=8)
tk.Label(root_window, text="This app allows for you to create the perfect gym schedule,\nwhich is scientifically proven to help you grow.",
         font=("Arial", 11)).pack(pady=10)
tk.Button(root_window, text="Create Workout Schedule", command=create_schedule, width=40).pack(pady=4)
tk.Button(root_window, text="Choose Exercises for Muscle", command=choose_exercises_for_muscle, width=40).pack(pady=4)
tk.Button(root_window, text="View Full Schedule (JSON)", command=view_full_schedule, width=40).pack(pady=4)
tk.Button(root_window, text="Reset all Data", command=reset_all_data, width=40).pack(pady=4)
tk.Button(root_window, text="Exit", command=root_window.quit, width=40).pack(pady=8)

output_textbox = scrolledtext.ScrolledText(root_window, wrap=tk.WORD, width=70, height=10, font=("Arial", 11))
output_textbox.pack(padx=8, pady=8, fill=tk.BOTH, expand=True)
update_output_box()

root_window.mainloop()
