from numpy import random
while True :
    print("Enter 'y' for output !")
    print("Enter 'q' to quit !")
    a = input()
    try:
        if a=="q":
            print("Thanks for playing !")
            break
        if a=="y":
            print(random.randint(1,6))
    except ValueError:
        print("Please enter Valid input !")
    
