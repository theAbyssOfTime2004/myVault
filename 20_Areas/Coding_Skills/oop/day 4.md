# Polymorphism

**GOALS**:
- Understand what polymorphism is and why it matters
- The two types of polymorphism: *method overriding* and *method overloading*
- How python uses *duck typing* for flexible behavior 
- How to apply polymorphism in real scenarios 

## 1. What is polymorphism

- You can call the same method (for example: `speak(), area(), draw()`) on different classes - and each one does something unique

```python
# Classic polymorphism example

class Dog:
	def speak(self):
		return "woof"

class Cat:
	def speak(self):
		return "Meow"

class Duck:
	def speak(self):
		return "Quack"

animals = [Dog(), Cat(), Duck()]
	
for a in animals:
	print(a.speak())
```

- Every object has a `speak()` method - Python doesn't care what type it is, just calls the method

## 2. Polymorphism with Inheritance (method overriding)

- Polymorphism often happens when a child class try to override a method from its parent class
```python
class Shape:
	def area(self):
		pass

class Rectangle(Shape):
	def __init__(self, width, height):
		self.width = width 
		self.height = height
	
	
	def area(self):
		return self.width * self.height
	
class Circle(shape):
	def __init__(self, radius):
		self.radius = radius 
	
	def area(self):
		import math
		return math.pi * self.radius

shapes = [Rectangle(4, 6), Circle(3)]

for shape in shapes:
    print(shape.area())

```

## 3. Duck Typing - Python's Dynamic Polymorphism

- Python doesn't care about Inheritance as long as the method exists:
	- *If it walks like a duck and quacks like a duck then its a duck*
```python
class Bird:
	def fly(self):
		print("Bird is flying")

class Airplane:
	def fly(self):
		print("Airplan is flying")

class Rocket:
	def fly(self):
		print("Rocket is flying")
		

for obj in [Bird(), Airplane(), Rocket()]:
    obj.fly()  # Works for all
```

- No need for a shared parent class - as long as `.fly()` exists. Python runs it. This is **duck typing**

## 4. "Overloading" in Python 

- Python doesn't allow true method overloading (same name, different params)
- Instead, you can use **default arguments** or `*args` to simulate it
```python
class MathTool:
	def add(self, a, b=0, c=0):
		return a+b+c

m = MathTool()
print(m.add(5))
print(m.add(5, 3))
print(m.add(5, 3, 2))
```

## Exercise 

```python
class Payment:
	def process_payment(self):
		pass

class CreditCardPayment:
	def process_payment(self):
		print("Processing credit card payment...")

class PaypalPayment:
	def process_payment(self):
		print("Processing PayPal payment...")

class CryptoPayment:
	def process_payment(self):
		print("Processing crypto payment...")
		
for p in [CreditCardPayment(), PaypalPayment(), CryptoPayment()]:
	p.process_payment()
```


```python
class Car:
	def move(self):
		print("the car is moving on the road")

class Airplane:
	def move(self):
		print("the plane is flying on the sky")
	
class Boat:
	def move(self):
		print("the boat is surfing on the river")

for vehicle in [Car(), Airplane(), Boat()]:
	vehicle.move()
```