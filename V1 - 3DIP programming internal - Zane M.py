# Initialise base data structure for weekly schedule
# Each entry contains a day of the week and a Boolean value:
# True = Rest Day (by default), False = Workout Day
day_list = [
    ['monday', True], ['tuesday', True], ['wednesday', True],
    ['thursday', True], ['friday', True], ['saturday', True], ['sunday', True]
]

# Stores all days that the user later chooses for workouts
chosen_day_list = []

# Convenience lists: one for all weekday names, another for rest statuses
workoutday = [day[0] for day in day_list]
rest = [day[1] for day in day_list]

def view_week():
    # Displays each day of the week and whether it is a workout or rest day.
    # Reads directly from the 'day_list' data structure.
    
    for day in day_list:
        weekday_name, rest = day  # Unpack the list for clarity
        if rest:
            print(f"{weekday_name}: Rest Day")
        else:
            print(f"{weekday_name}: Workout Day")


# Allows the user to choose which days of the week they want to work out.
def create_schedule():
    # Extract just the day names for validation purposes
    # The input is validated, and selected days are marked as workout days.
    
    days_of_the_week = [day[0] for day in day_list]

    while True:
        # Print available days for reference
        print("Days of the week:", days_of_the_week)

        # Get user input and convert everything to lowercase for consistency
        day_input = input("Which days do you want to work out? (Separate days with spaces): ").lower()
        chosen_days = [day.strip() for day in day_input.split(' ')]

        # Validate that every entered day actually exists
        if all(day in days_of_the_week for day in chosen_days):
            for day in day_list:
                # Mark selected days as workout days
                if day[0] in chosen_days:
                    day[1] = False
                    chosen_day_list.append(day[0])
            view_week()  # Show the updated schedule immediately
            break
        else:
            # Handle typos or invalid day entries
            print("Invalid input \nPlease enter a valid day from the week.")


print("Welcome to Zane's Fitness App! We are here to help you grow and improve yourself.")

# The program runs continuously until the user chooses to exit.
while True:
    option = int(input(
        "\nHow would you like to improve yourself today? "
        "\nType 1 to create or view your workout schedule "
        "\nType 9 to end the program "
        "\n:"
    ))

    if option == 1:
        create_schedule()
    elif option == 9:
        print("Thank you for using this program! Have a great day :D")
        break
