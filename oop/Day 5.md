# Abstraction 

**GOAL**:
- Understand what abstraction really means
- Use Python's `abc` module to create abstract classes and methods 
- Combine abstraction with inheritance and polymorphism
- Design flexible, scalable class architecture
## 1. What is abstraction

- **Abstraction** means *showing only the essential features of an object while hiding unnecessary details*
- In simpler words: 
	- The user should focus on what an object does not how it does 
## 2. Abstraction in Python

- Python supports abstraction through the `abc` module (**Abstract base class**)
- This allow you to define a **template** that subclasses must follow
- Example:
```python
from abc import ABC, abstractmethod

class Vehicle(ABC)
	@abstractmethod
	def strat_engine(self)
		pass
	
	@abstractmethod
	def stop_engine(self)
		pass
		
class Car(Vehicle)
	def start_engine(self)
		print("Car engine started")

	def stop_engine(self)
		print("Car engine stopped")

class Motorcycle(Vehicle)
	def start_engine(self):
		print("Motorcycle engine started")
	
	def stop_engine(self):
		print("Motorcycle engine stopped")
		
		
# You can’t instantiate Vehicle directly:
# v = Vehicle() ❌ TypeError

for v in [Car(), Motorcycle()]:
    v.start_engine()
    v.stop_engine()
```

## 3.  Abstraction + Polymorphism

- Abstract class defines a **shared interface**, you can easily combine them with polymorphism
- Example: Shape system
```python
from abc import ABC, abstractmethod
import math

class Shape(ABC):
	@abstractmethod
	def area(self):
		pass

class Circle(Shape):
	def __init__(self, radius):
		self
```