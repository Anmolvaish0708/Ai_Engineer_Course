# Question 1:

# Create a program that
# 1. Opens a file in write mode"names.txt"
# 2. Writes 5 names (one per line) entered by the user
# 3. Then opens the same file in read mode and prints all names

# with open("names.txt", "w") as file:
#     for i in range(5):
#         name = input(f"Enter Name {i+1}: ")
#         file.write(name + "\n")

# with open("names.txt", "r") as file:
#     content = file.read()
# print(content)  

# Question 2:

# Create a program that:
# 1. Has a list of numbers: [5, 10, 15, 20, 25]
# 2. Uses a list comprehension to create a new list with only numbers greater
# than 15
# 3. Prints the new list

# numbers = [5, 10, 15, 20, 25]
# new_list = [num for num in numbers if num > 15]
# print(new_list)

# Question 3:

#  Create a Python dictionary of 3 cities and their populations. Save it to
# "cities.json"
# 1. Then load the JSON and print each city and its population.
# 2. Ask the user for a new city & its population - update this info in the json
# file

# import json

# dic = {
#     "New York": 8419600,
#     "Los Angeles": 3980400,
#     "Chicago": 2716000
# }

# with open("cities.json", "w") as file:
#     json.dump(dic, file, indent=4)

# with open("cities.json", "r") as file:
#     data = json.load(file)
#     # print(data)/
#     for city, population in data.items():
#         print(f"{city}: {population}")

# new_city = input("Enter a new city: ")
# new_population = int(input(f"Enter the population of {new_city}: "))

# data[new_city] = new_population
# with open("cities.json", "w") as file:
#     json.dump(data, file, indent=4)

# Question 4:

#  Write a program that tries to open "data.txt" in read mode. If the file does not
# exist, catch the exception and print "File not found!".

# try:
#     with open("data.txt", "r") as file:
#         content = file.read()
#         print(content)
# except FileNotFoundError as err:
#     print("File not found!")
#     print("Error:", err)       


# Question 5:

# Given a list, print all elements that appear more than once in the list

# numbers = [1, 2, 3, 2, 4, 5, 3, 6]

# seen = set()
# duplicates = set()

# for num in numbers:
#     if num in seen:
#         duplicates.add(num)
#     else:
#         seen.add(num)

# print("Elements that appear more than once:", list(duplicates))


# Question 6:

# Ask the user for a string and print:
# • All unique characters
# • The count of unique characters

# user_string = input("Enter a string: ")
# unique_characters = set(user_string)
# print("Unique characters:", unique_characters)
# print("Count of unique characters:", len(unique_characters))

#Question 7:
#Write a program to check whether two lists share no common elements.

numbers1 = [1, 2, 3, 4, 5]
numbers2 = [3, 7, 8, 9, 10]

if not set(numbers1) & set(numbers2):
    print("The two lists share no common elements.")
else:
    print("The two lists have common elements.")    

