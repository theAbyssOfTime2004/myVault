2025-07-18 23:32

[[30 Days of Pandas - Leetcode]], [[beginner]]
Tags:

# Days 1 - 30 Days of Pandas

### 595. Big countries
```python
	import pandas as pd
 
def big_countries(world: pd.DataFrame) -> pd.DataFrame:
	return world[(world["area"] >= 3000000) | (world["population"]>= 25000000)][["name", "population", "area"]]
```

### 1757. Recyclable and Low Fat Products 
```python
import pandas as pd

def find_products(products: pd.DataFrame) -> pd.DataFrame:

	return products[(products["low_fats"] == "Y") & (products["recyclable"] == "Y")][["product_id"]]
```

### 183. Customers Who Never Order
```python
import pandas as pd


def find_customers(customers: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:

	no_orders = customers[~customers["id"].isin(orders["customerId"])]
	return no_orders.rename(columns={"name": "Customers"})[["Customers"]]
```
- A faster way to approach: 
```python
def find_customers(customers: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    no_orders = customers[~customers["id"].isin(orders["customerId"])]
    return no_orders.rename(columns={"name": "Customers"})[["Customers"]]

```

### 1148. Article Views I 
```python 
import pandas as pd

def article_views(views: pd.DataFrame) -> pd.DataFrame:
    # Lọc các dòng có author_id = viewer_id (tác giả xem bài viết của chính mình)
    result_df = views[views["author_id"] == views["viewer_id"]]
    
    # Đổi tên cột author_id thành id
    result_df = result_df.rename(columns={"author_id": "id"})
    
    # Loại bỏ duplicate và chỉ giữ lại cột id
    result_df = result_df[["id"]].drop_duplicates()
    
    return result_df.sort_values("id", ascending=True)
    
```

- A faster way to approach: 
```python
import pandas as pd

def article_views(views: pd.DataFrame) -> pd.DataFrame:
mask = views["author_id"].values == views["viewer_id"].values
unique_ids = np.unique(views.loc[mask, "author_id"].values)
return pd.DataFrame({"id": unique_ids})
```

# References
