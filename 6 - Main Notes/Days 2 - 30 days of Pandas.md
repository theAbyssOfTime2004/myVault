2025-07-21 23:38


Tags: [[30 Days of Pandas - Leetcode]]

# Days 2 - 30 days of Pandas

### 1683. Invalid Tweets
```python
import pandas as pd

def invalid_tweets(tweets: pd.Dataframe)
-> pd.Dataframe
	return tweets[tweets["content"].str.len() > 15][["tweets_id"]]
```

- faster approach:
```python
df.loc[df["content"].str.len() > 15, "tweet_id"]
```
- It avoids creating a temporary full df like `[["tweets_id]]` 
- `df.loc[<conditions>, <columns>]`, in this case `df["contents"].str.len() > 15` is a boolean mask which will return `1` or `0` according to the condition, and willl return the corresponding `tweet_id`

### 1873. Calculate Special Bonus

```python
import pandas as pd

def calculate_special_bonus(df: pd.Dataframe)
-> pd.Dataframe
	condition = (df[employee_id] % 2 == 0) & (~df["name"].str.startswith("M"))
	df["bonus"] = np.where(condition, df["salary"], 0)
	return df[["employee_id", "bonus"]].sort_values[["employee_id"]] 
```

### 1667. Fix Names in a Table

```python
import pandas as pd

def fix_names(users: pd.Dataframe)
-> pd.Dataframe
	users["name"] = users["name"].str.capitalize()
	users = users.sort_values(by="user_id")
return users[["user_id", "name"]]
```
- method `.str.capitalize` to uppercase the first letter and lowercase the rest
# References
