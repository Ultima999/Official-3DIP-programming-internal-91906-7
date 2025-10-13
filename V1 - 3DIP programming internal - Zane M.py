day_list = [['monday', True], ['tuesday', True], ['wednesday', True], ['thursday', True], ['friday', True], ['saturday', True], ['sunday', True]]
chosen_day_list = []

workoutday = [day[0] for day in day_list]
rest = [day[1] for day in day_list]

def view_week():
    for day in day_list:
        weekday_name, rest = day
        if rest:
            print(f"{weekday_name}: Rest Day")
        else:
            print(f"{weekday_name}: Workout Day")

def create_schedule():
    days_of_the_week = [day[0] for day in day_list]
    
    while True:
        print("Days of the week:", days_of_the_week)
        day_input = input("Which days do you want to work out? (Separate days with spaces): ").lower()
        chosen_days = [day.strip() for day in day_input.split(' ')]

        if all(day in days_of_the_week for day in chosen_days):
            for day in day_list:
                if day[0] in chosen_days:
                    day[1] = False 
                    chosen_day_list.append(day[0])
            view_week()
            break
        else:
            print("Invalid input \nPlease enter a valid day from the week.")

print("Welcome to Zane's Fitness App! We are here to help you grow and improve yourself.")

while True:
    option = int(input("\nHow would you like to improve yourself today? \nType 1 to create or view your workout schedule \nType 9 to end the program \n:"))
    if option == 1:
        create_schedule()
    elif option == 9:
        print("Thank you for using this program! Have a great day :D")
        break