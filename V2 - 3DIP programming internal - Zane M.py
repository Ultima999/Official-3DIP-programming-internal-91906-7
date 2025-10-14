import json

# Loads the dictionary of muscle groups and sub-muscles from file
with open('V2muscle_groups.json', 'r') as fileM:
    dataM = json.load(fileM)
muscle_groups = dataM["muscle_groups"]

# Loads a separate JSON file containing exercises linked to each muscle
with open('V2exercises.json', 'r') as fileE:
    dataE = json.load(fileE)
exercises = dataE["exercises"]

# Initialize a list representing all days in a week
# Each entry: [day_name, True/False], where True = Rest Day, False = Workout Day
day_list = [
    ['monday', True], ['tuesday', True], ['wednesday', True],
    ['thursday', True], ['friday', True], ['saturday', True], ['sunday', True]
]
chosen_day_list = []  # Stores all chosen workout days for the week

# Convenience lists to separate days and their statuses
workoutday = [day[0] for day in day_list]
rest = [day[1] for day in day_list]

def find_exercises_by_muscle(muscle_name):
    #Returns a formatted string of recommended exercises for a chosen muscle group.
    #Uses the JSON exercise dataset to match user input with stored values.

    if muscle_name in exercises:
        exercise_list = exercises[muscle_name]

        # If only one exercise exists, print it directly
        if len(exercise_list) == 1:
            return f"For {muscle_name}, a recommended exercise is: {exercise_list[0]}."
        else:
            # Otherwise, join all exercise names neatly with commas
            other_exercises = ", ".join(exercise_list[:-1])
            last_exercise = exercise_list[-1]
            return f"For {muscle_name}, you can do: {other_exercises}, and {last_exercise}."
    else:
        # Handles invalid or missing muscle inputs
        return f"Sorry, no exercises found for '{muscle_name}'. Please try another muscle group."

def describe_muscle_hit(muscle_name):
    # Returns a readable description of which sub-muscles are targeted
    # when training a specific main muscle group.

    sub_muscles = muscle_groups.get(muscle_name, [])  # Retrieve list of sub-muscles if available

    # Case 1: No sub-muscles exist
    if not sub_muscles:
        return f"This hits {muscle_name}."

    # Case 2: One sub-muscle found
    if len(sub_muscles) == 1:
        return f"This hits {muscle_name}, specifically the {sub_muscles[0]}."

    # Case 3: Multiple sub-muscles → join all but the last with commas
    last = sub_muscles[-1]
    others = ", ".join(sub_muscles[:-1])
    return f"This hits {muscle_name}, specifically the {others}, and {last}."

def view_week():
    # Displays each day of the week and whether it's a workout or rest day.
    # Uses the current 'day_list' values to print results dynamically.

    for day in day_list:
        weekday_name, rest = day
        if rest:
            print(f"{weekday_name.title()}: Rest Day")
        else:
            print(f"{weekday_name.title()}: Workout Day")

def create_schedule():
    # Allows the user to select which days they want to work out.
    #Updates the 'day_list' and displays the updated schedule.

    days_of_the_week = [day[0] for day in day_list]

    while True:
        # Show available days to the user
        print("Days of the week:", days_of_the_week)
        day_input = input("Which days do you want to work out? (Separate days with spaces): ").lower()
        chosen_days = [day.strip() for day in day_input.split(' ')]

        # Validation: ensure all inputted days exist in the week
        if all(day in days_of_the_week for day in chosen_days):
            for day in day_list:
                if day[0] in chosen_days:
                    day[1] = False  # Mark as workout day
                    chosen_day_list.append(day[0])
            view_week()  # Display the updated schedule
            break
        else:
            # Error message for invalid or misspelled days
            print("Invalid input \nPlease enter a valid day from the week.")

print("Welcome to Zane's Fitness App! We are here to help you grow and improve yourself.")

# The interactive menu repeatedly prompts user for actions until exit (option 9)
while True:
    option = int(input(
        "\nHow would you like to improve yourself today? "
        "\nType 1 to create your workout schedule "
        "\nType 2 to view your workout schedule "
        "\nType 3 to find exercises for a muscle group you are interested in "
        "\nType 4 to describe the sub muscles in a muscle group you are interested in "
        "\n:"
    ))
# options for user to run the functions
    if option == 1:
        create_schedule()
    if option == 2:
        view_week()
    if option == 3:
        muscle_name = input("Which muscle group are you interested in? : ").capitalize()
        print(find_exercises_by_muscle(muscle_name))
    if option == 4:
        muscle_name = input("Which muscle group are you interested in? : ").capitalize()
        print(describe_muscle_hit(muscle_name))
    elif option == 9:
        print("Thank you for using this program! Have a great day :D")
        break
