# 📅 Ngày 2025-08-09

## 🎯 Kế hoạch hôm nay
- [ ] Học lý thuyết: `hashmap: dict, set cơ bản`
- [ ] Làm bài:
  - [ ] ...

## 🕒 Thời gian thực hành
- Bắt đầu: ...
- Kết thúc: ...

## 🧠 Ghi chú nhanh
- Micro-cheat sheet for today 
```python 
# duyệt mảng kèm index
nusms = [5, 8, 10]
for i, x in enumerate(nums):
	print(i, x)

# dict cơ bản: tra cứu & gán 
seen = {}
seen['a'] = 1 # gán key -> value
print(seen['a']) # lấy value
print('a' in seen) # true

#set cơ bản: phát hiện trùng
s = set()
s.add(10)
print(10 in s) # True

# in debug nhanh
print(f"{i}, {x=})

# đếm ký tự (hôm sau dùng cho Anagram)
from collections import Counter
Counter("aabcc") # {'a':2, 'b':1, 'c':2}
```

### Bài Two-Sum
- 2 vòng lặp: 
```python
def twoSum(self, nums, target):
	"""
	:type nums: List[int]
	:type target: int
	:rtype: List[int]
	"""
	seen = {}
	for i, x in enumerate(nums):
		seenp[x] = i

	for i, x in enumerate(nums):
		need = target - x 
		if need in seen and seen[need] != i:
			return[i, seen[need]]
	return None
```

- 1 vòng lặp: 
```python
def twoSum(self, nums, target):
	seen {}
	for i, x in enumerate(nums):
		need = target - x 
		if need in seen: 
			return[seen[need], i]
		seen[x] = i
	return None
```