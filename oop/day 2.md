# Encapsulation

**GOAL**: must understand:
- What encapsulation means and why it matters
- The difference between *public*, *protected* and *private* attributes
- How to use *getter/setter* methods
- how to use `@property` decorator to make code cleaner

## 1. Encapsulation

- Encapsulation = *hiding data inside an object and controlling what access to it*
=> To **keep internal details private**, and provide methods for **safe access or modification**

```python
class BankAccount:
	def __init__(self, owner, balance):
		self.owner = owner
		self.__balance = balance # private attribute
	
	def deposit(self, amount):
		if amount > 0:
			self.__balance += amount
		else: 
			print("deposit amount must be positive")
	
	def withdraw(self, amount): 
		if 0 < amount <= self.__balance:
			self.__balance -= amount
		else:
			print("Invalid withdrawal amount")
			
	def get_balance(self):
		return self.__balance
	
acc = BankAccount("Dang", 1000)
acc.deposit(500)

print(get_balance()) # works

print(acc.__balance) # AttributeError (cannot access directly)


# another example:

class Student:
	def __init__(sellf, name, grade):
		self.name = name # public
		self._grade = grade # protected
		self.__id = 12345 # private

```

## 2. Getter/Setter methods

- Sometimes you want to control how data is modified - for example, to prevent invalid values
```python
class Person:
	def __init__(self, name, age):
		self. name = name
		self.__age = age
	
	def get_age(self):
		return self.__age
	
	def set_age(self, new_age):
		if new_age >= 0:
			self.__age = new_age
		else:
			print("Age cannot be negative")
	

p = person("Mai", 21)
print(p.get_age())
p._set_age(-5)
p.set_age(20)
```

## 3. Cleaner way using `@property`

- Python give a more elegant way to define getters and setters using **decorators**
```python
class Employee:
	def __init__(self, name, salary):
		self.name = name 
		self.__salary = salary
	
	@property
	def salary(self):
		return self.__salary
	
	@salary.setter
	def salary(self, value):
		if value >= 0:
			self.__salary = value
		else:
			print("Salary must be non-negative")
	
	e = Employee("Dang", 5000)
	print(e.salary) # calls the getter
	e.salary  = 6000 # calls the setter
	e.salary = -10 # invalid value
```

## 4. Exercise

```python
class BankAccount:
	def __init__(self, owner, balance):
		self.owner = owner
		self.__balance = balance
	
	@property
	def balance(self):
		return self.__balance
	
	@balance.setter
	def balance(self, value):
		if value >= 0:
			self.__balance = value
		else:
			print("balance must be non-negative")
	
	def deposit(self, amount):
		if amount > 0:
			self.__balance += amount
		else: 
			print("deposit amount must be positive")
	
	def withdraw(self, amount): 
		if 0 < amount <= self.__balance:
			self.__balance -= amount
		else:
			print("Invalid withdrawal amount")
	
	acc = BankAccount("Dang", 1000)
	print(acc.balance)
	acc.balance = 2000
		
```


```python
class Temperature:
	def __init__(self, )
```