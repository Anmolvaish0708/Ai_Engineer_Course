# try:
#     num1 = int(input("Please enter your age: "))
#     print(num1)
# except ValueError:
#     print("Try block could not be executed")

# print("This is the final important logic")





# try:
#     number = 10
#     divisor = "Vikash"

#     result = number / divisor
#     print(result)   

# except TypeError:
#     print("Both values have to be numbers.")
# except ZeroDivisionError:
#     print("Invalid value, cant divide by zero.")



# try:
#     num1 = int("50")
# except ValueError:
#     print("Invalid number.")
# else:
#     print("Conversion successful.")
#     print(num1)


# try:
#     num1 = int("25A")
#     print(num1)
# except ValueError:
#     print("Invalid number")
# finally:
#     print("This block always runs, no matter what")


# try:
#     number = int("abc")

# except ValueError as error:
#     print("An error occurred:")
#     print(error)

# print("I want to to be printed.")


# defining custom error

# class InsufficientBalanceError(Exception):
#     pass

# balance = 500
# withdraw_amount = 1000

# try:
#     if withdraw_amount > balance:
#         raise InsufficientBalanceError(
#             "Custom Error: Withdrawal amount is greater than the balance."
#         )
#     print("Withdraw successful.")

# except InsufficientBalanceError as error:
#     print("Error: ", error)
# print("End to end execution successful.")    



#local vs global variable

# def show_name():
#     name = "Rahul"
#     print(name)

# show_name()
# print(name)




# course = "GenAI"

# def show_course():
#     print(course)

# show_course()



# name = "Rahul"

# def change_name():
#     global name
#     name = "Priya"
#     print(f"Inside function: {name}")

# change_name()
# print(f"Outside function: {name}")

#file handling

# with open("students.txt", "w") as file:
#     file.write("Rahul\n")
#     file.write("Priya\n")
#     file.write("Amit\n")


# with open("students.txt", "r") as file:
#     content = file.read()

# print(content)

# with open("students.txt", "a") as file:
#     file.write("Rahul got his memship reviewed.\n")
#     file.write("Priya has resigned from the organization.\n")
#     file.write("Amit is on leave.\n")



# my_students = ["Sachin", "Prateek", "Rahul"]

# with open("students1.txt", "w") as file:
#     for student in my_students:
#         file.write(student + "\n")

#in built libraries

# import math

# print(math.sqrt(9))
# print(math.ceil(4.2))
# print(math.floor(4.2))

# import random  

# print(random.randint(11, 30))

# from datetime import datetime

# current_time = datetime.now()
# print("Current date and time: ", current_time)

# __name__ == "__main__"

# def myfunc1():
#     print("Hi, my name is Vikash")

# def myfunc2():
#     print("Vikash likes pixar movies")

# def myfunc3():
#     print("Vikash likes to eat momos on weekend.")

# print("Going to my neighbor...")
# print(__name__)

# if __name__ == "__main__":
#     myfunc1()
#     myfunc2()
#     myfunc3()

# practice questions

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
     