import schedule
import time


def periodic_task():
    print("This task happens periodically. \n Press 'Ctrl + C' to stop the periodic backup")

number = 0
while True:
    user_input = input("Please enter how often (in seconds) the copy should be performed: ")
    try:
        number = int(user_input)
        if number > 0:
            break  # Exit the loop if the input is a positive integer
        else:
            print("Please enter a positive integer.")
    except ValueError:
        print("Please enter a valid integer.")
            

schedule.every(number).seconds.do(periodic_task)
print(number)


while True:
    schedule.run_pending()
    time.sleep(1)  # Optional: sleep to reduce CPU usage