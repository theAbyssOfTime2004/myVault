
### Problem: Library Management System

You are tasked with implementing two classes to manage a library's book inventory.

#### 1. `Book` Class
This class represents a single book and should have the following attributes:
- **`title`** (string): The title of the book.
- **`genre`** (string): The genre of the book.
- **`rating`** (float): The customer rating of the book.

#### 2. `LibraryManagement` Class
This class manages the collection of books and should have the following methods:
- **`add_book(book)`**: Adds a new `Book` object to the inventory.
- **`get_highest_rated_books(x)`**: Returns a list of the top `x` highest-rated books. The list must be sorted by rating in descending order. If two books have the same rating, they should be sorted by their title in descending order.
- **`recommend_top_book_by_genre(genre)`**: Returns the single highest-rated book for a specified genre. If no books exist in that genre, it should return `None`.

#### Constraints
- The number of recommended books requested will be less than or equal to the total number of books in the library.

*Note: The code for reading input, calling these methods, and producing the final output is already provided.*


```python
class Book:
	def __init__(self, title, genre, rating):
		self.title = title
		self.genre = genre
		self.rating = rating
		
		
@dataclass
	class LibraryManagement:
		
```