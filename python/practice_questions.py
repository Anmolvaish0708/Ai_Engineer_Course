#convert the string "100" into an integer using try/except
# Handle valueError

# try:
#     num = int("100")
#     print(f"printing the value:", num)
# except ValueError as e:
#     print("Invalid input!, kindly provide integer as an input.")   
#     print("Error:", e) 

# ques 4: create a program that handles both:
# ValueError and ZeroDivisionError exceptions. The program should take two numbers as input from the user and perform division. If the user enters a non-integer value, it should handle ValueError. If the user tries to divide by zero, it should handle ZeroDivisionError.

# num1 = input("Enter the first number: ")
# num2 = input("Enter the second number: ")

# try:
#     num1 = int(num1)
#     num2 = int(num2)
#     result = num1 / num2
#     print(f"The result of division is: {result}")

# except ValueError:
#     print("Invalid input! Please enter valid integers.")

# except ZeroDivisionError:
#     print("Error: Division by zero is not allowed.")

    # create a custom exception called InvalidMarksError
    # Raise it when marks are below 0 or above 100. Handle the exception and print an appropriate message.

    # class InvalidMarksError(Exception):
    #     pass

    # try:
    #     marks = int(input("Enter the marks: "))
    #     if marks < 0 or marks > 100:
    #         raise InvalidMarksError("Invalid marks! Please enter marks between 0 and 100.")
    #     print(f"Valid marks entered: {marks}")

    # except InvalidMarksError as e:
    #     print("Error:",e)

    # create a custom exception called InvalidPasswordError.
    # Raise it if password has fewer than 8 characters. Handle the exception and print an appropriate message.

    # class InvalidPasswordError(Exception):
    #     pass

    # try:
    #     password = input("Enter your password: ")
    #     if len(password) < 8:
    #         raise InvalidPasswordError("Invalid password! Password must be at least 8 characters long.")
    #     print("Password is valid.")

    # except InvalidPasswordError as e:
    #     print("Error:", e)        


   # create a global variable score = 10
   # create a function that uses the global keyword to increase the score by 5
   # once print inside then outside the function to show that the global variable has been updated.

score = 10

def increase_score():
        global score
        score += 5
        print(f"Score inside function: {score}")

increase_score()
print(f"Score outside function: {score}")
     