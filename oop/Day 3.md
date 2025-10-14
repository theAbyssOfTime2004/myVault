# Inheritance

**GOAL**:
- Understand what *inheritance* is
- Create subclasses that is inherented from its parent class
- understand and being able to use `super()`
- Override parent methods for custom behavior
- Work with multiple inheritance 

## 1. What is inheritance

- Inheritance allows one class *(child/subclass)* to **reuse** and **extend** the functionality of another class *(parent/superclass)*

- Example of basic inheritance:
```python
class Animal:
	def __init__(self, name):
		self.name = name
	
	def speak(self):
		print("Some generic sound...")
		
class Dog(Animal):
	def speak(self):
		print("Woof")

class Cat(Animal):
	def speak(self):
		print("Meow")

dog = Dog("Gấu")
cat = Cat("Chanhh")

dog.speak()
cat.speak()
```

- Dog and Cat both inherit `__init__()` from `Animal`, but override the `speak()` method with their own version

## 2. Using `super()` to access parent methods

- Sometimes a subclass wants to extend (not completely replace) the behaviour of the parent class
```python
class Animal:
	def __init__(self, name):
		self.name = nameiinit
		print("Animal created")

class Dog(Animal):
	def __init__(self, name, breed):
			super().__init__(name) # call parent constructor 
		self.breed = breed
		print("Dog created")

dog = dog("Gấu", "Chó bắc hà")
```

- `super()` is how python lets the child class call methods from parent class (like constructors or overriden methods)

## 3. Method Overriding

- If a sublass defines a method with the *same name* as the parent, python automatically uses the child's version - this is called overriding
```python 
class Vehicle:
	def move(self):
		print("Vehicle is moving...")

class Car(Vehicle):
	def move(self):
		print("Car is driving...")
	
v = Vehicle()
c = Car()

v.move()
c.move()	
```

## 4. Multiple Inheritance

- A class can inherit from **more than one** parent class
```python
class Flyer:
	def fly(self):
		print("Flying high")

class Swimmer:
	def swim(self):
		print("swimming fast")

class Duck(Flyer, Swimmer):
	pass

d = duck()
d.fly()
d.swim()
```


## Exercise

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
    
    def display_info(self):
        print(f"Name: {self.name}, Salary: {self.salary}")


class Manager(Employee):
    def __init__(self, name, salary, department):
        super().__init__(name, salary)
        self.department = department
    
    def display_info(self):
        super().display_info()
        print(f"Department: {self.department}")


e1 = Employee("Dang", 5000)
m1 = Manager("Mai", 8000, "AI Research")

e1.display_info()
m1.display_info()
```

- When a child class inherits from a parent:
	- It automatically **inherits all methods and properties** (including getters and setters).
	- You only need to **override** them if you want to change their logic.

```python
from abc import ABC, abstractmethod
import math

# Abstract Parent Class
class Shape(ABC):
    @abstractmethod
    def area(self):
        pass


# Rectangle subclass
class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


# Circle subclass
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

rect = Rectangle(5, 10)
circle = Circle(7)

print(f"Rectangle area: {rect.area()}")
print(f"Circle area: {circle.area():.2f}")

```