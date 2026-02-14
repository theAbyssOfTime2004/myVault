# Special Methods and Dataclasses

**GOAL**: Understand 
- What special methods are
- How to implement common one (`__str__`, `__repr__`, `__eq__`, `__len__`, `__add__`)
- How `@dataclass` can automately generate these methods
- How to combine both to write elegant, maintainable classes

## 1. What are special/dunder methods?

- They're **built-in hooks** that makes your class compatible with Python's Syntax and built-in operations
```python
for example:
__init__: #constructor (called when creating an object)
__str__: #defines how the object is print
__len__: #let you use len(obj)
__eq__: #allows obj1 == obj2
__add__: #define behavior for obj1 + obj2
```

- example 1: `__repr__` and `__str__`
```python 
class Book: 
	def __init__(self, title, author):
		self.title = title
		self.author = author
	
	def __repr__(self):
		return f"Book({self.title!r}, {self.author!r})"
		
	def __str__(self):
			return f"'{self.title}' by {self.author}"

b = book("1984", "George Orwell")

print(b)
print(repr(b))
```

- Output: 
```css
'1984' by George Orwell
Book('1984', 'George Orwell') 
```

- example 2: `__len__` and `__eq__`
```python
class Team:
	def __init__(self, name, members):
		self.name = name
		self.members = members
	
	def __len__(self)
		return len(self.members)
	
	def __eq__(self)
			return self.name == other.name and self.members == other.members
	
t1 = Team("Avengers", ["Iron Man", "Thor"])
t2 = Team("Avengers", ["Iron Man", "Thor"])

print(len(t1))       # 2
print(t1 == t2)      # True

```

- example 3: `__add__`
```python
class Vector:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	def __add__(self, other):
		return Vector(self.x + other.x, self.y + other.y)
	
	def __repr__(self):
		return f"Vector({self.x}, {self.y})"
	
v1 = Vector(1, 3)
v2 = Vector(2, 4)
print(v1 + v2) #Vector(3, 7)
```

## 2. Simplify with `@dataclass`

`@dataclass` automatically generate:
- `__init__`
- `__repr__`
- `__eq__`
- (optionally) ordering methods (`<`, `>`, etc.)
```python
from dataclasses import dataclass

@dataclass
class student:
	name: str
	age: int
	gpa: float

s1 = student(Mai, 20, 3.5)
s2 = student(Mai, 20, 3.5)

	print(s1) # Student(name='Mai', age=21, gpa=3.5)
	print(s1==s2) #true
```

- Can even add methods
```python
@dataclass
class Rectangle:
	width: float
	height: float
	
	def area(self)
		return self.width * self.height
		

r = Rectangle(5, 10)
print(r)
print(r.area())
```


|Feature|Purpose|Example|
|---|---|---|
|`__str__`|readable string|`print(obj)`|
|`__repr__`|debug representation|`repr(obj)`|
|`__eq__`|equality comparison|`obj1 == obj2`|
|`__len__`|length of container|`len(obj)`|
|`__add__`|addition operator|`obj1 + obj2`|
|`@dataclass`|auto-generate methods|`@dataclass class Student:`|

## 3. Exercise

```python
class Product:
	def __init__(self, name, price):
		self.name = name
		self.price = price
	
	def __str__(self):
		return f"{self.name}: {self.price}"
		
	def __eq__(self, other):
		return self.name == other.name and self.price == other.price
	
	def __add__(self, other):
		return self.price + other.price
		
```

```python
from dataclasses import dataclass

@dataclass
class Product:
	name: str
	price: int

	def discount(self, percent):
		return self.price - (self.price*percent/100)
```