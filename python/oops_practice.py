# # mini-project 1:

# class BankAccount:
#     bank_name = "State Bank of India"
#     total_accounts = 0

#     def __init__(self, account_holder, balance=0):
#         self.account_holder = account_holder
#         self.__balance = balance
#         BankAccount.total_accounts += 1

#     def Deposit(self, amount):
#         if amount > 0:
#             self.__balance += amount
#             print(f"Rs.{amount}/- deposited successfully.")

#     def Withdraw(self, amount):
#         if amount <= self.__balance:
#             self.__balance -= amount
#             print(f"Rs.{amount}/- withdrawn successfully.")

#     def Display_Balance(self):
#         print(f"{self.account_holder} has Rs.{self.__balance}/- in the account.")


# acc1 = BankAccount("Rahul", 10000)
# acc1.Deposit(5000)
# acc1.Withdraw(2000)

# acc2 = BankAccount("Omkar", 20000)
# acc2.Deposit(50000)
# acc2.Withdraw(10000)

# acc3 = BankAccount("Ramesh", 30000)
# acc3.Deposit(10000)
# acc3.Withdraw(5000)

# print(f"Total accounts created: {BankAccount.total_accounts}")


# mini-project 2:

# class Employee:
#     company_name = "OpenAI"
#     annual_bonus_percent = 10

#     def __init__(self, name, salary):
#         self.name = name
#         self.__salary = salary

#     def annual_salary_with_bonus(self):
#         bonus = (self.__salary * Employee.annual_bonus_percent) / 100
#         return self.__salary + bonus

    
#     @classmethod
#     def set_bonus_percent(cls, new_bonus_percent):
#         Employee.annual_bonus_percent = new_bonus_percent
#         print(f"Annual bonus percent updated to {new_bonus_percent}%.")


#     @classmethod
#     def from_string(cls, emp_str):
#         # it is an alternative constructor that allows creating an Employee object from a string representation
#         name, salary = emp_str.split("-")
#         return cls(name = name, salary = int(salary))

#     @staticmethod
#     def is_valid_salary(salary):
#         return salary > 0

# emp1 = Employee("Rahul", 500000)
# emp2 = Employee("Anmol", 1200000)
# emp3 = Employee.from_string("Omkar-800000")


# Employee.set_bonus_percent(15)

# print(emp1.annual_salary_with_bonus())   # 15% bonus -> 575000.0
# print(emp2.annual_salary_with_bonus())   # 15% bonus -> 1380000.0
# print(emp3.annual_salary_with_bonus())

# print(Employee.is_valid_salary(-100000))


# mini-project 3:

# class User:

#     def __init__(self, username, age, email):
#         self.__username = username
#         self.age = age
#         self.email = email

#     @property
#     def age(self):
#         return self.__age


#     @age.setter
#     def age(self, new_age):

#         if (new_age < 0 or new_age > 120):
#             raise ValueError(f"Invalid age: {new_age}. Must be between 0 and 120.")
#         else:
#             self.__age = new_age  


#     @property
#     def email(self):
#         return self.__email          


#     @email.setter
#     def email(self, email):

#         if "@" not in email:
#             raise ValueError(f"Invalid email: {email}")
#         else:
#             self.__email = email    

#     def display_profile(self):
#         print(f"{self.__username} is {self.__age} yrs old having mail id {self.__email}")        


# user = User("Anmol", 25, "anmolvaishnaw0708@gmail.com")
# user.display_profile()

# try:
#     bad_user = User("Test", 200, "abc@gmail.com")
# except ValueError as e:
#     print("Failed to create user:", e)

# mini-project 4:(Abstraction + polymorphism)

from abc import ABC, abstractmethod

class Shape(ABC):

    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def parimeter(self):
        pass

    def display_name(self):
        print("This is a shape.")


class Rectangle(Shape):
     
    def __init__(self,length,width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

    def parimeter(self):
        return 2 * (self.length + self.width)

class Circle(Shape):

    def __init__(self, radius):
          self.radius = radius

    def area(self):
        return 3.14 * self.radius * self.radius

    def parimeter(self):
        return 2*3.14*self.radius

class Triangle(Shape):

    def __init__(self, base, height, s1, s2, s3):
        self.base = base
        self.height = height
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3

    def area(self):
        return 0.5*self.base*self.height

    def parimeter(self):
        return self.s1 + self.s2 + self.s3   

# shape = Shape()         # ERROR! Can't instantiate abstract class

# Objects banao
rect = Rectangle(10, 5)
circle = Circle(7)
triangle = Triangle(6, 4, 5, 5, 6)

shapes = [rect, circle, triangle]

for shape in shapes:
    shape.display_name()   # ye Shape (parent) se inherit kiya method hai, sabke paas hai
    print(f"Area: {shape.area()}")
    print(f"Perimeter: {shape.parimeter()}")
    print("-" * 30)
