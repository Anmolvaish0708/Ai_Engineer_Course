class student:
    def __init__(self, name, roll_no, marks):
        self.name = name
        self.roll_no = roll_no
        self.marks = marks

    def total_marks(self):
        return sum(self.marks)  

    def percentage(self):
        total = self.total_marks()
        return (total / (len(self.marks) * 100)) * 100  

    def display_info(self):
        print(f"Name: {self.name}")
        print(f"Roll No: {self.roll_no}")
        print(f"Marks: {self.marks}")
        print(f"Total Marks: {self.total_marks()}")
        print(f"Percentage: {self.percentage():.2f}%")

s1 = student("Alice", 101, [85, 90, 78])
s1.display_info()        

# class student:

#     # magic/dunder method -> Constructor -> __init__
#     def __init__(self, arg_name, arg_age, arg_course):
#         self.name = arg_name
#         self.age = arg_age
#         self.course = arg_course

#     def introduce(self):
#         print(f"Hello, My name is {self.name}. I am a student.")

    
#     # Student: Harsh | Age: xx | Course: xxx
#     def __str__(self):
#         return f"Student: {self.name} | Age: {self.age} | Course: {self.course}"
    
#     def __len__(self):
#         return len(self.name)

# student1 = student("Harsh", 25, "GenAI")
# str_value = "GenAI"
# num1 = 100
# bool1 = True


# print(bool1)
# print(num1)
# print(str_value)
# print(student1)


# print(f"Number of characters in str_value: {len(str_value)}")
# print(f"Number of characters in student object name: {len(student1)}")

# class BankAccount:

#     def __init__(self, owner, balance) -> None:
#         self.owner = owner
#         self.__balance = balance

#     def show_balance(self):
#         print(f"Balance: Rs{self.__balance}/-")

# acc1 = BankAccount("Rahul", 10000)

# print(acc1.owner)
# print(acc1._BankAccount__balance)
# # acc1.show_balance()
# # acc1.show_balance()


# mini project

# class BankAccount:

#     # Class Attribute
#     bank_name = "OpenAI Bank"

#     def __init__(self, account_number, holder_name, balance):
#         self.account_number = account_number
#         self.holder_name = holder_name
        
#         self.__balance = balance

#     def deposit(self, amount):
#         if amount>0:
#             self.__balance += amount
#             print(f"Rs.{amount}/- deposited successfully.")

#     def withdraw(self, amount):
#         if amount <= self.__balance:
#             self.__balance -= amount
#             print(f"Rs.{amount}/- withdrawn successfully.")
#         else:
#             print("Insufficient balance.")

#     def get_balance(self):
#         return self.__balance
    
#     @staticmethod
#     def calculate_interest(balance):
#         return balance * 0.05
    
#     def __str__(self):
#         return f"{self.holder_name} <<->> {self.account_number}"
    
#     def __len__(self):
#         return len(str(self.account_number))



# acc1 = BankAccount(1001, "Rahul", 5000)
# acc2 = BankAccount(1002, "Omkar", 50000)

# print(acc1)
# print(acc2)

# acc1.deposit(10000)
# acc1.withdraw(8000)

# print(f"Current balance: {acc1.get_balance()}")
# print(f"Current balance: {acc2.get_balance()}")

# interest = BankAccount.calculate_interest(acc2.get_balance())
# print(f"Estimated interest: {interest}")