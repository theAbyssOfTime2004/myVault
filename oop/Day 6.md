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
- (optionally) 