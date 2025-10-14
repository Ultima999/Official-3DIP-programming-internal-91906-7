import json

# Loads Data from the JSON file containing both exercise and muscle group data from an external file
with open('V3-5BothEandM.json', 'r') as file:
    data = json.load(file)

# Loads Data from the JSON file template which attempts to open an existing saved schedule; otherwise errors are handled later
with open("V3-5schedule.json", "r") as f:
    data_schedule = json.load(f)

# Extract exercise and muscle data from JSON structure
exercises = data["exercises"]
muscle_groups = data["muscle_groups"]

# Initialize list for each day of the week: [Day Name, Rest/Workout Status]
day_list = [
    ['Monday', True], ['Tuesday', True], ['Wednesday', True],
    ['Thursday', True], ['Friday', True], ['Saturday', True], ['Sunday', True]
]

# Additional tracking lists for user selections
chosen_day_list = []                         # Stores which days are selected as workout days
days_of_the_week = [day[0] for day in day_list]  # Extracts only day names for printing and validation
rest = [day[1] for day in day_list]              # Extracts rest day statuses (True/False)

def find_exercises_by_muscle(muscle_name):
    # Finds and returns exercises for a given muscle group.
    # Uses both exercises.json and muscle_groups.json for combined description output.

    while True:
        # Check if the given muscle exists in the JSON file
        if muscle_name in exercises:
            # Get exercise list and related sub-muscle data
            exercise_list = exercises[muscle_name]
            sub_muscles = muscle_groups.get(muscle_name, [])
            last_sub_muscle = sub_muscles[-1]
            others_sub_muscle = ", ".join(sub_muscles[:-1])

            # If there's only one exercise, display it directly
            if len(exercise_list) == 1:
                return f"For {muscle_name}, a recommended exercise is: {exercise_list[0]}. " \
                       f"This will specifically hit the {others_sub_muscle} and the {last_sub_muscle}."
            else:
                # Otherwise, list all available exercises neatly
                other_exercises = ", ".join(exercise_list[:-1])
                last_exercise = exercise_list[-1]
                return f"For {muscle_name}, you can do: {other_exercises}, and {last_exercise}. " \
                       f"These will specifically hit the {others_sub_muscle} and the {last_sub_muscle}."
        else:
            # Handles case where an invalid or missing muscle is entered
            return f"Sorry, no exercises found for '{muscle_name}'. Please try another muscle group."

def create_schedule():
    # Allows the user to create a weekly workout schedule through text-based input.
    # Collects chosen days, validates them, and assigns muscles to those days.
    
    while True:
        print("Days of the week:", ", ".join(days_of_the_week))
        day_input = input("Which days do you want to work out? (Separate days with commas): ").title()
        chosen_days = [day.strip() for day in day_input.split(',') if day.strip()]

        # Displays all available muscle groups from JSON
        print("\nHere are all the main muscle groups in the human body:")
        for muscles in muscle_groups.keys():
            print(f"- {muscles}")

        # Validate if all chosen days exist in the list of valid weekday names
        if all(day in days_of_the_week for day in chosen_days):
            for day in day_list:
                if day[0] in chosen_days:
                    day[1] = False  # Mark the day as a workout day
                    if day[0] not in chosen_day_list:
                        chosen_day_list.append(day[0])

                    # Ask user which muscles they want to train on that day
                    muscle_input = input(f"What muscle groups do you want to train on {day[0]}? (Separate with commas): ").title()
                    muscle_day = [m.strip() for m in muscle_input.split(",") if m.strip()]
                    day.append(muscle_day)
                else:
                    day[1] = True  # Marks non-selected days as rest days
            break
        else:
            # Error message for invalid input
            print("❌ Invalid input. Please enter valid days from the week.")

    # Save the completed schedule to a JSON file
    save_schedule_to_json()

    print("\nYour workout schedule has been updated!\n")
    view_week()  # Display weekly summary once created

def view_week():
    # Displays the current weekly schedule directly in the console.
    # Prints which days are workout days and which are rest days.

    for day in day_list:
        weekday_name, rest, *muscles = day
        if rest:
            print(f"{weekday_name.title()}: Rest Day")
        else:
            if muscles:
                print(f"{weekday_name.title()}: Workout Day → {', '.join(muscles[0])}")

def save_schedule_to_json(filename="V3-5schedule.json"):
    # Saves the schedule from day_list into the schedule.json file.
    # Each entry includes: day name, rest status, chosen muscles, and empty exercises.
    
    data_schedule = {"workout_schedule": []}
    for day in day_list:
        day_name = day[0]
        rest_status = day[1]
        muscle_day = day[2] if len(day) > 2 else []

        # Append a structured JSON object for each day
        data_schedule["workout_schedule"].append({
            "name": day_name,
            "rest": rest_status,
            "workout_purpose": muscle_day,
            "exercises": []
        })

    # Write formatted JSON file with indentation for readability
    with open(filename, "w") as f:
        json.dump(data_schedule, f, indent=2)
    print("✅ Schedule saved in JSON!")

def view_full_schedule(filename="V3-5schedule.json"):
    # Opens and displays the entire workout schedule from JSON file.
    # This includes all days, their workout purposes, and exercises.
   
    try:
        with open(filename, "r") as f:
            data_schedule = json.load(f)

        for day in data_schedule["workout_schedule"]:
            status = "Rest Day" if day["rest"] else "Workout Day"
            purposes = ", ".join(day["workout_purpose"]) if day["workout_purpose"] else "None"
            exercises = ", ".join(day["exercises"]) if day["exercises"] else "None"

            # Output a clean and readable weekly summary
            print(f"\n{day['name'].title()}: {status}")
            print(f"  Muscles: {purposes}")
            print(f"  Exercises: {exercises}")

        print("✅ Schedule loaded successfully!")

    except FileNotFoundError:
        # Error handling if JSON file not found
        print(f"❌ {filename} not found. Please create or upload a schedule first.")

print("Welcome to Zane's Fitness App! We are here to help you grow and improve yourself.")

# The program remains active until user chooses to exit (option 9)
while True:
    option = int(input(
        "\nHow would you like to improve yourself today? "
        "\nType 1 to create your workout schedule "
        "\nType 2 view your workout schedule "
        "\nType 3 to find exercises for a specific muscle group "
        "\nType 4 to update ths schedule to your dedicated JSON file "
        "\nType 5 to view your full schedule on JSON "
        "\nType 9 to end the program "
        "\n:"
    ))

    # Program Home screen, equivalent of a home page with every option.
    if option == 1:
        create_schedule()
    if option == 2:
        view_week()
    if option == 3:
        print("Here are all the main muscle groups in the human body.\n")
        for muscles in muscle_groups.keys():
            print(f"- {muscles}")
        muscle_name = input("What muscle group do you want to learn exercises for? \n:").title()
        print(find_exercises_by_muscle(muscle_name))
    if option == 4:
        print(save_schedule_to_json())
    if option == 5:
        print(view_full_schedule())
    elif option == 9:
        print("Thank you for using this program! Have a great day :D")
        break
