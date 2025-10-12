# Classes and Object 

**GOAL**:
- understand what *class* and *object* are
- Define a class with ``__init__`` and instantce attributes
- Use *method* and `self`
- Know the difference between **class attribute** and **instance attribute**

## 1. Class

- **Class** is a blueprint - define how to build objects
- **Object** (is also called an *instance*) is a specific thing created from that blueprint
```python
class Person: 
	def __init__(self, name, age):
		self.name = name #instance attribute
		self.age = age #instance attribute
	
	def greet(self)
		print(f"hi, my name is{self.name}, and im {self.age} years old")
		
#Create 2 objects

p1 = Person("Alice", 25)
p2 = Person("Bob", 27)

p1.greet()
p2.greet()
```

- `__init__:` is the *constructor* - it runs automatically when a new object is created 
- `self`: refers to the current object
	- Each object (`p1` and `p2`) has it own attributes (`name, age`)
- *object* is made from *class*

## 2. Instance Attributes vs Class Attributes

- We can store data in 2 ways:
	- **Instance attributes**: belong to one object
	- **Class attributes**: shared by all objects in the class 

```python
class Student:
	school = "hcmus" # Class attribute
	
	def __init__(self, name):
		self.name = name # Instance attribute 

s1 = Student("Mai")
s2 = Student("Dang")

print(s1.school) # hcmus
print(s2.school) # hcmus

s1.school = "UIT" #change only for s1
print(s1.school) # UIT
print(s2.school) # hcmus

```

- Class Attribute is **shared** and Instance Attribute is not 

## 3. Method and `Self`

- **Methods** are just *functions inside a class* that describe what objects can do
```python
class Car:
	def __init__(self, brand):
		self.brand = brand
	
	def drive(self):
		print(f"{self.brand} is driving")

car1 = Car("Toyota")
car1.drive()
```

- When you call `car1.drive()` <=> python will run `Car.drive(car1)` 


## 4. Exercises

```python
class Book:
	def __init__(self, title, author, year):
		self.title = title
		self.author = author
		self.year = year
	
	def display_info(self):
		print(f"""Title: {self.title}
			Author: {self.author}
			Year: {self.year}""")

book1 = Book("1984", "George Orwell", 1949)
book1.display_info()

```


```python
class Rectangle:
	def __init__(self, width, height):
		self.width = width
		self.height = height
	
	def area(self):
		return self.width*self.height
	
	def perimeter(self):
		return (self.width+self.height)*2
```