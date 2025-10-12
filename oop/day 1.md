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