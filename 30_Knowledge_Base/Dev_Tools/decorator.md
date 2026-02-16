Chắc chắn rồi, đây là phiên bản hoàn chỉnh cho note của bạn, bổ sung các khái niệm và ví dụ để làm rõ hơn.

---

2025-11-17 00:03

Tags: [[FSDS]], [[High Performance Python]]

# Decorator, Context Manager và High-Order Function

## 1. Nền tảng: Functions as First-Class Citizens

Trước khi đi vào chi tiết, cần hiểu một khái niệm cốt lõi trong Python: **Hàm là công dân hạng nhất (Functions are first-class citizens)**. Điều này có nghĩa là hàm có thể được đối xử như mọi đối tượng khác:
- Gán cho một biến.
- Truyền vào một hàm khác như một đối số.
- Được trả về từ một hàm khác.

Đây chính là nền tảng cho cả ba khái niệm dưới đây.


## 2. High-Order Function (Hàm bậc cao)

**Định nghĩa:** Một hàm bậc cao là một hàm thỏa mãn ít nhất một trong các điều kiện sau:
- Nhận một hoặc nhiều hàm khác làm đối số.
- Trả về một hàm khác làm kết quả.

Các hàm như `map()`, `filter()` là ví dụ kinh điển. Tuy nhiên, ứng dụng mạnh mẽ nhất của nó chính là tạo ra các **decorator**.


## 3. Decorator

### Mục tiêu

Mục tiêu chính của decorator là để **mở rộng chức năng của một hàm mà không cần phải chỉnh sửa hay thay đổi code gốc của hàm đó**.

### Cấu trúc cơ bản

Về bản chất, decorator là một hàm nhận một hàm khác làm đối số, thêm một số chức năng và trả về một hàm mới.

```python
def my_decorator(func):
    # `wrapper` là hàm sẽ "bọc" hàm gốc
    def wrapper(*args, **kwargs):
        print("Có gì đó xảy ra TRƯỚC khi hàm được gọi.")
        result = func(*args, **kwargs) # Gọi hàm gốc
        print("Có gì đó xảy ra SAU khi hàm được gọi.")
        return result
    return wrapper
```

### Cú pháp `@`

Để sử dụng decorator, ta dùng cú pháp `@` đặt ngay trên định nghĩa hàm.

```python
@my_decorator
def say_hello():
    print("Hello!")

say_hello()
```

Dòng `@my_decorator` chỉ là một cách viết gọn (syntactic sugar) cho:
`say_hello = my_decorator(say_hello)`

### Tầm quan trọng của `functools.wraps`

Khi sử dụng decorator, hàm được "bọc" sẽ mất đi các thông tin metadata gốc (như tên hàm `__name__`, docstring `__doc__`). Để giải quyết vấn đề này, ta dùng decorator `@wraps` từ thư viện `functools`.

```python
import functools

def my_decorator(func):
    @functools.wraps(func) # Giữ lại metadata của hàm gốc
    def wrapper(*args, **kwargs):
        # ...
        return func(*args, **kwargs)
    return wrapper
```

### Stacked Decorators (Decorator lồng nhau)

Ta có thể áp dụng nhiều decorator cho cùng một hàm.

![[Pasted image 20251117000636.png]]

Thứ tự áp dụng sẽ đi **từ trong ra ngoài** (từ dưới lên trên khi đọc code). Đoạn code trên tương đương với:

`predict = timer(lru_cache(predict))`

Nghĩa là, hàm `predict` được bọc bởi `lru_cache` trước, sau đó kết quả đó lại được bọc tiếp bởi `timer`.

---

## 4. Context Manager

### Mục tiêu

Context Manager được dùng để **quản lý tài nguyên** (như file, kết nối mạng, database) một cách hiệu quả. Nó đảm bảo rằng các hành động thiết lập (setup) và dọn dẹp (teardown) luôn được thực thi, ngay cả khi có lỗi xảy ra trong quá trình xử lý.

### Cú pháp `with`

Cách phổ biến nhất để sử dụng Context Manager là thông qua câu lệnh `with`.

```python
with open('some_file.txt', 'w') as f:
    f.write('Hello, world!')
# Khi khối `with` kết thúc, file sẽ tự động được đóng (f.close() được gọi)
```

### Cách tạo một Context Manager

Có hai cách chính:

**a. Dùng Class:**
Tạo một class có hai phương thức đặc biệt là `__enter__` (thiết lập) và `__exit__` (dọn dẹp).

**b. Dùng `contextlib` (Khuyến khích):**
Đây là cách đơn giản và "Pythonic" hơn, sử dụng decorator `@contextmanager`.

```python
from contextlib import contextmanager

@contextmanager
def managed_file(name):
    try:
        f = open(name, 'w')
        yield f # Giá trị này sẽ được gán cho biến sau `as`
    finally:
        # Phần dọn dẹp luôn được thực thi
        f.close()
        print("File đã được đóng.")

with managed_file('hello.txt') as f:
    f.write('hello, world!')
```

---

## 5. Mối liên hệ

- Cả ba khái niệm đều được xây dựng dựa trên nguyên tắc **Functions are first-class citizens** của Python.
- **Decorator** là một ứng dụng thực tế và phổ biến của **High-Order Function**.
- **Context Manager** có thể được tạo ra một cách thanh lịch bằng cách sử dụng decorator (`@contextmanager`), cho thấy sự giao thoa mạnh mẽ giữa các khái niệm này.

# References