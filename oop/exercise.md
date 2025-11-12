
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
		self.is_borrowed = False
	def __str__(self):
		status = "Borrwed" if self.is_borrowed else "Available"
		return f"{self.title} (self.genre) - * {self.rating} | {status}"
		
class LibraryManagement:
	def __init__(self):
		self.books = []
	
	def add_book(self, book):
		self.books.append(book)
	
	def remove_book(self, book):
		for book in self.books:
			if book.title.lower() == title.lower():
				self.books.remove(book)
				print(f"removed book: {title}")
				return 
		print(f"No book found with title '{title}')
	
	def list_books(self):
		if not self.books:
			print("No books in the library")
		else:
			for book in self.books:
				print(book) 
	
	def get_highest_rated_books(self, x):
		sorted_books = sorted(self.books, key=lambda book: (book.rating, book.title), reverse=True)
		return(sorted_books[:x]) 
	
	def recommend_top_book_by_genre(self, genre):
		genre_books = []
		for book in self.books:
			if book.genre == genre:
				genre_books.append(book)
		if genre_books == []
			return None
		sorted_genre_book = sorted(genre_books, key=lambda book: (book.rating)
			return sorted_genre_book[0]
			
	def borrow_book(self, title):
		for book in self.books:
			if book.title.lower() == title.lower() and not book.is_borrowed:
			book.is_borrowed = False
			return book
		return None
```


Chào anh/chị! Wakamono có nhiều sản phẩm chất lượng, nổi bật gồm:
1. 🥢 Măng Wakamono với các vị:
    - Cay nhẹ (phù hợp đa số khẩu vị)
    - Ớt ngâm (cay đậm, thích hợp người mê cay)
    - Không cay (an toàn cho mọi lứa tuổi)
    - Teriyaki (vị ngọt thanh, phá cách)
2. 🍵 Kỳ tử Wakamono:
    - Kỳ tử sạch, nhập khẩu chính ngạch từ Ninh Hạ (Trung Quốc)
    - Không phẩm màu, không chất bảo quản
    - Đóng gói hút chân không, có giấy kiểm định VSATTP
3. 🍄 Đông Trùng Hạ Thảo cao cấp Wakamono:
    - Hộp 5g, dùng pha trà hoặc nấu ăn        
    - Sấy thăng hoa, bảo quản tốt, dùng tiện lợi
4. 🍃 Combo trà thảo dược Đông Trùng Hạ Thảo Wakamono:
    - Combo 2 hộp (thìa canh + xạ đen)
    - Combo 3 hộp (xạ đen + thìa canh + tía tô)
    - Đóng gói 10 gói/hộp, không chất bảo quản
Anh/chị muốn em tư vấn chi tiết sản phẩm nào hoặc gợi ý combo phù hợp không ạ?